"""
File that will get the tracks from a Spotify playlist
"""
import cv2
import numpy as np
import requests
import spotipy
import os

# from curses import color_content
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials
from logging import raiseExceptions
from sklearn.cluster import KMeans
from collections import Counter

config = load_dotenv(".env") #load envirnoment vars from .env files

CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
PLAYLIST_ID = "1BXj2SlxJLcXSy07Fv9Bgg"
TRACK_IMAGE_DIM = 16
SCALE_IMAGE_PERCENTAGE = 50
SCALE_TRACK_PERCENTAGE = 25


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

def get_dominant_colors(trackData):
    image_objects = []
    colors = []
    for image in trackData:
        
        try:
            url = image["imageURL"]
            res = requests.get(url, stream = True)
            npArr = np.frombuffer(res.content, np.uint8)
            imgArr = cv2.imdecode(npArr, cv2.IMREAD_UNCHANGED)
            resizedImgArr = resize_image(imgArr, SCALE_TRACK_PERCENTAGE)
            # resize_image(imgArr, SCALE_TRACK_PERCENTAGE)
            color = most_dominent_color(resizedImgArr)

            # resize track image and add to imgData
            # resizedImgArr = resize_image(imgArr, SCALE_TRACK_PERCENTAGE)

            imgData = {
                "color" : color,                     
                "image" : resizedImgArr
            }

            image_objects.append(imgData)
            colors.append(color)

        except requests.exceptions.RequestException as e:
            # print("Call to Spotify to download track image failed: Ensure id is correct")
            raise e
            
    return image_objects, colors
    

def most_dominent_color(imgArr, size=(16, 16), k=4):
    # resize image for faster processing
    # image = cv2.resize(imgArr, size, 
    #                         interpolation = cv2.INTER_AREA)

    # turn image array into 1D array 
    image = imgArr.reshape((imgArr.shape[0] * imgArr.shape[1], 3))

    #cluster and assign labels to the pixels 
    clt = KMeans(n_clusters = k, n_init="auto")
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
    closest = colors[index_of_smallest]
    return index_of_smallest[0][0]# , closest 

def save_image(filename, imgArr):
    cv2.imwrite(filename, imgArr)

def resize_image(imgArr, scale):
    width = int(imgArr.shape[1] * scale / 100)
    height = int(imgArr.shape[0] * scale / 100)
    dim = (width, height)
    image = cv2.resize(imgArr, dim, interpolation = cv2.INTER_AREA)

    return image

def create_mosaic(imgArr, imageData, colors):
    # resize org image and create new blank image
    # loop thru each pixel and find closest color
    # write color to image
    height = imgArr.shape[0]
    width = imgArr.shape[1]
    # print(width, height)

    mosaic = np.zeros((height * TRACK_IMAGE_DIM,width * TRACK_IMAGE_DIM,3), np.uint8)

    # pixel = imgArr[0][0]
    # print(pixel)
    # index = closest_color(colors, pixel)
    # print(colors[index])

    # paste_tile(blank_image, imageData[index]["image"], [0,0])
    

    curr_x = 0
    for i in range(height):
        # print(curr_x)
        curr_y = 0
        for j in range(width):
            pixel = imgArr[i][j]
            # print(type(pixel))
            index = closest_color(colors, pixel)
            # print(colors[index])
            paste_tile(mosaic, imageData[index]["image"], [curr_x,curr_y])
            
            curr_y += 16
            # print([curr_x,curr_y])
        curr_x += 16
    save_image(f"./images/simple-resolution-{SCALE_IMAGE_PERCENTAGE}.jpg", mosaic)
        

"""
Function will write smaller image to larger image at a specified coordinate

@param: image - image object that will be written to
@param: tile - smaller image that 
@param: coord - the x and y coordinate where the tile will be pasted
"""
def paste_tile(image, tile, coord):
    x1, x2 = coord[1], coord[1] + TRACK_IMAGE_DIM
    y1, y2 = coord[0], coord[0] + TRACK_IMAGE_DIM

    image[y1:y2, x1:x2] = tile


def main():
    print("Getting track image data from spotify...")
    track_data = get_track_data(PLAYLIST_ID)
    # print(len(track_data))
    print("Calculating tracks most dominant color...")
    imageData, colors = get_dominant_colors(track_data)

    # pathToImg = "./images/beach-255x198.jpeg"
    # img = cv2.imread(pathToImg)

    # create_mosaic()


    # track_img = imageData[0]["image"]
    # print(track_img)
    # blank_image = np.zeros((100,100,3), np.uint8)
    # paste_tile(blank_image, track_img, (0,0))
    # save_image("./images/testPastedTile.jpg", blank_image)

    # testing resizing
    # pathToImg = "./images/beach-800x800.jpg"
    # test_img = cv2.imread(pathToImg)
    # resized = resize_image(track_img, SCALE_TRACK_PERCENTAGE)
    # resized = resize_image(test_img, SCALE_IMAGE_PERCENTAGE)
    # save_image("./images/testNewResize_3.jpg", resized)

    # testing mosaic creation
    print("Reading in test image")
    pathToImg = "./images/purple_tree.jpg"
    test_img = cv2.imread(pathToImg)
    resized = resize_image(test_img, SCALE_IMAGE_PERCENTAGE)
    print("Creating Mosaic image")
    create_mosaic(resized, imageData, colors)
    print("Finished creating Mosaic image")

# to install packages: pip install -r requirements.txt 



if __name__=="__main__":
    main()