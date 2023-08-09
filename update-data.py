import psycopg2
from sqlalchemy import create_engine
import pandas as pd

DATABASE_URL = "postgresql://artur:Aqwe123!@localhost:5432/lotofacil"
CSV_PATH = 'lotofacil-29-05.csv'

# Create a connection using SQLAlchemy
engine = create_engine(DATABASE_URL)

# Create table (we'll use raw psycopg2 for this)
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS lotofacil_data (
        Concurso INTEGER,
        Data DATE,
        Bola1 INTEGER,
        Bola2 INTEGER,
        Bola3 INTEGER,
        Bola4 INTEGER,
        Bola5 INTEGER,
        Bola6 INTEGER,
        Bola7 INTEGER,
        Bola8 INTEGER,
        Bola9 INTEGER,
        Bola10 INTEGER,
        Bola11 INTEGER,
        Bola12 INTEGER,
        Bola13 INTEGER,
        Bola14 INTEGER,
        Bola15 INTEGER,
        Soma INTEGER
    );
""")
conn.commit()
conn.close()

# Load CSV data
data = pd.read_csv(CSV_PATH)
# Encontre todas as colunas que começam com 'bola'
bola_columns = [col for col in data.columns if 'bola' in col.lower()]

# Calcule a soma dessas colunas
data['Soma'] = data[bola_columns].sum(axis=1)

# Use the SQLAlchemy engine to insert data into the table
data.to_sql('lotofacil_data', engine, if_exists='replace', index=False)
