# Spesia - AppAnonimizador

Aplicativo em Streamlit para anonimização e desanonimização de dados com suporte a Oracle, CSV, TXT e XLSX.

## 🔐 Funcionalidades

- Tela de login com autenticação embutida.
- Upload ou conexão com banco Oracle.
- Anonimização baseada em k-anonimato, com generalização de dados.
- Download de dados anonimizados em CSV, XLSX ou TXT.
- Reversão da anonimização com base em arquivo de mapeamento JSON.

## 📦 Requisitos

- Python 3.8+
- Oracle Instant Client (para uso do `cx_Oracle`)

Instalação dos pacotes:

```bash
pip install -r requirements.txt
