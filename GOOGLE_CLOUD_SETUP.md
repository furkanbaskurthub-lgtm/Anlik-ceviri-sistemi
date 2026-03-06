# Google Cloud API Kurulum Rehberi

## Gerekli API'ler

Bu proje için 3 Google Cloud API'si gereklidir:

1. **Cloud Speech-to-Text API** - Konuşmayı metne çevirir
2. **Cloud Translation API** - Metni çevirir
3. **Cloud Text-to-Speech API** - Metni sese çevirir

## Adım Adım Kurulum

### 1. Google Cloud Console'a Giriş
- https://console.cloud.google.com/ adresine gidin
- Google hesabınızla giriş yapın

### 2. Yeni Proje Oluşturun
1. Üst menüden proje seçici'ye tıklayın
2. "NEW PROJECT" butonuna tıklayın
3. Proje adı: `translation-call-system`
4. "CREATE" butonuna tıklayın
5. Proje oluşturulmasını bekleyin (30 saniye)

### 3. API'leri Aktif Edin

Her bir API için:

#### a) Cloud Speech-to-Text API
1. Sol menüden "APIs & Services" > "Library"
2. Arama kutusuna "Speech-to-Text" yazın
3. "Cloud Speech-to-Text API" seçin
4. "ENABLE" butonuna tıklayın

#### b) Cloud Translation API
1. "APIs & Services" > "Library"
2. Arama kutusuna "Translation" yazın
3. "Cloud Translation API" seçin
4. "ENABLE" butonuna tıklayın

#### c) Cloud Text-to-Speech API
1. "APIs & Services" > "Library"
2. Arama kutusuna "Text-to-Speech" yazın
3. "Cloud Text-to-Speech API" seçin
4. "ENABLE" butonuna tıklayın

### 4. Service Account Oluşturun

1. Sol menüden "IAM & Admin" > "Service Accounts"
2. "CREATE SERVICE ACCOUNT" butonuna tıklayın
3. Bilgileri doldurun:
   ```
   Service account name: translation-service
   Service account ID: (otomatik oluşur)
   Description: Service account for translation call system
   ```
4. "CREATE AND CONTINUE" butonuna tıklayın

### 5. Roller (Permissions) Ekleyin

Aşağıdaki rolleri ekleyin:

**Seçenek 1: Özel Roller (Önerilen)**
- `Cloud Speech Client`
- `Cloud Translation API User`
- `Cloud Text-to-Speech Client`

**Seçenek 2: Basit (Sadece Test İçin)**
- `Owner` veya `Editor`

"CONTINUE" > "DONE"

### 6. JSON Key Dosyası Oluşturun

1. Service Accounts listesinde oluşturduğunuz account'u bulun
2. Sağ taraftaki 3 nokta menüsüne tıklayın > "Manage keys"
3. "ADD KEY" > "Create new key"
4. **JSON** formatını seçin
5. "CREATE" butonuna tıklayın
6. Dosya otomatik indirilecek (örn: `translation-call-system-abc123.json`)

### 7. JSON Dosyasını Yerleştirin

1. İndirilen JSON dosyasını şu konuma taşıyın:
   ```
   C:\Users\Admin\Desktop\translation\backend\service-account.json
   ```

2. Dosya adını `service-account.json` olarak değiştirin

### 8. .env Dosyasını Kontrol Edin

`backend/.env` dosyasında şu satır olmalı:
```
GOOGLE_APPLICATION_CREDENTIALS=C:/Users/Admin/Desktop/translation/backend/service-account.json
```

**Not:** Windows'ta path'lerde `/` veya `\\` kullanabilirsiniz.

## Test Etme

Backend klasöründe test scriptini çalıştırın:

```cmd
cd backend
venv\Scripts\activate
python test_google_apis.py
```

Tüm testler geçerse şunu göreceksiniz:
```
🎉 All tests passed! Your Google Cloud APIs are ready.
```

## Sorun Giderme

### "API not enabled" Hatası
- Google Cloud Console'da API'lerin enabled olduğunu kontrol edin
- API'leri enable ettikten sonra 2-3 dakika bekleyin

### "Permission denied" Hatası
- Service account'a doğru rollerin eklendiğini kontrol edin
- Rolleri ekledikten sonra 1-2 dakika bekleyin

### "Credentials not found" Hatası
- JSON dosyasının doğru konumda olduğunu kontrol edin
- .env dosyasındaki path'in doğru olduğunu kontrol edin
- Path'te Türkçe karakter varsa sorun olabilir

### "Quota exceeded" Hatası
- Google Cloud'da ücretsiz quota'nız dolmuş olabilir
- Billing account ekleyin (kredi kartı gerekli ama test için ücret alınmaz)

## Ücretsiz Kullanım Limitleri

Google Cloud her ay ücretsiz quota verir:

- **Speech-to-Text:** İlk 60 dakika ücretsiz
- **Translation:** İlk 500,000 karakter ücretsiz
- **Text-to-Speech:** İlk 1 milyon karakter ücretsiz

Normal kullanımda bu limitler yeterlidir.

## Güvenlik Notları

⚠️ **Önemli:**
- JSON key dosyasını asla GitHub'a yüklemeyin
- `.gitignore` dosyasına `service-account.json` ekleyin
- Production'da environment variables kullanın
- Key'i düzenli olarak rotate edin

## Faydalı Linkler

- [Google Cloud Console](https://console.cloud.google.com/)
- [Speech-to-Text Docs](https://cloud.google.com/speech-to-text/docs)
- [Translation Docs](https://cloud.google.com/translate/docs)
- [Text-to-Speech Docs](https://cloud.google.com/text-to-speech/docs)
- [Pricing Calculator](https://cloud.google.com/products/calculator)

## Hızlı Kontrol Listesi

✅ Google Cloud hesabı oluşturuldu
✅ Yeni proje oluşturuldu
✅ 3 API enabled edildi:
   - Cloud Speech-to-Text API
   - Cloud Translation API
   - Cloud Text-to-Speech API
✅ Service account oluşturuldu
✅ Roller eklendi
✅ JSON key indirildi
✅ JSON dosyası backend klasörüne kopyalandı
✅ .env dosyası güncellendi
✅ Test scripti çalıştırıldı ve başarılı oldu

Tüm adımlar tamamlandıysa sisteminiz hazır! 🚀
