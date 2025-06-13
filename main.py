import os
from fastapi import FastAPI, Request
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

# MODE TEST DUMMY — tanpa selenium
def run_bot(order_url):
    print(f"[TEST MODE] Pretend to visit: {order_url}")
    return True

# ✅ Ini WAJIB agar Railway bisa run
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
