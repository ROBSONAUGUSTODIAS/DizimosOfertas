"""
Página de Registro de Lançamentos
Permite cadastrar novos dízimos, ofertas e contribuições
Otimizado para Desktop e Mobile
"""
import streamlit as st
from datetime import datetime
from database import adicionar_lancamento
from config import TIPOS_PAGAMENTO, CATEGORIAS
from utils import validar_nome, validar_valor
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
    Com dados de contato opcionais
    Layout responsivo para mobile
    """
    config = detectar_mobile()
    
    st.subheader("➕ Registrar Novo Lançamento")
    
    # Inicializa contador de formulários para forçar reset
    if "form_counter" not in st.session_state:
        st.session_state.form_counter = 0
    
    with st.form(key=f"registrar_form_{st.session_state.form_counter}"):
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
        
        # Telefone/Celular (opcional)
        telefone = st.text_input(
            "Celular (opcional)",
            max_chars=15,
            placeholder="(11) 99999-9999",
            help="Celular com DDD para cadastro"
        )
        
        # Email (OPCIONAL)
        email = st.text_input(
            "Email (opcional)",
            max_chars=100,
            placeholder="exemplo@email.com",
            help="Email para registro"
        )
        
        # Botão de submit - Full width em mobile
        st.markdown("---")
        submit_button = st.form_submit_button("✅ Registrar Lançamento", type="primary", width="stretch")
        
        # ============================================
        # PROCESSAMENTO DO FORMULÁRIO
        # ============================================
        if submit_button:
            # Mostra indicador de carregamento para validação e processamento
            with st.spinner("🔄 Processando lançamento..."):
                # Validação do nome
                if not validar_nome(nome):
                    st.error("❌ O nome deve ter pelo menos 2 caracteres.")
                    return
                
                # Validação do valor
                if not validar_valor(valor):
                    st.error("❌ O valor deve ser maior que zero.")
                    return
                
                telefone_formatado = None
                if telefone.strip():
                    telefone_valido, msg_telefone = validar_telefone(telefone)
                    if not telefone_valido:
                        st.error(f"❌ {msg_telefone}")
                        return
                    telefone_formatado = formatar_telefone(telefone)
                
                # Mostra progresso detalhado
                progress_placeholder = st.empty()
                progress_placeholder.info("💾 Salvando dados no banco...")
                
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
                    progress_placeholder.empty()
                    st.success("✅ Lançamento registrado com sucesso!")
                    
                    # Incrementa contador do formulário para forçar limpeza dos campos
                    st.session_state.form_counter += 1
                    
                    # Mostra mensagem de reload
                    with st.spinner("🔄 Limpando formulário..."):
                        import time
                        time.sleep(1.5)
                    st.rerun()
                else:
                    progress_placeholder.empty()
                    st.error("❌ Erro ao registrar lançamento. Tente novamente.")
