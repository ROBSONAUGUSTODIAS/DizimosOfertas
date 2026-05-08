"""
Sistema de Gestão de Dízimos e Ofertas
Arquitetura Modular com Separação de Responsabilidades
Otimizado para Desktop e Mobile
"""
import streamlit as st
from streamlit_option_menu import option_menu
from datetime import datetime, timedelta

# Importações dos módulos personalizados
from config import PAGE_TITLE, PAGE_ICON, LAYOUT
from database import init_db
from auth import verificar_login
from utils import display_logo, exibir_usuario_info
from modules.visualizar import exibir_pagina_visualizar
from modules.registrar import exibir_pagina_registrar
from modules.editar import exibir_pagina_editar
from modules.membros import exibir_pagina_membros
from modules.duvidas import exibir_pagina_duvidas
from modules.aniversariantes import exibir_pagina_aniversariantes
from modules.certificado import exibir_pagina_certificado
from modules.permissoes import exibir_painel_permissoes
from modules.newsletter import exibir_pagina_newsletter
from modules.calendario import exibir_pagina_calendario
from mobile_config import aplicar_css_mobile
from permissions import usuario_tem_permissao


def exibir_tela_login():
    """Exibe a tela de login - otimizado para mobile"""
    # Proteção básica contra tentativa excessiva de login por sessão
    if "login_tentativas" not in st.session_state:
        st.session_state["login_tentativas"] = 0
    if "login_bloqueado_ate" not in st.session_state:
        st.session_state["login_bloqueado_ate"] = None

    # Centralizar conteúdo em mobile
    col1, col2, col3 = st.columns([1, 6, 1])
    
    with col2:
        # ── Logo Ministério Dehomai ──────────────────────────────────────
        import os
        logo_login = "./imagem/logo-login.png"
        if os.path.exists(logo_login):
            c1, c2, c3 = st.columns([1.5, 1, 1.5])
            with c2:
                st.image(logo_login, use_container_width=True)
        else:
            st.title("🔐 Login")

        # Debug: Verificar se secrets estão configurados (Streamlit Cloud)
        from config import USUARIOS_HASHES
        if not any(USUARIOS_HASHES.values()):
            st.error("⚠️ **ERRO DE CONFIGURAÇÃO**")
            st.warning("""
            Os **Secrets não estão configurados** no Streamlit Cloud!
            
            **Solução:**
            1. Acesse: [App Settings](https://share.streamlit.io/)
            2. Clique em **Settings** → **Secrets**
            3. Configure os hashes dos usuários no formato exigido
            """)
            st.info("📖 Veja o guia completo: TROUBLESHOOTING_LOGIN.md")
        
        st.markdown("---")
        
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
                bloqueado_ate = st.session_state.get("login_bloqueado_ate")
                agora = datetime.now()
                if bloqueado_ate and agora < bloqueado_ate:
                    restante = int((bloqueado_ate - agora).total_seconds() // 60) + 1
                    st.error(f"❌ Muitas tentativas inválidas. Tente novamente em {restante} minuto(s).")
                    return

                usuario_info = verificar_login(usuario, senha)
                if usuario_info:
                    st.session_state["login_tentativas"] = 0
                    st.session_state["login_bloqueado_ate"] = None
                    st.session_state["usuario"] = usuario_info["usuario"]
                    st.session_state["nome"] = usuario_info["nome"]
                    st.session_state["nivel"] = usuario_info["nivel"]
                    st.session_state["ultima_atividade"] = datetime.now().isoformat()
                    st.success(f"✅ Bem-vindo, {usuario_info['nome']}!")
                    st.rerun()
                else:
                    st.session_state["login_tentativas"] += 1
                    if st.session_state["login_tentativas"] >= 5:
                        st.session_state["login_bloqueado_ate"] = datetime.now() + timedelta(minutes=15)
                        st.error("❌ Muitas tentativas inválidas. Acesso bloqueado por 15 minutos.")
                        return
                    st.error("❌ Credenciais inválidas. Tente novamente.")


def configurar_menu():
    """Configura o menu lateral com base nas permissões do usuário"""
    usuario = st.session_state["usuario"]
    nivel   = st.session_state["nivel"]

    opcoes_menu = []
    icons = []

    # Cada módulo aparece no menu somente se o usuário tiver permissão
    if usuario_tem_permissao(usuario, "visualizar"):
        opcoes_menu.append("Visualizar")
        icons.append("list")

    if usuario_tem_permissao(usuario, "registrar"):
        opcoes_menu.append("Registrar")
        icons.append("plus-circle")

    if usuario_tem_permissao(usuario, "editar"):
        opcoes_menu.append("Editar")
        icons.append("pencil-square")

    if usuario_tem_permissao(usuario, "membros"):
        opcoes_menu.append("Cadastro de Membros")
        icons.append("people")

    if usuario_tem_permissao(usuario, "aniversariantes"):
        opcoes_menu.append("Aniversariantes")
        icons.append("balloon-heart")

    if usuario_tem_permissao(usuario, "certificado"):
        opcoes_menu.append("Certificado")
        icons.append("award")

    if usuario_tem_permissao(usuario, "newsletter"):
        opcoes_menu.append("Newsletter")
        icons.append("envelope-paper")

    if usuario_tem_permissao(usuario, "calendario"):
        opcoes_menu.append("Calendário")
        icons.append("calendar-event")

    # Painel de permissões — exclusivo para admin
    if nivel == "admin":
        opcoes_menu.append("Permissões")
        icons.append("shield-lock")

    # Dúvidas está sempre disponível para todos
    opcoes_menu.append("Dúvidas")
    icons.append("question-circle")
    
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
    usuario = st.session_state["usuario"]
    nivel   = st.session_state["nivel"]

    if escolha == "Visualizar" and usuario_tem_permissao(usuario, "visualizar"):
        exibir_pagina_visualizar()

    elif escolha == "Registrar" and usuario_tem_permissao(usuario, "registrar"):
        exibir_pagina_registrar()

    elif escolha == "Cadastro de Membros" and usuario_tem_permissao(usuario, "membros"):
        exibir_pagina_membros()

    elif escolha == "Aniversariantes" and usuario_tem_permissao(usuario, "aniversariantes"):
        exibir_pagina_aniversariantes()

    elif escolha == "Certificado" and usuario_tem_permissao(usuario, "certificado"):
        exibir_pagina_certificado()

    elif escolha == "Newsletter" and usuario_tem_permissao(usuario, "newsletter"):
        exibir_pagina_newsletter()

    elif escolha == "Calendário" and usuario_tem_permissao(usuario, "calendario"):
        exibir_pagina_calendario()

    elif escolha == "Editar" and usuario_tem_permissao(usuario, "editar"):
        exibir_pagina_editar()

    elif escolha == "Permissões" and nivel == "admin":
        exibir_painel_permissoes()

    elif escolha == "Dúvidas":
        exibir_pagina_duvidas()


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
        # Expiração básica de sessão por inatividade
        agora = datetime.now()
        ultima_atividade = st.session_state.get("ultima_atividade")
        if ultima_atividade:
            try:
                ultimo_acesso = datetime.fromisoformat(ultima_atividade)
                if (agora - ultimo_acesso) > timedelta(minutes=30):
                    st.session_state.clear()
                    st.warning("⚠️ Sessão expirada por inatividade. Faça login novamente.")
                    st.rerun()
            except ValueError:
                pass

        st.session_state["ultima_atividade"] = agora.isoformat()
        exibir_pagina_principal()


if __name__ == "__main__":
    main()

