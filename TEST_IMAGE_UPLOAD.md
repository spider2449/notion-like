# Testing Image Upload Feature

## Steps to Test

1. **Restart the Flask server** to load the new routes:
   ```bash
   python start.py
   ```
   Or if already running:
   - Stop the server (Ctrl+C)
   - Start it again

2. **Verify the uploads directory exists**:
   - Check that `uploads/` folder is present in the project root
   - It should have been created automatically

3. **Test the image block**:
   - Open a document in the app
   - Type `/` to open the slash menu
   - Select "Image" from the menu
   - Try uploading an image or pasting an image URL

## Troubleshooting

### If you get a 404 error:

1. **Check the server console** for any error messages
2. **Verify the route is registered**:
   - The upload endpoint should be at: `POST /api/upload/image`
   - The serve endpoint should be at: `GET /uploads/<filename>`

3. **Check browser console** (F12) to see the exact URL being requested

4. **Verify authentication**:
   - Make sure you're logged in
   - Check that the JWT token is in localStorage

### Common Issues:

- **Server not restarted**: New routes won't work until server restarts
- **CORS issues**: Should be handled by Flask-CORS
- **File permissions**: Make sure the `uploads/` directory is writable
- **Max file size**: Files over 16MB will be rejected

## Expected Behavior

When working correctly:
1. Click on image upload area → file picker opens
2. Select an image → uploads to server
3. Image displays in the block
4. Can add a caption below the image
5. Hover over image → "Change Image" button appears

## API Endpoints Added

- `POST /api/upload/image` - Upload image file (requires auth)
- `GET /uploads/<filename>` - Serve uploaded images

## Supported Formats

- PNG (.png)
- JPEG (.jpg, .jpeg)
- GIF (.gif)
- WebP (.webp)
- SVG (.svg)

Max file size: 16MB
