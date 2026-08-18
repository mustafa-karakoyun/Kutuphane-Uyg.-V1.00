# -*- coding: utf-8 -*-
"""
Kitap Listesi ve Yönetim Modülü
"""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import sys
from ana_sayfa import *
from KitapEkleDialog import KitapEkleDialog
from database import Database
from styles import MODERN_STYLE


class AnaSayfa(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Anasayfa()
        self.ui.setupUi(self)
        self.currow = 0
        
        # Modern stil
        self.setStyleSheet(MODERN_STYLE)
        self.setWindowTitle("Kitap Listesi")
        
        # Veritabanı
        self.db = Database()
        
        # Tablo ayarları
        self.ui.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.ui.tableWidget.setAlternatingRowColors(True)
        self.ui.tableWidget.setStyleSheet("""
            QTableWidget {
                gridline-color: #e0e0e0;
            }
            QTableWidget::item {
                padding: 8px;
            }
        """)
        
        # Buton bağlantıları
        self.ui.btnEkle.clicked.connect(self.Ekle_sayfasi)
        self.ui.btnDuzenle.clicked.connect(self.Duzenle_sayfasi)
        self.ui.btnSil.clicked.connect(self.sil_kitap)
        self.ui.leKitapara.textChanged.connect(self.ARA)
        self.ui.btnsonraki.clicked.connect(self.SONRAKI)
        self.ui.btnonceki.clicked.connect(self.ONCEKI)
        
        self.ui.tableWidget.itemSelectionChanged.connect(self.itemSelectionChanged)
        
        # Kitap listesini yükle
        self.kitaplari_listele()
        
        
    def kitaplari_listele(self, arama_terimi=""):
        """Kitapları listele"""
        self.ui.tableWidget.setRowCount(0)
        kitaplar = self.db.kitaplari_getir(arama_terimi)
        
        rowcount = len(kitaplar)
    
        # Her kitap için tabloya satır ekle
        for satir_numarasi, kitap in enumerate(kitaplar):
            self.ui.tableWidget.insertRow(satir_numarasi)
    
            # Sadece ilk 5 sütunu göster (id, ad, yazar, tür, basımyılı)
            for sutun_numarasi in range(min(5, len(kitap))):
                veri = kitap[sutun_numarasi]
                item = QTableWidgetItem(str(veri) if veri is not None else "")
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget.setItem(satir_numarasi, sutun_numarasi, item)
        
        # currow sınır kontrolü
        if rowcount == 0:
            self.currow = 0
        elif self.currow >= rowcount:
            self.currow = rowcount - 1
        elif self.currow < 0:
            self.currow = 0
    
        if rowcount > 0:
            self.ui.tableWidget.setCurrentCell(self.currow, 0)
        self.ui.progressBar.setMaximum(max(rowcount, 1))
        self.ui.progressBar.setValue(self.currow + 1)
    
    
    def itemSelectionChanged(self):
        indeks = self.ui.tableWidget.currentIndex()
        self.currow = indeks.row()
        self.ui.progressBar.setValue(self.currow + 1)
        

    def Ekle_sayfasi(self):
        sayfa = KitapEkleDialog()
        if sayfa.exec_() == QDialog.Accepted:
            self.kitaplari_listele()
        
    def Duzenle_sayfasi(self):
        secilen_satir = self.ui.tableWidget.currentRow()
        if secilen_satir < 0:
            QMessageBox.warning(self, "Uyarı", "Lütfen düzenlemek istediğiniz kitabı seçin!")
            return
    
        kitap = []
        for i in range(5):  # id, ad, yazar, tür, basimyili
            item = self.ui.tableWidget.item(secilen_satir, i)
            kitap.append(item.text() if item else "")
    
        sayfa = KitapEkleDialog(kitap)  
        if sayfa.exec_() == QDialog.Accepted:
            self.kitaplari_listele()

        
    def sil_kitap(self):
        secilen_satir = self.ui.tableWidget.currentRow()
        if secilen_satir < 0:
            QMessageBox.warning(self, "Uyarı", "Lütfen silmek istediğiniz kitabı seçin!")
            return
            
        response = QMessageBox.question(
            self, 
            "Silme Onay", 
            "Seçili kaydı silmek istediğinize emin misiniz?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if response == QMessageBox.Yes:
            kitap_id = int(self.ui.tableWidget.item(secilen_satir, 0).text())
            if self.db.kitap_sil(kitap_id):
                QMessageBox.information(self, "Başarılı", "Kitap silindi!")
                self.kitaplari_listele()
            else:
                QMessageBox.critical(self, "Hata", "Kitap silinirken bir hata oluştu!")
        
    def ARA(self):
        arama_terimi = self.ui.leKitapara.text()
        self.kitaplari_listele(arama_terimi)
        
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
    window = AnaSayfa()
    window.show()
    sys.exit(app.exec_())
