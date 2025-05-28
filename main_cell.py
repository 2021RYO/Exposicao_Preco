import streamlit as st
import pandas as pd
import os
import plotly.graph_objects as go

# Caminho do Excel
EXCEL_PATH = "Evolucao.xlsx"

# Layout centralizado para celular
st.set_page_config(page_title="📈 Preços e Exposição", layout="centered")
st.title("📊 Evolução de Preços e Exposição")

if not os.path.exists(EXCEL_PATH):
    st.error(f"❌ Arquivo Excel não encontrado: `{EXCEL_PATH}`.")
else:
    try:
        xls = pd.ExcelFile(EXCEL_PATH)

        # ========== GRÁFICO 1: GESTORA ==========
        st.subheader("📈 Evolução por Gestora")
        df_gestora = pd.read_excel(xls, sheet_name="Historico_Posicoes_Gestora")
        df_gestora['Data'] = pd.to_datetime(df_gestora['Data'], dayfirst=True, errors='coerce')
        df_gestora = df_gestora.dropna(subset=['Data'])

        df_gestora['Exposicao %'] = df_gestora['Exposicao Gestora'] / 100

        ativo_g = st.selectbox("🔎 Ativo (Gestora):", sorted(df_gestora['Ativo'].dropna().unique()))
        dados_g = df_gestora[df_gestora['Ativo'] == ativo_g].sort_values(by='Data')

        with st.expander(f"📊 Gráfico {ativo_g} - Gestora", expanded=True):
            fig1 = go.Figure()
            fig1.add_trace(go.Scatter(x=dados_g['Data'], y=dados_g['Preco'], mode='lines', name='Preço'))
            fig1.add_trace(go.Scatter(
                x=dados_g['Data'], y=dados_g['Exposicao %'],
                mode='lines', name='Exposição (%)', yaxis='y2'
            ))

            fig1.update_layout(
                xaxis=dict(title='Data'),
                yaxis=dict(title='Preço'),
                yaxis2=dict(title='Exposição (%)', overlaying='y', side='right', tickformat=".2%"),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
            )

            st.plotly_chart(fig1, use_container_width=True)

        # ========== GRÁFICO 2: FUNDOS ==========
        st.subheader("📉 Evolução por Fundo")
        df_fundos = pd.read_excel(xls, sheet_name="Historico_Posicoes_Fundos")
        df_fundos['Data'] = pd.to_datetime(df_fundos['Data'], dayfirst=True, errors='coerce')
        df_fundos = df_fundos.dropna(subset=['Data'])

        df_fundos['Exposicao %'] = df_fundos['Exposicao Fundo'] / 100

        fundo_f = st.selectbox("🏦 Fundo:", sorted(df_fundos['Fundo'].dropna().unique()))
        ativo_f = st.selectbox("🔎 Ativo (Fundo):", sorted(df_fundos['Ativo'].dropna().unique()))
        dados_f = df_fundos[(df_fundos['Fundo'] == fundo_f) & (df_fundos['Ativo'] == ativo_f)].sort_values(by='Data')

        with st.expander(f"📊 Gráfico {ativo_f} - Fundo {fundo_f}", expanded=True):
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(x=dados_f['Data'], y=dados_f['Preco'], mode='lines', name='Preço'))
            fig2.add_trace(go.Scatter(
                x=dados_f['Data'], y=dados_f['Exposicao %'],
                mode='lines', name='Exposição (%)', yaxis='y2'
            ))

            fig2.update_layout(
                xaxis=dict(title='Data'),
                yaxis=dict(title='Preço'),
                yaxis2=dict(title='Exposição (%)', overlaying='y', side='right', tickformat=".2%"),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
            )

            st.plotly_chart(fig2, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Erro ao processar o arquivo: {e}")
