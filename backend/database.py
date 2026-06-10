import os
from sqlalchemy import create_engine, text

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:anbu18@localhost:5432/expense_db"
)

engine = create_engine(DATABASE_URL)

def create_tables():

    with engine.connect() as conn:

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(100) UNIQUE,
                password VARCHAR(100)
            )
        """))

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS expenses (
                id SERIAL PRIMARY KEY,
                title VARCHAR(100),
                amount FLOAT,
                category VARCHAR(100),
                date DATE,
                user_id INTEGER
            )
        """))

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS income (
                id SERIAL PRIMARY KEY,
                source VARCHAR(100),
                amount FLOAT,
                date DATE,
                user_id INTEGER
            )
        """))

        conn.commit()