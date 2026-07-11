# Diário de Aprendizado - TaskAgent V2 (Orquestração de Agentes de IA)

Este diário serve para documentar os conceitos estudados, implementações técnicas e evoluções ao longo do desenvolvimento do TaskAgent V2.

---

## 📝 Setup Inicial e Estruturação do Fluxo com LangGraph - 11/07/2026 11:55

### 🛠️ O que eu Modifiquei

Nesta inicialização da versão V2 do TaskAgent, eu migrei a arquitetura para usar o framework **LangGraph**, estruturando o agente como um Grafo de Estado. Os arquivos que eu criei e configurei foram:

*   **[graph/state.py](graph/state.py)**: Definição do estado global do agente utilizando `TypedDict` (`TaskAgentState`). Eu configurei este estado para gerenciar as informações persistentes do fluxo:
    *   `mensagem_usuario`: Entrada atual do usuário.
    *   `historico`: Histórico de conversas acumulado.
    *   `intencao` e `parametros`: Intenção inferida (ex: criar, listar, deletar) e variáveis associadas (título, ID).
    *   `clareza`: Indicador lógico (booleano) de que eu possuo todos os dados necessários.
    *   `duvida` e `resposta_api`/`resposta_final`: Informações sobre clarificações pendentes e retornos da execução.
*   **[graph/graph.py](graph/graph.py)**: Configuração e compilação do grafo (`StateGraph`). Eu defini os nós e a lógica de transição/roteamento:
    *   Nós que eu registrei: `interpretar`, `clarificar`, `executar`, `confirmar`.
    *   Ponto de Entrada: Nó `interpretar`.
    *   Transições Condicionais: Utilizei a função de roteamento `deve_clarificar_ou_executar` baseada na flag `clareza` do estado.
    *   Loops: Apontei o nó `clarificar` de volta para `interpretar` para que eu possa reavaliar a entrada do usuário após a clarificação.
*   **[graph/nodes.py](graph/nodes.py)**: Implementação lógica de cada nó com mocks (simulações que pretendo integrar com LLMs e APIs reais no futuro):
    *   `interpretar_intencao`: Usei expressões regulares e buscas de palavras-chave simples para identificar intenções (`criar`, `listar`, `deletar`) e parâmetros adicionais.
    *   `pedir_clarificacao`: Criei uma interação síncrona com o usuário para obter parâmetros ausentes.
    *   `executar_task`: Fiz simulações de chamadas de API simulando a criação, listagem e remoção de tarefas.
    *   `confirmar_resultado`: Formatei a exibição da mensagem de sucesso ou erro final para o usuário.
*   **[main.py](main.py)**: Ponto de entrada do sistema que executa um loop REPL no terminal, onde eu coleto as entradas e aciono o método `app.invoke()` do grafo compilado.
*   **Ambiente e Gerenciamento**: Configurei o ambiente do projeto com `pyproject.toml`, `.python-version` e gerenciei as dependências com o `uv` (gerando o `uv.lock`).

---

### 🧠 O que eu Aprendi / Conceitos Estudados

1.  **Orquestração baseada em Grafo de Estados (State Graphs)**:
    *   Compreendi que, diferentemente de fluxos sequenciais rígidos, a orquestração por grafo de estados permite definir comportamentos complexos com ciclos, ramificações e memória compartilhada.
    *   Estudei que o **Estado (State)** atua como a única fonte de verdade da execução. Cada nó que eu programo lê o estado e retorna apenas os campos que deseja atualizar.
2.  **Nós (Nodes) vs Bordas (Edges)**:
    *   **Nós**: Entendi que representam as ações do agente. Cada nó que escrevi executa uma tarefa dedicada.
    *   **Bordas Normais**: Fluxos direcionados estáticos conectando um nó ao próximo.
    *   **Bordas Condicionais (Conditional Edges)**: Tomada de decisão dinâmica. Eu vi como o grafo avalia uma função baseada no estado para decidir o próximo nó ativo (decidindo se preciso clarificar ou se já posso executar).
3.  **Human-in-the-loop (Loops de Interação)**:
    *   Entendi como modelar um ciclo de feedback para que o agente pause a execução para interagir comigo (`clarificar`), salvando a dúvida e reavaliando a nova resposta no nó de interpretação.
4.  **Mocking e Arquitetura Desacoplada**:
    *   Percebi a importância de usar funções mockadas para validar a topologia e lógica do grafo antes de introduzir custos e latência de LLMs ou complexidades de bancos de dados.

---

### 🚀 Meus Próximos Passos
*   Substituir a lógica de interpretação de keywords/regex por chamadas a uma LLM real.
*   Integrar o nó de execução com uma API externa (FastAPI) para manipulação real de tarefas.
