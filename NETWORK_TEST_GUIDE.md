# Farklı Cihazlardan Test Etme Rehberi

## Adım 1: IP Adresinizi Öğrenin

### Windows:
```cmd
ipconfig
```
"IPv4 Address" satırını bulun, örneğin: `192.168.1.100`

### Mac/Linux:
```bash
ifconfig
```
veya
```bash
ip addr show
```

## Adım 2: Backend'i Başlatın

```cmd
cd backend
venv\Scripts\activate
python -m uvicorn app.main:socket_app --host 0.0.0.0 --port 8000 --reload
```

**Önemli:** `--host 0.0.0.0` parametresi backend'i tüm network interface'lerine açar.

## Adım 3: Frontend'i Başlatın

```cmd
cd frontend
npm start
```

Frontend otomatik olarak `0.0.0.0:8081` adresinde başlayacak.

## Adım 4: Güvenlik Duvarı Ayarları

### Windows Firewall:
1. Windows Güvenlik Duvarı'nı açın
2. "Gelişmiş ayarlar"a tıklayın
3. "Gelen Kurallar" > "Yeni Kural"
4. Port: 8000 ve 8081 için izin verin

### Hızlı Test (Geçici):
```cmd
netsh advfirewall firewall add rule name="Backend" dir=in action=allow protocol=TCP localport=8000
netsh advfirewall firewall add rule name="Frontend" dir=in action=allow protocol=TCP localport=8081
```

## Adım 5: Diğer Cihazdan Bağlanın

### Aynı WiFi Ağında:
Diğer cihazdan (telefon, tablet, başka bilgisayar) tarayıcıda şunu açın:

```
http://192.168.1.100:8081
```

(192.168.1.100 yerine kendi IP adresinizi yazın)

## Adım 6: Test Senaryosu

### Cihaz 1 (Ana Bilgisayar):
1. `http://localhost:8081` veya `http://192.168.1.100:8081` açın
2. Kullanıcı1 ile kayıt olun ve giriş yapın

### Cihaz 2 (Telefon/Tablet/Başka PC):
1. `http://192.168.1.100:8081` açın
2. Kullanıcı2 ile kayıt olun ve giriş yapın

### Arkadaş Ekleme:
1. Cihaz 1'de "Arkadaş Ekle" > Kullanıcı2
2. Cihaz 2'de "İstekler" > Kabul Et

### Çağrı Testi:
1. Cihaz 1'de Kullanıcı2'yi arayın
2. Cihaz 2'de çağrıyı kabul edin
3. Her iki cihazda da kamera/mikrofon izni verin
4. Dil seçimlerini yapın
5. Konuşmaya başlayın!

## Sorun Giderme

### "Bağlantı Kurulamadı" Hatası:
1. Her iki cihaz da aynı WiFi ağında mı?
2. IP adresi doğru mu?
3. Backend çalışıyor mu? (Terminal'de kontrol edin)
4. Güvenlik duvarı portları açık mı?

### IP Adresini Test Etme:
Diğer cihazdan ping atın:
```cmd
ping 192.168.1.100
```

### Backend'e Erişim Testi:
Diğer cihazın tarayıcısında:
```
http://192.168.1.100:8000/health
```

Şunu görmelisiniz: `{"status":"healthy"}`

### Kamera/Mikrofon Çalışmıyor:
- HTTPS gerekli değil (localhost ve local IP'ler için HTTP yeterli)
- Tarayıcı izinlerini kontrol edin
- Cihazın kamera/mikrofonu çalışıyor mu test edin

## Mobil Cihazlarda Test

### Android Chrome:
1. Chrome'da `http://192.168.1.100:8081` açın
2. Kamera/mikrofon izni isteğini kabul edin
3. Normal şekilde kullanın

### iOS Safari:
1. Safari'de `http://192.168.1.100:8081` açın
2. Kamera/mikrofon izni isteğini kabul edin
3. Normal şekilde kullanın

**Not:** iOS Safari bazen WebRTC ile sorun yaşayabilir. Chrome kullanmanız önerilir.

## İnternet Üzerinden Test (Gelişmiş)

Eğer farklı ağlardan test etmek isterseniz:

### Seçenek 1: ngrok (Önerilen)
```cmd
# ngrok'u indirin: https://ngrok.com/download

# Backend için:
ngrok http 8000

# Frontend için (başka terminal):
ngrok http 8081
```

ngrok size public URL verecek, örneğin:
- Backend: `https://abc123.ngrok.io`
- Frontend: `https://xyz789.ngrok.io`

### Seçenek 2: Port Forwarding
Router ayarlarından 8000 ve 8081 portlarını forward edin.

## Güvenlik Notları

⚠️ **Önemli:**
- Bu ayarlar sadece test içindir
- Production'da HTTPS kullanın
- Güvenlik duvarı kurallarını test sonrası kaldırın
- Public IP'nizi paylaşmayın

## Performans İpuçları

- 5GHz WiFi kullanın (2.4GHz yerine)
- Router'a yakın olun
- Diğer ağ trafiğini azaltın
- Kaliteli mikrofon kullanın
- Sessiz ortamda test edin

## Başarılı Test Kontrol Listesi

✅ Her iki cihaz da aynı WiFi'ye bağlı
✅ Backend `0.0.0.0:8000` üzerinde çalışıyor
✅ Frontend `0.0.0.0:8081` üzerinde çalışıyor
✅ Güvenlik duvarı portları açık
✅ IP adresi doğru
✅ Her iki cihazda da kamera/mikrofon izni verildi
✅ MongoDB çalışıyor
✅ Google Cloud credentials ayarlandı
