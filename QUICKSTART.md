# Quick Start Guide

## Get Started in 3 Steps

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python start.py
```

This will:
- Create the database (if it doesn't exist)
- Add sample data
- Start the server at http://localhost:5000

### 3. Log In
Open your browser to http://localhost:5000 and log in with:
- **Username**: testuser
- **Password**: password123

## What You Can Do

✅ Create and organize documents in folders  
✅ Add content blocks with different types  
✅ Right-click blocks to change their type  
✅ Auto-save as you type  
✅ Navigate through your document tree  

## Block Types Available

- **Paragraph** - Regular text
- **Heading 1, 2, 3** - Different heading sizes
- **Bullet List** - Unordered lists
- **Numbered List** - Ordered lists
- **Code Block** - Monospace code formatting

## Tips

- Right-click on any block to change its type
- Content saves automatically after 1 second of inactivity
- Use folders to organize your documents
- Delete blocks by hovering and clicking the delete button

## Troubleshooting

**Port already in use?**
- Change the port in `backend/app.py` (line with `app.run`)

**Database errors?**
- Delete `notion.db` and run `python start.py` again

**Can't log in?**
- Make sure you ran the seed data script
- Check that the server is running

## Need Help?

Check the full README.md for detailed documentation.
