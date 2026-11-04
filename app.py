import streamlit as st
import requests

st.set_page_config(page_title="Sistema de Gestão de Estacionamento", layout="wide")

# Configuração da URL base da API Xano (ajustável conforme ambiente)
XANO_API_URL = "https://x8ki-letl-twmt.n7.xano.io/api:estacionamento"

# Inicialização do session_state para autenticação
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.token = None
    st.session_state.user = None

def api_request(method, endpoint, json_data=None):
    headers = {}
    if st.session_state.token:
        headers["Authorization"] = f"Bearer {st.session_state.token}"

    url = f"{XANO_API_URL}/{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=json_data)
        elif method == "PATCH":
            response = requests.patch(url, headers=headers, json=json_data)
        else:
            return None, {"error": "Método não suportado"}

        if response.status_code in [200, 201]:
            return response.json(), None
        else:
            try:
                err = response.json()
            except:
                err = {"message": response.text}
            return None, err
    except Exception as e:
        return None, {"message": str(e)}

# --- TELA DE LOGIN ---
if not st.session_state.logged_in:
    st.title("Login - Sistema de Estacionamento")

    with st.form("login_form"):
        email = st.text_input("E-mail")
        password = st.text_input("Senha", type="password")
        submit = st.form_submit_button("Entrar")

        if submit:
            if not email or not password:
                st.warning("Preencha e-mail e senha.")
            else:
                data, err = api_request("POST", "usuario/login", {"email": email, "password": password})
                if err:
                    st.error(f"Erro ao autenticar: {err.get('message', 'Credenciais inválidas.')}")
                else:
                    st.session_state.logged_in = True
                    st.session_state.token = data.get("authToken")
                    st.session_state.user = data.get("user")
                    st.success("Login realizado com sucesso!")
                    st.rerun()
else:
    # --- APLICAÇÃO PRINCIPAL ---
    user = st.session_state.user
    st.sidebar.write(f"**Usuário:** {user.get('name')}")
    st.sidebar.write(f"**Perfil:** {user.get('type')}")

    if st.sidebar.button("Sair"):
        st.session_state.logged_in = False
        st.session_state.token = None
        st.session_state.user = None
        st.rerun()

    st.title("Sistema de Gestão de Estacionamento")

    # Abas de navegação
    tabs = ["Vagas e Ocupação", "Movimentação", "Cadastros"]
    if user.get("type") == "admin":
        tabs.append("Gerenciamento de Usuários")

    selected_tab = st.selectbox("Navegação", tabs)

    if selected_tab == "Vagas e Ocupação":
        st.header("Status das Vagas")
        data, err = api_request("GET", "vaga/ocupacao")
        if err:
            st.error(f"Erro ao carregar vagas: {err.get('message')}")
        else:
            st.json(data)

    elif selected_tab == "Movimentação":
        st.header("Registro de Entrada e Saída")
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Registrar Entrada")
            with st.form("entrada_form"):
                veiculo_id = st.number_input("ID do Veículo", min_value=1, step=1)
                vaga_id = st.number_input("ID da Vaga", min_value=1, step=1)
                submit_entrada = st.form_submit_button("Registrar Entrada")

                if submit_entrada:
                    payload = {"veiculo_id": int(veiculo_id), "vaga_id": int(vaga_id)}
                    res, err = api_request("POST", "parking/entrada", payload)
                    if err:
                        st.error(f"Erro: {err.get('message')}")
                    else:
                        st.success("Entrada registrada com sucesso!")
                        st.json(res)

        with col2:
            st.subheader("Registrar Saída")
            with st.form("saida_form"):
                mov_id = st.number_input("ID da Movimentação", min_value=1, step=1)
                submit_saida = st.form_submit_button("Registrar Saída")

                if submit_saida:
                    payload = {"movimentacao_id": int(mov_id)}
                    res, err = api_request("POST", "parking/saida", payload)
                    if err:
                        st.error(f"Erro: {err.get('message')}")
                    else:
                        st.success("Saída registrada com sucesso!")
                        st.json(res)

    elif selected_tab == "Cadastros":
        st.header("Cadastros Básicos (Veículos e Mensalistas)")
        st.info("Utilize os formulários para cadastrar veículos e mensalistas.")

    elif selected_tab == "Gerenciamento de Usuários" and user.get("type") == "admin":
        st.header("Gestão de Usuários (Administrador)")

        # Listar usuários
        st.subheader("Usuários Cadastrados")
        users_data, err = api_request("GET", "usuario")
        if err:
            st.error(f"Erro ao listar usuários: {err.get('message')}")
        else:
            st.dataframe(users_data)

        st.subheader("Cadastrar Novo Usuário")
        with st.form("new_user_form"):
            new_name = st.text_input("Nome")
            new_email = st.text_input("E-mail")
            new_password = st.text_input("Senha", type="password")
            new_type = st.selectbox("Tipo", ["operador", "admin"])
            submit_user = st.form_submit_button("Cadastrar Usuário")

            if submit_user:
                payload = {
                    "name": new_name,
                    "email": new_email,
                    "password": new_password,
                    "type": new_type
                }
                res, err = api_request("POST", "usuario", payload)
                if err:
                    st.error(f"Erro ao criar usuário: {err.get('message')}")
                else:
                    st.success("Usuário criado com sucesso!")
                    st.rerun()
