@echo off
echo Setting up Python 3.13.4 environment...

:: Create virtual environment
echo Creating virtual environment...
python -m venv venv

:: Activate virtual environment
call venv\Scripts\activate

:: Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip setuptools wheel

:: Install NumPy with pre-built wheel
echo Installing NumPy...
pip install --only-binary=:all: numpy==1.26.4

:: Install core dependencies
echo Installing core dependencies...
pip install fastapi==0.110.0 uvicorn[standard]==0.27.0 neo4j==5.16.0
pip install python-jose[cryptography]==3.3.0 passlib[bcrypt]==1.7.4 python-multipart==0.0.6
pip install python-dotenv==1.0.0 pydantic==2.6.0 pydantic-settings==2.2.1

:: Verify installation
echo Verifying installation...
python -c "import numpy; print(f'NumPy version: {numpy.__version__}')"
python -c "import fastapi; print(f'FastAPI version: {fastapi.__version__}')"

echo Setup complete! Activate the virtual environment with: venv\Scripts\activate
pause
