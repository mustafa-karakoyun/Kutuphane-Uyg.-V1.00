# -*- coding: utf-8 -*-
"""
Modern UI Stilleri
"""

MODERN_STYLE = """
QMainWindow {
    background-color: #f5f5f5;
}

QPushButton {
    background-color: #4CAF50;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    font-weight: bold;
    font-size: 12px;
}

QPushButton:hover {
    background-color: #45a049;
}

QPushButton:pressed {
    background-color: #3d8b40;
}

QPushButton#btnEkle {
    background-color: #2196F3;
}

QPushButton#btnEkle:hover {
    background-color: #1976D2;
}

QPushButton#btnDuzenle {
    background-color: #FF9800;
}

QPushButton#btnDuzenle:hover {
    background-color: #F57C00;
}

QPushButton#btnSil {
    background-color: #f44336;
}

QPushButton#btnSil:hover {
    background-color: #d32f2f;
}

QLineEdit {
    border: 1px solid #e0e0e0;
    padding: 5px;
    border-radius: 4px;
    background-color: white;
}

QLineEdit:focus {
    border: 2px solid #2196F3;
}

QTableWidget {
    gridline-color: #e0e0e0;
    background-color: white;
}

QTableWidget::item {
    padding: 5px;
    border: none;
}

QTableWidget::item:selected {
    background-color: #2196F3;
    color: white;
}

QDialog {
    background-color: #f5f5f5;
}

QGroupBox {
    border: 1px solid #e0e0e0;
    border-radius: 5px;
    margin-top: 10px;
    padding-top: 10px;
    font-weight: bold;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    margin-left: 10px;
}

QLabel {
    color: #333333;
}

QComboBox {
    border: 1px solid #e0e0e0;
    padding: 5px;
    border-radius: 4px;
    background-color: white;
}

QComboBox:focus {
    border: 2px solid #2196F3;
}

QDateEdit {
    border: 1px solid #e0e0e0;
    padding: 5px;
    border-radius: 4px;
    background-color: white;
}

QDateEdit:focus {
    border: 2px solid #2196F3;
}
"""
