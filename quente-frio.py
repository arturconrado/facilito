from fastapi import FastAPI
from sqlalchemy import create_engine
import pandas as pd
from statsmodels.tsa.arima_model import ARIMA


quente_frio = FastAPI()

# Conexão com o banco de dados
engine = create_engine('postgresql://artur:Aqwe123!@localhost/lotofacil')


@quente_frio.on_event("startup")
@quente_frio.get("/trends/hot_and_cold_numbers")
def hot_and_cold_numbers():
    # Carregar os dados da tabela stats
    data = pd.read_sql('SELECT * FROM resultados', engine)
    bola_columns = [col for col in data.columns if 'bola' in col.lower()]

    # Treine o modelo ARIMA
    model = ARIMA(data, order=(5, 1, 0))
    model_fit = model.fit(disp=0)
    # Calcular a frequência de cada número
    frequency = data[bola_columns].value_counts()

    # Identificar os números quentes e frios
    hot_numbers_prediction = model_fit.forecast(steps=5)
    cold_numbers = frequency.tail(5).index.tolist()

    return {"hot_numbers": hot_numbers_prediction, "cold_numbers": cold_numbers}
