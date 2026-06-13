import json
import os
import time
import urllib.error
import urllib.request
from datetime import date, timedelta

import boto3


dynamodb = boto3.resource("dynamodb")
secrets_client = boto3.client("secretsmanager")

_cached_api_key = None


def log(level, message, **kwargs):
    print(json.dumps({
        "level": level,
        "message": message,
        **kwargs
    }))


def get_previous_day():
    return (date.today() - timedelta(days=1)).isoformat()


def get_massive_api_key():
    global _cached_api_key

    if _cached_api_key:
        return _cached_api_key

    secret_arn = os.environ["MASSIVE_SECRET_ARN"]
    response = secrets_client.get_secret_value(SecretId=secret_arn)

    secret_value = response["SecretString"]

    try:
        parsed_secret = json.loads(secret_value)
        _cached_api_key = parsed_secret["MASSIVE_API_KEY"]
    except json.JSONDecodeError:
        _cached_api_key = secret_value

    return _cached_api_key


def fetch_stock_data(ticker, trade_date, api_key, retries=3):
    url = (
        f"https://api.massive.com/v1/open-close/{ticker}/{trade_date}"
        f"?adjusted=true&apiKey={api_key}"
    )

    for attempt in range(1, retries + 1):
        try:
            with urllib.request.urlopen(url, timeout=10) as response:
                data = json.loads(response.read().decode("utf-8"))

            log(
                "INFO",
                "Fetched stock data",
                ticker=ticker,
                trade_date=trade_date,
                attempt=attempt
            )

            return data

        except urllib.error.HTTPError as e:
            retryable = e.code in [429, 500, 502, 503, 504]

            log(
                "WARN" if retryable else "ERROR",
                "Massive API HTTP error",
                ticker=ticker,
                trade_date=trade_date,
                status_code=e.code,
                attempt=attempt,
                retryable=retryable
            )

            if not retryable or attempt == retries:
                raise

            time.sleep(2 ** (attempt - 1))

        except Exception as e:
            log(
                "WARN",
                "Massive API request failed",
                ticker=ticker,
                trade_date=trade_date,
                error=str(e),
                attempt=attempt
            )

            if attempt == retries:
                raise

            time.sleep(2 ** (attempt - 1))


def lambda_handler(event, context):
    api_key = get_massive_api_key()
    table_name = os.environ["DYNAMODB_TABLE"]
    watchlist = os.environ["WATCHLIST"].split(",")

    table = dynamodb.Table(table_name)
    trade_date = get_previous_day()

    log(
        "INFO",
        "Starting daily stock processing",
        trade_date=trade_date,
        watchlist=watchlist
    )

    results = []

    for ticker in watchlist:
        try:
            data = fetch_stock_data(ticker, trade_date, api_key)

            open_price = float(data["open"])
            close_price = float(data["close"])
            percent_change = ((close_price - open_price) / open_price) * 100

            results.append({
                "ticker": ticker,
                "open": round(open_price, 2),
                "close": round(close_price, 2),
                "percent_change": round(percent_change, 2)
            })

        except Exception as e:
            log(
                "ERROR",
                "Failed to process ticker",
                ticker=ticker,
                trade_date=trade_date,
                error=str(e)
            )

    if not results:
        log(
            "ERROR",
            "No stock data processed",
            trade_date=trade_date
        )

        return {
            "statusCode": 500,
            "body": json.dumps({"message": "No stock data processed"})
        }

    top_mover = max(results, key=lambda x: abs(x["percent_change"]))

    item = {
        "trade_date": trade_date,
        "ticker": top_mover["ticker"],
        "open": str(top_mover["open"]),
        "close": str(top_mover["close"]),
        "percent_change": str(top_mover["percent_change"]),
        "all_results": json.dumps(results)
    }

    table.put_item(Item=item)

    log(
        "INFO",
        "Stored top mover result",
        trade_date=trade_date,
        ticker=top_mover["ticker"],
        percent_change=top_mover["percent_change"],
        close=top_mover["close"]
    )

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Stock data processed successfully",
            "top_mover": {
                "trade_date": trade_date,
                "ticker": top_mover["ticker"],
                "open": top_mover["open"],
                "close": top_mover["close"],
                "percent_change": top_mover["percent_change"]
            }
        })
    }