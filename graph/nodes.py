from graph.state import TaskAgentState
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import json
import os
import re

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

        print(f"[Interpretar] LLM retornou → intenção: {intencao} | parâmetros: {parametros} | clareza: {clareza}")

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


# Nó 2: pede clarificação ao usuário
def pedir_clarificacao(state: TaskAgentState) -> dict:
    print(f"\n[Clarificação] {state['duvida']}")
    
    resposta = input(f"Agente: {state['duvida']}\nVocê: ")
    
    historico_atualizado = state["historico"] + [
        f"agente: {state['duvida']}",
        f"usuário: {resposta}"
    ]

    return {
        "mensagem_usuario": resposta,
        "historico": historico_atualizado
    }


# Nó 3: executa a ação chamando a API (mock por enquanto)
def executar_task(state: TaskAgentState) -> dict:
    print(f"\n[Executar] Intenção: {state['intencao']} | Parâmetros: {state['parametros']}")
    
    # --- MOCK: substituirei por chamada real à FastAPI na Aula 4 ---
    intencao = state["intencao"]
    parametros = state["parametros"]
    
    if intencao == "criar":
        resposta_api = {"status": "criada", "task": {"titulo": parametros.get("titulo"), "id": 99}}
    elif intencao == "listar":
        resposta_api = {"tasks": [{"id": 1, "titulo": "Estudar LangGraph"}, {"id": 2, "titulo": "Revisar RAG"}]}
    elif intencao == "deletar":
        alvo = parametros.get("titulo") or parametros.get("id")
        resposta_api = {"status": "deletada", "titulo": alvo}
    else:
        resposta_api = {"erro": "intenção não reconhecida"}

    return {"resposta_api": resposta_api}


# Nó 4: formata a resposta final para o usuário
def confirmar_resultado(state: TaskAgentState) -> dict:
    intencao = state["intencao"]
    resposta_api = state["resposta_api"]
    
    if intencao == "criar":
        msg = f"Task '{resposta_api['task']['titulo']}' criada com ID {resposta_api['task']['id']}."
    elif intencao == "listar":
        tasks = resposta_api.get("tasks", [])
        lista = "\n".join([f"  [{t['id']}] {t['titulo']}" for t in tasks])
        msg = f"Tasks encontradas:\n{lista}"
    elif intencao == "deletar":
        msg = f"Task '{resposta_api.get('titulo')}' deletada com sucesso."
    else:
        msg = f"Não consegui processar: {resposta_api.get('erro')}"

    print(f"\n[Resultado] {msg}")
    
    historico_atualizado = state["historico"] + [f"agente: {msg}"]

    return {
        "resposta_final": msg,
        "historico": historico_atualizado
    }