"""
Página de Registro de Lançamentos
Permite cadastrar novos dízimos, ofertas e contribuições com envio de WhatsApp
Otimizado para Desktop e Mobile
"""
import streamlit as st
import re
from datetime import datetime
from database import adicionar_lancamento
from config import TIPOS_PAGAMENTO, CATEGORIAS
from utils import validar_nome, validar_valor, formatar_data
from whatsapp_service import enviar_whatsapp_contribuicao
from mobile_config import detectar_mobile


def validar_telefone(telefone: str) -> tuple[bool, str]:
    """
    Valida formato de telefone brasileiro
    
    Args:
        telefone: Número de telefone
    
    Returns:
        (valido: bool, mensagem: str)
    
    Formatos aceitos:
    - (11) 99999-9999
    - 11999999999
    - 11 999999999
    """
    if not telefone:
        return False, "Telefone é obrigatório."
    
    # Remove caracteres não numéricos
    numeros = ''.join(filter(str.isdigit, telefone))
    
    # Valida quantidade de dígitos (DDD + 9 dígitos)
    if len(numeros) != 11:
        return False, "Telefone deve conter 11 dígitos (DDD + 9 dígitos)."
    
    # Valida se começa com dígito 9 (celular)
    if numeros[2] != '9':
        return False, "Número deve ser de celular (iniciar com 9)."
    
    return True, "Telefone válido."


def formatar_telefone(telefone: str) -> str:
    """
    Formata telefone para padrão visual
    
    Args:
        telefone: Telefone com apenas números
    
    Returns:
        String formatada: (11) 99999-9999
    """
    numeros = ''.join(filter(str.isdigit, telefone))
    if len(numeros) == 11:
        return f"({numeros[:2]}) {numeros[2:7]}-{numeros[7:]}"
    return telefone


def exibir_pagina_registrar():
    """
    Exibe a página de registro de novos lançamentos
    Com foco em WhatsApp e email opcional
    Layout responsivo para mobile
    """
    config = detectar_mobile()
    
    st.subheader("➕ Registrar Novo Lançamento")
    
    # Informação sobre notificações WhatsApp
    st.info("📱 **WhatsApp:** Disponível apenas para pagamentos via **PIX**! Preencha o celular para enviar confirmação automática.")
    
    with st.form("registrar_form"):
        # ============================================
        # SEÇÃO: DADOS DO LANÇAMENTO
        # ============================================
        st.markdown("#### 📋 Dados do Lançamento")
        
        # Data da contribuição
        data = st.date_input(
            "Data", 
            value=datetime.today(),
            help="Data em que a contribuição foi realizada"
        )
        
        # Nome do contribuinte
        nome = st.text_input(
            "Nome Completo *", 
            max_chars=100,
            placeholder="Digite o nome completo",
            help="Nome completo do contribuinte"
        )
        
        # Valor da contribuição
        valor = st.number_input(
            "Valor (R$) *", 
            min_value=0.01, 
            step=0.01, 
            format="%.2f",
            help="Valor da contribuição em reais"
        )
        
        # Tipo de pagamento - responsivo, empilha em mobile via CSS
        col1, col2 = st.columns(config["form_dupla"])
        with col1:
            tipo = st.selectbox(
                "Tipo de Pagamento *", 
                TIPOS_PAGAMENTO,
                help="Forma de pagamento utilizada"
            )
        
        with col2:
            categoria = st.selectbox(
                "Categoria *", 
                CATEGORIAS,
                help="Tipo de contribuição"
            )
        
        # ============================================
        # SEÇÃO: DADOS DE CONTATO
        # ============================================
        st.markdown("---")
        st.markdown("#### 📞 Dados de Contato")
        
        # Telefone/Celular (OBRIGATÓRIO para WhatsApp)
        telefone = st.text_input(
            "Celular (WhatsApp) *",
            max_chars=15,
            placeholder="(11) 99999-9999",
            help="Celular com DDD para envio de confirmação via WhatsApp"
        )
        
        # Email (OPCIONAL)
        email = st.text_input(
            "Email (opcional)",
            max_chars=100,
            placeholder="exemplo@email.com",
            help="Email para registro (opcional - WhatsApp é prioritário)"
        )
        
        # Checkbox para enviar WhatsApp (APENAS PARA PIX)
        enviar_whatsapp = False
        if tipo == "Pix":
            enviar_whatsapp = st.checkbox(
                "📲 Enviar confirmação via WhatsApp",
                value=True,
                help="Confirmação automática via WhatsApp disponível apenas para pagamentos PIX"
            )
        else:
            st.info("ℹ️ Confirmação via WhatsApp disponível apenas para pagamentos via **PIX**")
        
        # Botão de submit - Full width em mobile
        st.markdown("---")
        submit_button = st.form_submit_button("✅ Registrar Lançamento", type="primary", use_container_width=True)
        
        # ============================================
        # PROCESSAMENTO DO FORMULÁRIO
        # ============================================
        if submit_button:
            # Validação do nome
            if not validar_nome(nome):
                st.error("❌ O nome deve ter pelo menos 2 caracteres.")
                return
            
            # Validação do valor
            if not validar_valor(valor):
                st.error("❌ O valor deve ser maior que zero.")
                return
            
            # Validação do telefone
            telefone_valido, msg_telefone = validar_telefone(telefone)
            if not telefone_valido:
                st.error(f"❌ {msg_telefone}")
                return
            
            # Formata telefone para salvamento
            telefone_formatado = formatar_telefone(telefone)
            
            # Adicionar lançamento ao banco
            sucesso = adicionar_lancamento(
                data.strftime("%Y-%m-%d"),
                nome.strip(),
                float(valor),
                tipo,
                categoria,
                st.session_state["usuario"],
                email.strip() if email else None,
                telefone=telefone_formatado
            )
            
            if sucesso:
                st.success("✅ Lançamento registrado com sucesso!")
                
                # Enviar WhatsApp se solicitado e se for PIX
                if enviar_whatsapp and tipo == "Pix":
                    with st.spinner("📱 Enviando confirmação via WhatsApp..."):
                        sucesso_whats, msg_whats = enviar_whatsapp_contribuicao(
                            telefone_formatado,
                            nome.strip(),
                            float(valor),
                            categoria,
                            formatar_data(data.strftime("%Y-%m-%d"))
                        )
                        
                        if sucesso_whats:
                            st.success(f"📲 {msg_whats}")
                        else:
                            st.warning(f"⚠️ Lançamento registrado, mas: {msg_whats}")
                
                # Aguarda um pouco e recarrega
                import time
                time.sleep(2)
                st.rerun()
            else:
                st.error("❌ Erro ao registrar lançamento. Tente novamente.")
