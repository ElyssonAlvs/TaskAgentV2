---
name: learning-diary
description: >-
  Use esta skill para registrar e documentar os aprendizados, progressos, alterações no código e conceitos teóricos de Orquestração de Agentes no diário de aprendizado (LEARNING_DIARY.md) do usuário.
---

# Skill de Diário de Aprendizado (Learning Diary)

Esta skill permite documentar as evoluções do projeto, o aprendizado teórico sobre orquestração de agentes de IA, conceitos discutidos e as modificações feitas pelo usuário. Ela deve atualizar cumulativamente o arquivo `LEARNING_DIARY.md` na raiz do projeto.

## Diretrizes de Execução

1. **Coleta de Informações**:
   - Obtenha a data e hora atual do sistema.
   - Verifique quais arquivos foram modificados (ou novos arquivos criados) usando comandos do Git (como `git log -1` ou `git diff --name-only`).
   - Identifique no chat os tópicos que o usuário estudou ou o que ele aprendeu recentemente (por exemplo, com ajuda de outros LLMs como Claude).

2. **Geração do Registro**:
   - Cada entrada do diário deve ser adicionada **no topo** (logo abaixo do título principal) do arquivo `LEARNING_DIARY.md`, mantendo os registros anteriores abaixo.
   - Formate a nova entrada com um título em markdown (nível 2, `## [Título da Entrada] - DD/MM/AAAA HH:MM`) e as seções descritas abaixo.

3. **Estrutura da Entrada e Tom de Voz**:
   - **Tom de Voz**: A escrita deve ser feita estritamente em **primeira pessoa do singular** (ex: "Eu alterei", "Eu aprendi", "Minha implementação"). O diário reflete a perspectiva de estudo pessoal do usuário.
   - **Data e Hora**: O timestamp da criação da entrada.
   - **O que foi Modificado**: Uma lista clara dos arquivos criados ou modificados, detalhando de forma pessoal a finalidade de cada alteração.
   - **O que foi Aprendido / Conceitos Estudados**: Explicações teóricas detalhadas dos conceitos de IA e Orquestração envolvidos (ex: State Graphs, Transições de Estado, Conditional Edges, Mocking de chamadas, Histórico de Diálogo, etc.).
   - **Próximos Passos / Plano de Estudos**: O que está planejado para ser estudado ou implementado a seguir.

4. **Persistência**:
   - Se o arquivo [LEARNING_DIARY.md](file:///C:/Users/elyss/Desktop/Projects/TaskAgentV2/LEARNING_DIARY.md) não existir, crie-o com um cabeçalho principal formatado e visualmente elegante:
     ```markdown
     # Diário de Aprendizado - TaskAgent V2 (Orquestração de Agentes de IA)

     Este diário serve para documentar os conceitos estudados, implementações técnicas e evoluções ao longo do desenvolvimento do TaskAgent V2.
     ```
   - Caso o arquivo já exista, faça a inserção da nova entrada logo abaixo do cabeçalho principal e acima da última entrada registrada.
