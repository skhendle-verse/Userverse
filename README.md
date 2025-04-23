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
├── docs
│   └── images
├── scripts
│   └── versions
└── tests
```

### database
    - Initialization and session management for the database (e.g. engine setup, session factory).

### logic
    - services: Business logic and use-case implementations (e.g. user registration, OTP flows).
    - repositories: Data-access layer abstracting CRUD operations and queries.

### middleware
    - Custom FastAPI/Starlette middleware (CORS, logging, error handling).

### models
    - Pyndatic models defining API schema entities.

### routers/API 
    - Route definitions grouped by resource (e.g. auth.py, users.py).

### security
    - Authentication/authorization utilities (JWT, password hashing, token refresh).

### utils/Shared 
    - Helper functions and integrations (email, OTP generation, etc.).

## docs
    - Diagrams and visuals supporting documentation.

## tests
    - Unit and integration tests mirroring the app/ structure.