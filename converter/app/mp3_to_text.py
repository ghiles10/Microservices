import requests 
import tempfile

import speech_recognition as sr
from pydub import AudioSegment

def convert_mp3_to_text(mp3_file):
    # Charger le fichier MP3 en utilisant pydub
    audio = AudioSegment.from_mp3(mp3_file)

    # Convertir en format audio reconnu par SpeechRecognition (WAV mono 16kHz)
    audio.export("temp.wav", format="wav")

    # Utiliser SpeechRecognition pour la reconnaissance vocale
    recognizer = sr.Recognizer()

    with sr.AudioFile("temp.wav") as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data, language='fr-FR')

    return text

# Exemple d'utilisation
mp3_file = "example.mp3"
text = convert_mp3_to_text(mp3_file)
print(text)
