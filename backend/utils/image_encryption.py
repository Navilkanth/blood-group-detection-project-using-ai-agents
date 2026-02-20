from cryptography.fernet import Fernet
import os

class ImageEncryption:
    """Encrypt/decrypt images for secure storage"""
    
    def __init__(self, key_path: str = ".encryption_key"):
        self.key_path = key_path
        self.cipher = self._get_or_create_key()
    
    def _get_or_create_key(self):
        """Get existing key or create new one"""
        if os.path.exists(self.key_path):
            with open(self.key_path, "rb") as f:
                key = f.read()
        else:
            key = Fernet.generate_key()
            with open(self.key_path, "wb") as f:
                f.write(key)
        
        return Fernet(key)
    
    def encrypt_image(self, image_path: str) -> bytes:
        """Encrypt image file"""
        with open(image_path, "rb") as f:
            image_data = f.read()
        return self.cipher.encrypt(image_data)
    
    def decrypt_image(self, encrypted_data: bytes, output_path: str):
        """Decrypt image data to file"""
        decrypted_data = self.cipher.decrypt(encrypted_data)
        with open(output_path, "wb") as f:
            f.write(decrypted_data)
