# GitHub'a Yükleme Rehberi

## Ön Hazırlık

### 1. Hassas Dosyaları Kontrol Edin

Aşağıdaki dosyaların .gitignore'da olduğundan emin olun:

✅ `.env` dosyaları
✅ `service-account.json` 
✅ `venv/` klasörü
✅ `node_modules/` klasörü
✅ `__pycache__/` klasörleri

### 2. Hassas Bilgileri Temizleyin

Eğer daha önce commit ettiyseniz:

\`\`\`bash
# Git cache'i temizle
git rm -r --cached .
git add .
git commit -m "Remove sensitive files"
\`\`\`

## GitHub'da Repository Oluşturma

### 1. GitHub'a Giriş Yapın
- https://github.com adresine gidin
- Giriş yapın

### 2. Yeni Repository Oluşturun
1. Sağ üst köşeden "+" > "New repository"
2. Repository bilgilerini doldurun:
   - **Repository name:** `translation-call-system`
   - **Description:** `Real-time video call with instant translation using Google Cloud AI`
   - **Public** veya **Private** seçin
   - ❌ "Initialize with README" seçmeyin (zaten var)
   - ❌ ".gitignore" eklemeyin (zaten var)
   - ✅ "Choose a license" > MIT License seçin (veya LICENSE dosyası zaten var)
3. "Create repository" butonuna tıklayın

## Projeyi GitHub'a Yükleme

### Seçenek 1: Yeni Repository (İlk Kez)

\`\`\`bash
# Proje klasörüne gidin
cd C:\Users\Admin\Desktop\translation

# Git başlat (eğer başlatılmamışsa)
git init

# Tüm dosyaları ekle
git add .

# İlk commit
git commit -m "Initial commit: Real-time translation call system"

# GitHub repository'nizi bağlayın (URL'i GitHub'dan kopyalayın)
git remote add origin https://github.com/KULLANICI_ADINIZ/translation-call-system.git

# Ana branch'i main olarak ayarla
git branch -M main

# GitHub'a yükle
git push -u origin main
\`\`\`

### Seçenek 2: Mevcut Repository'yi Güncelleme

\`\`\`bash
# Değişiklikleri ekle
git add .

# Commit
git commit -m "Update: Add documentation and security improvements"

# Push
git push origin main
\`\`\`

## Güvenlik Kontrolü

Yüklemeden önce şunları kontrol edin:

\`\`\`bash
# .gitignore'un çalıştığını kontrol et
git status

# Şunlar GÖRÜNMEMELI:
# - .env
# - service-account.json
# - venv/
# - node_modules/
# - __pycache__/
\`\`\`

Eğer bu dosyalar görünüyorsa:

\`\`\`bash
# Cache'i temizle
git rm -r --cached .
git add .
git commit -m "Fix: Remove sensitive files from tracking"
\`\`\`

## Hassas Bilgi Sızdıysa Ne Yapmalı?

### 1. Hemen Credentials'ı Değiştirin
- Google Cloud Console'da service account key'i revoke edin
- Yeni key oluşturun
- MongoDB şifresini değiştirin

### 2. Git History'den Silin

\`\`\`bash
# BFG Repo-Cleaner kullanın
# https://rtyley.github.io/bfg-repo-cleaner/

# Veya git filter-branch
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch service-account.json" \
  --prune-empty --tag-name-filter cat -- --all

# Force push
git push origin --force --all
\`\`\`

### 3. GitHub'a Bildirin
- Settings > Security > Report a vulnerability

## Repository Ayarları

### 1. Branch Protection (Önerilen)

GitHub'da:
1. Settings > Branches
2. "Add rule"
3. Branch name pattern: \`main\`
4. Seçenekler:
   - ✅ Require pull request reviews
   - ✅ Require status checks to pass

### 2. Secrets Ekleme (GitHub Actions için)

GitHub'da:
1. Settings > Secrets and variables > Actions
2. "New repository secret"
3. Ekleyin:
   - \`MONGODB_URL\`
   - \`GOOGLE_CREDENTIALS\` (JSON içeriği)

### 3. README Badges Ekleyin

README.md'ye ekleyin:

\`\`\`markdown
![Build Status](https://github.com/KULLANICI_ADINIZ/translation-call-system/workflows/CI/badge.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
\`\`\`

## Güncellemeler İçin

Her değişiklikten sonra:

\`\`\`bash
# Değişiklikleri gör
git status

# Tüm değişiklikleri ekle
git add .

# Veya belirli dosyaları ekle
git add backend/app/main.py
git add frontend/src/App.tsx

# Commit (açıklayıcı mesaj)
git commit -m "feat: Add new translation feature"

# Push
git push origin main
\`\`\`

## Commit Mesaj Formatı (Önerilen)

\`\`\`
feat: Yeni özellik
fix: Bug düzeltme
docs: Dokümantasyon
style: Kod formatı
refactor: Kod iyileştirme
test: Test ekleme
chore: Genel işler
\`\`\`

Örnekler:
\`\`\`bash
git commit -m "feat: Add German language support"
git commit -m "fix: Resolve camera permission issue"
git commit -m "docs: Update installation guide"
\`\`\`

## Faydalı Git Komutları

\`\`\`bash
# Son commit'i geri al (dosyalar kalır)
git reset --soft HEAD~1

# Değişiklikleri geri al
git checkout -- filename

# Branch oluştur
git checkout -b feature/new-feature

# Branch'leri listele
git branch -a

# Remote repository'yi kontrol et
git remote -v

# Son değişiklikleri çek
git pull origin main

# Commit geçmişini gör
git log --oneline

# Belirli bir dosyanın geçmişini gör
git log --follow filename
\`\`\`

## .gitignore Test

Hassas dosyaların ignore edildiğini test edin:

\`\`\`bash
# Test dosyası oluştur
echo "test" > backend/service-account.json
echo "test" > backend/.env

# Git status kontrol et
git status

# Bu dosyalar görünmemeli!
# Eğer görünüyorsa .gitignore'u kontrol edin
\`\`\`

## Collaborator Ekleme

Başkalarının projeye katkı yapması için:

1. GitHub'da Settings > Collaborators
2. "Add people"
3. Kullanıcı adını girin
4. Davet gönderin

## GitHub Pages (Opsiyonel)

Dokümantasyon için GitHub Pages kullanabilirsiniz:

1. Settings > Pages
2. Source: \`main\` branch, \`/docs\` folder
3. Dokümantasyonu \`docs/\` klasörüne koyun

## Kontrol Listesi

Yüklemeden önce:

✅ .gitignore dosyası var ve doğru
✅ README.md güncel
✅ LICENSE dosyası var
✅ .env.example dosyası var (gerçek .env yok!)
✅ service-account.json yok!
✅ Hassas bilgiler temizlendi
✅ Commit mesajları açıklayıcı
✅ Test edildi ve çalışıyor

## Başarılı Yükleme Sonrası

Repository'niz hazır! Şimdi:

1. ⭐ Kendi repository'nize star verin
2. 📝 README'yi kişiselleştirin
3. 🏷️ Release oluşturun (v1.0.0)
4. 📢 Sosyal medyada paylaşın
5. 🤝 Katkıda bulunmak isteyenleri bekleyin

## Sorun Giderme

### "Permission denied" Hatası
\`\`\`bash
# SSH key oluşturun
ssh-keygen -t ed25519 -C "email@example.com"

# Public key'i GitHub'a ekleyin
# Settings > SSH and GPG keys > New SSH key
\`\`\`

### "Remote origin already exists" Hatası
\`\`\`bash
# Mevcut remote'u kaldır
git remote remove origin

# Yeni remote ekle
git remote add origin https://github.com/KULLANICI_ADINIZ/repo.git
\`\`\`

### "Large files" Hatası
\`\`\`bash
# Git LFS kullanın
git lfs install
git lfs track "*.mp4"
git add .gitattributes
\`\`\`

---

🎉 Tebrikler! Projeniz artık GitHub'da!
