# Virtual Environment Setup Guide

## Overview
This directory contains scripts to help you set up and manage the Python virtual environment for the Cinei-Reader backend.

## Scripts Available

### Windows Users
- **`setup_venv.bat`** - Creates a new virtual environment and installs all dependencies
- **`activate_venv.bat`** - Activates the virtual environment and shows available commands

### Unix/Linux/macOS Users  
- **`setup_venv.sh`** - Creates a new virtual environment and installs all dependencies
- **`activate_venv.sh`** - Activates the virtual environment and shows available commands

## Quick Start

### First-time Setup

**Windows:**
```cmd
# Run the setup script
setup_venv.bat

# Activate the environment
activate_venv.bat
```

**Unix/Linux/macOS:**
```bash
# Make scripts executable (first time only)
chmod +x setup_venv.sh activate_venv.sh

# Run the setup script
./setup_venv.sh

# Activate the environment
source activate_venv.sh
```

### Daily Development

**Windows:**
```cmd
activate_venv.bat
```

**Unix/Linux/macOS:**
```bash
source venv/bin/activate
```

## What the Setup Script Does

1. ✅ Checks if Python 3.8+ is installed
2. 🧹 Removes any existing virtual environment
3. 📦 Creates a new virtual environment in `venv/`
4. 🔧 Activates the virtual environment
5. 📈 Upgrades pip to the latest version
6. 📚 Installs all dependencies from `requirements.txt`
7. 📋 Shows next steps for development

## Available Commands (After Activation)

- **Start Server:** `uvicorn app.main:app --reload --host 127.0.0.1 --port 8003`
- **Run Tests:** `pytest tests/ -v`
- **Test Server:** `python test_server.py`
- **Check Imports:** `python -c "import app.main; print('✅ All imports working')"`
- **Database Migration:** `alembic upgrade head`

## Environment Configuration

1. **Copy the environment template:**
   ```bash
   cp env.template .env
   ```

2. **Edit `.env` file** with your specific configuration:
   - Database URL
   - JWT secret (use a strong, unique secret for production)
   - API settings

## Troubleshooting

### Python Not Found
- Install Python 3.8+ from https://python.org
- Make sure Python is added to your system PATH

### Permission Denied (Unix/Linux/macOS)
```bash
chmod +x setup_venv.sh activate_venv.sh
```

### Dependencies Installation Failed
- Check your internet connection
- Try upgrading pip: `python -m pip install --upgrade pip`
- Check if any dependencies have conflicts

### Virtual Environment Already Exists
The setup script will automatically remove and recreate the virtual environment.

## Manual Setup (Alternative)

If the scripts don't work, you can set up manually:

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate.bat

# Activate (Unix/Linux/macOS)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Deactivating the Environment

When you're done working:
```bash
deactivate
```

## Directory Structure
```
backend/
├── venv/              # Virtual environment (created by setup)
├── setup_venv.bat     # Windows setup script
├── setup_venv.sh      # Unix setup script
├── activate_venv.bat  # Windows activation script
├── activate_venv.sh   # Unix activation script
├── requirements.txt   # Python dependencies
├── env.template       # Environment variables template
└── VENV_SETUP.md     # This file
```
