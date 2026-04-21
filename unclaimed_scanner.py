from web3 import Web3
from backend.contracts.predefined_list import PREDEFINED_CONTRACTS

class UnclaimedScanner:
    def __init__(self, network, web3):
        self.network = network
        self.w3 = web3
        self.contracts = PREDEFINED_CONTRACTS.get(network, {})
    
    def check_unclaimed_rewards(self, address):
        unclaimed = []
        
        # Simple ABI for checking rewards
        reward_abi = [
            {'constant':True,'inputs':[{'name':'_owner','type':'address'}],'name':'earned','outputs':[{'name':'','type':'uint256'}],'type':'function'},
            {'constant':True,'inputs':[{'name':'_owner','type':'address'}],'name':'pendingReward','outputs':[{'name':'','type':'uint256'}],'type':'function'},
            {'constant':True,'inputs':[{'name':'_owner','type':'address'}],'name':'claimable','outputs':[{'name':'','type':'uint256'}],'type':'function'}
        ]
        
        for contract_name, contract_addr in self.contracts.items():
            try:
                checksum_addr = Web3.to_checksum_address(contract_addr)
                checksum_wallet = Web3.to_checksum_address(address)
                
                contract = self.w3.eth.contract(address=checksum_addr, abi=reward_abi)
                
                # Try different function names
                for func_name in ['earned', 'pendingReward', 'claimable']:
                    try:
                        reward = contract.functions[func_name](checksum_wallet).call()
                        if reward and reward > 0:
                            unclaimed.append({
                                'contract': contract_name,
                                'amount': float(reward) / 10**18,
                                'function': func_name
                            })
                        break
                    except:
                        continue
            except:
                continue
        
        return unclaimed