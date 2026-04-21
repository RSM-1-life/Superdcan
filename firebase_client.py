import json
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime

class FirebaseClient:
    def __init__(self, config_json, service_account_json):
        self.config = json.loads(config_json)
        self.service_account = json.loads(service_account_json)
        
        cred = credentials.Certificate(self.service_account)
        firebase_admin.initialize_app(cred, {
            'databaseURL': self.config.get('databaseURL')
        })
        
        self.ref = db.reference('scanned_wallets')
    
    def save_wallet(self, wallet_data):
        try:
            wallet_ref = self.ref.child(wallet_data['address'])
            wallet_ref.set({
                'address': wallet_data['address'],
                'network': wallet_data['network'],
                'balance_usd': wallet_data.get('balance_usd', 0),
                'tokens': wallet_data.get('tokens', []),
                'last_transaction': wallet_data.get('last_transaction', ''),
                'inactive_days': wallet_data.get('inactive_days', 0),
                'is_honeypot': wallet_data.get('is_honeypot', False),
                'unclaimed_rewards': wallet_data.get('unclaimed_rewards', []),
                'scanned_at': datetime.now().isoformat()
            })
            return True
        except Exception as e:
            print(f"Firebase save error: {e}")
            return False
    
    def get_last_scanned(self):
        try:
            last = self.ref.order_by_child('scanned_at').limit_to_last(1).get()
            return last
        except:
            return None