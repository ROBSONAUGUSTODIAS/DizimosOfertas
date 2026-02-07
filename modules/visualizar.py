"""
Página de Visualização de Lançamentos
Otimizado para visualização em Desktop e Mobile
"""
import streamlit as st
import pandas as pd
from datetime import datetime
from database import obter_lancamentos
from utils import formatar_data, formatar_valor, calcular_totais
from mobile_config import detectar_mobile


def exibir_pagina_visualizar():
    """
    Exibe a página de visualização de lançamentos
    Mostra todos os dados incluindo informações de contato
    Layout responsivo para mobile
    """
    st.subheader("📊 Lançamentos Recentes")
    
    lancamentos = obter_lancamentos(
        st.session_state["usuario"],
        st.session_state["nivel"]
    )
    
    if lancamentos:
        # Resumo Financeiro ANTES da tabela para mobile
        exibir_resumo_financeiro(lancamentos)
        
        st.markdown("---")
        st.markdown("#### 📋 Tabela de Lançamentos")
        
        # Montagem da tabela com novos campos
        columns = ["ID", "Data", "Nome", "Valor (R$)", "Tipo", "Categoria", "Usuário", "Email", "Celular"]
        
        dados = []
        for lanc in lancamentos:
            # Dados básicos (sempre presentes)
            linha = [
                lanc[0],  # ID
                formatar_data(lanc[1]),  # Data
                lanc[2],  # Nome
                formatar_valor(lanc[3]),  # Valor
                lanc[4],  # Tipo
                lanc[5],  # Categoria
            ]
            
            # Verificar se é admin (tem coluna usuario na query)
            if st.session_state["nivel"] == "admin":
                usuario = lanc[6] if len(lanc) > 6 else "-"
                email = lanc[7] if len(lanc) > 7 else None
                codigo_area = lanc[8] if len(lanc) > 8 else None
                celular = lanc[9] if len(lanc) > 9 else None
            else:
                usuario = st.session_state["usuario"]
                email = lanc[6] if len(lanc) > 6 else None
                codigo_area = lanc[7] if len(lanc) > 7 else None
                celular = lanc[8] if len(lanc) > 8 else None
            
            # Adicionar usuário
            linha.append(usuario if usuario else "-")
            
            # Adicionar email
            linha.append(email if email else "-")
            
            # Adicionar celular formatado
            if codigo_area and celular:
                celular_formatado = f"({codigo_area}) {celular}"
            else:
                celular_formatado = "-"
            
            linha.append(celular_formatado)
            dados.append(linha)
        
        df = pd.DataFrame(dados, columns=columns)
        
        # Info sobre scroll horizontal em mobile
        st.info("👉 Deslize para o lado para ver mais colunas")
        
        # Tabela com altura fixa e scroll
        st.dataframe(
            df, 
            use_container_width=True, 
            hide_index=True,
            height=400  # Altura fixa para melhor controle em mobile
        )
        
    else:
        st.info("ℹ️ Nenhum lançamento registrado ainda.")


def exibir_resumo_financeiro(lancamentos):
    """Exibe o resumo financeiro dos lançamentos - layout responsivo"""
    config = detectar_mobile()
    
    st.subheader("📈 Resumo Financeiro")
    st.markdown("---")
    
    totais = calcular_totais(lancamentos)
    
    # Exibição das métricas principais
    st.markdown("#### 💵 Totais de Entradas")
    
    # Métricas em colunas que colapsam em mobile via CSS
    col1, col2, col3 = st.columns(config["metricas_principais"])
    
    with col1:
        st.metric(
            "📅 Hoje", 
            formatar_valor(totais["total_dia"]), 
            help="Total de entradas registradas hoje"
        )
    
    mes_atual = datetime.today().strftime('%b/%Y')
    with col2:
        st.metric(
            f"📆 Mês ({mes_atual})", 
            formatar_valor(totais["total_mes"]), 
            help="Total de entradas registradas no mês atual"
        )
    
    with col3:
        st.metric(
            "📊 Total Geral", 
            formatar_valor(totais["total_geral"]), 
            help="Total de todas as entradas registradas"
        )
    
    # Detalhes por Categoria
    st.markdown("---")
    st.markdown("#### 🎯 Detalhes por Categoria (Mês Atual)")
    
    col4, col5, col6 = st.columns(config["metricas_principais"])
    
    with col4:
        st.metric("💵 Dízimos", formatar_valor(totais["total_dizimo_mes"]))
    with col5:
        st.metric("🎁 Ofertas", formatar_valor(totais["total_oferta_mes"]))
    with col6:
        st.metric("👥 Visitantes", formatar_valor(totais["total_visitante_mes"]))
    
    # Gráfico de distribuição mensal
    if any([totais["total_dizimo_mes"], totais["total_oferta_mes"], totais["total_visitante_mes"]]):
        st.markdown("---")
        st.markdown("#### 📊 Distribuição Mensal")
        chart_data = pd.DataFrame({
            'Categoria': ['Dízimo', 'Oferta', 'Visitante'],
            'Valor': [
                totais["total_dizimo_mes"], 
                totais["total_oferta_mes"], 
                totais["total_visitante_mes"]
            ]
        })
        st.bar_chart(chart_data.set_index('Categoria'), use_container_width=True)
    
    # Seção expansível para totais gerais
    with st.expander("📁 Ver Totais Gerais por Categoria (Acumulado)"):
        st.write(f"**Total Geral de Dízimos:** {formatar_valor(totais['total_dizimo_geral'])}")
        st.write(f"**Total Geral de Ofertas:** {formatar_valor(totais['total_oferta_geral'])}")
        st.write(f"**Total Geral de Visitantes:** {formatar_valor(totais['total_visitante_geral'])}")
