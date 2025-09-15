@echo off
echo Setting up Python environment...

:: Check Python version
python --version

:: Create virtual environment with Python 3.10
echo Creating virtual environment...
python -m venv --python=python3.10 venv

:: Activate virtual environment
call venv\Scripts\activate

:: Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip setuptools wheel

:: Install NumPy with pre-built wheel
echo Installing NumPy...
pip install numpy==1.24.3

:: Install core dependencies
echo Installing core dependencies...
pip install fastapi==0.104.1
pip install uvicorn[standard]==0.24.0
pip install neo4j==5.14.1
pip install python-jose[cryptography]==3.3.0
pip install passlib[bcrypt]==1.7.4
pip install python-multipart==0.0.6
pip install python-dotenv==1.0.0
pip install pydantic==2.5.0
pip install pydantic-settings==2.1.0

:: Verify installation
echo Verifying installation...
python -c "import numpy; print(f'NumPy version: {numpy.__version__}')"
python -c "import fastapi; print(f'FastAPI version: {fastapi.__version__}')"

echo Setup complete! Activate the virtual environment with: venv\Scripts\activate
pause
