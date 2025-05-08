import streamlit as st
import pandas as pd
import json
from io import BytesIO
from anon_utils.anonymizer import deanonymize_data

st.set_page_config(page_title="De-Anonimizador", layout="wide")

st.sidebar.title("Menu")
st.sidebar.markdown("## De-Anonimizador")

st.title("🔓 De-Anonimizador de Dados")

uploaded_data = st.file_uploader("Selecione o arquivo anonimizado", type=["csv", "xlsx", "txt"])
uploaded_map = st.file_uploader("Selecione o arquivo de mapeamento (JSON)", type=["json"])

df = None

if uploaded_data:
    _, ext = uploaded_data.name.split(".")
    if ext == "csv":
        df = pd.read_csv(uploaded_data)
    elif ext == "xlsx":
        df = pd.read_excel(uploaded_data)
    elif ext == "txt":
        df = pd.read_csv(uploaded_data, sep="\t")

if df is not None and uploaded_map:
    try:
        mapping_dict = json.load(uploaded_map)
        st.dataframe(df)
        if st.button("Desanonimizar"):
            with st.spinner("Revertendo anonimização..."):
                recovered_df = deanonymize_data(df, mapping_dict)
                st.success("Dados desanonimizados com sucesso.")
                st.dataframe(recovered_df)

                buffer = BytesIO()
                export_format = st.selectbox("Formato para download", ["CSV", "XLSX", "TXT"])
                file_name = st.text_input("Nome do arquivo de saída", value="dados_revertidos")

                if export_format == "CSV":
                    recovered_df.to_csv(buffer, index=False)
                    st.download_button("📥 Baixar CSV", buffer.getvalue(), f"{file_name}.csv", "text/csv")
                elif export_format == "XLSX":
                    recovered_df.to_excel(buffer, index=False)
                    st.download_button("📥 Baixar XLSX", buffer.getvalue(), f"{file_name}.xlsx", "application/vnd.ms-excel")
                elif export_format == "TXT":
                    recovered_df.to_csv(buffer, sep="\t", index=False)
                    st.download_button("📥 Baixar TXT", buffer.getvalue(), f"{file_name}.txt", "text/plain")
    except Exception as e:
        st.error(f"Erro ao carregar o mapeamento: {e}")
