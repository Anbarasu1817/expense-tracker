from fastapi import APIRouter
from sqlalchemy import text
from database import engine

router = APIRouter()


@router.post("/register")
def register(user: dict):

    with engine.connect() as conn:

        check = conn.execute(
            text("""
                SELECT *
                FROM users
                WHERE username=:username
            """),
            {"username": user["username"]}
        ).fetchone()

        if check:
            return {"message": "Username already exists"}

        conn.execute(
            text("""
                INSERT INTO users
                (username, password)
                VALUES
                (:username, :password)
            """),
            {
                "username": user["username"],
                "password": user["password"]
            }
        )

        conn.commit()

    return {"message": "Registered Successfully"}


@router.post("/login")
def login(user: dict):

    with engine.connect() as conn:

        result = conn.execute(
            text("""
                SELECT *
                FROM users
                WHERE username=:username
                AND password=:password
            """),
            {
                "username": user["username"],
                "password": user["password"]
            }
        )

        row = result.fetchone()

        if row:
            return {
                "message": "Login Successful",
                "user_id": row.id,
                "username": row.username
            }

        return {"message": "Invalid Credentials"}