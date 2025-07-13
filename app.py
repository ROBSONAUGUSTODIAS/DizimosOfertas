import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
from streamlit_option_menu import option_menu
from PIL import Image

# ============================================
# CONFIGURAÇÃO DE USUÁRIOS E ACESSOS
# ============================================

USUARIOS = {
    "admin": "Admin@#",
    "pastor": "pastor@#",
    "tesoureiro": "teseoureiro@#",
    "diacono01": "diacono01@#",
    "diacono02": "diacono02@#"
}

NIVEIS_ACESSO = {
    "admin": "admin",
    "pastor": "visualizador",
    "tesoureiro": "editor",
    "diacono01": "admin",
    "diacono02": "admin"
}

NOMES_USUARIOS = {
    "admin": "Administrador",
    "pastor": "Pastor Marcio",
    "tesoureiro": "Tesoureira Telma",
    "diacono01": "Diácono01",
    "diacono02": "Diácono02"
}

# ============================================
# FUNÇÕES DO SISTEMA
# ============================================

def display_logo():
    try:
        logo = Image.open("./imagem/igrejadechomai.jpg")
        st.image(logo, width=150)
    except:
        st.markdown("""
        <style>
            .logo {
                font-size: 15px;
                font-weight: bold;
                color: #2c3e50;
                margin-bottom: 15px;
            }
        </style>
        <div class="logo">MINISTÉRIO DECHONAI</div>
        """, unsafe_allow_html=True)

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
            categoria TEXT NOT NULL,
            usuario TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def adicionar_lancamento(data, nome, valor, tipo, categoria, usuario):
    conn = sqlite3.connect("dizimos_ofertas.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO lancamentos (data, nome, valor, tipo, categoria, usuario) 
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (data, nome, valor, tipo, categoria, usuario))
    conn.commit()
    conn.close()

def obter_lancamentos(usuario=None):
    conn = sqlite3.connect("dizimos_ofertas.db")
    cursor = conn.cursor()
    
    if usuario and NIVEIS_ACESSO.get(usuario) != "admin":
        cursor.execute('''
            SELECT id, data, nome, valor, tipo, categoria 
            FROM lancamentos 
            WHERE usuario = ? 
            ORDER BY data DESC
        ''', (usuario,))
    else:
        cursor.execute('''
            SELECT id, data, nome, valor, tipo, categoria, usuario 
            FROM lancamentos 
            ORDER BY data DESC
        ''')
    
    lancamentos = cursor.fetchall()
    conn.close()
    return lancamentos

def atualizar_lancamento(id_lancamento, data, nome, valor, tipo, categoria):
    conn = sqlite3.connect("dizimos_ofertas.db")
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE lancamentos 
        SET data = ?, nome = ?, valor = ?, tipo = ?, categoria = ?
        WHERE id = ?
    ''', (data, nome, valor, tipo, categoria, id_lancamento))
    conn.commit()
    conn.close()

def excluir_lancamento(id_lancamento):
    conn = sqlite3.connect("dizimos_ofertas.db")
    cursor = conn.cursor()
    cursor.execute('DELETE FROM lancamentos WHERE id = ?', (id_lancamento,))
    conn.commit()
    conn.close()

def verificar_login(usuario, senha):
    if usuario in USUARIOS and USUARIOS[usuario] == senha:
        return {
            "usuario": usuario,
            "nome": NOMES_USUARIOS.get(usuario, usuario),
            "nivel": NIVEIS_ACESSO.get(usuario, "visualizador")
        }
    return None

# ============================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================

st.set_page_config(
    page_title="Dízimos e Ofertas",
    page_icon="💰",
    layout="wide"
)

# ============================================
# TELA DE LOGIN
# ============================================

if "usuario" not in st.session_state:
    st.title("💻 Tela de Login")
    
    with st.form("login_form"):
        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")
        submitted = st.form_submit_button("Entrar")
        
        if submitted:
            usuario_info = verificar_login(usuario, senha)
            if usuario_info:
                st.session_state["usuario"] = usuario_info["usuario"]
                st.session_state["nome"] = usuario_info["nome"]
                st.session_state["nivel"] = usuario_info["nivel"]
                st.success(f"Bem-vindo, {usuario_info['nome']}!")
                st.rerun()
            else:
                st.error("Credenciais inválidas. Tente novamente.")

# ============================================
# PÁGINA PRINCIPAL (APÓS LOGIN)
# ============================================

else:
    col_title, col_user_info = st.columns([4, 2])
    with col_title:
        st.title("Sistema de Dízimos e Ofertas")
    with col_user_info:
        st.write(f"Usuário: {st.session_state['nome']}")
        st.write(f"Nível: {st.session_state['nivel'].capitalize()}")
        if st.button("Sair"):
            st.session_state.clear()
            st.rerun()

    init_db()

    opcoes_menu = ["Visualizar"]
    if st.session_state["nivel"] in ["admin", "editor"]:
        opcoes_menu.append("Registrar")
    if st.session_state["nivel"] == "admin":
        opcoes_menu.append("Editar")
    
    with st.sidebar:
        display_logo()
        escolha = option_menu(
            "Menu",
            opcoes_menu,
            icons=["list", "plus-circle", "pencil-square"],
            menu_icon="menu",
            default_index=0
        )

    if escolha == "Visualizar":
        st.subheader("📊 Lançamentos Recentes")
        lancamentos = obter_lancamentos(st.session_state["usuario"])
        
        if lancamentos:
            columns = ["ID", "Data", "Nome", "Valor (R$)", "Tipo", "Categoria"]
            if st.session_state["nivel"] == "admin":
                columns.append("Usuário")
            
            dados = []
            for lanc in lancamentos:
                linha = [
                    lanc[0],
                    datetime.strptime(lanc[1], "%Y-%m-%d").strftime("%d/%m/%Y"),
                    lanc[2],
                    f"R$ {lanc[3]:.2f}",
                    lanc[4],
                    lanc[5]
                ]
                if st.session_state["nivel"] == "admin":
                    linha.append(lanc[6])
                dados.append(linha)
            
            df = pd.DataFrame(dados, columns=columns)
            st.dataframe(df, use_container_width=True, hide_index=True)

            # ============================================
            # RESUMO FINANCEIRO MELHORADO
            # ============================================
            st.subheader("📈 Resumo Financeiro")
            st.markdown("---") # Separador visual

            # Cálculos para o resumo
            total_geral = sum(l[3] for l in lancamentos)
            hoje = datetime.today().strftime("%Y-%m-%d")
            mes_atual_str = datetime.today().strftime("%Y-%m")
            
            lancamentos_hoje = [l for l in lancamentos if l[1] == hoje]
            lancamentos_mes_atual = [l for l in lancamentos if l[1].startswith(mes_atual_str)]

            total_dia = sum(l[3] for l in lancamentos_hoje)
            total_mes = sum(l[3] for l in lancamentos_mes_atual)
            
            total_dizimo_geral = sum(l[3] for l in lancamentos if l[5] == "Dízimo")
            total_oferta_geral = sum(l[3] for l in lancamentos if l[5] == "Oferta")
            total_visitante_geral = sum(l[3] for l in lancamentos if l[5] == "Visitante")

            total_dizimo_mes = sum(l[3] for l in lancamentos_mes_atual if l[5] == "Dízimo")
            total_oferta_mes = sum(l[3] for l in lancamentos_mes_atual if l[5] == "Oferta")
            total_visitante_mes = sum(l[3] for l in lancamentos_mes_atual if l[5] == "Visitante")

            # Exibição das métricas principais
            st.markdown("#### Totais de Entradas")
            col1, col2, col3 = st.columns(3)
            col1.metric("Hoje", f"R$ {total_dia:.2f}", help="Total de entradas registradas hoje")
            col2.metric(f"Mês Atual ({datetime.today().strftime('%b/%Y')})", f"R$ {total_mes:.2f}", help="Total de entradas registradas no mês atual")
            col3.metric("Total Geral (Desde o Início)", f"R$ {total_geral:.2f}", help="Total de todas as entradas registradas")

            st.markdown("---")
            st.markdown("#### Detalhes por Categoria (Mês Atual)")
            col4, col5, col6 = st.columns(3)
            col4.metric("Dízimos", f"R$ {total_dizimo_mes:.2f}")
            col5.metric("Ofertas", f"R$ {total_oferta_mes:.2f}")
            col6.metric("Visitantes", f"R$ {total_visitante_mes:.2f}")

            # Gráfico de distribuição mensal
            if total_dizimo_mes > 0 or total_oferta_mes > 0 or total_visitante_mes > 0:
                st.markdown("---")
                st.markdown("#### Distribuição Mensal de Dízimos, Ofertas e Visitantes")
                chart_data = pd.DataFrame({
                    'Categoria': ['Dízimo', 'Oferta', 'Visitante'],
                    'Valor': [total_dizimo_mes, total_oferta_mes, total_visitante_mes]
                })
                st.bar_chart(chart_data.set_index('Categoria'))

            # Seção expansível para totais gerais por categoria
            with st.expander("Ver Totais Gerais por Categoria (Acumulado)"):
                st.write(f"**Total Geral de Dízimos:** R$ {total_dizimo_geral:.2f}")
                st.write(f"**Total Geral de Ofertas:** R$ {total_oferta_geral:.2f}")
                st.write(f"**Total Geral de Visitantes:** R$ {total_visitante_geral:.2f}")
            # ============================================
            # FIM DO RESUMO FINANCEIRO MELHORADO
            # ============================================

        else:
            st.info("ℹ️ Nenhum lançamento registrado ainda.")

    elif escolha == "Registrar" and st.session_state["nivel"] in ["admin", "editor"]:
        st.subheader("➕ Registrar Novo Lançamento")
        with st.form("registrar_form"):
            data = st.date_input("Data", value=datetime.today())
            nome = st.text_input("Nome", max_chars=100)
            valor = st.number_input("Valor (R$)", min_value=0.01, step=0.01, format="%.2f")
            tipo = st.selectbox("Tipo de Pagamento", ["Dinheiro", "Cartão", "Transferência", "Cheque"," Pix"])
            categoria = st.selectbox("Categoria", ["Dízimo", "Oferta", "Visitante"])
            submit_button = st.form_submit_button("Registrar")
            
            if submit_button:
                adicionar_lancamento(
                    data.strftime("%Y-%m-%d"),
                    nome.strip(),
                    float(valor),
                    tipo,
                    categoria,
                    st.session_state["usuario"]
                )
                st.success("Lançamento registrado com sucesso!")
                st.rerun()

    elif escolha == "Editar" and st.session_state["nivel"] == "admin":
        st.subheader("✏️ Editar Lançamentos")
        lancamentos = obter_lancamentos()
        
        if lancamentos:
            lancamentos_para_edicao = {f"ID: {l[0]} - {l[2]} - R$ {l[3]:.2f} - {l[1]}": l[0] for l in lancamentos}
            selected = st.selectbox("Selecione um lançamento para editar", options=list(lancamentos_para_edicao.keys()))
            id_selecionado = lancamentos_para_edicao[selected]
            
            lancamento_selecionado = [l for l in lancamentos if l[0] == id_selecionado][0]
            
            with st.form("editar_form"):
                data = st.date_input("Data", value=datetime.strptime(lancamento_selecionado[1], "%Y-%m-%d"))
                nome = st.text_input("Nome", value=lancamento_selecionado[2])
                valor = st.number_input("Valor (R$)", value=float(lancamento_selecionado[3]), min_value=0.01, step=0.01, format="%.2f")
                
                tipos_pagamento = ["Dinheiro", "Cartão", "Transferência", "Cheque", "Pix"]
                try:
                    index_tipo = tipos_pagamento.index(lancamento_selecionado[4])
                except ValueError:
                    index_tipo = 0
                
                tipo = st.selectbox("Tipo de Pagamento", tipos_pagamento, index=index_tipo)
                
                categorias = ["Dízimo", "Oferta", "Visitante"]
                try:
                    index_categoria = categorias.index(lancamento_selecionado[5])
                except ValueError:
                    index_categoria = 0
                
                categoria = st.selectbox("Categoria", categorias, index=index_categoria)
                
                col1, col2 = st.columns(2)
                with col1:
                    atualizar_btn = st.form_submit_button("Atualizar")
                with col2:
                    excluir_btn = st.form_submit_button("Excluir")
                
                if atualizar_btn:
                    atualizar_lancamento(
                        id_selecionado,
                        data.strftime("%Y-%m-%d"),
                        nome.strip(),
                        float(valor),
                        tipo,
                        categoria
                    )
                    st.success("Lançamento atualizado com sucesso!")
                    st.rerun()
                
                if excluir_btn:
                    excluir_lancamento(id_selecionado)
                    st.success("Lançamento excluído com sucesso!")
                    st.rerun()
        else:
            st.info("ℹ️ Nenhum lançamento disponível para edição")
