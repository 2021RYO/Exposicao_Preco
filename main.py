

import streamlit as st
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go

# Caminho do arquivo Excel
EXCEL_PATH = r"Z:\Risco\Workspace\VictorRoure\Evolucao_Precos_Exposicao\Evolucao.xlsx"

st.set_page_config(
    page_title="Evolução de Preços - Exposição",
    layout="wide",
)

st.title("📊 Visualizador de Evolução de Preços - Exposição")
st.markdown("Este aplicativo permite explorar os dados de preços e exposição de forma interativa a partir de um arquivo Excel.")

# Verifica se o arquivo existe
if not os.path.exists(EXCEL_PATH):
    st.error(f"❌ O arquivo Excel não foi encontrado no caminho: `{EXCEL_PATH}`.")
else:
    try:
        xls = pd.ExcelFile(EXCEL_PATH)
        aba = st.selectbox("Selecione a aba para visualização:", xls.sheet_names)
        df = pd.read_excel(xls, sheet_name=aba)

        st.subheader("📄 Dados brutos")
        st.dataframe(df, use_container_width=True)

        # Filtros interativos
        st.subheader("🔍 Filtros interativos")
        filtro_colunas = st.multiselect("Selecione colunas para aplicar filtros:", df.columns)
        df_filtrado = df.copy()
        for col in filtro_colunas:
            valores_unicos = df[col].dropna().unique()
            if len(valores_unicos) < 30:
                selecao = st.multiselect(f"Filtrar valores para '{col}':", sorted(valores_unicos))
                if selecao:
                    df_filtrado = df_filtrado[df_filtrado[col].isin(selecao)]

        st.subheader("📈 Resultado com filtros aplicados")
        st.dataframe(df_filtrado, use_container_width=True)

        # Gráfico
        st.subheader("📊 Visualização Gráfica")

        col_preco = 'Preço D0' if 'Preço D0' in df_filtrado.columns else 'Preço'
        colunas_necessarias = ['Ativo', 'Data', col_preco, 'Quantidade']

        if all(col in df_filtrado.columns for col in colunas_necessarias):
            df_filtrado['Data'] = pd.to_datetime(df_filtrado['Data'], errors='coerce')
            df_filtrado = df_filtrado.dropna(subset=['Data'])

            if df_filtrado['Data'].nunique() > 1:
                # Gráfico de linha (evolução temporal)
                ativos = df_filtrado['Ativo'].dropna().unique()
                ativo_selecionado = st.selectbox("Selecione um ativo:", sorted(ativos))
                df_ativo = df_filtrado[df_filtrado['Ativo'] == ativo_selecionado].sort_values(by='Data')

                fig = go.Figure()
                fig.add_trace(go.Scatter(x=df_ativo['Data'], y=df_ativo[col_preco], mode='lines', name='Preço'))
                fig.add_trace(go.Scatter(x=df_ativo['Data'], y=df_ativo['Quantidade'], mode='lines', name='Quantidade', yaxis='y2'))

                fig.update_layout(
                    title=f"Evolução de Preço e Quantidade - {ativo_selecionado}",
                    xaxis=dict(title='Data'),
                    yaxis=dict(title='Preço'),
                    yaxis2=dict(title='Quantidade', overlaying='y', side='right'),
                    legend=dict(title='Variável')
                )

                st.plotly_chart(fig, use_container_width=True)
            else:
                # Gráficos de barras (preço e quantidade por ativo)
                st.info("⚠️ Apenas uma data disponível. Exibindo gráficos de barras comparativos.")

                fig_preco = px.bar(df_filtrado, x='Ativo', y=col_preco, title="Preço por Ativo", labels={col_preco: 'Preço (R$)'})
                fig_preco.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig_preco, use_container_width=True)

                fig_quantidade = px.bar(df_filtrado, x='Ativo', y='Quantidade', title="Quantidade por Ativo", labels={'Quantidade': 'Quantidade'})
                fig_quantidade.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig_quantidade, use_container_width=True)
        else:
            st.warning(f"O DataFrame precisa conter as colunas: {colunas_necessarias}")

    except Exception as e:
        st.error(f"❌ Erro ao processar o arquivo Excel: {e}")


#python -m streamlit run Z:\Risco\Workspace\VictorRoure\Evolucao_Precos_Exposicao\main.py
