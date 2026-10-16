"""Ejecuta una demostración del flujo de delegación."""

from graph import build_graph


if __name__ == "__main__":
    app = build_graph()
    result = app.invoke({
        "question": "¿Qué opinan los clientes del servicio y qué deberíamos mejorar?",
        "research_results": [], "analysis": {}, "validation": {}, "final_answer": "",
        "contributions": [], "steps": 0, "max_steps": 6,
    })
    print(result["final_answer"])
    print("\nTrazabilidad:")
    for contribution in result["contributions"]:
        print(f"- {contribution['agent']}: {contribution['summary']}")
