import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
from streamlit_option_menu import option_menu

# Credenciais de login (simples)
USER_CREDENTIALS = {"usuario": "admin", "senha": "1234"}

# Função para inicializar o banco de dados
def init_db():
    conn = sqlite3.connect("dizimos_ofertas.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lancamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT NOT NULL,
            nome TEXT NOT NULL,
            valor REAL NOT NULL,
            tipo TEXT NOT NULL,
            categoria TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Função para adicionar um lançamento
def adicionar_lancamento(data, nome, valor, tipo, categoria):
    conn = sqlite3.connect("dizimos_ofertas.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO lancamentos (data, nome, valor, tipo, categoria) VALUES (?, ?, ?, ?, ?)", 
                   (data, nome, valor, tipo, categoria))
    conn.commit()
    conn.close()

# Função para obter os lançamentos
def obter_lancamentos():
    conn = sqlite3.connect("dizimos_ofertas.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, data, nome, valor, tipo, categoria FROM lancamentos ORDER BY data DESC")
    lancamentos = cursor.fetchall()
    conn.close()
    return lancamentos

# Função para obter a soma dos lançamentos por dia
def obter_soma_por_dia():
    conn = sqlite3.connect("dizimos_ofertas.db")
    cursor = conn.cursor()
    cursor.execute("SELECT data, SUM(valor) FROM lancamentos GROUP BY data ORDER BY data DESC")
    soma_por_dia = cursor.fetchall()
    conn.close()
    return soma_por_dia

# Função para atualizar um lançamento
def atualizar_lancamento(id, data, nome, valor, tipo, categoria):
    conn = sqlite3.connect("dizimos_ofertas.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE lancamentos SET data = ?, nome = ?, valor = ?, tipo = ?, categoria = ? WHERE id = ?", 
                   (data, nome, valor, tipo, categoria, id))
    conn.commit()
    conn.close()

# Função para verificar o login
def verificar_login(usuario, senha):
    if usuario == USER_CREDENTIALS["usuario"] and senha == USER_CREDENTIALS["senha"]:
        return True
    return False

# Configuração da página
st.set_page_config(page_title="Dízimos e Ofertas", page_icon="💰", layout="wide")

# Tela de login
if "logado" not in st.session_state or not st.session_state["logado"]:
    st.title("💻 Tela de Login")
    
    with st.form("login_form"):
        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")
        login_btn = st.form_submit_button("Entrar")
        
        if login_btn:
            if verificar_login(usuario, senha):
                st.session_state["logado"] = True
                st.success("Login bem-sucedido!")
                st.rerun()  # Redireciona após login
            else:
                st.error("Credenciais inválidas. Tente novamente.")
else:
    # Menu lateral após login
    with st.sidebar:
        escolha = option_menu("Menu", ["Registrar", "Visualizar", "Editar"], icons=["plus-circle", "list", "pencil-square"], menu_icon="menu")

    # Inicializar banco de dados
    init_db()

    # Adicionar botão de Sair
    if st.sidebar.button("Sair"):
        st.session_state["logado"] = False
        st.session_state.clear()  # Limpa a sessão
        st.experimental_rerun()  # Redireciona para a tela de login
    
    # Seção de "Registrar"
    if escolha == "Registrar":
        st.subheader("📌 Registrar Novo Lançamento")
        with st.form("form_lancamento"):
            data = st.date_input("Data do Lançamento", datetime.today())
            nome = st.text_input("Nome da Pessoa")
            valor = st.number_input("Valor da Oferta/Dízimo", min_value=0.01, format="%.2f")
            tipo = st.selectbox("Forma de Pagamento", ["Dinheiro","Pix" ,"Máquina de Cartão"])
            categoria = st.selectbox("Categoria", ["Dízimo", "Oferta"])  # Nova opção de categoria
            submitted = st.form_submit_button("Registrar")
            if submitted:
                if nome.strip():
                    adicionar_lancamento(data.strftime("%Y-%m-%d"), nome, valor, tipo, categoria)
                    st.success("✅ Lançamento registrado com sucesso!")
                else:
                    st.error("⚠️ Por favor, insira o nome da pessoa.")

    # Seção de "Visualizar"
    elif escolha == "Visualizar":
        st.subheader("📊 Lançamentos Recentes")
        lancamentos = obter_lancamentos()
        if lancamentos:
            # Formatar as datas antes de exibir
            lancamentos_formatados = [(l[0], datetime.strptime(l[1], "%Y-%m-%d").strftime("%d/%m/%Y"), l[2], l[3], l[4], l[5]) for l in lancamentos]
            df = pd.DataFrame(lancamentos_formatados, columns=["ID", "Data", "Nome", "Valor", "Forma de Pagamento", "Categoria"])
            st.dataframe(df, use_container_width=True)
        else:
            st.write("🔍 Nenhum lançamento registrado.")

        st.subheader("📈 Total de Lançamentos por Dia")
        soma_por_dia = obter_soma_por_dia()
        if soma_por_dia:
            df_soma = pd.DataFrame(soma_por_dia, columns=["Data", "Total do Dia"])
            st.dataframe(df_soma, use_container_width=True)
        else:
            st.write("📉 Nenhuma soma disponível.")

    # Seção de "Editar"
    elif escolha == "Editar":
        st.sidebar.subheader("✏️ Editar Lançamento")
        id_edit = st.sidebar.number_input("ID do Lançamento para Editar", min_value=1, step=1)
        data_edit = st.sidebar.date_input("Nova Data")
        nome_edit = st.sidebar.text_input("Novo Nome")
        valor_edit = st.sidebar.number_input("Novo Valor", min_value=0.01, format="%.2f")
        tipo_edit = st.sidebar.selectbox("Nova Forma de Pagamento", ["Dinheiro", "Máquina de Cartão","Pix"])
        categoria_edit = st.sidebar.selectbox("Nova Categoria", ["Dízimo","Pix" ,"Oferta"])  # Nova categoria
        edit_submit = st.sidebar.button("Atualizar Lançamento")

        if edit_submit:
            atualizar_lancamento(id_edit, data_edit.strftime("%Y-%m-%d"), nome_edit, valor_edit, tipo_edit, categoria_edit)
            st.sidebar.success("✅ Lançamento atualizado com sucesso!")
            st.experimental_rerun()  # Recarrega a página
