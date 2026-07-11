from graph.state import TaskAgentState
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import json
import os
import re
import httpx

BASE_URL = "http://127.0.0.1:8000"

load_dotenv()

# Inicializa o LLM uma vez — fora das funções para não recriar a cada chamada
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)

SYSTEM_PROMPT = """Você é um interpretador de intenções para um gerenciador de tasks.

Analise a mensagem do usuário e o histórico da conversa, e retorne APENAS um JSON válido com esta estrutura:

{
  "intencao": "criar" | "listar" | "atualizar" | "deletar" | "desconhecida",
  "parametros": {
    "id": <número ou null>,
    "titulo": "<string ou null>",
    "status": "<string ou null>"
  },
  "clareza": true | false,
  "duvida": "<pergunta para o usuário caso clareza seja false, senão string vazia>"
}

Regras:
- Se a mensagem for uma resposta a uma clarificação anterior, use o histórico para inferir a intenção
- clareza é false quando falta informação essencial para executar a ação
- Para criar: precisa de título
- Para deletar/atualizar: precisa de id ou título
- Para listar: sempre clareza true
- Retorne SOMENTE o JSON, sem texto adicional, sem markdown, sem explicações, em pt-br"""


def interpretar_intencao(state: TaskAgentState) -> dict:
    mensagem = state["mensagem_usuario"]
    historico = state["historico"]

    print(f"\n[Interpretar] Mensagem: '{mensagem}'")

    # Monta o contexto com histórico para o LLM entender respostas de clarificação
    historico_formatado = "\n".join(historico) if historico else "Nenhum histórico ainda."

    prompt = f"""Histórico da conversa:
{historico_formatado}

Mensagem atual do usuário: {mensagem}"""

    try:
        resposta = llm.invoke([
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ])

        conteudo = resposta.content.strip()

        # Remove markdown caso o LLM insista em retornar ```json
        conteudo = re.sub(r"```json|```", "", conteudo).strip()

        dados = json.loads(conteudo)

        intencao = dados.get("intencao", "desconhecida")
        parametros = dados.get("parametros", {})
        clareza = dados.get("clareza", False)
        duvida = dados.get("duvida", "")

        # Limpa nulls do dicionário de parâmetros
        parametros = {k: v for k, v in parametros.items() if v is not None}

        print(f"[Interpretar] LLM retornou -> intencao: {intencao} | parametros: {parametros} | clareza: {clareza}")

    except json.JSONDecodeError as e:
        print(f"[Interpretar] Erro ao parsear JSON do LLM: {e}")
        print(f"[Interpretar] Resposta bruta: {conteudo}")
        intencao = state.get("intencao", "desconhecida")
        parametros = state.get("parametros", {})
        clareza = False
        duvida = "Não entendi bem. Pode repetir de outra forma?"

    historico_atualizado = historico + [f"usuário: {mensagem}"]

    return {
        "intencao": intencao,
        "parametros": parametros,
        "clareza": clareza,
        "duvida": duvida,
        "historico": historico_atualizado
    }


# Nó 2: pede clarificação ao usuário (versão assíncrona Web sem bloqueio de console)
def pedir_clarificacao(state: TaskAgentState) -> dict:
    print(f"\n[Clarificação] Enviando dúvida ao frontend: '{state['duvida']}'")
    
    # Adiciona apenas a pergunta do agente no histórico
    historico_atualizado = state["historico"] + [
        f"agente: {state['duvida']}"
    ]

    return {
        "resposta_final": state["duvida"],
        "historico": historico_atualizado
    }


# Nó 3: executa a ação chamando a API
def executar_task(state: TaskAgentState) -> dict:
    intencao = state["intencao"]
    parametros = state["parametros"]

    print(f"\n[Executar] Intenção: {intencao} | Parâmetros: {parametros}")

    try:
        if intencao == "criar":
            resposta = httpx.post(
                f"{BASE_URL}/v1/tasks/",
                json={"title": parametros.get("titulo")}
            )

        elif intencao == "listar":
            resposta = httpx.get(f"{BASE_URL}/v1/tasks/")

        elif intencao == "deletar":
            task_id = parametros.get("id")

            # Se veio título em vez de ID, busca o ID primeiro
            if not task_id and parametros.get("titulo"):
                busca = httpx.get(f"{BASE_URL}/v1/tasks/")
                tasks = busca.json()
                titulo_alvo = parametros["titulo"].lower()
                match = next(
                    (t for t in tasks if titulo_alvo in t.get("title", "").lower()),
                    None
                )
                if match:
                    task_id = match["id"]
                else:
                    return {"resposta_api": {"erro": f"Nenhuma task encontrada com título '{parametros['titulo']}'"}}

            resposta = httpx.delete(f"{BASE_URL}/v1/tasks/{task_id}")

        elif intencao == "atualizar":
            task_id = parametros.get("id")
            
            # Mapeia português/variantes de status para os valores válidos do enum do backend: pending, done, in_progress
            status_map = {
                "concluida": "done",
                "concluída": "done",
                "done": "done",
                "pendente": "pending",
                "pending": "pending",
                "em progresso": "in_progress",
                "in_progress": "in_progress",
                "em_progresso": "in_progress"
            }
            
            payload = {}
            if "titulo" in parametros and parametros["titulo"] is not None:
                payload["title"] = parametros["titulo"]
            if "status" in parametros and parametros["status"] is not None:
                status_original = parametros["status"].lower().strip()
                payload["status"] = status_map.get(status_original, status_original)

            resposta = httpx.put(
                f"{BASE_URL}/v1/tasks/{task_id}",
                json=payload
            )

        else:
            return {"resposta_api": {"erro": "intenção não reconhecida"}}

        resposta.raise_for_status()
        
        # 204 No Content não possui corpo JSON para decodificar
        if resposta.status_code == 204 or not resposta.content:
            return {"resposta_api": {"status": "sucesso"}}
            
        return {"resposta_api": resposta.json()}

    except httpx.HTTPStatusError as e:
        print(f"[Executar] Erro HTTP: {e.response.status_code}")
        return {"resposta_api": {"erro": f"Erro da API: {e.response.status_code}"}}

    except httpx.ConnectError:
        print("[Executar] API não está rodando")
        return {"resposta_api": {"erro": "Não consegui conectar à API. Ela está rodando?"}}


# Nó 4: formata a resposta final para o usuário
def confirmar_resultado(state: TaskAgentState) -> dict:
    intencao = state["intencao"]
    resposta_api = state["resposta_api"]

    if "erro" in resposta_api:
        msg = f"Erro: {resposta_api['erro']}"

    elif intencao == "criar":
        msg = f"Task '{resposta_api.get('title')}' criada com ID {resposta_api.get('id')}."

    elif intencao == "listar":
        # API pode retornar lista direta ou dict com chave "tasks"
        tasks = resposta_api if isinstance(resposta_api, list) else resposta_api.get("tasks", [])
        if not tasks:
            msg = "Nenhuma task encontrada."
        else:
            lista = "\n".join([f"  [{t['id']}] {t.get('title')} - {t.get('status', 'sem status')}" for t in tasks])
            msg = f"Tasks encontradas:\n{lista}"

    elif intencao == "deletar":
        msg = f"Task deletada com sucesso."

    elif intencao == "atualizar":
        msg = f"Task '{resposta_api.get('title')}' atualizada com sucesso."

    else:
        msg = "Ação concluída."

    print(f"\n[Resultado] {msg}")

    historico_atualizado = state["historico"] + [f"agente: {msg}"]

    return {
        "resposta_final": msg,
        "historico": historico_atualizado
    }