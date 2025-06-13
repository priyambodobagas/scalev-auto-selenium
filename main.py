# main.py
import os
import hmac
import base64
import json
from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

app = Flask(__name__)

SCALEV_SECRET = os.getenv("SCALEV_SECRET")
AUTH_TOKEN = os.getenv("SCALEV_AUTH")

@app.route("/", methods=["GET"])
def home():
    return "Scalev Auto Mark Not Spam is running."

@app.route("/webhook", methods=["POST"])
def webhook():
    sig = request.headers.get("X-Scalev-Hmac-Sha256")
    raw_body = request.data

    calculated_hmac = base64.b64encode(
        hmac.new(SCALEV_SECRET.encode(), raw_body, "sha256").digest()
    ).decode()

    if sig != calculated_hmac:
        return "Invalid signature", 403

    data = request.json
    order_url = data["data"]["order_id"]  # ganti jika bukan order_id numeric
    order_id_numeric = extract_numeric_order_id(order_url)
    
    print(f"Marking as not spam: {order_id_numeric}")
    success = mark_not_spam(order_id_numeric)
    return jsonify({"success": success})

def extract_numeric_order_id(order_str):
    # Dummy function for now - you can refine this
    return "2903409"  # Ganti ini nanti dengan parser dinamis

def mark_not_spam(order_id):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    try:
        driver.get(f"https://app.scalev.id/order/{order_id}")
        time.sleep(3)

        # Tambahkan login jika diperlukan
        # driver.find_element(By.ID, "email").send_keys("xxx")
        # driver.find_element(By.ID, "password").send_keys("xxx")

        button = driver.find_element(By.XPATH, "//*[contains(text(), 'Not Spam') or contains(text(), 'Bukan Spam')]")
        button.click()
        time.sleep(2)
        return True
    except Exception as e:
        print("Error:", e)
        return False
    finally:
        driver.quit()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
