import os
import csv
from pytube import YouTube


def download_videos(targeted_channel, video_id):
    yt = YouTube("https://www.youtube.com/" + video_id)
    yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download("C:/Users/DELL/PycharmProjects/Davinci-Code-Youtube/data/" + targeted_channel)
    print("completed")
    check_downloaded_videos_file(targeted_channel)


def check_downloaded_videos_file(targeted_channel):
    if not os.path.exists(os.path.join("data", targeted_channel, "downloaded_videos.csv")):
        file_downloaded_videos = open(os.path.join("data", targeted_channel, "downloaded_videos.csv"), "w", newline="")
        file_downloaded_videos.close()

    file_downloaded_videos = open(os.path.join("data", targeted_channel, "downloaded_videos.csv"), "r", newline="")
    content = file_downloaded_videos.read()
    file_downloaded_videos.close()

    if ("Channel name" or "Video id" or "Video title" or "Video description" or "Video rating" or "Video view count" or "Video like count" or "Video comment count" or "Video license" or "Video duration" or "Video publish time") not in content:
        file_downloaded_videos = open(os.path.join("data", targeted_channel, "downloaded_videos.csv"), "w", newline="")
        row = ("Channel name", "Video id", "Video title", "Video description", "Video rating", "Video view count", "Video like count", "Video comment count", "Video license", "Video duration", "Video publish time")
        csv.writer(file_downloaded_videos).writerow(row)
        file_downloaded_videos.close()


