import requests

def lambda_handler(event, context):
    requests.get("https://www.google.com/search?q=hello")
    print(event)
    