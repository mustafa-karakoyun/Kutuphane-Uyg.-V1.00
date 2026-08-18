# Modern Kütüphane Yönetim Sistemi

Modern, kullanıcı dostu bir kütüphane yönetim uygulaması. PyQt5 ile geliştirilmiş, SQLite veritabanı kullanan masaüstü uygulaması.

## 🚀 Özellikler

### ✨ Modern Arayüz
- Modern ve şık tasarım
- Renkli butonlar ve görsel geri bildirimler
- Kullanıcı dostu arayüz
- Responsive tablo görünümleri

### 📚 Kitap Yönetimi
- Kitap ekleme, düzenleme ve silme
- Gelişmiş arama özelliği (kitap adı ve yazar)
- Kitap türleri: Roman, Tarih, Bilim, Bilim-Kurgu, Şiir, Kurgu Dışı
- Kitap durumu takibi (Mevcut/Ödünç Verildi)

### 👥 Üye Yönetimi
- Üye ekleme, düzenleme ve silme
- Üye bilgileri: Ad, Soyad, Telefon, E-posta
- Üye arama özelliği

### 📖 Ödünç Verme Sistemi
- Kitap ödünç verme işlemleri
- Otomatik kitap adı tamamlama
- Tarih seçici ile veriliş/teslim tarihi belirleme
- Varsayılan 14 günlük ödünç süresi

### 📋 Emanet Takibi
- Tüm ödünç verilen kitapların listesi
- Geç teslim uyarıları (kırmızı renk kodlaması)
- İade işlemi
- Durum takibi (Ödünç Verildi/İade Edildi)

### 🗄️ Veritabanı
- SQLite veritabanı
- Otomatik tablo oluşturma
- Merkezi veritabanı yönetimi
- İlişkisel veri yapısı

## 📦 Kurulum

### Gereksinimler
- Python 3.7 veya üzeri
- PyQt5

### Kurulum Adımları

1. Gerekli paketleri yükleyin:
```bash
pip install PyQt5
```

2. Uygulamayı çalıştırın:
```bash
python KutuphaneSayfası.py
```

## 🎯 Kullanım

### Ana Menü
Uygulama açıldığında ana menüde 5 modül bulunur:
- **KİTAPLAR**: Kitap listesi ve arama
- **İŞLEMLER**: Kitap ekleme/düzenleme
- **ÖDÜNÇ AL**: Kitap ödünç verme
- **EMANETLER**: Ödünç verilen kitapların listesi
- **ÜYE YÖNETİMİ**: Üye ekleme/düzenleme

### Kitap Ekleme
1. **İŞLEMLER** butonuna tıklayın
2. Kitap bilgilerini girin (Ad, Yazar, Tür, Basım Yılı)
3. **EKLE** butonuna tıklayın

### Ödünç Verme
1. **ÖDÜNÇ AL** butonuna tıklayın
2. Üye adını girin
3. Kitap adını yazın (otomatik tamamlama aktif)
4. Veriliş ve teslim tarihlerini seçin
5. **KAYDET** butonuna tıklayın

### İade İşlemi
1. **EMANETLER** butonuna tıklayın
2. İade edilecek kitabı seçin
3. **İADE ET** butonuna tıklayın

## 🎨 Özellikler

### Renk Kodlaması
- **Kırmızı**: Geç teslim edilmesi gereken kitaplar
- **Sarı**: Ödünç verilmiş kitaplar
- **Yeşil**: İade edilmiş kitaplar

### Validasyon
- Boş alan kontrolü
- Tarih kontrolü (teslim tarihi veriliş tarihinden önce olamaz)
- Kitap durumu kontrolü (zaten ödünç verilmiş kitaplar tekrar verilemez)

## 📁 Dosya Yapısı

```
Kutuphane-Uyg.-V1.00-main/
├── KutuphaneSayfası.py      # Ana menü
├── AnaSayfa.py               # Kitap listesi
├── KitapEkleDialog.py        # Kitap ekleme/düzenleme
├── emanetsayfası.py          # Ödünç verme
├── emanetListeSayfasi.py     # Emanet listesi
├── uyeYonetimi.py            # Üye yönetimi
├── database.py               # Veritabanı işlemleri
├── styles.py                 # Modern UI stilleri
├── kutuphane.db              # SQLite veritabanı (otomatik oluşturulur)
└── README.md                  # Bu dosya
```

## 🔧 Teknik Detaylar

### Veritabanı Şeması

**kitaplar tablosu:**
- id (Primary Key)
- ad (Kitap Adı)
- yazar (Yazar)
- tür (Kitap Türü)
- basımyılı (Basım Yılı)
- eklenmetarihi (Eklenme Tarihi)
- durum (Mevcut/Ödünç Verildi)

**uyeler tablosu:**
- id (Primary Key)
- ad (Ad)
- soyad (Soyad)
- telefon (Telefon)
- email (E-posta)
- kayittarihi (Kayıt Tarihi)

**emanet tablosu:**
- id (Primary Key)
- uyeid (Üye ID - Foreign Key)
- uyeadi (Üye Adı)
- kitapid (Kitap ID - Foreign Key)
- kitapadi (Kitap Adı)
- verilmetarihi (Veriliş Tarihi)
- teslimtarihi (Teslim Tarihi)
- iadetarihi (İade Tarihi)
- durum (Ödünç Verildi/İade Edildi)

## 🆕 Yeni Özellikler (v2.0)

- ✅ Modern UI tasarımı
- ✅ Merkezi veritabanı yönetimi
- ✅ Üye yönetimi modülü
- ✅ İade işlemi
- ✅ Geç teslim uyarıları
- ✅ Gelişmiş validasyon
- ✅ Hata yönetimi
- ✅ Renk kodlaması

## 📝 Notlar

- Veritabanı dosyası (`kutuphane.db`) ilk çalıştırmada otomatik oluşturulur
- Tüm tarihler `dd-MM-yyyy` formatında saklanır
- Kitap durumu otomatik güncellenir (ödünç verildiğinde/iadede)

## 👨‍💻 Geliştirici

Modern kütüphane yönetim sistemi - v2.0

## 📄 Lisans

Bu proje eğitim amaçlı geliştirilmiştir.
