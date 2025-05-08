import pandas as pd
import cx_Oracle
import json
import os

def generalize_value(value):
    if isinstance(value, int):
        return (value // 10) * 10
    elif isinstance(value, str):
        return value[0] + '*' * (len(value) - 1)
    return value

def anonymize_data(df, quasi_identifiers, sensitive_attributes, k=3):
    df_anonymized = df.copy()
    mapping_dict = {}

    for column in quasi_identifiers + sensitive_attributes:
        mapping_dict[column] = {}
        df_anonymized[column] = df[column].apply(lambda val: mapping_dict[column].setdefault(val, generalize_value(val)))

    with open("mapeamento.json", "w") as f:
        json.dump(mapping_dict, f, ensure_ascii=False, indent=2)

    return df_anonymized

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
