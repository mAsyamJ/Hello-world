# voice_of_the_patient.py
import logging
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO
import os
from groq import Groq

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def record_audio(file_path, timeout=20, phrase_time_limit=None):
    """
    Simplified function to record audio from the microphone and save it as an MP3 file.

    Args:
    file_path (str): Path to save the recorded audio file.
    timeout (int): Maximum time to wait for a phrase to start (in seconds).
    phrase_time_limit (int): Maximum time for the phrase to be recorded (in seconds).
    """
    recognizer = sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
            logging.info("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=2)  # Increase duration for better noise adjustment
            logging.info("Start speaking now...")
            
            # Record the audio
            audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            logging.info("Recording complete.")
            
            # Convert the recorded audio to an MP3 file
            wav_data = audio_data.get_wav_data()
            audio_segment = AudioSegment.from_wav(BytesIO(wav_data))
            audio_segment.export(file_path, format="mp3", bitrate="128k")
            
            logging.info(f"Audio saved to {file_path}")

    except sr.WaitTimeoutError:
        logging.error("No speech detected within the timeout period.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

def transcribe_with_groq(audio_filepath, GROQ_API_KEY, stt_model="whisper-large-v3"):
    """
    Transcribe audio using Groq's API.

    Args:
    audio_filepath (str): Path to the audio file.
    GROQ_API_KEY (str): Groq API key.
    stt_model (str): Speech-to-text model to use (default: "whisper-large-v3").

    Returns:
    str: Transcribed text.
    """
    client = Groq(api_key=GROQ_API_KEY)
    
    try:
        with open(audio_filepath, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model=stt_model,
                file=audio_file,
                language="en"
            )
        return transcription.text
    except Exception as e:
        logging.error(f"An error occurred during transcription: {e}")
        return None

# Example usage
# audio_filepath = "patient_voice_test_for_patient.mp3"
# record_audio(file_path=audio_filepath)
# transcription = transcribe_with_groq(audio_filepath, os.environ.get("GROQ_API_KEY"))
# print(transcription)