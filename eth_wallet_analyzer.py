import requests
import anthropic
import pandas as pd
from openai import OpenAI
from groq import Groq
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

openrouter_client = OpenAI(
    api_key=ETHERSCAN_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

def get_transactions(address):
    url = "https://api.etherscan.io/v2/api"

    params = {
        "module": "account",
        "action": "txlist",
        "address": address,
        "startblock": 0,
        "endblock": 99999999,
        "sort": "desc",
        "apikey": ETHERSCAN_API_KEY,
        "chainid": 1
    }

    response = requests.get(url, params=params)
    data = response.json()

    # 🔥 Hard validation
    if data.get("status") != "1":
        print("Etherscan error:", data.get("message"), data.get("result"))
        return []

    result = data.get("result")

    # 🔥 This is the key fix
    if not isinstance(result, list):
        print("Result is not a list:", result)
        return []
    
    return result

def analyze_transactions(tx_list):
    if not isinstance(tx_list, list) or len(tx_list) == 0:
        print("No valid transaction data")
        return {}

    df = pd.DataFrame(tx_list)
    
    df["value"] = df["value"].astype(float)
    df["timeStamp"] = df["timeStamp"].astype(int)
    
    total_tx = len(df)
    avg_value = df["value"].mean()

    max_value = df["value"].max()
    unique_addresses = df["to"].nunique()

    # ✅ Compute active_days
    min_ts = df["timeStamp"].min()
    max_ts = df["timeStamp"].max()
    active_days = max(1, (max_ts - min_ts) / 86400)

    # ✅ Compute threshold
    threshold = avg_value * 2

    # ✅ Final features
    features = {
        "total_tx": total_tx,
        "avg_value": avg_value,
        "max_value": max_value,
        "unique_addresses": unique_addresses,
        "tx_frequency": total_tx / active_days,
        "large_tx_ratio": (df["value"] > threshold).mean(),
    }

    return features


def call_your_llm(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "google/gemma-3-4b-it:free",  # your working model
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code != 200:
        return "⚠️ AI explanation unavailable (API error)"

    result = response.json()

    return result["choices"][0]["message"]["content"]

def convert_wei_to_eth(wei_value):
    return wei_value / 1e18  # Convert Wei to ETH

def generate_ai_summary(features, signals_with_severity):
    # Convert the Wei values to ETH
    avg_value_eth = convert_wei_to_eth(features['avg_value'])  # Convert to ETH
    max_value_eth = convert_wei_to_eth(features['max_value'])  # Convert to ETH


    # Round for better readability (optional)
    avg_value_eth = round(avg_value_eth, 5)  # Rounded to 5 decimals
    max_value_eth = round(max_value_eth, 5)  # Rounded to 5 decimals

    prompt = f"""
    Wallet features:
    Total Transactions: {features['total_tx']}
    Average Transaction Value (ETH): {avg_value_eth} ETH
    Maximum Transaction Value (ETH): {max_value_eth} ETH
    Transaction Frequency: {features['tx_frequency']}
    Unique Addresses Interacted With: {features['unique_addresses']}
    Large Transaction Ratio: {features['large_tx_ratio']}

    Detected Signals:
    {signals_with_severity}

    Explain the risk in simple terms, considering the values are in ETH and rounded to 5 decimal places.
    """

    return call_your_llm(prompt)

def compute_risk_score(features):
    score = 0

    if features["avg_value"] > 1:
        score += 0.2
    if features["max_value"] > 10:
        score += 0.2
    if features["tx_frequency"] > 20:
        score += 0.2
    if features["unique_addresses"] > 50:
        score += 0.2
    if features["large_tx_ratio"] > 0.3:
        score += 0.2

    return min(score, 1.0)

def risk_category(score):
    if score < 0.3:
        return "Low Risk"
    elif score < 0.7:
        return "Medium Risk"
    else:
        return "High Risk"
    
def is_valid_address(address):
    return isinstance(address, str) and address.startswith("0x") and len(address) == 42
    
def detect_signals(features):
    signals = []

    # 🧠 High activity
    if features["tx_frequency"] > 20:
        signals.append("High transaction frequency")

    # 💣 Large spikes
    if features["max_value"] > 10:
        signals.append("Large transaction spike detected")

    # 🔁 Many counterparties
    if features["unique_addresses"] > 50:
        signals.append("Interacting with many unique addresses")

    # 📈 Large tx ratio
    if features["large_tx_ratio"] > 0.3:
        signals.append("Frequent large transactions")

    # 🤖 Bot-like behavior
    if features["avg_value"] < 0.01 and features["tx_frequency"] > 30:
        signals.append("Possible bot-like activity (many small frequent txs)")

    # ⚠️ Abnormal burst activity
    if features["tx_frequency"] > 50 and features["avg_value"] > 0.5:
        signals.append("Abnormal burst trading behavior")

    # 🔄 Wash trading suspicion
    if features["unique_addresses"] < 5 and features["tx_frequency"] > 25:
        signals.append("Possible wash trading (low counterparties, high activity)")

    # 💸 Low-value spam pattern
    if features["avg_value"] < 0.001 and features["tx_frequency"] > 40:
        signals.append("Spam transaction pattern detected")

    # 🧍 Dormant then active (basic proxy)
    if features["tx_frequency"] < 1 and features["max_value"] > 20:
        signals.append("Large transaction from low-activity wallet")

    return signals

def detect_signs_with_severity(features):
    signals = []

    if features["tx_frequency"] > 20:
        signals.append(("High transaction frequency", "medium"))

    if features["max_value"] > 10:
        signals.append(("Large transaction spike", "high"))

    if features["unique_addresses"] > 50:
        signals.append(("Many counterparties", "medium"))

    if features["large_tx_ratio"] > 0.3:
        signals.append(("Frequent large transactions", "high"))

    if features["avg_value"] < 0.01 and features["tx_frequency"] > 30:
        signals.append(("Bot-like behavior", "high"))

    return signals

def analyze_wallet(wallet_address):
    try:
        # ✅ Validate address
        if not is_valid_address(wallet_address):
            print("❌ Invalid wallet address format")
            return

        print(f"\nAnalyzing wallet: {wallet_address}")

        # 🔁 Fetch transactions (your existing function)
        txs = get_transactions(wallet_address)

        # ❌ Handle API failure or empty response
        if txs is None:
            print("❌ Failed to fetch transactions (API issue)")
            return

        if len(txs) == 0:
            print("⚠️ Wallet has no transactions")
            return

        # Step 1: Analyze transactions and extract features
        features = analyze_transactions(txs)

        if not features:
            print("❌ Failed to extract features")
            return

        # Step 2: Compute risk score and category
        score = compute_risk_score(features)
        category = risk_category(score)

        # Step 3: Detect signals (with severity)
        signals_with_severity = detect_signs_with_severity(features)

        # Step 4: Sort signals by severity
        severity_order = {"high": 3, "medium": 2, "low": 1}
        signals_with_severity.sort(
            key=lambda x: severity_order.get(x[1], 0),
            reverse=True
        )

        # Step 5: Optional: Detect plain signals (no severity)
        signals = detect_signals(features)

        # Step 6: Generate AI explanation
        explanation = generate_ai_summary(features, signals_with_severity)

        # Step 7: Display results
        print("\n=== WALLET ANALYSIS ===")
        print(f"Risk Score: {score:.2f}")
        print(f"Risk Category: {category}")

        # Display signals with severity
        print("\n--- Signals (with severity) ---")
        if not signals_with_severity:
            print("No suspicious signals detected")
        else:
            for signal, severity in signals_with_severity:
                print(f"- [{severity.upper()}] {signal}")

        # Display key features
        print("\n--- Key Features ---")
        for key, value in features.items():
            print(f"{key}: {value}")

        # Display AI explanation
        print("\n--- AI Explanation ---")
        print(explanation)

    except Exception as e:
        print(f"❌ Unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    wallet = input("Enter wallet address: ")
    analyze_wallet(wallet)