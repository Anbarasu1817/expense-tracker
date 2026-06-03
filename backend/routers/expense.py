from fastapi import APIRouter
from sqlalchemy import text
from database import engine

router = APIRouter()


# Get all expenses
@router.get("/expenses")
def get_expenses():

    with engine.connect() as conn:

        result = conn.execute(
            text("""
                SELECT *
                FROM expenses
                ORDER BY id DESC
            """)
        ).mappings().all()

        return result


# Add expense
@router.post("/expenses")
def add_expense(expense: dict):

    required_fields = ["title", "amount", "category", "date"]

    for field in required_fields:
        if field not in expense:
            return {"error": f"{field} is required"}

    with engine.connect() as conn:

        conn.execute(
            text("""
                INSERT INTO expenses
                (title, amount, category, date)
                VALUES
                (:title, :amount, :category, :date)
            """),
            {
                "title": expense.get("title"),
                "amount": expense.get("amount"),
                "category": expense.get("category"),
                "date": expense.get("date")
            }
        )

        conn.commit()

    return {"message": "Expense Added Successfully"}


# Delete expense
@router.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int):

    with engine.connect() as conn:

        conn.execute(
            text("""
                DELETE FROM expenses
                WHERE id = :id
            """),
            {"id": expense_id}
        )

        conn.commit()

    return {"message": "Expense Deleted Successfully"}


# Update expense
@router.put("/expenses/{expense_id}")
def update_expense(expense_id: int, expense: dict):

    required_fields = ["title", "amount", "category", "date"]

    for field in required_fields:
        if field not in expense:
            return {"error": f"{field} is required"}

    with engine.connect() as conn:

        conn.execute(
            text("""
                UPDATE expenses
                SET
                    title = :title,
                    amount = :amount,
                    category = :category,
                    date = :date
                WHERE id = :id
            """),
            {
                "id": expense_id,
                "title": expense.get("title"),
                "amount": expense.get("amount"),
                "category": expense.get("category"),
                "date": expense.get("date")
            }
        )

        conn.commit()

    return {"message": "Expense Updated Successfully"}