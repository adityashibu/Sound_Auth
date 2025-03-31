import streamlit as st
import ggwave
import pyaudio

# Function to play the waveform using PyAudio
def play_audio(waveform):
    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paFloat32, channels=1, rate=48000, output=True, frames_per_buffer=4096)
    stream.write(waveform, len(waveform)//4)
    stream.stop_stream()
    stream.close()

    p.terminate()

# Streamlit UI elements
st.title("GGWave Audio Encoder")

# Input from the user (text to encode)
input_text = st.text_input("Enter text to encode:", "hello python")

# Slider to adjust volume
volume = st.slider("Select volume level:", min_value=1, max_value=100, value=20)

# Dropdown to select Tx protocol
protocol_options = {
    0: "Normal",
    1: "Fast",
    2: "Fastest",
    3: "[U] Normal",
    4: "[U] Fast",
    5: "[U] Fastest",
    6: "[DT] Normal",
    7: "[DT] Fast",
    8: "[DT] Fastest",
    9: "[MT] Normal",
    10: "[MT] Fast",
    11: "[MT] Fastest"
}

# Display the protocol selection dropdown
protocol_choice = st.selectbox("Select Tx protocol:", list(protocol_options.values()))

# Map the selected protocol string to protocol ID
protocol_id = list(protocol_options.keys())[list(protocol_options.values()).index(protocol_choice)]

# Button to encode and play the audio
if st.button("Play Encoded Audio"):
    if input_text:
        # Encode the input text to audio waveform with selected protocol
        waveform = ggwave.encode(input_text, protocolId=protocol_id, volume=volume)
        
        # Play the audio
        st.write(f"Transmitting text: '{input_text}' with protocol: {protocol_choice}")
        play_audio(waveform)
    else:
        st.warning("Please enter some text to encode.")
