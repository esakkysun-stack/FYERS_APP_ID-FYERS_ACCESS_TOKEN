# FYERS Live Market Connector

Safe starter connector for FYERS API v3 market-data WebSocket.

## What it does
- Connects to FYERS using environment variables.
- Streams `SymbolUpdate` data for configured symbols.
- Defaults to NIFTY 50 and SENSEX index feeds.
- Writes the latest received ticks to `latest_ticks.json` locally.
- Does **not** place orders.

## Required environment variables

```text
FYERS_APP_ID=your_app_id
FYERS_ACCESS_TOKEN=your_access_token
FYERS_SYMBOLS=NSE:NIFTY50-INDEX,BSE:SENSEX-INDEX
```

Never commit `.env`, access tokens, API secrets, or other credentials to this repository.

## Run

```bash
pip install -r requirements.txt
python fyers_live.py
```

The live feed uses FYERS API v3 Data WebSocket `SymbolUpdate`. Add option symbols to `FYERS_SYMBOLS` after confirming their exact FYERS symbol names.

This connector is market-data only. Order placement should be added separately after API permissions and current FYERS/SEBI retail-algo requirements are verified.
