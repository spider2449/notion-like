# Notion Clone

A Notion-like web application built with Python 3.11, JavaScript, and SQLite.

## Features

- **User Authentication**: Secure registration and login with JWT tokens
- **Document Management**: Create, edit, and organize documents in folders
- **Content Blocks**: Create different types of content blocks (paragraphs, headings, lists, code)
- **Block Type Switching**: Right-click on any block to change its type
- **Auto-save**: Content is automatically saved as you type
- **Hierarchical Navigation**: Organize documents in folders with multiple levels of nesting

## Installation

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)

### Setup

1. Clone the repository or extract the files

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Initialize the database and create seed data:
```bash
python seed_data.py
```

## Running the Application

1. Start the Flask backend server:
```bash
python backend/app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

3. Log in with the test credentials:
   - Username: `testuser`
   - Password: `password123`

## Project Structure

```
.
├── backend/
│   ├── models/          # Data models (User, Document, Folder, Block)
│   ├── repositories/    # Database access layer
│   ├── services/        # Business logic
│   ├── routes/          # API endpoints
│   ├── middleware/      # Authentication middleware
│   ├── utils/           # Utility functions (security)
│   ├── database.py      # Database connection and initialization
│   └── app.py           # Flask application entry point
├── frontend/
│   ├── html/            # HTML pages (login, register, app)
│   ├── css/             # Stylesheets
│   └── js/              # JavaScript modules
├── requirements.txt     # Python dependencies
├── seed_data.py        # Database seeding script
└── README.md           # This file
```

## Usage

### Creating Documents

1. Click "New Document" in the sidebar
2. Enter a document title
3. Click on the document to open it in the editor

### Creating Folders

1. Click "New Folder" in the sidebar
2. Enter a folder name
3. Drag documents into folders (or create documents directly in folders)

### Working with Blocks

- **Add Block**: Click the "+ Add Block" button at the bottom of the document
- **Edit Block**: Click on any block and start typing
- **Change Block Type**: Right-click on a block and select a new type
- **Delete Block**: Hover over a block and click the "Delete" button

### Block Types

- **Paragraph**: Regular text
- **Heading 1**: Large heading
- **Heading 2**: Medium heading
- **Heading 3**: Small heading
- **Bullet List**: Unordered list item
- **Numbered List**: Ordered list item
- **Code Block**: Monospace code formatting

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/logout` - Logout user

### Documents
- `GET /api/documents` - Get all documents and folders
- `POST /api/documents` - Create new document
- `PUT /api/documents/<id>` - Update document
- `DELETE /api/documents/<id>` - Delete document

### Folders
- `POST /api/folders` - Create new folder
- `DELETE /api/folders/<id>` - Delete folder

### Blocks
- `GET /api/documents/<id>/blocks` - Get document blocks
- `POST /api/blocks` - Create new block
- `PUT /api/blocks/<id>` - Update block
- `DELETE /api/blocks/<id>` - Delete block
- `PUT /api/documents/<id>/blocks/reorder` - Reorder blocks

## Security Features

- Password hashing with bcrypt (cost factor 12)
- JWT token-based authentication
- Input sanitization to prevent XSS attacks
- Parameterized SQL queries to prevent SQL injection
- Authorization checks on all protected endpoints
- CORS configuration

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Development

The application uses:
- **Backend**: Flask 3.0.0, Flask-CORS, PyJWT, bcrypt
- **Frontend**: Vanilla JavaScript (ES6+), HTML5, CSS3
- **Database**: SQLite 3

## License

This project is for educational purposes.
