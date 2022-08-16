from functions.download_videos import download_videos
from functions.upload_videos import upload_videos
from functions.get_subscriptions import get_subscriptions
from functions.get_videos import get_videos
import os
import csv
import requests


def main():

    download_videos("FOOT BALL", "pvOZ3lOVkaY")
    upload_videos("FOOT BALL", "pvOZ3lOVkaY")


if __name__ == "__main__":
    main()
