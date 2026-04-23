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

    df["value"] = df["value"].astype(float) / 1e18

    total_tx = len(df)
    avg_value = df["value"].mean()
    max_value = df["value"].max()

    unique_addresses = df["to"].nunique()

    return {
        "total_tx": total_tx,
        "avg_value": avg_value,
        "max_value": max_value,
        "unique_addresses": unique_addresses
    }


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

def analyze_wallet(address):
    txs = get_transactions(address)
    features = analyze_transactions(txs)
    summary = generate_ai_summary(features)

    print("\n=== WALLET ANALYSIS ===")
    print(summary)


if __name__ == "__main__":
    wallet = input("Enter wallet address: ")
    analyze_wallet(wallet)