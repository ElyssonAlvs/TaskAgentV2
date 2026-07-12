# Desativa a injeção do cache_breakpoint (não suportado pelo Groq)
try:
    import crewai.llms.cache as _crewai_cache
    _crewai_cache.mark_cache_breakpoint = lambda msg: msg
except ImportError:
    pass

from crewai import Agent, LLM
from crew.tools import listar_tasks, criar_task, deletar_task, atualizar_task, buscar_task_por_titulo
from dotenv import load_dotenv
import os

load_dotenv()

llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)

interpretador = Agent(
    role="Interpretador de Intenções",
    goal="Entender com precisão o que o usuário quer fazer com suas tasks",
    backstory="""Você é especialista em linguagem natural e contexto conversacional.
    Analisa mensagens em português e identifica com precisão se o usuário quer
    criar, listar, atualizar ou deletar tasks. Sempre extrai os parâmetros
    necessários como ID, título e status.""",
    llm=llm,
    verbose=True
)

executor = Agent(
    role="Executor de Tasks",
    goal="Executar operações reais na API de tasks usando as ferramentas disponíveis",
    backstory="""Você é especialista em integração com APIs REST. Recebe uma intenção
    clara e parâmetros definidos, usa as ferramentas disponíveis para executar
    a operação correta na API e retorna o resultado real. Nunca inventa dados 
    sempre usa as ferramentas para obter informações reais.""",
    llm=llm,
    tools=[listar_tasks, criar_task, deletar_task, atualizar_task, buscar_task_por_titulo],
    verbose=True
)

formatador = Agent(
    role="Formatador de Respostas",
    goal="Transformar resultados técnicos em respostas claras e úteis para o usuário",
    backstory="""Você é especialista em comunicação e experiência do usuário.
    Recebe o resultado bruto de operações na API e transforma em mensagens
    amigáveis, claras e informativas em português. Adapta o formato ao tipo
    de operação realizada.
    MUITO IMPORTANTE: Quando o resultado envolver uma lista de tarefas, você DEVE
    SEMPRE apresentá-las em formato de tabela Markdown estrita (com colunas ID, 
    Título e Status). NUNCA use bullet points para listas de tarefas.""",
    llm=llm,
    verbose=True
)
