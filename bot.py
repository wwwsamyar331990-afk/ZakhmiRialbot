import requests
import time
import telebot

BOT_TOKEN = "7998734835:AAFn_DgaRGbBURcL5SQt3gco5eQ7DuSjwsQ"
OWNER_ID = "1071593338"

bot = telebot.TeleBot(BOT_TOKEN)

def fetch_dexscreener():
    try:
        url = 'https://api.dexscreener.com/latest/dex/pairs/solana'
        res = requests.get(url, timeout=10)
        return res.json().get('pairs', []) if res.status_code == 200 else []
    except: return []

def fetch_pumpfun():
    try:
        url = 'https://pump.fun/api/token/list'
        res = requests.get(url, timeout=10)
        return res.json().get('tokens', []) if res.status_code == 200 else []
    except: return []

def fetch_gmgn_score(address):
    try:
        url = f'https://gmgn.ai/api/rugcheck/{address}'
        res = requests.get(url, timeout=10)
        data = res.json()
        return data.get('score', 0)
    except: return 0

def fetch_jupiter_liquidity(address):
    try:
        url = f'https://quote-api.jup.ag/v6/quote?inputMint={address}&outputMint=So11111111111111111111111111111111111111112&amount=1000000'
        res = requests.get(url, timeout=10)
        data = res.json()
        return data.get('routes', [{}])[0].get('outAmount', 0)
    except: return 0

def filter_token(token):
    try:
        volume = float(token['volume']['h1'])
        liquidity = float(token['liquidity']['usd'])
        tx_count = int(token['txCount']['h1'])
        age_minutes = int(token.get('ageMinutes', 999))
        holders = int(token.get('holders', 0))
        name = token['baseToken']['name'].lower()
        symbol = token['baseToken']['symbol'].lower()
        address = token['pairAddress']

        score = fetch_gmgn_score(address)
        jup_liq = fetch_jupiter_liquidity(address)

        if volume > 10000 and liquidity > 15000 and tx_count > 50 and age_minutes < 60 and holders < 300 and score > 85 and jup_liq > 1000000:
            if any(k in name for k in ['zakhmi','ashk','hope','rial']) or any(k in symbol for k in ['zrb','ashk','hope']):
                return True
    except: return False
    return False

def send_signal(token):
    try:
        name = token['baseToken']['name']
        address = token['pairAddress']
        volume = token['volume']['h1']
        liquidity = token['liquidity']['usd']
        link = f"https://dexscreener.com/solana/{address}"

        message = f"""
🔥 سیگنال پامپ واقعی شناسایی شد!

🪙 نام: {name}
📈 حجم: {volume} دلار
🔒 نقدینگی: {liquidity} دلار
🧠 اعتبار: تأیید شده توسط GMGN و Jupiter

📎 آدرس خرید: {link}

💬 پیام ربات:
"توکن زخمی، ولی امیدوار... مثل دل ما. آماده‌ی پرواز؟ 💔📈"
"""
        bot.send_message(int(OWNER_ID), message)
    except Exception as e:
        print(f"❌ Send error: {e}")

def main():
    sent = set()
    while True:
        tokens = fetch_dexscreener()
        for token in tokens:
            if filter_token(token):
                address = token['pairAddress']
                if address not in sent:
                    send_signal(token)
                    sent.add(address)
        time.sleep(60)

if __name__ == '__main__':
    main()
