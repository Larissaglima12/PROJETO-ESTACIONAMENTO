import html
import streamlit as st
import requests
import pandas as pd
import time

st.set_page_config(
    page_title="Sistema de Gestão de Estacionamento",
    page_icon="🅿️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS CUSTOMIZADO PARA PADRÃO SaaS ADMINISTRATIVO ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Estilização Geral e Cores de Fundo */
    .stApp {
        background-color: #F5F7FB;
        color: #1F2937;
    }

    /* Sidebar Profissional */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0;
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #1F2937 !important;
    }

    /* Títulos e Cabeçalhos */
    h1, h2, h3 {
        color: #1E3A8A !important;
        font-weight: 700 !important;
    }

    /* Cartões e Containers */
    div[data-testid="metric-container"] {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        border: 1px solid #E2E8F0;
    }

    div[data-testid="metric-container"] label {
        color: #64748B !important;
        font-weight: 500 !important;
        font-size: 0.875rem !important;
    }

    /* Botões Padronizados */
    .stButton>button {
        background-color: #2563EB;
        color: white;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        border: none;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background-color: #1E40AF;
        color: white;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
    }

    /* Inputs e Forms */
    .stTextInput>div>div>input, .stSelectbox>div>div>div {
        border-radius: 8px !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        font-weight: 500;
        color: #64748B;
    }
    .stTabs [aria-selected="true"] {
        color: #2563EB !important;
        border-bottom-color: #2563EB !important;
    }
</style>
""", unsafe_allow_html=True)

# Configuração da URL base da API Xano
XANO_API_URL = "https://x8ki-letl-twmt.n7.xano.io/api:estacionamento"

# Inicialização do session_state para autenticação
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.token = None
    st.session_state.user = None

if "data_version" not in st.session_state:
    st.session_state.data_version = 0

if "api_cache" not in st.session_state:
    st.session_state.api_cache = {}

def cached_api_get(user_id: int, endpoint: str, data_version: int):
    """
    Estratégia de cache por sessão (st.session_state) para garantir isolamento e segurança.
    Não utiliza st.cache_data (global) para evitar compartilhamento indevido entre usuários.
    """
    now = time.time()
    cache_entry = st.session_state.api_cache.get(endpoint)

    # Verificar validade do cache: existência, TTL (30s) e versão dos dados
    if cache_entry and (now - cache_entry['timestamp'] < 30) and (cache_entry['version'] == data_version):
        return cache_entry['data'], None

    # Se inválido ou expirado, realizar nova consulta
    data, err = api_request("GET", endpoint)

    # Armazenar no cache apenas se for sucesso (evita cachear erros temporários)
    if err is None:
        st.session_state.api_cache[endpoint] = {
            'data': data,
            'timestamp': now,
            'version': data_version
        }

    return data, err

def api_request(method, endpoint, json_data=None):
    headers = {}
    if st.session_state.token:
        headers["Authorization"] = f"Bearer {st.session_state.token}"

    url = f"{XANO_API_URL}/{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=10)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=json_data, timeout=10)
        elif method == "PATCH":
            response = requests.patch(url, headers=headers, json=json_data, timeout=10)
        else:
            return None, {"error": "Método HTTP não suportado."}

        if response.status_code in [200, 201]:
            try:
                return response.json(), None
            except ValueError:
                return None, {"message": "O servidor Xano retornou uma resposta inválida."}
        else:
            try:
                err = response.json()
            except ValueError:
                err = {"message": response.text or f"Erro HTTP {response.status_code}"}
            if not isinstance(err, dict):
                err = {"message": response.text or f"Erro HTTP {response.status_code}"}

            # Tratamento amigável por código de status
            status = response.status_code
            if status == 429 or "rate limit" in response.text.lower() or "too many requests" in response.text.lower():
                retry_after = response.headers.get("Retry-After", "20")
                err["message"] = f"Limite de requisições excedido (Plano Gratuito do Xano). Por favor, aguarde {retry_after} segundos antes de tentar novamente."
            elif status == 400:
                if not err.get("message"):
                    err["message"] = "Requisição inválida ou dados incorretos."
            elif status == 401:
                if not err.get("message"):
                    err["message"] = "Sessão expirada ou credenciais inválidas. Faça login novamente."
            elif status == 403:
                if not err.get("message"):
                    err["message"] = "Acesso negado para o seu perfil de usuário."
            elif status == 404:
                if not err.get("message"):
                    err["message"] = "Recurso ou endpoint não encontrado."
            elif status == 409:
                if not err.get("message"):
                    err["message"] = "Conflito detectado (registro duplicado ou em uso)."
            elif status >= 500:
                if not err.get("message"):
                    err["message"] = "Erro interno no servidor Xano. Tente novamente mais tarde."

            return None, err
    except requests.exceptions.Timeout:
        return None, {"message": "A requisição excedeu o tempo limite (timeout). Verifique sua conexão."}
    except requests.exceptions.ConnectionError:
        return None, {"message": "Falha de conexão com o servidor Xano. Verifique sua rede."}
    except requests.exceptions.RequestException as e:
        return None, {"message": f"Erro de comunicação: {str(e)}"}

def parse_xano_timestamp_utc(value):
    if value is None or pd.isna(value):
        return pd.NaT

    timestamp = pd.to_numeric(value, errors='coerce')
    if pd.notna(timestamp):
        return pd.to_datetime(timestamp, unit='ms', errors='coerce', utc=True)

    timestamp = pd.to_datetime(value, errors='coerce')
    if pd.isna(timestamp):
        return pd.NaT
    if timestamp.tzinfo is None:
        timestamp = timestamp.tz_localize("America/Sao_Paulo")
    return timestamp.tz_convert("UTC")

def format_xano_timestamp(value):
    timestamp = parse_xano_timestamp_utc(value)
    if pd.isna(timestamp):
        return "—"
    return timestamp.tz_convert("America/Sao_Paulo").strftime("%d/%m/%Y %H:%M:%S")

def format_stay_duration(entry_time, exit_time):
    entry = parse_xano_timestamp_utc(entry_time)
    exit = parse_xano_timestamp_utc(exit_time)
    if pd.isna(entry) or pd.isna(exit) or exit < entry:
        return None

    total_seconds = int((exit - entry).total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours}h {minutes}min {seconds}s"

# --- TELA DE LOGIN ---
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; color: #1E293B;'>🅿️ Estacionamento</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #64748B;'>Sistema Administrativo de Gestão</p><br>", unsafe_allow_html=True)

        with st.container():
            with st.form("login_form"):
                st.subheader("Acesso ao Sistema")
                email = st.text_input("E-mail corporativo")
                password = st.text_input("Senha", type="password")
                st.markdown("<br>", unsafe_allow_html=True)
                submit = st.form_submit_button("Entrar no Sistema", use_container_width=True)

                if submit:
                    if not email or not password:
                        st.warning("Preencha e-mail e senha.")
                    else:
                        data, err = api_request("POST", "usuario/login", {"email": email, "password": password})
                        if err:
                            st.error(f"Erro ao autenticar: {err.get('message', 'Credenciais inválidas.')}")
                        elif not isinstance(data, dict) or not data.get("authToken") or not isinstance(data.get("user"), dict):
                            st.error("O servidor retornou dados de autenticação inválidos.")
                        else:
                            st.session_state.logged_in = True
                            st.session_state.token = data.get("authToken")
                            st.session_state.user = data.get("user")
                            st.session_state.api_cache = {} # Limpar cache ao logar
                            if "last_entry_result" in st.session_state:
                                del st.session_state["last_entry_result"]
                            if "last_exit_result" in st.session_state:
                                del st.session_state["last_exit_result"]
                            st.success("Login realizado com sucesso!")
                            st.rerun()
else:
    # --- APLICAÇÃO PRINCIPAL ---
    user = st.session_state.user

    # --- CABEÇALHO PROFISSIONAL ---
    user_name = html.escape(str(user.get("name") or ""), quote=True)
    with st.container():
        col_h1, col_h2 = st.columns([3, 1])
        with col_h1:
            st.markdown(f"<h1 style='margin-bottom: 0;'>🅿️ Sistema de Gestão de Estacionamento</h1>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: #64748B; font-size: 1.1rem;'>Bem-vindo, <b>{user_name}</b> ({user.get('type').upper()})</p>", unsafe_allow_html=True)
        with col_h2:
            st.markdown("<div style='text-align: right; margin-top: 25px;'>", unsafe_allow_html=True)
            if st.button("🚪 Sair do Sistema", key="logout_btn", use_container_width=False):
                st.session_state.logged_in = False
                st.session_state.token = None
                st.session_state.user = None
                st.session_state.api_cache = {}
                if "last_entry_result" in st.session_state:
                    del st.session_state["last_entry_result"]
                if "last_exit_result" in st.session_state:
                    del st.session_state["last_exit_result"]
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

    # Sidebar Profissional (Navegação)
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/parking.png", width=64)
        st.markdown("### Navegação")

        nav_options = ["📊 Dashboard", "🅿️ Vagas e Ocupação", "🔄 Movimentação"]
        if user.get("type") == "admin":
            nav_options.append("💰 Faturamento")
        nav_options.append("📋 Cadastros Básicos")

        if user.get("type") == "admin":
            nav_options.append("⚙️ Gestão de Vagas")
            nav_options.append("👥 Gerenciamento de Usuários")

        selected_nav = st.radio("Menu Principal", nav_options, label_visibility="collapsed")

    # Mapear seleção da sidebar para as abas lógicas
    selected_tab = selected_nav.split(" ", 1)[1] if " " in selected_nav else selected_nav

    # --- TELA: DASHBOARD ---
    if selected_tab == "Dashboard":
        st.markdown("### 📊 Visão Geral do Pátio")
        st.markdown("<br>", unsafe_allow_html=True)

        data, err = api_request("GET", "vaga/ocupacao")
        if err:
            st.error(f"Erro ao carregar dados de ocupação: {err.get('message')}")
        else:
            livres = data.get("livres", 0)
            ocupadas = data.get("ocupadas", 0)
            total = livres + ocupadas
            taxa = (ocupadas / total * 100) if total > 0 else 0.0

            # Grid de Métricas Modernizado (SaaS Style usando st.metric)
            m1, m2, m3, m4 = st.columns(4)

            with m1:
                st.metric("Vagas Totais", total)
            with m2:
                st.metric("Vagas Livres", livres, delta=f"{livres} disponíveis", delta_color="normal")
            with m3:
                st.metric("Vagas Ocupadas", ocupadas, delta=f"{ocupadas} em uso", delta_color="inverse")
            with m4:
                st.metric("Taxa de Ocupação", f"{taxa:.1f}%")

            st.markdown("<br>", unsafe_allow_html=True)

            # --- DISTRIBUIÇÃO VISUAL E DETALHAMENTO ---
            col_chart, col_info = st.columns([1, 1.5], gap="large")

            with col_chart:
                st.markdown("#### Distribuição Visual")
                deg = (taxa / 100) * 360
                donut_html = f'''
                <div style="display: flex; justify-content: center; align-items: center; height: 180px;">
                    <div style="width: 150px; height: 150px; border-radius: 50%; background: conic-gradient(#DC2626 0deg {deg}deg, #16A34A {deg}deg 360deg); display: flex; justify-content: center; align-items: center; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
                        <div style="width: 105px; height: 105px; border-radius: 50%; background-color: #FFFFFF; display: flex; flex-direction: column; justify-content: center; align-items: center;">
                            <span style="font-size: 1.4rem; font-weight: 700; color: #1E3A8A;">{taxa:.1f}%</span>
                            <span style="font-size: 0.65rem; color: #64748B; font-weight: 600;">OCUPADO</span>
                        </div>
                    </div>
                </div>
                '''
                st.markdown(donut_html, unsafe_allow_html=True)

            with col_info:
                st.markdown("#### Progresso de Ocupação")
                st.markdown(f"**{ocupadas}** de **{total}** vagas ocupadas ({taxa:.1f}%).")

                # Utilizando st.progress nativo do Streamlit (extremamente confiável e sem bugs de renderização)
                progress_val = float(ocupadas / total) if total > 0 else 0.0
                st.progress(progress_val)

                st.markdown("<br>", unsafe_allow_html=True)

                c_inf1, c_inf2 = st.columns(2)
                with c_inf1:
                    st.metric("Vagas Ocupadas", ocupadas, delta="Em uso", delta_color="inverse")
                with c_inf2:
                    st.metric("Vagas Livres", livres, delta="Disponíveis", delta_color="normal")

            st.markdown("<br><br>", unsafe_allow_html=True)
            st.info("💡 **Dica Operacional:** Utilize a aba 'Movimentação' no menu lateral para registrar novos veículos ou liberar vagas ocupadas.")

    # --- TELA: VAGAS E OCUPAÇÃO ---
    elif selected_tab == "Vagas e Ocupação":
        st.markdown("### 🅿️ Disponibilidade do Pátio")
        st.markdown("Acompanhamento visual detalhado das vagas em tempo real.")
        st.markdown("<br>", unsafe_allow_html=True)

        data, err = api_request("GET", "vaga/ocupacao")
        vagas_list, err_list = cached_api_get(user.get('id'), "vaga", st.session_state.data_version)

        if err:
            st.error(f"Erro ao carregar sumário de vagas: {err.get('message')}")
        else:
            livres = data.get("livres", 0)
            ocupadas = data.get("ocupadas", 0)

            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("🟢 Vagas Livres", livres)
            with col_b:
                st.metric("🔴 Vagas Ocupadas", ocupadas)

            st.markdown("<br>", unsafe_allow_html=True)
            st.subheader("Grade de Vagas")

            if err_list:
                st.warning(f"Atenção: {err_list.get('message', 'Não foi possível carregar a listagem detalhada das vagas no momento.')}")
                st.info("Tente recarregar a página em alguns segundos se o problema persistir (Limite de requisições do Xano).")
            elif vagas_list:
                # Ordenar vagas por número
                sorted_vagas = sorted(vagas_list, key=lambda x: x.get('number', 0))

                cols = st.columns(5)
                for idx, vaga in enumerate(sorted_vagas):
                    col = cols[idx % 5]
                    v_num = vaga.get('number')
                    v_status = vaga.get('status', 'livre')
                    v_type = vaga.get('type', 'carro').capitalize()

                    if v_status == 'ocupada':
                        bg_color = "#FEE2E2"
                        border_color = "#EF4444"
                        text_color = "#991B1B"
                        status_label = "OCUPADA"
                        icon = "🚗"
                    else:
                        bg_color = "#F0FDF4"
                        border_color = "#16A34A"
                        text_color = "#166534"
                        status_label = "LIVRE"
                        icon = "✅"

                    with col:
                        st.markdown(f"""
                        <div style="background-color: {bg_color}; border: 1px solid {border_color}; padding: 16px; border-radius: 12px; text-align: center; margin-bottom: 16px; box-shadow: 0 1px 2px rgba(0,0,0,0.05);">
                            <div style="font-size: 1.5rem; margin-bottom: 4px;">{icon}</div>
                            <h4 style="margin: 0; color: #1E293B; font-size: 1.1rem;">Vaga #{v_num}</h4>
                            <p style="margin: 4px 0; font-size: 0.8rem; color: #64748B; font-weight: 500;">{v_type}</p>
                            <div style="display: inline-block; margin-top: 8px; padding: 2px 8px; border-radius: 4px; background-color: {border_color}; color: white; font-size: 0.7rem; font-weight: 700; letter-spacing: 0.05em;">{status_label}</div>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.info("Nenhuma vaga cadastrada.")

    # --- TELA: FATURAMENTO (ADMIN) ---
    elif selected_tab == "Faturamento" and user.get("type") == "admin":
        st.title("💰 Dashboard Financeiro")
        st.markdown("Acompanhamento de valores cobrados e desempenho financeiro.")
        st.markdown("<br>", unsafe_allow_html=True)

        fin_data, err_f = api_request("GET", "parking/financeiro")

        if err_f:
            st.error(f"Erro ao carregar dados financeiros: {err_f.get('message')}")
        else:
            # Métricas principais
            f1, f2, f3, f4 = st.columns(4)
            with f1:
                st.metric("Faturamento Hoje", f"R$ {fin_data.get('faturamento_dia', 0):.2f}".replace('.', ','))
            with f2:
                st.metric("Faturamento Mês", f"R$ {fin_data.get('faturamento_mes', 0):.2f}".replace('.', ','))
            with f3:
                st.metric("Ticket Médio", f"R$ {fin_data.get('ticket_medio', 0):.2f}".replace('.', ','))
            with f4:
                st.metric("Movimentações", fin_data.get('movimentacoes_concluidas', 0))

            st.markdown("<br>", unsafe_allow_html=True)

            # Histórico detalhado
            st.subheader("📋 Histórico de Movimentações Finalizadas")
            hist = fin_data.get("historico") or []
            if hist:
                df_hist = pd.DataFrame(hist).reindex(
                    columns=['plate', 'vaga_number', 'entry_time', 'exit_time', 'amount']
                )
                df_hist['amount_numeric'] = pd.to_numeric(df_hist['amount'], errors='coerce')

                for column in ('entry_time', 'exit_time'):
                    df_hist[f'{column}_parsed'] = pd.to_datetime(
                        df_hist[column].map(parse_xano_timestamp_utc),
                        errors='coerce',
                        utc=True
                    ).dt.tz_convert("America/Sao_Paulo")

                df_display = df_hist[
                    ['plate', 'vaga_number', 'entry_time_parsed', 'exit_time_parsed', 'amount_numeric']
                ].copy()
                df_display['plate'] = df_display['plate'].astype('string').fillna('—')
                df_display['vaga_number'] = df_display['vaga_number'].astype('string').fillna('—')
                df_display['entry_time_parsed'] = (
                    df_display['entry_time_parsed'].dt.strftime('%d/%m/%Y %H:%M:%S').fillna('—')
                )
                df_display['exit_time_parsed'] = (
                    df_display['exit_time_parsed'].dt.strftime('%d/%m/%Y %H:%M:%S').fillna('—')
                )
                df_display['amount_numeric'] = df_display['amount_numeric'].map(
                    lambda value: f"R$ {value:.2f}".replace('.', ',') if pd.notna(value) else '—'
                )
                df_display.columns = ['Placa', 'Vaga', 'Entrada', 'Saída', 'Valor Cobrado']
                st.dataframe(df_display, use_container_width=True)
            else:
                st.info("Nenhuma movimentação finalizada encontrada no período.")

            # Gráfico de Faturamento Recente
            if hist:
                st.markdown("<br>", unsafe_allow_html=True)
                st.subheader("📈 Evolução Diária (Últimos 10 dias)")
                chart_data = df_hist[
                    ['exit_time_parsed', 'amount_numeric']
                ].dropna(
                    subset=['exit_time_parsed', 'amount_numeric']
                ).copy()
                if not chart_data.empty:
                    chart_data['local_day'] = chart_data['exit_time_parsed'].dt.normalize()
                    chart_data = (
                        chart_data.groupby('local_day')['amount_numeric']
                        .sum()
                        .sort_index()
                        .tail(10)
                        .to_frame('amount')
                    )
                    st.line_chart(chart_data)

    # --- TELA: MOVIMENTAÇÃO ---
    elif selected_tab == "Movimentação":
        st.title("🔄 Registro de Movimentações")
        st.markdown("Controle operacional de entradas e saídas de veículos.")
        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2 = st.columns(2, gap="large")

        with col1:
            st.subheader("📥 Registrar Entrada")

            if "last_entry_result" in st.session_state:
                ler_in = st.session_state["last_entry_result"]
                st.success("Entrada registrada com sucesso!")
                st.info(f"**Placa do Veículo:** {ler_in.get('plate')} | **Vaga Ocupada:** #{ler_in.get('vaga_number')}")
                st.success("Status: Veículo estacionado")
                st.markdown("<hr>", unsafe_allow_html=True)

            # Buscar veículos e vagas livres para seleção dinâmica via cache inteligente
            veiculos_data, err_v = cached_api_get(user.get('id'), "veiculo", st.session_state.data_version)
            vagas_data, err_vg = cached_api_get(user.get('id'), "vaga", st.session_state.data_version)

            livres_vagas = [v for v in (vagas_data or []) if v.get('status') == 'livre' and v.get('active', True)]

            with st.form("entrada_form"):
                veiculo_dict = {f"{v.get('plate')} - {v.get('model')}": (v.get('id'), v.get('plate')) for v in (veiculos_data or [])}
                vaga_dict = {f"Vaga #{v.get('number')} ({v.get('type')})": (v.get('id'), v.get('number')) for v in livres_vagas}

                selected_veiculo_label = st.selectbox("Selecione o Veículo", list(veiculo_dict.keys()) if veiculo_dict else ["Nenhum veículo cadastrado"])
                selected_vaga_label = st.selectbox("Selecione a Vaga Livre", list(vaga_dict.keys()) if vaga_dict else ["Nenhuma vaga livre"])

                st.markdown("<br>", unsafe_allow_html=True)
                submit_entrada = st.form_submit_button("Registrar Entrada", use_container_width=True)

                if submit_entrada:
                    if not veiculo_dict or not vaga_dict:
                        st.error("É necessário ter veículos e vagas livres cadastrados para registrar a entrada.")
                    else:
                        v_id, v_plate = veiculo_dict[selected_veiculo_label]
                        vg_id, vg_number = vaga_dict[selected_vaga_label]
                        payload = {"veiculo_id": int(v_id), "vaga_id": int(vg_id)}
                        res, err = api_request("POST", "parking/entrada", payload)
                        if err:
                            st.error(f"Erro ao registrar entrada: {err.get('message', 'Erro desconhecido.')}")
                        else:
                            st.session_state.data_version += 1
                            vaga_res = res.get("vaga", {})
                            st.session_state['last_entry_result'] = {
                                "plate": v_plate,
                                "vaga_number": vaga_res.get("number", vg_number)
                            }
                            if "last_exit_result" in st.session_state:
                                del st.session_state["last_exit_result"]
                            st.rerun()

        with col2:
            st.subheader("📤 Registrar Saída")

            if "last_exit_result" in st.session_state:
                ler = st.session_state["last_exit_result"]
                st.success("Saída registrada com sucesso!")
                st.info(f"**Placa do Veículo:** {ler.get('plate')} | **Vaga Liberada:** #{ler.get('vaga_number')}")
                if ler.get("entry_time") is not None:
                    st.write(f"**Entrada:** {format_xano_timestamp(ler.get('entry_time'))}")
                if ler.get("exit_time") is not None:
                    st.write(f"**Saída:** {format_xano_timestamp(ler.get('exit_time'))}")
                stay_duration = format_stay_duration(ler.get("entry_time"), ler.get("exit_time"))
                if stay_duration is not None:
                    st.write(f"**Tempo de permanência:** {stay_duration}")
                amount = ler.get('amount')
                if amount is None:
                    st.warning("Valor a Pagar: Valor não informado")
                else:
                    try:
                        amt_float = float(amount)
                        st.metric("Valor a Pagar", f"R$ {amt_float:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
                    except (ValueError, TypeError):
                        st.metric("Valor a Pagar", f"R$ {amount}")
                st.markdown("<hr>", unsafe_allow_html=True)

            movs_abertas, err_m = api_request("GET", "parking/movimentacao/abertas")

            if err_m:
                st.error(f"Erro ao carregar movimentações: {err_m.get('message', 'Erro desconhecido.')}")
                mov_id = None
                m_plate = None
                m_vaga_number = None
                m_entry_time = None
            elif not movs_abertas:
                st.info("Nenhum veículo estacionado no momento.")
                mov_id = None
                m_plate = None
                m_vaga_number = None
                m_entry_time = None
            else:
                selected_mov_index = st.selectbox(
                    "Selecione o Veículo Estacionado",
                    range(len(movs_abertas)),
                    format_func=lambda index: (
                        f"Placa: {movs_abertas[index].get('plate')} | "
                        f"Vaga #{movs_abertas[index].get('vaga_number')}"
                    )
                )
                selected_movement = movs_abertas[selected_mov_index]
                mov_id = selected_movement.get('movimentacao_id')
                m_plate = selected_movement.get('plate')
                m_vaga_number = selected_movement.get('vaga_number')
                m_entry_time = selected_movement.get('entry_time')
                st.info(
                    f"**Movimentação selecionada**  \n"
                    f"**Placa:** {m_plate or '—'} · **Vaga:** #{m_vaga_number or '—'}  \n"
                    f"**Entrada:** {format_xano_timestamp(m_entry_time)}"
                )

            with st.form("saida_form"):
                st.markdown("<br><br>", unsafe_allow_html=True)
                submit_saida = st.form_submit_button("Registrar Saída", use_container_width=True)

                if submit_saida:
                    if not mov_id:
                        st.error("Selecione uma movimentação válida para registrar a saída.")
                    else:
                        payload = {"movimentacao_id": int(mov_id)}
                        res, err = api_request("POST", "parking/saida", payload)
                        if err:
                            st.error(f"Erro ao registrar saída: {err.get('message', 'Erro desconhecido.')}")
                        else:
                            st.session_state.data_version += 1
                            mov_res = res.get("movimentacao", {})
                            vaga_res = res.get("vaga", {})
                            st.session_state['last_exit_result'] = {
                                "mov_id": mov_id,
                                "plate": m_plate,
                                "vaga_number": vaga_res.get("number", m_vaga_number),
                                "entry_time": mov_res.get("entry_time") or m_entry_time,
                                "exit_time": mov_res.get("exit_time"),
                                "amount": mov_res.get("amount")
                            }
                            if "last_entry_result" in st.session_state:
                                del st.session_state["last_entry_result"]
                            st.rerun()

    # --- TELA: CADASTROS BÁSICOS ---
    elif selected_tab == "Cadastros Básicos":
        st.title("📋 Cadastros Básicos")
        st.markdown("Gestão de veículos e clientes mensalistas do estacionamento.")
        st.markdown("<br>", unsafe_allow_html=True)

        cad_tab1, cad_tab2 = st.tabs(["🚗 Veículos", "👤 Mensalistas"])

        with cad_tab1:
            st.subheader("Veículos Cadastrados")
            veiculos_data, err = api_request("GET", "veiculo")
            if err:
                st.error(f"Erro ao listar veículos: {err.get('message', 'Erro desconhecido.')}")
            else:
                if veiculos_data:
                    st.dataframe(veiculos_data, use_container_width=True)
                else:
                    st.info("Nenhum veículo cadastrado.")

            st.markdown("<br>", unsafe_allow_html=True)
            st.subheader("Cadastrar Novo Veículo")

            mensalistas_data, _ = cached_api_get(user.get('id'), "mensalista", st.session_state.data_version)
            mensalista_options = {"Nenhum (Avulso)": None}
            if mensalistas_data:
                for m in mensalistas_data:
                    mensalista_options[f"{m.get('name')} (ID: {m.get('id')})"] = m.get('id')

            with st.form("new_veiculo_form"):
                c1, c2 = st.columns(2)
                with c1:
                    v_plate = st.text_input("Placa do Veículo (ex: ABC1D23)")
                    v_model = st.text_input("Modelo")
                with c2:
                    v_color = st.text_input("Cor")
                    v_type = st.selectbox("Tipo de Veículo", ["carro", "moto", "outro"])

                v_mensalista_label = st.selectbox("Vincular a Mensalista (Opcional)", list(mensalista_options.keys()))

                st.markdown("<br>", unsafe_allow_html=True)
                submit_veiculo = st.form_submit_button("Cadastrar Veículo", use_container_width=True)

                if submit_veiculo:
                    if not v_plate or not v_model:
                        st.warning("Preencha ao menos a placa e o modelo do veículo.")
                    else:
                        payload = {
                            "plate": v_plate.upper().strip(),
                            "model": v_model.strip(),
                            "color": v_color.strip(),
                            "type": v_type,
                            "mensalista_id": mensalista_options[v_mensalista_label]
                        }
                        res, err = api_request("POST", "veiculo", payload)
                        if err:
                            st.error(f"Erro ao cadastrar veículo: {err.get('message', 'Erro ao processar requisição.')}")
                        else:
                            st.session_state.data_version += 1
                            st.success("Veículo cadastrado com sucesso!")
                            st.rerun()

        with cad_tab2:
            st.subheader("Clientes Mensalistas")
            mensalistas_data, err = cached_api_get(user.get('id'), "mensalista", st.session_state.data_version)
            if err:
                st.error(f"Erro ao listar mensalistas: {err.get('message', 'Erro desconhecido.')}")
            else:
                if mensalistas_data:
                    st.dataframe(mensalistas_data, use_container_width=True)
                else:
                    st.info("Nenhum mensalista cadastrado.")

            st.markdown("<br>", unsafe_allow_html=True)
            st.subheader("Cadastrar Novo Mensalista")
            with st.form("new_mensalista_form"):
                c1, c2 = st.columns(2)
                with c1:
                    m_name = st.text_input("Nome Completo")
                    m_phone = st.text_input("Telefone / Contato")
                    m_fee = st.number_input("Valor da Mensalidade (R$)", min_value=0.0, value=280.0, step=10.0)
                with c2:
                    m_start = st.date_input("Data de Início")
                    m_end = st.date_input("Data de Término")

                st.markdown("<br>", unsafe_allow_html=True)
                submit_mensalista = st.form_submit_button("Cadastrar Mensalista", use_container_width=True)

                if submit_mensalista:
                    if not m_name or not m_phone:
                        st.warning("Preencha o nome e o telefone do mensalista.")
                    else:
                        payload = {
                            "name": m_name.strip(),
                            "phone": m_phone.strip(),
                            "monthly_fee": float(m_fee),
                            "start_date": str(m_start),
                            "end_date": str(m_end)
                        }
                        res, err = api_request("POST", "mensalista", payload)
                        if err:
                            st.error(f"Erro ao cadastrar mensalista: {err.get('message', 'Erro ao processar requisição.')}")
                        else:
                            st.session_state.data_version += 1
                            st.success("Mensalista cadastrado com sucesso!")
                            st.rerun()

    # --- TELA: GESTÃO DE VAGAS (ADMIN) ---
    elif selected_tab == "Gestão de Vagas" and user.get("type") == "admin":
        st.title("⚙️ Gestão de Vagas (Administrador)")
        st.markdown("Painel administrativo para cadastro, listagem, edição e desativação lógica de vagas.")
        st.markdown("<br>", unsafe_allow_html=True)

        vaga_tab1, vaga_tab2, vaga_tab3, vaga_tab4 = st.tabs(["📋 Listagem de Vagas", "➕ Cadastrar Vaga", "✏️ Editar Vaga", "🗑️ Desativar Vaga"])

        with vaga_tab1:
            st.subheader("Vagas Ativas Cadastradas")
            vagas_data, err = cached_api_get(user.get('id'), "vaga", st.session_state.data_version)
            if err:
                st.error(f"Erro ao listar vagas: {err.get('message', 'Erro desconhecido.')}")
            else:
                if vagas_data:
                    st.dataframe(vagas_data, use_container_width=True)
                else:
                    st.info("Nenhuma vaga cadastrada no momento.")

        with vaga_tab2:
            st.subheader("Cadastrar Nova Vaga")
            with st.form("new_vaga_form"):
                vaga_number = st.number_input("Número da Vaga", min_value=1, step=1)
                vaga_type = st.selectbox("Tipo de Vaga", ["carro", "moto", "idoso", "deficiente"])
                st.markdown("<br>", unsafe_allow_html=True)
                submit_vaga = st.form_submit_button("Cadastrar Vaga", use_container_width=True)

                if submit_vaga:
                    payload = {"number": int(vaga_number), "type": vaga_type}
                    res, err = api_request("POST", "vaga", payload)
                    if err:
                        st.error(f"Erro ao cadastrar vaga: {err.get('message', 'Erro ao processar requisição.')}")
                    else:
                        st.session_state.data_version += 1
                        st.success(f"Vaga número {vaga_number} cadastrada com sucesso!")
                        st.rerun()

        with vaga_tab3:
            st.subheader("Editar Vaga Existente")
            vagas_data, err = cached_api_get(user.get('id'), "vaga", st.session_state.data_version)
            if err:
                st.error(f"Erro ao carregar vagas: {err.get('message', 'Erro desconhecido.')}")
            elif not vagas_data:
                st.info("Nenhuma vaga disponível para edição.")
            else:
                vaga_options = {f"Vaga #{v.get('number')} (ID: {v.get('id')})": v for v in vagas_data}
                selected_vaga_label = st.selectbox("Selecione a Vaga", list(vaga_options.keys()))
                selected_vaga = vaga_options[selected_vaga_label]

                with st.form("edit_vaga_form"):
                    new_number = st.number_input("Novo Número", min_value=1, step=1, value=int(selected_vaga.get('number', 1)))
                    new_type = st.selectbox("Novo Tipo", ["carro", "moto", "idoso", "deficiente"], index=["carro", "moto", "idoso", "deficiente"].index(selected_vaga.get('type', 'carro')))
                    st.markdown("<br>", unsafe_allow_html=True)
                    submit_edit = st.form_submit_button("Salvar Alterações", use_container_width=True)

                    if submit_edit:
                        payload = {"number": int(new_number), "type": new_type}
                        res, err = api_request("PATCH", f"vaga/{selected_vaga.get('id')}", payload)
                        if err:
                            st.error(f"Erro ao atualizar vaga: {err.get('message', 'Erro ao processar requisição.')}")
                        else:
                            st.session_state.data_version += 1
                            st.success(f"Vaga ID {selected_vaga.get('id')} atualizada com sucesso!")
                            st.rerun()

        with vaga_tab4:
            st.subheader("Desativação Lógica de Vaga")
            st.warning("⚠️ A desativação lógica (active = false) reserva o número permanentemente e impede novas entradas. Vagas ocupadas ou com movimentação em aberto não podem ser desativadas.")

            vagas_data, err = cached_api_get(user.get('id'), "vaga", st.session_state.data_version)
            if err:
                st.error(f"Erro ao carregar vagas: {err.get('message', 'Erro desconhecido.')}")
            elif not vagas_data:
                st.info("Nenhuma vaga disponível para desativação.")
            else:
                livres_vagas = [v for v in vagas_data if v.get('status') == 'livre' and v.get('active', True)]
                if not livres_vagas:
                    st.info("Não há vagas livres no momento para desativação (vagas ocupadas não podem ser desativadas).")
                else:
                    deactivate_options = {f"Vaga #{v.get('number')} (ID: {v.get('id')}) - Status: {v.get('status')}": v for v in livres_vagas}
                    selected_deactivate_label = st.selectbox("Selecione a Vaga para Desativar", list(deactivate_options.keys()))
                    target_vaga = deactivate_options[selected_deactivate_label]

                    with st.form("deactivate_vaga_form"):
                        st.write(f"**Detalhes da Vaga:** Número {target_vaga.get('number')} | Tipo: {target_vaga.get('type')} | Status: {target_vaga.get('status')}")
                        confirm_deactivate = st.checkbox("Confirmo que desejo desativar esta vaga logicamente.")
                        st.markdown("<br>", unsafe_allow_html=True)
                        submit_deactivate = st.form_submit_button("Desativar Vaga", use_container_width=True)

                        if submit_deactivate:
                            if not confirm_deactivate:
                                st.error("Você precisa marcar a caixa de confirmação para prosseguir.")
                            else:
                                payload = {"active": False}
                                res, err = api_request("PATCH", f"vaga/{target_vaga.get('id')}", payload)
                                if err:
                                    st.error(f"Erro ao desativar vaga: {err.get('message', 'Erro ao processar requisição.')}")
                                else:
                                    st.session_state.data_version += 1
                                    st.success(f"Vaga número {target_vaga.get('number')} desativada com sucesso!")
                                    st.rerun()

    # --- TELA: GERENCIAMENTO DE USUÁRIOS (ADMIN) ---
    elif selected_tab == "Gerenciamento de Usuários" and user.get("type") == "admin":
        st.title("👥 Gestão de Usuários (Administrador)")
        st.markdown("Painel administrativo para controle de operadores e administradores do sistema.")
        st.markdown("<br>", unsafe_allow_html=True)

        users_data, err = cached_api_get(user.get('id'), "usuario", st.session_state.data_version)
        if err:
            st.error(f"Erro ao listar usuários: {err.get('message')}")
        else:
            st.subheader("Usuários Cadastrados")
            st.dataframe(users_data, use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("Cadastrar Novo Usuário")
        with st.form("new_user_form"):
            c1, c2 = st.columns(2)
            with c1:
                new_name = st.text_input("Nome completo")
                new_email = st.text_input("E-mail corporativo")
            with c2:
                new_password = st.text_input("Senha", type="password")
                new_type = st.selectbox("Perfil de Acesso", ["operador", "admin"])

            st.markdown("<br>", unsafe_allow_html=True)
            submit_user = st.form_submit_button("Cadastrar Usuário", use_container_width=True)

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
                    st.session_state.data_version += 1
                    st.success("Usuário criado com sucesso!")
                    st.rerun()
