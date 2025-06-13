# Scalev Auto Mark Not Spam

Otomatisasi klik tombol "Mark Not Spam" di dashboard Scalev menggunakan Python dan Selenium.  
Dibuat untuk bypass sistem reCAPTCHA v3 yang sering menandai orderan real sebagai spam.

## Cara Kerja
- Menerima webhook dari Scalev saat ada order spam.
- Ekstrak order ID dari webhook.
- Jalankan headless browser (via Selenium) untuk login dan klik tombol "Mark Not Spam".
- Dihosting otomatis di Railway.

## Teknologi
- Python
- Selenium
- Railway

## Status
🚧 Dalam pengembangan
