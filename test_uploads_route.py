"""
Test if the uploads route is working
Run this after starting the Flask server
"""
import requests

# Test if the uploads route exists
url = "http://localhost:5000/uploads/3e73944d2eeb449a94937250cd57c6ed_2mb-jpg-example-fileaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.jpeg"

print("Testing uploads route...")
print(f"URL: {url}")

try:
    response = requests.get(url)
    print(f"Status code: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ SUCCESS! The uploads route is working!")
        print(f"Content type: {response.headers.get('Content-Type')}")
        print(f"Content length: {len(response.content)} bytes")
    elif response.status_code == 404:
        print("❌ FAILED! 404 Not Found")
        print("The Flask server needs to be restarted to register the /uploads route")
    else:
        print(f"⚠️  Unexpected status: {response.status_code}")
        
except requests.exceptions.ConnectionError:
    print("❌ Cannot connect to Flask server")
    print("Make sure the server is running on http://localhost:5000")
except Exception as e:
    print(f"❌ Error: {e}")
