import smtplib
import json
import os
import time
import csv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# E-posta bilgileri
SMTP_SERVER = "smtp.gmail.com"  # Gmail için
SMTP_PORT = 587
EMAIL_SENDER = "seninmailin@gmail.com"  # Gönderen mail adresi
EMAIL_PASSWORD = "uygulama-şifresi"  # Gmail için uygulama şifresi alman gerekebilir
EMAIL_RECEIVER = "bildirimalacakmail@gmail.com"  # Bildirimin gideceği adres

# Tarayıcı ayarları
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Arka planda çalıştır
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# WebDriver başlat
service = Service('chromedriver')  # 'chromedriver' path belirt
driver = webdriver.Chrome(service=service, options=options)

# URL (Gerçek Koton URL'sini eklemelisin)
url = "https://example.com"

# Önceki fiyatları saklayacağımız dosya
PRICE_FILE = "previous_prices.json"

# E-posta gönderme fonksiyonu
def send_email(subject, body):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("📩 E-posta gönderildi!")
    except Exception as e:
        print(f"❌ E-posta gönderilirken hata oluştu: {e}")

# Koton Erkek Bölümünü Tarayan Fonksiyon
def scrape_koton_mens_section():
    try:
        print("Koton erkek kategorisi taranıyor...")
        driver.get(url)
        time.sleep(3)  # Sayfanın tam yüklenmesini bekle

        # Ürünleri bul
        products = driver.find_elements(By.CSS_SELECTOR, ".product-wrapper")  
        results = {}

        for product in products:
            try:
                title = product.find_element(By.CSS_SELECTOR, ".product-title").text
                price = product.find_element(By.CSS_SELECTOR, ".price").text
                
                # İndirim kontrolü
                try:
                    discount_price = product.find_element(By.CSS_SELECTOR, ".discount-price").text
                    price = discount_price
                except:
                    pass  

                results[title] = price

            except Exception as e:
                print(f"Ürün bilgisi alınırken hata oluştu: {e}")

        return results

    except Exception as e:
        print(f"Hata oluştu: {e}")
        return {}
    finally:
        driver.quit()

# Fiyatları kaydetme ve kontrol etme fonksiyonu
def check_price_changes(new_prices):
    if os.path.exists(PRICE_FILE):
        with open(PRICE_FILE, "r", encoding="utf-8") as f:
            old_prices = json.load(f)
    else:
        old_prices = {}

    indirim_olanlar = []

    for title, new_price in new_prices.items():
        old_price = old_prices.get(title, None)

        # Daha önce fiyat varsa ve yeni fiyat daha düşükse indirim var
        if old_price and new_price < old_price:
            indirim_olanlar.append(f"✅ **{title}** ürünü indirime girdi!\n🔻 Eski Fiyat: {old_price}\n🟢 Yeni Fiyat: {new_price}")

    if indirim_olanlar:
        email_body = "\n\n".join(indirim_olanlar)
        send_email("📢 Koton İndirim Bildirimi", email_body)

    # Yeni fiyatları kaydet
    with open(PRICE_FILE, "w", encoding="utf-8") as f:
        json.dump(new_prices, f, ensure_ascii=False, indent=4)

def main():
    new_prices = scrape_koton_mens_section()
    if new_prices:
        check_price_changes(new_prices)
    else:
        print("❌ Ürün bilgisi alınamadı.")

if __name__ == "__main__":
    main()
