# encryption.py - Encryption/Decryption Module

import os
import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from config import RSA_KEY_SIZE, AES_KEY_SIZE, IV_SIZE

def generate_keys():
    """Generate RSA private and public keys."""
    private_key = rsa.generate_private_key(
        public_exponent=65537, 
        key_size=RSA_KEY_SIZE, 
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key

def serialize_public_key(public_key):
    """Serialize a public key to PEM format."""
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

def deserialize_public_key(pem_data):
    """Deserialize a public key from PEM format."""
    return serialization.load_pem_public_key(pem_data, backend=default_backend())

def encrypt_message(public_key, message):
    """Encrypt a message using AES-256 and RSA-4096."""
    # Generate AES key and IV
    aes_key = os.urandom(AES_KEY_SIZE)
    iv = os.urandom(IV_SIZE)
    
    # Encrypt message with AES
    cipher = Cipher(
        algorithms.AES(aes_key), 
        modes.CFB(iv), 
        backend=default_backend()
    )
    encryptor = cipher.encryptor()
    encrypted_message = encryptor.update(message.encode()) + encryptor.finalize()
    
    # Encrypt AES key with RSA
    encrypted_aes_key = public_key.encrypt(
        aes_key, 
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()), 
            algorithm=hashes.SHA256(), 
            label=None
        )
    )
    
    # Return base64 encoded values
    return (
        base64.b64encode(encrypted_aes_key).decode(),
        base64.b64encode(iv).decode(),
        base64.b64encode(encrypted_message).decode()
    )

def decrypt_message(private_key, encrypted_aes_key_b64, iv_b64, encrypted_message_b64):
    """Decrypt a message using AES-256 and RSA-4096."""
    # Decode from base64
    encrypted_aes_key = base64.b64decode(encrypted_aes_key_b64)
    iv = base64.b64decode(iv_b64)
    encrypted_message = base64.b64decode(encrypted_message_b64)
    
    # Decrypt AES key with RSA
    aes_key = private_key.decrypt(
        encrypted_aes_key, 
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()), 
            algorithm=hashes.SHA256(), 
            label=None
        )
    )
    
    # Decrypt message with AES
    cipher = Cipher(
        algorithms.AES(aes_key), 
        modes.CFB(iv), 
        backend=default_backend()
    )
    decryptor = cipher.decryptor()
    decrypted_message = decryptor.update(encrypted_message) + decryptor.finalize()
    
    return decrypted_message.decode()