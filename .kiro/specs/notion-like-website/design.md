# Design Document

## Overview

The Notion-like web application will follow a client-server architecture with a Python Flask backend serving a REST API and a vanilla JavaScript frontend. The system uses SQLite for data persistence and implements real-time content saving with debouncing. The architecture emphasizes simplicity, maintainability, and clear separation of concerns between the presentation layer, business logic, and data access layer.

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────┐
│         Frontend (JavaScript)            │
│  ┌────────────┐  ┌──────────────────┐  │
│  │ UI Layer   │  │  API Client      │  │
│  │ - Editor   │  │  - HTTP Requests │  │
│  │ - Nav Tree │  │  - Auth Tokens   │  │
│  │ - Context  │  │                  │  │
│  └────────────┘  └──────────────────┘  │
└─────────────────────────────────────────┘
                    │
                    │ HTTPS/REST API
                    ▼
┌─────────────────────────────────────────┐
│       Backend (Python 3.11/Flask)       │
│  ┌────────────┐  ┌──────────────────┐  │
│  │ API Routes │  │  Services        │  │
│  │ - Auth     │  │  - User Service  │  │
│  │ - Blocks   │  │  - Block Service │  │
│  │ - Docs     │  │  - Doc Service   │  │
│  └────────────┘  └──────────────────┘  │
│         │                  │            │
│         └──────┬───────────┘            │
│                ▼                        │
│  ┌──────────────────────────────────┐  │
│  │      Repository Layer            │  │
│  │  - User Repository               │  │
│  │  - Block Repository              │  │
│  │  - Document Repository           │  │
│  └──────────────────────────────────┘  │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│          SQLite Database                │
│  - users                                │
│  - documents                            │
│  - blocks                               │
│  - folders                              │
└─────────────────────────────────────────┘
```

### Technology Stack

- **Backend**: Python 3.11 with Flask framework
- **Frontend**: Vanilla JavaScript (ES6+), HTML5, CSS3
- **Database**: SQLite 3
- **Authentication**: JWT (JSON Web Tokens) with bcrypt password hashing
- **API**: RESTful JSON API

## Components and Interfaces

### Backend Components

#### 1. Authentication Module
- **Purpose**: Handle user registration, login, and session management
- **Key Functions**:
  - `register_user(username, email, password)`: Create new user account
  - `authenticate_user(email, password)`: Validate credentials and issue JWT
  - `verify_token(token)`: Validate JWT and extract user identity
- **Dependencies**: User Repository, bcrypt, JWT library

#### 2. Block Service
- **Purpose**: Manage content block operations
- **Key Functions**:
  - `create_block(document_id, content, block_type, order)`: Create new block
  - `update_block(block_id, content, block_type)`: Update existing block
  - `delete_block(block_id)`: Remove block
  - `get_blocks_by_document(document_id)`: Retrieve all blocks for a document
  - `reorder_blocks(document_id, block_order_list)`: Update block ordering
- **Dependencies**: Block Repository

#### 3. Document Service
- **Purpose**: Manage documents and folder structure
- **Key Functions**:
  - `create_document(user_id, title, parent_folder_id)`: Create new document
  - `get_user_documents(user_id)`: Retrieve user's document tree
  - `update_document(document_id, title, parent_folder_id)`: Update document metadata
  - `delete_document(document_id)`: Remove document and its blocks
  - `create_folder(user_id, name, parent_folder_id)`: Create folder
- **Dependencies**: Document Repository, Block Repository

#### 4. API Routes
- **Authentication Routes**:
  - `POST /api/auth/register`: User registration
  - `POST /api/auth/login`: User login
  - `POST /api/auth/logout`: User logout
- **Document Routes**:
  - `GET /api/documents`: Get user's documents
  - `POST /api/documents`: Create new document
  - `PUT /api/documents/<id>`: Update document
  - `DELETE /api/documents/<id>`: Delete document
  - `POST /api/folders`: Create folder
- **Block Routes**:
  - `GET /api/documents/<id>/blocks`: Get document blocks
  - `POST /api/blocks`: Create block
  - `PUT /api/blocks/<id>`: Update block
  - `DELETE /api/blocks/<id>`: Delete block
  - `PUT /api/documents/<id>/blocks/reorder`: Reorder blocks

### Frontend Components

#### 1. Authentication UI
- **Purpose**: Login and registration forms
- **Key Elements**:
  - Login form with email/password
  - Registration form with username/email/password
  - Token storage in localStorage
  - Automatic token inclusion in API requests

#### 2. Navigation Panel
- **Purpose**: Display and interact with document/folder tree
- **Key Features**:
  - Hierarchical tree view
  - Expand/collapse folders
  - Click to open documents
  - Create new documents/folders
  - Delete documents/folders
- **State Management**: Maintains current document selection

#### 3. Editor Component
- **Purpose**: Display and edit content blocks
- **Key Features**:
  - Render blocks with appropriate styling
  - Inline editing with contenteditable
  - Auto-save with debouncing (1 second delay)
  - Add new blocks
  - Delete blocks
  - Drag-and-drop reordering (optional enhancement)

#### 4. Context Menu Component
- **Purpose**: Block type switching interface
- **Key Features**:
  - Right-click detection on blocks
  - Display menu with block type options
  - Apply type change and update styling
  - Close on selection or outside click

#### 5. API Client
- **Purpose**: Centralized HTTP communication
- **Key Functions**:
  - `request(method, endpoint, data)`: Generic API request with auth headers
  - Error handling and response parsing
  - Token refresh logic

## Data Models

### Database Schema

#### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Folders Table
```sql
CREATE TABLE folders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    parent_folder_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (parent_folder_id) REFERENCES folders(id) ON DELETE CASCADE
);
```

#### Documents Table
```sql
CREATE TABLE documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    folder_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (folder_id) REFERENCES folders(id) ON DELETE SET NULL
);
```

#### Blocks Table
```sql
CREATE TABLE blocks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_id INTEGER NOT NULL,
    content TEXT NOT NULL DEFAULT '',
    block_type TEXT NOT NULL DEFAULT 'paragraph',
    order_index INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE
);
```

### Block Types

Supported block types with their rendering characteristics:
- `paragraph`: Regular text block
- `heading1`: Large heading (h1)
- `heading2`: Medium heading (h2)
- `heading3`: Small heading (h3)
- `bullet_list`: Unordered list item
- `numbered_list`: Ordered list item
- `code`: Monospace code block

## Error Handling

### Backend Error Handling

1. **Authentication Errors**:
   - Invalid credentials: Return 401 with error message
   - Expired token: Return 401 with "Token expired" message
   - Missing token: Return 401 with "Authentication required" message

2. **Authorization Errors**:
   - User accessing another user's resources: Return 403 Forbidden

3. **Validation Errors**:
   - Invalid input data: Return 400 with specific validation errors
   - Missing required fields: Return 400 with field names

4. **Database Errors**:
   - Connection failures: Return 500 with generic error message
   - Constraint violations: Return 409 Conflict
   - Log detailed errors server-side for debugging

5. **Not Found Errors**:
   - Resource doesn't exist: Return 404 with resource type

### Frontend Error Handling

1. **Network Errors**:
   - Display user-friendly message: "Connection error. Please check your internet."
   - Retry mechanism for failed saves

2. **Authentication Errors**:
   - Redirect to login page on 401
   - Clear stored tokens

3. **Validation Errors**:
   - Display inline error messages near form fields
   - Prevent form submission until valid

4. **Loading States**:
   - Show spinner for operations > 500ms
   - Disable UI elements during operations to prevent duplicate requests

## Testing Strategy

### Backend Testing

1. **Unit Tests**:
   - Test each service function in isolation
   - Mock repository layer
   - Test authentication logic (password hashing, token generation)
   - Test business logic (block ordering, document hierarchy)

2. **Integration Tests**:
   - Test API endpoints with test database
   - Verify request/response formats
   - Test authentication flow end-to-end
   - Test database operations

3. **Database Tests**:
   - Verify schema constraints
   - Test cascade deletes
   - Test foreign key relationships

### Frontend Testing

1. **Manual Testing**:
   - Test user flows (registration, login, document creation)
   - Test block type switching
   - Test navigation tree interactions
   - Cross-browser testing (Chrome, Firefox, Safari, Edge)

2. **Integration Testing**:
   - Test API client with mock responses
   - Test error handling scenarios
   - Test auto-save debouncing

### Test Data

- Create seed data for development and testing
- Include sample users, documents, and blocks
- Test edge cases: empty documents, maximum nesting, long content

## Security Considerations

1. **Password Security**:
   - Use bcrypt with appropriate cost factor (12+)
   - Never log or expose passwords

2. **Authentication**:
   - JWT tokens with reasonable expiration (24 hours)
   - Secure token storage (httpOnly cookies or localStorage with XSS protection)

3. **Authorization**:
   - Verify user ownership for all resource operations
   - Implement middleware to check permissions

4. **Input Validation**:
   - Sanitize all user inputs
   - Validate data types and formats
   - Prevent SQL injection (use parameterized queries)
   - Prevent XSS attacks (escape HTML in content)

5. **CORS**:
   - Configure appropriate CORS headers
   - Restrict origins in production

## Performance Considerations

1. **Database Optimization**:
   - Index foreign keys and frequently queried columns
   - Use connection pooling
   - Implement pagination for large document lists

2. **Frontend Optimization**:
   - Debounce auto-save (1 second)
   - Lazy load documents (only load blocks when document is opened)
   - Minimize DOM manipulations

3. **Caching**:
   - Cache user session data
   - Consider caching document tree structure

## Deployment Considerations

- Use environment variables for configuration
- Separate development and production databases
- Implement logging for debugging and monitoring
- Use HTTPS in production
- Set up database backups
