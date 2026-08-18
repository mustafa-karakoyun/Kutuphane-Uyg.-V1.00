# -*- coding: utf-8 -*-
"""
Emanet Listesi Modülü
"""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
import sys
from datetime import datetime
from emanetListeui import *
from database import Database
from styles import MODERN_STYLE


class EmanetList(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_EmanetListe()
        self.ui.setupUi(self)
        self.currow = 0
        
        # Modern stil
        self.setStyleSheet(MODERN_STYLE)
        self.setWindowTitle("Emanet Listesi")
        
        # Veritabanı
        self.db = Database()
        
        # Tablo ayarları
        self.ui.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.ui.tableWidget.setAlternatingRowColors(True)
        
        # İade butonu ekle
        self.btnIade = QPushButton("İADE ET", self.ui.groupBox)
        self.btnIade.setGeometry(640, 210, 80, 30)
        self.btnIade.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 5px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.btnIade.clicked.connect(self.iade_et)
        
        self.ui.tableWidget.itemSelectionChanged.connect(self.itemSelectionChanged)
        self.ui.btnYukari_2.clicked.connect(self.SONRAKI)
        self.ui.btnYukari.clicked.connect(self.ONCEKI)
        
        self.emanetleri_listele()
        
    def itemSelectionChanged(self):
        indeks = self.ui.tableWidget.currentIndex()
        self.currow = indeks.row()
        self.ui.progressBar.setValue(self.currow + 1)
        
    def emanetleri_listele(self):
        """Emanetleri listele ve geç teslim kontrolü yap"""
        self.ui.tableWidget.setRowCount(0)
        emanetler = self.db.emanetleri_getir()
        
        self.ui.progressBar.setMaximum(len(emanetler))
        
        # Sütun başlıklarını ayarla
        headers = ["ID", "Üye Adı", "Kitap Adı", "Veriliş Tarihi", "Teslim Tarihi", "Durum"]
        self.ui.tableWidget.setColumnCount(len(headers))
        for i, header in enumerate(headers):
            self.ui.tableWidget.setHorizontalHeaderItem(i, QTableWidgetItem(header))
    
        for satir_numarasi, emanet in enumerate(emanetler):
            self.ui.tableWidget.insertRow(satir_numarasi)
            
            # Emanet sütunları: id, uyeid, uyeadi, kitapid, kitapadi, verilmetarihi, teslimtarihi, iadetarihi, durum
            # Gösterilecek: id(0), uyeadi(2), kitapadi(4), verilmetarihi(5), teslimtarihi(6), durum(8)
            sutun_indeksleri = [0, 2, 4, 5, 6, 8]
            
            for sutun_numarasi, sutun_idx in enumerate(sutun_indeksleri):
                if sutun_idx < len(emanet):
                    veri = emanet[sutun_idx]
                    item = QTableWidgetItem(str(veri) if veri is not None else "")
                    item.setTextAlignment(Qt.AlignCenter)
                    
                    # Geç teslim kontrolü ve renk kodlama
                    if sutun_idx == 6:  # Teslim tarihi sütunu
                        if veri and len(emanet) > 8 and emanet[8] == 'Ödünç Verildi':
                            if self.db.gec_teslim_kontrol(str(veri)):
                                item.setBackground(QColor(255, 200, 200))  # Kırmızı arka plan
                                item.setForeground(QColor(200, 0, 0))  # Kırmızı yazı
                    
                    # Durum sütunu için renk kodlama
                    if sutun_idx == 8:  # Durum sütunu
                        if str(veri) == 'İade Edildi':
                            item.setBackground(QColor(200, 255, 200))  # Yeşil
                        elif str(veri) == 'Ödünç Verildi':
                            item.setBackground(QColor(255, 255, 200))  # Sarı
                    
                    self.ui.tableWidget.setItem(satir_numarasi, sutun_numarasi, item)
        
        if len(emanetler) > 0:
            if 0 <= self.currow < len(emanetler):
                self.ui.tableWidget.setCurrentCell(self.currow, 0)
            else:
                self.ui.tableWidget.setCurrentCell(0, 0)
    
    def iade_et(self):
        """Seçili emaneti iade et"""
        secilen_satir = self.ui.tableWidget.currentRow()
        if secilen_satir < 0:
            QMessageBox.warning(self, "Uyarı", "Lütfen iade edilecek emaneti seçin!")
            return
        
        emanet_id_item = self.ui.tableWidget.item(secilen_satir, 0)
        if not emanet_id_item:
            QMessageBox.warning(self, "Uyarı", "Emanet ID bulunamadı!")
            return
        
        emanet_id = int(emanet_id_item.text())
        
        # Durum kontrolü
        durum_item = self.ui.tableWidget.item(secilen_satir, 5)
        if durum_item and durum_item.text() == 'İade Edildi':
            QMessageBox.information(self, "Bilgi", "Bu emanet zaten iade edilmiş!")
            return
        
        response = QMessageBox.question(
            self,
            "İade Onayı",
            "Seçili emaneti iade etmek istediğinize emin misiniz?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if response == QMessageBox.Yes:
            if self.db.emanet_iade(emanet_id):
                QMessageBox.information(self, "Başarılı", "Kitap iade edildi!")
                self.emanetleri_listele()
            else:
                QMessageBox.critical(self, "Hata", "İade işlemi sırasında bir hata oluştu!")
            
    
    def SONRAKI(self):
        self.currow+=1
        if (self.currow==self.ui.tableWidget.rowCount()):
            self.currow=0
        self.ui.tableWidget.setCurrentCell(self.currow,0)
    
    def ONCEKI(self):
        self.currow-=1
        if (self.currow<0):
            self.currow=self.ui.tableWidget.rowCount()-1
        self.ui.tableWidget.setCurrentCell(self.currow,0)

        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = EmanetList()
    window.show()
    sys.exit(app.exec_())
