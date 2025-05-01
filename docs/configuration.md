# 📘 Application Configuration Guide

This guide explains how to manage and load configuration for the **Userverse** backend API. Configuration can be supplied through two sources:

1. `pyproject.toml` (preferred)
2. `sample-config.json` (fallback)

---

## 🔧 Configuration Loader

The app uses a flexible `ConfigLoader` class that allows selecting a configuration source. If no source is specified, it attempts to load from `pyproject.toml`, and falls back to JSON if unavailable.

### ✅ Usage

```python
from config_loader import ConfigLoader

loader = ConfigLoader(source="toml")  # or "json"
config = loader.load()
```

---

## 1️⃣ `pyproject.toml` Format (Recommended)

Place your configuration under `[tool.userverse.config]`:

```toml
[tool.userverse.config]
environment = "production"
version = "1.0.0"
name = "Userverse"
description = "Userverse backend API"

[tool.userverse.config.database]
development = "sqlite:///dev.db"
production = "postgresql://user:pass@host:port/dbname"

[tool.userverse.config.jwt]
secret_key = "supersecret"
algorithm = "HS256"

[tool.userverse.config.email]
smtp_host = "smtp.mailserver.com"
smtp_port = 587
username = "no-reply@domain.com"
password = "emailpassword"

[tool.userverse.config.cor_origins]
allowed = ["https://yourdomain.com"]
blocked = ["http://localhost:3000"]
```

---

## 2️⃣ `sample-config.json` Format (Fallback)

A simplified JSON alternative with the same structure:

```json
{
  "environment": "development",
  "version": "1.0.0",
  "name": "Userverse",
  "description": "Userverse backend API",
  "database": {
    "development": "sqlite:///dev.db",
    "production": "postgresql://user:pass@host/db"
  },
  "jwt": {
    "secret_key": "supersecret",
    "algorithm": "HS256"
  },
  "email": {
    "smtp_host": "smtp.mailserver.com",
    "smtp_port": 587,
    "username": "no-reply@domain.com",
    "password": "emailpassword"
  },
  "cor_origins": {
    "allowed": ["https://yourdomain.com"],
    "blocked": ["http://localhost:3000"]
  }
}
```

---

## 📤 Extending

You can easily extend the config structure by updating the `_transform_config()` method in the `ConfigLoader` class to include new keys or sections as needed.