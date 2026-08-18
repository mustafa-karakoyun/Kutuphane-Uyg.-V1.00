# 🚀 Uygulamayı Çalıştırma Talimatları

## 📋 Gereksinimler

- Python 3.7 veya üzeri
- PyQt5 kütüphanesi

## 🔧 Kurulum Adımları

### 1. Python'un Yüklü Olduğunu Kontrol Edin

Terminal/Command Prompt'ta şu komutu çalıştırın:
```bash
python --version
```
veya
```bash
python3 --version
```

Python 3.7 veya üzeri bir sürüm görmelisiniz.

### 2. PyQt5'i Yükleyin

Terminal/Command Prompt'ta şu komutu çalıştırın:

**Windows:**
```bash
pip install PyQt5
```

**Mac/Linux:**
```bash
pip3 install PyQt5
```

veya requirements.txt dosyası ile:
```bash
pip install -r requirements.txt
```

### 3. Uygulamayı Çalıştırın

**ÖNEMLİ:** Uygulamayı çalıştırmadan önce, doğru klasöre gittiğinizden emin olun!

**Windows PowerShell/Command Prompt:**
```bash
cd "C:\Users\karak\Downloads\Kutuphane-Uyg.-V1.00-main\Kutuphane-Uyg.-V1.00-main"
python KutuphaneSayfası.py
```

**Mac/Linux Terminal:**
```bash
cd /path/to/Kutuphane-Uyg.-V1.00-main/Kutuphane-Uyg.-V1.00-main
python3 KutuphaneSayfası.py
```

## ⚠️ Sorun Giderme

### Hata: "ModuleNotFoundError: No module named 'PyQt5'"
**Çözüm:** PyQt5'i yükleyin:
```bash
pip install PyQt5
```

### Hata: "No module named 'database'"
**Çözüm:** `database.py` dosyasının aynı klasörde olduğundan emin olun.

### Hata: "No module named 'styles'"
**Çözüm:** `styles.py` dosyasının aynı klasörde olduğundan emin olun.

### Uygulama açılmıyor
**Çözüm:** 
1. Tüm dosyaların aynı klasörde olduğundan emin olun
2. Python sürümünüzü kontrol edin (3.7+)
3. Terminal'de hata mesajlarını kontrol edin

## 📁 Gerekli Dosyalar

Uygulamanın çalışması için şu dosyaların aynı klasörde olması gerekir:

- ✅ `KutuphaneSayfası.py` (Ana dosya)
- ✅ `database.py`
- ✅ `styles.py`
- ✅ `AnaSayfa.py`
- ✅ `KitapEkleDialog.py`
- ✅ `emanetsayfası.py`
- ✅ `emanetListeSayfasi.py`
- ✅ `uyeYonetimi.py`
- ✅ `Kutuphaneui.py`
- ✅ `ana_sayfa.py`
- ✅ `Kitap_Ekle.py`
- ✅ `emanet.py`
- ✅ `emanetListeui.py`

## 🎯 Hızlı Başlangıç

1. Terminal'i açın
2. Proje klasörüne gidin:
   ```bash
   cd "C:\Users\karak\Downloads\Kutuphane-Uyg.-V1.00-main\Kutuphane-Uyg.-V1.00-main"
   ```
3. Uygulamayı çalıştırın:
   ```bash
   python KutuphaneSayfası.py
   ```

## 💡 İpucu

Eğer sık sık kullanacaksanız, bir kısayol oluşturabilirsiniz:
- Windows: `.bat` dosyası oluşturun
- Mac/Linux: Shell script oluşturun

## 📝 Not

İlk çalıştırmada `kutuphane.db` veritabanı dosyası otomatik olarak oluşturulacaktır.

