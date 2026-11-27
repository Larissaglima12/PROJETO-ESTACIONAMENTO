# Sistema de Gestão de Estacionamento

Projeto acadêmico de gestão de vagas e movimentações, com interface em
Streamlit e backend/API REST no Xano.

## Tecnologias e arquitetura

- **Frontend:** Python e Streamlit (`app.py`).
- **Dados e regras de negócio:** Xano, por endpoints XanoScript na pasta
  `xano/`.
- **Especificação:** OpenSpec na pasta `openspec/`.
- **Documentação:** `docs/`.

O Streamlit mantém o estado de autenticação e consome as rotas do Xano. A
autorização efetiva deve ser feita no backend, não somente pela visibilidade
das telas.

## Funcionalidades

- Login de administrador e operador e logout da sessão Streamlit.
- Dashboard de ocupação e consulta de vagas ativas.
- Cadastro e consulta de veículos e mensalistas.
- Registro de entrada e saída e cálculo de cobrança no backend.
- Gestão administrativa de vagas e usuários.
- Faturamento diário/mensal, ticket médio, histórico e gráfico por dia.
- Cache de GET isolado por sessão e tratamento de erros HTTP, incluindo 429.

## Modelo de dados

Os arquivos locais do Xano descrevem as entidades `usuario`, `veiculo`,
`mensalista`, `vaga` e `movimentacao`. As movimentações referenciam veículo,
vaga e operador, além de registrar entrada, saída, valor cobrado e indicador
de cancelamento. Consulte `xano/table/` e [docs/domain-model.md](docs/domain-model.md)
para os detalhes.

## Endpoints usados pelo frontend

| Método | Rota | Uso |
|---|---|---|
| POST | `usuario/login` | Autenticação |
| GET / POST | `veiculo` | Listar / cadastrar veículos |
| GET / POST | `mensalista` | Listar / cadastrar mensalistas |
| GET / POST | `vaga` | Listar / cadastrar vagas |
| PATCH | `vaga/{id}` | Editar ou desativar vaga |
| GET | `vaga/ocupacao` | Resumo de ocupação |
| GET / POST | `usuario` | Listar / cadastrar usuários |
| POST | `parking/entrada` | Registrar entrada |
| GET | `parking/movimentacao/abertas` | Consultar movimentações abertas |
| POST | `parking/saida` | Registrar saída |
| GET | `parking/financeiro` | Indicadores e histórico financeiro |

As rotas administrativas de vagas, usuários e financeiro verificam o perfil no
backend. **Pendência de segurança:** as rotas de veículo e mensalista não
declaram autenticação nos arquivos locais atuais. Não considerar essas rotas
protegidas até uma correção e validação em Change própria.

## Regras de negócio atuais

- Até 10 minutos de permanência são gratuitos.
- Após a tolerância, cobra R$ 5,00 por fração de 15 minutos, com teto de
  R$ 50,00 por movimentação.
- Mensalista ativo e dentro da vigência não recebe cobrança avulsa.
- O faturamento considera saídas registradas e movimentações não canceladas,
  com datas calculadas em `America/Sao_Paulo`.
- A movimentação deve registrar o operador autenticado; entradas e saídas
  possuem verificações transacionais no backend.

## Requisitos para execução

- Python compatível com as versões instaladas e testadas no projeto (Python
  3.14.7 no ambiente auditado).
- Dependências listadas em `requirements.txt`.
- Workspace Xano configurado; `app.py` aponta para a URL base definida na
  constante `XANO_API_URL`.

### Instalação no Windows

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Configure o workspace Xano e os usuários pelo procedimento seguro do projeto.
Não grave tokens, senhas ou `secrets.toml` no repositório.

### Executar

```powershell
.\.venv\Scripts\Activate.ps1
streamlit run app.py
```

## Validação

```powershell
python -m py_compile app.py
npx openspec list
npx openspec validate dashboard-financeiro --strict
xano workspace push -d ./xano --dry-run
```

O dry-run é somente uma prévia. Não execute push geral sem revisar o resultado
e obter autorização. A concorrência e operações de escrita devem ser testadas
somente em workspace isolado com dados sintéticos.

As evidências e as verificações ainda pendentes estão em
[docs/finalizacao-status.md](docs/finalizacao-status.md) e
[docs/checklist-testes.md](docs/checklist-testes.md). O roteiro de vídeo está
em [docs/roteiro-apresentacao.md](docs/roteiro-apresentacao.md).

## Limitações conhecidas

- O manual/requisitos oficiais do professor não foi localizado; conformidade
  acadêmica integral não pode ser declarada.
- As rotas de veículos e mensalistas precisam de autenticação e autorização
  no backend.
- A tela financeira ainda não expõe filtros de período.
- Testes de concorrência e de escrita no Xano real não foram executados nesta
  auditoria.
