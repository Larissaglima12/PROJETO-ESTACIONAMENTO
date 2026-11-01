# AGENTS.md

Regras para agentes de IA que trabalham neste projeto.

## Contexto

Antes de qualquer alteração significativa, consulte:
- `docs/project-overview.md`
- `docs/domain-model.md`
- `openspec/config.yaml`
- `openspec/specs/`

## Fluxo de trabalho

- Mudanças funcionais devem seguir o OpenSpec: Explore, Propose, Review,
  Apply e Archive.
- Não implemente funcionalidades nem crie Changes sem solicitação
  explícita do usuário.
- Não altere código ou banco de dados fora do escopo da Change atual.

## Arquitetura

- Backend e banco: Xano, escrito em XanoScript.
- Não presuma a sintaxe do XanoScript. Consulte o Xano Developer MCP ou a
  documentação oficial atual e valide o código antes de entregar.
- Reutilize o que já existe e evite duplicação.

## Frontend

O frontend do projeto deve ser implementado exclusivamente com Streamlit.

Não introduza React, Vue, Angular, Next.js ou outra tecnologia de
frontend para substituir ou complementar o Streamlit, salvo quando houver
uma alteração arquitetural explicitamente aprovada para o projeto.

## Segurança

- Regras de autorização e de negócio ficam no backend.
- Nunca coloque tokens, senhas ou chaves em arquivos versionados.
- Não proponha o uso do Xano MCP Server com acesso direto ao workspace.
  A sincronização é feita pelo Xano CLI.

## Sincronização com o Xano

- Os arquivos `.xs` ficam na pasta `xano/`.
- O envio ao Xano é feito pelo usuário com `xano workspace push`. Sugira
  sempre o `--dry-run` antes.
- Antes de trabalhar, o usuário pode rodar `xano workspace pull` para
  evitar conflitos.

## Verificação

- Toda mudança funcional deve ter uma estratégia de verificação.
- Não marque tarefas como concluídas sem verificar.

## Idioma

Escreva a documentação e os artefatos do OpenSpec em português
brasileiro.