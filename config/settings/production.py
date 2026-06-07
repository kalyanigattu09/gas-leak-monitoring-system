"""
Production settings — secure defaults for deployment.
"""
from .base import *  # noqa: F401, F403

DEBUG = False
ALLOWED_HOSTS = ['gas-leak-monitoring-system.onrender.com', '*']

# Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Use strict CORS in production
CORS_ALLOW_ALL_ORIGINS = False

# Production email backend (override via environment)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
