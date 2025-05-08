import pandas as pd
import os
import json

# Generalização simples
def generalize_value(value):
    if isinstance(value, int):
        return (value // 10) * 10
    elif isinstance(value, str):
        return value[0] + '*' * (len(value) - 1)
    else:
        return value

# K-Anonimato
def k_anonymity(df, quasi_identifiers, k):
    df_anonymized = df.copy()
    for qi in quasi_identifiers:
        df_anonymized[qi] = df_anonymized[qi].apply(generalize_value)
    grouped = df_anonymized.groupby(quasi_identifiers)
    valid_groups = [group for group in grouped.groups if len(grouped.groups[group]) >= k]
    df_result = pd.concat([grouped.get_group(group) for group in valid_groups])
    return df_result

# Anonimização com armazenamento de mapeamento
def anonymize_data(df, quasi_identifiers, sensitive_attributes, k=3):
    df_anonymized = df.copy()
    mapping_dict = {}

    for column in quasi_identifiers + sensitive_attributes:
        mapping_dict[column] = {}
        anon_col = []
        for val in df[column]:
            if val not in mapping_dict[column]:
                mapping_dict[column][val] = generalize_value(val)
            anon_col.append(mapping_dict[column][val])
        df_anonymized[column] = anon_col

    with open("mapeamento.json", "w") as f:
        json.dump(mapping_dict, f, ensure_ascii=False, indent=4)

    return df_anonymized

# Desanonimização com base no dicionário
def deanonymize_data(df_anonymized, mapping_dict):
    df_original = df_anonymized.copy()
    for column, mapping in mapping_dict.items():
        reverse_mapping = {v: k for k, v in mapping.items()}
        df_original[column] = df_original[column].map(reverse_mapping).fillna(df_original[column])
    return df_original

# Salvamento de dados
def save_data(df, output_path):
    _, ext = os.path.splitext(output_path)
    if ext == ".csv":
        df.to_csv(output_path, index=False)
    elif ext == ".xlsx":
        df.to_excel(output_path, index=False)
    elif ext == ".txt":
        df.to_csv(output_path, sep="\t", index=False)
    else:
        raise ValueError("Formato não suportado.")
