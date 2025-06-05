import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
import io

# Arquivos parquet
GESTORA_PARQUET = "gestora.parquet"
FUNDOS_PARQUET = "fundos.parquet"

st.set_page_config(page_title="📈 Preços - Parquet", layout="centered")
st.title("Relatório - Evolução de Preços e Exposição")

# Verificação dos arquivos
if not os.path.exists(GESTORA_PARQUET) or not os.path.exists(FUNDOS_PARQUET):
    st.error("❌ Arquivos .parquet não encontrados. Envie 'gestora.parquet' e 'fundos.parquet'.")
else:
    try:
        # ===================== GESTORA =====================
        st.subheader("📈 Evolução por Gestora")
        df_gestora = pd.read_parquet(GESTORA_PARQUET)
        df_gestora['Data'] = pd.to_datetime(df_gestora['Data'], dayfirst=True, errors='coerce')
        df_gestora = df_gestora.dropna(subset=['Data'])
        df_gestora['Exposicao %'] = df_gestora['Exposicao Gestora'] / 100

        ativo_g = st.selectbox("🔎 Ativo (Gestora):", sorted(df_gestora['Ativo'].dropna().unique()))
        dados_g = df_gestora[df_gestora['Ativo'] == ativo_g].sort_values(by='Data')

        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=dados_g['Data'], y=dados_g['Preco'], mode='lines', name='Preço',
                                  line=dict(color='#1f77b4')))  # Azul escuro
        fig1.add_trace(go.Scatter(x=dados_g['Data'], y=dados_g['Exposicao %'], mode='lines',
                                  name='Exposição (%)', yaxis='y2', line=dict(color='#ff7f0e')))  # Laranja
        fig1.update_layout(
            xaxis=dict(title='Data'),
            yaxis=dict(title='Preço'),
            yaxis2=dict(title='Exposição (%)', overlaying='y', side='right', tickformat=".2%"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig1, use_container_width=True)

        # Botão para baixar Excel da gestora
        buffer_g = io.BytesIO()
        dados_g.to_excel(buffer_g, index=False, engine='openpyxl')
        buffer_g.seek(0)
        st.download_button("📥 Baixar dados (Gestora)", data=buffer_g,
                           file_name=f"dados_gestora_{ativo_g}.xlsx",
                           mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

        # ===================== FUNDOS =====================
        st.subheader("📉 Evolução por Fundo")
        df_fundos = pd.read_parquet(FUNDOS_PARQUET)
        df_fundos['Data'] = pd.to_datetime(df_fundos['Data'], dayfirst=True, errors='coerce')
        df_fundos = df_fundos.dropna(subset=['Data'])
        df_fundos['Exposicao %'] = df_fundos['Exposicao Fundo'] / 100

        fundo_f = st.selectbox("🏦 Fundo:", sorted(df_fundos['Fundo'].dropna().unique()))
        ativos_disponiveis = df_fundos[df_fundos['Fundo'] == fundo_f]['Ativo'].dropna().unique()
        ativo_f = st.selectbox("🔎 Ativo (Fundo):", sorted(ativos_disponiveis))

        dados_f = df_fundos[(df_fundos['Fundo'] == fundo_f) & (df_fundos['Ativo'] == ativo_f)].sort_values(by='Data')

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=dados_f['Data'], y=dados_f['Preco'], mode='lines', name='Preço',
                                  line=dict(color='#1f77b4')))  # Azul escuro
        fig2.add_trace(go.Scatter(x=dados_f['Data'], y=dados_f['Exposicao %'], mode='lines',
                                  name='Exposição (%)', yaxis='y2', line=dict(color='#ff7f0e')))  # Laranja
        fig2.update_layout(
            xaxis=dict(title='Data'),
            yaxis=dict(title='Preço'),
            yaxis2=dict(title='Exposição (%)', overlaying='y', side='right', tickformat=".2%"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig2, use_container_width=True)

        # Botão para baixar Excel do fundo
        buffer_f = io.BytesIO()
        dados_f.to_excel(buffer_f, index=False, engine='openpyxl')
        buffer_f.seek(0)
        st.download_button("📥 Baixar dados (Fundo)", data=buffer_f,
                           file_name=f"dados_fundo_{fundo_f}_{ativo_f}.xlsx",
                           mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    except Exception as e:
        st.error(f"❌ Erro ao processar os arquivos: {e}")
