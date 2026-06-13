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
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "GET,OPTIONS",
            "Content-Type": "application/json",
            "Cache-Control": "public, max-age=300",
            "X-Project": "Pennymac-Stock-Pipeline",
            "X-Data-Source": "DynamoDB",
            "X-Result-Count": str(len(items))
        },
        "body": json.dumps(items)
    }