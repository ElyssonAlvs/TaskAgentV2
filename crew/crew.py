from crewai import Crew, Process
from crew.agents import interpretador, executor, formatador
from crew.tasks import criar_tasks
import os

def executar_crew(mensagem: str, historico: list[str]) -> str:
    # Configura o diretório de memória local para evitar concorrência/travas na pasta AppData do sistema
    os.environ["CREWAI_STORAGE_DIR"] = "./db/crewai_storage"
    
    historico_formatado = "\n".join(historico) if historico else "Sem histórico."

    tasks = criar_tasks(mensagem, historico_formatado)

    crew = Crew(
        agents=[interpretador, executor, formatador],
        tasks=tasks,
        process=Process.sequential,
        memory=True,
        embedder={
            "provider": "google-generativeai",
            "config": {
                "api_key": os.getenv("GOOGLE_GEMINI_KEY"),
                "model_name": "gemini-embedding-001"
            }
        },
        verbose=True
    )

    resultado = crew.kickoff()
    return str(resultado)
