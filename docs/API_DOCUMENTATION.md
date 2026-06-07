# API Documentation

Base URL: `http://127.0.0.1:8000/api/v1/`

Authentication: **Session Authentication** (login via browser or session cookie)

All endpoints require an authenticated user unless noted.

---

## Authentication

Login via Django session:

```
POST /accounts/login/
Content-Type: application/x-www-form-urlencoded

username=youruser&password=yourpass&csrfmiddlewaretoken=...
```

Or use the browsable API at `/api/v1/` after logging in through the web interface.

---

## Rooms

### List Rooms

```
GET /api/v1/rooms/
```

**Response 200:**

```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Kitchen",
      "description": "Main kitchen area",
      "created_at": "2026-06-07T10:00:00Z",
      "current_gas_level": 35,
      "current_status": "SAFE"
    }
  ]
}
```

**Query Parameters:**

| Param | Description |
|-------|-------------|
| `search` | Search by room name |
| `ordering` | `name`, `-name`, `created_at`, `-created_at` |
| `page` | Page number |

### Create Room

```
POST /api/v1/rooms/
Content-Type: application/json

{
  "name": "Garage",
  "description": "Attached garage"
}
```

### Retrieve Room

```
GET /api/v1/rooms/{id}/
```

### Update Room

```
PUT /api/v1/rooms/{id}/
PATCH /api/v1/rooms/{id}/
```

### Delete Room

```
DELETE /api/v1/rooms/{id}/
```

---

## Gas Readings

### List Readings

```
GET /api/v1/readings/
```

**Query Parameters:**

| Param | Description |
|-------|-------------|
| `room` | Filter by room ID |
| `status` | SAFE, WARNING, or DANGER |
| `ordering` | `timestamp`, `-timestamp`, `gas_level`, `-gas_level` |
| `page` | Page number |

**Response 200:**

```json
{
  "count": 100,
  "results": [
    {
      "id": 42,
      "room": 1,
      "room_name": "Kitchen",
      "gas_level": 85,
      "status": "DANGER",
      "timestamp": "2026-06-07T12:00:00Z"
    }
  ]
}
```

### Latest Readings (All Rooms)

```
GET /api/v1/readings/latest/
```

Returns the most recent reading for each room.

**Response 200:**

```json
[
  {
    "id": 42,
    "room": 1,
    "room_name": "Kitchen",
    "gas_level": 85,
    "status": "DANGER",
    "timestamp": "2026-06-07T12:00:00Z"
  }
]
```

### Retrieve Reading

```
GET /api/v1/readings/{id}/
```

---

## Alerts

### List Alerts

```
GET /api/v1/alerts/
```

**Query Parameters:**

| Param | Description |
|-------|-------------|
| `room` | Filter by room ID |
| `status` | ACTIVE or RESOLVED |
| `ordering` | `timestamp`, `-timestamp`, `level`, `-level` |

**Response 200:**

```json
{
  "count": 5,
  "results": [
    {
      "id": 1,
      "room": 1,
      "room_name": "Kitchen",
      "level": 85,
      "message": "DANGER: Gas level 85 detected in Kitchen...",
      "status": "ACTIVE",
      "timestamp": "2026-06-07T12:00:00Z"
    }
  ]
}
```

### Update Alert Status

```
PATCH /api/v1/alerts/{id}/
Content-Type: application/json

{
  "status": "RESOLVED"
}
```

---

## Analytics

### Summary

```
GET /api/v1/analytics/summary/
```

**Response 200:**

```json
{
  "daily_average": 42.5,
  "weekly_average": 38.2,
  "monthly_average": 35.0,
  "peak_reading": 98,
  "alert_count": 12,
  "total_readings": 1500,
  "room_comparison": [
    {
      "room_id": 1,
      "room_name": "Kitchen",
      "average": 45.2,
      "peak": 98,
      "reading_count": 300
    }
  ]
}
```

### Chart Data

```
GET /api/v1/analytics/charts/
```

**Response 200:**

```json
{
  "line_chart": {
    "labels": ["Mon 01", "Tue 02", "..."],
    "values": [35.2, 42.1, 38.5]
  },
  "pie_chart": {
    "labels": ["SAFE", "WARNING", "DANGER"],
    "values": [800, 500, 200]
  },
  "bar_chart": {
    "labels": ["Kitchen", "Living Room"],
    "values": [98, 76]
  }
}
```

### Dashboard Stats

```
GET /api/v1/analytics/dashboard/
```

**Response 200:**

```json
{
  "total_rooms": 5,
  "total_alerts": 3,
  "peak_reading": 98,
  "average_reading": 42.5,
  "status_counts": {
    "SAFE": 800,
    "WARNING": 500,
    "DANGER": 200
  }
}
```

---

## WebSocket API

**Endpoint:** `ws://127.0.0.1:8000/ws/gas/`

No authentication required in development. Receives broadcast messages when simulation runs.

**Message format:**

```json
{
  "type": "gas_update",
  "reading": {
    "room_id": 1,
    "room_name": "Kitchen",
    "gas_level": 85,
    "status": "DANGER",
    "timestamp": "2026-06-07T12:00:00.000000+00:00"
  },
  "alert": {
    "id": 10,
    "room_id": 1,
    "room_name": "Kitchen",
    "level": 85,
    "message": "DANGER: Gas level 85 detected...",
    "status": "ACTIVE",
    "timestamp": "2026-06-07T12:00:00.000000+00:00"
  }
}
```

The `alert` field is only present when gas level exceeds 70.

---

## Error Responses

| Code | Meaning |
|------|---------|
| 401 | Not authenticated |
| 403 | Permission denied |
| 404 | Resource not found |
| 400 | Validation error |

**Example 400:**

```json
{
  "name": ["room with this name already exists."]
}
```

---

## Browsable API

Visit http://127.0.0.1:8000/api/v1/ after logging in for an interactive API explorer provided by Django REST Framework.
