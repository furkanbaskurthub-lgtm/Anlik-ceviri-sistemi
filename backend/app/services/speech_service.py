from google.cloud import speech
import os
from google.oauth2 import service_account

class SpeechService:
    def __init__(self):
        # Load credentials
        credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        if credentials_path and os.path.exists(credentials_path):
            credentials = service_account.Credentials.from_service_account_file(credentials_path)
            self.client = speech.SpeechClient(credentials=credentials)
            print(f"Speech-to-Text client initialized with credentials from: {credentials_path}")
        else:
            print(f"WARNING: Credentials not found at: {credentials_path}")
            self.client = speech.SpeechClient()

    async def transcribe_audio(self, audio_content: bytes, language_code: str = "tr-TR"):
        """
        Convert audio to text using Google Cloud Speech-to-Text
        """
        try:
            audio = speech.RecognitionAudio(content=audio_content)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,
                sample_rate_hertz=48000,
                language_code=language_code,
                enable_automatic_punctuation=True,
                model='default'
            )

            response = self.client.recognize(config=config, audio=audio)

            if not response.results:
                return None

            transcript = response.results[0].alternatives[0].transcript
            return transcript

        except Exception as e:
            print(f"Error in speech to text conversion: {str(e)}")
            return None 