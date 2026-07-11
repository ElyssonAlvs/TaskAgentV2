from graph.graph import construir_grafo

def main():
    app = construir_grafo()

    print("TaskAgent v2 — digite sua mensagem (ctrl+c para sair)\n")

    while True:
        mensagem = input("Você: ")
        
        estado_inicial = {
            "mensagem_usuario": mensagem,
            "historico": [],
            "intencao": "",
            "parametros": {},
            "clareza": False,
            "duvida": "",
            "resposta_api": {},
            "resposta_final": ""
        }

        resultado = app.invoke(estado_inicial)
        print(f"\nAgente: {resultado['resposta_final']}\n")

if __name__ == "__main__":
    main()