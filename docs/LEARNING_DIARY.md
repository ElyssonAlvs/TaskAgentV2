# Diário de Aprendizado - TaskAgent V2 (Orquestração de Agentes de IA)

Este diário serve para documentar os conceitos estudados, implementações técnicas e evoluções ao longo do desenvolvimento do TaskAgent V2.

---

## 👥 Início da Integração com CrewAI (Multiagentes) — 11/07/2026 19:28

### 🛠️ O que eu Modifiquei

Eu iniciei a transição/estudo da orquestração de tarefas utilizando o framework **CrewAI** em paralelo com o LangGraph.

*   **Configuração de Ambiente**:
    *   Instalei o framework `crewai` no projeto via `uv add crewai`.
*   **Estrutura de Diretórios**:
    *   Criei a pasta `crew/` contendo:
        *   `crew/__init__.py`: Inicialização do módulo.
        *   `crew/agents.py`: Definição de três agentes especializados (`interpretador`, `executor`, `formatador`) usando o LLM `llama3-70b-8192` via Groq.
        *   `crew/tasks.py`: Definição das tarefas sequenciais do time (`task_interpretar`, `task_executar`, `task_formatar`).
        *   `crew/crew.py`: Montagem do time (`Crew`) com fluxo sequencial (`Process.sequential`).
*   **Script de Teste**:
    *   Criei o arquivo `test_crew.py` na raiz para testar a execução sequencial isoladamente no console antes da integração com a interface web.

---

### 🧠 O que eu Aprendi / Conceitos Estudados

1.  **Orquestração de Múltiplos Agentes**:
    *   Compreendi os conceitos centrais do **CrewAI**:
        *   **Agent**: Entidade dotada de papel (`role`), objetivo (`goal`) e histórico de fundo (`backstory`) que molda a sua personalidade e direcionamento.
        *   **Task**: Uma instrução concreta com descrição e o formato de saída esperado (`expected_output`), associada a um agente específico.
        *   **Crew**: O contêiner de execução que orquestra a colaboração entre agentes e tarefas através de processos (sequencial ou hierárquico).
2.  **Diferenças entre Frameworks (LangGraph vs CrewAI)**:
    *   Assimilei que, enquanto o LangGraph nos dá controle fino e imperativo sobre o fluxo usando lógica de grafos de decisão, o CrewAI fornece uma abstração declarativa baseada na personalidade de múltiplos agentes cooperando entre si.

---

### 🚀 Meus Próximos Passos
*   Aguardar orientações para a execução de `test_crew.py` e ver o *verbose* dos agentes cooperando antes de ligá-los ao frontend web.

---

## 📖 Atualização da Documentação Técnica de Arquitetura — 11/07/2026 18:01

### 🛠️ O que eu Modifiquei

Eu atualizei a documentação técnica da arquitetura para torná-la mais visual, didática e fiel ao estado atual do código.

*   **[docs/arquitetura.md](file:///C:/Users/elyss/Desktop/Projects/TaskAgentV2/docs/arquitetura.md)**:
    *   Reescrevi todo o documento em **primeira pessoa do singular** para dar um tom de estudo pessoal.
    *   Adicionei um diagrama **Mermaid** detalhando a arquitetura geral do ecossistema (Frontend, FastAPI Agent Server na porta 8001, FastAPI TaskManager API na porta 8000 e SQLite).
    *   Corrigi o diagrama **Mermaid** do ciclo de vida do LangGraph, que agora reflete fielmente o fluxo *stateless* onde a clarificação encerra o ciclo (`clarificar --> END`).

---

### 🧠 O que eu Aprendi / Conceitos Estudados

1.  **Representação Gráfica com Mermaid**:
    *   Aprendi a usar a notação do Mermaid para criar diagramas de arquitetura de ecossistema (`graph TD` com subgrafos) e diagramas de fluxo de grafos de decisão de forma integrada diretamente nos arquivos markdown.
2.  **Sincronização de Documentação com Código**:
    *   Compreendi a importância de manter diagramas arquiteturais rigorosamente alinhados às mudanças de infraestrutura e fluxo do sistema (como a alteração da transição do nó `clarificar`), evitando desinformação para futuros desenvolvedores.

---

### 🚀 Meus Próximos Passos
*   Continuar evoluindo o agente com novos testes de interações de tarefas no frontend.

---

## 🔍 Busca de Tarefas por ID e Ajustes de Tipo no Estado - 11/07/2026 17:58

### 🛠️ O que eu Modifiquei

Eu adicionei suporte para buscar tarefas específicas pelo ID (tanto no backend quanto no mapeamento do frontend) e tornei a tipagem do estado mais flexível para lidar com as diferentes estruturas de resposta da API.

*   **[graph/nodes.py](file:///C:/Users/elyss/Desktop/Projects/TaskAgentV2/graph/nodes.py)**:
    *   **Consulta por ID**: No nó `executar_task`, implementei a lógica para que, se o usuário solicitar a listagem informando um ID, o agente realize a chamada ao endpoint `/v1/tasks/{task_id}` em vez de trazer todas as tarefas.
    *   **Exibição de Tarefa Única**: No nó `confirmar_resultado`, adicionei a validação para que, se `resposta_api` for um dicionário contendo a chave `title`, a mensagem final seja formatada como uma única tarefa encontrada.
*   **[graph/state.py](file:///C:/Users/elyss/Desktop/Projects/TaskAgentV2/graph/state.py)**:
    *   **Tipagem Flexível (`Any`)**: Alterei o tipo de `resposta_api` no `TaskAgentState` de `dict` para `Any` para refletir de maneira precisa que ela pode receber tanto listas (`list`) de tarefas quanto objetos individuais (`dict`).
*   **[main.py](file:///C:/Users/elyss/Desktop/Projects/TaskAgentV2/main.py)**:
    *   **Tratamento de Erros mais Seguro**: Ajustei a validação de erros na resposta da API para verificar se `resposta_api` é um dicionário antes de fazer a busca pela chave `"erro"`.
    *   **Envelopamento para Renderização**: Na rota `/chat`, se a API retornar uma tarefa única (dicionário contendo `title`), eu a envelopo em uma lista (`tasks = [resposta_api]`). Isso permite que a tabela do frontend renderize a tarefa com a mesma estrutura padrão sem precisar de código extra.
*   **[agent.py](file:///C:/Users/elyss/Desktop/Projects/TaskAgentV2/agent.py)**:
    *   Passei a retornar também os campos `clareza` e `duvida` na resposta da função `executar_agente`.

---

### 🧠 O que eu Aprendi / Conceitos Estudados

1.  **Polimorfismo de Resposta de API na Orquestração**:
    *   Entendi como tratar de forma elegante e flexível fluxos cujas respostas de API mudam de formato (de uma lista de objetos para um objeto único) dependendo dos parâmetros de entrada (`id`).
    *   Compreendi a importância de "envelopar" dados no backend para simplificar o consumo no frontend. Ao transformar o objeto único de tarefa em uma lista de um único elemento (`[task]`), o componente de tabela no JS continua funcionando perfeitamente sem alteração de contrato.
2.  **Segurança de Tipagem em Python com `Any`**:
    *   Assimilei que, embora o LangGraph não restrinja os tipos em runtime, utilizar tipagens coerentes no `TypedDict` (como `Any` para dados polimórficos) ajuda no autocompletar e na clareza do código para manutenção.

---

### 🚀 Meus Próximos Passos
*   Subir os servidores e testar a busca por ID digitando mensagens como "quais os detalhes da tarefa 5?" ou "me mostre a task 2".

---

## 🧹 Resolução do Problema de Cache e Ajustes no Feedback da API - 11/07/2026 17:40

### 🛠️ O que eu Modifiquei

Eu corrigi o problema em que os títulos das tarefas apareciam como `undefined` na interface gráfica e ajustei a mensagem de pensamento quando o agente não executava uma chamada à API.

*   **[main.py](file:///C:/Users/elyss/Desktop/Projects/TaskAgentV2/main.py)**:
    *   **Desativar Cache**: Modifiquei a rota que serve o arquivo `index.html` para retornar a resposta com cabeçalhos HTTP que previnem o cache agressivo do navegador (`Cache-Control: no-cache, no-store, must-revalidate`). Isso resolveu o problema do título "undefined", pois o navegador estava preso em uma versão antiga do JavaScript que não extraía o `title` corretamente.
    *   **Feedback Condicional**: Modifiquei a lógica que compõe o "pensamento" na interface web. Agora, quando o agente não consegue interpretar a intenção ou a clareza é falsa (necessitando clarificação), ele não exibe "API respondeu com sucesso", mas sim "Aguardando clarificação do usuário".
*   **[static/index.html](file:///C:/Users/elyss/Desktop/Projects/TaskAgentV2/static/index.html)**:
    *   Adicionei a string padrão `'Sem título'` como fallback para tarefas que venham sem título. A renderização agora é validada como `t.title || t.titulo || 'Sem título'`.

---

### 🧠 O que eu Aprendi / Conceitos Estudados

1.  **Gerenciamento de Cache de Navegador (HTTP Cache-Control)**:
    *   Entendi que interfaces HTML/JS servidas de forma estática costumam ser cacheadas agressivamente pelo navegador.
    *   Aprendi que alterações no frontend (`index.html`) podem não surtir efeito imediato se o servidor web (FastAPI) não enviar os headers corretos informando ao navegador para revalidar ou descartar o cache temporário.
2.  **Validação Condicional em Respostas de API Mistas**:
    *   Estudei como garantir que os logs e mensagens de *feedback* da interface reflitam a realidade de fluxos encurtados do agente (como no caso do nó `clarificar`), onde interações de pausa não utilizam a API externa.

---

### 🚀 Meus Próximos Passos
*   Realizar uma recarga forçada no navegador (`Ctrl+F5`) com os servidores online e testar se a interface está mapeando perfeitamente as propriedades das tarefas da API.

---

## 🐛 Correção do Loop de Clarificação na Web (Stateless Request-Response) - 11/07/2026 17:28

### 🛠️ O que eu Modifiquei

Eu resolvi o travamento ("loop") na interface web que ocorria quando o agente precisava pedir clarificações ao usuário. As alterações foram:

*   **[graph/nodes.py](file:///C:/Users/elyss/Desktop/Projects/TaskAgentV2/graph/nodes.py)**:
    *   Removi a chamada síncrona `input()` de dentro do nó `pedir_clarificacao`.
    *   Agora, o nó apenas registra a dúvida do agente no histórico de conversas e a define como a `resposta_final` a ser enviada ao frontend.
*   **[graph/graph.py](file:///C:/Users/elyss/Desktop/Projects/TaskAgentV2/graph/graph.py)**:
    *   Modifiquei a borda de saída do nó `clarificar`. Ao invés de retornar para `interpretar` internamente em loop contínuo síncrono, a borda agora aponta diretamente para o fim do grafo (`END`). Isso força a finalização imediata da execução e libera a resposta HTTP do FastAPI com a dúvida para o navegador.

---

### 🧠 O que eu Aprendi / Conceitos Estudados

1.  **Diferenças de Ciclo de Vida: CLI vs API Web**:
    *   Compreendi que loops interativos de terminal síncronos baseados em `input()` bloqueiam a thread principal do servidor web (bloqueando o loop de eventos do FastAPI).
    *   Aprendi que o design de interações para web deve ser **stateless (sem estado ativo)**. A clarificação deve terminar a requisição atual devolvendo a dúvida ao frontend. A resposta do usuário virá em uma nova requisição, e o histórico acumulado na sessão servirá como o contexto para o LLM.

---

### 🚀 Meus Próximos Passos
*   Subir os servidores e validar o fluxo completo de criação e clarificação via chat web.

---

## 🌐 Interface Web para o TaskAgent V2 - 11/07/2026 17:00

### 🛠️ O que eu Modifiquei

Nesta etapa (Aula 5), eu transformei o meu agente CLI em um serviço web completo com interface gráfica no navegador. As principais alterações foram:

*   **[main.py](file:///C:/Users/elyss/Desktop/Projects/TaskAgentV2/main.py)**: Reestruturei completamente o ponto de entrada da aplicação, convertendo-o em um servidor FastAPI que expõe:
    *   `POST /chat`: Executa o agente e retorna o pensamento do agente, a resposta amigável e as tarefas extraídas.
    *   `DELETE /chat/historico`: Limpa o histórico de sessões em memória.
    *   `GET /`: Serve a interface web montada em HTML/CSS estáticos.
*   **[agent.py](file:///C:/Users/elyss/Desktop/Projects/TaskAgentV2/agent.py)**: Criei este módulo para encapsular a lógica de execução do agente, mantendo a construção do grafo LangGraph isolada do servidor web.
*   **[static/index.html](file:///C:/Users/elyss/Desktop/Projects/TaskAgentV2/static/index.html)**: Criei uma interface visual moderna e escura (Dark Mode) usando HTML/CSS vanilla (com fonte Inter e transições sutis). A interface exibe:
    *   Mensagens do usuário e do agente em caixas dedicadas.
    *   O pensamento estruturado do agente (intenção, parâmetros, status de resposta).
    *   Tabela formatada com IDs, Títulos e Badges de Status (Done, Pending, In Progress) coloridos quando o agente lista tarefas.
*   **Gerenciamento de dependências (`pyproject.toml` e `uv.lock`)**: Instalei os pacotes `fastapi`, `uvicorn` e `python-multipart` necessários para rodar e testar o servidor ASGI.

---

### 🧠 O que eu Aprendi / Conceitos Estudados

1.  **Exposição de Grafos de Estado via HTTP**:
    *   Compreendi como transformar um ciclo de execução síncrono de console em endpoints RESTful assíncronos. O estado do LangGraph agora é instanciado a cada requisição de chat e alimentado com o histórico persistido em memória no backend.
2.  **Transparência e UX de Agentes (Cadeia de Pensamento)**:
    *   Aprendi a separar a resposta final textual do agente da sua "cadeia de raciocínio" (parâmetros extraídos, intenção detectada). Exibir essa camada de raciocínio em uma seção separada da interface web melhora significativamente a experiência do usuário, fornecendo clareza sobre o comportamento interno do LLM.
3.  **Renderização de Dados Ricos na UI**:
    *   Estudei como estruturar e renderizar dinamicamente componentes como tabelas de tarefas e badges de status contextuais com base no payload JSON retornado pela API do agente.

---

### 🚀 Meus Próximos Passos
*   Iniciar e testar os servidores da API (TaskManager) e do Agente em paralelo para rodar o chat web integrado.

---

## 🐛 Correção da Integração com a API Externa do TaskManager - 11/07/2026 16:45

### 🛠️ O que eu Modifiquei

Eu corrigi diversos problemas de comunicação entre o agente e a API externa do `TaskManager`, garantindo o correto mapeamento de rotas e formatos de payload sem realizar nenhuma alteração no código da API. As modificações foram:

*   **[graph/nodes.py](file:///C:/Users/elyss/Desktop/Projects/TaskAgentV2/graph/nodes.py)**:
    *   **Correção de Rotas (404)**: Ajustei todos os endpoints para utilizarem o prefixo `/v1/tasks/` (ex: `/v1/tasks/` em vez de `/tasks/`), que é a rota exposta pelo roteador da API FastAPI.
    *   **Mapeamento de Payload (422/Erros de Validação)**: Mapeei o campo de entrada do estado do agente (`titulo`) para o campo esperado pelo schema do backend (`title`).
    *   **Mapeamento de Status**: Adicionei um dicionário de tradução e mapeamento para converter termos em português/variantes (como "concluída", "pendente", "em progresso") para as opções válidas do enum de status da API (`done`, `pending`, `in_progress`).
    *   **Tratamento de Status 204**: Adicionei uma verificação para a rota de remoção (DELETE), que retorna o código HTTP `204 No Content` sem corpo de resposta, evitando que o agente tente decodificar um JSON vazio e cause um erro de parsing.
    *   **Apresentação dos Resultados**: Corrigi a leitura das chaves no dicionário de resposta (`t.get('title')` em vez de `t['titulo']`) para evitar erros de `KeyError` e exibir o título e o status corretos no terminal.
    *   **Compatibilidade de Console (Windows)**: Substituí caracteres unicode especiais (`→`, `—`) por caracteres ASCII equivalentes (`->`, `-`) nos logs de `print`, evitando erros de decodificação de console (`UnicodeEncodeError`) no Windows PowerShell.

---

### 🧠 O que eu Aprendi / Conceitos Estudados

1.  **Divergências de Modelagem (Agent-to-API Contract)**:
    *   Compreendi que o estado interno do agente de IA (como usar termos em português como `titulo`) frequentemente difere da especificação da API consumida (que usa `title`). Fazer o mapeamento explícito no nó de execução del grafo (`executar_task`) é vital para manter as duas camadas desacopladas.
2.  **Robusteza com Respostas Sem Conteúdo (HTTP 204)**:
    *   Entendi a importância de validar o status code da resposta HTTP e a existência de conteúdo antes de invocar métodos como `.json()`, prevenindo exceções de decode em requisições de remoção ou atualizações que retornem corpo vazio.

---

### 🚀 Meus Próximos Passos
*   Continuar testando a integração de novas ações e fluxos complexos de conversação no terminal.

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
