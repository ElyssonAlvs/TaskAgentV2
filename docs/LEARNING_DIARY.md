# Diário de Aprendizado - TaskAgent V2 (Orquestração de Agentes de IA)

Este diário serve para documentar os conceitos estudados, implementações técnicas e evoluções ao longo do desenvolvimento do TaskAgent V2.

---

## 🔌 Estruturação do Ecossistema e Integração do TaskManager - 11/07/2026 16:27

### 🛠️ O que eu Modifiquei

Nesta etapa, eu estruturei a integração da API de backend que servirá de suporte para as ações reais do meu agente:

*   **Configuração de Integração**: Introduzi e configurei no meu workspace o repositório externo do **[TaskManager](file:///C:/Users/elyss/Desktop/Projects/TaskAgentV2/TaskManager/)**, uma API RESTful completa desenvolvida em FastAPI que expõe operações CRUD de tarefas integradas ao banco SQLite.
*   **[.gitignore](file:///C:/Users/elyss/Desktop/Projects/TaskAgentV2/.gitignore)**: Atualizei as configurações de ignore do Git para rastrear apenas o código do agente (`TaskAgentV2`), isolando o repositório da API `TaskManager` para que ambos continuem versionados de forma independente e limpa.

---

### 🧠 O que eu Aprendi / Conceitos Estudados

1.  **Arquitetura de Agentes desacoplada de Serviços de Persistência**:
    *   Compreendi que, em um design de arquitetura de software moderno, o agente de IA não deve ter acesso de escrita direta ou lógica de negócio sobre o banco de dados. Em vez disso, ele deve interagir via chamadas de API (REST/HTTP). Isso melhora o desacoplamento, a segurança e a testabilidade individual do agente e da aplicação de tarefas.
2.  **Modularidade de Ambientes e Versionamento (Multi-Repo)**:
    *   Entendi a importância de usar regras adequadas de Git ignore ao aninhar repositórios de estudo, garantindo que o versionamento do projeto de IA não rastreie arquivos do microsserviço de tarefas, mantendo o histórico de commits do `TaskAgentV2` focado estritamente na lógica do agente.

---

### 🚀 Meus Próximos Passos
*   Substituir os mocks das chamadas HTTP no nó de execução (`executar_task`) em [graph/nodes.py](graph/nodes.py) por requisições HTTP reais usando `httpx` ou `requests`, conectando meu agente de forma integrada aos endpoints da API do `TaskManager`.

---

## 🤖 Integração com LLM (Groq) e Correção dos Nós do Grafo - 11/07/2026 12:46

### 🛠️ O que eu Modifiquei

Eu integrei um LLM real para interpretar as intenções do usuário e corrigi erros de importação causados pela ausência dos outros nós do grafo. As alterações realizadas foram:

*   **[graph/nodes.py](file:///C:/Users/elyss/Desktop/Projects/TaskAgentV2/graph/nodes.py)**:
    *   Substituí a lógica de palavras-chave/regex mockada por uma chamada real à API do Groq utilizando o modelo `llama-3.3-70b-versatile` (`ChatGroq`).
    *   Defini um prompt de sistema estruturado para instruir o LLM a analisar o histórico e a mensagem atual do usuário, retornando as informações no formato JSON esperado pelo estado global do agente (com campos como `intencao`, `parametros`, `clareza` e `duvida`).
    *   Restaurei as funções dos outros nós do grafo (`pedir_clarificacao`, `executar_task` e `confirmar_resultado`) que haviam sido acidentalmente deletadas durante a transição para o LLM. Isso resolveu o erro `ImportError: cannot import name 'pedir_clarificacao' from 'graph.nodes'`.

---

### 🧠 O que eu Aprendi / Conceitos Estudados

1.  **Transição de Mocks para LLMs (Structured Output)**:
    *   Compreendi como estruturar prompts para obter respostas consistentes no formato JSON por meio de LLMs de chat.
    *   Entendi a importância de tratar exceções de parse de JSON (`json.JSONDecodeError`) para garantir a robustez do fluxo, definindo valores padrão para o estado caso o LLM retorne texto inesperado.
2.  **Manutenção da Integridade do Grafo no LangGraph**:
    *   Reconheci que, ao registrar nós como `add_node("clarificar", pedir_clarificacao)` no `StateGraph`, é impreterível que os callbacks correspondentes permaneçam implementados e expostos no módulo de nós. A remoção acidental de qualquer nó quebra as importações do arquivo de construção do grafo (`graph.py`).

---

### 🚀 Meus Próximos Passos
*   Substituir a lógica mockada do nó de execução (`executar_task`) por chamadas reais a uma API FastAPI.

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
