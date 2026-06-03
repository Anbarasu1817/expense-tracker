from fastapi import APIRouter
from fastapi.responses import FileResponse
from sqlalchemy import text
from database import engine
from reportlab.platypus import SimpleDocTemplate, Table

router = APIRouter()

@router.get("/export-pdf")
def export_pdf():

    pdf_file = "expense_report.pdf"

    with engine.connect() as conn:

        result = conn.execute(
            text("""
                SELECT title, amount, category, date
                FROM expenses
            """)
        )

        data = [["Title", "Amount", "Category", "Date"]]

        for row in result:
            data.append([
                row[0],
                str(row[1]),
                row[2],
                str(row[3])
            ])

    pdf = SimpleDocTemplate(pdf_file)

    table = Table(data)

    pdf.build([table])

    return FileResponse(
        pdf_file,
        media_type="application/pdf",
        filename="expense_report.pdf"
    )