@echo off
chcp 65001 >nul
echo ========================================
echo Son Kontrol - GitHub'a Yüklemeden Önce
echo ========================================
echo.

echo Hassas dosyaları kontrol ediyorum...
echo.

if exist "backend\.env" (
    echo ❌ backend\.env BULUNDU - Silinmeli veya .gitignore'da olmalı
) else (
    echo ✅ backend\.env bulunamadı
)

if exist "backend\service-account.json" (
    echo ❌ backend\service-account.json BULUNDU - Silinmeli veya .gitignore'da olmalı
) else (
    echo ✅ backend\service-account.json bulunamadı
)

if exist "venv\" (
    echo ⚠️  venv\ klasörü bulundu - .gitignore'da olmalı
) else (
    echo ✅ venv\ klasörü bulunamadı
)

if exist "frontend\node_modules\" (
    echo ⚠️  frontend\node_modules\ klasörü bulundu - .gitignore'da olmalı
) else (
    echo ✅ frontend\node_modules\ klasörü bulunamadı
)

echo.
echo ========================================
echo Gerekli dosyaları kontrol ediyorum...
echo ========================================
echo.

if exist "README.md" (
    echo ✅ README.md var
) else (
    echo ❌ README.md YOK
)

if exist "LICENSE" (
    echo ✅ LICENSE var
) else (
    echo ❌ LICENSE YOK
)

if exist ".gitignore" (
    echo ✅ .gitignore var
) else (
    echo ❌ .gitignore YOK
)

if exist "backend\.env.example" (
    echo ✅ backend\.env.example var
) else (
    echo ❌ backend\.env.example YOK
)

echo.
echo ========================================
echo Kontrol tamamlandı!
echo ========================================
echo.
echo Eğer tüm kontroller ✅ ise, upload_to_github.bat dosyasını çalıştırabilirsiniz.
echo.
pause
