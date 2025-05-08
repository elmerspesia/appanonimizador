import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


import streamlit as st
from PIL import Image

# Logo
logo = Image.open("spesia_logo.png")

# Configuração da página
st.set_page_config(
    page_title="Spesia - Anonimizador de Dados",
    page_icon=logo,
    layout="centered"
)

# Cabeçalho com logo
col1, col2 = st.columns([1, 4])
with col1:
    st.image(logo, width=80)
with col2:
    st.markdown("<h1 style='margin-top: 10px;'>Spesia - Anonimizador de Dados</h1>", unsafe_allow_html=True)

# Controle de sessão
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Login
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

    import anonimizador_view
