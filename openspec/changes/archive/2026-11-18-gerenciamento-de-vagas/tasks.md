# Tasks

## 1. Auditoria e Diagnóstico Inicial (Somente Leitura)
- [x] 1.1 Realizar auditoria somente de leitura dos schemas existentes (`vaga`, `movimentacao`) e endpoints de vagas e estacionamento, verificando índices e campos atuais. (Verificação: Relatório de auditoria gerado sem nenhuma alteração no workspace).
- [x] 1.2 Verificar a existência e o estado da vaga legada de número 0 na tabela `vaga`, bem como eventuais referências históricas na tabela `movimentacao`, incluindo o registro de teste ID 3. (Verificação: Identificação documentada das dependências da vaga número 0 e movimentações).

## 2. Planejamento e Aprovação de Migração de Dados e Schema
- [x] 2.1 Preparar a especificação da migração do campo `active` (booleano, default `true`), campo `cancelled` (booleano, default `false`) e a restrição do enum `status` para conter exclusivamente `livre` e `ocupada` (removendo `manutencao`), mantendo o índice único global de numeração. (Verificação: Arquivos revisados com sucesso).
- [x] 2.2 Verificar o plano de auditoria dos status atuais, regularização da vaga número 0 para número positivo e marcação da movimentação de teste ID 3 como `cancelled = true` (sem execução automática). (Verificação: Plano submetido para aprovação humana).
- [x] 2.3 **PONTO DE APROVAÇÃO HUMANA:** Obter aprovação explícita da pessoa responsável antes de prosseguir com qualquer migração de dados, alteração de schema, execução de push no Xano ou criação das 30 vagas iniciais. (Verificação: Confirmação de aprovação registrada).

## 3. Implementação Backend (XanoScript) - Endpoints Administrativos e Validações
- [x] 3.1 Implementar ou ajustar o endpoint de cadastro de vagas (`vaga_create_POST`), exigindo autenticação de administrador (`admin`), número inteiro único e positivo (>= 1) com validação contra duplicidade, zero, negativos ou decimais, iniciando com status `livre` e `active = true`. (Verificação: Validação de sintaxe com o MCP do Xano e testes de permissão).
- [x] 3.2 Implementar o endpoint de atualização de vagas e o endpoint de desativação lógica (`active = false`), exigindo perfil `admin`, bloqueando desativação de vagas ocupadas ou com movimentação aberta (`exit_time == null && cancelled == false`), e preservando o histórico de movimentações. (Verificação: Validação de sintaxe XanoScript e testes de restrição).
- [x] 3.3 Atualizar os endpoints de listagem (`vaga_list_GET`) e ocupação (`vaga_ocupacao_GET`) para filtrar e considerar exclusivamente vagas com `active == true`. (Verificação: Resposta correta filtrada no Xano).

## 4. Concorrência e Proteção Transacional (Entrada e Saída)
- [x] 4.1 Confirmar a sintaxe e o comportamento de `db.transaction` com isolamento `serializable` no XanoScript para o endpoint de entrada (`entrada_POST`). (Verificação: Documentação e sintaxe validas via MCP).
- [x] 4.2 Atualizar `entrada_POST` e `saida_POST` para incluir validação transacional de status (`livre`/`ocupada`), verificação do `active == true`, desconsideração de movimentações canceladas (`cancelled == true`), e garantia de transição atômica de status. (Verificação: Validação sintática dos arquivos `.xs` modificados).

## 5. Testes, Verificação e Concorrência
- [x] 5.1 Executar testes de concorrência disparando requisições simultâneas de entrada na mesma vaga, verificando que apenas uma movimentação aberta é persistida sem parciais ou inconsistências. (Verificação: Requisição A (veículo 1, vaga 1) retornou HTTP 200, criando movimentação ID 14; Requisição B (veículo 3, vaga 1) retornou HTTP 400 com mensagem "A vaga já possui uma movimentação em aberto."; tabela `movimentacao` com 14 registros sem duplicação; vaga 1 ocupada e ativa; vaga 2 livre).
- [x] 5.2 Validar permissões de administrador vs operador (verificando erro 403 em tentativas de gerenciar vagas por operadores). (Verificação: Resposta HTTP 403 confirmada e integridade da vaga mantida).
- [x] 5.3 Validar o tratamento de movimentações canceladas (`cancelled = true`), entrada, saída, e integridade histórica. (Verificação: Comportamento testado e confirmado).

## 6. Integração Frontend (Streamlit)
- [x] 6.1 Atualizar a aplicação Streamlit (`app.py`) para exibir e permitir o gerenciamento de vagas (cadastro, listagem, desativação) exclusivamente para administradores. (Verificação: Interface validada e restrita por perfil de usuário).

## 7. Validação Final
- [x] 7.1 Executar `openspec validate gerenciamento-de-vagas --type change --strict` e `openspec status --change gerenciamento-de-vagas` para confirmar a conformidade total da Change. (Verificação: Validação estrita aprovada com sucesso).

## Workflow follow-up
- Apresentar a entrega final para revisão humana e posterior arquivamento da Change quando aprovada.
