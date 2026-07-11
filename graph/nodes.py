from graph.state import TaskAgentState
import re

# Nó 1: interpreta a intenção do usuário
def interpretar_intencao(state: TaskAgentState) -> dict:
    mensagem = state["mensagem_usuario"]
    historico = state["historico"]
    
    print(f"\n[Interpretar] Mensagem: '{mensagem}'")
    
    # --- MOCK: substituirei por LLM na Aula 3 ---
    # Preserva a intenção que já estava no estado, se houver
    intencao = state.get("intencao", "desconhecida")
    if not intencao:
        intencao = "desconhecida"
        
    parametros = state.get("parametros", {})
    if not parametros:
        parametros = {}
        
    clareza = False
    duvida = ""

    msg_lower = mensagem.lower()

    # Verifica se há uma nova intenção clara na mensagem
    if "cria" in msg_lower or "adiciona" in msg_lower:
        intencao = "criar"
    elif "lista" in msg_lower or "mostra" in msg_lower:
        intencao = "listar"
    elif "deleta" in msg_lower or "remove" in msg_lower:
        intencao = "deletar"

    if intencao == "criar":
        if "título" in msg_lower or "titulo" in msg_lower:
            titulo = mensagem.split("título")[-1].strip() if "título" in msg_lower else mensagem.split("titulo")[-1].strip()
            parametros = {"titulo": titulo}
            clareza = True
        elif state.get("intencao") == "criar":
            # Se for resposta à clarificação, assume que a mensagem inteira é o título
            parametros = {"titulo": mensagem.strip()}
            clareza = True
        else:
            duvida = "Qual o título da task que você quer criar?"

    elif intencao == "listar":
        clareza = True

    elif intencao == "deletar":
        match_id = re.search(r'\d+', mensagem)
        
        if "título" in msg_lower or "titulo" in msg_lower:
            titulo = mensagem.split("título")[-1].strip() if "título" in msg_lower else mensagem.split("titulo")[-1].strip()
            parametros = {"titulo": titulo}
            clareza = True
        elif match_id:
            # Extração de parâmetros aceita ID numérico
            parametros = {"id": int(match_id.group())}
            clareza = True
        elif state.get("intencao") == "deletar":
            # Se não tem ID mas tem intenção de deletar na clarificação, assume como título
            parametros = {"titulo": mensagem.strip()}
            clareza = True
        else:
            duvida = "Qual task você quer deletar? Me diz o título ou ID."

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