# Smart Gas Leakage Monitoring and Alert Simulation System

A production-quality Django application that simulates gas sensor readings, classifies danger levels, sends real-time WebSocket notifications and email alerts, and provides analytics dashboards with PDF reporting.

---

## Features

- **Gas Simulation** — Random readings every 5 seconds for all rooms
- **Status Classification** — SAFE (0–40), WARNING (41–70), DANGER (71–100)
- **Real-Time Monitoring** — Django Channels WebSocket live updates
- **Email Alerts** — Automatic notifications when level exceeds 70
- **REST API** — Full CRUD for rooms, readings, alerts, and analytics
- **Analytics** — Chart.js line, bar, and pie charts
- **PDF Reports** — ReportLab-generated room and system reports
- **Authentication** — Registration, login, profile, password change
- **Admin Dashboard** — Customized Django admin with statistics

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 5, Python 3.10+ |
| Database | PostgreSQL 14+ |
| API | Django REST Framework |
| WebSockets | Django Channels + Redis (InMemory in dev) |
| Frontend | Bootstrap 5, Chart.js |
| PDF | ReportLab |
| Email | Django mail (console in dev, SMTP in production) |

---

## Quick Start

### 1. Prerequisites

- Python 3.10+
- PostgreSQL 14+
- Redis 6+ (optional in development — uses InMemory channel layer)

### 2. Setup

```powershell
cd "C:\Users\kalya\OneDrive\Projects-3rd year\Gas project"

# Automated setup (Windows)
.\scripts\setup_env.ps1

# Or manual setup
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

### 3. PostgreSQL

```powershell
psql -U postgres -f scripts/create_db_portable.sql
```

Edit `.env` with your database credentials and a secure `SECRET_KEY`.

### 4. Migrate & Seed

```powershell
python manage.py migrate
python manage.py seed_sample_data
python manage.py createsuperuser
```

### 5. Run the Application

**Terminal 1 — ASGI server (required for WebSockets):**

```powershell
daphne -b 0.0.0.0 -p 8000 config.asgi:application
```

**Terminal 2 — Gas simulation:**

```powershell
python manage.py run_gas_simulation
```

Open http://127.0.0.1:8000/ → Register → Dashboard.

> **Note:** Use `daphne` instead of `runserver` for WebSocket support. For HTTP-only testing, `python manage.py runserver` works but WebSockets will not connect.

---

## Project Structure

```
Gas project/
├── apps/
│   ├── accounts/       # Auth, profile, password change
│   ├── analytics/      # Analytics dashboard & Chart.js
│   ├── api/            # REST API (DRF ViewSets)
│   ├── core/           # Home page, seed command
│   ├── monitoring/     # Gas readings, alerts, simulation, WebSockets
│   ├── reports/        # PDF report generation
│   └── rooms/          # Room CRUD
├── config/             # Settings, URLs, ASGI, admin
├── docs/               # Architecture, API, schema docs
├── scripts/            # Setup & DB scripts
├── static/             # CSS, JavaScript
└── templates/          # Bootstrap 5 templates
```

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for the full architecture diagram.

---

## Gas Level Thresholds

| Range | Status | Action |
|-------|--------|--------|
| 0 – 40 | SAFE | Normal monitoring |
| 41 – 70 | WARNING | Elevated — monitor closely |
| 71 – 100 | DANGER | Alert created, email sent, WebSocket notification |

---

## Management Commands

| Command | Description |
|---------|-------------|
| `python manage.py run_gas_simulation` | Simulate readings every 5s |
| `python manage.py run_gas_simulation --once` | Single simulation cycle |
| `python manage.py seed_sample_data` | Create 5 sample rooms |

---

## API Endpoints

Base URL: `/api/v1/`

| Endpoint | Methods | Description |
|----------|---------|-------------|
| `/rooms/` | GET, POST, PUT, PATCH, DELETE | Room management |
| `/readings/` | GET | Gas readings (filter by room, status) |
| `/readings/latest/` | GET | Latest reading per room |
| `/alerts/` | GET, PATCH | Alert list and status update |
| `/analytics/summary/` | GET | Analytics summary |
| `/analytics/charts/` | GET | Chart.js data |
| `/analytics/dashboard/` | GET | Dashboard statistics |

Full documentation: [docs/API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md)

---

## WebSocket

Connect to: `ws://127.0.0.1:8000/ws/gas/`

Receives JSON messages:

```json
{
  "type": "gas_update",
  "reading": {
    "room_id": 1,
    "room_name": "Kitchen",
    "gas_level": 85,
    "status": "DANGER",
    "timestamp": "2026-06-07T12:00:00Z"
  },
  "alert": { ... }
}
```

---

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | — |
| `DEBUG` | Debug mode | `True` |
| `DB_NAME` | PostgreSQL database | `smart_gas_db` |
| `DB_USER` | Database user | `postgres` |
| `DB_PASSWORD` | Database password | — |
| `REDIS_URL` | Redis for Channels | `redis://127.0.0.1:6379/0` |
| `ALERT_ADMIN_EMAIL` | Alert recipient | Staff users |
| `EMAIL_*` | SMTP settings | Console backend |

---

## Testing Checklist

- [ ] Register and login at `/accounts/register/`
- [ ] Add rooms at `/rooms/add/`
- [ ] Run simulation: `python manage.py run_gas_simulation --once`
- [ ] View dashboard at `/monitoring/dashboard/`
- [ ] Verify WebSocket live updates (use daphne)
- [ ] Check alerts at `/monitoring/alerts/`
- [ ] View analytics at `/analytics/`
- [ ] Download PDF at `/reports/system/`
- [ ] Test API at `/api/v1/rooms/` (login required)
- [ ] Check email output in console when level > 70
- [ ] Admin panel at `/admin/`

---

## Documentation

- [Installation Guide](docs/MODULE_01_SETUP.md)
- [Architecture Diagram](docs/ARCHITECTURE.md)
- [Database Schema](docs/DATABASE_SCHEMA.md)
- [API Documentation](docs/API_DOCUMENTATION.md)

---

## License

Educational project — Smart Gas Leakage Monitoring and Alert Simulation System.
