# Diário de Aprendizado - TaskAgent V2 (Orquestração de Agentes de IA)

Este diário serve para documentar os conceitos estudados, implementações técnicas e evoluções ao longo do desenvolvimento do TaskAgent V2.

---

## 📝 Setup Inicial e Estruturação do Fluxo com LangGraph - 11/07/2026 11:55

### 🛠️ O que foi Modificado

Nesta inicialização da versão V2 do TaskAgent, migramos a arquitetura para usar o framework **LangGraph**, estruturando o agente como um Grafo de Estado. Os arquivos criados e configurados foram:

*   **[graph/state.py](file:///C:/Users/elyss/Desktop/Projects/TaskAgentV2/graph/state.py)**: Definição do estado global do agente utilizando `TypedDict` (`TaskAgentState`). Ele gerencia informações persistentes ao longo do fluxo, como:
    *   `mensagem_usuario`: Entrada atual.
    *   `historico`: Histórico de conversas acumulado.
    *   `intencao` e `parametros`: Intenção inferida (ex: criar, listar, deletar) e variáveis associadas (título, ID).
    *   `clareza`: Indicador lógico (booleano) de que temos todos os dados necessários.
    *   `duvida` e `resposta_api`/`resposta_final`: Informações sobre clarificações pendentes e retornos da execução.
*   **[graph/graph.py](file:///C:/Users/elyss/Desktop/Projects/TaskAgentV2/graph/graph.py)**: Configuração e compilação do grafo (`StateGraph`). Define os nós e a lógica de transição/roteamento:
    *   Nós registrados: `interpretar`, `clarificar`, `executar`, `confirmar`.
    *   Ponto de Entrada: Nó `interpretar`.
    *   Transições Condicionais: Usa a função de roteamento `deve_clarificar_ou_executar` baseada na flag `clareza` do estado.
    *   Loops: O nó `clarificar` aponta de volta para o nó `interpretar` para reavaliar a entrada do usuário após a clarificação.
*   **[graph/nodes.py](file:///C:/Users/elyss/Desktop/Projects/TaskAgentV2/graph/nodes.py)**: Implementação lógica de cada nó com mocks (simulações que serão integradas com LLMs e APIs reais no futuro):
    *   `interpretar_intencao`: Realiza parsing regex/keyword para identificar intenções (`criar`, `listar`, `deletar`) e parâmetros adicionais.
    *   `pedir_clarificacao`: Interage de forma síncrona com o usuário para obter parâmetros ausentes.
    *   `executar_task`: Simula chamadas de API simulando a criação, listagem e remoção de tarefas.
    *   `confirmar_resultado`: Formata e exibe a mensagem de sucesso ou erro final.
*   **[main.py](file:///C:/Users/elyss/Desktop/Projects/TaskAgentV2/main.py)**: Ponto de entrada do sistema que executa um loop REPL no terminal, coletando entradas do usuário e acionando o método `app.invoke()` do grafo compilado.
*   **Ambiente e Gerenciamento**: Configuração do projeto com `pyproject.toml`, `.python-version` e gerenciador de pacotes `uv` (gerando o `uv.lock`).

---

### 🧠 O que foi Aprendido / Conceitos Estudados

1.  **Orquestração baseada em Grafo de Estados (State Graphs)**:
    *   Diferente de fluxos sequenciais rígidos ou loops autônomos de agentes simples, a orquestração por grafo de estados permite definir comportamentos complexos com ciclos, ramificações e memória compartilhada.
    *   O **Estado (State)** é a única fonte de verdade da execução. Cada nó lê o estado e retorna apenas os campos que deseja atualizar, promovendo uma programação funcional e previsível.
2.  **Nós (Nodes) vs Bordas (Edges)**:
    *   **Nós**: Representam ações ou agentes específicos. Cada nó realiza uma tarefa dedicada (ex: chamar um LLM para extração de intenções, ou executar uma chamada de sistema).
    *   **Bordas Normais**: Fluxos direcionados estáticos conectando um nó ao próximo de forma direta.
    *   **Bordas Condicionais (Conditional Edges)**: Tomada de decisão dinâmica em tempo de execução. O grafo avalia uma função baseada no estado atual para decidir o próximo nó ativo (permitindo que o agente decida se precisa clarificar ou se já pode executar).
3.  **Human-in-the-loop (Loops de Interação)**:
    *   O design permite pausar/retornar a execução solicitando informações ao usuário (`clarificar`). O agente acumula a dúvida no estado, coleta a resposta e alimenta a nova informação no nó de interpretação original, criando um ciclo de correção e enriquecimento de dados interativo.
4.  **Mocking e Arquitetura Desacoplada**:
    *   O uso de funções mockadas no início do projeto facilita a validação da topologia e lógica do grafo antes de introduzir custos e latência de LLMs ou complexidades de integração de bancos de dados/APIs externas.

---

### 🚀 Próximos Passos
*   Substituir a lógica de interpretação de keywords/regex por chamadas a uma LLM real.
*   Integrar o nó de execução com uma API externa (FastAPI) para manipulação real de tarefas.
