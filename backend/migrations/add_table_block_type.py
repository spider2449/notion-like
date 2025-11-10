"""
Migration: Add table block type support

This migration adds support for the 'table' block type.
No database schema changes are required since block_type is stored as TEXT.

The table block type stores its data as JSON in the content field with the structure:
{
    "rows": 3,
    "cols": 3,
    "data": {
        "0-0": "Column 1",
        "0-1": "Column 2",
        "1-0": "Cell data",
        ...
    }
}

Changes:
- Added 'table' to VALID_BLOCK_TYPES in block_service.py
- Added table rendering in editor-enhanced.js
- Added table styling in app.css
- Added table option to slash menu in app.html
"""

# No database changes needed - this is a documentation file
print("Table block type support added - no database migration required")
