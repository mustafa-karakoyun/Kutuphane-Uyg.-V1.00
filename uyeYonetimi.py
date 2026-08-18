# -*- coding: utf-8 -*-
"""
Üye Yönetimi Modülü
"""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import sys
from database import Database
from styles import MODERN_STYLE


class UyeYonetimi(QDialog):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.currow = 0
        
        # Modern stil
        self.setStyleSheet(MODERN_STYLE)
        self.setWindowTitle("Üye Yönetimi")
        self.setMinimumSize(700, 500)
        
        # Veritabanı
        self.db = Database()
        
        # Tablo ayarları
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableWidget.setAlternatingRowColors(True)
        
        # Buton bağlantıları
        self.btnEkle.clicked.connect(self.uye_ekle)
        self.btnDuzenle.clicked.connect(self.uye_duzenle)
        self.btnSil.clicked.connect(self.uye_sil)
        self.btnYeni.clicked.connect(self.form_temizle)
        self.leArama.textChanged.connect(self.arama_yap)
        
        self.uyeleri_listele()
    
    def setup_ui(self):
        """Arayüzü oluştur"""
        layout = QVBoxLayout()
        
        # Form grubu
        form_group = QGroupBox("Üye Bilgileri")
        form_layout = QGridLayout()
        
        # Form alanları
        form_layout.addWidget(QLabel("Ad:"), 0, 0)
        self.leAd = QLineEdit()
        form_layout.addWidget(self.leAd, 0, 1)
        
        form_layout.addWidget(QLabel("Soyad:"), 0, 2)
        self.leSoyad = QLineEdit()
        form_layout.addWidget(self.leSoyad, 0, 3)
        
        form_layout.addWidget(QLabel("Telefon:"), 1, 0)
        self.leTelefon = QLineEdit()
        form_layout.addWidget(self.leTelefon, 1, 1)
        
        form_layout.addWidget(QLabel("E-posta:"), 1, 2)
        self.leEmail = QLineEdit()
        form_layout.addWidget(self.leEmail, 1, 3)
        
        form_group.setLayout(form_layout)
        layout.addWidget(form_group)
        
        # Butonlar
        btn_layout = QHBoxLayout()
        self.btnEkle = QPushButton("EKLE")
        self.btnEkle.setObjectName("btnEkle")
        self.btnDuzenle = QPushButton("DÜZENLE")
        self.btnDuzenle.setObjectName("btnDuzenle")
        self.btnSil = QPushButton("SİL")
        self.btnSil.setObjectName("btnSil")
        self.btnYeni = QPushButton("YENİ")
        
        btn_layout.addWidget(self.btnEkle)
        btn_layout.addWidget(self.btnDuzenle)
        btn_layout.addWidget(self.btnSil)
        btn_layout.addWidget(self.btnYeni)
        btn_layout.addStretch()
        
        layout.addLayout(btn_layout)
        
        # Arama
        arama_layout = QHBoxLayout()
        arama_layout.addWidget(QLabel("Ara:"))
        self.leArama = QLineEdit()
        self.leArama.setPlaceholderText("Ad veya soyad ile ara...")
        arama_layout.addWidget(self.leArama)
        layout.addLayout(arama_layout)
        
        # Tablo
        table_group = QGroupBox("Üyeler")
        table_layout = QVBoxLayout()
        
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(["ID", "Ad", "Soyad", "Telefon", "E-posta"])
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.itemSelectionChanged.connect(self.tablo_secildi)
        
        table_layout.addWidget(self.tableWidget)
        table_group.setLayout(table_layout)
        layout.addWidget(table_group)
        
        self.setLayout(layout)
    
    def uyeleri_listele(self, arama_terimi=""):
        """Üyeleri listele"""
        self.tableWidget.setRowCount(0)
        uyeler = self.db.uyeleri_getir()
        
        # Arama filtresi
        if arama_terimi:
            arama_terimi = arama_terimi.lower()
            uyeler = [u for u in uyeler if 
                     arama_terimi in str(u[1]).lower() or 
                     arama_terimi in str(u[2]).lower()]
        
        for satir_numarasi, uye in enumerate(uyeler):
            self.tableWidget.insertRow(satir_numarasi)
            for sutun_numarasi in range(min(5, len(uye))):
                veri = uye[sutun_numarasi]
                item = QTableWidgetItem(str(veri) if veri is not None else "")
                item.setTextAlignment(Qt.AlignCenter)
                self.tableWidget.setItem(satir_numarasi, sutun_numarasi, item)
    
    def tablo_secildi(self):
        """Tablodan seçilen üyeyi forma yükle"""
        secilen_satir = self.tableWidget.currentRow()
        if secilen_satir >= 0:
            self.currow = secilen_satir
            self.leAd.setText(self.tableWidget.item(secilen_satir, 1).text() if self.tableWidget.item(secilen_satir, 1) else "")
            self.leSoyad.setText(self.tableWidget.item(secilen_satir, 2).text() if self.tableWidget.item(secilen_satir, 2) else "")
            self.leTelefon.setText(self.tableWidget.item(secilen_satir, 3).text() if self.tableWidget.item(secilen_satir, 3) else "")
            self.leEmail.setText(self.tableWidget.item(secilen_satir, 4).text() if self.tableWidget.item(secilen_satir, 4) else "")
    
    def uye_ekle(self):
        """Yeni üye ekle"""
        ad = self.leAd.text().strip()
        soyad = self.leSoyad.text().strip()
        telefon = self.leTelefon.text().strip()
        email = self.leEmail.text().strip()
        
        if not ad or not soyad:
            QMessageBox.warning(self, "Uyarı", "Ad ve soyad alanları boş bırakılamaz!")
            return
        
        if self.db.uye_ekle(ad, soyad, telefon, email):
            QMessageBox.information(self, "Başarılı", "Üye eklendi!")
            self.form_temizle()
            self.uyeleri_listele()
        else:
            QMessageBox.critical(self, "Hata", "Üye eklenirken bir hata oluştu!")
    
    def uye_duzenle(self):
        """Üye bilgilerini güncelle"""
        secilen_satir = self.tableWidget.currentRow()
        if secilen_satir < 0:
            QMessageBox.warning(self, "Uyarı", "Lütfen düzenlemek istediğiniz üyeyi seçin!")
            return
        
        uye_id = int(self.tableWidget.item(secilen_satir, 0).text())
        ad = self.leAd.text().strip()
        soyad = self.leSoyad.text().strip()
        telefon = self.leTelefon.text().strip()
        email = self.leEmail.text().strip()
        
        if not ad or not soyad:
            QMessageBox.warning(self, "Uyarı", "Ad ve soyad alanları boş bırakılamaz!")
            return
        
        # Güncelleme işlemi (database.py'ye eklenebilir)
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE uyeler SET ad=?, soyad=?, telefon=?, email=? WHERE id=?",
                (ad, soyad, telefon, email, uye_id)
            )
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Başarılı", "Üye güncellendi!")
            self.uyeleri_listele()
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Güncelleme sırasında hata: {str(e)}")
    
    def uye_sil(self):
        """Üye sil"""
        secilen_satir = self.tableWidget.currentRow()
        if secilen_satir < 0:
            QMessageBox.warning(self, "Uyarı", "Lütfen silmek istediğiniz üyeyi seçin!")
            return
        
        response = QMessageBox.question(
            self,
            "Silme Onayı",
            "Seçili üyeyi silmek istediğinize emin misiniz?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if response == QMessageBox.Yes:
            uye_id = int(self.tableWidget.item(secilen_satir, 0).text())
            try:
                conn = self.db.get_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM uyeler WHERE id=?", (uye_id,))
                conn.commit()
                conn.close()
                QMessageBox.information(self, "Başarılı", "Üye silindi!")
                self.form_temizle()
                self.uyeleri_listele()
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Silme sırasında hata: {str(e)}")
    
    def form_temizle(self):
        """Formu temizle"""
        self.leAd.setText("")
        self.leSoyad.setText("")
        self.leTelefon.setText("")
        self.leEmail.setText("")
        self.leAd.setFocus()
    
    def arama_yap(self):
        """Arama yap"""
        arama_terimi = self.leArama.text()
        self.uyeleri_listele(arama_terimi)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = UyeYonetimi()
    window.show()
    sys.exit(app.exec_())
