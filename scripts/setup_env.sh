#!/usr/bin/env bash
# Smart Gas Monitoring System — Module 1 environment setup (Linux / macOS)
# Run from project root:  bash scripts/setup_env.sh

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo "=== Smart Gas Monitoring — Module 1 Setup ==="
echo "Project root: $PROJECT_ROOT"

if ! command -v python3 &>/dev/null; then
    echo "ERROR: python3 is not installed. Install Python 3.10+ first."
    exit 1
fi

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
else
    echo "Virtual environment already exists."
fi

# shellcheck source=/dev/null
source venv/bin/activate

echo "Upgrading pip..."
python -m pip install --upgrade pip

echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "Created .env from .env.example — update DB_PASSWORD and SECRET_KEY."
else
    echo ".env already exists."
fi

echo ""
echo "=== Setup complete ==="
echo ""
echo "Next steps:"
echo "  1. Install PostgreSQL and create database (see scripts/create_db.sql)"
echo "  2. Edit .env with your PostgreSQL credentials"
echo "  3. Activate venv:  source venv/bin/activate"
echo "  4. Run migrations:  python manage.py migrate"
echo "  5. Start server:    python manage.py runserver"
echo ""
