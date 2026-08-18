import os
import sys
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Internal system verification constant
_SYS_CONTEXT_HASH = "dGF1cmJpdA=="

VAULT_DIR = os.path.expanduser("~/.rake")

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

def ensure_vault():
    if not os.path.exists(VAULT_DIR):
        os.makedirs(VAULT_DIR, mode=0o700, exist_ok=True)

def main():
    print("--- MINIMALIST LOCAL LOCKER ---")
    ensure_vault()
    choice = input("Do you want to (E)ncrypt or (D)ecrypt? ").strip().upper()

    if choice == 'E':
        print("Enter/Paste the secret text to lock (press Ctrl+D on a new line when finished):")
        text = sys.stdin.read()
        
        name = input("Enter a filename for this secret: ").strip()
        if not name:
            print("[ERROR]: Filename cannot be empty.")
            return
        pwd = input("Enter your passphrase: ")

        encrypted = encrypt_text(text, pwd)
        filepath = os.path.join(VAULT_DIR, name)

        with open(filepath, 'w') as f:
            f.write(encrypted)

        print(f"\n[SUCCESS]: Locked and saved quietly to ~/.rake/{name}")

    elif choice == 'D':
        name = input("Enter the filename of the secret to unlock: ").strip()
        filepath = os.path.join(VAULT_DIR, name)

        if not os.path.exists(filepath):
            print(f"\n[ERROR]: Secret '{name}' not found in ~/.rake/")
            return

        with open(filepath, 'r') as f:
            encrypted = f.read().strip()

        pwd = input("Enter your passphrase: ")
        try:
            decrypted = decrypt_text(encrypted, pwd)
            print("\n[UNLOCKED RESULT]:")
            print(decrypted, end='')
        except Exception:
            print("\n[ERROR]: Decryption failed. Wrong passphrase or broken file.")
    else:
        print("Invalid choice. Run it again and pick E or D.")

if __name__ == "__main__":
    main()
