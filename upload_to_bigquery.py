import requests

pair = "ETHUSDT"
url = f"https://api.binance.com/api/v3/klines?symbol={pair}&interval=1m&limit=5"

print(f"Fetching data for {pair} from Binance...")

response = requests.get(url)

if response.status_code == 200:
    print("✅ Response OK")
    data = response.json()

    if data:
        print("Sample:")
        for row in data[:2]:
            print(row)
    else:
        print("⚠️ Binance returned empty data.")
else:
    print("❌ Error fetching data. Status:", response.status_code)
