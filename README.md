# MembershipAPI

A professional, scalable FastAPI application with PostgreSQL database, comprehensive API design, and modern development practices.

## 🚀 Features

- **Professional Architecture**: Clean separation of concerns with services, models, and API layers
- **PostgreSQL Database**: Production-ready database with connection pooling
- **Environment Configuration**: Flexible configuration management with `.env` files
- **Comprehensive API**: RESTful endpoints with proper error handling and response models
- **Authentication**: Basic HTTP authentication (easily extensible)
- **Logging**: Structured logging with configurable levels
- **Docker Support**: Easy deployment with Docker Compose
- **Test Data**: Automated test data generation script
- **API Documentation**: Auto-generated OpenAPI/Swagger documentation

## 📁 Project Structure

```
├── app/
│   ├── api/                    # API layer
│   │   ├── deps.py            # Dependencies
│   │   ├── exceptions.py      # Custom exceptions
│   │   └── responses.py       # Response models
│   ├── core/                  # Core configuration
│   │   ├── config.py          # Settings management
│   │   └── logging.py         # Logging configuration
│   ├── db/                    # Database layer
│   │   └── db.py              # Database connection and session
│   ├── models/                # Data models
│   │   ├── core.py            # All models with relationships
│   │   └── ...                # Individual model files
│   ├── routers/               # API routes
│   │   ├── customers.py       # Customer endpoints
│   │   ├── plans.py           # Plan endpoints
│   │   └── transactions.py    # Transaction endpoints
│   ├── services/              # Business logic layer
│   │   ├── base.py            # Base service class
│   │   ├── customer.py        # Customer service
│   │   ├── plan.py            # Plan service
│   │   └── transaction.py     # Transaction service
│   └── main.py                # FastAPI application
├── create_multiple_transactions.py  # Test data script
├── docker-compose.yml         # Docker services
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables
└── README.md                  # This file
```

## 🛠️ Setup Instructions

### Prerequisites

- Python 3.10+
- Docker and Docker Compose (for PostgreSQL)
- Git

### 1. Clone and Setup Environment

```bash
# Clone the repository
git clone <your-repo-url>
cd fastapi-professional

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Database Setup

#### Option A: Using Docker (Recommended)

```bash
# Start PostgreSQL and pgAdmin
docker-compose up -d

# Check if services are running
docker-compose ps
```

Services will be available at:

- PostgreSQL: `localhost:5432`
- pgAdmin: `http://localhost:8080` (admin@example.com / admin)

#### Option B: Local PostgreSQL Installation

1. Install PostgreSQL locally
2. Create database and user:

```sql
CREATE DATABASE fastapi_db;
CREATE USER fastapi_user WITH PASSWORD 'fastapi_password';
GRANT ALL PRIVILEGES ON DATABASE fastapi_db TO fastapi_user;
```

### 3. Environment Configuration

Copy the example environment file and adjust as needed:

```bash
cp .env.example .env
```

Edit `.env` file with your database credentials:

```env
DATABASE_URL=postgresql://fastapi_user:fastapi_password@localhost:5432/fastapi_db
# ... other settings
```

### 4. Run the Application

```bash
# Start the FastAPI server
fastapi dev app/main.py

# Or with uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The application will be available at:

- API: `http://localhost:8000`
- Documentation: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

### 5. Create Test Data

```bash
# Run the test data creation script
python create_multiple_transactions.py
```

This will create:

- 3 test customers
- 3 test plans
- Customer-plan relationships
- 225 test transactions

## 🔐 Authentication

The application uses HTTP Basic Authentication:

- **Username**: `admin` (configurable in `.env`)
- **Password**: `secret` (configurable in `.env`)

## 📚 API Endpoints

### Public Endpoints

- `GET /health` - Health check
- `GET /time/{iso_code}` - Get time by country code

### Authenticated Endpoints

#### Customers

- `POST /api/v1/customers` - Create customer
- `GET /api/v1/customers` - List customers (paginated)
- `GET /api/v1/customers/{id}` - Get customer by ID
- `PATCH /api/v1/customers/{id}` - Update customer
- `DELETE /api/v1/customers/{id}` - Delete customer
- `POST /api/v1/customers/{id}/plans/{plan_id}` - Add plan to customer
- `DELETE /api/v1/customers/{id}/plans/{plan_id}` - Remove plan from customer
- `GET /api/v1/customers/{id}/plans` - Get customer plans

#### Plans

- `POST /api/v1/plans` - Create plan
- `GET /api/v1/plans` - List plans (paginated)
- `GET /api/v1/plans/{id}` - Get plan by ID
- `PATCH /api/v1/plans/{id}` - Update plan
- `DELETE /api/v1/plans/{id}` - Delete plan

#### Transactions

- `POST /api/v1/transactions` - Create transaction
- `GET /api/v1/transactions` - List transactions (paginated)
- `GET /api/v1/transactions/{id}` - Get transaction by ID
- `PATCH /api/v1/transactions/{id}` - Update transaction
- `DELETE /api/v1/transactions/{id}` - Delete transaction
- `GET /api/v1/customers/{id}/transactions` - Get customer transactions
- `GET /api/v1/customers/{id}/transactions/total` - Get customer transaction total

## 🧪 Testing

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests (when implemented)
pytest
```

## 📝 Configuration

Key configuration options in `.env`:

```env
# Database
DATABASE_URL=postgresql://user:pass@host:port/db
DB_HOST=localhost
DB_PORT=5432
DB_NAME=fastapi_db
DB_USER=fastapi_user
DB_PASSWORD=fastapi_password

# Application
APP_NAME=FastAPI Professional App
DEBUG=True
SECRET_KEY=your-secret-key

# API
API_V1_PREFIX=/api/v1
CORS_ORIGINS=["http://localhost:3000"]

# Security
BASIC_AUTH_USERNAME=admin
BASIC_AUTH_PASSWORD=secret

# Logging
LOG_LEVEL=INFO
```

## 🚀 Deployment

### Docker Deployment

1. Build the application image:

```bash
# Create Dockerfile (not included in this setup)
docker build -t fastapi-app .
```

2. Use docker-compose for full deployment:

```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Production Considerations

- Use environment-specific `.env` files
- Set `DEBUG=False` in production
- Use a strong `SECRET_KEY`
- Configure proper CORS origins
- Set up SSL/TLS certificates
- Use a reverse proxy (nginx)
- Implement proper monitoring and logging

## 🔧 Development

### Adding New Features

1. **Models**: Add to `app/models/core.py`
2. **Services**: Create service in `app/services/`
3. **Routes**: Add routes in `app/routers/`
4. **Tests**: Add tests in `tests/`

### Code Style

- Follow PEP 8
- Use type hints
- Add docstrings to functions and classes
- Use meaningful variable names

## 📊 Monitoring

- Application logs are written to `app.log`
- Request timing is logged automatically
- Health check endpoint available at `/health`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.
