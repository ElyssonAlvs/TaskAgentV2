from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel
from agent import executar_agente

app = FastAPI()

# Histórico em memória por sessão simples
historico_sessao: list[str] = []

class MensagemRequest(BaseModel):
    mensagem: str

@app.post("/chat")
def chat(request: MensagemRequest):
    global historico_sessao

    resultado = executar_agente(request.mensagem, historico_sessao)

    # Atualiza histórico da sessão
    historico_sessao = resultado["historico"]

    # Formata pensamento do agente para exibir na UI
    pensamento = []
    pensamento.append(f" Intenção detectada: {resultado['intencao']}")

    if resultado["parametros"]:
        pensamento.append(f" Parâmetros: {resultado['parametros']}")

    if isinstance(resultado.get("resposta_api"), dict) and "erro" in resultado["resposta_api"]:
        pensamento.append(f" Erro: {resultado['resposta_api']['erro']}")
    elif resultado["intencao"] == "desconhecida" or not resultado["clareza"]:
        pensamento.append(f" Aguardando clarificação do usuário")
    else:
        pensamento.append(f" API respondeu com sucesso")

    # Detecta se a resposta é uma lista de tasks ou task única
    resposta_api = resultado["resposta_api"]
    tasks = None
    if isinstance(resposta_api, list):
        tasks = resposta_api
    elif isinstance(resposta_api, dict) and "title" in resposta_api:
        # Tarefa única buscada por ID — envolve em lista para o frontend renderizar na tabela
        tasks = [resposta_api]
    elif isinstance(resposta_api, dict) and "tasks" in resposta_api:
        tasks = resposta_api["tasks"]

    return {
        "pensamento": pensamento,
        "resposta": resultado["resposta_final"],
        "tasks": tasks
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