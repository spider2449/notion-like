# Debug Image Upload Issue

## Steps to Debug

### 1. Restart the Server
```bash
# Stop the server (Ctrl+C)
# Then restart:
python start.py
```

### 2. Open Browser Console (F12)
When you try to upload an image, you should see console logs like:
```
File selected: image.jpg 123456 bytes
Starting upload for block: 123
Uploading to /api/upload/image...
Upload response status: 200
Upload successful, URL: /uploads/abc123_image.jpg
Saving image URL to block: 123 /uploads/abc123_image.jpg
Updating block with content: {"url":"/uploads/abc123_image.jpg","caption":""}
Updated local block data
Re-rendering block element
Image saved successfully
```

### 3. Check Server Console
You should see logs like:
```
Upload request received from user 1
Files in request: ['image']
File received: image.jpg
File extension: jpg
Generated unique filename: abc123_image.jpg
Saving to: uploads/abc123_image.jpg
File saved successfully
Returning URL: /uploads/abc123_image.jpg
```

## Common Issues and Solutions

### Issue 1: "No image file provided"
**Cause**: FormData not sending correctly
**Solution**: Check that the file input has `accept="image/*"`

### Issue 2: 401 Unauthorized
**Cause**: Not logged in or token expired
**Solution**: 
- Check localStorage has 'token'
- Try logging out and back in

### Issue 3: 404 Not Found
**Cause**: Route not registered
**Solution**: 
- Restart the Flask server
- Check that block_routes.bp is registered in app.py

### Issue 4: Image uploads but doesn't display
**Cause**: Block not re-rendering or URL incorrect
**Solution**:
- Check browser console for the URL being saved
- Try accessing the URL directly: `http://localhost:5000/uploads/filename.jpg`
- Check that the uploads/ folder exists and has the file

### Issue 5: CORS Error
**Cause**: Cross-origin request blocked
**Solution**: Flask-CORS should handle this, but verify CORS(app) is in app.py

### Issue 6: File too large
**Cause**: File exceeds 16MB limit
**Solution**: Try a smaller image or increase MAX_CONTENT_LENGTH in app.py

## Manual Test

### Test 1: Upload Endpoint
```bash
# Get your token from browser localStorage
curl -X POST http://localhost:5000/api/upload/image \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -F "image=@path/to/test-image.jpg"
```

Expected response:
```json
{
  "message": "Image uploaded successfully",
  "url": "/uploads/abc123_test-image.jpg"
}
```

### Test 2: Serve Endpoint
After uploading, test if the image is accessible:
```
http://localhost:5000/uploads/abc123_test-image.jpg
```

Should display the image in your browser.

## Checklist

- [ ] Server restarted after adding image upload code
- [ ] `uploads/` directory exists in project root
- [ ] Logged in to the application
- [ ] Browser console shows no errors
- [ ] Server console shows upload logs
- [ ] Image block type appears in slash menu
- [ ] File picker opens when clicking upload area
- [ ] Upload completes without errors
- [ ] Block re-renders with image displayed

## If Still Not Working

1. **Check the exact error message** in browser console
2. **Check server logs** for Python errors
3. **Verify the block content** is being saved:
   - Open browser DevTools → Application → Local Storage
   - Check the block data structure
4. **Try pasting an image URL** instead of uploading:
   - Use a public image URL like: `https://via.placeholder.com/400`
   - This tests if the rendering works without upload
