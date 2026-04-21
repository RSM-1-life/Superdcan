import requests
from backend.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

class TelegramBot:
    def __init__(self):
        self.token = TELEGRAM_BOT_TOKEN
        self.chat_id = TELEGRAM_CHAT_ID
        self.base_url = f"https://api.telegram.org/bot{self.token}"
    
    def send_message(self, text):
        if not self.token or not self.chat_id:
            return
        try:
            url = f"{self.base_url}/sendMessage"
            payload = {
                'chat_id': self.chat_id,
                'text': text,
                'parse_mode': 'HTML'
            }
            requests.post(url, json=payload, timeout=10)
        except Exception as e:
            print(f"Telegram error: {e}")
    
    def send_wallet_alert(self, wallet_data):
        message = f"""
🔴 <b>NEW DUST WALLET FOUND!</b> 🔴

📍 <b>Address:</b> <code>{wallet_data['address'][:10]}...{wallet_data['address'][-8:]}</code>
🌐 <b>Network:</b> {wallet_data['network'].upper()}
💰 <b>Balance:</b> ${wallet_data.get('balance_usd', 0):.2f}
📅 <b>Inactive:</b> {wallet_data.get('inactive_days', 0)} days
⚠️ <b>Honeypot:</b> {'Yes ❌' if wallet_data.get('is_honeypot') else 'No ✅'}

🎁 <b>Unclaimed Rewards:</b> {len(wallet_data.get('unclaimed_rewards', []))} found

👉 Check Firebase for details
"""
        self.send_message(message)