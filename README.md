# 🌍 Anlık Çeviri Sistemi (Real-Time Translation Call System)

Gerçek zamanlı video görüşme ve anlık çeviri yapabilen web uygulaması. Google Cloud AI servisleri kullanarak konuşmaları anında farklı dillere çevirir.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![React](https://img.shields.io/badge/react-18.2.0-blue.svg)
![Node](https://img.shields.io/badge/node-16+-green.svg)
![GitHub](https://img.shields.io/badge/github-furkanbaskurthub--lgtm-blue.svg)

## ✨ Özellikler

- 🎥 **WebRTC Video Görüşme**: Peer-to-peer video ve ses iletişimi
- 🗣️ **Gerçek Zamanlı Çeviri**: Konuşmaları anında çevir (3 saniyelik parçalar)
- 🌐 **12 Dil Desteği**: Türkçe, İngilizce, İspanyolca, Fransızca, Almanca, İtalyanca ve daha fazlası
- 👥 **Arkadaş Sistemi**: Arkadaş ekleme, çevrimiçi durum takibi
- 🔐 **Güvenli Kimlik Doğrulama**: Bcrypt ile şifrelenmiş kullanıcı sistemi
- 📱 **Responsive Tasarım**: Mobil ve masaüstü uyumlu
- 🎨 **Modern UI**: Styled-components ile şık arayüz

## 🛠️ Teknolojiler

### Frontend
- React 18 + TypeScript
- Socket.IO Client
- WebRTC API
- Styled Components
- Material-UI Icons

### Backend
- FastAPI (Python)
- Socket.IO Server
- MongoDB (Motor - Async)
- Google Cloud APIs:
  - Speech-to-Text
  - Translation
  - Text-to-Speech

## 📋 Gereksinimler

- Python 3.8+
- Node.js 16+
- MongoDB
- Google Cloud Account (API credentials)

## 🚀 Kurulum

### 1. Repository'yi Klonlayın

\`\`\`bash
git clone https://github.com/furkanbaskurthub-lgtm/Anlik-ceviri-sistemi.git
cd Anlik-ceviri-sistemi
\`\`\`

### 2. Backend Kurulumu

\`\`\`bash
cd backend

# Virtual environment oluştur
python -m venv venv

# Aktif et (Windows)
venv\Scripts\activate

# Aktif et (Mac/Linux)
source venv/bin/activate

# Bağımlılıkları yükle
pip install -r requirements.txt
\`\`\`

### 3. Frontend Kurulumu

\`\`\`bash
cd frontend
npm install
\`\`\`

### 4. MongoDB Kurulumu

MongoDB'yi indirin ve başlatın:
- [MongoDB Community Server](https://www.mongodb.com/try/download/community)

### 5. Google Cloud API Kurulumu

Detaylı kurulum için [GOOGLE_CLOUD_SETUP.md](GOOGLE_CLOUD_SETUP.md) dosyasına bakın.

**Kısa özet:**
1. Google Cloud Console'da yeni proje oluşturun
2. Şu API'leri aktif edin:
   - Cloud Speech-to-Text API
   - Cloud Translation API
   - Cloud Text-to-Speech API
3. Service Account oluşturun ve JSON key indirin
4. JSON dosyasını \`backend/service-account.json\` olarak kaydedin

### 6. Environment Variables

\`backend/.env\` dosyası oluşturun:

\`\`\`env
MONGODB_URL=mongodb://localhost:27017/
DATABASE_NAME=anlikcevirisistemi
COLLECTION_NAME=users
GOOGLE_APPLICATION_CREDENTIALS=./service-account.json
\`\`\`

### 7. API'leri Test Edin

\`\`\`bash
cd backend
python test_google_apis.py
\`\`\`

Tüm testler geçerse hazırsınız! ✅

## 🎮 Kullanım

### Backend'i Başlatın

\`\`\`bash
cd backend
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux
python -m uvicorn app.main:socket_app --host 0.0.0.0 --port 8000 --reload
\`\`\`

### Frontend'i Başlatın

\`\`\`bash
cd frontend
npm start
\`\`\`

Tarayıcınızda \`http://localhost:8081\` adresini açın.

## 📱 Farklı Cihazlardan Test

Aynı WiFi ağındaki farklı cihazlardan test etmek için:

1. Bilgisayarınızın IP adresini öğrenin:
   \`\`\`bash
   ipconfig  # Windows
   ifconfig  # Mac/Linux
   \`\`\`

2. Diğer cihazdan tarayıcıda açın:
   \`\`\`
   http://192.168.1.XXX:8081
   \`\`\`

Detaylı test rehberi için [NETWORK_TEST_GUIDE.md](NETWORK_TEST_GUIDE.md) dosyasına bakın.

## 🎯 Kullanım Senaryosu

1. **Kayıt Ol**: İki farklı kullanıcı hesabı oluşturun
2. **Giriş Yap**: Her iki cihazda da giriş yapın
3. **Arkadaş Ekle**: Birbirini arkadaş olarak ekleyin
4. **Çağrı Başlat**: Bir kullanıcı diğerini arasın
5. **Dil Seç**: Her kullanıcı kendi dilini ve hedef dili seçsin
6. **Konuş**: Konuşmaya başlayın, çeviriler otomatik olacak!

## 📚 Proje Yapısı

\`\`\`
translation-call-system/
├── backend/
│   ├── app/
│   │   ├── database/
│   │   │   └── mongodb.py
│   │   ├── models/
│   │   │   └── user.py
│   │   ├── routes/
│   │   │   └── auth.py
│   │   ├── services/
│   │   │   ├── speech_service.py
│   │   │   ├── translation_service.py
│   │   │   ├── tts_service.py
│   │   │   └── user_service.py
│   │   └── main.py
│   ├── requirements.txt
│   ├── .env (oluşturulacak)
│   └── service-account.json (oluşturulacak)
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── CallInterface.tsx
│   │   │   ├── IncomingCallDialog.tsx
│   │   │   ├── FriendsList.tsx
│   │   │   └── ...
│   │   ├── styles/
│   │   │   └── theme.ts
│   │   └── App.tsx
│   ├── package.json
│   └── webpack.config.js
├── .gitignore
└── README.md
\`\`\`

## 🔒 Güvenlik

- ⚠️ **Asla** \`service-account.json\` dosyasını GitHub'a yüklemeyin
- ⚠️ **Asla** \`.env\` dosyasını paylaşmayın
- 🔐 Şifreler bcrypt ile hashlenir
- 🔐 WebRTC bağlantıları şifrelidir
- 🔐 Socket.IO bağlantıları güvenlidir

## 🐛 Sorun Giderme

### Kamera/Mikrofon Erişimi Reddedildi
- Tarayıcı izinlerini kontrol edin
- HTTPS veya localhost kullanın

### Çağrı Bağlanmıyor
- Her iki kullanıcı da online mi kontrol edin
- Backend ve MongoDB çalışıyor mu kontrol edin
- Console'da hata mesajlarını kontrol edin (F12)

### Çeviri Çalışmıyor
- Google Cloud credentials doğru mu kontrol edin
- API'ler enabled mi kontrol edin
- \`test_google_apis.py\` scriptini çalıştırın

Daha fazla bilgi için [TEST_GUIDE.md](TEST_GUIDE.md) dosyasına bakın.

## 📊 Performans

- **Çeviri Gecikmesi**: ~2-4 saniye
- **Video Kalitesi**: 720p (ayarlanabilir)
- **Ses Kalitesi**: 48kHz Opus codec
- **Eşzamanlı Kullanıcı**: Sınırsız (sunucu kapasitesine bağlı)

## 🌟 Gelecek Özellikler

- [ ] Grup görüşmeleri
- [ ] Ekran paylaşımı
- [ ] Çeviri geçmişi kaydetme
- [ ] Ses efektleri ve filtreler
- [ ] Mobil uygulama (React Native)
- [ ] Daha fazla dil desteği

## 🤝 Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun (\`git checkout -b feature/amazing-feature\`)
3. Commit edin (\`git commit -m 'Add amazing feature'\`)
4. Push edin (\`git push origin feature/amazing-feature\`)
5. Pull Request açın

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## 👨‍💻 Geliştirici

**Furkan Başkurt**
- GitHub: [@furkanbaskurthub-lgtm](https://github.com/furkanbaskurthub-lgtm)

## 🙏 Teşekkürler

- Google Cloud Platform
- FastAPI
- React
- Socket.IO
- WebRTC

## 📞 İletişim

Sorularınız için issue açabilir veya email gönderebilirsiniz.

---

⭐ Bu projeyi beğendiyseniz yıldız vermeyi unutmayın!
