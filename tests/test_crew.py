from crew.crew import executar_crew

cenarios = [
    "mostra todas as tasks",
    "cria uma task com título Testar CrewAI",
    "deleta a task de número 8"
]

for mensagem in cenarios:
    print(f"\n{'='*50}")
    print(f"MENSAGEM: {mensagem}")
    print('='*50)
    resultado = executar_crew(mensagem, [])
    print(f"\nRESULTADO: {resultado}")
