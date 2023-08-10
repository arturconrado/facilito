from fastapi import FastAPI
from sqlalchemy import create_engine
import pandas as pd

app = FastAPI()

# Conexão com o banco de dados
engine = create_engine('postgresql://user:password@localhost/dbname')

@app.get("/trends/hot_and_cold_numbers")
def hot_and_cold_numbers():
    # Carregar os dados da tabela stats
    data = pd.read_sql('SELECT * FROM stats', engine)

    # Calcular a frequência de cada número
    frequency = data['numbers'].value_counts()

    # Identificar os números quentes e frios
    hot_numbers = frequency.head(5).index.tolist()
    cold_numbers = frequency.tail(5).index.tolist()

    return {"hot_numbers": hot_numbers, "cold_numbers": cold_numbers}
