import speech_recognition as sr
from pydub import AudioSegment
import tempfile


def convert_mp3_to_text(mp3_file):

    """Takes MP3 file and convert it to text file with speech to reconition """

    # upload MP3 using pydub
    audio = AudioSegment.from_mp3(mp3_file)

    # Créer un fichier temporaire pour le fichier audio
    with tempfile.NamedTemporaryFile(suffix=".wav") as temp_audio:
        temp_file_path = temp_audio.name
       
        # Exporter le fichier audio temporaire au format WAV
        audio.export(temp_file_path, format="wav")

        # Utiliser SpeechRecognition pour la reconnaissance vocale
        recognizer = sr.Recognizer()

        with sr.AudioFile(temp_file_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)


    return text

# Exemple d'utilisation
mp3_file = "/workspaces/Microservices/sample-1.mp3"
text = convert_mp3_to_text(mp3_file)
print(text)
