# AI Wallet Risk Analyzer

An AI-powered cryptocurrency wallet analysis tool that evaluates wallet behavior and assigns a risk score based on transaction patterns.

This project combines **deterministic feature engineering** with **AI-generated explanations** to produce an explainable and practical wallet risk assessment.

---

## 🚀 Features

* 📊 Extracts real transaction-based features
* 🔢 Computes a deterministic risk score (0–1)
* 🧠 Provides AI-generated explanations
* ⚠️ Detects suspicious behavioral signals
* 🛡 Handles invalid inputs and API failures gracefully

---

## 🧠 How It Works

### 1. Data Collection

Fetches transaction data for a given wallet address.

### 2. Feature Engineering

Derives key behavioral metrics:

* Total transactions
* Average transaction value
* Maximum transaction value
* Transaction frequency
* Unique counterparties
* Large transaction ratio

### 3. Risk Scoring

Applies rule-based scoring:

* High transaction frequency
* Large value spikes
* Many unique counterparties
* Abnormal transaction patterns

### 4. Signal Detection

Identifies suspicious behaviors such as:

* Bot-like activity
* High-frequency trading
* Large irregular transfers

### 5. AI Explanation

Generates a natural-language explanation of the wallet's risk profile.

---

## 📦 Installation

```bash
git clone https://github.com/hotnerd000/AI_Eth_Wallet_Analyzer.git
cd wallet-analyzer
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file:

```
OPENROUTER_API_KEY=your_key_here
ETHERSCAN_API_KEY=your_key_here
```

---

## ▶️ Usage

Run the script:

```bash
python main.py
```

Enter a wallet address:

```
Enter wallet address: 0x...
```

---

## 📊 Example Output

```
=== WALLET ANALYSIS ===
Risk Score: 0.78
Risk Category: High Risk

--- Signals ---
- High transaction frequency
- Large transaction spikes
- Many unique counterparties

--- Key Features ---
total_tx: 120
avg_value: 1.5
max_value: 15
tx_frequency: 25
unique_addresses: 65
large_tx_ratio: 0.4

--- AI Explanation ---
This wallet exhibits high-frequency transactions and large value spikes...
```

---

## ⚠️ Error Handling

The system gracefully handles:

* Invalid wallet addresses
* API failures
* Wallets with zero transactions
* Unexpected runtime errors

---

## 🧱 Tech Stack

* Python
* Pandas
* Etherscan API
* Groq / OpenRouter (LLM APIs)
* dotenv for environment management

---

## 🔮 Future Improvements

* Detect DEX interactions (Uniswap, PancakeSwap)
* NFT activity analysis
* Time-window based behavior (recent vs historical)
* Machine learning-based scoring
* Web dashboard UI

---

## 🎯 Use Cases

* Crypto risk analysis
* Fraud detection prototypes
* Gitcoin bounty submissions
* AI + blockchain portfolio projects

---

## 🧠 Key Insight

This project separates:

* **Scoring (deterministic logic)**
* **Explanation (AI layer)**

This makes the system both **trustworthy** and **interpretable**.

---

## 📜 License

MIT License
