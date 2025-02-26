# -*- coding: utf-8 -*-
import boto3
import json
from botocore.config import Config

config = Config(
    retries={"max_attempts": 10, "mode": "standard"},
    connect_timeout=5,
    read_timeout=5,
)
session = boto3.Session(profile_name="smartflux")
endpoint_url = "https://fmqkl4r7pk.execute-api.us-east-1.amazonaws.com/production"
# endpoint_url = "https://vpce-03139a52c49e45519-84bkg7fs-us-east-1b.execute-api.us-east-1.vpce.amazonaws.com/production"
client = session.client(
    "apigatewaymanagementapi",
    endpoint_url=endpoint_url,
    region_name="us-east-1",
    config=config,
)
connection_id = "GmEkcd9QIAMCIGg="
print("send")
response = client.post_to_connection(
    ConnectionId=connection_id, Data=json.dumps({"test": "conect1"})
)
print(response)
