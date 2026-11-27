# Proposal: Gerenciamento de Vagas

## Why
O sistema precisa de um gerenciamento completo de vagas de estacionamento — abrangendo cadastro, listagem, atualização e desativação lógica de vagas, além do controle rigoroso de disponibilidade baseado estritamente nos status `livre` e `ocupada` —, garantindo integridade com o fluxo de entradas e saídas, tratamento adequado de movimentações de teste/legadas via cancelamento lógico (`cancelled`), regularização de numeração legada e aplicação de restrições de acesso administrativo e validações de consistência operacional.

## What Changes
- **Cadastro e Edição de Vagas:** Implementar e consolidar o cadastro e a edição de vagas (com numeração inicial recomendada de 1 a 30, sem repetição, expansível pelo administrador), restritos a administradores com perfil `admin`. Novas vagas iniciam sempre com status `livre` e `active = true`.
- **Status das Vagas:** Adotar exclusivamente os status `livre` e `ocupada`, removendo qualquer referência ao status `manutencao`.
- **Desativação Lógica e Exclusão Segura:** Permitir a desativação lógica de vagas (`active = false`) exclusivamente se estiverem livres e sem movimentações abertas vinculadas, preservando o histórico de movimentações.
- **Tratamento de Movimentações de Teste/Legadas:** Adicionar o campo booleano `cancelled` na tabela `movimentacao` (default `false`) para representar movimentações canceladas ou de teste sem inventar horários de saída fictícios. Uma movimentação só é considerada aberta se `exit_time == null && cancelled == false`.
- **Regularização de Dados Legados:** Planear a regularização da vaga legada (`number = 0` para número positivo disponível) e a migração explícita de registros antigos (`active = true`, `cancelled = false`).
- **Consulta e Listagem:** Aprimorar a consulta e listagem de vagas ativas (`active == true`) respeitando as regras de autenticação existentes.
- **Integração com Entrada e Saída:** Garantir que a entrada de um veículo altere o status da vaga para `ocupada` (bloqueando tentativas de entrada em vagas já ocupadas ou inativas) e a saída altere para `livre`. Impedir encerramento de movimentações canceladas e alterações manuais de status incompatíveis com movimentações abertas.

## Capabilities

### New Capabilities
- (Nenhuma nova capacidade standalone; a capacidade de domínio existente `parking-management` será modificada).

### Modified Capabilities
- `parking-management`: Adiciona e consolida os requisitos operacionais de gerenciamento de vagas (cadastro, edição, desativação lógica restrita, status `livre`/`ocupada`, campo `cancelled` em movimentações, regularização de numeração e validações de integridade) sob autenticação adequada.

## Impact
- **Backend (Xano):** Novos endpoints ou aprimoramentos nos endpoints de vagas (`vaga_create_POST`, atualização, desativação) e validações robustas em `entrada_POST`, `saida_POST` e checagens de movimentações abertas.
- **Frontend (Streamlit):** Atualização da interface de gerenciamento de vagas, permitindo que administradores criem, editem e desativem vagas conforme as novas regras de negócio.
- **Banco de Dados:** Ajustes no schema da tabela `vaga` (`active`, remoção de `manutencao`) e da tabela `movimentacao` (`cancelled`).
