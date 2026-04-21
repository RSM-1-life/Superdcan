// Firebase Config (আপনার config দিয়ে replace করবেন)
const firebaseConfig = {
    apiKey: "AIzaSyDUH69P7VHInciflgDRO3fjycGzpjTuncU",
    authDomain: "rsm-scener.firebaseapp.com",
    databaseURL: "https://rsm-scener-default-rtdb.asia-southeast1.firebasedatabase.app",
    projectId: "rsm-scener",
    storageBucket: "rsm-scener.firebasestorage.app",
    messagingSenderId: "985325079341",
    appId: "1:985325079341:web:a38f7aa3bb55726fc961a4",
    measurementId: "G-TL143GZ220"
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);
const database = firebase.database();

let allWallets = [];

// Load wallets from Firebase
function loadWallets() {
    const networkFilter = document.getElementById('networkFilter').value;
    const daysFilter = parseInt(document.getElementById('daysFilter').value);
    const minBalance = parseFloat(document.getElementById('minBalance').value) || 0;
    
    const walletsRef = database.ref('scanned_wallets');
    
    walletsRef.on('value', (snapshot) => {
        const data = snapshot.val();
        if (data) {
            allWallets = Object.values(data);
            filterAndDisplay(networkFilter, daysFilter, minBalance);
            updateStats(allWallets);
        } else {
            document.getElementById('walletsList').innerHTML = '<div class="empty">No wallets found yet. Scanner is running...</div>';
        }
    });
}

function filterAndDisplay(network, days, minBalance) {
    let filtered = allWallets.filter(w => {
        if (network !== 'all' && w.network !== network) return false;
        if (w.inactive_days < days) return false;
        if (w.balance_usd < minBalance) return false;
        return true;
    });
    
    displayWallets(filtered);
}

function displayWallets(wallets) {
    const container = document.getElementById('walletsList');
    
    if (wallets.length === 0) {
        container.innerHTML = '<div class="empty">No wallets match your filters</div>';
        return;
    }
    
    wallets.sort((a, b) => b.balance_usd - a.balance_usd);
    
    container.innerHTML = wallets.map(w => `
        <div class="wallet-card">
            <div class="wallet-header">
                <span class="wallet-address">${w.address.substring(0, 10)}...${w.address.substring(w.address.length - 8)}</span>
                <span class="wallet-balance">$${w.balance_usd.toFixed(2)}</span>
            </div>
            <div class="wallet-details">
                <span>🌐 ${w.network.toUpperCase()}</span>
                <span>📅 Inactive: ${w.inactive_days} days</span>
                <span>💰 ${w.tokens ? w.tokens.length : 0} tokens</span>
                ${w.is_honeypot ? '<span class="badge danger">⚠️ Honeypot</span>' : '<span class="badge success">✅ Safe</span>'}
                ${w.unclaimed_rewards && w.unclaimed_rewards.length > 0 ? `<span class="badge">🎁 ${w.unclaimed_rewards.length} unclaimed</span>` : ''}
            </div>
        </div>
    `).join('');
}

function updateStats(wallets) {
    const totalFound = wallets.length;
    const totalValue = wallets.reduce((sum, w) => sum + w.balance_usd, 0);
    const lastScan = wallets.length > 0 ? new Date(wallets[0].scanned_at).toLocaleString() : '-';
    
    document.getElementById('totalFound').textContent = totalFound;
    document.getElementById('totalValue').textContent = `$${totalValue.toFixed(2)}`;
    document.getElementById('lastScan').textContent = lastScan.substring(0, 16);
}

// Event listeners
document.getElementById('networkFilter').addEventListener('change', () => {
    const network = document.getElementById('networkFilter').value;
    const days = parseInt(document.getElementById('daysFilter').value);
    const minBalance = parseFloat(document.getElementById('minBalance').value);
    filterAndDisplay(network, days, minBalance);
});

document.getElementById('daysFilter').addEventListener('change', () => {
    const network = document.getElementById('networkFilter').value;
    const days = parseInt(document.getElementById('daysFilter').value);
    const minBalance = parseFloat(document.getElementById('minBalance').value);
    filterAndDisplay(network, days, minBalance);
});

document.getElementById('minBalance').addEventListener('input', () => {
    const network = document.getElementById('networkFilter').value;
    const days = parseInt(document.getElementById('daysFilter').value);
    const minBalance = parseFloat(document.getElementById('minBalance').value);
    filterAndDisplay(network, days, minBalance);
});

document.getElementById('refreshBtn').addEventListener('click', () => {
    const network = document.getElementById('networkFilter').value;
    const days = parseInt(document.getElementById('daysFilter').value);
    const minBalance = parseFloat(document.getElementById('minBalance').value);
    filterAndDisplay(network, days, minBalance);
});

// Start loading
loadWallets();