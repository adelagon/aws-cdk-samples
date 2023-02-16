import json
import requests

def handler(event, context):
    print("Scheduled Event Triggered")
    r = requests.get("https://api.chucknorris.io/jokes/random")
    print(r.json())
    return r.json()['value']