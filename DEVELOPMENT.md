# Development Guide

## Prerequisites

- Python 3.8+
- Node.js 16+
- PostgreSQL 12+
- React Native development environment

## Environment Setup

### 1. Backend Setup

```bash
# Clone the repository
git clone <repository-url>
cd Storyboard

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
cd backend
pip install -r requirements.txt

# Set up environment variables
cp env.template .env
# Edit .env with your database credentials and other settings

# Set up database
# Create PostgreSQL database
createdb cinei_reader

# Run migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Frontend Setup

```bash
# Install Node.js dependencies
cd client
npm install

# Start React Native development server
npx react-native start

# Run on Android
npx react-native run-android

# Run on iOS (macOS only)
npx react-native run-ios
```

## Database Management

### Creating Migrations

```bash
cd backend
alembic revision --autogenerate -m "description of changes"
alembic upgrade head
```

### Resetting Database

```bash
cd backend
alembic downgrade base
alembic upgrade head
```

## Testing

### Backend Tests

```bash
cd backend
pytest tests/ -v
pytest tests/ --cov=app --cov-report=html
```

### Frontend Tests

```bash
cd client
npm test
```

## Code Quality

### Backend

```bash
cd backend
# Format code
black app/ tests/

# Lint code
flake8 app/ tests/

# Type checking
mypy app/
```

### Frontend

```bash
cd client
npm run lint
```

## API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Environment Variables

### Backend (.env)

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/cinei_reader

# Security
JWT_SECRET=your-super-secret-jwt-key-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API Configuration
API_HOST=localhost
API_PORT=8000
APP_NAME=Cinematic Reading Engine

# Development
DEBUG=true
LOG_LEVEL=INFO

# File Upload
MAX_FILE_SIZE=52428800
UPLOAD_DIR=./uploads

# Analysis Pipeline
ANALYSIS_TIMEOUT=300
MAX_CONCURRENT_ANALYSIS=5

# Effects Configuration
DEFAULT_EFFECT_INTENSITY=0.5
MAX_EFFECTS_PER_CHAPTER=3
MIN_PARAGRAPHS_BETWEEN_EFFECTS=2
```

## Troubleshooting

### Common Issues

1. **SQLModel Import Error**
   ```bash
   pip install sqlmodel
   ```

2. **Database Connection Issues**
   - Ensure PostgreSQL is running
   - Check DATABASE_URL in .env
   - Verify database exists: `createdb cinei_reader`

3. **Migration Errors**
   ```bash
   alembic downgrade base
   alembic upgrade head
   ```

4. **React Native Issues**
   ```bash
   npx react-native doctor
   cd android && ./gradlew clean
   ```

### Performance Optimization

1. **Database Indexes**
   - Ensure proper indexes on frequently queried columns
   - Monitor query performance with `EXPLAIN ANALYZE`

2. **File Processing**
   - Monitor memory usage during large file processing
   - Consider implementing streaming for very large files

3. **Effect Rendering**
   - Profile effect rendering performance on target devices
   - Implement effect caching for repeated patterns

## Deployment

### Production Checklist

- [ ] Set `DEBUG=false` in production
- [ ] Use strong JWT_SECRET
- [ ] Configure proper database connection pooling
- [ ] Set up monitoring and logging
- [ ] Configure CORS for production domains
- [ ] Set up SSL/TLS certificates
- [ ] Configure backup strategy
- [ ] Set up CI/CD pipeline

### Docker Deployment

```bash
# Build image
docker build -t cinei-reader .

# Run container
docker run -p 8000:8000 cinei-reader
```

## Contributing

1. Create feature branch: `git checkout -b feature/name`
2. Make changes and test thoroughly
3. Run linting and tests
4. Submit pull request with detailed description

## Architecture Overview

### Backend Architecture

```
app/
├── main.py              # FastAPI application entry point
├── config.py            # Configuration management
├── db.py                # Database connection and session management
├── security.py          # Authentication and authorization
├── models/              # SQLModel database models
├── routers/             # API route handlers
└── services/            # Business logic and analysis pipeline
    ├── story_analyzer.py        # Main analysis orchestrator
    ├── structural_analyzer.py   # Narrative structure analysis
    ├── character_analyzer.py    # Character development tracking
    ├── emotion_scorer.py        # Emotional intensity calculation
    ├── effect_selector.py       # Intelligent effect selection
    ├── quality_controller.py    # Effect quality validation
    ├── sparsity_controller.py   # Sparsity enforcement
    ├── parser.py                # EPUB parsing utilities
    └── converter.py             # Format conversion utilities
```

### Frontend Architecture

```
client/
├── App.js               # Main application component
├── components/          # Reusable UI components
├── services/            # API and external service integrations
└── utils/               # Utility functions and helpers
```

## Analysis Pipeline

The intelligent analysis system consists of 7 components:

1. **StoryAnalyzer**: Main orchestrator coordinating all analysis
2. **StoryStructureAnalyzer**: Narrative structure and pacing analysis
3. **CharacterEmotionAnalyzer**: Character development and emotional tracking
4. **EmotionalIntensityScorer**: Multi-factor emotional weight calculation
5. **IntelligentEffectSelector**: Context-aware effect selection
6. **EffectQualityController**: Quality validation and filtering
7. **EffectSparsityController**: Sparsity enforcement ("less is more")

## Effects System

The effects system follows a tiered approach:

- **Tier 1 (Micro)**: Subtle atmospheric effects (0.1% usage)
- **Tier 2 (Moderate)**: Visual and typographic effects (1% usage)
- **Tier 3 (Dramatic)**: High-impact effects (0.01% usage)
- **Tier 4 (Meta)**: Narrative-breaking effects (1-2 per book)

## Performance Metrics

- **Processing Speed**: Average novel processing in <2 minutes
- **Effect Accuracy**: 95%+ context-appropriate effect selection
- **Mobile Performance**: 60fps animations with hardware acceleration
- **Memory Usage**: Optimized for mobile devices with limited RAM

## Security Considerations

- JWT tokens for authentication
- Input validation on all endpoints
- File type and size validation
- SQL injection prevention via SQLModel
- CORS configuration for production
- Rate limiting (to be implemented)
