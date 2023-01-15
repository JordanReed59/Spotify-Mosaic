"""
File that will get the tracks from a Spotify playlist
"""
from curses import color_content
import cv2
import numpy as np
import requests
import spotipy
import os

from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials
from logging import raiseExceptions
from sklearn.cluster import KMeans
from collections import Counter

load_dotenv() #load envirnoment vars from .env files

CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
PLAYLIST_ID = "1BXj2SlxJLcXSy07Fv9Bgg"
TRACK_IMAGE_HIEGHT = 64
TRACK_IMAGE_WIDTH = 64


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

def get_images_dominant_color(trackData):
    image_objects = []
    colors = []
    for image in trackData:
        
        try:
            url = image["imageURL"]
            res = requests.get(url, stream = True)
            npArr = np.frombuffer(res.content, np.uint8)
            imgArr = cv2.imdecode(npArr, cv2.IMREAD_UNCHANGED)

            color = most_dominent_color(imgArr)

            imgData = {
                "color" : color,
                "image" : imgArr
            }

            image_objects.append(imgData)
            colors.append(color)

        except requests.exceptions.RequestException as e:
            # print("Call to Spotify to download track image failed: Ensure id is correct")
            raise e
            
    return image_objects, colors
    

def most_dominent_color(imgArr, size=(16, 16), k=4):
    # resize image for faster processing
    image = cv2.resize(imgArr, size, 
                            interpolation = cv2.INTER_AREA)

    # turn image array into 1D array 
    image = image.reshape((image.shape[0] * image.shape[1], 3))

    #cluster and assign labels to the pixels 
    clt = KMeans(n_clusters = k)
    labels = clt.fit_predict(image)

    #count labels to find most popular
    label_counts = Counter(labels)

    #subset out most popular centroid and round color
    dominant_color = clt.cluster_centers_[label_counts.most_common(1)[0][0]]
    rounded = np.around(dominant_color)
    # image = np.zeros((16, 16, 3), np.uint8)
    # image[:] = dominant_color
    # save_image("./images/second-image-dominant-color.png", image)

    return rounded

"""
Function that finds the closest color in a list of colors
"""
def closest_color(colors, color):
    colors = np.array(colors)
    color = np.array(color)
    distances = np.sqrt(np.sum((colors-color)**2,axis=1))
    index_of_smallest = np.where(distances==np.amin(distances))
    smallest_distance = colors[index_of_smallest]
    return index_of_smallest[0][0], smallest_distance 

def save_image(filename, imgArr):
    cv2.imwrite(filename, imgArr)

def resize_image(imgArr, size=(16, 16)):
    image = cv2.resize(imgArr, size, 
                            interpolation = cv2.INTER_AREA)

    return image

def create_mosaic():
    # resize org image and create new blank image
    # loop thru each pixel and find closest color
    # write color to image
    width = 100
    height = 100

    for i in range(width):
        for j in range(height):
            pass
    pass

"""
Function will write smaller image to larger image at a specified coordinate

@param: image - image object that will be written to
@param: tile - smaller image that 
@param: coord - the x and y coordinate where the tile will be pasted
"""
def paste_tile(image, tile, coord):
    x1, x2 = coord[1], coord[1] + TRACK_IMAGE_WIDTH
    y1, y2 = coord[0], coord[0] + TRACK_IMAGE_HIEGHT

    image[y1:y2, x1:x2] = tile


def main():
    track_data = get_track_data(PLAYLIST_ID)
    # print(len(track_data))

    imageData, colors = get_images_dominant_color(track_data)

    # pathToImg = "./images/beach-255x198.jpeg"
    # img = cv2.imread(pathToImg)

    # create_mosaic()


    track_img = imageData[0]["image"]
    # print(track_img)
    blank_image = np.zeros((100,100,3), np.uint8)
    paste_tile(blank_image, track_img, (0,0))
    save_image("./images/testPastedTile.jpg", blank_image)



if __name__=="__main__":
    main()