import json
import os
import time
from datetime import datetime, timezone

from dotenv import load_dotenv
from fyers_apiv3.FyersWebsocket import data_ws

load_dotenv()

APP_ID = os.getenv("FYERS_APP_ID")
ACCESS_TOKEN = os.getenv("FYERS_ACCESS_TOKEN")
SYMBOLS = [s.strip() for s in os.getenv(
    "FYERS_SYMBOLS", "NSE:NIFTY50-INDEX,BSE:SENSEX-INDEX"
).split(",") if s.strip()]

if not APP_ID or not ACCESS_TOKEN:
    raise RuntimeError("Set FYERS_APP_ID and FYERS_ACCESS_TOKEN as environment variables; never commit them to GitHub.")

latest = {}


def on_message(message):
    if not isinstance(message, dict):
        return
    symbol = message.get("symbol")
    if not symbol:
        return
    latest[symbol] = message
    payload = {
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "symbols": latest,
    }
    with open("latest_ticks.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, default=str)
    print(message, flush=True)


def on_error(message):
    print("FYERS socket error:", message, flush=True)


def on_close(message):
    print("FYERS socket closed:", message, flush=True)


def on_connect():
    print("Connected to FYERS live data.", flush=True)
    print("Subscribing:", SYMBOLS, flush=True)
    fyers.subscribe(symbols=SYMBOLS, data_type="SymbolUpdate")
    fyers.keep_running()


fyers = data_ws.FyersDataSocket(
    access_token=f"{APP_ID}:{ACCESS_TOKEN}",
    log_path="",
    litemode=False,
    write_to_file=False,
    reconnect=True,
    on_connect=on_connect,
    on_message=on_message,
    on_error=on_error,
    on_close=on_close,
)

print("Starting FYERS live market feed...", flush=True)
fyers.connect()

while True:
    time.sleep(60)
