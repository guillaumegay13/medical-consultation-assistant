#!/bin/bash

# Exit on error
set -e

# Default port if not set in environment
export PORT=${PORT:-8000}

echo "🏗️ Building frontend..."
cd frontend
npm install
npm run build
cd ..

echo "🐍 Setting up Python environment..."
cd backend
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt

echo "🚀 Starting server on port $PORT..."
python app.py 