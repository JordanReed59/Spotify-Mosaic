"""
File that will get the tracks from a Spotify playlist
"""
import spotipy
import os

from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv() #load envirnoment vars from .env files

CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')

def main():
    
    print(CLIENT_ID, CLIENT_SECRET)
    print(os.environ.get('USER'))
    auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    sp = spotipy.Spotify(auth_manager=auth_manager)
    print(sp)
    

if __name__=="__main__":
    main()