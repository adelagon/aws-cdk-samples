import os
import json
import urllib.request

def handler(event, context):
    body = json.loads(event['Records'][0]['body'])
    print ("Got Task from Queue: {}".format(body))
    url = os.path.join(body['url'], body['id'])
    
    print ("Sending API call to: {}".format(url))
    print ("HELLO SMIC!")
    req = urllib.request.Request(url)
    try:
        res = urllib.request.urlopen(url)
        print("API Call Successful: {}".format(res.read()))
    except urllib.error.HTTPError as e:
        print("Got Error Response: {}".format(e.code))
        print(e.read())