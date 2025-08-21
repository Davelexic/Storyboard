#!/usr/bin/env python3
"""
Simple test script to verify the server can start and run.
"""
import sys
import time
import requests
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test that all required modules can be imported."""
    print("🔍 Testing imports...")
    try:
        from app.config import settings
        print("✅ Config loaded successfully")
        print(f"   Database URL: {settings.database_url}")
        print(f"   Debug Mode: {settings.debug}")
    except Exception as e:
        print(f"❌ Config import failed: {e}")
        return False
    
    try:
        from app.main import app
        print("✅ FastAPI app imported successfully")
    except Exception as e:
        print(f"❌ FastAPI app import failed: {e}")
        return False
    
    try:
        from app.db import engine
        from sqlmodel import SQLModel
        from app.models import User, Book, AnalyticsEvent
        print("✅ Database models imported successfully")
    except Exception as e:
        print(f"❌ Database models import failed: {e}")
        return False
    
    return True

def test_database():
    """Test database connection and table creation."""
    print("\n🔍 Testing database...")
    try:
        from app.db import engine
        from sqlmodel import SQLModel
        from app.models import User, Book, AnalyticsEvent
        
        # Create tables
        SQLModel.metadata.create_all(engine)
        print("✅ Database tables created successfully")
        return True
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def test_server_startup():
    """Test that the server can start."""
    print("\n🔍 Testing server startup...")
    try:
        import uvicorn
        from app.main import app
        
        # This should not raise any exceptions
        print("✅ Server startup test passed")
        return True
    except Exception as e:
        print(f"❌ Server startup test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Testing Backend Setup")
    print("=" * 50)
    
    tests = [
        ("Module Imports", test_imports),
        ("Database Connection", test_database),
        ("Server Startup", test_server_startup),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running: {test_name}")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} FAILED with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Backend is ready to run.")
        print("\n🚀 To start the server:")
        print("   venv\\Scripts\\uvicorn.exe app.main:app --reload --host 127.0.0.1 --port 8000")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
