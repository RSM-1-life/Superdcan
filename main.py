import time
import json
from datetime import datetime
from backend.config import *
from backend.utils.firebase_client import FirebaseClient
from backend.utils.telegram_bot import TelegramBot
from backend.scanners.balance_scanner import BalanceScanner
from backend.scanners.inactivity_scanner import InactivityScanner
from backend.scanners.honeypot_scanner import HoneypotScanner
from backend.scanners.unclaimed_scanner import UnclaimedScanner

class DustScanner:
    def __init__(self):
        self.firebase = FirebaseClient(FIREBASE_CONFIG, FIREBASE_SERVICE_ACCOUNT)
        self.telegram = TelegramBot()
        self.honeypot_scanner = HoneypotScanner()
        
        # Generate some wallet addresses to scan
        self.wallets_to_scan = self.generate_wallet_range()
    
    def generate_wallet_range(self, start=1, count=100):
        """Generate sequential wallet addresses for testing"""
        wallets = []
        for i in range(start, start + count):
            hex_str = hex(i)[2:].zfill(40)
            wallets.append(f"0x{hex_str}")
        return wallets
    
    def scan_wallet(self, network, address):
        print(f"Scanning {address} on {network}...")
        
        # Initialize scanners for this network
        balance_scanner = BalanceScanner(network)
        if not balance_scanner.connect():
            return None
        
        inactivity_scanner = InactivityScanner(network)
        unclaimed_scanner = UnclaimedScanner(network, balance_scanner.w3)
        
        # Get balance
        total_usd, tokens = balance_scanner.get_stable_balance_usd(address)
        
        if total_usd < MIN_BALANCE_USD:
            return None
        
        # Get inactivity
        inactive_days = inactivity_scanner.get_inactive_days(address)
        
        if inactive_days < INACTIVE_DAYS_MIN:
            return None
        
        # Check each token for honeypot
        for token in tokens:
            # Simplified: check token contract (would need token address)
            pass
        
        # Get unclaimed rewards
        unclaimed = unclaimed_scanner.check_unclaimed_rewards(address)
        
        wallet_data = {
            'address': address,
            'network': network,
            'balance_usd': total_usd,
            'tokens': tokens,
            'inactive_days': inactive_days,
            'unclaimed_rewards': unclaimed,
            'is_honeypot': False,
            'last_transaction': f"{inactive_days} days ago"
        }
        
        return wallet_data
    
    def run(self):
        print("=" * 50)
        print("Crypto Dust Scanner Started")
        print(f"Time: {datetime.now()}")
        print(f"Networks: {NETWORKS}")
        print(f"Inactive range: {INACTIVE_DAYS_MIN} - {INACTIVE_DAYS_MAX} days")
        print(f"Min balance: ${MIN_BALANCE_USD}")
        print("=" * 50)
        
        found_wallets = []
        
        for network in NETWORKS:
            print(f"\n🔍 Scanning {network.upper()}...")
            
            for wallet in self.wallets_to_scan[:WALLETS_PER_SCAN]:
                try:
                    result = self.scan_wallet(network, wallet)
                    
                    if result:
                        print(f"✅ FOUND! {wallet} - ${result['balance_usd']:.2f}")
                        self.firebase.save_wallet(result)
                        self.telegram.send_wallet_alert(result)
                        found_wallets.append(result)
                    else:
                        print(f"❌ No dust: {wallet}")
                    
                    time.sleep(0.1)  # Rate limiting
                except Exception as e:
                    print(f"Error scanning {wallet}: {e}")
        
        print("\n" + "=" * 50)
        print(f"Scan Complete! Found {len(found_wallets)} wallets with dust")
        print("=" * 50)
        
        # Send summary to Telegram
        if found_wallets:
            total_value = sum(w['balance_usd'] for w in found_wallets)
            summary = f"""
✅ <b>SCAN COMPLETE</b> ✅

📊 <b>Summary:</b>
• Wallets scanned: {len(self.wallets_to_scan)}
• Dust found: {len(found_wallets)}
• Total value: ${total_value:.2f}

🔗 Check Firebase for details
"""
            self.telegram.send_message(summary)

if __name__ == "__main__":
    scanner = DustScanner()
    scanner.run()