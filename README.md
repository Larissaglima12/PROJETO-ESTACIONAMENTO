# Sistema Web de Gestão de Estacionamento

## 1. Apresentação

O **Sistema Web de Gestão de Estacionamento** organiza as atividades diárias
de um estacionamento em uma aplicação web. Seu objetivo é facilitar o
acompanhamento das vagas, dos veículos, das entradas e saídas e dos valores
cobrados.

A solução reduz a dependência de controles manuais, que podem dificultar a
localização de vagas livres, a consulta de movimentações e o acompanhamento do
faturamento. O público-alvo são **administradores** e **operadores** de
estacionamentos.

## 2. Acesso ao aplicativo

O aplicativo é executado localmente. Não há endereço de deploy informado neste
README.

### Instalação no Windows

É necessário ter Python 3.14 instalado. No PowerShell, na pasta do projeto,
execute:

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### Execução

Com o ambiente virtual ativado, inicie o aplicativo:

```powershell
streamlit run app.py
```

Abra o navegador em [http://localhost:8501](http://localhost:8501). Para
acessar, utilize a conta fornecida pelo responsável pelo ambiente Xano. Este
README não contém senhas, tokens ou credenciais.

O aplicativo precisa estar configurado para a URL base do workspace Xano por
meio da constante `XANO_API_URL` em `app.py`. Não compartilhe tokens ou senhas
ao configurar ou demonstrar o sistema.

## 3. Perfis de usuários

O aplicativo possui dois perfis:

- **Administrador:** acompanha o estacionamento e o faturamento, gerencia
  vagas e usuários e também pode realizar as operações disponíveis ao operador.
- **Operador:** consulta a ocupação, registra entradas e saídas e utiliza as
  telas de cadastro básico de veículos e mensalistas.

| Funcionalidade | Administrador | Operador | Observação |
|---|---:|---:|---|
| Login, dashboard, ocupação e movimentações | Sim | Sim | Operações de entrada e saída exigem usuário autenticado no backend. |
| Consultar e cadastrar veículos | Sim, na interface | Sim, na interface | As rotas de veículos não declaram autenticação no backend. |
| Consultar e cadastrar mensalistas | Sim, na interface | Sim, na interface | As rotas de mensalistas não declaram autenticação no backend. |
| Consultar faturamento | Sim | Não | A opção fica restrita ao administrador e o endpoint valida o perfil. |
| Cadastrar, editar e desativar vagas | Sim | Não | A interface e os endpoints de gestão de vagas verificam o perfil administrativo. |
| Consultar e cadastrar usuários | Sim | Não | O cadastro permite escolher entre `operador` e `admin`. |

**Atenção:** a visibilidade de uma tela não substitui a autorização no
backend. Em especial, não considere as rotas de veículos e mensalistas
protegidas até que a autenticação seja implementada e validada nelas.

## 4. Funcionalidades

- **Login e logout:** acesso por conta cadastrada e encerramento da sessão do
  aplicativo.
- **Dashboard:** resumo da quantidade de vagas livres e ocupadas e da taxa de
  ocupação.
- **Vagas e ocupação:** consulta da disponibilidade e da situação das vagas
  ativas.
- **Cadastro de veículos:** consulta e cadastro de placa, modelo, cor, tipo e
  vínculo opcional com mensalista.
- **Cadastro de mensalistas:** consulta e cadastro de nome, contato, valor da
  mensalidade e período de vigência.
- **Entrada e saída:** registro da entrada em vaga livre, consulta de
  movimentações abertas e encerramento na saída.
- **Cobrança:** cálculo realizado pelo backend conforme as regras atuais,
  incluindo tolerância, frações e valor máximo.
- **Faturamento:** indicadores diário e mensal, ticket médio, quantidade de
  movimentações concluídas, histórico e gráfico diário, baseados em saídas
  registradas e não canceladas no fuso `America/Sao_Paulo`; disponível ao
  administrador.
- **Gestão de vagas:** cadastro, edição e desativação lógica de vagas pelo
  administrador.
- **Gerenciamento de usuários:** consulta e cadastro de usuários pelo
  administrador, com os perfis `operador` e `admin`.

## 5. Manual de utilização

### Jornada do operador

1. **Entrar:** na tela de login, informe o e-mail e a senha da sua conta e
   clique em **Entrar no Sistema**. Após a autenticação, o dashboard será
   exibido.
2. **Consultar vagas:** no menu lateral, clique em **Vagas e Ocupação**. Veja
   os totais e a grade para identificar vagas livres e ocupadas.
3. **Cadastrar um veículo:** clique em **Cadastros Básicos** e abra a aba
   **Veículos**. Preencha a placa e o modelo; informe cor e tipo e, se
   aplicável, selecione um mensalista. Clique em **Cadastrar Veículo**. A
   listagem apresenta os veículos retornados pela API.
4. **Registrar entrada:** abra **Movimentação**. Na seção **Registrar
   Entrada**, selecione um veículo cadastrado e uma vaga livre e clique em
   **Registrar Entrada**. A tela informa a placa e a vaga ocupada após o
   sucesso.
5. **Consultar movimentações abertas:** permaneça em **Movimentação** e veja
   a lista da seção **Registrar Saída**. Ela apresenta os veículos que ainda
   não têm saída registrada.
6. **Registrar saída:** selecione a movimentação correspondente na lista e
   clique em **Registrar Saída**. Se não houver movimentação aberta, a tela
   informa que não há veículo estacionado.
7. **Consultar o valor:** após uma saída bem-sucedida, confira o valor exibido
   em **Valor a Pagar**. O valor calculado é retornado pelo backend.
8. **Confirmar a liberação da vaga:** clique em **Vagas e Ocupação** e
   confira se a vaga aparece como livre. A lista é atualizada após a operação.
9. **Cadastrar ou consultar mensalistas:** em **Cadastros Básicos**, abra a
   aba **Mensalistas**. Para cadastrar, informe nome, telefone, valor da
   mensalidade e datas de início e término; clique em **Cadastrar Mensalista**.
   A listagem exibe os registros retornados. As rotas correspondentes ainda
   não exigem autenticação no backend; evite usá-las com dados reais até essa
   limitação ser corrigida.
10. **Sair:** clique em **Sair do Sistema** no cabeçalho para encerrar a sessão
    do aplicativo.

### Jornada do administrador

1. **Entrar:** na tela de login, informe as credenciais da conta administrativa
   e clique em **Entrar no Sistema**.
2. **Consultar o dashboard:** a página inicial apresenta os totais de vagas e
   a taxa de ocupação.
3. **Acompanhar o faturamento:** no menu lateral, clique em **Faturamento**.
   Consulte os indicadores **Faturamento Hoje**, **Faturamento Mês**,
   **Ticket Médio** e **Movimentações**, além do histórico e do gráfico diário.
   A página não apresenta controles de filtro de período.
4. **Cadastrar vagas:** clique em **Gestão de Vagas** e abra **Cadastrar
   Vaga**. Informe o número e o tipo e clique em **Cadastrar Vaga**. A nova
   vaga começa livre e ativa.
5. **Editar vagas:** em **Gestão de Vagas**, abra **Editar Vaga Existente**,
   selecione a vaga, ajuste o número ou o tipo e clique em **Salvar
   Alterações**.
6. **Desativar vagas:** abra **Desativar Vaga**, selecione uma vaga livre,
   marque a confirmação e clique em **Desativar Vaga**. Vagas ocupadas ou com
   movimentação em aberto não podem ser desativadas. A desativação é lógica;
   o registro histórico é preservado.
7. **Consultar usuários:** clique em **Gerenciamento de Usuários** para ver a
   lista disponibilizada pelo backend.
8. **Cadastrar usuários e definir o perfil:** na mesma página, informe nome,
   e-mail e senha, selecione **operador** ou **admin** em **Perfil de
   Acesso** e clique em **Cadastrar Usuário**. Não compartilhe a senha em
   capturas, gravações ou documentos.
9. **Sair:** clique em **Sair do Sistema** no cabeçalho para encerrar a sessão
   do aplicativo.

## 6. Exemplos de utilização

Os exemplos abaixo usam **dados fictícios** e ilustram o comportamento esperado
conforme as regras implementadas. Não são resultados de testes executados.

### Entrada e saída de um veículo avulso

Uma pessoa chega com o veículo fictício de placa `ABC1D23`. O operador
cadastra o veículo, seleciona uma vaga livre e registra a entrada. Na saída,
seleciona a movimentação aberta correspondente e encerra o estacionamento.
Após o sucesso, a aplicação mostra o valor retornado pelo backend e a vaga
deve aparecer livre na consulta de ocupação.

### Exemplo de cálculo de cobrança

Considere uma permanência fictícia de 20 minutos para um veículo avulso. Até
10 minutos são gratuitos. Depois de ultrapassado esse limite, o cálculo atual
usa frações de 15 minutos sobre o tempo total da permanência:

```text
ceil(20 / 15) = 2 frações
2 × R$ 5,00 = R$ 10,00
```

O valor máximo por movimentação é R$ 50,00. Até 10 minutos, o valor é R$ 0,00.

### Atendimento de mensalista ativo

Considere um veículo fictício associado a um mensalista com status ativo e
vigência que inclui a data da saída. Nesse caso, o backend aplica isenção da
tarifa avulsa e registra valor cobrado de R$ 0,00. Um mensalista inativo ou
fora da vigência segue a regra de cobrança avulsa.

### Consulta financeira pelo administrador

Suponha que o histórico fictício contenha três movimentações finalizadas,
com valores de R$ 5,00, R$ 0,00 e R$ 20,00. O administrador consulta a página
**Faturamento** e visualiza os indicadores calculados pelo backend, o
histórico e a evolução diária. Os valores do exemplo não representam dados do
workspace.

### Tentativa de usar uma vaga ocupada

Se uma vaga fictícia já estiver ocupada, ela não aparece entre as vagas livres
para entrada. Se uma solicitação de entrada incompatível chegar ao backend, a
operação deve ser rejeitada pela validação de disponibilidade.

## 7. Limitações conhecidas

- As rotas de cadastro e listagem de veículos e mensalistas não declaram
  autenticação no backend. A proteção visual do menu não impede chamadas
  diretas a essas rotas.
- A página de faturamento não oferece filtros de período, embora o endpoint
  aceite datas inicial e final.
- As verificações locais incluem compilação, checagem de dependências e
  validação sintática dos arquivos XanoScript e simulações do frontend com
  respostas mockadas. Elas não comprovam, por si só, o funcionamento integrado
  com o workspace Xano.
- Testes de concorrência e operações de escrita não foram executados nesta
  validação. O script `test_concurrency.py` pode realizar chamadas mutativas;
  não o execute contra um workspace com dados reais.
- O enum local de vagas ainda contém `manutencao`, embora a especificação
  principal descreva apenas `livre` e `ocupada`; esse estado não foi validado
  funcionalmente.
- O plano gratuito do Xano pode limitar a quantidade de requisições. Quando o
  serviço retorna HTTP 429, o aplicativo apresenta uma mensagem de espera;
  o limite e o tempo de recuperação dependem do plano e da resposta do serviço.
- Arquivos de demonstração e configurações locais já estão rastreados no Git.
  Um scanner sinalizou um possível valor literal de senha em arquivo de
  demonstração; confirme se é apenas exemplo e substitua/rotacione se for real.
- As orientações oficiais de entrega da Faculdade Impacta foram consideradas
  na organização deste README. Isso não comprova conformidade integral do
  projeto com todos os critérios; cada requisito precisa ser confrontado com
  sua evidência de implementação e validação.

## 8. Tecnologias e arquitetura

### Tecnologias

- **Python:** linguagem da aplicação.
- **Streamlit:** interface web, executada localmente.
- **Pandas:** tratamento de datas, valores e histórico financeiro na interface.
- **Requests:** comunicação HTTP entre o aplicativo e a API.
- **Xano:** backend, banco de dados e API REST.
- **XanoScript:** definição local de tabelas e endpoints na pasta `xano/`.
- **OpenSpec:** organização das especificações e mudanças na pasta
  `openspec/`.

### Modelo de dados

Os arquivos locais descrevem as entidades `usuario`, `veiculo`, `mensalista`,
`vaga` e `movimentacao`. As movimentações relacionam veículo, vaga e usuário
operador e guardam horários de entrada e saída, valor cobrado e indicador de
cancelamento. Consulte `xano/table/` e
[docs/domain-model.md](docs/domain-model.md) para mais detalhes.

### Endpoints consumidos pelo aplicativo

| Método | Rota | Utilização |
|---|---|---|
| POST | `usuario/login` | Autenticação |
| GET / POST | `veiculo` | Consulta e cadastro de veículos |
| GET / POST | `mensalista` | Consulta e cadastro de mensalistas |
| GET / POST | `vaga` | Consulta e cadastro de vagas |
| PATCH | `vaga/{id}` | Edição e desativação lógica de vaga |
| GET | `vaga/ocupacao` | Resumo de ocupação |
| GET / POST | `usuario` | Consulta e cadastro de usuários |
| POST | `parking/entrada` | Registro de entrada |
| GET | `parking/movimentacao/abertas` | Consulta de movimentações abertas |
| POST | `parking/saida` | Registro de saída e cálculo de cobrança |
| GET | `parking/financeiro` | Indicadores e histórico financeiro |

O backend aplica autenticação e verificações administrativas em rotas de
faturamento, gestão de vagas e gestão de usuários. Confirme as limitações de
autorização indicadas na seção anterior antes de usar as rotas de veículos e
mensalistas com dados reais.

### Documentação complementar

- [Visão geral do projeto](docs/project-overview.md)
- [Modelo de domínio](docs/domain-model.md)
- [Status da finalização e matriz de requisitos](docs/finalizacao-status.md)
- [Checklist de testes e demonstração](docs/checklist-testes.md)
- [Roteiro de apresentação](docs/roteiro-apresentacao.md)

### Verificações locais

Para verificar a sintaxe do aplicativo:

```powershell
python -m py_compile app.py
```

Para validar a Change financeira no OpenSpec:

```powershell
npx openspec validate dashboard-financeiro --strict
```

Antes de qualquer publicação no Xano, use o dry-run e revise os arquivos
listados:

```powershell
xano workspace push -d ./xano --dry-run
```

O dry-run não publica alterações. Não faça push sem revisar o resultado e
obter autorização.
