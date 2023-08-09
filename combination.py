from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from itertools import combinations
import random
import utils

# Database configuration
DATABASE_URL = "postgresql://artur:Aqwe123!@localhost:5432/lotofacil"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()
is_prime = utils.is_prime
is_fibonacci = utils.is_fibonacci

Base = declarative_base()

combination = FastAPI()


class Stats(Base):
    __tablename__ = "lotofacil_stats"
    average_sum = Column(Float, primary_key=True)
    max_sum = Column(Float)
    min_sum = Column(Float)
    max_even_count = Column(Float)
    max_odd_numbers = Column(Float)
    max_prime_count = Column(Float)
    max_fibonacci_count = Column(Float)


def generate_combinations():
    stats_data = db.query(Stats).first()
    all_combinations = list(combinations(range(1, 26), 15))
    valid_combinations = []

    for comb in all_combinations:
        sum_comb = sum(comb)
        even_count = sum(1 for x in comb if x % 2 == 0)
        odd_count = 15 - even_count
        prime_count = sum(1 for x in comb if is_prime(x))
        fibonacci_count = sum(1 for x in comb if is_fibonacci(x))

        # Check if the combination meets the criteria
        if (stats_data.min_sum <= sum_comb <= stats_data.max_sum and
                even_count <= stats_data.max_even_count and
                odd_count <= stats_data.max_odd_numbers and
                prime_count <= stats_data.max_prime_count and
                fibonacci_count <= stats_data.max_fibonacci_count):
            valid_combinations.append(comb)
            if len(valid_combinations) == 10:
                break

    return valid_combinations


@combination.get("/combination")
# Output the 10 valid combinations
def get_combination():
    valid_combinations = generate_combinations()
    return {"combinations": valid_combinations}
