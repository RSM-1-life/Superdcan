# প্রি-ডিফাইন্ড কন্ট্রাক্ট লিস্ট যেখানে আনক্লেইমড রিওয়ার্ড থাকতে পারে

PREDEFINED_CONTRACTS = {
    'ethereum': {
        'uniswap_v2_router': '0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D',
        'uniswap_v3_router': '0xE592427A0AEce92De3Edee1F18E0157C05861564',
        'sushiswap_router': '0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F',
        'aave_lending': '0x7d2768dE32b0b80b7a3454c06BdAc94A69DDc7A9',
        'compound_comptroller': '0x3d9819210A31b4961b30EF54bE2aeD79B9c9Cd3B',
        'curve_finance': '0xE78388b4CE79068e89Bf8aA7f218eF6b9AB0e9d0',
        'oneinch_router': '0x1111111254EEB25477B68fb85Ed929f73A960582',
        'dydx': '0x1E0447b19BB6EcFdAe1e4AE1694b0C3659614e4E',
        'layerzero': '0x72aFcD32DdC1fA09Dd2E6E3D5bA4C8A6E6B9F7D'
    },
    'bsc': {
        'pancakeswap_router': '0x10ED43C718714eb63d5aA57B78B54704E256024E',
        'biswap_router': '0x3a6d8cA21D1CF76F653A67577FA0D27453350d5',
        'apeswap_router': '0xcF0feBd3f17CEf5b47b0cD257aCf6025c5BFf3b7',
        'venus': '0xfD36E2c2a6789Db23113685031d7F16329158384',
        'pancake_v3_router': '0x13f4EA83D0bd40E75C8222255bc855a974568Dd4'
    }
}

# Burn addresses to filter out
BURN_ADDRESSES = [
    '0x0000000000000000000000000000000000000000',
    '0x000000000000000000000000000000000000dead',
    '0x000000000000000000000000000000000000dEaD',
    '0xffffffffffffffffffffffffffffffffffffffff',
    '0x1111111111111111111111111111111111111111'
]

# Token addresses for balance checking (USDT, USDC, BUSD, etc.)
STABLE_COINS = {
    'ethereum': {
        'usdt': '0xdAC17F958D2ee523a2206206994597C13D831ec7',
        'usdc': '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48',
        'dai': '0x6B175474E89094C44Da98b954EedeAC495271d0F'
    },
    'bsc': {
        'usdt': '0x55d398326f99059fF775485246999027B3197955',
        'usdc': '0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d',
        'busd': '0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56'
    }
}