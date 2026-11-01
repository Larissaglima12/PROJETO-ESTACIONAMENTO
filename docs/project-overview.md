# Project Overview — Sistema de Gestão de Estacionamento

## 1. Visão geral

Sistema web para gerenciar a operação de um estacionamento: controle de
vagas, cadastro de veículos e mensalistas, e registro de entradas e
saídas de veículos.

## 2. Problema

O controle manual de entradas, saídas e ocupação de vagas é sujeito a
erros e dificulta saber quais vagas estão livres e quanto cobrar de cada
veículo.

## 3. Objetivos

- Registrar a entrada e a saída de veículos de forma confiável.
- Mostrar a ocupação das vagas em tempo real.
- Manter o cadastro de veículos e de mensalistas.
- Calcular o valor a cobrar na saída (ver seção 13).

## 4. Usuários

- **Administrador:** gerencia o sistema e seus cadastros.
- **Operador:** registra entradas e saídas no dia a dia.
- **Mensalista:** cliente com contrato mensal. É apenas um cadastro, não
  acessa o sistema.

## 5. Escopo

**Dentro do escopo inicial:** autenticação de usuários, cadastro de
veículos, mensalistas e vagas, registro de entrada e saída, painel de
ocupação das vagas e cálculo do valor cobrado.

**A definir:** relatórios, pagamento online, acesso de mensalistas ao
sistema, integração com cancelas ou câmeras.

## 6. Principais funcionalidades

- Login de administrador e operador.
- Cadastro e consulta de veículos, mensalistas e vagas.
- Registro de entrada e de saída de veículos.
- Painel de ocupação das vagas.
- Cálculo do valor na saída.

## 7. Requisitos e restrições

- O desenvolvimento deve seguir o fluxo OpenSpec (Explore, Propose,
  Review, Apply, Archive).
- O projeto é acadêmico: prazo e funcionalidades mínimas a definir.
- As regras de negócio devem ficar no backend.

## 8. Arquitetura tecnológica

- **Backend e banco de dados:** Xano (XanoScript), com API REST.
- **Frontend:** Streamlit, consumindo a API do Xano.
- **Versionamento:** Git e GitHub.
- **Sincronização com o Xano:** Xano CLI.
- **Agente de IA:** Gemini CLI, com o Xano Developer MCP para
  documentação e validação.
- **Especificação:** OpenSpec.

Streamlit será utilizado como tecnologia exclusiva para implementação do
frontend da aplicação.

## 9. Princípios de desenvolvimento

- Desenvolvimento incremental, em mudanças pequenas e verificáveis.
- A especificação vem antes da implementação.
- O código gerado pela IA é sempre revisado antes de ser publicado.

## 10. Segurança e integridade

- A autorização é aplicada no backend. O frontend não é mecanismo de
  segurança.
- Tokens e senhas nunca são versionados.
- Dados sensíveis (senha, e-mail) são tratados como sensíveis no Xano.

## 11. Estratégia de desenvolvimento

O modelo de domínio é global, mas a implementação é incremental: o banco
e as APIs evoluem junto com as funcionalidades, uma Change por vez. Já
existe um backend inicial no Xano (tabelas e endpoints de estacionamento),
que será revisado e ajustado pelas Changes.

## 12. Fonte de verdade e documentação

- `docs/domain-model.md`: conceitos e relacionamentos do domínio.
- `openspec/specs/`: comportamento consolidado do sistema.
- `openspec/changes/`: mudanças em andamento.
- `AGENTS.md` e `openspec/config.yaml`: regras para o agente.

## 13. Decisões de negócio da primeira versão

Valores de referência inspirados nos estacionamentos da Rua Cubatão
(Paraíso/Vila Mariana, São Paulo). São parâmetros do projeto e podem
ser ajustados.

- Cobrança em frações de 15 minutos; hora de referência R$ 12,00
  (R$ 3,00 por fração); até 15 minutos de permanência são gratuitos.
- Teto de R$ 25,00 por movimentação.
- Mensalista ativo e dentro da vigência: valor cobrado R$ 0,00 na saída.
  Mensalista inativo, suspenso ou vencido: tarifa avulsa.
- Mensalidade de referência para dados de teste: R$ 280,00.
- Login obrigatório para operar; o usuário da movimentação vem do token
  de autenticação, não de um campo enviado pelo cliente.
- O tipo da vaga não restringe o tipo do veículo nesta versão.
- Veículo com movimentação aberta não pode registrar nova entrada.
- Veículo sem entrada em aberto não pode registrar saída.
- A vaga só aceita entrada se estiver livre; o operador escolhe a vaga.
- Funcionamento 24 horas, sem restrição de horário.