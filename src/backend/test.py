# import cv2
# import numpy as np
# import requests
# import spotipy
# import os

# from curses import color_content
# from dotenv import load_dotenv
# from spotipy.oauth2 import SpotifyClientCredentials
# from logging import raiseExceptions
# from sklearn.cluster import KMeans
# from collections import Counter

def lambda_handler(event, context):
    # requests.get("https://www.google.com/search?q=hello")
    print(event)
    response = {
        "statusCode": 200,
        "headers": {
            'Content-Type': 'text/html; charset=utf-8',
        },
        "body": "The backend says hi!"
    }

    return response
    