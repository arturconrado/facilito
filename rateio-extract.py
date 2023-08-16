import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import env

## Ler o arquivo CSV
df = pd.read_csv('lotofacil/rateio_lotofacil.csv')

# Remover o símbolo de moeda e outros caracteres não numéricos
df['Prêmio'] = df['Prêmio'].replace('[^0-9.]', '', regex=True)

# Converter a coluna 'Prêmio' para float e dividir por 100 para corrigir os dois zeros extras
df['Prêmio'] = df['Prêmio'].astype(float) / 100

# Mapear a coluna 'Faixa' para valores inteiros
faixa_mapping = {
    '15 Acertos': 15,
    '14 Acertos': 14,
    '13 Acertos': 13,
    '12 Acertos': 12,
    '11 Acertos': 11,
}
df['Faixa'] = df['Faixa'].map(faixa_mapping)

# Criar uma conexão com o banco de dados PostgreSQL
engine = create_engine(env.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

# Inserir os dados na tabela 'rateio'
df.to_sql('rateio', engine, index=False, if_exists='append', method='multi')

print("Dados inseridos com sucesso!")
