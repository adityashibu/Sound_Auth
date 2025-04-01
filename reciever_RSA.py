import ggwave
import pyaudio
import logging
import base64
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives import hashes
import zlib

# Load the private key
with open("private_key.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(f.read(), password=None)

# Maximum size for RSA decryption (depends on key size)
MAX_RSA_KEY_SIZE = 245  # Example for 2048-bit RSA (2048 bits = 256 bytes, minus padding)

# Function to decrypt message
def decrypt_message(encrypted_message: str) -> str:
    encrypted_chunks = encrypted_message.split("|")  # Split the message by '|'
    decrypted_message = b""
    
    for encrypted_chunk in encrypted_chunks:
        encrypted_chunk_bytes = base64.b64decode(encrypted_chunk)  # Base64 decode each chunk
        decrypted_chunk = private_key.decrypt(
            encrypted_chunk_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        decrypted_message += decrypted_chunk  # Combine decrypted chunks
    
    decompressed_message = zlib.decompress(decrypted_message).decode("utf-8")  # Decompress the message
    return decompressed_message

# Initialize PyAudio for listening
p = pyaudio.PyAudio()

# Open the audio stream
stream = p.open(
    format=pyaudio.paFloat32, 
    channels=1, 
    rate=48000,  # Adjust sample rate if necessary (e.g., 96000 or 192000)
    input=True, 
    frames_per_buffer=2048  # Increase buffer size if needed
)

# Log the start of listening
print('Listening ... Press Ctrl+C to stop')

# Initialize GGWave instance
instance = ggwave.init()

# Configure logging for error handling
logging.basicConfig(level=logging.DEBUG)

try:
    while True:
        # Read incoming audio data
        try:
            data = stream.read(2048, exception_on_overflow=False)
        except IOError as e:
            logging.error(f"Error reading audio stream: {e}")
            continue  # Skip to the next iteration if reading fails
        
        # Decode GGWave transmission
        try:
            res = ggwave.decode(instance, data)
            
            if res:  # If a message was received
                print(f"Received {len(res)} bytes of data.")
                try:
                    encrypted_message = res.decode("utf-8")  # Attempt to decode
                    print(f"Received encrypted message: {encrypted_message}")
                    decrypted_message = decrypt_message(encrypted_message)  # Decrypt the message
                    print(f"Decrypted message: {decrypted_message}")
                except UnicodeDecodeError:
                    logging.error("Error decoding the received message.")
        except Exception as e:
            logging.error(f"Error decoding GGWave data: {e}")
except KeyboardInterrupt:
    print("\n[!] Stopping receiver")

finally:
    # Clean up GGWave instance and PyAudio stream
    ggwave.free(instance)
    stream.stop_stream()
    stream.close()
    p.terminate()
