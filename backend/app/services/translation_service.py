from google.cloud import translate
import os
from google.oauth2 import service_account

class TranslationService:
    def __init__(self):
        # Load credentials
        credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        if credentials_path and os.path.exists(credentials_path):
            credentials = service_account.Credentials.from_service_account_file(credentials_path)
            self.client = translate.TranslationServiceClient(credentials=credentials)
            print(f"Translation client initialized with credentials from: {credentials_path}")
        else:
            print(f"WARNING: Credentials not found at: {credentials_path}")
            self.client = translate.TranslationServiceClient()
            
        self.project_id = "prime-service-458411-j6"
        
    async def translate_text(self, text: str, source_language: str, target_language: str):
        """
        Translate text from source language to target language
        """
        try:
            parent = f"projects/{self.project_id}"
            
            response = self.client.translate_text(
                request={
                    "parent": parent,
                    "contents": [text],
                    "mime_type": "text/plain",
                    "source_language_code": source_language,
                    "target_language_code": target_language,
                }
            )

            if not response.translations:
                return None

            translation = response.translations[0].translated_text
            return translation

        except Exception as e:
            print(f"Error in translation: {str(e)}")
            return None 