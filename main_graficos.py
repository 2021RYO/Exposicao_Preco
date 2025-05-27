import streamlit as st
import pandas as pd
import os
import plotly.graph_objects as go

# Caminho relativo ao arquivo Excel
EXCEL_PATH = "Evolucao.xlsx"

st.set_page_config(page_title="📈 Evolução de Preços", layout="wide")
st.title("📊 Painel de Evolução de Preços e Exposição")

# Verifica se o arquivo existe
if not os.path.exists(EXCEL_PATH):
    st.error(f"❌ Arquivo Excel não encontrado: `{EXCEL_PATH}`.")
else:
    try:
        xls = pd.ExcelFile(EXCEL_PATH)

        # ========== GRÁFICO 1: EVOLUÇÃO GESTORA ==========
        st.header("📈 Evolução por Gestora")
        df_gestora = pd.read_excel(xls, sheet_name="Historico_Posicoes_Gestora")
        df_gestora['Data'] = pd.to_datetime(df_gestora['Data'], errors='coerce')
        df_gestora = df_gestora.dropna(subset=['Data'])

        # Calcula percentual
        df_gestora['Quantidade %'] = df_gestora['Quantidade'] / 100

        gestores = df_gestora['Gestora'].dropna().unique()
        ativo = st.selectbox("Selecione o ativo (Gestora):", sorted(df_gestora['Ativo'].dropna().unique()))
        gestora = st.selectbox("Selecione a gestora:", sorted(gestores))

        filtro_gestora = df_gestora[(df_gestora['Gestora'] == gestora) & (df_gestora['Ativo'] == ativo)]
        filtro_gestora = filtro_gestora.sort_values(by='Data')

        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=filtro_gestora['Data'], y=filtro_gestora['Preço'], mode='lines', name='Preço'))
        fig1.add_trace(go.Scatter(x=filtro_gestora['Data'], y=filtro_gestora['Quantidade %'], mode='lines', name='Quantidade (%)', yaxis='y2'))

        fig1.update_layout(
            title=f"Evolução: {ativo} - Gestora {gestora}",
            xaxis=dict(title='Data'),
            yaxis=dict(title='Preço'),
            yaxis2=dict(title='Quantidade (%)', overlaying='y', side='right', tickformat=".2%"),
            legend=dict(title='Variável')
        )

        st.plotly_chart(fig1, use_container_width=True)

        # ========== GRÁFICO 2: EVOLUÇÃO FUNDOS ==========
        st.header("📉 Evolução por Fundo")

        df_fundo = pd.read_excel(xls, sheet_name="Historico_Posicoes_Fundo")
        df_fundo['Data'] = pd.to_datetime(df_fundo['Data'], errors='coerce')
        df_fundo = df_fundo.dropna(subset=['Data'])

        df_fundo['Quantidade %'] = df_fundo['Quantidade'] / 100

        fundos = df_fundo['Fundo'].dropna().unique()
        ativos_fundo = df_fundo['Ativo'].dropna().unique()

        fundo_sel = st.selectbox("Selecione o fundo:", sorted(fundos))
        ativo_sel = st.selectbox("Selecione o ativo (Fundo):", sorted(ativos_fundo))

        filtro_fundo = df_fundo[(df_fundo['Fundo'] == fundo_sel) & (df_fundo['Ativo'] == ativo_sel)]
        filtro_fundo = filtro_fundo.sort_values(by='Data')

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=filtro_fundo['Data'], y=filtro_fundo['Preço'], mode='lines', name='Preço'))
        fig2.add_trace(go.Scatter(x=filtro_fundo['Data'], y=filtro_fundo['Quantidade %'], mode='lines', name='Quantidade (%)', yaxis='y2'))

        fig2.update_layout(
            title=f"Evolução: {ativo_sel} - Fundo {fundo_sel}",
            xaxis=dict(title='Data'),
            yaxis=dict(title='Preço'),
            yaxis2=dict(title='Quantidade (%)', overlaying='y', side='right', tickformat=".2%"),
            legend=dict(title='Variável')
        )

        st.plotly_chart(fig2, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Erro ao processar o arquivo: {e}")
