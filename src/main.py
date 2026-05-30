import json
import boto3
import os

TABLE_NAME = os.environ["TABLE_NAME"]
PK_VALUE = os.environ["PK_VALUE"]

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)


def lambda_handler(event, context):

    print("EVENT:", json.dumps(event))

    record = event["Records"][0]

    bucket = record["s3"]["bucket"]["name"]
    key = record["s3"]["object"]["key"]

    print(f"Bucket={bucket}")
    print(f"Key={key}")

    # Vérifier si déjà enregistré
    response = table.get_item(
        Key={
            "PK": PK_VALUE,
            "SK": key
        }
    )

    if "Item" in response:
        print("Fichier déjà traité")
        return {
            "statusCode": 200,
            "body": json.dumps("Already processed")
        }

    # Sinon enregistrer
    table.put_item(
        Item={
            "PK": PK_VALUE,
            "SK": key,
            "bucket": bucket
        }
    )

    print("Fichier enregistré")

    return {
        "statusCode": 200,
        "body": json.dumps("Processed")
    }

    