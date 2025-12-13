# MembershipAPI

A professional FastAPI REST API for membership management. Built as a portfolio project to demonstrate modern Python backend development practices.

## 🚀 Live Demo

[**View Live API Documentation →**](https://membershipapi.onrender.com/docs)

## ✨ Features

- **RESTful API** with full CRUD operations
- **SQLModel ORM** for type-safe database operations
- **Auto-generated documentation** (Swagger UI & ReDoc)
- **HTTP Basic Authentication**
- **Professional architecture** with services, models, and routers
- **Demo data** auto-generated on startup

## 🛠️ Tech Stack

- **FastAPI** - Modern, fast web framework
- **SQLModel** - SQL database with Python type hints
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server
- **SQLite** - Lightweight database (PostgreSQL compatible)

## 📁 Project Structure

```
├── app/
│   ├── api/            # Dependencies, exceptions, responses
│   ├── core/           # Configuration and logging
│   ├── db/             # Database connection and seeding
│   ├── models/         # SQLModel data models
│   ├── routers/        # API route handlers
│   ├── services/       # Business logic layer
│   └── main.py         # FastAPI application
├── render.yaml         # Render deployment config
├── requirements.txt    # Python dependencies
└── README.md
```

## 🏃 Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/membershipapi.git
cd membershipapi

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn app.main:app --reload
```

Visit `http://localhost:8000/docs` for the interactive API documentation.

## 📚 API Endpoints

### Public
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/time/{iso_code}` | Get time by country code |

### Customers (Authenticated)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/customers` | Create customer |
| GET | `/api/v1/customers` | List customers |
| GET | `/api/v1/customers/{id}` | Get customer |
| PATCH | `/api/v1/customers/{id}` | Update customer |
| DELETE | `/api/v1/customers/{id}` | Delete customer |

### Plans (Authenticated)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/plans` | Create plan |
| GET | `/api/v1/plans` | List plans |
| GET | `/api/v1/plans/{id}` | Get plan |
| PATCH | `/api/v1/plans/{id}` | Update plan |
| DELETE | `/api/v1/plans/{id}` | Delete plan |

### Transactions (Authenticated)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/transactions` | Create transaction |
| GET | `/api/v1/transactions` | List transactions |
| GET | `/api/v1/transactions/{id}` | Get transaction |
| PATCH | `/api/v1/transactions/{id}` | Update transaction |
| DELETE | `/api/v1/transactions/{id}` | Delete transaction |

## 🔐 Authentication

HTTP Basic Authentication:
- **Username**: `admin`
- **Password**: `secret`

## 🚀 Deploy to Render

1. Push your code to GitHub
2. Go to [render.com](https://render.com) → New → Blueprint
3. Select your repository
4. Render will auto-detect `render.yaml` and deploy

## 📄 License

MIT License
