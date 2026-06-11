import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
LAMBDA_DIR = PROJECT_ROOT / "lambda"
sys.path.insert(0, str(LAMBDA_DIR))

os.environ["MASSIVE_API_KEY"] = "test-key"
os.environ["DYNAMODB_TABLE"] = "test-table"
os.environ["WATCHLIST"] = "AAPL,MSFT,GOOGL,AMZN,TSLA,NVDA"

import handler


def test_percent_change_math():
    open_price = 100
    close_price = 110

    percent_change = ((close_price - open_price) / open_price) * 100

    assert percent_change == 10


def test_watchlist_env():
    watchlist = os.environ["WATCHLIST"].split(",")

    assert "AAPL" in watchlist
    assert "NVDA" in watchlist
    assert len(watchlist) == 6