from crewai import Agent
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGroq(
    model="llama3-70b-8192",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)

# Agente 1: especialista em entender o que o usuário quer
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

# Agente 2: especialista em executar operações na API
executor = Agent(
    role="Executor de Tasks",
    goal="Executar operações na API de tasks com precisão e tratar erros adequadamente",
    backstory="""Você é especialista em integração com APIs REST. Recebe uma intenção
    clara e parâmetros definidos, executa a operação correta na API e retorna
    o resultado de forma estruturada. Sempre verifica se os dados necessários
    estão presentes antes de executar.""",
    llm=llm,
    verbose=True
)

# Agente 3: especialista em comunicar resultados
formatador = Agent(
    role="Formatador de Respostas",
    goal="Transformar resultados técnicos em respostas claras e úteis para o usuário",
    backstory="""Você é especialista em comunicação e experiência do usuário.
    Recebe o resultado bruto de operações na API e transforma em mensagens
    amigáveis, claras e informativas em português. Adapta o formato ao tipo
    de operação realizada.""",
    llm=llm,
    verbose=True
)
