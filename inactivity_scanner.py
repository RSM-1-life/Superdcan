import requests
from datetime import datetime, timedelta
from backend.config import ETHERSCAN_API, BSCSCAN_API

class InactivityScanner:
    def __init__(self, network):
        self.network = network
        self.api_key = ETHERSCAN_API if network == 'ethereum' else BSCSCAN_API
        self.base_url = 'https://api.etherscan.io/api' if network == 'ethereum' else 'https://api.bscscan.com/api'
    
    def get_last_transaction(self, address):
        try:
            # Get normal transactions
            url = f"{self.base_url}?module=account&action=txlist&address={address}&sort=desc&apikey={self.api_key}"
            response = requests.get(url, timeout=15)
            data = response.json()
            
            if data.get('status') == '1' and data.get('result'):
                last_tx = data['result'][0]
                timestamp = int(last_tx['timeStamp'])
                return datetime.fromtimestamp(timestamp)
            
            # Check internal transactions if no normal tx
            url = f"{self.base_url}?module=account&action=txlistinternal&address={address}&sort=desc&apikey={self.api_key}"
            response = requests.get(url, timeout=15)
            data = response.json()
            
            if data.get('status') == '1' and data.get('result'):
                last_tx = data['result'][0]
                timestamp = int(last_tx['timeStamp'])
                return datetime.fromtimestamp(timestamp)
            
            return None
        except Exception as e:
            print(f"Error getting last tx for {address}: {e}")
            return None
    
    def get_inactive_days(self, address):
        last_tx = self.get_last_transaction(address)
        if not last_tx:
            # No transactions ever - very old wallet
            return 730  # Max 2 years
        
        days = (datetime.now() - last_tx).days
        return min(days, 730)