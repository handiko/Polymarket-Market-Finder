# Polymarket Live Bitcoin (and Ethereum) Market Finder
A Python utility to discover active Polymarket Bitcoin (BTC) 5-minute and 15-minute "Up/Down" prediction markets in real-time. (A demonstration)

## Motivation
Traditional methods of polling the Gamma API to discover new markets often suffer from significant latency between the actual creation of a market on-chain and its indexing by the API.

This script solves this issue by using Unix Timestamps to generate the expected URL of a market based on the current UTC time. By calculating the exact 5 or 15-minute interval, we can query the API for the specific market directly, bypassing the delay in market indexing.

## Features
* **Real-time Detection:** Generates URLs based on the current UTC-time and a specific interval.
* **Asset Support:** Focused on BTC and ETH, with support for 5m and 15m intervals.
* **Price Discovery:** Fetches current BEST BUY and BEST SELL prices directly from the Polymarket CLOB (Central Limit Order Book) API.
* **Market ID Extraction:** Parses raw market data to extract Market IDs and individual Token IDs (Yes/No) needed for trading.

## Prerequisites
* Python 3.7+
* ```request``` library

## Installation
```
git clone https://github.com/handiko/Polymarket-Market-Finder.git
cd Polymarket-Market-Finder
pip install requests
```

## Usage
Run the script directly from your terminal:
```
python PolymarketMarketFinder.py
```

## Example Output
```
--- Fetching Live Prices for Current Interval (UTC: 15:21:57) ---

Asset: BTC 5m
URL: https://polymarket.com/event/btc-updown-5m-1771168800
Market ID: 1377134
UP Token ID: 37821824917908613625836367318395386033792488832282809847663104034253138956671
  -> Best Buy: $0.53 | Best Sell: $0.54
DOWN Token ID: 31506978541488321121449168307313520999908839836227531485069766650000847130568
  -> Best Buy: $0.44 | Best Sell: $0.46

Asset: BTC 15m
URL: https://polymarket.com/event/btc-updown-15m-1771168500
Market ID: 1377128
UP Token ID: 12343373580422814284454092174002344667656980742190953199415190397796829221911
  -> Best Buy: $0.04 | Best Sell: $0.05
DOWN Token ID: 37599731880017853065304291745216765655177051803699962057184013504718539551771
  -> Best Buy: $0.95 | Best Sell: $0.96

Asset: ETH 15m
URL: https://polymarket.com/event/eth-updown-15m-1771168500
Market ID: 1377132
UP Token ID: 111841859373566848185706809524203423163948363506930589904759063387477932628563
  -> Best Buy: $0.13 | Best Sell: $0.14
DOWN Token ID: 59898753075487786912894361042484719997620431583938959946833805171419720746596
  -> Best Buy: $0.86 | Best Sell: $0.87

Process finished with exit code 0
```

## How It Works
1. **URL Generation:** ```generate_polymarket_url(asset_pair, duration_minutes)``` calculates the current time, rounds it down to the nearest 5 or 15-minute interval, and constructs the URL that Polymarket uses for that specific market.
2. **API Query:** ```get_market_and_token_ids(url)``` queries the Gamma API to confirm the market exists and retrieves the ```clobTokenIds``` (the specific IDs for "Yes" and "No" outcomes).
3. **Price Fetching:** ```get_token_price(token_id)``` queries the CLOB API for the best available prices on the order book for that token.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
