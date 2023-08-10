import logging

from fastapi import FastAPI
from sqlalchemy import create_engine, text
import pandas as pd
import utils

stats = FastAPI()

DATABASE_URL = "postgresql://artur:Aqwe123!@localhost:5432/lotofacil"
engine = create_engine(DATABASE_URL)

# Funções utilitárias
is_prime = utils.is_prime
is_fibonacci = utils.is_fibonacci


# Função para carregar dados
def load_data_from_db():
    try:
        return pd.read_sql('SELECT * FROM resultados', engine)
    except Exception as e:
        print("Erro ao executar a consulta SQL:", e)
        return pd.DataFrame()


# Função para calcular estatísticas
def calculate_statistics(data):
    logging.info("Calculando estatísticas...")
    # Verificando se o DataFrame está vazio
    if data.empty:
        print("DataFrame está vazio. Verifique a tabela 'resultados' no banco de dados.")
        return {}

    # Cálculo das estatísticas
    data['fibonacci_count'] = data.iloc[:, 2:-1].apply(lambda row: sum(is_fibonacci(n) for n in row), axis=1)
    data['even_count'] = data.iloc[:, 2:-1].apply(lambda row: sum(n % 2 == 0 for n in row), axis=1)
    data['odd_count'] = data.iloc[:, 2:-1].apply(lambda row: sum(n % 2 == 1 for n in row), axis=1)
    data['prime_count'] = data.iloc[:, 2:-1].apply(lambda row: sum(is_prime(n) for n in row), axis=1)
    data['Soma'] = data.iloc[:, 2:-1].sum(axis=1)

    # Resultado das estatísticas
    result = {
        'average_sum': data['Soma'].mean(),
        'max_sum': data['Soma'].max(),
        'min_sum': data['Soma'].min(),
        'last_sum': data['Soma'].iloc[-1],
        'sum_std': data['Soma'].std(),
        'max_odd_count': data['odd_count'].max(),
        'max_even_count': data['even_count'].max(),
        'max_prime_count': data['prime_count'].max(),
        'max_fibonacci_count': data['fibonacci_count'].max(),
        'last_odd_count': data['odd_count'].iloc[-1],
        'last_even_count': data['even_count'].iloc[-1],
        'last_prime_count': data['prime_count'].iloc[-1],
        'last_fibonacci_count': data['fibonacci_count'].iloc[-1],
        'fibonacci_count_std': data['fibonacci_count'].std(),
        'prime_count_std': data['prime_count'].std(),
        'even_count_std': data['even_count'].std(),
        'odd_count_std': data['odd_count'].std(),
        'average_odd_count': data['odd_count'].mean(),
        'average_even_count': data['even_count'].mean(),
        'average_prime_count': data['prime_count'].mean(),
        'average_fibonacci_count': data['fibonacci_count'].mean(),
        'min_odd_count': data['odd_count'].min(),
        'min_even_count': data['even_count'].min(),
        'min_prime_count': data['prime_count'].min(),
        'min_fibonacci_count': data['fibonacci_count'].min(),
        'last_bola1': data['bola 1'].iloc[-1],
        'last_bola2': data['bola 2'].iloc[-1],
        'last_bola3': data['bola 3'].iloc[-1],
        'last_bola13': data['bola 13'].iloc[-1],
        'last_bola14': data['bola 14'].iloc[-1],
        'last_bola15': data['bola 15'].iloc[-1],
        'average_bola1': data['bola 1'].mean(),
        'average_bola2': data['bola 2'].mean(),
        'average_bola3': data['bola 3'].mean(),
        'average_bola13': data['bola 13'].mean(),
        'average_bola14': data['bola 14'].mean(),
        'average_bola15': data['bola 15'].mean(),
        'max_bola1': data['bola 1'].max(),
        'max_bola2': data['bola 2'].max(),
        'max_bola3': data['bola 3'].max(),
        'max_bola13': data['bola 13'].max(),
        'max_bola14': data['bola 14'].max(),
        'max_bola15': data['bola 15'].max(),
        'min_bola13': data['bola 13'].min(),
        'min_bola14': data['bola 14'].min(),
        'min_bola15': data['bola 15'].min(),
        'bola13_std': data['bola 13'].std(),
        'bola14_std': data['bola 14'].std(),
        'bola15_std': data['bola 15'].std(),

    }

    # Convertendo os valores para tipos nativos do Python
    result = {key: value.item() if hasattr(value, 'item') else value for key, value in result.items()}

    return result


# Função para inserir estatísticas no banco de dados
def insert_statistics(result):
    logging.info("Inserindo estatísticas no banco de dados...")
    fields = ', '.join(result.keys())
    values = ', '.join([f':{key}' for key in result.keys()])
    query_text = f"""
        INSERT INTO stats (
            {fields}
        ) VALUES (
            {values}
        )
    """
    query = text(query_text)
    logging.info("Query de inserção de estatísticas:")

    with engine.connect() as conn:
        conn.execute(query, result)
        conn.commit()


# Rota de inicialização para carregar dados e calcular estatísticas
@stats.on_event("startup")
@stats.get("/stats")
def load_and_calculate():
    logging.info("Iniciando o cálculo das estatísticas...")
    data = load_data_from_db()
    result = calculate_statistics(data)
    insert_statistics(result)
    logging.info("Estatísticas calculadas e inseridas no banco de dados.")

    return result
