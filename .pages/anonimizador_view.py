import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import pandas as pd
from io import BytesIO

from anon_utils.anonymizer import anonymize_data, save_data
from anon_utils.oracle_connector import test_oracle_connection, load_data_from_oracle


import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

st.set_page_config(page_title="Anonimizador", layout="wide")

st.sidebar.title("Menu")
st.sidebar.markdown("## Anonimizador")

st.title("📊 Anonimizador de Dados")

input_type = st.selectbox("Selecione o tipo de entrada de dados", ["Oracle", "CSV", "TXT", "XLSX"])

df = None
mapping_dict = {}

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
            result = test_oracle_connection(host, port, service_name, user, password)
            st.success("Conexão bem-sucedida!") if result else st.error("Erro na conexão.")

    if st.button("Carregar Dados") and table_name:
        query = f"SELECT * FROM {table_name}"
        with st.spinner(f"Carregando dados da tabela `{table_name}`..."):
            try:
                df = load_data_from_oracle(host, port, service_name, user, password, query)
                st.success("Dados carregados com sucesso.")
            except Exception as e:
                st.error(f"Erro ao carregar dados: {e}")

else:
    uploaded_file = st.file_uploader("Faça upload do arquivo de entrada", type=["csv", "txt", "xlsx"])
    if uploaded_file:
        _, ext = os.path.splitext(uploaded_file.name)
        if ext == ".csv":
            df = pd.read_csv(uploaded_file)
        elif ext == ".txt":
            df = pd.read_csv(uploaded_file, delimiter="\t")
        elif ext == ".xlsx":
            df = pd.read_excel(uploaded_file)

if df is not None:
    st.dataframe(df)
    st.markdown("### Selecione colunas a anonimizar")
    selected_columns = st.multiselect("Colunas Quasi-Identificadoras", df.columns.tolist())
    sensitive_columns = st.multiselect("Colunas Sensíveis", df.columns.tolist())

    if st.button("Anonimizar"):
        with st.spinner("Anonimizando dados..."):
            anon_df = anonymize_data(df, selected_columns, sensitive_columns)
            st.success("Anonimização concluída.")
            st.dataframe(anon_df)

            buffer = BytesIO()
            export_format = st.selectbox("Formato de exportação", ["CSV", "XLSX", "TXT"])
            file_name = st.text_input("Nome do arquivo de saída", value="dados_anonimizados")

            if export_format == "CSV":
                anon_df.to_csv(buffer, index=False)
                st.download_button("📥 Baixar CSV", buffer.getvalue(), f"{file_name}.csv", "text/csv")
            elif export_format == "XLSX":
                anon_df.to_excel(buffer, index=False)
                st.download_button("📥 Baixar XLSX", buffer.getvalue(), f"{file_name}.xlsx", "application/vnd.ms-excel")
            elif export_format == "TXT":
                anon_df.to_csv(buffer, sep="\t", index=False)
                st.download_button("📥 Baixar TXT", buffer.getvalue(), f"{file_name}.txt", "text/plain")
