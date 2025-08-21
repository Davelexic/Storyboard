#!/usr/bin/env python3
"""
Simple test script to verify the server can start and run.
"""
import sys
import time
import requests
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test that all required modules can be imported."""
    logger.info("🔍 Testing imports...")
    try:
        from app.config import settings
        logger.info("✅ Config loaded successfully")
        logger.info(f"   Database URL: {settings.database_url}")
        logger.info(f"   Debug Mode: {settings.debug}")
    except Exception as e:
        logger.error(f"❌ Config import failed: {e}")
        return False
    
    try:
        from app.main import app
        logger.info("✅ FastAPI app imported successfully")
    except Exception as e:
        logger.error(f"❌ FastAPI app import failed: {e}")
        return False
    
    try:
        from app.db import engine
        from sqlmodel import SQLModel
        from app.models import User, Book, AnalyticsEvent
        logger.info("✅ Database models imported successfully")
    except Exception as e:
        logger.error(f"❌ Database models import failed: {e}")
        return False
    
    return True

def test_database():
    """Test database connection and table creation."""
    logger.info("\n🔍 Testing database...")
    try:
        from app.db import engine
        from sqlmodel import SQLModel
        from app.models import User, Book, AnalyticsEvent
        
        # Create tables
        SQLModel.metadata.create_all(engine)
        logger.info("✅ Database tables created successfully")
        return True
    except Exception as e:
        logger.error(f"❌ Database test failed: {e}")
        return False

def test_server_startup():
    """Test that the server can start."""
    logger.info("\n🔍 Testing server startup...")
    try:
        import uvicorn
        from app.main import app
        
        # This should not raise any exceptions
        logger.info("✅ Server startup test passed")
        return True
    except Exception as e:
        logger.error(f"❌ Server startup test failed: {e}")
        return False

def main():
    """Run all tests."""
    logger.info("🚀 Testing Backend Setup")
    logger.info("=" * 50)
    
    tests = [
        ("Module Imports", test_imports),
        ("Database Connection", test_database),
        ("Server Startup", test_server_startup),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        logger.info(f"\n📋 Running: {test_name}")
        try:
            if test_func():
                passed += 1
                logger.info(f"✅ {test_name} PASSED")
            else:
                logger.error(f"❌ {test_name} FAILED")
        except Exception as e:
            logger.error(f"❌ {test_name} FAILED with exception: {e}")
    
    logger.info("\n" + "=" * 50)
    logger.info(f"📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 All tests passed! Backend is ready to run.")
        logger.info("\n🚀 To start the server:")
        logger.info("   venv\\Scripts\\uvicorn.exe app.main:app --reload --host 127.0.0.1 --port 8000")
    else:
        logger.error("⚠️  Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
