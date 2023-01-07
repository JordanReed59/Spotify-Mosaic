"""
File that will get the tracks from a Spotify playlist
"""
import cv2
import numpy as np
import requests
import spotipy
import os

from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials
from logging import raiseExceptions

load_dotenv() #load envirnoment vars from .env files

CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
PLAYLIST_ID = "1BXj2SlxJLcXSy07Fv9Bgg"

"""
Function that extracts track data from a playlist

@param playlistid - id of playlist
@return tracks - list of data for each track

"""
def get_track_data(playlistId):
    try:
        auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
        sp = spotipy.Spotify(auth_manager=auth_manager)
        playlist = sp.playlist_tracks(playlistId)

    except spotipy.SpotifyException as e:
        raise e

    # extract useful attributes
    seenAlbums = [] #ensures that we don't get duplicate images
    tracks = []
    for item in playlist["items"]:
        albumId = item["track"]["album"]["id"]
        if albumId not in seenAlbums:
            track = {}
            track["songId"] = item["track"]["id"]
            track["imageURL"] = item["track"]["album"]["images"][2]["url"]
            tracks.append(track)
            seenAlbums.append(albumId)

    return tracks

def get_images(trackData):
    for image in trackData:
        try:
            url = image["imageURL"]

            res = requests.get(url, stream = True)
            # print(type(res.content))

            npArr = np.frombuffer(res.content, np.uint8)
            # print(type(npArr))

            imgArr = cv2.imdecode(npArr, cv2.IMREAD_UNCHANGED)
            # print(type(imgArr))

            print(f"Got track image for: {image['songId']}")

        except requests.exceptions.RequestException as e:
            # print("Call to Spotify to download track image failed: Ensure id is correct")
            raise e


def main():
    track_data = get_track_data(PLAYLIST_ID)
    print(len(track_data))

    get_images(track_data)


if __name__=="__main__":
    main()