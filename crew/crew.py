from crewai import Crew, Process
from crew.agents import interpretador, executor, formatador
from crew.tasks import criar_tasks

def executar_crew(mensagem: str, historico: list[str]) -> str:
    historico_formatado = "\n".join(historico) if historico else "Sem histórico."

    tasks = criar_tasks(mensagem, historico_formatado)

    crew = Crew(
        agents=[interpretador, executor, formatador],
        tasks=tasks,
        process=Process.sequential,
        verbose=True
    )

    resultado = crew.kickoff()
    return str(resultado)
