from cryptography.fernet import Fernet

key = Fernet.generate_key()  # Generate a key
with open("symmetric.key", "wb") as f:
    f.write(key)

print("Symmetric key generated:", key)
