"""
Seed data script to create sample users, documents, folders, and blocks for testing.
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

from backend.database import init_db
from backend.services.auth_service import AuthService
from backend.services.document_service import DocumentService
from backend.services.block_service import BlockService

def seed_database():
    """Create seed data for testing."""
    print("Initializing database...")
    init_db()
    
    print("\nCreating test users...")
    
    # Create test user 1
    try:
        user1 = AuthService.register_user('testuser', 'test@example.com', 'password123')
        print(f"✓ Created user: {user1.username} (ID: {user1.id})")
    except ValueError as e:
        print(f"✗ User creation failed: {e}")
        return
    
    # Create test user 2
    try:
        user2 = AuthService.register_user('alice', 'alice@example.com', 'password123')
        print(f"✓ Created user: {user2.username} (ID: {user2.id})")
    except ValueError as e:
        print(f"Note: {e}")
    
    print("\nCreating folders...")
    
    # Create folders for user1
    folder1 = DocumentService.create_folder(user1.id, 'Work Projects')
    print(f"✓ Created folder: {folder1.name} (ID: {folder1.id})")
    
    folder2 = DocumentService.create_folder(user1.id, 'Personal Notes')
    print(f"✓ Created folder: {folder2.name} (ID: {folder2.id})")
    
    subfolder1 = DocumentService.create_folder(user1.id, 'Q4 2024', folder1.id)
    print(f"✓ Created subfolder: {subfolder1.name} (ID: {subfolder1.id})")
    
    print("\nCreating documents...")
    
    # Create documents
    doc1 = DocumentService.create_document(user1.id, 'Welcome to Notion Clone', None)
    print(f"✓ Created document: {doc1.title} (ID: {doc1.id})")
    
    doc2 = DocumentService.create_document(user1.id, 'Project Roadmap', folder1.id)
    print(f"✓ Created document: {doc2.title} (ID: {doc2.id})")
    
    doc3 = DocumentService.create_document(user1.id, 'Meeting Notes', folder1.id)
    print(f"✓ Created document: {doc3.title} (ID: {doc3.id})")
    
    doc4 = DocumentService.create_document(user1.id, 'Shopping List', folder2.id)
    print(f"✓ Created document: {doc4.title} (ID: {doc4.id})")
    
    print("\nCreating blocks...")
    
    # Add blocks to Welcome document
    block1 = BlockService.create_block(doc1.id, user1.id, 'Welcome to Notion Clone!', 'heading1')
    print(f"✓ Created block: heading1 (ID: {block1.id})")
    
    block2 = BlockService.create_block(doc1.id, user1.id, 'This is a Notion-like web application built with Python, JavaScript, and SQLite.', 'paragraph')
    print(f"✓ Created block: paragraph (ID: {block2.id})")
    
    block3 = BlockService.create_block(doc1.id, user1.id, 'Features', 'heading2')
    print(f"✓ Created block: heading2 (ID: {block3.id})")
    
    block4 = BlockService.create_block(doc1.id, user1.id, 'Create and edit content blocks', 'bullet_list')
    print(f"✓ Created block: bullet_list (ID: {block4.id})")
    
    block5 = BlockService.create_block(doc1.id, user1.id, 'Right-click to change block types', 'bullet_list')
    print(f"✓ Created block: bullet_list (ID: {block5.id})")
    
    block6 = BlockService.create_block(doc1.id, user1.id, 'Organize documents in folders', 'bullet_list')
    print(f"✓ Created block: bullet_list (ID: {block6.id})")
    
    block7 = BlockService.create_block(doc1.id, user1.id, 'Auto-save functionality', 'bullet_list')
    print(f"✓ Created block: bullet_list (ID: {block7.id})")
    
    # Add blocks to Project Roadmap
    block8 = BlockService.create_block(doc2.id, user1.id, 'Q4 2024 Roadmap', 'heading1')
    print(f"✓ Created block: heading1 (ID: {block8.id})")
    
    block9 = BlockService.create_block(doc2.id, user1.id, 'Complete user authentication', 'numbered_list')
    print(f"✓ Created block: numbered_list (ID: {block9.id})")
    
    block10 = BlockService.create_block(doc2.id, user1.id, 'Implement document management', 'numbered_list')
    print(f"✓ Created block: numbered_list (ID: {block10.id})")
    
    block11 = BlockService.create_block(doc2.id, user1.id, 'Add block type switching', 'numbered_list')
    print(f"✓ Created block: numbered_list (ID: {block11.id})")
    
    # Add code block example
    block12 = BlockService.create_block(doc2.id, user1.id, 'def hello_world():\n    print("Hello, World!")', 'code')
    print(f"✓ Created block: code (ID: {block12.id})")
    
    # Add blocks to Shopping List
    block13 = BlockService.create_block(doc4.id, user1.id, 'Grocery Shopping', 'heading2')
    print(f"✓ Created block: heading2 (ID: {block13.id})")
    
    block14 = BlockService.create_block(doc4.id, user1.id, 'Milk', 'bullet_list')
    print(f"✓ Created block: bullet_list (ID: {block14.id})")
    
    block15 = BlockService.create_block(doc4.id, user1.id, 'Bread', 'bullet_list')
    print(f"✓ Created block: bullet_list (ID: {block15.id})")
    
    block16 = BlockService.create_block(doc4.id, user1.id, 'Eggs', 'bullet_list')
    print(f"✓ Created block: bullet_list (ID: {block16.id})")
    
    print("\n✅ Seed data created successfully!")
    print("\nTest credentials:")
    print("  Email: test@example.com")
    print("  Password: password123")
    print("\nYou can now start the application and log in with these credentials.")

if __name__ == '__main__':
    seed_database()
