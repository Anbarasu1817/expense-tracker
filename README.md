# 💰 Expense Tracker
# 💰 Expense Tracker App

A full-stack Expense Tracker built using **FastAPI + PostgreSQL + Streamlit**

---

## 🚀 Features

- 👤 User Registration & Login  
- 💸 Add / Edit / Delete Expenses  
- 💰 Income Tracking  
- 📊 Dashboard with Charts  
- 📅 Monthly Reports  
- 📥 PDF Download  
- 🔍 Search & Filter Expenses  

---

## 🛠️ Tech Stack

- Frontend: Streamlit  
- Backend: FastAPI  
- Database: PostgreSQL  
- Visualization: Plotly  

---

## 🔗 Live Demo

Frontend:
[https://your-app.streamlit.app](http://localhost:8501/)

Backend API:
[https://your-api.onrender.com/docs](http://127.0.0.1:8000/docs)

---

## 🎯 API Endpoints
POST /register
POST /login
GET /expenses
POST /expenses
DELETE /expenses/{id}
GET /income

--- 

## 📁 Project Structure
expense-tracker/
  backend/
    app/
      api/          # Route handlers (auth, expenses, income, categories, summary)
      models/       # SQLAlchemy ORM models
      schemas/      # Pydantic request/response schemas
      services/     # Business logic layer
      core/         # Config, security helpers
      db/           # Database connection, initialization
    tests/          # Unit tests
  frontend/
    pages/          # Dashboard, Add Expense, Add Income, History
    utils/          # API client, auth helpers
    .streamlit/     # Streamlit theme config
  .env.example
  requirements.txt

---

## Backend Start:
   cd backend
   uvicorn main:app --reload

## Frontend Start:
   cd frontend
   streamlit run app.py

---
