import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

load_dotenv()

app = FastAPI()

# Histórico em memória por sessão simples
historico_sessao: list[str] = []

# ──────────────────────────────────────────────────────────────────
# Motor de execução selecionável via variável de ambiente
# AGENT_ENGINE=crewai  → equipe multiagente com CrewAI  (padrão)
# AGENT_ENGINE=langgraph → grafo de estado com LangGraph (legado)
# ──────────────────────────────────────────────────────────────────
ENGINE = os.getenv("AGENT_ENGINE", "crewai").lower()

class MensagemRequest(BaseModel):
    mensagem: str


@app.post("/chat")
def chat(request: MensagemRequest):
    global historico_sessao

    if ENGINE == "langgraph":
        # ── Motor LangGraph ──────────────────────────────────────
        from agent import executar_agente
        resultado = {}
        try:
            resultado = executar_agente(request.mensagem, historico_sessao)
            resposta_final = resultado.get("resposta_final", "")
        except Exception as e:
            print(f"Erro na execução do LangGraph: {e}")
            resposta_final = (
                "Desculpe, ocorreu um erro no motor LangGraph. "
                "Tente novamente em instantes."
            )

        pensamento = [
            "🔀 Processado por: LangGraph (Grafo de Estado)",
            f"🎯 Intenção detectada: {resultado.get('intencao', '?')}",
            f"📦 Parâmetros: {resultado.get('parametros', {})}",
            f"✅ Clareza: {resultado.get('clareza', False)}",
        ]

    else:
        # ── Motor CrewAI (padrão) ────────────────────────────────
        from crew.crew import executar_crew
        try:
            resposta_final = str(executar_crew(request.mensagem, historico_sessao))
        except Exception as e:
            print(f"Erro na execução do CrewAI: {e}")
            resposta_final = (
                "Desculpe, o servidor de inteligência artificial atingiu o limite de "
                "requisições temporariamente. Por favor, aguarde alguns segundos e tente "
                "novamente.\n\n"
                "*(Nota: A operação solicitada pode ter sido realizada com sucesso no banco "
                "de dados, pois o erro ocorreu no processamento final da resposta).* "
            )

        pensamento = [
            "🤖 Processado por: CrewAI (Multi-Agentes)",
            "👥 Papéis envolvidos: Interpretador → Executor → Formatador",
        ]

    # Atualiza histórico da sessão
    historico_sessao.append(f"Usuário: {request.mensagem}")
    historico_sessao.append(f"Agente: {resposta_final}")

    return {
        "pensamento": pensamento,
        "resposta": resposta_final,
        "tasks": None,
    }


@app.get("/engine")
def get_engine():
    return {"engine": ENGINE}


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
        "Expires": "0",
    })