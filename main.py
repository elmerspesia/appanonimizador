import streamlit as st
from PIL import Image
import importlib.util
import os

# Logo
logo = Image.open("spesia_logo.png")
st.set_page_config(page_title="Spesia - Anonimizador de Dados", page_icon=logo, layout="centered")

# Cabeçalho
col1, col2 = st.columns([1, 4])
with col1:
    st.image(logo, width=80)
with col2:
    st.markdown("<h1 style='margin-top: 10px;'>Spesia - Anonimizador de Dados</h1>", unsafe_allow_html=True)

# Autenticação
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("### Login de Acesso")
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if username == "spesia123" and password == "spesia123":
            st.success("Login bem-sucedido!")
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Usuário ou senha incorretos.")
else:
    st.markdown("## Bem-vindo ao Anonimizador!")
    st.markdown("Carregando funcionalidades...")

    # 🔄 Carregando anonimizador_view dinamicamente com importlib
    spec = importlib.util.spec_from_file_location("anonimizador_view", os.path.join(os.path.dirname(__file__), "anonimizador_view.py"))
    anon_view = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(anon_view)
