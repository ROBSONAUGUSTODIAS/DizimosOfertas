"""
Página de Visualização de Lançamentos
Otimizado para visualização em Desktop e Mobile
"""
import streamlit as st
import pandas as pd
import base64
import streamlit.components.v1 as components
from datetime import datetime, timedelta
from database import obter_lancamentos
from utils import formatar_data, formatar_valor, calcular_totais
from mobile_config import detectar_mobile


def exibir_pagina_visualizar():
    """
    Exibe a página de visualização de lançamentos
    Mostra todos os dados incluindo informações de contato
    Layout responsivo para mobile
    """
    st.subheader("📊 Consulta de Lançamentos")

    todos_lancamentos = obter_lancamentos(
        st.session_state["usuario"],
        st.session_state["nivel"]
    )

    if todos_lancamentos:
        modo_consulta = st.radio(
            "Período da consulta",
            ["Histórico completo", "Últimos 30 dias"],
            horizontal=True
        )

        if modo_consulta == "Histórico completo":
            lancamentos = todos_lancamentos
        else:
            data_limite = datetime.today().date() - timedelta(days=30)
            lancamentos = []
            for lanc in todos_lancamentos:
                try:
                    data_lancamento = datetime.strptime(lanc[1], "%Y-%m-%d").date()
                    if data_lancamento >= data_limite:
                        lancamentos.append(lanc)
                except ValueError:
                    continue

        st.caption(f"{len(lancamentos)} lançamento(s) encontrado(s) para a consulta selecionada")

        if not lancamentos:
            st.info("ℹ️ Nenhum lançamento encontrado para o período selecionado.")
            return

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
            width="stretch", 
            hide_index=True,
            height=400  # Altura fixa para melhor controle em mobile
        )

        exibir_exportacao_csv(df)
        
    else:
        st.info("ℹ️ Nenhum lançamento registrado ainda.")


def exibir_exportacao_csv(df):
    """Exibe ações de exportação CSV com suporte a compartilhamento no celular."""
    st.markdown("---")
    st.markdown("#### ⬇️ Exportar Dados")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo = f"lancamentos_{timestamp}.csv"

    csv_texto = df.to_csv(index=False, sep=";", encoding="utf-8-sig")
    csv_bytes = csv_texto.encode("utf-8-sig")

    st.download_button(
        label="⬇️ Baixar CSV",
        data=csv_bytes,
        file_name=nome_arquivo,
        mime="text/csv",
        use_container_width=True,
        key=f"download_csv_{timestamp}"
    )

    st.caption("No celular, toque em **📲 Compartilhar CSV** e escolha **Google Drive** para salvar na nuvem.")

    csv_base64 = base64.b64encode(csv_bytes).decode("utf-8")

    components.html(
        f"""
        <div style="margin-top: 8px; margin-bottom: 8px;">
            <button id="shareCsvBtn" style="
                width: 100%;
                min-height: 44px;
                border: 1px solid #d0d7de;
                border-radius: 8px;
                background: #f6f8fa;
                color: #24292f;
                font-weight: 600;
                font-size: 16px;
                cursor: pointer;
            ">
                📲 Compartilhar CSV (celular)
            </button>
            <div id="shareCsvStatus" style="font-size: 13px; margin-top: 6px; color: #57606a;"></div>
        </div>

        <script>
        const botao = document.getElementById('shareCsvBtn');
        const status = document.getElementById('shareCsvStatus');
        const csvBase64 = "{csv_base64}";
        const fileName = "{nome_arquivo}";

        function base64ParaBytes(base64) {{
            const binario = atob(base64);
            const tamanho = binario.length;
            const bytes = new Uint8Array(tamanho);
            for (let i = 0; i < tamanho; i++) {{
                bytes[i] = binario.charCodeAt(i);
            }}
            return bytes;
        }}

        botao.addEventListener('click', async () => {{
            status.textContent = '';
            try {{
                const bytes = base64ParaBytes(csvBase64);
                const arquivo = new File([bytes], fileName, {{ type: 'text/csv;charset=utf-8;' }});

                if (navigator.share && navigator.canShare && navigator.canShare({{ files: [arquivo] }})) {{
                    await navigator.share({{
                        title: 'Exportação de Lançamentos',
                        text: 'Arquivo CSV dos lançamentos',
                        files: [arquivo]
                    }});
                    status.textContent = 'Compartilhado com sucesso.';
                    return;
                }}

                const blob = new Blob([bytes], {{ type: 'text/csv;charset=utf-8;' }});
                const url = URL.createObjectURL(blob);
                const link = document.createElement('a');
                link.href = url;
                link.download = fileName;
                document.body.appendChild(link);
                link.click();
                link.remove();
                URL.revokeObjectURL(url);
                status.textContent = 'Seu navegador não suportou compartilhamento direto. Foi iniciado o download.';
            }} catch (erro) {{
                status.textContent = 'Não foi possível compartilhar agora. Use o botão Baixar CSV.';
            }}
        }});
        </script>
        """,
        height=110
    )


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
        st.bar_chart(chart_data.set_index('Categoria'), width="stretch")
    
    # Seção expansível para totais gerais
    with st.expander("📁 Ver Totais Gerais por Categoria (Acumulado)"):
        st.write(f"**Total Geral de Dízimos:** {formatar_valor(totais['total_dizimo_geral'])}")
        st.write(f"**Total Geral de Ofertas:** {formatar_valor(totais['total_oferta_geral'])}")
        st.write(f"**Total Geral de Visitantes:** {formatar_valor(totais['total_visitante_geral'])}")
