import requests

class HoneypotScanner:
    def __init__(self):
        self.base_url = "https://api.gopluslabs.io/api/v1/token_security"
    
    def check_token(self, chain_id, token_address):
        """
        chain_id: 1 for Ethereum, 56 for BSC
        """
        try:
            url = f"{self.base_url}/{chain_id}?contract_addresses={token_address}"
            response = requests.get(url, timeout=15)
            data = response.json()
            
            if data.get('code') == 1 and data.get('result'):
                result = data['result'].get(token_address.lower(), {})
                
                is_honeypot = False
                warnings = []
                
                # Check honeypot indicators
                if result.get('is_honeypot') == '1':
                    is_honeypot = True
                    warnings.append("Honeypot detected")
                
                if result.get('cannot_buy') == '1':
                    is_honeypot = True
                    warnings.append("Cannot buy")
                
                if result.get('cannot_sell_all') == '1':
                    is_honeypot = True
                    warnings.append("Cannot sell all")
                
                # Check liquidity
                liquidity_locked = result.get('liquidity_lock', {}).get('is_locked') == '1'
                
                # Check ownership
                owner_renounced = result.get('owner_renounced') == '1'
                
                return {
                    'is_honeypot': is_honeypot,
                    'warnings': warnings,
                    'liquidity_locked': liquidity_locked,
                    'owner_renounced': owner_renounced,
                    'buy_tax': float(result.get('buy_tax', '0')),
                    'sell_tax': float(result.get('sell_tax', '0'))
                }
            
            return {'is_honeypot': False, 'warnings': [], 'liquidity_locked': False, 'owner_renounced': False, 'buy_tax': 0, 'sell_tax': 0}
        except Exception as e:
            print(f"Honeypot check error: {e}")
            return {'is_honeypot': False, 'warnings': [], 'liquidity_locked': False, 'owner_renounced': False, 'buy_tax': 0, 'sell_tax': 0}