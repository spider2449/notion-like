# Admin System Guide

## Overview

The admin system allows designated users to manage all user accounts in the application.

## Features

### Admin Capabilities
- View all users and statistics
- Create new users (with or without admin privileges)
- Grant/revoke admin privileges to/from users
- Delete user accounts
- View user statistics (total users, admin count, regular user count)

### Security
- Admin-only routes are protected by `@require_admin` middleware
- Admins cannot modify their own admin status or delete themselves
- All admin actions require authentication

## Making a User Admin

### Using the Command Line Script

```bash
# List all users
python make_admin.py --list

# Make a user admin by email
python make_admin.py user@example.com
```

### Using the Admin Panel (if you're already an admin)

1. Log in as an admin user
2. Navigate to Admin Panel (crown icon in sidebar)
3. Find the user in the table
4. Click "Make Admin" button

## Accessing the Admin Panel

1. Log in with an admin account
2. Look for the "Admin Panel" button (👑) in the sidebar
3. Click to access the admin dashboard

**Note:** The Admin Panel button only appears for users with admin privileges.

## Admin Panel Features

### Dashboard Statistics
- Total Users: Count of all registered users
- Admin Users: Count of users with admin privileges
- Regular Users: Count of non-admin users

### User Management Table
- View all users with their details (ID, username, email, role, creation date)
- Toggle admin status for any user (except yourself)
- Delete users (except yourself)
- Create new users with optional admin privileges

### Creating Users
1. Click "Create User" button
2. Fill in username, email, and password
3. Optionally check "Admin privileges" checkbox
4. Click "Create User"

## API Endpoints

All admin endpoints require authentication and admin privileges:

- `GET /api/admin/users` - Get all users
- `GET /api/admin/users/:id` - Get specific user
- `POST /api/admin/users` - Create new user
- `PUT /api/admin/users/:id/admin` - Update admin status
- `DELETE /api/admin/users/:id` - Delete user
- `GET /api/admin/statistics` - Get user statistics

## Database Schema

The `users` table includes an `is_admin` column:
- `0` = Regular user
- `1` = Admin user

## First Admin Setup

When setting up the application for the first time:

1. Create a regular user account through registration
2. Use the `make_admin.py` script to grant admin privileges:
   ```bash
   python make_admin.py your-email@example.com
   ```
3. Log in and access the Admin Panel

## Security Best Practices

1. **Limit Admin Accounts**: Only grant admin privileges to trusted users
2. **Regular Audits**: Periodically review the list of admin users
3. **Strong Passwords**: Ensure admin accounts use strong passwords
4. **Monitor Activity**: Keep track of admin actions in your logs

## Troubleshooting

### Admin Panel Not Showing
- Verify your account has admin privileges: `python make_admin.py --list`
- Log out and log back in to refresh your session
- Check browser console for errors

### Cannot Access Admin Routes
- Ensure you're logged in with an admin account
- Check that the `is_admin` column exists in your database
- Run the migration: `python backend/migrations/add_admin_role.py`

### Migration Issues
If the `is_admin` column doesn't exist, run:
```bash
python backend/migrations/add_admin_role.py
```

## Files Structure

```
backend/
├── middleware/
│   └── admin_middleware.py      # Admin authorization middleware
├── services/
│   └── admin_service.py         # Admin business logic
├── routes/
│   └── admin_routes.py          # Admin API endpoints
└── migrations/
    └── add_admin_role.py        # Database migration for admin role

frontend/
├── html/
│   └── admin.html               # Admin panel UI
├── js/
│   └── admin.js                 # Admin panel logic
└── css/
    └── admin.css                # Admin panel styles

make_admin.py                     # CLI tool for managing admins
```
