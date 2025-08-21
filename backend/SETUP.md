# Backend Setup Guide

## Quick Start

### 1. Virtual Environment Setup

The project uses a virtual environment to isolate dependencies. The virtual environment is already created in the `venv/` directory.

#### Windows (Command Prompt)
```cmd
# Activate virtual environment
venv\Scripts\activate.bat

# Or use the convenience script
activate_venv.bat
```

#### Windows (PowerShell)
```powershell
# Activate virtual environment
venv\Scripts\Activate.ps1
```

#### Linux/macOS
```bash
# Activate virtual environment
source venv/bin/activate
```

### 2. Install Dependencies

Dependencies are already installed in the virtual environment. If you need to reinstall:

```bash
# Activate virtual environment first, then:
pip install -r requirements.txt
```

### 3. Environment Configuration

Copy the environment template and configure it:

```bash
cp env.template .env
# Edit .env with your database credentials and other settings
```

### 4. Database Setup

#### Option A: PostgreSQL (Recommended)
```bash
# Create database
createdb cinei_reader

# Run migrations
alembic upgrade head
```

#### Option B: SQLite (Development)
```bash
# Update .env to use SQLite
DATABASE_URL=sqlite:///./cinei_reader.db

# Run migrations
alembic upgrade head
```

### 5. Start Development Server

```bash
# Activate virtual environment first, then:
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- Main API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

### Run Tests
```bash
# Activate virtual environment first, then:
pytest tests/ -v
```

### Run Tests with Coverage
```bash
pytest tests/ --cov=app --cov-report=html
```

## Development Workflow

### 1. Activate Virtual Environment
Always activate the virtual environment before working on the backend:

```bash
# Windows
venv\Scripts\activate.bat

# Linux/macOS
source venv/bin/activate
```

### 2. Make Code Changes
Edit files in the `app/` directory.

### 3. Test Changes
```bash
# Run tests
pytest tests/ -v

# Check imports
python -c "from app.main import app; print('Imports OK')"
```

### 4. Start Server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Database Management

### Create New Migration
```bash
alembic revision --autogenerate -m "description of changes"
alembic upgrade head
```

### Reset Database
```bash
alembic downgrade base
alembic upgrade head
```

### View Migration History
```bash
alembic history
```

## Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   # Ensure virtual environment is activated
   venv\Scripts\activate.bat
   
   # Reinstall dependencies
   pip install -r requirements.txt
   ```

2. **Database Connection Issues**
   ```bash
   # Check .env file
   # Ensure database exists
   # Verify connection string
   ```

3. **Migration Errors**
   ```bash
   # Reset migrations
   alembic downgrade base
   alembic upgrade head
   ```

4. **Port Already in Use**
   ```bash
   # Use different port
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
   ```

### Virtual Environment Issues

If the virtual environment is corrupted:

```bash
# Remove old environment
rmdir /s venv

# Create new environment
python -m venv venv

# Activate and install dependencies
venv\Scripts\activate.bat
pip install -r requirements.txt
```

## Production Deployment

### Environment Variables
Set these in production:
- `DEBUG=false`
- `JWT_SECRET=strong-secret-key`
- `DATABASE_URL=production-database-url`

### Start Production Server
```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## API Endpoints

### Authentication
- `POST /users/register` - Register new user
- `POST /users/login` - Login user
- `GET /users/me` - Get current user

### Books
- `POST /books/upload` - Upload EPUB file
- `GET /books/jobs/{job_id}/status` - Check processing status
- `GET /books/jobs/{job_id}/result` - Get processed markup
- `GET /books/` - List user's books
- `GET /books/{book_id}` - Get specific book
- `GET /books/{book_id}/markup` - Get book markup
- `DELETE /books/{book_id}` - Delete book

### Analytics
- `POST /analytics/events` - Log analytics events
- `GET /analytics/summary` - Get analytics summary

## File Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration
│   ├── db.py                # Database setup
│   ├── security.py          # Authentication
│   ├── models/              # Database models
│   ├── routers/             # API routes
│   └── services/            # Business logic
├── tests/                   # Test files
├── alembic/                 # Database migrations
├── venv/                    # Virtual environment
├── requirements.txt         # Python dependencies
├── env.template             # Environment template
├── activate_venv.bat        # Windows activation script
└── SETUP.md                 # This file
```

## Dependencies

### Core
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `sqlmodel` - Database ORM
- `alembic` - Database migrations

### Authentication
- `passlib` - Password hashing
- `python-jose` - JWT tokens

### File Processing
- `python-multipart` - File uploads

### Testing
- `pytest` - Testing framework
- `httpx` - HTTP client for testing

### Development
- `python-dotenv` - Environment variables
- `requests` - HTTP client
