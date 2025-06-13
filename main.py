import os
import time
from fastapi import FastAPI, Request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from dotenv import load_dotenv

load_dotenv()

SCALEV_EMAIL = os.getenv("SCALEV_EMAIL")
SCALEV_PASSWORD = os.getenv("SCALEV_PASSWORD")

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "Scalev Auto Mark Not Spam is running."}

@app.post("/")
async def receive_webhook(req: Request):
    payload = await req.json()
    secret_slug = payload["data"]["secret_slug"]
    order_url = f"https://app.scalev.id/order/public/{secret_slug}"

    result = run_bot(order_url)
    return {"status": "done", "url": order_url, "success": result}

def run_bot(order_url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    try:
        driver.get("https://app.scalev.id/login")
        time.sleep(2)

        driver.find_element(By.NAME, "email").send_keys(SCALEV_EMAIL)
        driver.find_element(By.NAME, "password").send_keys(SCALEV_PASSWORD)
        driver.find_element(By.TAG_NAME, "form").submit()
        time.sleep(3)

        driver.get(order_url)
        time.sleep(3)

        button = driver.find_element(By.XPATH, "//*[contains(text(), 'Not Spam') or contains(text(), 'Bukan Spam')]")
        button.click()
        time.sleep(2)
        return True
    except Exception as e:
        print("Gagal:", e)
        return False
    finally:
        driver.quit()
