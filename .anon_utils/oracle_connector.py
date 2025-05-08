import pandas as pd
import cx_Oracle

def test_oracle_connection(host, port, service_name, user, password):
    dsn = cx_Oracle.makedsn(host, port, service_name=service_name)
    try:
        with cx_Oracle.connect(user=user, password=password, dsn=dsn) as connection:
            return True
    except Exception:
        return False

def load_data_from_oracle(host, port, service_name, user, password, query):
    dsn = cx_Oracle.makedsn(host, port, service_name=service_name)
    with cx_Oracle.connect(user=user, password=password, dsn=dsn) as connection:
        df = pd.read_sql(query, con=connection)
    return df
