@echo off
echo Installing Python dependencies with pre-built binaries...

:: Upgrade pip
echo Upgrading pip, setuptools, and wheel...
python -m pip install --upgrade pip setuptools wheel

:: Install NumPy first with pre-built binaries
echo Installing NumPy...
pip install numpy==1.26.4 --only-binary=:all:

:: Install other packages from minimal requirements
echo Installing core dependencies...
pip install -r requirements-minimal.txt

echo Installation complete!
pause
