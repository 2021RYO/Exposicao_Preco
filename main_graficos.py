import streamlit as st
import pandas as pd
import os
import plotly.graph_objects as go

# Caminho do Excel
EXCEL_PATH = "Evolucao.xlsx"

st.set_page_config(page_title="📈 Evolução de Preços", layout="wide")
st.title("📊 Painel de Evolução de Preços e Exposição")

if not os.path.exists(EXCEL_PATH):
    st.error(f"❌ Arquivo Excel não encontrado: `{EXCEL_PATH}`.")
else:
    try:
        xls = pd.ExcelFile(EXCEL_PATH)

        # ========== GRÁFICO 1: EVOLUÇÃO GESTORA ==========
        st.header("📈 Evolução por Gestora")
        df_gestora = pd.read_excel(xls, sheet_name="Historico_Posicoes_Gestora")
        df_gestora['Data'] = pd.to_datetime(df_gestora['Data'], dayfirst=True, errors='coerce')
        df_gestora = df_gestora.dropna(subset=['Data'])

        df_gestora['Exposicao %'] = df_gestora['Exposicao Gestora'] / 100

        ativos_g = sorted(df_gestora['Ativo'].dropna().unique())
        ativo_sel_g = st.selectbox("Selecione o ativo (Gestora):", ativos_g)

        filtro_g = df_gestora[df_gestora['Ativo'] == ativo_sel_g].sort_values(by='Data')

        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=filtro_g['Data'], y=filtro_g['Preco'], mode='lines', name='Preço'))
        fig1.add_trace(go.Scatter(
            x=filtro_g['Data'],
            y=filtro_g['Exposicao %'],
            mode='lines',
            name='Exposição (%)',
            yaxis='y2'
        ))

        fig1.update_layout(
            title=f"Evolução: {ativo_sel_g} - Gestora",
            xaxis=dict(title='Data'),
            yaxis=dict(title='Preço'),
            yaxis2=dict(title='Exposição (%)', overlaying='y', side='right', tickformat=".2%"),
            legend=dict(title='Variável')
        )

        st.plotly_chart(fig1, use_container_width=True)

        # ========== GRÁFICO 2: EVOLUÇÃO FUNDOS ==========
        st.header("📉 Evolução por Fundo")
        df_fundos = pd.read_excel(xls, sheet_name="Historico_Posicoes_Fundos")
        df_fundos['Data'] = pd.to_datetime(df_fundos['Data'], dayfirst=True, errors='coerce')
        df_fundos = df_fundos.dropna(subset=['Data'])

        df_fundos['Exposicao %'] = df_fundos['Exposicao Fundo'] / 100

        fundos_f = sorted(df_fundos['Fundo'].dropna().unique())
        ativos_f = sorted(df_fundos['Ativo'].dropna().unique())

        fundo_sel = st.selectbox("Selecione o fundo (Fundo):", fundos_f)
        ativo_sel = st.selectbox("Selecione o ativo (Fundo):", ativos_f)

        filtro_f = df_fundos[
            (df_fundos['Fundo'] == fundo_sel) & 
            (df_fundos['Ativo'] == ativo_sel)
        ].sort_values(by='Data')

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=filtro_f['Data'], y=filtro_f['Preco'], mode='lines', name='Preço'))
        fig2.add_trace(go.Scatter(
            x=filtro_f['Data'],
            y=filtro_f['Exposicao %'],
            mode='lines',
            name='Exposição (%)',
            yaxis='y2'
        ))

        fig2.update_layout(
            title=f"Evolução: {ativo_sel} - Fundo {fundo_sel}",
            xaxis=dict(title='Data'),
            yaxis=dict(title='Preço'),
            yaxis2=dict(title='Exposição (%)', overlaying='y', side='right', tickformat=".2%"),
            legend=dict(title='Variável')
        )

        st.plotly_chart(fig2, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Erro ao processar o arquivo: {e}")
