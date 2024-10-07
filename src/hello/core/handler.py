import json
from src.btg import say_hello_from_btg_repository


def respond(res, status=200):

    return {
        "isBase64Encoded": False,
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json",
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
            'Access-Control-Allow-Headers': 'Content-Type'
        },
        "body": json.dumps(res)
    }


def hello(event, context):
    return respond({"msg": "Hello", "repository_msg": say_hello_from_btg_repository()}, status=200)
