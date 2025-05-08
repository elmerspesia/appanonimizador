import pandas as pd
import cx_Oracle
import os
import json
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import constant_time
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import hmac
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# === GERENCIAMENTO DE CHAVE ===
KEY_PATH = "key.key"

def generate_key():
    key = Fernet.generate_key()
    with open(KEY_PATH, "wb") as key_file:
        key_file.write(key)

def load_key():
    if not os.path.exists(KEY_PATH):
        generate_key()
    with open(KEY_PATH, "rb") as key_file:
        return key_file.read()

# === CRIPTOGRAFIA ===
def encrypt_value(value, fernet):
    if pd.isna(value):
        return value
    value_str = str(value)
    token = fernet.encrypt(value_str.encode())
    return base64.urlsafe_b64encode(token).decode()

def decrypt_value(value, fernet):
    if pd.isna(value):
        return value
    try:
        token = base64.urlsafe_b64decode(value.encode())
        return fernet.decrypt(token).decode()
    except:
        return value  # Caso o valor já não esteja criptografado

# === ANONIMIZAÇÃO COM CRIPTOGRAFIA ===
def anonymize_data(df, quasi_identifiers, sensitive_attributes):
    df_anonymized = df.copy()
    fernet = Fernet(load_key())

    mapping_dict = {}

    for column in quasi_identifiers + sensitive_attributes:
        mapping_dict[column] = {}
        df_anonymized[column] = df[column].apply(
            lambda val: mapping_dict[column].setdefault(val, encrypt_value(val, fernet))
        )

    with open("mapeamento.json", "w") as f:
        json.dump(mapping_dict, f, ensure_ascii=False, indent=2)

    return df_anonymized

def deanonymize_data(df_anonymized):
    fernet = Fernet(load_key())
    df_original = df_anonymized.copy()
    for column in df_original.columns:
        df_original[column] = df_original[column].apply(lambda val: decrypt_value(val, fernet))
    return df_original

# === ORACLE ===
def test_oracle_connection(host, port, service_name, user, password):
    dsn = cx_Oracle.makedsn(host, port, service_name=service_name)
    try:
        with cx_Oracle.connect(user=user, password=password, dsn=dsn):
            return True
    except:
        return False

def load_data_from_oracle(host, port, service_name, user, password, query):
    dsn = cx_Oracle.makedsn(host, port, service_name=service_name)
    with cx_Oracle.connect(user=user, password=password, dsn=dsn) as connection:
        return pd.read_sql(query, con=connection)

# === ARQUIVOS ===
def load_uploaded_file(uploaded_file):
    ext = os.path.splitext(uploaded_file.name)[1].lower()
    if ext == ".csv":
        return pd.read_csv(uploaded_file)
    elif ext == ".xlsx":
        return pd.read_excel(uploaded_file)
    elif ext == ".txt":
        return pd.read_csv(uploaded_file, delimiter="\t")
    else:
        raise ValueError("Formato não suportado.")

def export_dataframe(df, buffer, fmt):
    if fmt == "CSV":
        df.to_csv(buffer, index=False)
    elif fmt == "XLSX":
        df.to_excel(buffer, index=False)
    elif fmt == "TXT":
        df.to_csv(buffer, sep="\t", index=False)
    else:
        raise ValueError("Formato inválido.")
