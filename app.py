import streamlit as st
import pyttsx3
import speech_recognition as sr
import requests
import os

# Function for Text-to-Speech (TTS)
def text_to_speech(text, filename="output_audio.wav"):
    engine = pyttsx3.init()  # Initialize pyttsx3 engine
    
    # Set properties (optional)
    engine.setProperty('rate', 150)  # Speed of speech (lower for slower speech)
    engine.setProperty('volume', 1)  # Volume (0.0 to 1.0)
    
    # List available voices
    voices = engine.getProperty('voices')
    
    # Set a more natural-sounding voice
    engine.setProperty('voice', voices[1].id)  # Choose another voice, usually index 1 is a more natural voice

    # Save speech as a .wav file
    engine.save_to_file(text, filename)
    print(f"Audio saved as {filename}")
    
    # Run the speech engine to generate the audio
    engine.runAndWait()

# Function for Speech-to-Text (STT)
def speech_to_text():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    print("Listening for your speech...")

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
        audio = recognizer.listen(source)

    try:
        print("Converting audio to text...")
        text = recognizer.recognize_google(audio)  # Recognize speech using Google's recognizer
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that.")
        return None
    except sr.RequestError as e:
        print(f"Error with the speech recognition service; {e}")
        return None

# Function to send text to middle bot and get response
def send_to_middle_bot(text):
    middle_bot_url = "https://5754-47-241-205-66.ngrok-free.app/process_text"  # URL of the middle bot
    
    # Sending the text to the middle bot
    response = requests.post(middle_bot_url, json={"text": text})
    
    if response.status_code == 200:
        print("Response from middle bot:", response.json())  # Printing the response from middle bot
        return response.json().get('response')  # Extract the 'response' field from the response JSON
    else:
        print(f"Error sending data to middle bot: {response.status_code}")
        return None

# Streamlit app
def chatbot_app():
    st.title("Government Service Bot")
    
    # Choose input mode (Text or Speech)
    input_mode = st.radio("Choose message type:", ("Text", "Speech"))

    if input_mode == "Text":
        user_input = st.text_input("Enter your text:")
        
        if st.button("Send"):
            if user_input:
                st.write(f"You: {user_input}")
                response_text = send_to_middle_bot(user_input)
                if response_text:
                    st.write(f"Agent: {response_text}")
                    # Convert the text response to audio
                    text_to_speech(response_text, "response_audio.wav")
                    # Play the audio response
                    st.audio("response_audio.wav")
            else:
                st.write("Please enter some text.")
    
    elif input_mode == "Speech":
        if st.button("Start"):
            # Record speech and convert to text
            spoken_text = speech_to_text()
            if spoken_text:
                st.write(f"Your speech: {spoken_text}")
                response_text = send_to_middle_bot(spoken_text)
                if response_text:
                    st.write(f"Agent: {response_text}")
                    # Convert the text response to audio
                    text_to_speech(response_text, "response_audio.wav")
                    # Play the audio response
                    st.audio("response_audio.wav")
            else:
                st.write("No speech detected.")

# Run the app
if __name__ == "__main__":
    chatbot_app()
