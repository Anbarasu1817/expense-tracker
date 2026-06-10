from fastapi import APIRouter
from sqlalchemy import text
from database import engine

router = APIRouter()


@router.get("/expenses/{user_id}")
def get_expenses(user_id: int):

    with engine.connect() as conn:

        result = conn.execute(
            text("""
                SELECT *
                FROM expenses
                WHERE user_id=:user_id
                ORDER BY id DESC
            """),
            {"user_id": user_id}
        ).mappings().all()

        return result


@router.post("/expenses")
def add_expense(expense: dict):

    with engine.connect() as conn:

        conn.execute(
            text("""
                INSERT INTO expenses
                (title, amount, category, date, user_id)
                VALUES
                (:title, :amount, :category, :date, :user_id)
            """),
            {
                "title": expense["title"],
                "amount": expense["amount"],
                "category": expense["category"],
                "date": expense["date"],
                "user_id": expense["user_id"]
            }
        )

        conn.commit()

    return {"message": "Expense Added"}