# Auditoria e status de finalização

## Escopo e limitações

Auditoria realizada sobre os arquivos locais, sem escrita no Xano e sem
operações em dados reais. O manual do trabalho e os requisitos oficiais do
professor não foram encontrados no repositório; por isso, esta matriz avalia
somente requisitos documentados no projeto e não declara conformidade
acadêmica integral.

## Matriz de requisitos e evidências

| Requisito | Funcionalidade correspondente | Arquivo ou endpoint | Evidência | Status | Pendências |
|---|---|---|---|---|---|
| Autenticação, sessão e logout | Login por token e encerramento da sessão Streamlit | `app.py`; `usuario_login_POST.xs` | Tela de login e logout presentes; resposta de login validada no frontend | Parcialmente atendido | Logout limpa a sessão da interface; invalidação do token no backend não foi comprovada |
| Perfis de administrador e operador | Menus e rotas administrativas | `app.py`; endpoints de vaga, usuário e financeiro | A interface esconde opções administrativas do operador; endpoints administrativos têm verificações de perfil | Parcialmente atendido | `veiculo` e `mensalista` não declaram autenticação nos endpoints de cadastro/listagem |
| Dashboard e disponibilidade | Totais, livres, ocupadas e grade de vagas | `app.py`; `vaga_ocupacao_GET.xs`; `vaga_list_GET.xs` | Chamadas e cálculos presentes; XanoScript validado | Parcialmente atendido | Não foi feita validação manual nesta auditoria contra dados do workspace |
| Cadastro e consulta de veículos | Cadastro e listagem de veículos | `app.py`; `veiculo_create_POST.xs`; `veiculo_list_GET.xs` | Telas e rotas presentes | Parcialmente atendido | Endpoints sem `auth`; exigir autorização no backend antes de afirmar proteção |
| Cadastro e consulta de mensalistas | Cadastro, vigência e vínculo com veículo | `app.py`; `mensalista_create_POST.xs`; `mensalista_list_GET.xs` | Telas e rotas presentes | Parcialmente atendido | Endpoints sem `auth`; exigir autorização no backend |
| Entrada, saída e cobrança | Registro transacional e cálculo de tarifa | `entrada_POST.xs`; `saida_POST.xs` | Validação sintática aprovada; regra atual: 10 min de tolerância, R$ 5 por fração de 15 min, teto de R$ 50 e isenção de mensalista válido | Parcialmente atendido | Teste de fluxo com dados reais não executado; não se deve usar produção para testar escrita |
| Regra de mensalista | Isenção durante status e vigência válidos | `saida_POST.xs` | Verificação de status, datas e fuso `America/Sao_Paulo` no código | Parcialmente atendido | Resultado funcional no Xano não foi revalidado com massa de teste isolada |
| Entradas duplicadas e concorrência | Bloqueios por veículo/vaga e transação | `entrada_POST.xs`; `saida_POST.xs`; `test_concurrency.py` | Verificações existem e a sintaxe foi validada | Não validado | O script de concorrência faz requisições mutativas reais; não foi executado nesta auditoria |
| Gerenciamento de vagas | Cadastro, edição e desativação lógica | `vaga_create_POST.xs`; `vaga_update_PATCH.xs`; `app.py`; `vaga.xs` | Regras de administrador e validações presentes; sintaxe validada | Parcialmente atendido | Testes de autorização pendentes; o enum local ainda inclui `manutencao`, mas a especificação principal descreve somente `livre` e `ocupada` |
| Gerenciamento de usuários | Listagem e cadastro por administrador | `usuario_create_POST.xs`; `usuario_list_GET.xs`; `app.py` | Rotas e barreiras administrativas presentes no código | Parcialmente atendido | Teste manual admin/operador pendente |
| Faturamento, ticket médio e histórico | Indicadores e movimentações encerradas | `financeiro_GET.xs`; `app.py` | O endpoint restringe admin, exclui canceladas, usa `exit_time`, `amount` e `America/Sao_Paulo`; o usuário informou validação visual no Xano/Streamlit | Atendido | Nenhuma pendência funcional identificada nesta revisão |
| Filtros de período | Datas inicial/final opcionais no endpoint | `financeiro_GET.xs`; `app.py` | Endpoint aceita `start_date` e `end_date` opcionais | Parcialmente atendido | A interface Streamlit não apresenta controles de período |
| Cache e limite da API | Cache de GET por sessão e mensagem para HTTP 429 | `app.py` | TTL de 30 s, invalidação por versão dos dados e tratamento de 429 no código | Parcialmente atendido | Limite real do Xano não foi provocado deliberadamente |
| Valores nulos, datas e gráfico | Histórico e agregação diária | `app.py` | Pandas disponível; conversão de epoch/ISO, valores nulos e fuso local tratados; teste com resposta simulada registrado no checklist | Parcialmente atendido | Falta validação visual manual final no workspace de demonstração |
| Requisitos oficiais do professor | Comparação com manual e rubrica | Documentos do projeto | Busca no repositório não encontrou manual nem rubrica | Não validado | Solicitar/incluir o manual para concluir a análise acadêmica |

### Percentual verificável

Considerando os 15 itens da matriz, atribui-se 1 ponto a “Atendido”, 0,5 a
“Parcialmente atendido” e 0 a “Não validado”: **46,7% (7/15 pontos)**. Esse
índice mede somente a evidência auditável nesta revisão; não é uma afirmação
de conformidade acadêmica nem um percentual global de qualidade do sistema.

## Verificações executadas

| Verificação | Resultado |
|---|---|
| `python -m py_compile app.py` | Aprovado |
| Inicialização Streamlit com AppTest | Aprovada sem exceções na tela de login e páginas simuladas |
| Página financeira com datas/nulos e acesso por perfil | Métricas, histórico, gráfico e menu admin/operador aprovados com respostas simuladas |
| Cache por sessão e limite HTTP 429 | Cache GET reutilizado na mesma sessão e `Retry-After` exibido em teste simulado |
| Renderização do nome de usuário | Valor com marcação HTML escapado no cabeçalho, verificado por AppTest |
| Dependências no `.venv` | Streamlit, Pandas e Requests disponíveis |
| Validação XanoScript local | 58 arquivos válidos; nenhum erro de sintaxe |
| `npx openspec validate dashboard-financeiro --strict` | Aprovado |
| Dry-run seletivo do Xano | “No changes to push” para `api/parking/**`, `table/movimentacao.xs` e `table/vaga.xs` |
| Concorrência ou fluxos mutativos no workspace real | Não executados |

## Achados e bloqueios

1. Os endpoints de cadastro e listagem de veículo e mensalista não têm
   `auth = "usuario"` nem verificação de perfil. A interface não substitui
   autorização no backend. Não foram alterados porque pertencem a uma Change
   funcional distinta da Change financeira.
2. O script `test_concurrency.py` pode gravar no workspace Xano; não executar
   contra dados reais.
3. O dry-run geral do Xano inclui arquivos de template e continua inadequado
   para publicação geral. O dry-run seletivo das rotas e tabelas de
   estacionamento não encontrou diferenças.
4. `docs/domain-model.md` continha uma tarifa divergente; foi alinhado à regra
   encontrada no endpoint de saída.
5. A interface não possui filtros de período, embora o endpoint aceite datas.
6. O scanner identificou um valor literal no campo `Password` em páginas de
   demonstração já rastreadas (`api/authentication/1_start_here_demo_page_GET.xs`
   e `xano/api/authentication/1_start_here_demo_page_GET.xs`). Não foi possível
   confirmar se é apenas exemplo; os valores foram omitidos e os arquivos não
   foram incluídos no staging. Confirmar e substituir/rotacionar se forem reais.
7. `.vscode/mcp.json` e arquivos `.gemini/` já estão rastreados; `.gitignore`
   não os remove do histórico. Permanecem fora do staging desta entrega.
8. O cliente HTTP agora captura exceções específicas do Requests. O nome de
   usuário é escapado antes da renderização HTML, confirmado por AppTest.

## Xano e OpenSpec

- Nenhuma publicação foi realizada. Não há comandos individuais de publicação
  necessários para o subconjunto auditado, pois o dry-run não apontou mudanças.
- Não executar push geral. Se uma alteração futura for aprovada, iniciar com
  `xano workspace push -d ./xano --dry-run` e revisar a lista antes de publicar.
- A Change `dashboard-financeiro` passou na validação estrita, teve as tarefas
  concluídas (6/6), sincronizou a especificação principal e foi arquivada em
  `openspec/changes/archive/2026-11-26-dashboard-financeiro/`.
- `openspec validate --specs` passou com um aviso preexistente de requisito
  extenso em outra parte da especificação principal.

## Git e entrega

- Branch observada: `main`.
- Repositório remoto observado: `Larissaglima12/PROJETO-ESTACIONAMENTO`.
- Nenhum commit ou push foi realizado.
- Staging seletivo preparado e revisado; commit e push aguardam confirmação
  humana. `test_concurrency.py` e alterações de configuração de agentes ficaram
  fora do staging.

## Próximos passos antes da gravação

1. Tratar os endpoints de veículos e mensalistas em uma Change própria e
   validar a autorização no backend.
2. Fazer a demonstração com dados sintéticos e sem mostrar token, senha,
   e-mail ou dados pessoais.
3. Validar visualmente o login, os dois perfis, ocupação, movimentação e
   financeiro em ambiente de demonstração.
4. Confirmar com o professor a duração e os critérios oficiais; o manual não
   está disponível no repositório.
5. Revisar a lista do staging, mantendo fora temporários, arquivos privados,
   scripts que escrevem no Xano e qualquer credencial.
