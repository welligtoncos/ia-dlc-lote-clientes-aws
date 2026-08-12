LIMITE_UPLOAD_BYTES = 5 * 1024 * 1024
TAREFA_INGERIR = "ingerir_clientes"


def validar_nome_csv(nome_arquivo: str) -> bool:
    return bool(nome_arquivo) and nome_arquivo.lower().endswith(".csv")
