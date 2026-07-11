from typing import TypedDict

class TaskAgentState(TypedDict):
    mensagem_usuario: str
    historico: list[str]
    intencao: str
    parametros: dict
    clareza: bool
    duvida: str
    resposta_api: dict
    resposta_final: str