"""
Migration: Add image block type support

This migration adds support for the 'image' block type with file upload functionality.
No database schema changes are required since block_type is stored as TEXT.

The image block type stores its data as JSON in the content field with the structure:
{
    "url": "/uploads/abc123_image.jpg",
    "caption": "Optional caption text"
}

Changes:
- Added 'image' to VALID_BLOCK_TYPES in block_service.py
- Added image upload endpoint in block_routes.py
- Added uploads folder configuration in app.py
- Added image rendering in editor-enhanced.js
- Added image styling in app.css
- Added image option to slash menu in app.html
- Created uploads/ directory for storing uploaded images

Features:
- Upload images via file picker
- Paste image URLs directly
- Add captions to images
- Change uploaded images
- Supports: png, jpg, jpeg, gif, webp, svg
- Max file size: 16MB
"""

import os

# Create uploads directory if it doesn't exist
uploads_dir = 'uploads'
if not os.path.exists(uploads_dir):
    os.makedirs(uploads_dir)
    print(f"Created {uploads_dir}/ directory")
else:
    print(f"{uploads_dir}/ directory already exists")

print("Image block type support added successfully")
