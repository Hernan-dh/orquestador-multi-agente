"""Estado compartido del orquestador."""

from __future__ import annotations

from operator import add
from typing import Annotated, Literal, TypedDict

from langgraph.graph import MessagesState


AgentName = Literal["researcher", "analyst", "validator", "synthesizer", "END"]


class OrchestratorState(MessagesState):
    """Estado estructurado que conserva los aportes de cada especialista."""

    question: str
    next_agent: AgentName
    research_results: list[dict[str, str]]
    analysis: dict[str, object]
    validation: dict[str, object]
    final_answer: str
    contributions: Annotated[list[dict[str, str]], add]
    steps: int
    max_steps: int
