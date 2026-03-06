# Anlık Çeviri Sistemi - Test Rehberi

## Önemli Not
Bu sistem gerçek zamanlı video görüşme ve çeviri yapıyor. **Aynı bilgisayarda test yapmak için:**

### Seçenek 1: İki Farklı Tarayıcı (Önerilen)
1. Bir kullanıcı için **Chrome** kullanın
2. Diğer kullanıcı için **Firefox** veya **Edge** kullanın
3. Her tarayıcı kendi kamera/mikrofon erişimine sahip olacak

### Seçenek 2: İki Farklı Cihaz (En İyi)
1. Bir bilgisayar + bir telefon
2. İki farklı bilgisayar
3. Bilgisayar + tablet

## Test Adımları

### 1. Backend Başlatma
```cmd
cd backend
venv\Scripts\activate
python -m uvicorn app.main:socket_app --reload --port 8000
```

### 2. Frontend Başlatma
```cmd
cd frontend
npm start
```

### 3. Kullanıcı Kayıt ve Giriş
1. İlk tarayıcıda: `localhost:8081` açın
2. "Kayıt Ol" ile kullanıcı oluşturun (örn: kullanici1)
3. İkinci tarayıcıda: `localhost:8081` açın
4. "Kayıt Ol" ile başka kullanıcı oluşturun (örn: kullanici2)
5. Her iki tarayıcıda da giriş yapın

### 4. Arkadaş Ekleme
1. Kullanıcı1'de "Arkadaş Ekle" butonuna tıklayın
2. Kullanıcı2'nin kullanıcı adını girin
3. Kullanıcı2'de "İstekler" butonuna tıklayın
4. Gelen isteği kabul edin
5. Artık her iki tarafta da arkadaş listesinde görüneceksiniz

### 5. Çağrı Başlatma
1. Kullanıcı1'de arkadaş listesinden Kullanıcı2'yi bulun
2. "Ara" butonuna tıklayın
3. Kullanıcı2'de gelen çağrı bildirimi görünecek
4. Yeşil telefon ikonuna tıklayarak kabul edin

### 6. Çeviri Testi
1. Çağrı bağlandıktan sonra her iki tarafta da dil seçimi yapın
2. Örnek:
   - Kullanıcı1: Türkçe → İngilizce
   - Kullanıcı2: İngilizce → Türkçe
3. Konuşmaya başlayın
4. 3 saniyede bir ses kaydedilip çevrilecek
5. Çevrilen ses otomatik olarak karşı tarafa gönderilip oynatılacak
6. Ekranda çeviri metinleri görünecek

### 7. Kontroller
- **Mikrofon**: Sesi aç/kapat
- **Kamera**: Videoyu aç/kapat
- **Çeviri**: Çeviriyi aktif/pasif yap
- **Kapat**: Çağrıyı sonlandır

## Desteklenen Diller
- Türkçe (tr)
- İngilizce (en)
- İspanyolca (es)
- Fransızca (fr)
- Almanca (de)
- İtalyanca (it)

## Sorun Giderme

### Kamera/Mikrofon Erişimi Reddedildi
1. Tarayıcı adres çubuğundaki kilit ikonuna tıklayın
2. Kamera ve Mikrofon izinlerini "İzin Ver" olarak ayarlayın
3. Sayfayı yenileyin

### Çağrı Bağlanmıyor
1. Her iki tarafın da online olduğundan emin olun
2. Console'da hata mesajlarını kontrol edin (F12)
3. Backend'in çalıştığından emin olun
4. MongoDB'nin çalıştığından emin olun

### Çeviri Çalışmıyor
1. Google Cloud credentials dosyasının doğru yolda olduğundan emin olun
2. Backend console'da hata mesajlarını kontrol edin
3. Mikrofon izinlerinin verildiğinden emin olun
4. En az 1-2 saniye konuşun (çok kısa sesler algılanmayabilir)

### Ses Duyulmuyor
1. Tarayıcı ses ayarlarını kontrol edin
2. Sistem ses seviyesini kontrol edin
3. Karşı tarafın mikrofonunun açık olduğundan emin olun

## Teknik Detaylar

### WebRTC Bağlantısı
- STUN sunucuları: Google STUN servers
- ICE candidate exchange via Socket.IO
- Peer-to-peer video/audio streaming

### Çeviri Pipeline
1. **Speech-to-Text**: Google Cloud Speech API
2. **Translation**: Google Cloud Translation API
3. **Text-to-Speech**: Google Cloud Text-to-Speech API
4. **Delivery**: Socket.IO real-time transmission

### Ses Kayıt Ayarları
- Format: WebM Opus
- Chunk Duration: 3 saniye
- Sample Rate: 48kHz
- Encoding: Opus codec

## Performans İpuçları
- İyi internet bağlantısı kullanın (en az 1 Mbps upload/download)
- Sessiz bir ortamda test edin
- Mikrofonu ağzınıza yakın tutun
- Net ve yavaş konuşun
- Her cümleden sonra kısa bir duraklama yapın

## Güvenlik Notları
- Tüm WebRTC bağlantıları şifrelidir
- Şifreler bcrypt ile hashlenir
- Socket.IO bağlantıları güvenlidir
- Google Cloud API'leri HTTPS üzerinden çalışır
