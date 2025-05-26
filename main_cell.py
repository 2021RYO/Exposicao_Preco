import streamlit as st
import pandas as pd
import os
import plotly.graph_objects as go
import plotly.express as px

# Caminho relativo ao Excel no repositório
EXCEL_PATH = "Evolucao.xlsx"

# Configuração do app
st.set_page_config(page_title="📈 Preços & Exposição", layout="centered")

st.title("📈 Evolução de Preços e Exposição")
st.markdown("Visualize rapidamente o comportamento de ativos com base nos dados do Excel.")

# Verifica se o arquivo existe
if not os.path.exists(EXCEL_PATH):
    st.error(f"❌ O arquivo Excel não foi encontrado: `{EXCEL_PATH}`.")
else:
    try:
        xls = pd.ExcelFile(EXCEL_PATH)
        aba = st.selectbox("📄 Escolha a aba do Excel:", xls.sheet_names)
        df = pd.read_excel(xls, sheet_name=aba)

        # Verifica colunas obrigatórias
        col_preco = 'Preço D0' if 'Preço D0' in df.columns else 'Preço'
        colunas_necessarias = ['Ativo', 'Data', col_preco, 'Quantidade']

        if all(col in df.columns for col in colunas_necessarias):
            df['Data'] = pd.to_datetime(df['Data'], errors='coerce')
            df = df.dropna(subset=['Data'])

            # Quantidade como percentual
            df['Quantidade %'] = df['Quantidade'] / 100

            # Ativo selecionado
            ativos = df['Ativo'].dropna().unique()
            ativo = st.selectbox("📌 Selecione o ativo:", sorted(ativos))
            df_ativo = df[df['Ativo'] == ativo].sort_values(by='Data')

            # Gráfico principal
            st.subheader(f"📊 Gráfico: {ativo}")
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df_ativo['Data'], y=df_ativo[col_preco], name='Preço', mode='lines'))
            fig.add_trace(go.Scatter(
                x=df_ativo['Data'], y=df_ativo['Quantidade %'],
                name='Quantidade (%)', mode='lines', yaxis='y2'
            ))

            fig.update_layout(
                xaxis_title='Data',
                yaxis=dict(title='Preço'),
                yaxis2=dict(title='Quantidade (%)', overlaying='y', side='right', tickformat=".2%"),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )

            st.plotly_chart(fig, use_container_width=True)

        else:
            st.warning("❗ O Excel precisa conter as colunas: 'Ativo', 'Data', 'Preço D0' ou 'Preço', e 'Quantidade'.")

        # Dados brutos (colapsável)
        with st.expander("📂 Ver dados brutos"):
            df['Quantidade %'] = df['Quantidade %'].map(lambda x: f"{x:.2%}")
            st.dataframe(df, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Erro ao carregar os dados: {e}")
