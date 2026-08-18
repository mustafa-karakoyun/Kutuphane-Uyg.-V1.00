# -*- coding: utf-8 -*-
"""
Modern Kütüphane Yönetim Sistemi
Ana Menü
"""

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QFont, QIcon
from PyQt5.QtCore import Qt, QSize
import sys
from Kutuphaneui import *
from AnaSayfa import *
from KitapEkleDialog import *
from emanetsayfası import *
from emanetListeSayfasi import *
from uyeYonetimi import *
from styles import MODERN_STYLE
from database import Database


class Kutuphane(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Veritabanı başlat
        self.db = Database()
        
        # Modern stil uygula
        self.setStyleSheet(MODERN_STYLE)
        
        # Pencere ayarları
        self.setWindowTitle("Modern Kütüphane Yönetim Sistemi")
        self.setMinimumSize(800, 600)
        
        # Buton bağlantıları
        self.ui.pushButton.clicked.connect(self.Kitaplar)
        self.ui.pushButton_2.clicked.connect(self.islem)
        self.ui.pushButton_3.clicked.connect(self.Emanet)
        self.ui.pushButton_4.clicked.connect(self.EmanetListesi)
        
        # Yeni üye yönetimi butonu ekle
        self.btnUyeler = QPushButton("ÜYE YÖNETİMİ", self.ui.centralwidget)
        self.btnUyeler.setGeometry(670, 180, 121, 51)
        self.btnUyeler.setObjectName("pushButton_5")
        self.btnUyeler.clicked.connect(self.UyeYonetimi)
        
        # Butonları modernize et
        self.modernize_buttons()
        
        # Arka plan görseli (varsa)
        try:
            self.label = QLabel(self)
            self.label.setPixmap(QPixmap("arka.jpg"))
            self.label.setScaledContents(True)
            self.label.resize(self.size())
            self.label.lower()
        except:
            pass

    def resizeEvent(self, event):
        if hasattr(self, 'label'):
            self.label.resize(self.size())
        return super().resizeEvent(event)
    
    def modernize_buttons(self):
        """Butonları modernize et"""
        buttons = [
            (self.ui.pushButton, "#2196F3", "KİTAPLAR"),
            (self.ui.pushButton_2, "#FF9800", "İŞLEMLER"),
            (self.ui.pushButton_3, "#4CAF50", "ÖDÜNÇ AL"),
            (self.ui.pushButton_4, "#9C27B0", "EMANETLER"),
        ]
        
        for btn, color, text in buttons:
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    border: none;
                    padding: 15px;
                    border-radius: 8px;
                    font-weight: bold;
                    font-size: 14px;
                }}
                QPushButton:hover {{
                    background-color: {self.darken_color(color)};
                }}
                QPushButton:pressed {{
                    background-color: {self.darken_color(color, 0.8)};
                }}
            """)
            btn.setText(text)
        
        # Üye yönetimi butonu stil
        self.btnUyeler.setStyleSheet("""
            QPushButton {
                background-color: #E91E63;
                color: white;
                border: none;
                padding: 15px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #C2185B;
            }
            QPushButton:pressed {
                background-color: #AD1457;
            }
        """)
    
    def darken_color(self, hex_color, factor=0.85):
        """Rengi koyulaştır"""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        rgb = tuple(int(c * factor) for c in rgb)
        return f"rgb({rgb[0]}, {rgb[1]}, {rgb[2]})"
    
    def Kitaplar(self):
        sayfa = AnaSayfa()
        sayfa.exec_()
        
    def islem(self):
        sayfa = KitapEkleDialog()
        sayfa.exec_()

    def Emanet(self):
        sayfa = Emanet()
        sayfa.exec_()    
    
    def EmanetListesi(self):
        sayfa = EmanetList()
        sayfa.exec_()
    
    def UyeYonetimi(self):
        sayfa = UyeYonetimi()
        sayfa.exec_()
    
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Modern görünüm için
    
    window = Kutuphane()
    window.show()
    sys.exit(app.exec_())
