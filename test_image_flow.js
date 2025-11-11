// Test script for image upload flow
// Paste this in browser console to test each step

console.log("=== IMAGE UPLOAD TEST ===");

// Test 1: Check if image block type is valid
console.log("\n1. Testing block type validation...");
const validTypes = ['paragraph', 'heading1', 'heading2', 'heading3', 
                    'bullet_list', 'numbered_list', 'code', 'quote', 
                    'callout', 'toggle', 'divider', 'table', 'image'];
console.log("Valid block types:", validTypes);
console.log("Image type included:", validTypes.includes('image'));

// Test 2: Check if token exists
console.log("\n2. Checking authentication...");
const token = localStorage.getItem('token');
console.log("Token exists:", !!token);
if (token) {
    console.log("Token length:", token.length);
}

// Test 3: Test image URL save (without upload)
console.log("\n3. Testing image URL save...");
async function testImageUrl() {
    try {
        // Find an image block
        const imageBlocks = document.querySelectorAll('[data-type="image"]');
        if (imageBlocks.length === 0) {
            console.log("❌ No image blocks found. Create one first by typing / and selecting Image");
            return;
        }
        
        const blockId = imageBlocks[0].dataset.blockId;
        console.log("Found image block:", blockId);
        
        // Test URL
        const testUrl = "https://via.placeholder.com/400";
        const imageData = { url: testUrl, caption: "Test image" };
        const content = JSON.stringify(imageData);
        
        console.log("Saving test URL:", testUrl);
        const response = await apiClient.updateBlock(blockId, content);
        console.log("✅ Save successful:", response);
        
        // Reload the page to see if it persists
        console.log("Reload the page to verify the image persists");
        
    } catch (error) {
        console.error("❌ Save failed:", error);
    }
}

// Test 4: Test upload endpoint
console.log("\n4. Testing upload endpoint...");
async function testUpload() {
    try {
        // Create a test file
        const canvas = document.createElement('canvas');
        canvas.width = 100;
        canvas.height = 100;
        const ctx = canvas.getContext('2d');
        ctx.fillStyle = 'red';
        ctx.fillRect(0, 0, 100, 100);
        
        const blob = await new Promise(resolve => canvas.toBlob(resolve, 'image/png'));
        const file = new File([blob], 'test.png', { type: 'image/png' });
        
        console.log("Created test file:", file.name, file.size, "bytes");
        
        const formData = new FormData();
        formData.append('image', file);
        
        console.log("Uploading to /api/upload/image...");
        const response = await fetch('/api/upload/image', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: formData
        });
        
        console.log("Response status:", response.status);
        const data = await response.json();
        console.log("Response data:", data);
        
        if (response.ok) {
            console.log("✅ Upload successful!");
            console.log("Image URL:", data.url);
            console.log("Try accessing:", window.location.origin + data.url);
        } else {
            console.error("❌ Upload failed:", data.error);
        }
        
    } catch (error) {
        console.error("❌ Upload error:", error);
    }
}

// Test 5: Check uploads directory
console.log("\n5. Checking if uploads are accessible...");
async function testUploadsAccess() {
    try {
        const response = await fetch('/uploads/test.txt');
        console.log("Uploads directory status:", response.status);
        if (response.status === 404) {
            console.log("⚠️  Uploads directory exists but no test file (this is normal)");
        }
    } catch (error) {
        console.error("❌ Cannot access uploads directory:", error);
    }
}

// Run tests
console.log("\n=== RUNNING TESTS ===");
console.log("Run these commands manually:");
console.log("1. testImageUrl() - Test saving image URL");
console.log("2. testUpload() - Test file upload");
console.log("3. testUploadsAccess() - Test uploads directory");

// Make functions available globally
window.testImageUrl = testImageUrl;
window.testUpload = testUpload;
window.testUploadsAccess = testUploadsAccess;

console.log("\n✅ Test functions loaded. Run them in console!");
