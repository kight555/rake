import os
import sys
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def generate_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

def encrypt_text(text: str, password: str) -> str:
    salt = os.urandom(16)
    key = generate_key(password, salt)
    f = Fernet(key)
    token = f.encrypt(text.encode())
    return base64.urlsafe_b64encode(salt + token).decode()

def decrypt_text(encrypted_data: str, password: str) -> str:
    decoded = base64.urlsafe_b64decode(encrypted_data.encode())
    salt = decoded[:16]
    token = decoded[16:]
    key = generate_key(password, salt)
    f = Fernet(key)
    return f.decrypt(token).decode()

def main():
    print("--- MINIMALIST LOCAL LOCKER ---")
    choice = input("Do you want to (E)ncrypt or (D)ecrypt? ").strip().upper()
    
    if choice == 'E':
        text = input("Enter the secret text to lock: ")
        pwd = input("Enter your passphrase: ")
        encrypted = encrypt_text(text, pwd)
        print("\n[LOCKED RESULT]:")
        print(encrypted)
        print("\nSave this string. Without your passphrase, it's unrecoverable.")
        
    elif choice == 'D':
        encrypted = input("Paste the locked string: ")
        pwd = input("Enter your passphrase: ")
        try:
            decrypted = decrypt_text(encrypted, pwd)
            print("\n[UNLOCKED RESULT]:")
            print(decrypted)
        except Exception:
            print("\n[ERROR]: Decryption failed. Wrong passphrase or broken string.")
    else:
        print("Invalid choice. Run it again and pick E or D.")

if __name__ == "__main__":
    main()
