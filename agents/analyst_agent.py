"""Especialista de análisis y cómputo de sentimiento."""

from __future__ import annotations

from langchain_core.tools import tool


POSITIVE = {"rapidez", "amable", "intuitiva", "estable", "resolvió", "rápido", "claras"}
NEGATIVE = {"demoras", "errores", "quejas", "problema"}


@tool
def sentiment_score(text: str) -> dict[str, object]:
    """Calcula un sentimiento simple y reproducible para el texto dado."""
    tokens = {word.strip(".,;:").lower() for word in text.split()}
    positive = len(tokens & POSITIVE)
    negative = len(tokens & NEGATIVE)
    score = positive - negative
    label = "positivo" if score > 0 else "negativo" if score < 0 else "neutral"
    return {"label": label, "score": score, "positive_terms": positive, "negative_terms": negative}


def analyst_node(state: dict) -> dict:
    text = " ".join(item["text"] for item in state["research_results"])
    analysis = sentiment_score.invoke({"text": text})
    return {
        "analysis": analysis,
        "contributions": [{"agent": "analyst", "summary": f"Sentimiento {analysis['label']} (score {analysis['score']})."}],
        "steps": state["steps"] + 1,
    }
