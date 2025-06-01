Finance-Tracker-with-FastAPi
This finance Tracker is built with python using FastAPi

💰 Personal Finance Tracker API
A FastAPI-based backend that helps users track income, expenses, and manage budgets. It supports transaction categorization, reporting, and is designed to integrate easily with a frontend like Streamlit or React.

🚀 Features
✅ User registration and authentication
✅ Add income and expense transactions
✅ Auto-categorize or manually assign categories
✅ Generate reports with total income, expenses, and net balance
✅ Filter transactions by category or date range
✅ Swagger UI for exploring the API
🛠 Tech Stack
FastAPI for building APIs
SQLModel for ORM
SQLite / PostgreSQL for the database
Pydantic for validation
Uvicorn as ASGI server

📂 Project Structure

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


## 🛠️ Planned Features
The following features are planned for future releases:

User Roles & Permissions
Currently, the API does not differentiate between user types. In future versions, we plan to introduce:

Standard Users: Can manage their own transactions and categories.

Admin Users: Can manage all users, categories, and oversee data integrity.

Role-Based Access Control (RBAC) using FastAPI dependencies or OAuth scopes


📄 License
This project is licensed under the MIT License. Feel free to use and adapt it.