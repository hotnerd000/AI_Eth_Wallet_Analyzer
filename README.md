🛠️ Crypto Wallet Risk Analyzer (AI-Powered)

This tool analyzes cryptocurrency wallet transactions to detect suspicious activity and generate a risk score based on transaction behavior. It combines deterministic feature engineering (for trustworthy scoring) with AI-generated explanations (for transparency). Ideal for crypto wallet analysis, fraud detection, and wallet security.

🚀 Features
Transaction Risk Scoring: Calculates a risk score based on wallet transaction behavior.
Suspicious Activity Detection: Identifies high-risk patterns such as bot-like behavior, wash trading, and large transaction spikes.
AI-Generated Explanations: Provides readable, human-understandable explanations for the detected risks.
Fully Automated: Fetches wallet transaction data from Etherscan and analyzes it in real time.

🛠️ Requirements
Python 3.x
Install dependencies:
pip install -r requirements.txt
API Keys:
Etherscan API Key: Create Etherscan API Key
OpenRouter API Key (or any LLM provider API key)

⚡ Setup
1. Clone the repository:
git clone https://github.com/your-username/crypto-wallet-risk-analyzer.git
cd crypto-wallet-risk-analyzer
2. Install dependencies:
pip install -r requirements.txt
3. Create a .env file:
touch .env

Inside the .env file, add your API keys:

ETHERSCAN_API_KEY=your_etherscan_api_key
OPENROUTER_API_KEY=your_openrouter_api_key

🧪 How to Use

1. Run the Analysis:

Run the script with the wallet address you want to analyze:

python analyze_wallet.py --address <wallet_address>

Example:

python analyze_wallet.py --address 0x123abc456def7890

2. Understand the Output:

The output will provide:

Risk Score: A number between 0 and 1 indicating the risk level (higher score = higher risk).
Risk Category: A descriptive category of the risk (e.g., "high risk").
Signals: Any suspicious behaviors detected, such as large transaction spikes, high transaction frequency, etc.
AI Explanation: A natural language explanation from the AI detailing the wallet’s risk behavior.

Example Output:

=== WALLET ANALYSIS ===
Risk Score: 0.82
Risk Category: High Risk

--- Signals (with severity) ---
- [HIGH] Large transaction spike
- [MEDIUM] High transaction frequency
- [LOW] Many counterparties

--- Key Features ---
Total Transactions: 150
Average Transaction Value (ETH): 0.006 ETH
Maximum Transaction Value (ETH): 20 ETH
Transaction Frequency: 25
Unique Addresses Interacted With: 50
Large Transaction Ratio: 0.3

--- AI Explanation ---
This wallet has a moderate risk due to a large transaction spike (20 ETH) and high transaction frequency. The wallet interacts with a moderate number of unique addresses, and the transaction size is generally small (average of 0.006 ETH). The risk is associated with the irregularity of transaction patterns and the potential for bot-like behavior or sudden market activity.

🛠️ Key Functions

1. analyze_transactions(txs):
Processes the list of wallet transactions and calculates key features like transaction frequency, average value, and max value.

2. compute_risk_score(features):
Calculates a numerical risk score based on the wallet’s transaction features.

3. detect_signals(features):
Identifies suspicious activity signals based on wallet transaction patterns.

4. generate_ai_summary(features, signals_with_severity):
Uses a language model (LLM) to generate a human-readable explanation of the wallet’s risk.

💡 Advanced Features (Optional)
Contract-Level Detection: Identify whether transactions are interacting with risky contracts (e.g., DEX, NFTs, bridges).
Time-Window Analysis: Compare wallet activity over the past week vs. all-time.
Custom Alerts: Set thresholds for specific transaction behaviors and get alerted when they are triggered.

📄 License
This project is licensed under the MIT License - see the LICENSE
 file for details.

💬 Contributing
Feel free to fork this repository and submit pull requests with improvements or bug fixes! If you find an issue or have a feature suggestion, please open an issue.

🚀 Next Steps
Test on different wallets: Try analyzing wallets with various transaction patterns to ensure robust functionality.
Deploy it: If you want to build a web app or dashboard with this project, integrate it with Flask or FastAPI to create an interactive UI.

👨‍💻 Author

Hotnerd000
[Your GitHub](https://github.com/hotnerd000)