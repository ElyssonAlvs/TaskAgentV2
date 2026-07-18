# Diário de Aprendizado - TaskAgent V2 (Orquestração de Agentes de IA)

 Este diário serve para documentar os conceitos estudados, implementações técnicas e evoluções ao longo do desenvolvimento do TaskAgent V2.

---

## 🛡️ Tratamento de Erros Amigáveis na API e Resiliência HTTP — 17/07/2026 17:48

### 🛠️ O que eu Modifiquei

Implementei um tratamento robusto e amigável para erros de comunicação com a API (como erros 404 de recurso não encontrado, 422 de validação de dados e falhas de conexão) em ambos os motores de execução do TaskAgent.

*   **[crew/tools.py](file:///c:/Users/elyss/Desktop/Projects/TaskAgentV2/crew/tools.py)**:
    *   Substituí os blocos genéricos de captura de exceções nas ferramentas (`listar_tasks`, `criar_task`, `deletar_task`, `atualizar_task`, `buscar_task_por_titulo`).
    *   Adicionei a captura explícita de `httpx.HTTPStatusError`, fornecendo mensagens de erro traduzidas, polidas e amigáveis em português de acordo com o código de status HTTP (como 404 e 422).
    *   Melhorei a tratativa de `httpx.ConnectError` para alertar o usuário caso a API do `TaskManager` não esteja ativa em tempo de execução.
    *   Adicionei um tratamento genérico `except Exception` para garantir resiliência e evitar que falhas inesperadas interrompam a execução do fluxo CrewAI.
*   **[graph/nodes.py](file:///c:/Users/elyss/Desktop/Projects/TaskAgentV2/graph/nodes.py)**:
    *   Refatorei o nó `executar_task` (motor LangGraph) para capturar e traduzir erros HTTP e de conexão.
    *   Em vez de retornar erros técnicos crus (como `"Erro da API: 404"`), passei a injetar mensagens de erro contextualizadas no estado do grafo (como `"A tarefa ou o recurso solicitado não foi encontrado no servidor (Erro 404)."`).
    *   Adicionei tratamento genérico no bloco final do nó para aumentar a resiliência contra outras exceções inesperadas.

### 🧠 O que foi Aprendido / Conceitos Estudados

1.  **Tratamento Amigável de Exceções HTTP em Agentes**:
    *   Compreendi que os agentes de IA não devem expor detalhes técnicos crus do protocolo HTTP (como stack traces, URIs completas e nomes internos de exceções) para o usuário final. Exibir termos técnicos como `"Client error '404 Not Found'"` degrada a experiência do usuário.
    *   O ideal é mapear as exceções conhecidas (`HTTPStatusError` do `httpx` ou `HTTPError` de bibliotecas de requisição) e convertê-las em mensagens orientadas a negócios no idioma de uso do chatbot.
2.  **Resiliência Multi-Motor**:
    *   Fixei que ao manter múltiplos motores de execução (CrewAI e LangGraph), os cuidados de tratamento de erro devem ser replicados de forma consistente em ambos os núcleos para que a experiência do usuário permaneça uniforme, independentemente de qual orquestrador esteja ativo.
3.  **Segurança de Runtime em Ferramentas (Tool Safety)**:
    *   Aprendi que exceções não tratadas dentro de ferramentas customizadas do CrewAI podem quebrar a execução completa da cadeia de agentes, caindo no tratamento global do servidor. Capturar todas as exceções e retornar strings descritivas de erro permite que o agente Formatador do CrewAI interprete a falha e responda adequadamente ao usuário de forma transparente.

---

## 📦 Organização de Versionamento e Commits Semânticos — 15/07/2026 19:35

### 🛠️ O que eu Modifiquei

Realizei a revisão e separação de todas as alterações pendentes no repositório, agrupando-as por objetivo e aplicando as melhores práticas de *Conventional Commits* (commits semânticos) antes de enviar para o GitHub.

### 🧠 O que foi Aprendido / Conceitos Estudados

1.  **Conventional Commits e Versionamento Semântico**:
    *   Reforcei a prática de não usar `git commit -am "várias coisas"`. Separar as mudanças em blocos lógicos como `feat(crew): ...`, `fix(crew): ...` e `feat(core): ...` facilita o rastreamento do histórico, o *code review* e o *rollback* em caso de falhas específicas.
    *   Compreendi que separar as entregas mantém o repositório limpo e profissional, demonstrando maturidade técnica em metodologias ágeis.

---

## ⚙️ Alternância Dinâmica de Motor (CrewAI/LangGraph) e Melhorias na UI — 15/07/2026 19:00

### 🛠️ O que eu Modifiquei

Implementei suporte para alternância dinâmica de motores de execução (CrewAI e LangGraph) via variável de ambiente, além de realizar aprimoramentos na interface web para indicar qual motor está ativo.

*   **[main.py](file:///C:/Users/elyss/Desktop/Projects/TaskAgentV2/main.py)**:
    *   **Seleção de Engine**: Adicionei o controle baseado na variável de ambiente `AGENT_ENGINE`, permitindo usar o LangGraph como legado ou o CrewAI como padrão, sem precisar alterar código-fonte.
    *   **Rota `/engine`**: Criei um novo endpoint para que a interface web saiba qual motor está ativo no backend.
*   **[static/index.html](file:///C:/Users/elyss/Desktop/Projects/TaskAgentV2/static/index.html)**:
    *   **Aprimoramento Visual**: Atualizei o componente de "pensamento" (trace) para renderizar distintamente o ícone e o rótulo do motor sendo utilizado (CrewAI ou LangGraph).
    *   **Loading e Histórico**: Melhorei o estado de *loading* com animações de pontos dinâmicos e adicionei mensagens de feedback ao limpar o histórico do chat.
*   **[.env.example](file:///C:/Users/elyss/Desktop/Projects/TaskAgentV2/.env.example)**:
    *   Documentei explicitamente as novas opções de motor de IA disponíveis para inicialização.

### 🧠 O que foi Aprendido / Conceitos Estudados

1.  **Arquitetura Plug-and-Play (Feature Flags)**:
    *   Compreendi que o uso de variáveis de ambiente como *feature flags* (ex: `AGENT_ENGINE`) permite manter múltiplas implementações de um mesmo serviço lado a lado, facilitando testes comparativos sem perigo de quebras sistêmicas.
2.  **Sincronização Frontend/Backend**:
    *   Entendi a importância de sincronizar a UI com o estado configurado do backend. A consulta da rota `/engine` no carregamento da página garante que o usuário saiba exatamente qual orquestrador de IA está gerando suas respostas.

---

## 🧠 Ativação da Memória Semântica com Google Embeddings e Correção de Paginação na API — 15/07/2026 18:40

### 🛠️ O que eu Modifiquei

Eu reativei a memória semântica nativa do CrewAI (ChromaDB/LanceDB) utilizando a API do Google Gemini para geração de embeddings e corrigi a exibição de tarefas longas limitadas pela paginação padrão do backend.

*   **[crew/crew.py](file:///C:/Users/elyss/Desktop/Projects/TaskAgentV2/crew/crew.py)**:
    *   **Isolamento do Diretório de Banco**: Configurei a variável de ambiente `CREWAI_STORAGE_DIR` para `./db/crewai_storage` antes de instanciar a equipe. Isso isolou o banco de dados LanceDB em uma pasta local do projeto, resolvendo os travamentos e erros de concorrência causados pela tentativa de alterar a pasta padrão do sistema (`AppData/Local`), que estava bloqueada em tempo de execução pelos servidores uvicorn rodando no background.
    *   **Configuração de Embedder Google**: Alterei o modelo de embeddings para `"gemini-embedding-001"`, que é plenamente suportado pela minha chave do Google AI Studio, solucionando erros de modelo não encontrado (`404 NOT_FOUND`) que aconteciam ao tentar carregar a string genérica `"text-multilingual-embedding-002"`.
*   **[crew/tools.py](file:///C:/Users/elyss/Desktop/Projects/TaskAgentV2/crew/tools.py)**:
    *   **Otimização de Limites da API**: Adicionei o parâmetro `?limit=100` nas requisições `GET` das ferramentas `listar_tasks` e `buscar_task_por_titulo`. Isso evitou o bug visual em que tarefas recém-criadas com IDs superiores a 13 eram ocultadas da visualização do agente devido ao limitador padrão (`limit=10`) configurado na rota da API REST.
*   **Dependências**:
    *   Instalei a biblioteca oficial `google-generativeai` para habilitar o motor nativo de geração de embeddings do Google integrado ao ChromaDB/LanceDB do CrewAI.

---

### 🧠 O que foi Aprendido / Conceitos Estudados

1.  **Compatibilidade de Modelos de Embeddings do Google AI Studio**:
    *   Compreendi que a lista de modelos de embeddings de uma chave gratuita do Gemini pode variar, sendo fundamental validar os nomes disponíveis programaticamente via `genai.list_models()`. O modelo estável correto do ecossistema AI Studio para buscas semânticas padrão é `models/gemini-embedding-001` (e o novo `models/gemini-embedding-2`), que fornecem representações de 3072 dimensões de alto desempenho.
2.  **Locks de Banco e Ambientes Concorrentes com Servidores Locais**:
    *   Aprendi que processos em execução persistente (como os recarregamentos de uvicorn em terminais de desenvolvimento) bloqueiam de forma exclusiva os diretórios locais de bancos de dados como o SQLite e o LanceDB. Configurar caminhos alternativos isolados (através de variáveis de escopo local como `CREWAI_STORAGE_DIR`) permite o desenvolvimento ágil em paralelo sem necessitar parar serviços ativos.
3.  **Restrições Invisíveis de Paginação de API**:
    *   Fixei a necessidade de verificar os contratos e limites de paginação das rotas consumidas. Em endpoints que retornam listas, limites padrão pequenos no backend podem dar a falsa impressão de que dados criados não foram gravados no banco de dados, sendo essencial que o cliente declare ativamente o limite desejado na requisição.

---
---

## 🧠 Correção de Tool Calling e Validação no CrewAI com Groq (Llama 3) — 14/07/2026 15:25

### 🛠️ O que eu Modifiquei

Eu corrigi um erro crítico de execução no time CrewAI que impedia a utilização de memória com LLMs hospedados no Groq (como o Llama 3.3).

*   **[crew/tasks.py](file:///C:/Users/elyss/Desktop/Projects/TaskAgentV2/crew/tasks.py)**:
    *   **Estruturação de Output com Pydantic**: Criei o modelo Pydantic `IntencaoSchema` para validar a saída da primeira tarefa (`task_interpretar`).
    *   **Configuração de output_json**: Adicionei o parâmetro `output_json=IntencaoSchema` na inicialização de `task_interpretar` e simplifiquei sua descrição para extrair os dados conforme o schema. Isso eliminou a necessidade de o modelo tentar inferir formatos de JSON textuais que causavam erros de validação de ferramentas no Groq.

---

### 🧠 O que foi Aprendido / Conceitos Estudados

1.  **Compatibilidade de Tool Calling em Modelos Open-Source (Groq/Llama 3)**:
    *   Compreendi que modelos open-source executados no Groq tendem a entrar em modo de "tool use" de forma agressiva quando qualquer ferramenta está presente na chamada (o que ocorre automaticamente quando habilitamos a memória do CrewAI, que injeta as ferramentas `search_memory` e `save_to_memory`).
    *   Em modo de "tool use", requisições livres de texto para extrair JSON fazem com que o modelo tente formatar a saída como uma chamada de função (no padrão XML `<function=...>`), muitas vezes alucinando nomes de ferramentas inexistentes (como `interpretar_mensagem` ou `interpretar_intencao`) que não constam na lista original de ferramentas permitidas, gerando falhas no gateway do Groq.
2.  **Uso de Pydantic para Saídas Estruturadas (output_json)**:
    *   Aprendi a utilizar o parâmetro `output_json` do CrewAI com um modelo Pydantic (`BaseModel`) para impor uma estrutura rígida de retorno diretamente na API de completude. Isso informa ao orquestrador e à LLM exatamente como formatar o retorno estruturado, resolvendo de forma nativa e robusta conflitos causados pela presença indesejada de outras ferramentas.

---
---

## 🛡️ Resiliência contra Limites de Requisição (Groq Rate Limits) — 12/07/2026 18:28

### 🛠️ O que eu Modifiquei

Eu implementei mecanismos de resiliência e otimização de tokens para lidar com as severas limitações de TPM (Tokens Per Minute) da API gratuita do Groq quando orquestrada via CrewAI.

*   **[crew/tools.py](file:///C:/Users/elyss/Desktop/Projects/TaskAgentV2/crew/tools.py)**:
    *   **Otimização de Payload (Token Saving)**: Modifiquei as ferramentas `listar_tasks` e `buscar_task_por_titulo` para remover campos desnecessários (como `description` e outras chaves longas) antes de retornar os dados à LLM. Retornar apenas `id`, `title` e `status` poupou milhares de tokens do contexto, reduzindo drasticamente a chance de estouro de limite.
*   **[crew/agents.py](file:///C:/Users/elyss/Desktop/Projects/TaskAgentV2/crew/agents.py)**:
    *   Adicionei o parâmetro `num_retries=5` à inicialização da classe `LLM` do CrewAI. Isso instrui o LiteLLM a realizar automaticamente tentativas com recuo exponencial (*backoff*) caso receba um código HTTP 429 de Rate Limit.
*   **[main.py](file:///C:/Users/elyss/Desktop/Projects/TaskAgentV2/main.py)**:
    *   **Tratamento de Exceções no Chat**: Envolvi a execução do CrewAI (`executar_crew`) em um bloco `try-except` para capturar falhas. Se a requisição ao Groq estourar o limite mesmo com retentativas, o backend agora retorna uma mensagem clara sugerindo que o usuário tente novamente em instantes e informando que a ação de modificação pode ter tido sucesso na API. Isso previne quebras com status HTTP 500 e alertas genéricos de conexão no navegador.

---

### 🧠 O que eu Aprendi / Conceitos Estudados

1.  **Redução Preventiva de Janela de Contexto**:
    *   Compreendi que orquestradores de múltiplos agentes carregam muita informação em cada chamada (instruções de papéis, ferramentas e histórico). Sendo assim, qualquer dado retornado pelas ferramentas (como respostas de bancos de dados ou APIs) deve ser o mais conciso e filtrado possível para evitar estouro da cota de TPM da API do LLM.
2.  **Mecanismos de Retentativa com Backoff Exponencial**:
    *   Estudei como delegar para o LiteLLM a tratativa do status 429 (Rate Limit Reached), permitindo que ele silenciosamente aguarde alguns segundos antes de reenviar a requisição à IA, melhorando a experiência do usuário final.

---
---

## 🎨 Renderização Premium de Tabelas Markdown no Frontend - 12/07/2026 18:05

### 🛠️ O que eu Modifiquei

Eu melhorei a visualização das tarefas retornadas pelo CrewAI. Antes elas apareciam como listas simples, e agora são exibidas como tabelas bem formatadas na interface web. As alterações foram:

*   **[crew/agents.py](file:///C:/Users/elyss/Desktop/Projects/TaskAgentV2/crew/agents.py)**:
    *   Atualizei o `backstory` do agente **Formatador de Respostas**, adicionando uma instrução explícita para que ele sempre formate listas de tarefas como tabelas Markdown estritas, proibindo o uso de *bullet points*.
*   **[static/index.html](file:///C:/Users/elyss/Desktop/Projects/TaskAgentV2/static/index.html)**:
    *   Importei a biblioteca oficial `marked.js` para realizar a conversão completa e confiável de Markdown para HTML no cliente.
    *   Refatorei os seletores CSS das tabelas (antes `.tabela-tasks`) para `.resposta table`, garantindo que as tabelas renderizadas via Markdown herdem o mesmo design premium (cores, bordas e *hover states*) planejado anteriormente.
    *   **Post-Processing do DOM**: Adicionei um loop simples para verificar o texto das células geradas dinamicamente (ex: "done", "pending") e as envolvi novamente com as classes de badge (`<span class="status-badge status-done">`), recuperando o aspecto de UI rica e nativa.
    *   **Ajustes de UI/UX**: Centralizei a coluna de Status, reduzi sua largura total para 100px, e deixei os badges mais compactos (fonte 8.5px, padding reduzido, e um dot indicator menor) para otimizar o espaço visual da tabela.

---

### 🧠 O que eu Aprendi / Conceitos Estudados

1.  **Engenharia de Prompt para Formatação Estrita**:
    *   Aprendi que agentes LLM, como os do CrewAI, podem ser instruídos a usar formatos de saída rigorosos (como tabelas Markdown) mediante comandos determinísticos no seu `backstory` (ex: "MUITO IMPORTANTE: [...] DEVE SEMPRE").
2.  **Bibliotecas de Renderização Client-side**:
    *   Percebi que usar uma biblioteca dedicada como `marked.js` é infinitamente superior a criar substituições regex pontuais, pois ela lida nativamente com elementos complexos como tabelas (`<table>`, `<th>`, `<td>`), blocos de código e espaçamentos com total segurança.

---
---

## 🎨 Correção de Formatação de Markdown e Quebra de Linhas no Frontend - 12/07/2026 18:00

### 🛠️ O que eu Modifiquei

Eu corrigi um problema de formatação na interface web em que as quebras de linha e marcações em negrito (`**`) das respostas do CrewAI não eram exibidas corretamente. As alterações foram:

*   **[static/index.html](file:///C:/Users/elyss/Desktop/Projects/TaskAgentV2/static/index.html)**:
    *   **CSS (.resposta)**: Adicionei a regra `white-space: pre-wrap;` para garantir que as quebras de linha (`\n`) enviadas pela resposta final do agente sejam renderizadas no navegador em vez de colapsarem.
    *   **JavaScript (adicionarRespostaAgente)**: Substituí a atribuição direta por `.textContent` para usar um conversor regex básico de markdown para HTML seguro (`.innerHTML`). Ele converte marcações de negrito (`**Texto**`) e itálico (`*Texto*`) enquanto previne falhas de segurança escapando tags indesejadas.

---

### 🧠 O que eu Aprendi / Conceitos Estudados

1.  **Renderização de Textos Dinâmicos e Espaçamento em HTML**:
    *   Compreendi que, por padrão, o HTML colapsa espaços múltiplos e quebras de linha (`\n`) em um único caractere de espaço. O uso de `white-space: pre-wrap;` permite o comportamento ideal de texto corrido mantendo a diagramação de quebras e listas originadas do LLM.
2.  **Conversão de Rich Text no Client-side**:
    *   Entendi a importância de sanitizar entradas de texto de terceiros (como LLMs) antes de renderizá-las via `innerHTML`. Escapar os caracteres `<` e `>` e aplicar substituições controladas com expressões regulares é uma solução rápida e eficiente para suportar formatação básica sem comprometer a segurança.

---
---

## 🎨 Integração do CrewAI no Frontend e Documentação Completa — 11/07/2026 20:29

### 🛠️ O que eu Modifiquei

Eu finalizei a conexão do time CrewAI à interface web do usuário e estruturei toda a documentação pública (README) do projeto de forma didática.

*   **[main.py](file:///C:/Users/elyss/Desktop/Projects/TaskAgentV2/main.py)**:
    *   Substituí a lógica antiga baseada em `executar_agente` (LangGraph) para invocar `executar_crew`.
    *   Ajustei o payload de resposta esperado pela UI: substituí o envio do array de `tasks` (que era renderizado numa tabela HTML) apenas pela resposta em formato textual rico formatada pelo agente Formatador do CrewAI.
    *   Alteri as mensagens estáticas de "Pensamento" no frontend para refletir a nova cadeia multiagente, indicando a atuação do Interpretador, Executor e Formatador de forma unificada.
*   **[README.md](file:///C:/Users/elyss/Desktop/Projects/TaskAgentV2/README.md)**:
    *   Reescrevi completamente o README para servir como "cartão de visitas" da aplicação. Adicionei seções fundamentais exigidas em padrões de mercado (O que é o projeto, Tecnologias Usadas, Como Rodar Localmente em dois terminais paralelos).
    *   Incluí um diagrama **Mermaid** macro mostrando as camadas (Cliente -> FastAPI -> CrewAI -> Backend API).
*   **Organização de Arquivos**:
    *   Movi o script `test_crew.py` solto na raiz para dentro de uma nova pasta `tests/` (`tests/test_crew.py`), mantendo a raiz limpa e um aspecto profissional de projeto bem estruturado.
    *   Criei o arquivo de exemplo `[`.env.example`](file:///C:/Users/elyss/Desktop/Projects/TaskAgentV2/.env.example) para expor as variáveis de ambiente necessárias (como a `GROQ_API_KEY`) sem vazar credenciais ativas, após confirmar o isolamento via `.gitignore`.

---

### 🧠 O que eu Aprendi / Conceitos Estudados

1.  **Refatoração e Adaptação de Interfaces (Contracts)**:
    *   Entendi como é vital adaptar a rota de comunicação (endpoints FastAPI) e as respostas da interface quando há uma mudança massiva no núcleo de orquestração (de LangGraph puro para CrewAI), lidando com as diferentes formas em que cada framework emite *outputs* finais.
2.  **Boas Práticas de Repositórios Open Source e Portfólio**:
    *   Pratiquei a padronização e documentação de projetos. A presença de um arquivo de exemplo `.env.example`, organização correta de testes fora da raiz principal, e um README completo com diagramas reduzem a fricção no *onboarding* de desenvolvedores e validam o aspecto de "projeto finalizado" e maduro.

---
---

## 🤖 Resolução do ValidationError e Configuração da LLM Groq no CrewAI - 11/07/2026 20:02

### 🛠️ O que eu Modifiquei

Eu corrigi o erro de validação do Pydantic (`ValidationError`) que ocorria ao tentar rodar o script de equipe de agentes (`test_crew.py`), mantendo o uso do modelo selecionado pelo usuário (`llama-3.3-70b-versatile`). As alterações foram:

*   **[crew/agents.py](file:///C:/Users/elyss/Desktop/Projects/TaskAgentV2/crew/agents.py)**:
    *   Substituí a classe `ChatGroq` do LangChain pela classe nativa `LLM` do CrewAI, configurando-a com o identificador `"groq/llama-3.3-70b-versatile"`.
    *   Mantive o monkey-patch que desativa a injeção automática de `cache_breakpoint` pelo CrewAI nas mensagens para o Groq, evitando erros de parâmetro não suportado pela API de destino.

---

### 🧠 O que eu Aprendi / Conceitos Estudados

1.  **Compatibilidade de Modelos de Chat nos Agentes CrewAI**:
    *   Notei que instâncias de `ChatGroq` geram erros de validação Pydantic no CrewAI porque a validação do parâmetro `llm` exige objetos que herdem de `BaseLLM` ou a classe nativa `LLM` da própria biblioteca.
    *   Reforcei que, ao usar a classe `LLM` do CrewAI para se conectar ao Groq via LiteLLM, a especificação correta do modelo mantendo as preferências do usuário (`groq/llama-3.3-70b-versatile`) resolve o acoplamento do tipo do objeto sem alterar o modelo selecionado.

---
---

## 🛠️ Equipando Agentes com Tools no CrewAI — 11/07/2026 19:53

### 🛠️ O que eu Modifiquei

Eu equipei o agente executor do CrewAI com ferramentas customizadas que realizam requisições HTTP reais à API do `TaskManager`, garantindo que os dados não sejam alucinados pelas LLMs.

*   **[crew/tools.py](file:///C:/Users/elyss/Desktop/Projects/TaskAgentV2/crew/tools.py)**:
    *   Criei este novo módulo para definir as ferramentas do time utilizando o decorador `@tool` do CrewAI.
    *   **Listar Tasks**: Envia requisição `GET` para `/v1/tasks/`.
    *   **Criar Task**: Envia requisição `POST` formatando o campo `title` esperado pelo backend.
    *   **Deletar Task**: Envia requisição `DELETE` utilizando o ID correspondente.
    *   **Atualizar Task**: Envia requisição `PUT` para alterar o status/título.
    *   **Buscar Task por Título**: Retorna IDs correspondentes a buscas de títulos textuais.
*   **[crew/agents.py](file:///C:/Users/elyss/Desktop/Projects/TaskAgentV2/crew/agents.py)**:
    *   Importei as ferramentas criadas e as associei como recursos ao agente `Executor de Tasks` (`tools=[...]`).
*   **[test_crew.py](file:///C:/Users/elyss/Desktop/Projects/TaskAgentV2/test_crew.py)**:
    *   Refatorei o script de testes para cobrir sequencialmente múltiplos cenários (listagem, criação e deleção) em lote.

---

### 🧠 O que eu Aprendi / Conceitos Estudados

1.  **Ferramentas Customizadas como Habilidades (Agent Skills)**:
    *   Entendi como dar poder de ação prática a agentes de IA. Através de decorações do tipo `@tool`, escrevemos código Python convencional (como chamadas HTTP) cuja finalidade e parâmetros são explicados em *docstrings*.
    *   O LLM lê essas explicações e decide dinamicamente quando usá-las, coletando as informações do contexto de entrada.
2.  **Saneamento de Contratos de API**:
    *   Evitei que os agentes falhassem garantindo que as chamadas usassem a rota correta `/v1/tasks/` do ecossistema e fizessem a tradução do payload do usuário (`titulo` -> `title`).

---
---

## 🛠️ Correção e Configuração dos LLMs no CrewAI - 11/07/2026 19:40

### 🛠️ O que eu Modifiquei

Eu corrigi os erros de validação e execução ao rodar a equipe multiagentes (`test_crew.py`) usando o CrewAI. As alterações realizadas foram:

*   **Instalação de Dependências**: Adicionei a biblioteca `litellm` ao projeto (`uv add litellm`) para suportar a conexão nativa com provedores externos no CrewAI.
*   **[crew/agents.py](file:///C:/Users/elyss/Desktop/Projects/TaskAgentV2/crew/agents.py)**:
    *   **Migração de LLM**: Removi a dependência do `ChatGroq` do LangChain e adotei a classe nativa `LLM` do CrewAI.
    *   **Atualização do Modelo**: Substituí o modelo descontinuado `llama3-70b-8192` pelo modelo ativo `llama-3.3-70b-versatile` no Groq.
    *   **Monkey-Patch de Caching**: Adicionei um patch para desativar a injeção automática de `cache_breakpoint` pelo CrewAI nas mensagens do Groq. Isso evita o erro `BadRequestError: 'messages.0': property 'cache_breakpoint' is unsupported`.

---

### 🧠 O que eu Aprendi / Conceitos Estudados

1.  **Diferenças de Interface de LLM entre Frameworks**:
    *   Entendi que a validação de tipos de agentes no CrewAI (versões mais recentes) exige instâncias do tipo nativo `LLM` ou strings, rejeitando instâncias de `ChatGroq` (que herdam de `BaseChatModel` do LangChain).
    *   Compreendi que o CrewAI utiliza `LiteLLM` internamente para gerenciar conexões de modelo com diferentes provedores usando um esquema unificado de strings (como `groq/nome_do_modelo`).
2.  **Incompatibilidade de Parâmetros de API (Context Caching)**:
    *   Notei que parâmetros automáticos injetados por frameworks (como `cache_breakpoint` do Anthropic) podem causar erros fatais ao serem passados para provedores que ainda não os suportam (como Groq). A aplicação de monkey-patches dinâmicos é uma estratégia de contorno útil nesses casos de incompatibilidade de versão.

---
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
---

## 🌐 Interface Web para o TaskAgent V2 - 11/07/2026 17:00

### 🛠️ O que eu Modifiquei

Nesta etapa, eu transformei o meu agente CLI em um serviço web completo com interface gráfica no navegador. As principais alterações foram:

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
