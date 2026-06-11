import json
import os
import boto3

dynamodb = boto3.resource("dynamodb")


def lambda_handler(event, context):
    table_name = os.environ["DYNAMODB_TABLE"]
    table = dynamodb.Table(table_name)

    response = table.scan()

    items = response.get("Items", [])

    items = sorted(
        items,
        key=lambda x: x["trade_date"],
        reverse=True
    )[:7]

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(items)
    }