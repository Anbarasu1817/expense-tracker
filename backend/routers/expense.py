from fastapi import APIRouter
from sqlalchemy import text
from database import engine

router = APIRouter()


# Get User Expenses
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


# Add Expense
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


# Delete Expense
@router.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int):

    with engine.connect() as conn:

        conn.execute(
            text("""
                DELETE FROM expenses
                WHERE id=:id
            """),
            {"id": expense_id}
        )

        conn.commit()

    return {"message": "Expense Deleted"}


# Update Expense
@router.put("/expenses/{expense_id}")
def update_expense(expense_id: int, expense: dict):

    with engine.connect() as conn:

        conn.execute(
            text("""
                UPDATE expenses
                SET
                    title=:title,
                    amount=:amount,
                    category=:category,
                    date=:date
                WHERE id=:id
            """),
            {
                "id": expense_id,
                "title": expense["title"],
                "amount": expense["amount"],
                "category": expense["category"],
                "date": expense["date"]
            }
        )

        conn.commit()

    return {"message": "Expense Updated"}