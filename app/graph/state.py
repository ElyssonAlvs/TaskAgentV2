from typing import TypedDict, Any

class TaskAgentState(TypedDict):
    mensagem_usuario: str
    historico: list[str]
    intencao: str
    parametros: dict
    clareza: bool
    duvida: str
    resposta_api: Any
    resposta_final: str