"""Grafo jerárquico: supervisor enruta, especialistas aportan y se valida antes del cierre."""

from __future__ import annotations

from typing import Literal

from langgraph.graph import END, START, StateGraph

from agents.analyst_agent import analyst_node
from agents.research_agent import research_node
from state import OrchestratorState


def supervisor_node(state: OrchestratorState) -> dict:
    """Router con criterio de suficiencia y límite de pasos contra ciclos infinitos."""
    if state["steps"] >= state["max_steps"]:
        next_agent = "synthesizer"
    elif not state.get("research_results"):
        next_agent = "researcher"
    elif not state.get("analysis"):
        next_agent = "analyst"
    elif not state.get("validation"):
        next_agent = "validator"
    elif state["validation"].get("approved"):
        next_agent = "synthesizer"
    else:
        next_agent = "researcher"
    return {"next_agent": next_agent}


def route_from_supervisor(state: OrchestratorState) -> Literal["researcher", "analyst", "validator", "synthesizer"]:
    return state["next_agent"]  # type: ignore[return-value]


def validator_node(state: OrchestratorState) -> dict:
    """Rúbrica: hay fuentes, análisis y un resultado interpretable."""
    analysis = state.get("analysis", {})
    approved = bool(state.get("research_results")) and "label" in analysis and "score" in analysis
    validation = {"approved": approved, "reason": "Fuentes y análisis disponibles." if approved else "Falta investigación o análisis."}
    return {"validation": validation, "contributions": [{"agent": "validator", "summary": validation["reason"]}], "steps": state["steps"] + 1}


def synthesizer_node(state: OrchestratorState) -> dict:
    sources = ", ".join(item["title"] for item in state.get("research_results", [])) or "sin fuentes"
    analysis = state.get("analysis", {})
    answer = (
        f"Investigación: se consultaron {sources}. "
        f"Análisis: sentimiento {analysis.get('label', 'no disponible')} "
        f"con puntaje {analysis.get('score', 'no disponible')}. "
        "Conclusión: se valora la velocidad y usabilidad; conviene priorizar reintegros, facturación y métodos de pago."
    )
    return {"final_answer": answer, "contributions": [{"agent": "synthesizer", "summary": "Respuesta final integrada."}]}


def build_graph():
    graph = StateGraph(OrchestratorState)
    graph.add_node("supervisor", supervisor_node)
    graph.add_node("researcher", research_node)
    graph.add_node("analyst", analyst_node)
    graph.add_node("validator", validator_node)
    graph.add_node("synthesizer", synthesizer_node)
    graph.add_edge(START, "supervisor")
    graph.add_conditional_edges("supervisor", route_from_supervisor)
    for node in ("researcher", "analyst", "validator"):
        graph.add_edge(node, "supervisor")
    graph.add_edge("synthesizer", END)
    return graph.compile()
