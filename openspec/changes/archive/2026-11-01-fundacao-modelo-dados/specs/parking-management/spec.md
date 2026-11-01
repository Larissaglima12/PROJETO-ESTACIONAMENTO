## ADDED Requirements

### Requirement: Referências da tabela movimentacao (estado atual)
A tabela `movimentacao` SHALL referenciar `veiculo` por `veiculo_id`, `vaga` por `vaga_id` e `usuario` por `usuario_id`, em `xano/table/movimentacao.xs`.

#### Scenario: Referências conferidas no workspace
- **WHEN** o arquivo `xano/table/movimentacao.xs` é verificado
- **THEN** os três campos apontam para as tabelas `veiculo`, `vaga` e `usuario`, e o Xano está igual ao arquivo (o dry-run não lista diferença nas tabelas do projeto).

### Requirement: Comportamento atual dos endpoints de estacionamento (as-is)
Os endpoints do grupo Estacionamento SHALL permanecer com a lógica atual nesta Change, que apenas a documenta.

#### Scenario: Entrada de veículo
- **WHEN** `entrada_POST` é chamado
- **THEN** o endpoint grava uma movimentação com `entry_time` agora e marca a vaga como ocupada
- **AND** não verifica se a vaga está livre, se o veículo já está estacionado nem se veículo e vaga existem
- **AND** recebe `usuario_id` no corpo da requisição.

#### Scenario: Saída de veículo
- **WHEN** `saida_POST` é chamado
- **THEN** o endpoint grava `exit_time` agora, define o valor fixo de R$ 15,00 e libera a vaga
- **AND** não calcula tarifa pelo tempo de permanência e não bloqueia saída duplicada.

#### Scenario: Cadastros e consultas
- **WHEN** `veiculo_create_POST`, `mensalista_create_POST`, `usuario_create_POST` ou os endpoints de listagem são chamados
- **THEN** os endpoints cadastram ou listam os registros
- **AND** `veiculo_create_POST` grava a placa em maiúsculas sem bloquear placa duplicada
- **AND** `mensalista_create_POST` cria o mensalista com status ativo sem validar vigência.

#### Scenario: Ocupação das vagas
- **WHEN** `vaga_ocupacao_GET` é chamado
- **THEN** o endpoint retorna a contagem de vagas livres e ocupadas.

### Requirement: Regras alvo de cobrança e operação (alvo)
O sistema SHALL, em Change futura, implementar as regras de negócio de referência:
- Cobrança de saída de veículos avulsos em frações de 15 minutos (R$ 3,00 por fração), com até 15 minutos gratuitos e teto diário de R$ 25,00.
- Isenção de cobrança para mensalistas ativos.
- Validação de vaga livre na entrada e bloqueio de entradas/saídas duplicadas.
- Validação de placas duplicadas e `usuario_id` obtido diretamente do token de autenticação.

#### Scenario: Planejamento das regras alvo
- **WHEN** o sistema for evoluído em Changes futuras
- **THEN** as regras de cobrança por fração de 15 min, isenção de mensalistas e validações de unicidade serão aplicadas.

### Requirement: Pendências e lacunas identificadas
O sistema SHALL registrar todas as pendências identificadas para tratamento em andamentos futuros do projeto:
1. Validação de vaga livre na entrada.
2. Prevenção de entrada duplicada para o mesmo veículo.
3. Prevenção de saída duplicada.
4. Substituição da tarifa fixa de R$ 15,00 pelo cálculo dinâmico baseado no tempo.
5. Verificação de placa duplicada no cadastro de veículos.
6. Obtenção do `usuario_id` a partir do token de autenticação em vez do corpo da requisição.
7. Validação de status do usuário no login.
8. Ausência de endpoint de criação de vaga (`vaga_create_POST`).
9. `usuario_create_POST` e `usuario_list_GET` sem autenticação adequada.
10. Login fora do grupo Estacionamento (atualmente no grupo `Authentication` usando a tabela `user`).
11. Existência de duas tabelas de usuário (`user` do template e `usuario` do projeto).
12. Bloqueio de push (`xano workspace push`) devido aos endpoints `auth/` do template.
13. Registro de teste em `movimentacao` contendo campos vazios.

#### Scenario: Listagem de pendências técnicas
- **WHEN** o projeto for auditado para novas implementações
- **THEN** as pendências de validação de vagas, duplicidade e autenticação estarão mapeadas.
