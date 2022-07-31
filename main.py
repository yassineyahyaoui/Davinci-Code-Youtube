from functions.download_videos import download_videos
from functions.upload_videos import upload_videos
from functions.get_subscriptions import get_subscriptions
from functions.get_videos import get_videos
import os
import csv
from pytube import YouTube
import requests
import struct


def main():
    # get_subscriptions("FOOT BALL")
    file_channels = open(os.path.join("data", "FOOT BALL", "channels.csv"), "r", newline="")
    content = csv.DictReader(file_channels)
    for row in content:
        get_videos("FOOT BALL", row["Channel id"], True)
    file_channels.close()

    file_videos = open(os.path.join("data", "FOOT BALL", "videos.csv"), "r", newline="")
    content = csv.DictReader(file_videos)
    i = 0
    for row in content:
        request = requests.get("https://www.youtube.com/watch?v=" + row["Video id"]).status_code
        if request == 200:
            if i < 2:
                download_videos("FOOT BALL", row["Video id"])
            i = i + 1
    file_videos.close()

    # request = requests.get("https://www.youtube.com/watch?v=Exc8PiwCUiI")
    # print(request.status_code)



    #upload_videos("FOOT BALL")
    #channels2 = []

    #file_videos = open(os.path.join("data", "FOOT BALL", "channels.csv"), "r", newline="")
    #content = csv.DictReader(file_videos)
    #for row in content:
        #channels2.append(row)
        #get_videos("FOOT BALL", row["Channel id"], True)
    #file_videos.close()

    #request = requests.get("https://www.youtube.com/watch?v=Exc8PiwCUiI")
    #print(request.status_code)
    #yt = YouTube("https://www.youtube.com/Exc8PiwCUiI")
    #yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(os.getcwd() + "/data/FOOT BALL/videos/Exc8PiwCUiI")


if __name__ == "__main__":
    main()
