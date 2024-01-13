from flask import Flask
import boto3
from boto3.dynamodb.conditions import Key
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
request_count = 0       


@app.route('/')
def get_data_dynamoDB():
    global request_count
    request_count += 1
    
    __TableName__ = "542final"

    DB = boto3.resource('dynamodb')
    table = DB.Table(__TableName__)

    air_condition = Key('type').eq("air") & Key('datatime').gt("2023-11-18T07:52:58.057Z")  # greater than
    air_response = table.query(
        KeyConditionExpression=air_condition,
        ScanIndexForward=False,
        Limit=1
    )

    soil_condition = Key('type').eq("soil") & Key('datatime').gt("2023-11-18T07:52:58.057Z")  # greater than

    soil_response = table.query(
        KeyConditionExpression=soil_condition,
        ScanIndexForward=False,
        Limit=1
    )

    air_item = air_response.get('Items', [])[0] if air_response.get('Items') else None
    soil_item = soil_response.get('Items', [])[0] if soil_response.get('Items') else None

    return {'air': air_item, 'soil': soil_item}


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=3100)
