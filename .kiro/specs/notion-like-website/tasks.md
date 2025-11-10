# Implementation Plan

- [x] 1. Set up project structure and dependencies


  - Create directory structure for backend (models, services, repositories, routes) and frontend (js, css, html)
  - Initialize Python virtual environment and install Flask, Flask-CORS, PyJWT, bcrypt, and SQLite dependencies
  - Create requirements.txt file
  - Set up basic Flask application entry point
  - _Requirements: 6.5_



- [-] 2. Implement database schema and connection utilities




  - Create SQLite database initialization script with tables for users, folders, documents, and blocks
  - Write database connection management utilities with proper error handling
  - Implement database migration/setup function to create tables on first run





  - Add indexes on foreign keys and frequently queried columns
  - _Requirements: 5.1, 5.2, 5.3_



- [x] 3. Implement user authentication system

  - [x] 3.1 Create User model and repository
    - Write User model class with fields for id, username, email, password_hash, timestamps
    - Implement UserRepository with methods for create, find_by_email, find_by_id
    - Use parameterized queries to prevent SQL injection
    - _Requirements: 1.1, 5.1_
  
  - [x] 3.2 Implement authentication service
    - Write password hashing function using bcrypt with cost factor 12
    - Implement JWT token generation and verification functions
    - Create register_user function with validation
    - Create authenticate_user function that verifies credentials and returns JWT
    - _Requirements: 1.1, 1.2_
  
  - [x] 3.3 Create authentication API routes
    - Implement POST /api/auth/register endpoint
    - Implement POST /api/auth/login endpoint
    - Implement POST /api/auth/logout endpoint
    - Add request validation and error handling with appropriate status codes
    - _Requirements: 1.1, 1.2, 1.3_
  
  - [x] 3.4 Create authentication middleware

    - Write JWT verification middleware to protect routes
    - Extract user identity from token and attach to request context
    - Handle expired and invalid tokens with 401 responses
    - _Requirements: 1.2, 1.4_

- [x] 4. Implement document and folder management

  - [x] 4.1 Create Document and Folder models and repositories

    - Write Document model with fields for id, user_id, title, folder_id, timestamps
    - Write Folder model with fields for id, user_id, name, parent_folder_id, timestamps
    - Implement DocumentRepository with CRUD methods
    - Implement FolderRepository with CRUD methods and hierarchy queries
    - _Requirements: 4.1, 4.2, 4.4, 5.3_
  
  - [x] 4.2 Implement document service


    - Write create_document function with user ownership
    - Write get_user_documents function that returns hierarchical structure
    - Write update_document function with authorization check
    - Write delete_document function that cascades to blocks
    - Write create_folder function with parent folder validation
    - _Requirements: 4.2, 4.3, 4.4, 4.5_
  

  - [x] 4.3 Create document API routes

    - Implement GET /api/documents endpoint with authentication
    - Implement POST /api/documents endpoint
    - Implement PUT /api/documents/<id> endpoint with ownership verification
    - Implement DELETE /api/documents/<id> endpoint with ownership verification
    - Implement POST /api/folders endpoint
    - _Requirements: 4.1, 4.2, 4.3, 4.5_


- [x] 5. Implement content block system


  - [x] 5.1 Create Block model and repository

    - Write Block model with fields for id, document_id, content, block_type, order_index, timestamps
    - Implement BlockRepository with CRUD methods
    - Add method to get blocks by document ordered by order_index
    - Add method to reorder blocks
    - _Requirements: 2.1, 2.3, 5.2_
  
  - [x] 5.2 Implement block service


    - Write create_block function with automatic order_index assignment
    - Write update_block function with content and type update support
    - Write delete_block function
    - Write get_blocks_by_document function
    - Write reorder_blocks function to update multiple block order_index values
    - Implement auto-save logic with timestamp tracking
    - _Requirements: 2.1, 2.2, 2.4, 3.2, 3.4_
  
  - [x] 5.3 Create block API routes


    - Implement GET /api/documents/<id>/blocks endpoint
    - Implement POST /api/blocks endpoint with document ownership verification
    - Implement PUT /api/blocks/<id> endpoint with ownership verification
    - Implement DELETE /api/blocks/<id> endpoint with ownership verification
    - Implement PUT /api/documents/<id>/blocks/reorder endpoint
    - Add validation for block_type to ensure only supported types are allowed
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 3.2, 3.4_

- [x] 6. Build frontend authentication UI



  - [x] 6.1 Create HTML structure for authentication pages

    - Create login.html with email and password form
    - Create register.html with username, email, and password form
    - Add basic styling for forms
    - _Requirements: 1.1, 1.2_
  

  - [x] 6.2 Implement authentication JavaScript

    - Write API client module with request function that includes JWT token
    - Implement login form submission handler
    - Implement registration form submission handler
    - Store JWT token in localStorage on successful login
    - Implement automatic redirect to main app on successful authentication
    - Handle authentication errors and display user-friendly messages
    - _Requirements: 1.1, 1.2, 1.3, 1.5_

- [x] 7. Build frontend navigation panel



  - [x] 7.1 Create navigation HTML and CSS

    - Create sidebar navigation structure in main app HTML
    - Style navigation tree with folders and documents
    - Add expand/collapse icons for folders
    - Add buttons for creating new documents and folders
    - _Requirements: 4.1, 4.2_
  
  - [x] 7.2 Implement navigation JavaScript


    - Write function to fetch and render document tree from API
    - Implement folder expand/collapse functionality
    - Implement document click handler to load document content
    - Implement create document functionality
    - Implement create folder functionality
    - Implement delete document/folder functionality with confirmation
    - Add loading indicators for navigation operations
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_


- [x] 8. Build frontend editor component


  - [x] 8.1 Create editor HTML and CSS

    - Create main editor area in app HTML
    - Style different block types (paragraph, headings, lists, code)
    - Add button to create new blocks
    - Style blocks with appropriate spacing and typography
    - _Requirements: 2.1, 2.3, 3.5_
  

  - [x] 8.2 Implement editor JavaScript for block rendering

    - Write function to fetch blocks for selected document
    - Implement block rendering function that applies correct styling based on block_type
    - Implement contenteditable functionality for inline editing
    - Add delete button to each block
    - _Requirements: 2.1, 2.3, 2.4, 3.5_
  
  - [x] 8.3 Implement auto-save functionality


    - Add input event listener to blocks with debouncing (1 second delay)
    - Implement save function that calls PUT /api/blocks/<id> endpoint
    - Show save status indicator (saving/saved)
    - Handle save errors with retry mechanism
    - _Requirements: 2.2, 3.4_
  

  - [x] 8.4 Implement block creation and deletion

    - Write function to create new block via POST /api/blocks
    - Add new block to DOM immediately for responsive feel
    - Implement delete block functionality with API call
    - Update order_index for remaining blocks after deletion
    - _Requirements: 2.1, 2.4_



- [x] 9. Implement context menu for block type switching

  - [x] 9.1 Create context menu HTML and CSS

    - Create context menu element with list of block types
    - Style menu with hover effects
    - Position menu absolutely for right-click placement
    - Add icons or labels for each block type option
    - _Requirements: 3.1, 3.3, 3.5_
  

  - [x] 9.2 Implement context menu JavaScript

    - Add right-click event listener to blocks that prevents default and shows menu
    - Position menu at cursor location within 200ms
    - Implement block type selection handler
    - Call PUT /api/blocks/<id> with new block_type
    - Update block styling immediately after type change
    - Close menu on selection or outside click
    - _Requirements: 3.1, 3.2, 3.4, 3.5_


- [x] 10. Implement error handling and loading states

  - Write centralized error handling in API client
  - Display user-friendly error messages for network failures
  - Implement loading spinners for operations over 500ms
  - Add 401 error handler that redirects to login and clears tokens
  - Disable UI elements during operations to prevent duplicate requests
  - _Requirements: 6.2, 6.3, 6.4_


- [x] 11. Add data persistence verification

  - Implement session state management to maintain user login
  - Verify blocks are saved to database on content change
  - Verify document tree structure persists across page reloads
  - Test that user data loads correctly on login
  - _Requirements: 1.4, 5.1, 5.2, 5.3, 5.4_


- [x] 12. Implement security measures

  - Add input sanitization for all user inputs on backend
  - Implement XSS prevention by escaping HTML in block content
  - Verify authorization checks on all protected endpoints
  - Configure CORS headers appropriately
  - Add rate limiting to authentication endpoints
  - _Requirements: 1.1, 1.2, 1.3_

- [x] 13. Create seed data and test the application


  - Write script to create sample users, documents, folders, and blocks
  - Test complete user flow: register, login, create document, add blocks, change types
  - Test navigation: create folders, organize documents, delete items
  - Test auto-save functionality with various timing scenarios
  - Test context menu on different block types
  - Cross-browser testing on Chrome, Firefox, Safari, and Edge
  - _Requirements: 1.1, 1.2, 2.1, 2.2, 3.1, 3.2, 4.1, 4.2, 4.3, 6.5_
