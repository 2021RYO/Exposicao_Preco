import streamlit as st
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go

# Caminho relativo ao arquivo Excel
EXCEL_PATH = "Evolucao.xlsx"

st.set_page_config(
    page_title="Evolução de Preços - Exposição",
    layout="wide",
)

st.title("📊 Visualizador de Evolução de Preços - Exposição")
st.markdown("Este aplicativo permite visualizar a evolução de preços e exposição de ativos a partir de um arquivo Excel.")

# Verifica se o arquivo existe
if not os.path.exists(EXCEL_PATH):
    st.error(f"❌ O arquivo Excel não foi encontrado no caminho: `{EXCEL_PATH}`.")
else:
    try:
        xls = pd.ExcelFile(EXCEL_PATH)
        aba = st.selectbox("Selecione a aba para visualização:", xls.sheet_names)
        df = pd.read_excel(xls, sheet_name=aba)

        # Converte Quantidade para percentual
        df['Quantidade %'] = df['Quantidade'] / 100

        # Gráfico
        st.subheader("📊 Visualização Gráfica")

        col_preco = 'Preço D0' if 'Preço D0' in df.columns else 'Preço'
        colunas_necessarias = ['Ativo', 'Data', col_preco, 'Quantidade']

        if all(col in df.columns for col in colunas_necessarias):
            df['Data'] = pd.to_datetime(df['Data'], errors='coerce')
            df = df.dropna(subset=['Data'])

            if df['Data'].nunique() > 1:
                ativos = df['Ativo'].dropna().unique()
                ativo_selecionado = st.selectbox("Selecione um ativo:", sorted(ativos))
                df_ativo = df[df['Ativo'] == ativo_selecionado].sort_values(by='Data')

                fig = go.Figure()
                fig.add_trace(go.Scatter(x=df_ativo['Data'], y=df_ativo[col_preco], mode='lines', name='Preço'))
                fig.add_trace(go.Scatter(
                    x=df_ativo['Data'],
                    y=df_ativo['Quantidade %'],
                    mode='lines',
                    name='Quantidade (%)',
                    yaxis='y2'
                ))

                fig.update_layout(
                    title=f"Evolução de Preço e Quantidade (%) - {ativo_selecionado}",
                    xaxis=dict(title='Data'),
                    yaxis=dict(title='Preço'),
                    yaxis2=dict(
                        title='Quantidade (%)',
                        overlaying='y',
                        side='right',
                        tickformat=".2%"
                    ),
                    legend=dict(title='Variável')
                )

                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("⚠️ Apenas uma data disponível. Exibindo gráficos de barras comparativos.")

                fig_preco = px.bar(df, x='Ativo', y=col_preco, title="Preço por Ativo", labels={col_preco: 'Preço (R$)'})
                fig_preco.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig_preco, use_container_width=True)

                fig_quantidade = px.bar(
                    df,
                    x='Ativo',
                    y='Quantidade %',
                    title="Quantidade (%) por Ativo",
                    labels={'Quantidade %': 'Quantidade (%)'}
                )
                fig_quantidade.update_layout(
                    xaxis_tickangle=-45,
                    yaxis_tickformat=".2%"
                )
                st.plotly_chart(fig_quantidade, use_container_width=True)
        else:
            st.warning(f"O DataFrame precisa conter as colunas: {colunas_necessarias}")

        # Dados brutos
        st.subheader("📄 Dados brutos")
        st.dataframe(df, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Erro ao processar o arquivo Excel: {e}")
