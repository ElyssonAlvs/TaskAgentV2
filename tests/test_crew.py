import os
import sys

# Configura o terminal para UTF-8 para evitar erros de renderização de emojis no Windows
if sys.platform.startswith('win'):
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from crew.crew import executar_crew

sessao = sys.argv[1] if len(sys.argv) > 1 else "1"

if sessao == "1":
    print("=== SESSÃO 1 ===")
    r = executar_crew("cria uma task com título Testar Memória do CrewAI", [])
    print(f"\nResposta: {r}\n")

elif sessao == "2":
    print("=== SESSÃO 2 ===")
    r = executar_crew("qual foi a última task que criamos?", [])
    print(f"\nResposta: {r}\n")