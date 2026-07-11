from graph.graph import construir_grafo

grafo = construir_grafo()

def executar_agente(mensagem: str, historico: list[str]) -> dict:
    estado_inicial = {
        "mensagem_usuario": mensagem,
        "historico": historico,
        "intencao": "",
        "parametros": {},
        "clareza": False,
        "duvida": "",
        "resposta_api": {},
        "resposta_final": ""
    }

    resultado = grafo.invoke(estado_inicial)

    return {
        "intencao": resultado["intencao"],
        "parametros": resultado["parametros"],
        "resposta_api": resultado["resposta_api"],
        "resposta_final": resultado["resposta_final"],
        "historico": resultado["historico"]
    }
