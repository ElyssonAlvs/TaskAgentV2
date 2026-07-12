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

    # Executa o CrewAI
    resultado = executar_crew(request.mensagem, historico_sessao)

    # Atualiza histórico da sessão
    historico_sessao.append(f"Usuário: {request.mensagem}")
    historico_sessao.append(f"Agente: {resultado}")

    # Formata pensamento do agente para exibir na UI
    pensamento = [
        "🤖 Processado por: CrewAI (Multi-Agentes)", 
        "👥 Papéis envolvidos: Interpretador, Executor, Formatador"
    ]

    return {
        "pensamento": pensamento,
        "resposta": str(resultado),
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