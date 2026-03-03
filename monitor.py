import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def get_aave_data():
    try:
        url = "https://api.llama.fi/protocol/aave-v3"
        response = requests.get(url, timeout=15)
        return response.json()
    except Exception as e:
        print(f"API error: {e}")
        return None

def format_message(data):
    if not data:
        return "Нет данных от Aave V3"
    
    chain_tvls = data.get("currentChainTvls", {})
    total_tvl = data.get("tvl", 0)
    
    message = "Aave V3 Monitor\n"
    message += "--------------------\n\n"
    if isinstance(total_tvl, list):
        total_tvl = total_tvl[-1].get("totalLiquidityUSD", 0) if total_tvl else 0
    message += f"Total TVL: ${float(total_tvl):,.0f}\n\n"
    
    target_chains = ["Ethereum", "Arbitrum", "Base", "Polygon"]
    for chain in target_chains:
        if chain in chain_tvls:
            tvl = chain_tvls[chain]
            borrowed_key = f"{chain}-borrowed"
            borrowed = chain_tvls.get(borrowed_key, 0)
            utilization = (borrowed / tvl * 100) if tvl > 0 else 0
            alert = "WARNING HIGH" if utilization > 80 else "OK"
            message += f"{alert} {chain}\n"
            message += f"  TVL: ${tvl:,.0f}\n"
            message += f"  Borrowed: ${borrowed:,.0f}\n"
            message += f"  Utilization: {utilization:.1f}%\n\n"
    
    return message

def send_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            print("Sent to Telegram successfully")
        else:
            print(f"Telegram error: {response.text}")
    except Exception as e:
        print(f"Telegram error: {e}")

def run():
    print("Aave V3 Monitor started")
    while True:
        print("Fetching data...")
        data = get_aave_data()
        message = format_message(data)
        send_telegram(message)
        print("Next update in 30 minutes...")
        time.sleep(1800)

if __name__ == "__main__":
    run()