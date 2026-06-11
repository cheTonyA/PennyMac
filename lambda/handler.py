import json
import os
import urllib.request
from datetime import date, timedelta
import boto3


dynamodb = boto3.resource("dynamodb")


def get_previous_day():
    return (date.today() - timedelta(days=1)).isoformat()


def fetch_stock_data(ticker, trade_date, api_key):
    url = (
        f"https://api.massive.com/v1/open-close/{ticker}/{trade_date}"
        f"?adjusted=true&apiKey={api_key}"
    )

    with urllib.request.urlopen(url) as response:
        return json.loads(response.read().decode("utf-8"))


def lambda_handler(event, context):
    api_key = os.environ["MASSIVE_API_KEY"]
    table_name = os.environ["DYNAMODB_TABLE"]
    watchlist = os.environ["WATCHLIST"].split(",")

    table = dynamodb.Table(table_name)
    trade_date = get_previous_day()

    results = []

    for ticker in watchlist:
        try:
            data = fetch_stock_data(ticker, trade_date, api_key)

            open_price = float(data["open"])
            close_price = float(data["close"])
            percent_change = ((close_price - open_price) / open_price) * 100

            results.append({
                "ticker": ticker,
                "open": open_price,
                "close": close_price,
                "percent_change": percent_change
            })

        except Exception as e:
            print(f"Failed to process {ticker}: {e}")

    if not results:
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
        "percent_change": str(round(top_mover["percent_change"], 2)),
        "all_results": json.dumps(results)
    }

    table.put_item(Item=item)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Stock data processed successfully",
            "top_mover": item
        })
    }