# Rake

A lightweight local cryptographic locker utility written in Python. 

## Why I Built This
Most encryption tools or password managers are bloated, require cloud accounts, or force you through heavy setup processes just to securely hide a few sensitive text strings or passwords. I wanted something dead-simple, completely local, and lightweight that lives right on the machine without any internet connection or third-party tracking. 

## Under the Hood
* **Encryption:** Uses AES-128 in CBC mode via the industry-standard `cryptography` library (`Fernet`).
* **Key Derivation:** Uses **PBKDF2 with SHA-256** and 100,000 iterations combined with a unique random salt per entry to securely turn your passphrase into an encryption key.
* **Privacy:** **What it does not do:** It doesn't use heavy databases, requires no external dependencies if you use the pre-compiled binary, and **never** sends your data or keys anywhere over the internet—everything stays completely on your machine.

## How to Run It

If you downloaded the pre-compiled binary file, open your terminal in the folder where the file is saved, make it executable, and run it with these commands:

```bash
chmod +x rake
./rake
