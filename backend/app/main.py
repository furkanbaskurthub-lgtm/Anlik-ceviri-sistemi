from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import socketio
from dotenv import load_dotenv
import os
from typing import Dict, List

from app.services.speech_service import SpeechService
from app.services.translation_service import TranslationService
from app.services.tts_service import TextToSpeechService
from app.services.user_service import UserService
from app.routes import auth

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Real-time Translation Service")

# Initialize services
speech_service = SpeechService()
translation_service = TranslationService()
tts_service = TextToSpeechService()

# Initialize Socket.IO
sio = socketio.AsyncServer(cors_allowed_origins='*', async_mode='asgi')
socket_app = socketio.ASGIApp(sio, app)

# Store active users and their socket IDs
active_users = {}
# Store active calls
active_calls = {}
# Store friend requests and friends
friend_requests: Dict[str, List[str]] = {}  # username -> [requesting_usernames]
friends: Dict[str, List[str]] = {}  # username -> [friend_usernames]

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["authentication"])

# Socket.IO events
@sio.on('connect')
async def connect(sid, environ):
    print(f'Client connected: {sid}')

@sio.on('disconnect')
async def disconnect(sid):
    username = next((user for user, s_id in active_users.items() if s_id == sid), None)
    if username:
        # Kullanıcının online durumunu güncelle
        await UserService.update_online_status(username, False)
        del active_users[username]
        # Notify other users about offline status
        await sio.emit('user_offline', {'username': username}, skip_sid=sid)
    print(f'Client disconnected: {sid}')

@sio.on('register_user')
async def register_user(sid, data):
    username = data.get('username')
    if username:
        # Kullanıcının online durumunu güncelle
        await UserService.update_online_status(username, True)
        active_users[username] = sid
        # Notify other users about online status
        await sio.emit('user_online', {'username': username}, skip_sid=sid)

        # Kullanıcının arkadaş listesini getir ve her bir arkadaşın durumunu kontrol et
        friends = await UserService.get_friends(username)
        for friend in friends:
            friend_username = friend['username']
            if friend_username in active_users:
                # Arkadaşa kullanıcının online olduğunu bildir
                await sio.emit('user_online', {'username': username}, room=active_users[friend_username])
                # Kullanıcıya arkadaşının online olduğunu bildir
                await sio.emit('user_online', {'username': friend_username}, room=sid)

@sio.on('call_user')
async def call_user(sid, data):
    caller_username = data.get('caller')
    callee_username = data.get('callee')
    offer = data.get('offer')
    
    if not caller_username or not callee_username or not offer:
        await sio.emit('error', {'message': 'Invalid call data'}, room=sid)
        return
        
    if callee_username not in active_users:
        await sio.emit('error', {'message': 'User is not online'}, room=sid)
        return
        
    # Arama bildirimini hedef kullanıcıya gönder
    callee_sid = active_users[callee_username]
    await sio.emit('incoming_call', {
        'caller': caller_username,
        'offer': offer
    }, room=callee_sid)

@sio.on('call_response')
async def call_response(sid, data):
    caller_username = data.get('caller')
    answer = data.get('answer')
    accepted = data.get('accepted')
    
    if not caller_username or not accepted:
        await sio.emit('error', {'message': 'Invalid response data'}, room=sid)
        return
        
    if caller_username not in active_users:
        await sio.emit('error', {'message': 'Caller is not online'}, room=sid)
        return
        
    caller_sid = active_users[caller_username]
    
    if accepted:
        if not answer:
            await sio.emit('error', {'message': 'Missing answer data'}, room=sid)
            return
            
        # Kabul edildiğinde answer'ı gönder
        await sio.emit('call_accepted', {
            'answer': answer
        }, room=caller_sid)
    else:
        # Reddedildiğinde bildir
        await sio.emit('call_rejected', room=caller_sid)

@sio.on('ice_candidate')
async def handle_ice_candidate(sid, data):
    target_username = data.get('target')
    candidate = data.get('candidate')
    
    if not target_username or not candidate:
        await sio.emit('error', {'message': 'Invalid ICE candidate data'}, room=sid)
        return
        
    if target_username not in active_users:
        await sio.emit('error', {'message': 'Target user is not online'}, room=sid)
        return
        
    # ICE adayını karşı tarafa ilet
    target_sid = active_users[target_username]
    await sio.emit('ice_candidate', {
        'candidate': candidate
    }, room=target_sid)

@sio.on('end_call')
async def end_call(sid, data):
    target_username = data.get('target')
    
    if not target_username:
        await sio.emit('error', {'message': 'Invalid end call data'}, room=sid)
        return
        
    if target_username in active_users:
        # Karşı tarafa aramanın sonlandırıldığını bildir
        target_sid = active_users[target_username]
        await sio.emit('call_ended', room=target_sid)

@sio.on('real_time_audio')
async def handle_real_time_audio(sid, data):
    """Real-time audio translation during call"""
    try:
        target_username = data.get('target')
        audio_chunk = data.get('audio')
        source_lang = data.get('source_language', 'tr')
        target_lang = data.get('target_language', 'en')
        
        if not target_username or not audio_chunk:
            return
        
        # Language code mapping for Speech-to-Text
        speech_lang_map = {
            'tr': 'tr-TR',
            'en': 'en-US',
            'es': 'es-ES',
            'fr': 'fr-FR',
            'de': 'de-DE',
            'it': 'it-IT',
            'pt': 'pt-PT',
            'ru': 'ru-RU',
            'ja': 'ja-JP',
            'ko': 'ko-KR',
            'zh': 'zh-CN',
            'ar': 'ar-SA'
        }
        
        # Language code mapping for Text-to-Speech
        tts_lang_map = {
            'tr': 'tr-TR',
            'en': 'en-US',
            'es': 'es-ES',
            'fr': 'fr-FR',
            'de': 'de-DE',
            'it': 'it-IT',
            'pt': 'pt-PT',
            'ru': 'ru-RU',
            'ja': 'ja-JP',
            'ko': 'ko-KR',
            'zh': 'zh-CN',
            'ar': 'ar-SA'
        }
            
        source_lang_code = speech_lang_map.get(source_lang, 'tr-TR')
        target_lang_code = tts_lang_map.get(target_lang, 'en-US')
        
        # 1. Speech to Text
        text = await speech_service.transcribe_audio(
            audio_content=audio_chunk,
            language_code=source_lang_code
        )
        
        if not text or len(text.strip()) == 0:
            return
            
        print(f"Transcribed: {text}")
            
        # 2. Translate
        translated_text = await translation_service.translate_text(
            text=text,
            source_language=source_lang,
            target_language=target_lang
        )
        
        if not translated_text:
            return
            
        print(f"Translated: {translated_text}")
            
        # 3. Text to Speech
        audio_content = await tts_service.synthesize_speech(
            text=translated_text,
            language_code=target_lang_code
        )
        
        if not audio_content:
            return
        
        # 4. Send to target user
        if target_username in active_users:
            target_sid = active_users[target_username]
            await sio.emit('translated_audio', {
                'audio': audio_content,
                'original_text': text,
                'translated_text': translated_text
            }, room=target_sid)
            
    except Exception as e:
        print(f"Error in real-time translation: {str(e)}")

# Original audio translation handler
@sio.on('audio_data')
async def handle_audio(sid, data):
    try:
        # 1. Convert audio to text
        text = await speech_service.transcribe_audio(
            audio_content=data['audio'],
            language_code=data.get('source_language', 'tr-TR')
        )
        
        if not text:
            await sio.emit('error', {'message': 'No speech detected'}, room=sid)
            return

        # 2. Translate text
        translated_text = await translation_service.translate_text(
            text=text,
            source_language=data.get('source_language', 'tr'),
            target_language=data.get('target_language', 'en')
        )
        
        if not translated_text:
            await sio.emit('error', {'message': 'Translation failed'}, room=sid)
            return

        # 3. Convert translated text to audio
        audio_content = await tts_service.synthesize_speech(
            text=translated_text,
            language_code=data.get('target_language', 'en-US')
        )

        # 4. Send results back to client
        await sio.emit('translation_result', {
            'original_text': text,
            'translated_text': translated_text,
            'audio': audio_content
        }, room=sid)

    except Exception as e:
        print(f"Error processing audio: {str(e)}")
        await sio.emit('error', {'message': 'Error processing audio'}, room=sid)

@sio.on('friend_request')
async def handle_friend_request(sid, data):
    from_user = data.get('from')
    to_user = data.get('to')
    
    if not from_user or not to_user:
        await sio.emit('error', {'message': 'Invalid friend request data'}, room=sid)
        return
        
    if to_user not in active_users:
        await sio.emit('error', {'message': 'User is not online'}, room=sid)
        return
        
    # MongoDB'ye arkadaşlık isteğini kaydet
    success = await UserService.send_friend_request(from_user, to_user)
    if not success:
        await sio.emit('error', {'message': 'Friend request failed'}, room=sid)
        return
    
    # Notify target user about new friend request
    target_sid = active_users[to_user]
    await sio.emit('friend_request_received', {
        'from': from_user
    }, room=target_sid)
    
    # Confirm to sender that request was sent
    await sio.emit('friend_request_sent', {
        'to': to_user
    }, room=sid)

@sio.on('accept_friend_request')
async def handle_accept_friend_request(sid, data):
    from_user = data.get('from')
    to_user = data.get('to')
    
    if not from_user or not to_user:
        await sio.emit('error', {'message': 'Invalid request data'}, room=sid)
        return
        
    # MongoDB'de arkadaşlık isteğini kabul et
    success = await UserService.accept_friend_request(to_user, from_user)
    if not success:
        await sio.emit('error', {'message': 'Failed to accept friend request'}, room=sid)
        return
    
    # Her iki kullanıcının arkadaş listesini güncelle
    if from_user in active_users:
        # From user'ın arkadaş listesini güncelle
        friends = await UserService.get_friends(from_user)
        await sio.emit('friends_list', {'friends': friends}, room=active_users[from_user])
        
    # To user'ın arkadaş listesini güncelle
    friends = await UserService.get_friends(to_user)
    await sio.emit('friends_list', {'friends': friends}, room=sid)
    
    # Her iki kullanıcıya bildirim gönder
    if from_user in active_users:
        await sio.emit('friend_request_accepted', {
            'username': to_user
        }, room=active_users[from_user])
        
    await sio.emit('friend_request_accepted', {
        'username': from_user
    }, room=sid)

@sio.on('reject_friend_request')
async def handle_reject_friend_request(sid, data):
    from_user = data.get('from')
    to_user = data.get('to')
    
    if not from_user or not to_user:
        await sio.emit('error', {'message': 'Invalid request data'}, room=sid)
        return
        
    # MongoDB'de arkadaşlık isteğini reddet
    success = await UserService.reject_friend_request(to_user, from_user)
    if not success:
        await sio.emit('error', {'message': 'Failed to reject friend request'}, room=sid)
        return
    
    # Notify requesting user if online
    if from_user in active_users:
        await sio.emit('friend_request_rejected', {
            'username': to_user
        }, room=active_users[from_user])

@sio.on('get_friend_requests')
async def handle_get_friend_requests(sid, data):
    username = data.get('username')
    
    if not username:
        await sio.emit('error', {'message': 'Invalid request'}, room=sid)
        return
        
    # MongoDB'den arkadaşlık isteklerini getir
    requests = await UserService.get_friend_requests(username)
    await sio.emit('friend_requests_list', {
        'requests': requests
    }, room=sid)

@sio.on('get_friends')
async def handle_get_friends(sid, data):
    username = data.get('username')
    
    if not username:
        await sio.emit('error', {'message': 'Invalid request'}, room=sid)
        return
        
    # MongoDB'den arkadaş listesini getir
    friends = await UserService.get_friends(username)
    await sio.emit('friends_list', {
        'friends': friends
    }, room=sid)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# For running the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:socket_app", host="0.0.0.0", port=8000, reload=True) 