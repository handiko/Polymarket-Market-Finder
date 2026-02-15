import datetime
import requests
import json

def generate_polymarket_url(asset_pair, duration_minutes):
    """Generates the Polymarket URL based on current UTC time."""
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    interval_seconds = duration_minutes * 60
    timestamp = int(now_utc.timestamp())
    rounded_timestamp = (timestamp // interval_seconds) * interval_seconds
    url = f"https://polymarket.com/event/{asset_pair}-updown-{duration_minutes}m-{rounded_timestamp}"
    return url

def get_market_and_token_ids(url):
    """Queries Gamma API to get Market ID and Token IDs (Yes/No)."""
    slug = url.split("/event/")[1]
    api_url = f"https://gamma-api.polymarket.com/events/slug/{slug}"

    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()

        if 'markets' in data and len(data['markets']) > 0:
            market = data['markets'][0]
            market_id = market['id']
            token_ids_raw = market.get('clobTokenIds', '[]')
            try:
                token_ids = json.loads(token_ids_raw)
            except json.JSONDecodeError:
                token_ids = []

            return {
                "market_id": market_id,
                "up_token_id": token_ids[0] if len(token_ids) > 0 else None,
                "down_token_id": token_ids[1] if len(token_ids) > 1 else None
            }
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {slug}: {e}")
        return None

def get_token_price(token_id):
    """Fetches the best Buy and Sell prices for a given token ID."""
    if not token_id:
        return None, None

    price_url = "https://clob.polymarket.com/price"

    # 1. Fetch BEST BUY Price
    buy_price = None
    try:
        response = requests.get(price_url, params={'token_id': token_id, 'side': 'BUY'})
        if response.status_code == 200:
            buy_price = response.json().get('price')
        else:
            print(f"Debug Info BUY: Status={response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching buy price: {e}")

    # 2. Fetch BEST SELL Price
    sell_price = None
    try:
        response = requests.get(price_url, params={'token_id': token_id, 'side': 'SELL'})
        if response.status_code == 200:
            sell_price = response.json().get('price')
        else:
            print(f"Debug Info SELL: Status={response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching sell price: {e}")

    return buy_price, sell_price

assets = [("btc", 5), ("btc", 15), ("eth", 15)]
print(f"--- Fetching Live Prices for Current Interval (UTC: {datetime.datetime.now(datetime.timezone.utc).strftime('%H:%M:%S')}) ---")

for asset, duration in assets:
    # 1. Generate URL
    url = generate_polymarket_url(asset, duration)

    # 2. Get IDs
    ids = get_market_and_token_ids(url)

    print(f"\nAsset: {asset.upper()} {duration}m")
    print(f"URL: {url}")

    if ids:
        print(f"Market ID: {ids['market_id']}")

        # 3. Get Prices for UP (Yes)
        up_buy, up_sell = get_token_price(ids['up_token_id'])
        print(f"UP Token ID: {ids['up_token_id']}")
        print(f"  -> Best Buy: ${up_buy} | Best Sell: ${up_sell}")

        # 4. Get Prices for DOWN (No)
        down_buy, down_sell = get_token_price(ids['down_token_id'])
        print(f"DOWN Token ID: {ids['down_token_id']}")
        print(f"  -> Best Buy: ${down_buy} | Best Sell: ${down_sell}")
    else:
        print("Could not find market data.")