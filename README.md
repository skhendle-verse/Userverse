
[![Build Status](https://github.com/skhendle-verse/Userverse/actions/workflows/testing-build.yml/badge.svg)](https://github.com/skhendle-verse/Userverse/actions/workflows/testing-build.yml)
[![codecov](https://codecov.io/gh/skhendle-verse/Userverse/branch/main/graph/badge.svg)](https://codecov.io/gh/skhendle-verse/Userverse)


# Userverse

Userverse is an open-source platform designed to make managing users, organizations, and their relationships simple and efficient. It’s built for developers, communities, and organizations who want a free, flexible, and secure way to handle user and organization management without relying on closed or proprietary systems.

## Directory Overview

```bash
├── alembic
│   └── versions
├── app
│   ├── database
│   ├── logic
│   │   └── user
│   │       └── repository
│   ├── middleware
│   ├── models
│   │   └── user
│   ├── routers
│   │   └── user
│   ├── security
│   └── utils
├── coverage_reports
├── docs
│   └── images
├── scripts
│   └── versions
└── tests
    ├── data
    │   ├── database
    │   └── http
    ├── database
    ├── http
    │   └── user
    └── utils
```

### Database
 - Database initialization, connection management, and session handling (engine setup, session factory)
### Logic
 - Services: Core business logic implementation (user registration, authentication flows)
 - Repositories: Data access layer for database operations with clean abstractions
### Middleware
 - Request/response processing components (CORS configuration, logging, error handlers)
### Models
 - Pydantic schema definitions for data validation and API documentation

### Routers
 - API endpoint definitions organized by resource domain (users, auth, etc.)

### Security
 - Authentication mechanisms and authorization controls (JWT, password hashing)
### Utils
 - Shared helper functions and third-party integrations (email, OTP generation)

### Docs
 - Technical documentation assets including diagrams and implementation guides

### Tests
 - Comprehensive test suite mirroring application structure for unit and integration testing