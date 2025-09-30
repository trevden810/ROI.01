#!/bin/bash
# Quick setup script for ROI.01 on macOS/Linux

echo "=================================="
echo "ROI.01 Setup Script"
echo "=================================="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Copy .env.example to .env if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "Creating .env file..."
    cp .env.example .env
    echo "✓ Created .env file"
    echo ""
    echo "IMPORTANT: Edit .env and add your Odds API key!"
    echo "Get your key at: https://the-odds-api.com/"
else
    echo ""
    echo ".env file already exists"
fi

echo ""
echo "=================================="
echo "Setup complete!"
echo "=================================="
echo ""
echo "Next steps:"
echo "1. Get your free API key from https://the-odds-api.com/"
echo "2. Edit the .env file and add your API key"
echo "3. Run: python main.py"
echo ""
echo "To activate the virtual environment later:"
echo "  source venv/bin/activate"
echo ""
