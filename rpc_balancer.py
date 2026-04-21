import random
import time
from web3 import Web3
from tenacity import retry, stop_after_attempt, wait_exponential

class RPCBalancer:
    def __init__(self, network, endpoints):
        self.network = network
        self.endpoints = endpoints.copy()
        self.current_index = 0
        self.working_endpoints = endpoints.copy()
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def get_web3(self):
        for endpoint in self.working_endpoints:
            try:
                w3 = Web3(Web3.HTTPProvider(endpoint, request_kwargs={'timeout': 10}))
                if w3.is_connected():
                    return w3
            except:
                continue
        
        # If all fail, reset and try original
        self.working_endpoints = self.endpoints.copy()
        time.sleep(5)
        raise Exception(f"No working RPC for {self.network}")
    
    def report_failure(self, endpoint):
        if endpoint in self.working_endpoints:
            self.working_endpoints.remove(endpoint)