# Checklist de testes e demonstração

## Evidências já registradas

- [x] `python -m py_compile app.py`.
- [x] Inicialização do Streamlit com AppTest na tela de login, sem exceções.
- [x] Teste local da página financeira com resposta HTTP simulada contendo
      valores nulos e datas epoch/ISO; nenhuma chamada de escrita ao Xano.
- [x] AppTest com respostas simuladas para menu admin/operador, cache de GET
      por sessão e HTTP 429 com `Retry-After`; nenhuma escrita ao Xano.
- [x] AppTest confirmou que o nome do usuário é escapado antes de ser renderizado
      no cabeçalho HTML.
- [x] Dependências Streamlit, Pandas e Requests encontradas no `.venv`.
- [x] Validação de sintaxe dos 58 arquivos `.xs`.
- [x] `npx openspec validate dashboard-financeiro --strict`.
- [x] Dry-run seletivo do Xano retornou “No changes to push”.

## Verificações manuais pendentes

Faça estes testes apenas em ambiente de demonstração isolado, com dados
sintéticos e autorização para operações de escrita.

### Autenticação e perfis

- [ ] Administrador faz login; confirmar menu administrativo.
- [ ] Operador faz login; confirmar que as opções administrativas ficam
      ocultas.
- [ ] Logout limpa o token e os dados de sessão no Streamlit.
- [ ] Senha incorreta apresenta erro sem revelar se o e-mail existe.
- [ ] Confirmar autorização no backend para cada endpoint usado pelo perfil.

### Dashboard, vagas e cadastros

- [ ] Comparar total/livres/ocupadas com a listagem de vagas ativas.
- [ ] Confirmar que vagas inativas não entram nos totais nem recebem entradas.
- [ ] Testar cadastro, edição e desativação de vaga com administrador e
      rejeição com operador.
- [ ] Validar cadastro/listagem de veículos e mensalistas somente após
      autorização dos endpoints no backend.

### Entrada, saída e cobrança

- [ ] Em ambiente isolado, registrar entrada e confirmar vaga ocupada.
- [ ] Tentar entrada repetida para veículo e vaga; confirmar rejeição.
- [ ] Registrar saída e confirmar cálculo/teto e vaga livre.
- [ ] Confirmar isenção de mensalista ativo dentro da vigência e cobrança
      avulsa para mensalista vencido/inativo.
- [ ] Não executar `test_concurrency.py` contra o workspace com dados reais:
      o script dispara requisições que podem gravar registros.

### Faturamento

- [ ] Confirmar que somente administrador acessa os dados financeiros também
      pelo endpoint, não apenas pelo menu.
- [ ] Conferir soma diária, soma mensal, ticket médio, contagem e histórico
      contra movimentações sintéticas finalizadas.
- [ ] Confirmar exclusão de movimentações canceladas e abertas.
- [ ] Validar datas no limite de dia/mês em `America/Sao_Paulo`.
- [ ] Confirmar gráfico com soma dos valores por dia e registros nulos/invalidos.
- [ ] Filtros de período ainda não estão expostos na interface.

### Limite da API e apresentação

- [ ] Confirmar a mensagem para HTTP 429 sem provocar limite no serviço real.
- [ ] Conferir recuperação após expiração/invalidação do cache da sessão.
- [ ] Usar apenas dados sintéticos; não exibir credenciais, tokens ou dados de
      clientes.
- [ ] Confirmar com o professor a duração oficial; o manual não foi localizado.
