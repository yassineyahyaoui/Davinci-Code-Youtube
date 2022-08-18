from functions.get_subscriptions import get_subscriptions
from functions.get_videos import get_videos
from functions.download_videos import download_videos
from functions.upload_videos import upload_videos
from functions.add_cracked_videos import add_cracked_videos
import os
import csv
import requests


def main():
    # GET SUBSCRIPTIONS
    get_subscriptions("FOOT BALL")

    # GET VIDEOS
    file_channels = open(os.path.join("data", "FOOT BALL", "channels.csv"), "r", newline="")
    content = csv.DictReader(file_channels)
    for row in content:
        get_videos("FOOT BALL", row["Channel id"], True)
    file_channels.close()

    # DOWNLOAD VIDEOS
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

    # UPLOAD OR CRACK VIDEOS
    file_downloaded_videos = open(os.path.join("data", "FOOT BALL", "downloaded_videos.csv"), "r", newline="")
    content_downloaded_videos = csv.DictReader(file_downloaded_videos)
    try:
        i = 0
        for row in content_downloaded_videos:
            if i < 2:
                upload_videos("FOOT BALL", row["Video id"])
            i = i + 1
        file_downloaded_videos.close()
    except:
        i = 0
        for row in content_downloaded_videos:
            if i < 1:
                add_cracked_videos("FOOT BALL", row["Video id"])
            i = i + 1
        file_downloaded_videos.close()
        print("The write operation timed out")


if __name__ == "__main__":
    main()
