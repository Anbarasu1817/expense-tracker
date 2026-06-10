from fastapi import APIRouter
from sqlalchemy import text
from database import engine

router = APIRouter()


@router.post("/income")
def add_income(data: dict):

    with engine.connect() as conn:

        conn.execute(
            text("""
                INSERT INTO income
                (amount, source, date, user_id)
                VALUES
                (:amount,:source,:date,:user_id)
            """),
            {
                "amount": data["amount"],
                "source": data["source"],
                "date": data["date"],
                "user_id": data["user_id"]
            }
        )

        conn.commit()

    return {"message": "Income Added"}


@router.get("/income/{user_id}")
def get_income(user_id: int):

    with engine.connect() as conn:

        result = conn.execute(
            text("""
                SELECT *
                FROM income
                WHERE user_id=:user_id
                ORDER BY id DESC
            """),
            {"user_id": user_id}
        )

        data = []

        for row in result:
            data.append({
                "id": row.id,
                "amount": row.amount,
                "source": row.source,
                "date": str(row.date)
            })

        return data