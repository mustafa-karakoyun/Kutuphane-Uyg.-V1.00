# -*- coding: utf-8 -*-
"""
Kitap Ekleme/Düzenleme Modülü
"""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import sys
from Kitap_Ekle import Ui_KitapEkleDialog
from database import Database
from styles import MODERN_STYLE


class KitapEkleDialog(QDialog):
    def __init__(self, kitap=None):
        super().__init__()
        self.ui = Ui_KitapEkleDialog()
        self.ui.setupUi(self)
        self.currow = 0
        
        # Modern stil
        self.setStyleSheet(MODERN_STYLE)
        
        # Veritabanı
        self.db = Database()
        
        # Tablo ayarları
        self.ui.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.ui.tableWidget.setAlternatingRowColors(True)
        
        self.kitaplari_listele()
        
        self.kitap = kitap
        # ID değişmemesi için
        self.ui.leid.setReadOnly(True) 
        self.ui.leid.setEnabled(False) 

        if self.kitap:
            self.setWindowTitle("Kitap Düzenle")
            self.ui.leid.setText(kitap[0])
            self.ui.leid.setEnabled(False)       
            self.ui.leKitapAdi.setText(self.kitap[1])
            self.ui.leYazar.setText(self.kitap[2])
            # Tür seçimi
            tur_index = self.ui.comboBox.findText(self.kitap[3])
            if tur_index >= 0:
                self.ui.comboBox.setCurrentIndex(tur_index)
            self.ui.leYazar_2.setText(self.kitap[4])
        else:
            self.setWindowTitle("Yeni Kitap Ekle")
        
        ###BUTON BAGLANTILARI
        self.ui.btnDuzelt.clicked.connect(self.Duzelt)
        self.ui.btnekle.clicked.connect(self.Ekle)
        self.ui.btnSil.clicked.connect(self.Sil)
        self.ui.btnYeni.clicked.connect(self.YENI)
        self.ui.btnCikis.clicked.connect(self.Cikis)
        self.ui.lineEdit.textChanged.connect(self.ARA)
        self.ui.btnAsagi.clicked.connect(self.SONRAKI)
        self.ui.btnYukari.clicked.connect(self.ONCEKI)
        
        self.ui.tableWidget.itemSelectionChanged.connect(self.itemSelectionChanged)
        
        
        
    def kitaplari_listele(self, arama_terimi=""):
        """Kitapları listele"""
        self.ui.tableWidget.setRowCount(0)
        kitaplar = self.db.kitaplari_getir(arama_terimi)
    
        # Her kitap için tabloya satır ekle
        for satir_numarasi, kitap in enumerate(kitaplar):
            self.ui.tableWidget.insertRow(satir_numarasi)
            # İlk 5 sütunu göster
            for sutun_numarasi in range(min(5, len(kitap))):
                veri = kitap[sutun_numarasi]
                item = QTableWidgetItem(str(veri) if veri is not None else "")
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget.setItem(satir_numarasi, sutun_numarasi, item)
                
        if len(kitaplar) > 0:
            self.ui.tableWidget.setCurrentCell(self.currow, 0)

    def itemSelectionChanged(self):
        """Seçili satırın bilgilerini forma aktar"""
        row = self.ui.tableWidget.currentRow()
        if row < 0:
            return

        self.currow = row
        for col, field in enumerate([
            (0, self.ui.leid),
            (1, self.ui.leKitapAdi),
            (2, self.ui.leYazar),
            (3, self.ui.comboBox),
            (4, self.ui.leYazar_2),
        ]):
            item = self.ui.tableWidget.item(row, col)
            if item is None:
                continue
            if field[1] is self.ui.comboBox:
                field[1].setCurrentText(item.text())
            else:
                field[1].setText(item.text())
    
    def Ekle(self):
        """Yeni kitap ekle"""
        ad = self.ui.leKitapAdi.text().strip()
        yazar = self.ui.leYazar.text().strip()
        tur = self.ui.comboBox.currentText()
        yil_text = self.ui.leYazar_2.text().strip()
        
        # Validasyon
        if not ad or not yazar:
            QMessageBox.warning(self, "Uyarı", "Kitap adı ve yazar alanları boş bırakılamaz!")
            return
        
        try:
            yil = int(yil_text) if yil_text else None
        except ValueError:
            QMessageBox.warning(self, "Uyarı", "Basım yılı geçerli bir sayı olmalıdır!")
            return
        
        if self.db.kitap_ekle(ad, yazar, tur, yil):
            QMessageBox.information(self, "Başarılı", "Kitap eklendi!")
            self.currow = self.ui.tableWidget.rowCount()
            self.kitaplari_listele()
            self.YENI()
        else:
            QMessageBox.critical(self, "Hata", "Kitap eklenirken bir hata oluştu!")
    
    def Duzelt(self):
        """Kitap bilgilerini güncelle"""
        if not self.kitap:
            QMessageBox.warning(self, "Uyarı", "Düzenlenecek kitap seçilmedi!")
            return
        
        ad = self.ui.leKitapAdi.text().strip()
        yazar = self.ui.leYazar.text().strip()
        tur = self.ui.comboBox.currentText()
        yil_text = self.ui.leYazar_2.text().strip()
        
        # Validasyon
        if not ad or not yazar:
            QMessageBox.warning(self, "Uyarı", "Kitap adı ve yazar alanları boş bırakılamaz!")
            return
        
        try:
            yil = int(yil_text) if yil_text else None
        except ValueError:
            QMessageBox.warning(self, "Uyarı", "Basım yılı geçerli bir sayı olmalıdır!")
            return
        
        kitap_id = int(self.kitap[0])
        if self.db.kitap_guncelle(kitap_id, ad, yazar, tur, yil):
            QMessageBox.information(self, "Başarılı", "Kitap güncellendi!")
            self.accept()
        else:
            QMessageBox.critical(self, "Hata", "Kitap güncellenirken bir hata oluştu!")
    
    def Sil(self):
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
         
    def YENI(self):
        self.ui.leKitapAdi.setText("")
        self.ui.leYazar.setText("")
        self.ui.leYazar_2.setText("")
        
        self.ui.leKitapAdi.setFocus(True) #True derseniz en başa konumlanır. False en sona
        
    def Cikis(self):
        soru = QMessageBox.question(self, "Çıkış", "Çıkış yapmak istiyor musunuz?", QMessageBox.Yes | QMessageBox.No)
        if soru == QMessageBox.Yes:
            self.close()
            
    def ARA(self):
        arama_terimi = self.ui.lineEdit.text()
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
        
            
    def TabletoForm(self):
            selectedrows = self.ui.tableWidget.selectedItems()
            if selectedrows and len(selectedrows) >= 5:
                self.kitap = [item.text() for item in selectedrows[:5]]
                self.ui.leid.setText(self.kitap[0])
                self.ui.leKitapAdi.setText(self.kitap[1])
                self.ui.leYazar.setText(self.kitap[2])
                self.ui.comboBox.setCurrentText(self.kitap[3])
                self.ui.leYazar_2.setText(self.kitap[4])

            

        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = KitapEkleDialog()
    window.show()
    sys.exit(app.exec_())
