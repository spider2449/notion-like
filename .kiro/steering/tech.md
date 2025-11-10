# Technology Stack

## Backend

- **Python 3.11+** - Primary language
- **Flask 3.0.0** - Web framework
- **Flask-CORS 4.0.0** - Cross-origin resource sharing
- **SQLite 3** - Database
- **PyJWT 2.8.0** - JWT token handling
- **bcrypt 4.1.2** - Password hashing

## Frontend

- **Vanilla JavaScript (ES6+)** - No frameworks
- **HTML5** - Markup
- **CSS3** - Styling

## Common Commands

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Initialize database and seed data
python seed_data.py
```

### Running the Application
```bash
# Quick start (recommended)
python start.py

# Or run backend directly
python backend/app.py
```

### Database Management
```bash
# Initialize empty database
python backend/database.py

# Seed with test data
python seed_data.py

# Reset database (delete and recreate)
# Delete notion.db file, then run seed_data.py
```

### Admin Tools
```bash
# Make a user admin
python make_admin.py
```

## Development Server

- Runs on `http://localhost:5000`
- Debug mode enabled by default
- Auto-reload on code changes

## Test Credentials

- Username: `testuser`
- Password: `password123`
