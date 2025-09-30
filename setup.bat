@echo off
REM Quick setup script for ROI.01 on Windows

echo ==================================
echo ROI.01 Setup Script
echo ==================================
echo.

REM Check Python version
echo Checking Python version...
python --version
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip
echo.

REM Install requirements
echo Installing dependencies...
pip install -r requirements.txt
echo.

REM Copy .env.example to .env if it doesn't exist
if not exist .env (
    echo Creating .env file...
    copy .env.example .env
    echo ✓ Created .env file
    echo.
    echo IMPORTANT: Edit .env and add your Odds API key!
    echo Get your key at: https://the-odds-api.com/
) else (
    echo .env file already exists
)

echo.
echo ==================================
echo Setup complete!
echo ==================================
echo.
echo Next steps:
echo 1. Get your free API key from https://the-odds-api.com/
echo 2. Edit the .env file and add your API key
echo 3. Run: python main.py
echo.
echo To activate the virtual environment later:
echo   venv\Scripts\activate
echo.
pause
