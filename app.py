"""
Sistema de Gestão de Dízimos e Ofertas
Arquitetura Modular com Separação de Responsabilidades
Otimizado para Desktop e Mobile
"""
import streamlit as st
from streamlit_option_menu import option_menu

# Importações dos módulos personalizados
from config import PAGE_TITLE, PAGE_ICON, LAYOUT
from database import init_db
from auth import verificar_login, pode_editar, pode_administrar
from utils import display_logo, exibir_usuario_info
from modules.visualizar import exibir_pagina_visualizar
from modules.registrar import exibir_pagina_registrar
from modules.editar import exibir_pagina_editar
from mobile_config import aplicar_css_mobile


def exibir_tela_login():
    """Exibe a tela de login - otimizado para mobile"""
    # Centralizar conteúdo em mobile
    col1, col2, col3 = st.columns([1, 6, 1])
    
    with col2:
        st.title("💻 Login")
        
        # Debug: Verificar se secrets estão configurados (Streamlit Cloud)
        from config import USUARIOS_HASHES
        if not any(USUARIOS_HASHES.values()):
            st.error("⚠️ **ERRO DE CONFIGURAÇÃO**")
            st.warning("""
            Os **Secrets não estão configurados** no Streamlit Cloud!
            
            **Solução:**
            1. Acesse: [App Settings](https://share.streamlit.io/)
            2. Clique em **Settings** → **Secrets**
            3. Cole este conteúdo:
            """)
            st.code("""[passwords]
USER_ADMIN_HASH = "$2b$12$kKdAncvxkviV412Bj.WuMe2ve/Qaqkn4sq1CiFXh.QeWF6Bp1hXbq"
USER_DIACONO01_HASH = "$2b$12$7erenEeA2eP5HecUUGGtp.LRxYuxXqYWKb/zNwT8VOIpM6UyeWMEy"
USER_DIACONO02_HASH = "$2b$12$7rxfZGjQqq9cOnpaiRvRnu9vLhNKmKVAFh2zwEvfC9fdaaqmEfSN"
""", language="toml")
            st.info("📖 Veja o guia completo: TROUBLESHOOTING_LOGIN.md")
        
        st.markdown("---")
        
        # Botão de diagnóstico (expander)
        with st.expander("🔍 Diagnóstico de Configuração (clique se login não funcionar)"):
            from config import USUARIOS_HASHES, USE_STREAMLIT_SECRETS
            
            st.write("**Ambiente:**", "Streamlit Cloud" if USE_STREAMLIT_SECRETS else "Desenvolvimento Local")
            st.write("**Secrets carregados:**")
            
            for usuario, hash_val in USUARIOS_HASHES.items():
                if hash_val:
                    st.success(f"✅ {usuario}: Hash configurado ({hash_val[:20]}...)")
                else:
                    st.error(f"❌ {usuario}: Hash NÃO configurado (None)")
            
            if USE_STREAMLIT_SECRETS:
                st.info("""
                **Como corrigir secrets não configurados:**
                1. Acesse Settings → Secrets no Streamlit Cloud
                2. Cole o conteúdo TOML fornecido acima
                3. Salve e aguarde o restart do app
                """)
            
            st.write("**Credenciais de TESTE:**")
            st.code("""
Usuário: admin
Senha: AdminSeguro@2026

Usuário: diacono01  
Senha: Diacono01@2026

Usuário: diacono02
Senha: Diacono02@2026
""")
        
        with st.form("login_form"):
            usuario = st.text_input("Usuário", placeholder="Digite seu usuário")
            senha = st.text_input("Senha", type="password", placeholder="Digite sua senha")
            
            st.markdown("""
            <style>
            .stFormSubmitButton button {
                width: 100%;
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
            }
            </style>
            """, unsafe_allow_html=True)
            
            submitted = st.form_submit_button("🔐 Entrar", type="primary")
            
            if submitted:
                usuario_info = verificar_login(usuario, senha)
                if usuario_info:
                    st.session_state["usuario"] = usuario_info["usuario"]
                    st.session_state["nome"] = usuario_info["nome"]
                    st.session_state["nivel"] = usuario_info["nivel"]
                    st.success(f"✅ Bem-vindo, {usuario_info['nome']}!")
                    st.rerun()
                else:
                    st.error("❌ Credenciais inválidas. Tente novamente.")


def configurar_menu():
    """Configura o menu lateral com base nas permissões do usuário"""
    opcoes_menu = ["Visualizar"]
    icons = ["list"]
    
    if pode_editar(st.session_state["nivel"]):
        opcoes_menu.append("Registrar")
        icons.append("plus-circle")
    
    if pode_administrar(st.session_state["nivel"]):
        opcoes_menu.append("Editar")
        icons.append("pencil-square")
    
    with st.sidebar:
        display_logo()
        escolha = option_menu(
            "Menu",
            opcoes_menu,
            icons=icons,
            menu_icon="menu-app",
            default_index=0
        )
    
    return escolha


def exibir_pagina_principal():
    """Exibe a página principal após o login"""
    # Exibir informações do usuário no topo
    exibir_usuario_info()
    
    # Configurar menu lateral
    escolha = configurar_menu()
    
    # Renderizar página selecionada
    if escolha == "Visualizar":
        exibir_pagina_visualizar()
    
    elif escolha == "Registrar" and pode_editar(st.session_state["nivel"]):
        exibir_pagina_registrar()
    
    elif escolha == "Editar" and pode_administrar(st.session_state["nivel"]):
        exibir_pagina_editar()


def main():
    """Função principal da aplicação"""
    # Configuração da página - layout centered para melhor mobile
    st.set_page_config(
        page_title=PAGE_TITLE,
        page_icon=PAGE_ICON,
        layout=LAYOUT,
        initial_sidebar_state="collapsed"  # Sidebar fechada em mobile por padrão
    )
    
    # Aplicar CSS responsivo para mobile
    aplicar_css_mobile()
    
    # Inicializar banco de dados
    init_db()
    
    # Verificar estado de autenticação
    if "usuario" not in st.session_state:
        exibir_tela_login()
    else:
        exibir_pagina_principal()


if __name__ == "__main__":
    main()

