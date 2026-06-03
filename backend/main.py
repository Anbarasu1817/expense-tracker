from fastapi import FastAPI, Response
from sqlalchemy.exc import OperationalError

from database import create_tables
from routers import auth, expense, income, report

app = FastAPI(
    title="Expense Tracker API",
    description="Expense Tracker Backend using FastAPI and PostgreSQL",
    version="1.0.0"
)

# Create tables when app starts
try:
    create_tables()
    print("Database connected and tables created.")
except OperationalError as e:
    print("Database connection error:", e)

# Register routers
app.include_router(auth.router)
app.include_router(expense.router)
app.include_router(income.router)
app.include_router(report.router)

# Home route
@app.get("/")
def home():
    return {
        "message": "Expense Tracker API Running"
    }

# Health check route
@app.get("/health")
def health():
    return {
        "status": "ok"
    }

# Prevent favicon 404 errors
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)