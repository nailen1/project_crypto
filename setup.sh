#!/bin/bash

# setup.sh
echo "🚀 Starting crypto-etl development environment setup..."

# 1. Create virtual environment
echo "📦 Creating Python virtual environment..."
python3 -m venv .env-crypto

# 2. Activate virtual environment
echo "✅ Activating virtual environment..."
source .env-crypto/bin/activate

# 3. Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# 4. Install packages
echo "📚 Installing packages..."
pip install -r requirements.txt

# 5. Create necessary data folders
echo "📂 Creating data folders..."
mkdir -p data/dataset-binance

echo "✨ Setup completed!"
echo ""
echo "To activate virtual environment:"
echo "  source .env-crypto/bin/activate"