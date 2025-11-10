#!/usr/bin/env python3
"""
Quick start script for the Notion Clone application.
This script will initialize the database, create seed data, and start the server.
"""

import os
import sys

def main():
    print("=" * 60)
    print("Notion Clone - Quick Start")
    print("=" * 60)
    
    # Check if database exists
    db_exists = os.path.exists('notion.db')
    
    if not db_exists:
        print("\n📦 Database not found. Creating database and seed data...")
        print("-" * 60)
        
        # Run seed data script
        import seed_data
        seed_data.seed_database()
        
        print("\n" + "=" * 60)
    else:
        print("\n✓ Database found")
    
    print("\n🚀 Starting Flask server...")
    print("-" * 60)
    print("\nServer will be available at: http://localhost:5000")
    print("\nTest credentials:")
    print("  Username: testuser")
    print("  Password: password123")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 60 + "\n")
    
    # Start the Flask app
    from backend.app import app
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped. Goodbye!")
        sys.exit(0)
