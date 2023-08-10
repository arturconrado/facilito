from fastapi import FastAPI
from sqlalchemy import create_engine, text
import pandas as pd
import utils

stats = FastAPI()

DATABASE_URL = "postgresql://artur:Aqwe123!@localhost:5432/lotofacil"
engine = create_engine(DATABASE_URL)
is_prime = utils.is_prime
is_fibonacci = utils.is_fibonacci


@stats.on_event("startup")
def load_data():
    global data

    # Conexão com o banco de dados
    try:
        engine = create_engine(DATABASE_URL)
        print("Conexão com o banco de dados estabelecida.")
    except Exception as e:
        print("Erro ao conectar ao banco de dados:", e)
        return

    # Executando a consulta SQL
    try:
        data = pd.read_sql('SELECT * FROM resultados', engine)
        print("Consulta SQL executada com sucesso. Número de linhas:", len(data))
    except Exception as e:
        print("Erro ao executar a consulta SQL:", e)
        return

    # Verificando se o DataFrame está vazio
    if data.empty:
        print("DataFrame está vazio. Verifique a tabela 'resultados' no banco de dados.")
        return

    # Cálculo da contagem de números primos
    try:
        prime_counts = data.iloc[:, 2:-1].apply(lambda row: sum(is_prime(n) for n in row), axis=1)
        print("Prime counts calculado com sucesso.")
        data['prime_count'] = prime_counts
    except Exception as e:
        print("Erro ao calcular a contagem de números primos:", e)
        return

    data = pd.read_sql('SELECT * FROM resultados', engine)
    print(data.columns)
    data['fibonacci_count'] = data.iloc[:, 2:-1].apply(lambda row: sum(is_fibonacci(n) for n in row), axis=1)
    data['even_count'] = data.iloc[:, 2:-1].apply(lambda row: sum(n % 2 == 0 for n in row), axis=1)
    data['odd_count'] = data.iloc[:, 2:-1].apply(lambda row: sum(n % 2 == 1 for n in row), axis=1)
    prime_counts = data.iloc[:, 2:-1].apply(lambda row: sum(is_prime(n) for n in row), axis=1)
    print("Prime counts:", prime_counts)
    data['prime_count'] = prime_counts


@stats.get("/stats")
def get_stats():
    print("Iniciando o carregamento dos dados...")
    load_data()
    mean_sum = data['Soma'].mean().item()
    max_sum = data['Soma'].max().item()
    min_sum = data['Soma'].min().item()
    average_even_numbers = data['even_count'].mean().item()
    average_odd_numbers = data['odd_count'].mean().item()
    average_prime_numbers = data['prime_count'].mean().item()
    average_fibonacci_numbers = data['fibonacci_count'].mean().item()
    last_sum = data['Soma'].iloc[-1].item()
    max_even_count = data['even_count'].max().item()
    max_odd_numbers = data['odd_count'].max().item()
    max_prime_count = data['prime_count'].max().item()
    max_fibonacci_count = data['fibonacci_count'].max().item()
    std_dev_sum = data['Soma'].std().item()

    # Resultado das estatísticas
    result = {
        "average_sum": mean_sum,
        "max_sum": max_sum,
        "min_sum": min_sum,
        "std_dev_sum": std_dev_sum,
        "last_sum": last_sum,
        "average_even_numbers": average_even_numbers,
        "average_odd_numbers": average_odd_numbers,
        "average_prime_numbers": average_prime_numbers,
        "max_even_count": max_even_count,
        "max_odd_numbers": max_odd_numbers,
        "max_prime_count": max_prime_count,
        "average_fibonacci_numbers": average_fibonacci_numbers,
        "max_fibonacci_count": max_fibonacci_count,
    }

    with engine.connect() as conn:
        query = text("""
            INSERT INTO stats (
                average_sum, max_sum, min_sum, std_dev_sum, last_sum,
                average_even_numbers, average_odd_numbers, average_prime_numbers,
                max_even_count, max_odd_numbers, max_prime_count,
                average_fibonacci_numbers, max_fibonacci_count
            ) VALUES (
                :average_sum, :max_sum, :min_sum, :std_dev_sum, :last_sum,
                :average_even_numbers, :average_odd_numbers, :average_prime_numbers,
                :max_even_count, :max_odd_numbers, :max_prime_count,
                :average_fibonacci_numbers, :max_fibonacci_count
            )
            """)
        conn.execute(query, result)
        conn.commit()

    return result
