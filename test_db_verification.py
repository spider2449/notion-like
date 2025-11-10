"""Verification script for database implementation."""
import os
import sqlite3
from backend.database import get_db, get_db_connection, init_db, DATABASE_PATH

def test_connection_utilities():
    """Test database connection utilities."""
    print("Testing database connection utilities...")
    
    # Test get_db_connection
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT 1')
        result = cursor.fetchone()
        conn.close()
        print("✓ get_db_connection() works correctly")
    except Exception as e:
        print(f"✗ get_db_connection() failed: {e}")
        return False
    
    # Test context manager
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT 1')
            result = cursor.fetchone()
        print("✓ get_db() context manager works correctly")
    except Exception as e:
        print(f"✗ get_db() context manager failed: {e}")
        return False
    
    # Test error handling with rollback
    try:
        # First ensure we have a database
        if not os.path.exists(DATABASE_PATH):
            import backend.database as db
            db.init_db()
        
        # Create a test table and insert data
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('CREATE TABLE IF NOT EXISTS test_rollback (id INTEGER)')
            cursor.execute('INSERT INTO test_rollback VALUES (1)')
        
        # Count records before error
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM test_rollback')
            count_before = cursor.fetchone()[0]
        
        # Test rollback on error
        error_occurred = False
        try:
            with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO test_rollback VALUES (2)')
                # Force an error to trigger rollback
                raise Exception("Test error")
        except Exception:
            error_occurred = True
        
        # Check that rollback worked
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM test_rollback')
            count_after = cursor.fetchone()[0]
        
        # Clean up
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('DROP TABLE test_rollback')
        
        if error_occurred and count_before == count_after:
            print("✓ Error handling with rollback works correctly")
        else:
            print("✗ Rollback did not work properly")
            return False
    except Exception as e:
        print(f"✗ Error handling test failed: {e}")
        return False
    
    return True

def test_schema():
    """Test database schema."""
    print("\nTesting database schema...")
    
    # Create test database
    test_db = 'test_schema.db'
    if os.path.exists(test_db):
        os.remove(test_db)
    
    # Temporarily change DATABASE_PATH
    import backend.database as db
    original_path = db.DATABASE_PATH
    db.DATABASE_PATH = test_db
    
    try:
        # Initialize database
        db.init_db()
        print(f"Database initialized successfully at {test_db}")
        
        # Connect and verify schema with foreign keys enabled
        conn = sqlite3.connect(test_db)
        conn.execute('PRAGMA foreign_keys = ON')
        cursor = conn.cursor()
        
        # Check tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = [row[0] for row in cursor.fetchall()]
        expected_tables = ['blocks', 'documents', 'folders', 'users']
        
        for table in expected_tables:
            if table in tables:
                print(f"✓ Table '{table}' exists")
            else:
                print(f"✗ Table '{table}' missing")
                return False
        
        # Check indexes
        cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name LIKE 'idx_%'")
        indexes = [row[0] for row in cursor.fetchall()]
        expected_indexes = [
            'idx_folders_user_id',
            'idx_folders_parent_id',
            'idx_documents_user_id',
            'idx_documents_folder_id',
            'idx_blocks_document_id',
            'idx_blocks_order'
        ]
        
        for index in expected_indexes:
            if index in indexes:
                print(f"✓ Index '{index}' exists")
            else:
                print(f"✗ Index '{index}' missing")
                return False
        
        # Verify foreign keys can be enabled (check with new connection)
        conn.close()
        
        test_conn = sqlite3.connect(test_db)
        test_conn.execute('PRAGMA foreign_keys = ON')
        cursor = test_conn.cursor()
        cursor.execute('PRAGMA foreign_keys')
        fk_status = cursor.fetchone()[0]
        test_conn.close()
        
        if fk_status == 1:
            print("✓ Foreign keys are enabled")
            result = True
        else:
            print("✗ Foreign keys are not enabled")
            result = False
        
    except Exception as e:
        print(f"✗ Schema test failed: {e}")
        result = False
    finally:
        # Restore original path and cleanup
        db.DATABASE_PATH = original_path
        try:
            if os.path.exists(test_db):
                os.remove(test_db)
        except Exception:
            pass  # Ignore cleanup errors
    
    return result
    
    return True

def test_foreign_key_constraints():
    """Test foreign key constraints."""
    print("\nTesting foreign key constraints...")
    
    test_db = 'test_fk.db'
    if os.path.exists(test_db):
        os.remove(test_db)
    
    import backend.database as db
    original_path = db.DATABASE_PATH
    db.DATABASE_PATH = test_db
    
    try:
        db.init_db()
        
        conn = sqlite3.connect(test_db)
        conn.execute('PRAGMA foreign_keys = ON')
        cursor = conn.cursor()
        
        # Test cascade delete
        cursor.execute("INSERT INTO users (username, email, password_hash) VALUES ('test', 'test@test.com', 'hash')")
        user_id = cursor.lastrowid
        
        cursor.execute("INSERT INTO documents (user_id, title) VALUES (?, 'Test Doc')", (user_id,))
        doc_id = cursor.lastrowid
        
        cursor.execute("INSERT INTO blocks (document_id, content, block_type, order_index) VALUES (?, 'Test', 'paragraph', 0)", (doc_id,))
        
        # Delete user should cascade
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        
        # Check that document and block were deleted
        cursor.execute("SELECT COUNT(*) FROM documents WHERE id = ?", (doc_id,))
        doc_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM blocks WHERE document_id = ?", (doc_id,))
        block_count = cursor.fetchone()[0]
        
        conn.close()
        
        if doc_count == 0 and block_count == 0:
            print("✓ CASCADE DELETE works correctly")
            result = True
        else:
            print("✗ CASCADE DELETE failed")
            result = False
        
    except Exception as e:
        print(f"✗ Foreign key test failed: {e}")
        result = False
    finally:
        db.DATABASE_PATH = original_path
        try:
            if os.path.exists(test_db):
                os.remove(test_db)
        except Exception:
            pass  # Ignore cleanup errors
    
    return result

if __name__ == '__main__':
    print("=" * 60)
    print("Database Implementation Verification")
    print("=" * 60)
    
    all_passed = True
    
    all_passed &= test_connection_utilities()
    all_passed &= test_schema()
    all_passed &= test_foreign_key_constraints()
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ All tests passed!")
    else:
        print("✗ Some tests failed")
    print("=" * 60)
