from typing import Optional, Dict, Any, Annotated
from pydantic import BaseModel, Field, BeforeValidator
from crewai import Task
from crew.agents import interpretador, executor, formatador

def coerce_bool(v: Any) -> bool:
    if isinstance(v, str):
        return v.lower() in ('true', '1')
    return bool(v)

class IntencaoSchema(BaseModel):
    intencao: str = Field(description="Intenção identificada: criar | listar | atualizar | deletar")
    parametros: Dict[str, Any] = Field(description="Parâmetros extraídos da mensagem (id, titulo, status). Chaves devem estar presentes, use null se não informados.")
    clareza: str = Field(description="Escreva 'true' se tem tudo necessário para executar a ação, 'false' caso contrário")
    duvida: Optional[str] = Field(None, description="Pergunta para o usuário se clareza for false, senão null ou string vazia")

def criar_tasks(mensagem: str, historico: str):

    task_interpretar = Task(
        description=f"""Analise a mensagem do usuário e o histórico da conversa.
        
        Histórico:
        {historico}
        
        Mensagem atual: {mensagem}
        
        Extraia e retorne os campos definidos no output_json.""",
        expected_output="Objeto JSON contendo intencao, parametros, clareza e duvida",
        agent=interpretador,
        output_json=IntencaoSchema
    )

    task_executar = Task(
        description="""Com base na interpretação anterior, execute a operação
        correspondente na API REST em http://127.0.0.1:8000
        
        Endpoints disponíveis:
        - GET /tasks/  listar todas
        - POST /tasks/  criar (body: {"titulo": "..."})
        - PUT /tasks/{id}  atualizar (body: {"titulo": "...", "status": "..."})
        - DELETE /tasks/{id}  deletar
        
        Se a intenção não estiver clara (clareza: false), não execute nada
        e retorne a dúvida para o usuário.
        
        Retorne o resultado da API ou a mensagem de erro.""",
        expected_output="Resultado da operação na API ou mensagem de erro",
        agent=executor
    )

    task_formatar = Task(
        description=f"""Com base no resultado da execução anterior e no histórico da conversa, formate
        uma resposta clara e amigável em português para o usuário.
        
        Histórico:
        {historico}
        
        Regras:
        - Para listagem: apresente as tasks de forma organizada com ID, título e status
        - Para criação: confirme com o título e ID gerado
        - Para atualização/deleção: confirme o que foi feito
        - Para erros: explique o problema de forma simples
        - Para dúvidas: se a dúvida já foi respondida ou pode ser inferida pelo histórico, responda diretamente. Caso contrário, faça a pergunta de forma natural e conversacional""",
        expected_output="Mensagem final formatada para o usuário em português",
        agent=formatador
    )

    return [task_interpretar, task_executar, task_formatar]
