from crewai import Task
from crew.agents import interpretador, executor, formatador

def criar_tasks(mensagem: str, historico: str):

    task_interpretar = Task(
        description=f"""Analise a mensagem do usuário e o histórico da conversa.
        
        Histórico:
        {historico}
        
        Mensagem atual: {mensagem}
        
        Extraia e retorne em formato JSON:
        - intencao: criar | listar | atualizar | deletar
        - parametros: id, titulo, status (null se não informado)
        - clareza: true se tem tudo necessário para executar, false caso contrário
        - duvida: pergunta para o usuário se clareza for false""",
        expected_output="JSON com intencao, parametros, clareza e duvida",
        agent=interpretador
    )

    task_executar = Task(
        description="""Com base na interpretação anterior, execute a operação
        correspondente na API REST em http://localhost:8000.
        
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
        description="""Com base no resultado da execução anterior, formate
        uma resposta clara e amigável em português para o usuário.
        
        Regras:
        - Para listagem: apresente as tasks de forma organizada com ID, título e status
        - Para criação: confirme com o título e ID gerado
        - Para atualização/deleção: confirme o que foi feito
        - Para erros: explique o problema de forma simples
        - Para dúvidas: faça a pergunta de forma natural e conversacional""",
        expected_output="Mensagem final formatada para o usuário em português",
        agent=formatador
    )

    return [task_interpretar, task_executar, task_formatar]
