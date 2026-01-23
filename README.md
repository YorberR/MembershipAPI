# ⚡ MMembershipAPI: Scalable SaaS Backend

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![SQLModel](https://img.shields.io/badge/SQLModel-Type_Safe-52B0E7?style=for-the-badge)
![Pydantic](https://img.shields.io/badge/Pydantic-Validation-E92063?style=for-the-badge)

A professional, type-safe REST API for membership management. Built as a portfolio project to demonstrate **modern Python backend development practices**, leveraging the speed of FastAPI and the reliability of Pydantic.

### 🚀 [View Live API Documentation (Swagger UI)](https://membershipapi-ymy1.onrender.com/docs)


## ✨ Key Features

* **High Performance:** Built on Starlette and Pydantic, making it one of the fastest Python frameworks available.
* **Type Safety:** Uses **SQLModel** (combining SQLAlchemy + Pydantic) to ensure data consistency from the database to the API response.
* **Architecture:** Implements a "Service Pattern" to separate business logic from route handlers.
* **Auto-Documentation:** Interactive Swagger UI & ReDoc generated automatically from the code.
* **Security:** HTTP Basic Authentication implementation.


## 🛠️ Tech Stack

* **Framework:** FastAPI
* **ORM:** SQLModel (SQLAlchemy wrapper)
* **Validation:** Pydantic
* **Server:** Uvicorn (ASGI)
* **Database:** SQLite (Embedded for Demo) / Compatible with PostgreSQL


## 📁 Project Architecture

The project follows a modular structure to ensure scalability and maintainability:

```text
├── app
│   ├── api/           # Dependencies & Error handling
│   ├── core/          # Config & Logging (Environment vars)
│   ├── db/            # Database connection & Seeding
│   ├── models/        # SQLModel definitions (DB Schemas)
│   ├── routers/       # Endpoints (Controller layer)
│   ├── services/      # Business Logic (Service layer)
│   └── main.py        # App Entry Point
```
## 🏃 Quick Start
To run this project locally:

1. **Clone the repository:**
```bash
git clone [https://github.com/YorberR/MembershipAPI.git](https://github.com/YorberR/MembershipAPI.git)
cd MembershipAPI
```
2. **Create virtual environment:**
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```
3. **Install dependencies:**
```bash
pip install -r requirements.txt
```
4. **Run the application:**
```bash
uvicorn app.main:app --reload
```
5. **Explore:** Visit http://localhost:8000/docs to see the interactive documentation.

---

## 📚 API Endpoints
The API provides full CRUD operations for the following resources:

🔐 **Authentication**

- **Standard HTTP Basic Auth** is required for write operations.

- **Demo Credentials:**

    - Username: admin

    - Password: secret

**👥 Customers**

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | `/api/v1/customers` | Register a new customer |
| GET | `/api/v1/customers` | List all customers |
| PATCH | `/api/v1/customers/{id}` | Update details |
| DELETE | `/api/v1/customers/{id}` | Remove customer |

**💳 Plans & Transactions**

- **Plans:** Manage subscription tiers (Gold, Silver, etc).

- **Transactions:** Record payments and subscription events.

(Full list available in the Swagger UI)


## 🚀 Deployment
This application is deployed on **Render** using a native Python environment.

- **Configuration:** render.yaml handles the build and start commands automatically.

- **Data:** The application auto-seeds demo data on startup if the database is empty.

## 📄 License

This project is released under [MIT License](https://github.com/YorberR/MembershipAPI/blob/main/LICENSE)

