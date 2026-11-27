# Roteiro de apresentação — Sistema de Gestão de Estacionamento

**Duração planejada:** 5 a 8 minutos. A duração oficial não foi confirmada,
pois o manual do professor não foi encontrado no repositório.
**Antes da gravação:** use dados sintéticos em ambiente de demonstração; oculte
e-mails, senhas, tokens e quaisquer dados pessoais.

## 1. Abertura — problema e objetivo (0:00–0:40)

**Mostrar:** título do projeto e tela de login.

**Falar:**

> Olá. Este é o Sistema de Gestão de Estacionamento, desenvolvido como
> projeto acadêmico da Faculdade Impacta. O problema que queremos resolver é
> o controle manual de entradas, saídas e ocupação, que dificulta localizar
> vagas disponíveis e acompanhar os valores cobrados. O objetivo é centralizar
> a operação em uma interface web conectada a uma API.

## 2. Tecnologias, arquitetura e OpenSpec (0:40–1:20)

**Mostrar:** rapidamente a estrutura do projeto; depois retornar ao app.

**Falar:**

> O frontend foi desenvolvido exclusivamente com Streamlit e Python. O
> backend e o banco de dados usam Xano, com endpoints descritos em XanoScript.
> O OpenSpec foi usado para organizar requisitos, decisões de implementação e
> tarefas. A aplicação Streamlit consome as rotas REST do Xano e envia o token
> de autenticação nas requisições protegidas.

## 3. Login, perfis e segurança (1:20–2:00)

**Mostrar:** login com usuário de demonstração, sem exibir a senha; mostrar
brevemente a diferença de menus entre administrador e operador, se houver
contas de demonstração disponíveis.

**Falar:**

> O sistema diferencia os perfis de administrador e operador. O operador
> realiza as atividades operacionais; as opções de gestão e faturamento são
> exibidas ao administrador. A interface não é, por si só, uma barreira de
> segurança: as permissões precisam ser verificadas também no backend. Na
> auditoria, confirmei verificações administrativas para faturamento e gestão
> de vagas e usuários. As rotas de veículos e mensalistas ainda precisam de
> proteção no backend; por isso, não afirmo que toda a API esteja protegida.

## 4. Dashboard, vagas e ocupação (2:00–2:45)

**Mostrar:** dashboard, indicadores e grade de vagas, usando registros
sintéticos.

**Falar:**

> No dashboard, a aplicação apresenta a quantidade de vagas livres e
> ocupadas e a taxa de ocupação calculada sobre os dados retornados pela API.
> Na grade, cada vaga mostra seu número e estado. A listagem e os totais
> consideram as vagas ativas. Esta tela ajuda a equipe a consultar a situação
> atual do estacionamento.

## 5. Veículos e mensalistas (2:45–3:20)

**Mostrar:** telas de cadastro/listagem apenas com dados sintéticos e sem
acionar novos cadastros durante a gravação.

**Falar:**

> O sistema possui telas para consultar e cadastrar veículos, e para manter
> os dados e o período de vigência dos mensalistas. Um veículo pode ser
> associado a um mensalista. Antes de disponibilizar essas rotas fora do
> ambiente de demonstração, é necessário concluir a autorização no backend.

## 6. Entrada, saída e cobrança (3:20–4:20)

**Mostrar:** movimentação com uma entrada e saída já preparadas em dados de
demonstração; não criar registros em workspace com dados reais.

**Falar:**

> Na operação, selecionamos um veículo e uma vaga livre para registrar a
> entrada. O backend valida a vaga e as movimentações abertas antes de gravar.
> Na saída, calcula o tempo de permanência, encerra a movimentação e libera a
> vaga. A regra implementada concede até dez minutos de tolerância; depois,
> cobra cinco reais por fração de quinze minutos, até o teto de cinquenta
> reais. Um mensalista ativo e dentro da vigência não paga a tarifa avulsa.

## 7. Gestão administrativa e faturamento (4:20–5:30)

**Mostrar:** gestão de vagas e usuários; depois a página de faturamento e o
histórico.

**Falar:**

> No perfil administrador, há telas de gerenciamento de vagas e usuários.
> Também há o módulo financeiro, com faturamento do dia, do mês, ticket médio,
> quantidade de movimentações concluídas, histórico e gráfico de valores por
> dia. O endpoint considera movimentações finalizadas, desconsidera
> cancelamentos e usa o fuso de São Paulo. O endpoint aceita datas de início e
> fim, mas a interface ainda não oferece controles de filtro.

## 8. Conclusão (5:30–6:00)

**Mostrar:** retornar ao dashboard; encerrar a sessão de demonstração.

**Falar:**

> O projeto reúne uma interface operacional em Streamlit, regras no backend
> Xano e especificação com OpenSpec. A auditoria confirmou a sintaxe local dos
> arquivos XanoScript e a página financeira, mas ainda há validações manuais e
> ajustes de autorização pendentes. Obrigado por assistir.

## Checklist de gravação

- Confirmar com o professor a duração oficial.
- Usar ambiente e registros exclusivamente de demonstração.
- Ocultar senhas, tokens, e-mails, placas reais e informações pessoais.
- Não executar testes de concorrência ou operações de escrita em dados reais.
- Não afirmar conformidade integral nem proteção completa da API.
