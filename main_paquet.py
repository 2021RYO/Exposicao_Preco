#import pandas as pd

# Convertendo para .parquet
#pd.read_excel("Evolucao.xlsx", sheet_name="Historico_Posicoes_Gestora").to_parquet("gestora.parquet", index=False)
#pd.read_excel("Evolucao.xlsx", sheet_name="Historico_Posicoes_Fundos").to_parquet("fundos.parquet", index=False)


import streamlit as st
import pandas as pd
import os
import plotly.graph_objects as go

# Arquivos parquet
GESTORA_PARQUET = "gestora.parquet"
FUNDOS_PARQUET = "fundos.parquet"

st.set_page_config(page_title="📈 Preços - Parquet", layout="centered")
st.title("📊 Teste com Arquivo Parquet")

# Verificação dos arquivos
if not os.path.exists(GESTORA_PARQUET) or not os.path.exists(FUNDOS_PARQUET):
    st.error("❌ Arquivos .parquet não encontrados. Envie 'gestora.parquet' e 'fundos.parquet'.")
else:
    try:
        # GESTORA
        st.subheader("📈 Evolução por Gestora")
        df_gestora = pd.read_parquet(GESTORA_PARQUET)
        df_gestora['Data'] = pd.to_datetime(df_gestora['Data'], dayfirst=True, errors='coerce')
        df_gestora = df_gestora.dropna(subset=['Data'])
        df_gestora['Exposicao %'] = df_gestora['Exposicao Gestora'] / 100

        ativo_g = st.selectbox("🔎 Ativo (Gestora):", sorted(df_gestora['Ativo'].dropna().unique()))
        dados_g = df_gestora[df_gestora['Ativo'] == ativo_g].sort_values(by='Data')

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

        # FUNDOS
        st.subheader("📉 Evolução por Fundo")
        df_fundos = pd.read_parquet(FUNDOS_PARQUET)
        df_fundos['Data'] = pd.to_datetime(df_fundos['Data'], dayfirst=True, errors='coerce')
        df_fundos = df_fundos.dropna(subset=['Data'])
        df_fundos['Exposicao %'] = df_fundos['Exposicao Fundo'] / 100

        fundo_f = st.selectbox("🏦 Fundo:", sorted(df_fundos['Fundo'].dropna().unique()))
        ativo_f = st.selectbox("🔎 Ativo (Fundo):", sorted(df_fundos['Ativo'].dropna().unique()))
        dados_f = df_fundos[(df_fundos['Fundo'] == fundo_f) & (df_fundos['Ativo'] == ativo_f)].sort_values(by='Data')

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
        st.error(f"❌ Erro ao processar os arquivos: {e}")
