"""
Google Cloud APIs Test Script
Bu script Google Cloud API'lerinin doğru çalışıp çalışmadığını test eder.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_credentials():
    """Test if credentials file exists"""
    creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    print(f"1. Credentials Path: {creds_path}")
    
    if not creds_path:
        print("   ❌ GOOGLE_APPLICATION_CREDENTIALS not set in .env")
        return False
    
    if not os.path.exists(creds_path):
        print(f"   ❌ Credentials file not found at: {creds_path}")
        return False
    
    print("   ✅ Credentials file found")
    return True

def test_speech_to_text():
    """Test Speech-to-Text API"""
    print("\n2. Testing Speech-to-Text API...")
    try:
        from google.cloud import speech
        client = speech.SpeechClient()
        print("   ✅ Speech-to-Text API initialized successfully")
        return True
    except Exception as e:
        print(f"   ❌ Speech-to-Text API error: {str(e)}")
        return False

def test_translation():
    """Test Translation API"""
    print("\n3. Testing Translation API...")
    try:
        from google.cloud import translate
        client = translate.TranslationServiceClient()
        print("   ✅ Translation API initialized successfully")
        return True
    except Exception as e:
        print(f"   ❌ Translation API error: {str(e)}")
        return False

def test_text_to_speech():
    """Test Text-to-Speech API"""
    print("\n4. Testing Text-to-Speech API...")
    try:
        from google.cloud import texttospeech
        client = texttospeech.TextToSpeechClient()
        print("   ✅ Text-to-Speech API initialized successfully")
        return True
    except Exception as e:
        print(f"   ❌ Text-to-Speech API error: {str(e)}")
        return False

def test_translation_functionality():
    """Test actual translation"""
    print("\n5. Testing Translation Functionality...")
    try:
        from google.cloud import translate
        client = translate.TranslationServiceClient()
        
        # Get project ID from credentials
        import json
        creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        with open(creds_path, 'r') as f:
            creds = json.load(f)
            project_id = creds.get('project_id')
        
        parent = f"projects/{project_id}"
        
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": ["Hello"],
                "mime_type": "text/plain",
                "source_language_code": "en",
                "target_language_code": "tr",
            }
        )
        
        translated = response.translations[0].translated_text
        print(f"   Test: 'Hello' → '{translated}'")
        print("   ✅ Translation working correctly")
        return True
    except Exception as e:
        print(f"   ❌ Translation test error: {str(e)}")
        return False

def main():
    print("=" * 60)
    print("Google Cloud APIs Test")
    print("=" * 60)
    
    results = []
    results.append(("Credentials", test_credentials()))
    results.append(("Speech-to-Text", test_speech_to_text()))
    results.append(("Translation", test_translation()))
    results.append(("Text-to-Speech", test_text_to_speech()))
    results.append(("Translation Test", test_translation_functionality()))
    
    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{name:20} {status}")
    
    all_passed = all(result for _, result in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 All tests passed! Your Google Cloud APIs are ready.")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print("\nCommon solutions:")
        print("1. Make sure all 3 APIs are enabled in Google Cloud Console")
        print("2. Check if service account has correct permissions")
        print("3. Verify credentials file path in .env")
        print("4. Wait a few minutes after enabling APIs")
    print("=" * 60)

if __name__ == "__main__":
    main()
