@echo off
chcp 65001 >nul
echo Modern Kutuphane Yonetim Sistemi Baslatiliyor...
echo.
cd /d "%~dp0"
python KutuphaneSayfası.py
pause

