# Product Overview

A Notion-like web application for document management and content editing.

## Core Features

- User authentication with JWT tokens
- Document and folder management with hierarchical organization
- Rich content editing with multiple block types (paragraphs, headings, lists, code blocks)
- Block type switching via right-click context menu
- Auto-save functionality (1 second after typing stops)
- Admin panel for user management

## User Experience

- Simple, clean interface focused on writing and organization
- Drag-and-drop document organization
- Real-time content persistence
- Multi-level folder nesting support

## Security

- Bcrypt password hashing (cost factor 12)
- JWT-based authentication with 24-hour token expiration
- Input sanitization to prevent XSS
- Parameterized SQL queries to prevent injection attacks
- Authorization checks on all protected endpoints
