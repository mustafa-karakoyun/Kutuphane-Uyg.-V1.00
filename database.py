# -*- coding: utf-8 -*-
"""
Veritabanı Yönetim Modülü
Modern kütüphane uygulaması için veritabanı işlemleri
"""

import sqlite3
from datetime import datetime, date
from typing import List, Tuple, Optional

class Database:
    """Veritabanı işlemleri için merkezi sınıf"""
    
    def __init__(self, db_name="kutuphane.db"):
        self.db_name = db_name
        self.init_database()
    
    def get_connection(self):
        """Veritabanı bağlantısı oluştur"""
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row  # Sözlük benzeri erişim
        return conn
    
    def init_database(self):
        """Veritabanı tablolarını oluştur ve eski şemaları güncelle"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Kitaplar tablosu
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS kitaplar (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ad TEXT NOT NULL,
                yazar TEXT NOT NULL,
                tür TEXT NOT NULL,
                basımyılı INTEGER,
                eklenmetarihi TEXT DEFAULT CURRENT_TIMESTAMP,
                durum TEXT DEFAULT 'Mevcut'
            )
        """)
        
        # Üyeler tablosu
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS uyeler (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ad TEXT NOT NULL,
                soyad TEXT NOT NULL,
                telefon TEXT,
                email TEXT,
                kayittarihi TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Emanet tablosu (geliştirilmiş)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS emanet (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                uyeid INTEGER,
                uyeadi TEXT NOT NULL,
                kitapid INTEGER NOT NULL,
                kitapadi TEXT,
                verilmetarihi TEXT NOT NULL,
                teslimtarihi TEXT NOT NULL,
                iadetarihi TEXT,
                durum TEXT DEFAULT 'Ödünç Verildi',
                FOREIGN KEY (kitapid) REFERENCES kitaplar(id),
                FOREIGN KEY (uyeid) REFERENCES uyeler(id)
            )
        """)

        # Eski SQLite veritabanı sürümlerinde eksik sütunlar varsa ekle
        # SQLite ALTER TABLE ile CURRENT_TIMESTAMP default'ı eklenemez; sabit default ile ekliyoruz.
        cursor.execute("PRAGMA table_info(kitaplar)")
        kitap_columns = [row[1] for row in cursor.fetchall()]

        for col_name, col_type in [('eklenmetarihi', 'TEXT'), ('durum', "TEXT DEFAULT 'Mevcut'")]:
            if col_name not in kitap_columns:
                if col_name == 'durum':
                    cursor.execute(f"ALTER TABLE kitaplar ADD COLUMN {col_name} {col_type}")
                else:
                    cursor.execute(f"ALTER TABLE kitaplar ADD COLUMN {col_name} {col_type}")

        cursor.execute("PRAGMA table_info(emanet)")
        emanet_columns = [row[1] for row in cursor.fetchall()]

        for col_name, col_type in [
            ('uyeid', 'INTEGER'),
            ('uyeadi', 'TEXT'),
            ('kitapid', 'INTEGER'),
            ('kitapadi', 'TEXT'),
            ('verilmetarihi', 'TEXT'),
            ('teslimtarihi', 'TEXT'),
            ('iadetarihi', 'TEXT'),
            ('durum', "TEXT DEFAULT 'Ödünç Verildi'"),
        ]:
            if col_name not in emanet_columns:
                cursor.execute(f"ALTER TABLE emanet ADD COLUMN {col_name} {col_type}")
        
        conn.commit()
        conn.close()
    
    # Kitap işlemleri
    def kitap_ekle(self, ad: str, yazar: str, tur: str, yil: int) -> bool:
        """Yeni kitap ekle"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO kitaplar (ad, yazar, tür, basımyılı) VALUES (?, ?, ?, ?)",
                (ad, yazar, tur, yil)
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Kitap ekleme hatası: {e}")
            return False
    
    def kitap_guncelle(self, kitap_id: int, ad: str, yazar: str, tur: str, yil: int) -> bool:
        """Kitap bilgilerini güncelle"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE kitaplar SET ad=?, yazar=?, tür=?, basımyılı=? WHERE id=?",
                (ad, yazar, tur, yil, kitap_id)
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Kitap güncelleme hatası: {e}")
            return False
    
    def kitap_sil(self, kitap_id: int) -> bool:
        """Kitap sil"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM kitaplar WHERE id=?", (kitap_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Kitap silme hatası: {e}")
            return False
    
    def kitaplari_getir(self, arama_terimi: str = "") -> List[Tuple]:
        """Kitapları getir (arama ile)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        if arama_terimi:
            cursor.execute(
                "SELECT * FROM kitaplar WHERE ad LIKE ? OR yazar LIKE ?",
                (f"%{arama_terimi}%", f"%{arama_terimi}%")
            )
        else:
            cursor.execute("SELECT * FROM kitaplar ORDER BY ad")
        kitaplar = cursor.fetchall()
        conn.close()
        return [tuple(row) for row in kitaplar]
    
    def kitap_adi_getir(self, kitap_id: int) -> Optional[str]:
        """Kitap adını ID'ye göre getir"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT ad FROM kitaplar WHERE id=?", (kitap_id,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None
    
    # Üye işlemleri
    def uye_ekle(self, ad: str, soyad: str, telefon: str = "", email: str = "") -> bool:
        """Yeni üye ekle"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO uyeler (ad, soyad, telefon, email) VALUES (?, ?, ?, ?)",
                (ad, soyad, telefon, email)
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Üye ekleme hatası: {e}")
            return False
    
    def uyeleri_getir(self) -> List[Tuple]:
        """Tüm üyeleri getir"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM uyeler ORDER BY ad, soyad")
        uyeler = cursor.fetchall()
        conn.close()
        return [tuple(row) for row in uyeler]
    
    def uye_adi_getir(self, uye_id: int) -> Optional[str]:
        """Üye adını ID'ye göre getir"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT ad, soyad FROM uyeler WHERE id=?", (uye_id,))
        result = cursor.fetchone()
        conn.close()
        if result:
            return f"{result[0]} {result[1]}"
        return None
    
    # Emanet işlemleri
    def emanet_ekle(self, uye_adi: str, kitap_id: int, verilis: str, teslim: str, uye_id: int = None) -> bool:
        """Yeni emanet kaydı ekle"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("PRAGMA table_info(emanet)")
            columns = [row[1] for row in cursor.fetchall()]
            kitap_adi = self.kitap_adi_getir(kitap_id)

            fields = ["uyeadi", "kitapid", "kitapadi", "verilmetarihi", "teslimtarihi"]
            values = [uye_adi, kitap_id, kitap_adi, verilis, teslim]

            if 'uyeid' in columns:
                fields.insert(0, 'uyeid')
                values.insert(0, uye_id)
            if 'iadetarihi' in columns:
                fields.append('iadetarihi')
                values.append(None)
            if 'durum' in columns:
                fields.append('durum')
                values.append('Ödünç Verildi')

            placeholders = ', '.join(['?'] * len(values))
            field_list = ', '.join(fields)
            cursor.execute(f"INSERT INTO emanet ({field_list}) VALUES ({placeholders})", tuple(values))

            cursor.execute("UPDATE kitaplar SET durum='Ödünç Verildi' WHERE id=?", (kitap_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Emanet ekleme hatası: {e}")
            return False
    
    def emanet_iade(self, emanet_id: int) -> bool:
        """Emanet iade et"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("PRAGMA table_info(emanet)")
            columns = [row[1] for row in cursor.fetchall()]

            cursor.execute("SELECT kitapid FROM emanet WHERE id=?", (emanet_id,))
            result = cursor.fetchone()
            if result:
                kitap_id = result[0]
                iade_tarihi = datetime.now().strftime("%d-%m-%Y")
                if 'durum' in columns and 'iadetarihi' in columns:
                    cursor.execute(
                        "UPDATE emanet SET iadetarihi=?, durum='İade Edildi' WHERE id=?",
                        (iade_tarihi, emanet_id)
                    )
                elif 'iadetarihi' in columns:
                    cursor.execute(
                        "UPDATE emanet SET iadetarihi=? WHERE id=?",
                        (iade_tarihi, emanet_id)
                    )
                else:
                    cursor.execute(
                        "UPDATE emanet SET iadetarihi=? WHERE id=?",
                        (iade_tarihi, emanet_id)
                    )
                cursor.execute("UPDATE kitaplar SET durum='Mevcut' WHERE id=?", (kitap_id,))
                conn.commit()
                conn.close()
                return True
            conn.close()
            return False
        except Exception as e:
            print(f"Emanet iade hatası: {e}")
            return False
    
    def emanetleri_getir(self, durum: str = None) -> List[Tuple]:
        """Emanetleri getir"""
        conn = self.get_connection()
        cursor = conn.cursor()
        if durum:
            cursor.execute("SELECT * FROM emanet WHERE durum=? ORDER BY verilmetarihi DESC", (durum,))
        else:
            cursor.execute("SELECT * FROM emanet ORDER BY verilmetarihi DESC")
        emanetler = cursor.fetchall()
        conn.close()
        return [tuple(row) for row in emanetler]
    
    def gec_teslim_kontrol(self, teslim_tarihi: str) -> bool:
        """Teslim tarihi geçmiş mi kontrol et"""
        try:
            teslim = datetime.strptime(teslim_tarihi, "%d-%m-%Y").date()
            return teslim < date.today()
        except:
            return False
