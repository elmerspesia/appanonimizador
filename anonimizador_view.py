import streamlit as st
import pandas as pd
from io import BytesIO
import utils

st.sidebar.title("Menu")
st.sidebar.markdown("## Anonimizador")

st.title("📊 Anonimizador de Dados")

input_type = st.selectbox("Selecione o tipo de entrada de dados", ["Oracle", "CSV", "TXT", "XLSX"])

df = None

if input_type == "Oracle":
    st.markdown("### Configuração Oracle")
    host = st.text_input("Host")
    port = st.text_input("Porta", value="1521")
    service_name = st.text_input("Service Name")
    user = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")
    table_name = st.text_input("Nome da Tabela")

    if st.button("Testar Conexão"):
        with st.spinner("Testando conexão..."):
            result = utils.test_oracle_connection(host, port, service_name, user, password)
            st.success("Conexão bem-sucedida!") if result else st.error("Erro na conexão.")

    if st.button("Carregar Dados") and table_name:
        query = f"SELECT * FROM {table_name}"
        with st.spinner(f"Carregando dados da tabela `{table_name}`..."):
            try:
                df = utils.load_data_from_oracle(host, port, service_name, user, password, query)
                st.success("Dados carregados com sucesso.")
            except Exception as e:
                st.error(f"Erro ao carregar dados: {e}")
else:
    uploaded_file = st.file_uploader("Faça upload do arquivo de entrada", type=["csv", "txt", "xlsx"])
    if uploaded_file:
        df = utils.load_uploaded_file(uploaded_file)

if df is not None:
    st.dataframe(df)
    selected_columns = st.multiselect("Colunas Quasi-Identificadoras", df.columns.tolist())
    sensitive_columns = st.multiselect("Colunas Sensíveis", df.columns.tolist())

    if st.button("Anonimizar"):
        with st.spinner("Anonimizando dados..."):
            anon_df = utils.anonymize_data(df, selected_columns, sensitive_columns)
            st.success("Anonimização concluída.")
            st.dataframe(anon_df)

            buffer = BytesIO()
            export_format = st.selectbox("Formato de exportação", ["CSV", "XLSX", "TXT"])
            file_name = st.text_input("Nome do arquivo de saída", value="dados_anonimizados")

            utils.export_dataframe(anon_df, buffer, export_format)

            st.download_button("📥 Baixar arquivo", buffer.getvalue(), f"{file_name}.{export_format.lower()}")
