from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql://postgres:anbu18@localhost:5432/expense_db"

engine = create_engine(DATABASE_URL, echo=True)


# ✅ Create tables function (THIS WAS MISSING BEFORE)
def create_tables():

    with engine.connect() as conn:

        # USERS TABLE
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(100) UNIQUE,
                password VARCHAR(100)
            )
        """))

        # EXPENSES TABLE
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS expenses (
                id SERIAL PRIMARY KEY,
                title VARCHAR(100),
                amount FLOAT,
                category VARCHAR(100),
                date DATE
            )
        """))

        # INCOME TABLE
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS income (
                id SERIAL PRIMARY KEY,
                source VARCHAR(100),
                amount FLOAT,
                date DATE
            )
        """))

        conn.commit()