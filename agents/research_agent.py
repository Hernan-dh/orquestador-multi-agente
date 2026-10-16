"""Especialista de búsqueda sobre un corpus local simulado."""

from __future__ import annotations

from langchain_core.tools import tool


SOURCES = [
    {
        "title": "Informe de soporte - marzo",
        "text": "Los clientes destacan la rapidez de respuesta y la atención amable. Algunos reportan demoras en reintegros.",
    },
    {
        "title": "Encuesta posventa",
        "text": "La aplicación es intuitiva y estable. La mayoría pide más métodos de pago y notificaciones claras.",
    },
    {
        "title": "Reseñas de producto",
        "text": "El servicio resolvió mi problema rápido. Hubo quejas aisladas por errores al facturar.",
    },
]


@tool
def search_local_sources(query: str) -> list[dict[str, str]]:
    """Busca fuentes del corpus local por palabras de la consulta."""
    terms = {word.lower().strip(".,¿?¡!") for word in query.split() if len(word) > 3}
    matches = [source for source in SOURCES if terms & set(source["text"].lower().split())]
    return matches or SOURCES


def research_node(state: dict) -> dict:
    results = search_local_sources.invoke({"query": state["question"]})
    return {
        "research_results": results,
        "contributions": [
            {"agent": "researcher", "summary": f"Se recuperaron {len(results)} fuentes locales."}
        ],
        "steps": state["steps"] + 1,
    }
