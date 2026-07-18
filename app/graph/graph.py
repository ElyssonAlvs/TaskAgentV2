from langgraph.graph import StateGraph, END
from app.graph.state import TaskAgentState
from app.graph.nodes import (
    interpretar_intencao,
    pedir_clarificacao,
    executar_task,
    confirmar_resultado
)

def deve_clarificar_ou_executar(state: TaskAgentState) -> str:
    if state["clareza"]:
        return "executar"
    return "clarificar"

def construir_grafo():
    grafo = StateGraph(TaskAgentState)

    grafo.add_node("interpretar", interpretar_intencao)
    grafo.add_node("clarificar", pedir_clarificacao)
    grafo.add_node("executar", executar_task)
    grafo.add_node("confirmar", confirmar_resultado)

    grafo.set_entry_point("interpretar")

    grafo.add_conditional_edges(
        "interpretar",
        deve_clarificar_ou_executar,
        {"executar": "executar", "clarificar": "clarificar"}
    )

    grafo.add_edge("clarificar", END)  # Retorna a dúvida para o frontend
    grafo.add_edge("executar", "confirmar")
    grafo.add_edge("confirmar", END)

    return grafo.compile()