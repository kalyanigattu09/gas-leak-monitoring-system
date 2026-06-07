# Module 1 — Project Setup Guide

Smart Gas Leakage Monitoring and Alert Simulation System

---

## Folder Structure

```
Gas project/
├── apps/                          # All Django applications
│   ├── __init__.py
│   └── core/                      # Core app (landing page, shared utilities)
│       ├── __init__.py
│       ├── apps.py
│       ├── urls.py
│       └── views.py
├── config/                        # Project configuration package
│   ├── __init__.py
│   ├── asgi.py                    # ASGI entry (WebSockets in Module 8)
│   ├── urls.py                    # Root URL configuration
│   ├── wsgi.py                    # WSGI entry
│   └── settings/
│       ├── __init__.py
│       ├── base.py                # Shared settings (PostgreSQL, DRF, Channels)
│       ├── development.py         # Local development overrides
│       └── production.py          # Production security overrides
├── logs/                          # Application log files
├── media/                         # User-uploaded files
├── scripts/
│   ├── create_db.sql              # PostgreSQL setup (Windows locale)
│   ├── create_db_portable.sql     # PostgreSQL setup (cross-platform)
│   ├── setup_env.ps1              # Windows virtual env + install script
│   └── setup_env.sh               # Linux/macOS virtual env + install script
├── static/
│   ├── css/
│   │   └── main.css
│   └── js/
├── staticfiles/                   # Collected static files (generated)
├── templates/
│   ├── base.html                  # Bootstrap 5 base layout
│   └── home.html                  # Module 1 verification page
├── .env.example                   # Environment variable template
├── .gitignore
├── manage.py                      # Django management CLI
└── requirements.txt               # Python dependencies
```

---

## Prerequisites

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.10+ | Runtime |
| PostgreSQL | 14+ | Database |
| Redis | 6+ | WebSockets (Module 8; optional for Module 1) |
| Git | Any | Version control |

---

## Step 1 — Virtual Environment & Dependencies

### Windows (PowerShell)

```powershell
cd "C:\Users\kalya\OneDrive\Projects-3rd year\Gas project"
.\scripts\setup_env.ps1
```

**What this does:**
- Finds Python 3 on your system
- Creates a `venv/` folder
- Activates the virtual environment
- Upgrades `pip`
- Installs all packages from `requirements.txt`
- Copies `.env.example` → `.env` if `.env` does not exist

### Manual setup (all platforms)

```powershell
# Create virtual environment
python -m venv venv

# Activate (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Activate (Linux/macOS)
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create environment file
copy .env.example .env        # Windows
cp .env.example .env          # Linux/macOS
```

---

## Step 2 — PostgreSQL Database

### Install PostgreSQL

Download from https://www.postgresql.org/download/ and install with default options.
Remember the `postgres` superuser password you set during installation.

### Create the database

**Option A — pgAdmin:** Create a database named `smart_gas_db`.

**Option B — psql command line:**

```powershell
psql -U postgres -f scripts/create_db_portable.sql
```

**Option C — Windows-specific script:**

```powershell
psql -U postgres -f scripts/create_db.sql
```

---

## Step 3 — Configure Environment Variables

Edit `.env` in the project root:

```env
SECRET_KEY=your-long-random-secret-key-here
DEBUG=True
DB_NAME=smart_gas_db
DB_USER=postgres
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432
```

Generate a secret key:

```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## Step 4 — Run Migrations & Start Server

```powershell
# Activate venv (if not already active)
.\venv\Scripts\Activate.ps1

# Apply database migrations
python manage.py migrate

# Create admin superuser (optional, for Django admin)
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

Open http://127.0.0.1:8000/ — you should see the **Smart Gas Leakage Monitoring** landing page.

---

## Step 5 — Verify Installation

```powershell
# Check Django configuration
python manage.py check

# List installed apps
python manage.py diffsettings | findstr INSTALLED_APPS

# Test database connection
python manage.py dbshell
```

---

## Installed Packages (requirements.txt)

| Package | Purpose |
|---------|---------|
| Django 5.x | Web framework |
| djangorestframework | REST APIs (Module 7) |
| django-cors-headers | CORS for API clients |
| django-environ | Environment variable management |
| psycopg2-binary | PostgreSQL adapter |
| channels + channels-redis + daphne | WebSockets (Module 8) |
| reportlab | PDF reports (Module 11) |
| Pillow | Image support |

---

## Settings Overview

| Setting | File | Description |
|---------|------|-------------|
| `DATABASES` | `base.py` | PostgreSQL connection via `.env` |
| `REST_FRAMEWORK` | `base.py` | DRF defaults (auth, pagination) |
| `CHANNEL_LAYERS` | `base.py` | Redis for WebSockets |
| `GAS_LEVEL_*` | `base.py` | Threshold constants (Module 5) |
| `DEBUG = True` | `development.py` | Development mode |
| Security headers | `production.py` | HSTS, secure cookies |

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `Python was not found` | Install Python 3.10+ and enable "Add to PATH" |
| `FATAL: password authentication failed` | Check `DB_PASSWORD` in `.env` |
| `database "smart_gas_db" does not exist` | Run `scripts/create_db_portable.sql` |
| `ModuleNotFoundError: No module named 'django'` | Activate venv before running commands |
| Port 8000 in use | Run `python manage.py runserver 8001` |

---

**Module 1 complete.** Confirm when ready to proceed to **Module 2: Authentication System**.
