import os
import json

# API Keys
ETHERSCAN_API = os.environ.get('ETHERSCAN_API', '')
BSCSCAN_API = os.environ.get('BSCSCAN_API', '')

# Telegram
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', '')

# Firebase
FIREBASE_CONFIG = os.environ.get('FIREBASE_CONFIG', '{}')
FIREBASE_SERVICE_ACCOUNT = os.environ.get('FIREBASE_SERVICE_ACCOUNT', '{}')

# Settings
INACTIVE_DAYS_MIN = 30      # 1 মাস
INACTIVE_DAYS_MAX = 730     # 2 বছর
MIN_BALANCE_USD = 1.0

# Networks to scan
NETWORKS = ['ethereum', 'bsc']

# RPC Endpoints
RPC_ENDPOINTS = {
    'ethereum': [
        'https://eth.llamarpc.com',
        'https://rpc.ankr.com/eth',
        'https://ethereum.publicnode.com'
    ],
    'bsc': [
        'https://bsc-dataseed.binance.org',
        'https://rpc.ankr.com/bsc',
        'https://bsc.publicnode.com'
    ]
}

# Scan settings
WALLETS_PER_SCAN = 500
BATCH_SIZE = 50
MAX_RETRIES = 3