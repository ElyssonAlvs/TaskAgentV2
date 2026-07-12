from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel
from crew.crew import executar_crew

app = FastAPI()

# Histórico em memória por sessão simples
historico_sessao: list[str] = []

class MensagemRequest(BaseModel):
    mensagem: str

@app.post("/chat")
def chat(request: MensagemRequest):
    global historico_sessao

    # Executa o CrewAI tratando possíveis falhas/limites de requisição
    try:
        resultado = executar_crew(request.mensagem, historico_sessao)
        resposta_final = str(resultado)
    except Exception as e:
        print(f"Erro na execução do CrewAI: {e}")
        resposta_final = (
            "Desculpe, o servidor de inteligência artificial (Groq) atingiu o limite de requisições temporariamente. "
            "Por favor, aguarde alguns segundos e tente novamente.\n\n"
            "*(Nota: A operação que você solicitou pode ter sido realizada com sucesso no banco de dados, pois o erro ocorreu no processamento final da resposta).* "
        )

    # Atualiza histórico da sessão
    historico_sessao.append(f"Usuário: {request.mensagem}")
    historico_sessao.append(f"Agente: {resposta_final}")

    # Formata pensamento do agente para exibir na UI
    pensamento = [
        "🤖 Processado por: CrewAI (Multi-Agentes)", 
        "👥 Papéis envolvidos: Interpretador, Executor, Formatador"
    ]

    return {
        "pensamento": pensamento,
        "resposta": resposta_final,
        "tasks": None
    }

@app.delete("/chat/historico")
def limpar_historico():
    global historico_sessao
    historico_sessao = []
    return {"status": "histórico limpo"}

# Serve o frontend
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def index():
    with open("static/index.html", "r", encoding="utf-8") as f:
        html = f.read()
    return HTMLResponse(content=html, headers={
        "Cache-Control": "no-cache, no-store, must-revalidate",
        "Pragma": "no-cache",
        "Expires": "0"
    })