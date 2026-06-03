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
                (amount, source, date)
                VALUES
                (:amount, :source, :date)
            """),
            {
                "amount": data["amount"],
                "source": data["source"],
                "date": data["date"]
            }
        )

        conn.commit()

    return {"message": "Income Added"}


@router.get("/income")
def get_income():

    with engine.connect() as conn:

        result = conn.execute(
            text("""
                SELECT *
                FROM income
                ORDER BY id DESC
            """)
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


@router.put("/income/{income_id}")
def update_income(income_id: int, data: dict):

    with engine.connect() as conn:

        conn.execute(
            text("""
                UPDATE income
                SET
                    amount=:amount,
                    source=:source,
                    date=:date
                WHERE id=:id
            """),
            {
                "id": income_id,
                "amount": data["amount"],
                "source": data["source"],
                "date": data["date"]
            }
        )

        conn.commit()

    return {"message": "Income Updated"}


@router.delete("/income/{income_id}")
def delete_income(income_id: int):

    with engine.connect() as conn:

        conn.execute(
            text("""
                DELETE FROM income
                WHERE id=:id
            """),
            {"id": income_id}
        )

        conn.commit()

    return {"message": "Income Deleted"}