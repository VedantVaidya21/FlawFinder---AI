@echo off
echo Setting up Python 3.10 environment...

:: Clean up any existing virtual environment
if exist venv (
    echo Removing existing virtual environment...
    rmdir /s /q venv
)

:: Create fresh virtual environment with Python 3.10
echo Creating new virtual environment...
py -3.10 -m venv venv

:: Activate virtual environment
call venv\Scripts\activate

:: Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip setuptools wheel

:: Install NumPy
echo Installing NumPy...
pip install numpy==1.23.5

:: Install core dependencies
echo Installing core dependencies...
pip install fastapi==0.95.2 uvicorn[standard]==0.22.0
pip install neo4j==5.9.0
pip install python-jose[cryptography]==3.3.0 passlib[bcrypt]==1.7.4
pip install python-multipart==0.0.6 python-dotenv==1.0.0
pip install pydantic==1.10.7 pydantic-settings==2.0.3

:: Verify installation
echo Verifying installation...
python -c "import numpy; print(f'NumPy version: {numpy.__version__}')"
python -c "import fastapi; print(f'FastAPI version: {fastapi.__version__}')"

echo Setup complete! Activate the virtual environment with: venv\Scripts\activate
pause
