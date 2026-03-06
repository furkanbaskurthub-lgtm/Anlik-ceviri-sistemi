# 🚀 Hızlı Başlangıç

## GitHub'a Yüklemeden Önce (5 Dakika)

### 1. Güvenlik Kontrolü Çalıştır
\`\`\`bash
python check_before_upload.py
\`\`\`

### 2. README'yi Kişiselleştir
\`README.md\` dosyasında değiştir:
- \`KULLANICI_ADINIZ\` → GitHub kullanıcı adınız
- \`[Adınız]\` → Gerçek adınız
- \`kullanici_adiniz\` → GitHub kullanıcı adınız

### 3. GitHub'da Repository Oluştur
1. https://github.com/new
2. Repository name: \`translation-call-system\`
3. Public veya Private seç
4. "Create repository"

### 4. Git Komutları
\`\`\`bash
# Proje klasörüne git
cd C:\Users\Admin\Desktop\translation

# Git başlat
git init

# Tüm dosyaları ekle
git add .

# İlk commit
git commit -m "Initial commit: Real-time translation call system"

# GitHub'ı bağla (URL'i GitHub'dan kopyala)
git remote add origin https://github.com/KULLANICI_ADINIZ/translation-call-system.git

# Main branch
git branch -M main

# Yükle
git push -u origin main
\`\`\`

## Yerel Kurulum (10 Dakika)

### Backend
\`\`\`bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
\`\`\`

### Frontend
\`\`\`bash
cd frontend
npm install
\`\`\`

### MongoDB
- MongoDB Community Server'ı indir ve başlat

### Google Cloud
1. Console'da proje oluştur
2. 3 API'yi aktif et (Speech, Translation, TTS)
3. Service account oluştur
4. JSON key indir → \`backend/service-account.json\`

### .env Dosyası
\`backend/.env\` oluştur:
\`\`\`
MONGODB_URL=mongodb://localhost:27017/
DATABASE_NAME=anlikcevirisistemi
COLLECTION_NAME=users
GOOGLE_APPLICATION_CREDENTIALS=./service-account.json
\`\`\`

### Test
\`\`\`bash
cd backend
python test_google_apis.py
\`\`\`

## Çalıştır

### Terminal 1 - Backend
\`\`\`bash
cd backend
venv\Scripts\activate
python -m uvicorn app.main:socket_app --host 0.0.0.0 --port 8000 --reload
\`\`\`

### Terminal 2 - Frontend
\`\`\`bash
cd frontend
npm start
\`\`\`

### Tarayıcı
\`http://localhost:8081\`

## Güncelleme

\`\`\`bash
git add .
git commit -m "Update: Your message"
git push origin main
\`\`\`

---

Detaylı bilgi için:
- [README.md](README.md) - Genel bilgi
- [GOOGLE_CLOUD_SETUP.md](GOOGLE_CLOUD_SETUP.md) - Google Cloud kurulumu
- [GITHUB_UPLOAD_GUIDE.md](GITHUB_UPLOAD_GUIDE.md) - GitHub detayları
- [NETWORK_TEST_GUIDE.md](NETWORK_TEST_GUIDE.md) - Farklı cihazlardan test
