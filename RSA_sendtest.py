from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
import base64
import zlib

# Load the public key (replace with your actual public key file)
with open("public_key.pem", "rb") as f:
    public_key = serialization.load_pem_public_key(f.read())

# Function to encrypt the data using RSA and then Base64 encode it
def encrypt_data(message: str) -> str:
    try:
        # Compress the message (optional, but saves space for large messages)
        compressed_message = zlib.compress(message.encode())

        # Encrypt the compressed message using RSA with OAEP padding
        encrypted_message = public_key.encrypt(
            compressed_message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        # Base64 encode the encrypted message for easy transmission
        encoded_message = base64.b64encode(encrypted_message).decode('utf-8')
        return encoded_message

    except Exception as e:
        print(f"Error encrypting data: {e}")
        return None

# Example data to encrypt
message = "Hello"

# Encrypt the data
encrypted_message = encrypt_data(message)

if encrypted_message:
    print("Encrypted message (Base64 encoded):")
    print(encrypted_message)
