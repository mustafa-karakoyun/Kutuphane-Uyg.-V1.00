# -*- coding: utf-8 -*-
"""
Ödünç Verme Modülü
"""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDate
import sys
from datetime import datetime, timedelta
from emanet import *
from database import Database
from styles import MODERN_STYLE


class Emanet(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Emanet()
        self.ui.setupUi(self)
        
        # Modern stil
        self.setStyleSheet(MODERN_STYLE)
        self.setWindowTitle("Kitap Ödünç Verme")
        
        # Veritabanı
        self.db = Database()
        
        # Tarih ayarları
        bugun = QDate.currentDate()
        self.ui.dateVerilis.setDate(bugun)
        self.ui.dateTeslim.setDate(bugun.addDays(14))  # Varsayılan 14 gün
        
        # Buton bağlantıları
        self.ui.btniptal.clicked.connect(self.iptal)
        self.ui.btnKaydet.clicked.connect(self.kaydet)
        
        # Tamamlayıcı - kitap ismi girildikçe öneriler çıkıyor
        kitap_adlari = self.kitaplari_getir()
        tamamlayici = QCompleter(kitap_adlari)
        tamamlayici.setCaseSensitivity(False)
        self.ui.leSecim.setCompleter(tamamlayici)
        
    def kitaplari_getir(self):
        """Mevcut kitapları getir"""
        kitaplar = self.db.kitaplari_getir()
        return [kitap[1] for kitap in kitaplar if kitap[1]]  # Kitap adları
        
    def kaydet(self):
        """Ödünç verme kaydı oluştur"""
        uye = self.ui.leUyeAd.text().strip()
        kitap_adi = self.ui.leSecim.text().strip()
        verilis = self.ui.dateVerilis.date().toString("dd-MM-yyyy")
        teslim = self.ui.dateTeslim.date().toString("dd-MM-yyyy")
        
        # Validasyon
        if not uye or not kitap_adi:
            QMessageBox.warning(self, "Uyarı", "Üye adı ve kitap adı boş bırakılamaz!")
            return
        
        # Tarih kontrolü
        if self.ui.dateTeslim.date() < self.ui.dateVerilis.date():
            QMessageBox.warning(self, "Uyarı", "Teslim tarihi, veriliş tarihinden önce olamaz!")
            return
        
        # Kitap ID bul
        kitaplar = self.db.kitaplari_getir()
        kitap_id = None
        for kitap in kitaplar:
            if kitap[1] == kitap_adi:
                kitap_id = kitap[0]
                break
        
        if kitap_id is None:
            QMessageBox.warning(self, "Hata", "Girilen kitap bulunamadı!")
            return
        
        # Kitap durumunu kontrol et
        kitaplar_detay = self.db.kitaplari_getir()
        for kitap in kitaplar_detay:
            if kitap[0] == kitap_id:
                if len(kitap) > 6 and kitap[6] == 'Ödünç Verildi':
                    QMessageBox.warning(self, "Uyarı", "Bu kitap zaten ödünç verilmiş!")
                    return
                break
        
        # Emanet kaydı oluştur
        if self.db.emanet_ekle(uye, kitap_id, verilis, teslim):
            QMessageBox.information(self, "Başarılı", "Kitap ödünç verildi!")
            self.YENI()
        else:
            QMessageBox.critical(self, "Hata", "Kayıt oluşturulurken bir hata oluştu!")
        
    def YENI(self):
        """Formu temizle"""
        self.ui.leUyeAd.setText("")
        self.ui.leSecim.setText("")
        bugun = QDate.currentDate()
        self.ui.dateVerilis.setDate(bugun)
        self.ui.dateTeslim.setDate(bugun.addDays(14))
        self.ui.leUyeAd.setFocus()
        
    def iptal(self):
        """İptal et ve kapat"""
        self.close()
        
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = Emanet()
    window.show()
    sys.exit(app.exec_())
