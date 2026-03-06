from google.cloud import texttospeech
import os
from google.oauth2 import service_account

class TextToSpeechService:
    def __init__(self):
        # Load credentials
        credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        if credentials_path and os.path.exists(credentials_path):
            credentials = service_account.Credentials.from_service_account_file(credentials_path)
            self.client = texttospeech.TextToSpeechClient(credentials=credentials)
            print(f"Text-to-Speech client initialized with credentials from: {credentials_path}")
        else:
            print(f"WARNING: Credentials not found at: {credentials_path}")
            self.client = texttospeech.TextToSpeechClient()

    async def synthesize_speech(self, text: str, language_code: str = "tr-TR"):
        """
        Convert text to speech using Google Cloud Text-to-Speech
        """
        try:
            synthesis_input = texttospeech.SynthesisInput(text=text)

            voice = texttospeech.VoiceSelectionParams(
                language_code=language_code,
                ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
            )

            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3,
                speaking_rate=1.0,
                pitch=0
            )

            response = self.client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )

            return response.audio_content

        except Exception as e:
            print(f"Error in text to speech conversion: {str(e)}")
            return None 