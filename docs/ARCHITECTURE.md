# Project Architecture

## System Overview

```mermaid
flowchart TB
    subgraph Client["Client Layer"]
        Browser["Browser (Bootstrap 5 + Chart.js)"]
        WSClient["WebSocket Client"]
        APIClient["API Client"]
    end

    subgraph Server["Django Application"]
        URLs["URL Router"]
        Auth["Accounts App"]
        Rooms["Rooms App"]
        Monitor["Monitoring App"]
        Analytics["Analytics App"]
        Reports["Reports App"]
        API["API App (DRF)"]
        Admin["Django Admin"]
    end

    subgraph Services["Service Layer"]
        GasSim["GasSimulationService"]
        Dashboard["DashboardService"]
        EmailSvc["Email Service"]
        PDFSvc["PDFReportService"]
        AnalyticsSvc["AnalyticsService"]
    end

    subgraph RealTime["Real-Time Layer"]
        Channels["Django Channels"]
        Consumer["GasMonitoringConsumer"]
        ChannelLayer["Channel Layer (Redis / InMemory)"]
    end

    subgraph Data["Data Layer"]
        PG["PostgreSQL"]
    end

    subgraph External["External"]
        SMTP["SMTP Server"]
        Redis["Redis"]
    end

    Browser --> URLs
    WSClient --> Consumer
    APIClient --> API
    URLs --> Auth
    URLs --> Rooms
    URLs --> Monitor
    URLs --> Analytics
    URLs --> Reports
    URLs --> API
    URLs --> Admin

    Monitor --> GasSim
    Monitor --> Dashboard
    GasSim --> EmailSvc
    GasSim --> Channels
    Reports --> PDFSvc
    Analytics --> AnalyticsSvc
    API --> AnalyticsSvc
    API --> Dashboard

    Consumer --> ChannelLayer
    ChannelLayer --> Redis
    GasSim --> PG
    Auth --> PG
    Rooms --> PG
    Monitor --> PG
    EmailSvc --> SMTP
```

## Application Modules

| App | Responsibility |
|-----|----------------|
| `apps.core` | Landing page, seed data command |
| `apps.accounts` | User registration, login, profile, password |
| `apps.rooms` | Room CRUD (name, description, created date) |
| `apps.monitoring` | GasReading, Alert models, simulation engine, dashboard, WebSockets |
| `apps.analytics` | Statistical analysis and Chart.js views |
| `apps.api` | REST API serializers, viewsets, routers |
| `apps.reports` | ReportLab PDF generation |

## Request Flow — Gas Simulation

```mermaid
sequenceDiagram
    participant CMD as run_gas_simulation
    participant SVC as GasSimulationService
    participant DB as PostgreSQL
    participant WS as WebSocket Consumer
    participant Email as Email Service
    participant Browser as Dashboard

    loop Every 5 seconds
        CMD->>SVC: process_all_rooms()
        SVC->>SVC: generate_gas_level()
        SVC->>DB: Save GasReading
        alt Level > 70
            SVC->>DB: Create Alert
            SVC->>Email: send_danger_alert_email()
        end
        SVC->>WS: Broadcast gas_update
        WS->>Browser: Live JSON update
    end
```

## Settings Architecture

```
config/settings/
├── base.py          # Shared: DB, DRF, Channels, email, thresholds
├── development.py   # DEBUG=True, InMemory channel layer
└── production.py    # Security headers, SMTP, Redis channel layer
```

## Deployment Topology (Production)

```mermaid
flowchart LR
    Nginx["Nginx / Reverse Proxy"]
    Daphne["Daphne ASGI"]
    PG["PostgreSQL"]
    Redis["Redis"]
    Worker["Simulation Worker"]

    Nginx --> Daphne
    Daphne --> PG
    Daphne --> Redis
    Worker --> PG
    Worker --> Redis
```

## Security

- All monitoring, room, analytics, and report routes require authentication (`LoginRequiredMixin`)
- API uses `IsAuthenticated` permission
- CSRF protection on all forms
- Production settings enforce HSTS, secure cookies, strict CORS
