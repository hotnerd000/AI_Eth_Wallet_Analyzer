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


openrouter_client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

def generate_ai_summary(features):
    prompt = f"""
    Analyze this Ethereum wallet behavior:

    Total transactions: {features.get('total_tx', 0)}
    Average value: {features.get('avg_value', 0)}
    Max value: {features.get('max_value', 0)}
    Unique addresses: {features.get('unique_addresses', 0)}

    1. Summarize behavior
    2. Assign a risk score (0 to 1)
    3. Explain reasoning briefly
    """

    # 🔁 Fallback to OpenRouter
    try:
        response = openrouter_client.chat.completions.create(
            model="google/gemma-3-4b-it:free",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

    except Exception as e:
        print("OpenRouter failed:", e)

    # 🔥 Final fallback (never crash)
    return "AI analysis unavailable"

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

    if features["tx_frequency"] > 20:
        signals.append("High transaction frequency")

    if features["max_value"] > 10:
        signals.append("Large transaction spike")

    if features["unique_addresses"] > 50:
        signals.append("Many unique counterparties")

    if features["large_tx_ratio"] > 0.3:
        signals.append("Frequent large transactions")

    if features["avg_value"] < 0.01 and features["tx_frequency"] > 30:
        signals.append("Possible bot-like activity")

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

        # 🔧 Feature extraction
        features = analyze_transactions(txs)

        if not features:
            print("❌ Failed to extract features")
            return

        # 📊 Scoring
        score = compute_risk_score(features)
        category = risk_category(score)
        signals = detect_signals(features)

        # 🤖 AI explanation
        explanation = generate_ai_summary(features)

        # 🔥 Final output
        print("\n=== WALLET ANALYSIS ===")
        print(f"Risk Score: {score:.2f}")
        print(f"Risk Category: {category}")

        print("\n--- Signals ---")
        for s in signals:
            print(f"- {s}")

        print("\n--- Key Features ---")
        for key, value in features.items():
            print(f"{key}: {value}")

        print("\n--- AI Explanation ---")
        print(explanation)

    except Exception as e:
        print(f"❌ Unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    wallet = input("Enter wallet address: ")
    analyze_wallet(wallet)