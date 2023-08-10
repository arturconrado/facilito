from sqlalchemy import create_engine, Column, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sklearn.ensemble import RandomForestRegressor
import numpy as np

# SQLAlchemy setup
Base = declarative_base()


class Stats(Base):
    __tablename__ = 'stats'
    average_sum = Column(Float)
    max_sum = Column(Float)
    min_sum = Column(Float)
    last_sum = Column(Float)
    sum_std = Column(Float)
    max_odd_count = Column(Float)
    max_even_count = Column(Float)
    max_prime_count = Column(Float)
    max_fibonacci_count = Column(Float)
    last_odd_count = Column(Float)
    last_even_count = Column(Float)
    last_prime_count = Column(Float)
    last_fibonacci_count = Column(Float)
    fibonacci_count_std = Column(Float)
    prime_count_std = Column(Float)
    even_count_std = Column(Float)
    odd_count_std = Column(Float)
    average_odd_count = Column(Float)
    average_even_count = Column(Float)
    average_prime_count = Column(Float)
    average_fibonacci_count = Column(Float)
    min_odd_count = Column(Float)
    min_even_count = Column(Float)
    min_prime_count = Column(Float)
    min_fibonacci_count = Column(Float)
    last_bola1 = Column(Float)
    last_bola2 = Column(Float)
    last_bola3 = Column(Float)
    last_bola13 = Column(Float)
    last_bola14 = Column(Float)
    last_bola15 = Column(Float)
    average_bola1 = Column(Float)
    average_bola2 = Column(Float)
    average_bola3 = Column(Float)
    average_bola13 = Column(Float)
    average_bola14 = Column(Float)
    average_bola15 = Column(Float)
    max_bola1 = Column(Float)
    max_bola2 = Column(Float)
    max_bola3 = Column(Float)
    max_bola13 = Column(Float)
    max_bola14 = Column(Float)
    max_bola15 = Column(Float)
    min_bola13 = Column(Float)
    min_bola14 = Column(Float)
    min_bola15 = Column(Float)
    bola13_std = Column(Float)
    bola14_std = Column(Float)
    bola15_std = Column(Float)


DATABASE_URL = "postgresql://artur:Aqwe123!@localhost:5432/lotofacil"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Query the stats table
db = SessionLocal()
stats_query = db.query(Stats).first()

# Prepare the data for training
X = [attr for attr in vars(stats_query).values() if isinstance(attr, (int, float))]

# Example model training; adjust this part according to your actual data
X = np.array([X])
y = np.array([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]])

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)


def generate_combinations(num_combinations, min_numbers, max_numbers):
    combinations = []
    for _ in range(num_combinations):
        generated_combination = model.predict([X[0]]).astype(int)[0][:max_numbers]
        combinations.append(generated_combination[:min_numbers])
    return combinations


# Ask the user for input
num_combinations = int(input("Quantas combinações únicas você deseja? "))
min_numbers = int(input("Quantos números de no mínimo (até 15)? "))
max_numbers = int(input("Quantos números de no máximo (até 20)? "))

# Generate the combinations
combinations = generate_combinations(num_combinations, min_numbers, max_numbers)

# Print the combinations
for combination in combinations:
    print(combination)
