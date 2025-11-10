# Project Structure

## Architecture Pattern

Layered architecture with clear separation of concerns:

```
Routes → Services → Repositories → Database
  ↓         ↓            ↓
Models ← Models ←  Models
```

## Backend Organization

### `/backend`

- **`app.py`** - Flask application entry point, blueprint registration, static file routes
- **`database.py`** - Database connection management, schema initialization, context managers

### `/backend/models`
Data models representing domain entities. Each model:
- Has a `to_dict()` method for JSON serialization
- Has a `from_row()` static method for database row conversion
- Excludes sensitive data (like password_hash) from `to_dict()`

### `/backend/repositories`
Data access layer. Repositories:
- Use parameterized queries exclusively (SQL injection prevention)
- Use `get_db()` context manager for automatic commit/rollback
- Return model instances, not raw database rows
- Handle all database operations for their entity

### `/backend/services`
Business logic layer. Services:
- Validate input data
- Sanitize user inputs
- Coordinate between repositories
- Implement authentication/authorization logic
- Raise `ValueError` for validation errors

### `/backend/routes`
API endpoints (Flask blueprints). Routes:
- Handle HTTP request/response
- Validate required fields
- Call service methods
- Return JSON responses with appropriate status codes
- Use try/except for error handling
- Return 400 for validation errors, 401 for auth errors, 500 for server errors

### `/backend/middleware`
Request interceptors:
- **`auth_middleware.py`** - JWT token verification, user authentication
- **`admin_middleware.py`** - Admin role verification

### `/backend/utils`
Utility functions:
- **`security.py`** - Input sanitization, validation helpers

### `/backend/migrations`
Database schema migration scripts

## Frontend Organization

### `/frontend/html`
HTML pages for each view (login, register, app, account, admin)

### `/frontend/css`
Stylesheets matching HTML pages

### `/frontend/js`
JavaScript modules:
- **`api-client.js`** - HTTP client for backend API calls
- **`auth.js`** - Authentication logic
- **`app.js`** - Main application logic
- **`editor.js`** - Block editor functionality
- **`navigation.js`** - Document tree navigation
- **`context-menu.js`** - Right-click menu for blocks
- **`theme.js`** - Theme management
- **`account.js`** - Account settings
- **`admin.js`** - Admin panel

## Database

- **`notion.db`** - SQLite database file (not in version control)
- Tables: users, folders, documents, blocks
- Foreign keys enabled with CASCADE/SET NULL
- Indexes on foreign keys and frequently queried columns

## Root Files

- **`start.py`** - Quick start script (initializes DB and starts server)
- **`seed_data.py`** - Database seeding with test data
- **`make_admin.py`** - Utility to grant admin privileges
- **`requirements.txt`** - Python dependencies

## Naming Conventions

- **Python**: snake_case for files, functions, variables
- **Classes**: PascalCase
- **JavaScript**: camelCase for functions and variables
- **Files**: kebab-case for multi-word files (e.g., `api-client.js`)
- **Database**: snake_case for tables and columns
