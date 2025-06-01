# Finance-Tracker-with-FastAPi
This finance Tracker is built with python using FastAPi 

# 💰 Personal Finance Tracker API

A FastAPI-based backend that helps users track income, expenses, and manage budgets. It supports transaction categorization, reporting, and is designed to integrate easily with a frontend like Streamlit or React.

---

## 🚀 Features

- ✅ User registration and authentication 
- ✅ Add income and expense transactions
- ✅ Auto-categorize or manually assign categories
- ✅ Generate reports with total income, expenses, and net balance
- ✅ Filter transactions by category or date range
- ✅ Swagger UI for exploring the API

---

## 🛠 Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/) for building APIs
- [SQLModel](https://sqlmodel.tiangolo.com/) for ORM
- SQLite / PostgreSQL for the database
- Pydantic for validation
- Uvicorn as ASGI server

---

## 📂 Project Structure

personal-finance-tracker-api/
│
├── app/
│ ├── main.py # FastAPI app entry point
│ ├── models.py # SQLModel models (User, Transaction, Category)
│ ├── database.py # DB engine and session
│ ├── routes/
│ │ ├── user_route.py # User routes
│ │ ├── transaction_route.py
│ │ └── category_route.py
│ └── utils/
│ └── auto_categorizer.py # Optional auto-categorization logic
│
├── requirements.txt
├── .gitignore
└── README.md
