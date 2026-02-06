"""Test script for database encryption

This script tests the encryption functionality to ensure:
1. pgcrypto extension is installed
2. Encryption/decryption works correctly
3. All tables are created with proper schema

Requirements: 7.1, 7.2, 7.3
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from app.database import AsyncSessionLocal, engine
from app.encryption import encryption_service
from sqlalchemy import text


async def test_pgcrypto_extension():
    """Test that pgcrypto extension is installed"""
    print("\n=== Testing pgcrypto Extension ===")
    
    async with AsyncSessionLocal() as db:
        try:
            result = await db.execute(
                text("SELECT extname FROM pg_extension WHERE extname = 'pgcrypto'")
            )
            row = result.fetchone()
            
            if row:
                print("✓ pgcrypto extension is installed")
                return True
            else:
                print("✗ pgcrypto extension is NOT installed")
                return False
        except Exception as e:
            print(f"✗ Error checking pgcrypto: {e}")
            return False


async def test_text_encryption():
    """Test text encryption and decryption"""
    print("\n=== Testing Text Encryption ===")
    
    async with AsyncSessionLocal() as db:
        try:
            # Test data
            plaintext = "This is sensitive patient data that must be encrypted"
            
            # Encrypt
            encrypted = await encryption_service.encrypt_text(db, plaintext)
            print(f"Original:  {plaintext}")
            print(f"Encrypted: {encrypted[:50]}..." if len(encrypted) > 50 else f"Encrypted: {encrypted}")
            
            # Verify encrypted is different from plaintext
            assert encrypted != plaintext, "Encrypted text should differ from plaintext"
            print("✓ Text is encrypted (differs from plaintext)")
            
            # Decrypt
            decrypted = await encryption_service.decrypt_text(db, encrypted)
            print(f"Decrypted: {decrypted}")
            
            # Verify decrypted matches original
            assert decrypted == plaintext, "Decrypted text should match original"
            print("✓ Text decryption successful (matches original)")
            
            return True
        except Exception as e:
            print(f"✗ Text encryption test failed: {e}")
            return False


async def test_json_encryption():
    """Test JSON encryption and decryption"""
    print("\n=== Testing JSON Encryption ===")
    
    async with AsyncSessionLocal() as db:
        try:
            # Test data
            data = {
                "patient_name": "John Doe",
                "age": 65,
                "medications": ["Aspirin", "Metformin"],
                "diagnosis": "Type 2 Diabetes"
            }
            
            # Encrypt
            encrypted = await encryption_service.encrypt_json(db, data)
            print(f"Original:  {data}")
            print(f"Encrypted: {encrypted[:50]}..." if len(encrypted) > 50 else f"Encrypted: {encrypted}")
            
            # Decrypt
            decrypted = await encryption_service.decrypt_json(db, encrypted)
            print(f"Decrypted: {decrypted}")
            
            # Verify decrypted matches original
            assert decrypted == data, "Decrypted JSON should match original"
            print("✓ JSON encryption/decryption successful")
            
            return True
        except Exception as e:
            print(f"✗ JSON encryption test failed: {e}")
            return False


async def test_table_creation():
    """Test that all tables are created"""
    print("\n=== Testing Table Creation ===")
    
    expected_tables = [
        'consent_records',
        'audio_recordings',
        'transcripts',
        'clinical_data_records',
        'submission_records',
        'audit_logs'
    ]
    
    async with AsyncSessionLocal() as db:
        try:
            result = await db.execute(
                text("""
                    SELECT tablename 
                    FROM pg_tables 
                    WHERE schemaname = 'public'
                    ORDER BY tablename
                """)
            )
            tables = [row[0] for row in result.fetchall()]
            
            print(f"Found tables: {tables}")
            
            all_present = True
            for table in expected_tables:
                if table in tables:
                    print(f"✓ Table '{table}' exists")
                else:
                    print(f"✗ Table '{table}' is missing")
                    all_present = False
            
            return all_present
        except Exception as e:
            print(f"✗ Error checking tables: {e}")
            return False


async def test_indexes():
    """Test that indexes are created"""
    print("\n=== Testing Index Creation ===")
    
    async with AsyncSessionLocal() as db:
        try:
            result = await db.execute(
                text("""
                    SELECT 
                        schemaname,
                        tablename,
                        indexname
                    FROM pg_indexes
                    WHERE schemaname = 'public'
                    ORDER BY tablename, indexname
                """)
            )
            indexes = result.fetchall()
            
            print(f"Found {len(indexes)} indexes:")
            for schema, table, index in indexes:
                print(f"  - {table}.{index}")
            
            # Check for some critical indexes
            index_names = [idx[2] for idx in indexes]
            critical_indexes = [
                'ix_consent_records_session_id',
                'ix_audio_recordings_session_id',
                'ix_transcripts_recording_id',
                'ix_clinical_data_records_transcript_id',
                'ix_submission_records_clinical_data_id',
                'ix_audit_logs_timestamp'
            ]
            
            all_present = True
            for idx in critical_indexes:
                if idx in index_names:
                    print(f"✓ Critical index '{idx}' exists")
                else:
                    print(f"✗ Critical index '{idx}' is missing")
                    all_present = False
            
            return all_present
        except Exception as e:
            print(f"✗ Error checking indexes: {e}")
            return False


async def test_enum_types():
    """Test that enum types are created"""
    print("\n=== Testing Enum Types ===")
    
    expected_enums = [
        'consent_method_enum',
        'recording_status_enum',
        'transcript_status_enum',
        'clinical_data_status_enum',
        'submission_status_enum'
    ]
    
    async with AsyncSessionLocal() as db:
        try:
            result = await db.execute(
                text("""
                    SELECT typname 
                    FROM pg_type 
                    WHERE typtype = 'e'
                    ORDER BY typname
                """)
            )
            enums = [row[0] for row in result.fetchall()]
            
            print(f"Found enum types: {enums}")
            
            all_present = True
            for enum in expected_enums:
                if enum in enums:
                    print(f"✓ Enum type '{enum}' exists")
                else:
                    print(f"✗ Enum type '{enum}' is missing")
                    all_present = False
            
            return all_present
        except Exception as e:
            print(f"✗ Error checking enum types: {e}")
            return False


async def run_all_tests():
    """Run all encryption and schema tests"""
    print("=" * 60)
    print("Database Encryption and Schema Tests")
    print("=" * 60)
    
    results = []
    
    # Test pgcrypto extension
    results.append(("pgcrypto Extension", await test_pgcrypto_extension()))
    
    # Test encryption
    results.append(("Text Encryption", await test_text_encryption()))
    results.append(("JSON Encryption", await test_json_encryption()))
    
    # Test schema
    results.append(("Table Creation", await test_table_creation()))
    results.append(("Index Creation", await test_indexes()))
    results.append(("Enum Types", await test_enum_types()))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✓ All tests passed! Database encryption is working correctly.")
        return 0
    else:
        print(f"\n✗ {total - passed} test(s) failed. Please check the errors above.")
        return 1


async def main():
    """Main entry point"""
    try:
        exit_code = await run_all_tests()
        sys.exit(exit_code)
    except Exception as e:
        print(f"\n✗ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        # Close the engine
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
