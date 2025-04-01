from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives import padding as sym_padding
import base64
import zlib

# Load the private key
with open("private_key.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(f.read(), password=None)

# Ciphertext you want to decrypt (replace this with your actual Base64-encoded data)
ciphertext = "jajKevZz95yVSuFaehSl733wvpap/gSlk+9a1DtV9sp6sRpDQ1cfo17XrcNMmzJ64GqAhmjhkNwKI7ZHWcLRrYDsMWma39vMzcpXSFnEeBCRcm6rsXB+lBiPW+tqBHA25Und3SHTzeq+"

# Decode the ciphertext from Base64
ciphertext_bytes = base64.b64decode(ciphertext)

# Decrypt the message using RSA private key
try:
    # Perform RSA decryption using OAEP padding
    decrypted_message = private_key.decrypt(
        ciphertext_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # If the message was compressed, decompress it (unzip)
    # (Assuming the message was compressed using zlib before encryption)
    decrypted_message = zlib.decompress(decrypted_message).decode('utf-8')  # Assuming it's a string

    print("Decrypted message:", decrypted_message)

except Exception as e:
    print(f"Error decrypting the message: {e}")
