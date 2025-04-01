import ggwave
import pyaudio
import time
import zlib
import base64
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization

# Load the public key
with open("public_key.pem", "rb") as f:
    public_key = serialization.load_pem_public_key(f.read())

# Function to compress and encrypt the message using RSA and then Base64 encode it
def encrypt_message(message: str) -> str:
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

# Function to play GGWave audio
def play_audio(waveform):
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32, channels=1, rate=48000, output=True, frames_per_buffer=4096)
    
    # Play the waveform
    stream.write(waveform, len(waveform)//4)
    
    # Keep the stream open for as long as the waveform duration
    time.sleep(len(waveform) / 48000)  # Duration in seconds based on 48000 Hz sampling rate
    
    stream.stop_stream()
    stream.close()
    p.terminate()

# Get input message
message = input("Enter message to send: ")

# Encrypt the message using the updated encryption function
encrypted_message = encrypt_message(message)

if encrypted_message:
    print("Encrypted message (Base64 encoded):")
    print(encrypted_message)

    # Encode the encrypted message using GGWave (using T5 ultrasound mode)
    waveform = ggwave.encode(encrypted_message, protocolId=5, volume=50)

    print("Transmitting encrypted message...")

    # Play the audio, ensuring it stays open for the duration of the message
    play_audio(waveform)

    print("Transmission complete.")
else:
    print("Failed to encrypt the message.")
