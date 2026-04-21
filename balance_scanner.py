from web3 import Web3
from backend.config import RPC_ENDPOINTS
from backend.utils.rpc_balancer import RPCBalancer
from backend.contracts.predefined_list import STABLE_COINS

class BalanceScanner:
    def __init__(self, network):
        self.network = network
        self.rpc_balancer = RPCBalancer(network, RPC_ENDPOINTS[network])
        self.w3 = None
    
    def connect(self):
        self.w3 = self.rpc_balancer.get_web3()
        return self.w3.is_connected()
    
    def get_native_balance(self, address):
        if not self.w3:
            self.connect()
        try:
            balance_wei = self.w3.eth.get_balance(Web3.to_checksum_address(address))
            balance_eth = Web3.from_wei(balance_wei, 'ether')
            return float(balance_eth)
        except:
            return 0
    
    def get_token_balance(self, address, token_address, decimals=18):
        if not self.w3:
            self.connect()
        try:
            checksum_token = Web3.to_checksum_address(token_address)
            checksum_wallet = Web3.to_checksum_address(address)
            
            # ERC-20 ABI for balanceOf
            contract = self.w3.eth.contract(
                address=checksum_token,
                abi=[{'constant':True,'inputs':[{'name':'_owner','type':'address'}],'name':'balanceOf','outputs':[{'name':'balance','type':'uint256'}],'type':'function'}]
            )
            balance = contract.functions.balanceOf(checksum_wallet).call()
            return balance / 10**decimals
        except:
            return 0
    
    def get_stable_balance_usd(self, address):
        total_usd = 0
        tokens_found = []
        
        # Check native balance (ETH/BNB)
        native_balance = self.get_native_balance(address)
        if native_balance > 0:
            # Approximate price (simplified)
            price = 3000 if self.network == 'ethereum' else 600
            usd_value = native_balance * price
            total_usd += usd_value
            tokens_found.append({
                'symbol': 'ETH' if self.network == 'ethereum' else 'BNB',
                'balance': native_balance,
                'usd_value': usd_value
            })
        
        # Check stable coins
        for symbol, token_addr in STABLE_COINS.get(self.network, {}).items():
            balance = self.get_token_balance(address, token_addr, 18)
            if balance > 0:
                usd_value = balance
                total_usd += usd_value
                tokens_found.append({
                    'symbol': symbol.upper(),
                    'balance': balance,
                    'usd_value': usd_value
                })
        
        return total_usd, tokens_found