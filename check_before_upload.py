"""
GitHub'a Yüklemeden Önce Güvenlik Kontrolü
Bu script hassas dosyaların git'e eklenmediğini kontrol eder.
"""

import os
import sys

def check_file_exists(filepath):
    """Dosyanın var olup olmadığını kontrol et"""
    return os.path.exists(filepath)

def check_gitignore():
    """gitignore dosyasını kontrol et"""
    print("=" * 60)
    print("1. .gitignore Kontrolü")
    print("=" * 60)
    
    if not check_file_exists('.gitignore'):
        print("❌ .gitignore dosyası bulunamadı!")
        return False
    
    with open('.gitignore', 'r', encoding='utf-8') as f:
        content = f.read()
    
    required_patterns = [
        '.env',
        'service-account.json',
        'venv/',
        'node_modules/',
        '__pycache__/'
    ]
    
    all_found = True
    for pattern in required_patterns:
        if pattern in content:
            print(f"✅ '{pattern}' .gitignore'da var")
        else:
            print(f"❌ '{pattern}' .gitignore'da YOK!")
            all_found = False
    
    return all_found

def check_sensitive_files():
    """Hassas dosyaların varlığını kontrol et"""
    print("\n" + "=" * 60)
    print("2. Hassas Dosya Kontrolü")
    print("=" * 60)
    
    sensitive_files = [
        'backend/.env',
        'backend/service-account.json',
        'frontend/.env'
    ]
    
    found_sensitive = []
    for filepath in sensitive_files:
        if check_file_exists(filepath):
            print(f"⚠️  '{filepath}' BULUNDU - Git'e eklenmemeli!")
            found_sensitive.append(filepath)
        else:
            print(f"✅ '{filepath}' bulunamadı (iyi)")
    
    return len(found_sensitive) == 0, found_sensitive

def check_example_files():
    """Example dosyalarının varlığını kontrol et"""
    print("\n" + "=" * 60)
    print("3. Example Dosya Kontrolü")
    print("=" * 60)
    
    example_files = [
        'backend/.env.example',
        'README.md',
        'LICENSE'
    ]
    
    all_exist = True
    for filepath in example_files:
        if check_file_exists(filepath):
            print(f"✅ '{filepath}' var")
        else:
            print(f"❌ '{filepath}' YOK!")
            all_exist = False
    
    return all_exist

def check_large_folders():
    """Büyük klasörlerin varlığını kontrol et"""
    print("\n" + "=" * 60)
    print("4. Büyük Klasör Kontrolü")
    print("=" * 60)
    
    large_folders = [
        'venv',
        'backend/venv',
        'node_modules',
        'frontend/node_modules',
        'backend/__pycache__',
        'frontend/build'
    ]
    
    found_large = []
    for folder in large_folders:
        if os.path.isdir(folder):
            print(f"⚠️  '{folder}' BULUNDU - Git'e eklenmemeli!")
            found_large.append(folder)
        else:
            print(f"✅ '{folder}' bulunamadı (iyi)")
    
    return len(found_large) == 0, found_large

def check_readme_placeholders():
    """README'de placeholder'ları kontrol et"""
    print("\n" + "=" * 60)
    print("5. README Placeholder Kontrolü")
    print("=" * 60)
    
    if not check_file_exists('README.md'):
        print("❌ README.md bulunamadı!")
        return False
    
    with open('README.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    placeholders = [
        'KULLANICI_ADINIZ',
        '[Adınız]',
        'kullanici_adiniz'
    ]
    
    found_placeholders = []
    for placeholder in placeholders:
        if placeholder in content:
            found_placeholders.append(placeholder)
    
    if found_placeholders:
        print("⚠️  README.md'de placeholder'lar bulundu:")
        for p in found_placeholders:
            print(f"   - {p}")
        print("   Bunları kendi bilgilerinizle değiştirin!")
        return False
    else:
        print("✅ README.md'de placeholder yok")
        return True

def main():
    print("\n" + "=" * 60)
    print("GitHub'a Yüklemeden Önce Güvenlik Kontrolü")
    print("=" * 60 + "\n")
    
    results = []
    
    # Kontroller
    results.append(("gitignore", check_gitignore()))
    
    sensitive_ok, sensitive_files = check_sensitive_files()
    results.append(("sensitive_files", sensitive_ok))
    
    results.append(("example_files", check_example_files()))
    
    large_ok, large_folders = check_large_folders()
    results.append(("large_folders", large_ok))
    
    results.append(("readme_placeholders", check_readme_placeholders()))
    
    # Özet
    print("\n" + "=" * 60)
    print("ÖZET")
    print("=" * 60)
    
    all_passed = all(result for _, result in results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{name:20} {status}")
    
    print("\n" + "=" * 60)
    
    if all_passed:
        print("🎉 Tüm kontroller başarılı!")
        print("✅ GitHub'a yüklemeye hazırsınız!")
        print("\nSonraki adımlar:")
        print("1. git add .")
        print("2. git commit -m 'Initial commit'")
        print("3. git remote add origin <URL>")
        print("4. git push -u origin main")
    else:
        print("⚠️  Bazı kontroller başarısız!")
        print("\nYapılması gerekenler:")
        
        if not results[1][1]:  # sensitive_files
            print("\n🔒 Hassas Dosyalar:")
            print("   Bu dosyaları .gitignore'a ekleyin veya silin:")
            for f in sensitive_files:
                print(f"   - {f}")
        
        if not results[3][1]:  # large_folders
            print("\n📦 Büyük Klasörler:")
            print("   Bu klasörlerin .gitignore'da olduğundan emin olun:")
            for f in large_folders:
                print(f"   - {f}")
        
        if not results[4][1]:  # readme_placeholders
            print("\n📝 README Güncellemesi:")
            print("   README.md'deki placeholder'ları değiştirin")
        
        print("\nDüzeltmelerden sonra bu scripti tekrar çalıştırın.")
        sys.exit(1)
    
    print("=" * 60)

if __name__ == "__main__":
    main()
