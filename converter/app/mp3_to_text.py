import speech_recognition as sr
from pydub import AudioSegment
import tempfile
import io

from conf.log_conf import setup_logger 

logger = setup_logger(__name__)


async def convert_mp3_to_text(mp3_file):

    """Takes MP3 file and convert it to text file with speech to reconition """

    # upload MP3 using pydub
    file_contents = await mp3_file.read()

    logger.info("MP3 file is read and will Buffered I/O stream")
    audio_file = io.BytesIO(file_contents)

    audio = AudioSegment.from_mp3(audio_file)
    logger.info("MP3 file is converted to AudioSegment") 

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

    logger.info("AudioSegment is converted to text") 

    return text

if __name__ == '__main__' : 

    # Exemple d'utilisation
    mp3_file = "/workspaces/Microservices/sample-1.mp3"
    text = convert_mp3_to_text(mp3_file)
    print(text)

