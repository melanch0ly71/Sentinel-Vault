import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class SentinelEngine:
    def __init__(self, password: str, salt=None):
        self.password = password.encode()
        # If no salt is provided (encryption), create a new 16-byte random salt
        self.salt = salt if salt else os.urandom(16)
        self.key = self._derive_key()

    def _derive_key(self):
        """Stretches the password into a 256-bit AES key."""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32, # 32 bytes = 256 bits
            salt=self.salt,
            iterations=480000,
        )
        return kdf.derive(self.password)

    def encrypt_data(self, data: bytes) -> bytes:
        """Encrypts raw bytes using AES-GCM."""
        aesgcm = AESGCM(self.key)
        nonce = os.urandom(12) # GCM needs a unique 12-byte nonce
        ciphertext = aesgcm.encrypt(nonce, data, None)
        # We store the salt and nonce WITH the ciphertext so we can decrypt later
        return self.salt + nonce + ciphertext

    @staticmethod
    def decrypt_data(password: str, encrypted_blob: bytes) -> bytes:
        """Extracts salt/nonce and decrypts the data."""
        salt = encrypted_blob[:16]
        nonce = encrypted_blob[16:28]
        ciphertext = encrypted_blob[28:]
        
        # Re-derive the key using the extracted salt
        engine = SentinelEngine(password, salt=salt)
        aesgcm = AESGCM(engine.key)
        
        return aesgcm.decrypt(nonce, ciphertext, None)

# --- QUICK TEST ---
if __name__ == "__main__":
    msg = b"Sensitive Cybersecurity Data"
    pwd = "Student_Sophisticated_PWD_2026"
    
    # Encrypt
    engine = SentinelEngine(pwd)
    encrypted = engine.encrypt_data(msg)
    print(f"Encrypted Blob: {encrypted.hex()[:50]}...")

    # Decrypt
    decrypted = SentinelEngine.decrypt_data(pwd, encrypted)
    print(f"Decrypted Result: {decrypted.decode()}")