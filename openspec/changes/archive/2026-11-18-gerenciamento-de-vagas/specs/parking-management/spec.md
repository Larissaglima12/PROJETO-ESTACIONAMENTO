# Spec Delta

## ADDED Requirements

### Requirement: Cadastro de vagas restrito a administradores com validações numéricas
O sistema SHALL permitir o cadastro de novas vagas exclusivamente para administradores autenticados (`admin`), exigindo um número inteiro único, positivo (maior ou igual a 1), e rejeitando números duplicados, zero, negativos ou não inteiros.

#### Scenario: Administrador cadastra nova vaga válida com sucesso
- **WHEN** um administrador autenticado envia um número inteiro único e positivo (ex: número 31)
- **THEN** o sistema cadastra a vaga com status inicial `livre` e `active = true`

#### Scenario: Operador tenta cadastrar vaga
- **WHEN** um operador autenticado tenta cadastrar uma nova vaga
- **THEN** o sistema rejeita a operação com erro de acesso negado (403)

#### Scenario: Cadastro rejeita número duplicado, zero, negativo ou não inteiro
- **WHEN** um administrador tenta cadastrar uma vaga com número já existente, zero, negativo ou decimal
- **THEN** o sistema rejeita a operação com erro de validação

### Requirement: Inicialização, capacidade planejada e regularização de vagas
O sistema SHALL iniciar novas vagas com o status `livre` e `active = true`, considerando capacidade inicial planejada de 30 vagas sem limite máximo fixo, e SHALL permitir a regularização da vaga legada `number = 0` para um número positivo disponível preservando seu ID e histórico.

#### Scenario: Vaga legada number = 0 é regularizada
- **WHEN** a vaga com `number = 0` é atualizada administrativamente para um número positivo válido
- **THEN** o ID da vaga e suas chaves estrangeiras históricas em movimentações permanecem intactos

### Requirement: Edição de vagas restrita a administradores e proteção contra duplicidade
O sistema SHALL permitir a edição de informações de vagas exclusivamente por administradores autenticados, rejeitando edições por operadores (403), números duplicados/inválidos e alterações manuais de status incompatíveis com movimentações abertas.

#### Scenario: Administrador edita dados da vaga com sucesso
- **WHEN** um administrador autenticado atualiza o número ou tipo de uma vaga com dados válidos e únicos
- **THEN** o sistema atualiza o registro com sucesso

#### Scenario: Operador tenta editar vaga
- **WHEN** um operador autenticado tenta editar uma vaga
- **THEN** o sistema rejeita a operação com erro de acesso negado (403)

#### Scenario: Edição rejeita número duplicado ou inválido
- **WHEN** um administrador tenta atualizar uma vaga com número duplicado, zero, negativo ou decimal
- **THEN** o sistema rejeita a operação

#### Scenario: Edição impede alteração manual de status incompatível com movimentação aberta
- **WHEN** um administrador tenta alterar manualmente o status de uma vaga para `livre` enquanto houver movimentação aberta vinculada
- **THEN** o sistema rejeita a alteração para evitar inconsistência operacional

### Requirement: Desativação lógica restrita, segura e preservação histórica de vagas
O sistema SHALL permitir a desativação lógica de vagas (`active = false`) exclusivamente por administradores autenticados, restrita a vagas livres e sem movimentações abertas, bloqueando operadores (403) e preservando referências históricas de movimentações vinculadas.

#### Scenario: Administrador desativa vaga livre sem movimentação aberta
- **WHEN** um administrador solicita a desativação lógica de uma vaga livre e sem movimentação aberta
- **THEN** o sistema define `active = false` na vaga, preservando o histórico de movimentações passadas

#### Scenario: Operador tenta desativar vaga
- **WHEN** um operador autenticado tenta desativar uma vaga
- **THEN** o sistema rejeita a operação com erro de acesso negado (403)

#### Scenario: Tentativa de desativar vaga ocupada ou com movimentação aberta
- **WHEN** um administrador tenta desativar uma vaga ocupada ou que possua movimentação aberta pendente
- **THEN** o sistema rejeita a desativação para garantir a integridade dos dados

### Requirement: Campo cancelled em movimentações e definição de movimentação aberta
O sistema SHALL suportar um campo booleano `cancelled` (default `false`) na tabela `movimentacao` para representar movimentações canceladas ou de teste, considerando uma movimentação como aberta somente quando `exit_time == null && cancelled == false`.

#### Scenario: Movimentação cancelada não bloqueia vaga nem é encerrada na saída
- **WHEN** uma movimentação de teste é marcada com `cancelled = true`
- **THEN** o sistema a desconsidera como movimentação aberta, permitindo liberar a vaga, e rejeita tentativas de encerrá-la via `saida_POST`

#### Scenario: Preservação de dados históricos no cancelamento
- **WHEN** uma movimentação é marcada como cancelada
- **THEN** o `exit_time` original e demais dados históricos permanecem inalterados

### Requirement: Consulta e listagem de vagas ativas com autenticação
O sistema SHALL fornecer endpoints de listagem de vagas e consulta de disponibilidade e ocupação (`vaga_list_GET`, `vaga_ocupacao_GET`) filtrando exclusivamente vagas ativas (`active == true`), respeitando as regras de autenticação do sistema.

#### Scenario: Consulta de vagas e ocupação por usuário autenticado
- **WHEN** um usuário autenticado consulta a listagem de vagas ativas ou o resumo de ocupação
- **THEN** o sistema retorna apenas os dados das vagas ativas (`active == true`)

### Requirement: Controle restrito de status livre e ocupada com prevenção de ocupação simultânea
O sistema SHALL suportar exclusivamente os status `livre` e `ocupada`, atualizando-os automaticamente na entrada (muda para `ocupada`, bloqueando entradas em vagas já ocupadas, inativas ou com inconsistência) e na saída (muda para `livre`), prevenindo ocupações simultâneas.

#### Scenario: Entrada de veículo ocupa a vaga disponível e ativa
- **WHEN** um veículo registra entrada em uma vaga com status `livre` e `active = true`
- **THEN** o status da vaga é alterado para `ocupada`

#### Scenario: Saída de veículo libera a vaga ocupada
- **WHEN** um veículo registra saída de uma vaga com status `ocupada`
- **THEN** o status da vaga é alterado para `livre`

#### Scenario: Tentativa de entrada em vaga ocupada, inativa ou com inconsistência de status
- **WHEN** uma entrada é solicitada para uma vaga cujo status é `ocupada`, inativa (`active = false`) ou com movimentação aberta conflitante
- **THEN** o sistema rejeita a operação prevenindo ocupação simultânea
