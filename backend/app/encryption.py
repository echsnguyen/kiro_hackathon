"""Encryption utilities using pgcrypto for column-level encryption

This module provides utilities for encrypting and decrypting sensitive data
using PostgreSQL's pgcrypto extension with AES-256-GCM encryption.

Requirements: 7.1, 7.2, 7.3, 7.6, 14.7
"""

import base64
from typing import Optional, Any
import json
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings


class EncryptionService:
    """Service for encrypting and decrypting sensitive data using pgcrypto"""
    
    def __init__(self, encryption_key: Optional[str] = None):
        """
        Initialize encryption service
        
        Args:
            encryption_key: Base64 encoded encryption key. If None, uses settings.encryption_key
        """
        self.encryption_key = encryption_key or settings.encryption_key
    
    async def encrypt_text(self, db: AsyncSession, plaintext: str) -> str:
        """
        Encrypt text using pgcrypto's pgp_sym_encrypt with AES-256
        
        Args:
            db: Database session
            plaintext: Text to encrypt
            
        Returns:
            Base64 encoded encrypted text
        """
        if not plaintext:
            return plaintext
        
        # Use pgcrypto's pgp_sym_encrypt for AES-256 encryption
        result = await db.execute(
            text("SELECT encode(pgp_sym_encrypt(:plaintext, :key, 'cipher-algo=aes256'), 'base64') as encrypted"),
            {"plaintext": plaintext, "key": self.encryption_key}
        )
        row = result.fetchone()
        return row[0] if row else ""
    
    async def decrypt_text(self, db: AsyncSession, encrypted_text: str) -> str:
        """
        Decrypt text using pgcrypto's pgp_sym_decrypt
        
        Args:
            db: Database session
            encrypted_text: Base64 encoded encrypted text
            
        Returns:
            Decrypted plaintext
        """
        if not encrypted_text:
            return encrypted_text
        
        # Use pgcrypto's pgp_sym_decrypt
        result = await db.execute(
            text("SELECT pgp_sym_decrypt(decode(:encrypted, 'base64'), :key) as decrypted"),
            {"encrypted": encrypted_text, "key": self.encryption_key}
        )
        row = result.fetchone()
        return row[0] if row else ""
    
    async def encrypt_json(self, db: AsyncSession, data: Any) -> str:
        """
        Encrypt JSON data
        
        Args:
            db: Database session
            data: Data to encrypt (will be JSON serialized)
            
        Returns:
            Base64 encoded encrypted JSON
        """
        if data is None:
            return None
        
        json_str = json.dumps(data)
        return await self.encrypt_text(db, json_str)
    
    async def decrypt_json(self, db: AsyncSession, encrypted_json: str) -> Any:
        """
        Decrypt JSON data
        
        Args:
            db: Database session
            encrypted_json: Base64 encoded encrypted JSON
            
        Returns:
            Decrypted and parsed JSON data
        """
        if not encrypted_json:
            return None
        
        json_str = await self.decrypt_text(db, encrypted_json)
        return json.loads(json_str) if json_str else None
    
    def encrypt_text_sync(self, plaintext: str) -> str:
        """
        Synchronous encryption using Python's cryptography library
        This is a fallback for cases where database session is not available
        
        Args:
            plaintext: Text to encrypt
            
        Returns:
            Base64 encoded encrypted text
        """
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
        import os
        
        if not plaintext:
            return plaintext
        
        # Decode the base64 key
        key = base64.b64decode(self.encryption_key)
        
        # Generate a random nonce
        nonce = os.urandom(12)
        
        # Create AESGCM cipher
        aesgcm = AESGCM(key)
        
        # Encrypt the plaintext
        ciphertext = aesgcm.encrypt(nonce, plaintext.encode('utf-8'), None)
        
        # Combine nonce and ciphertext
        encrypted = nonce + ciphertext
        
        # Return base64 encoded result
        return base64.b64encode(encrypted).decode('utf-8')
    
    def decrypt_text_sync(self, encrypted_text: str) -> str:
        """
        Synchronous decryption using Python's cryptography library
        This is a fallback for cases where database session is not available
        
        Args:
            encrypted_text: Base64 encoded encrypted text
            
        Returns:
            Decrypted plaintext
        """
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
        
        if not encrypted_text:
            return encrypted_text
        
        # Decode the base64 key
        key = base64.b64decode(self.encryption_key)
        
        # Decode the encrypted text
        encrypted = base64.b64decode(encrypted_text)
        
        # Extract nonce and ciphertext
        nonce = encrypted[:12]
        ciphertext = encrypted[12:]
        
        # Create AESGCM cipher
        aesgcm = AESGCM(key)
        
        # Decrypt the ciphertext
        plaintext = aesgcm.decrypt(nonce, ciphertext, None)
        
        return plaintext.decode('utf-8')


# Global encryption service instance
encryption_service = EncryptionService()


async def encrypt_sensitive_fields(db: AsyncSession, data: dict, fields: list[str]) -> dict:
    """
    Encrypt specified fields in a dictionary
    
    Args:
        db: Database session
        data: Dictionary containing data
        fields: List of field names to encrypt
        
    Returns:
        Dictionary with encrypted fields
    """
    encrypted_data = data.copy()
    for field in fields:
        if field in encrypted_data and encrypted_data[field] is not None:
            encrypted_data[field] = await encryption_service.encrypt_text(db, str(encrypted_data[field]))
    return encrypted_data


async def decrypt_sensitive_fields(db: AsyncSession, data: dict, fields: list[str]) -> dict:
    """
    Decrypt specified fields in a dictionary
    
    Args:
        db: Database session
        data: Dictionary containing encrypted data
        fields: List of field names to decrypt
        
    Returns:
        Dictionary with decrypted fields
    """
    decrypted_data = data.copy()
    for field in fields:
        if field in decrypted_data and decrypted_data[field] is not None:
            decrypted_data[field] = await encryption_service.decrypt_text(db, decrypted_data[field])
    return decrypted_data


# List of sensitive fields that should be encrypted at rest
SENSITIVE_FIELDS = {
    'consent_records': ['signature_data'],
    'transcripts': ['raw_text', 'segments', 'speakers'],
    'clinical_data_records': ['extracted_data', 'validated_data', 'validation_status'],
    'submission_records': ['payload'],
    'audit_logs': ['details'],
}
