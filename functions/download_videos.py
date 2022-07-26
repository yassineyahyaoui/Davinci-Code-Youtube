import os
import csv
from pytube import YouTube


def download_videos(targeted_channel, video_id):
    yt = YouTube("https://www.youtube.com/" + video_id)
    yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download("/data/" + targeted_channel + "/videos/" + video_id)

    check_downloaded_videos_file(targeted_channel)
    update_downloaded_videos_file(targeted_channel, video_id)
    update_videos_file(targeted_channel, video_id)


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


def update_downloaded_videos_file(targeted_channel, video_id):
    videos_list = []
    file_videos = open(os.path.join("data", targeted_channel, "videos.csv"), "r", newline="")
    content = csv.DictReader(file_videos)
    for video in content:
        videos_list.append(video)
    file_videos.close()

    for video in videos_list:
        if video["Video id"] == video_id:
            file_downloaded_videos = open(os.path.join("data", targeted_channel, "downloaded_videos.csv"), "a",
                                          newline="")
            row = (video["Channel name"], video["Video id"], video["Video title"], video["Video description"],
                   video["Video rating"], video["Video view count"], video["Video like count"],
                   video["Video comment count"], video["Video license"], video["Video duration"],
                   video["Video publish time"])
            csv.writer(file_downloaded_videos).writerow(row)
            file_downloaded_videos.close()


def update_videos_file(targeted_channel, video_id):
    videos_list = []
    file_videos = open(os.path.join("data", targeted_channel, "videos.csv"), "r", newline="")
    content = csv.DictReader(file_videos)
    for video in content:
        videos_list.append(video)
    file_videos.close()

    file_videos = open(os.path.join("data", targeted_channel, "videos.csv"), "w", newline="")
    row = ("Channel name", "Video id", "Video title", "Video description", "Video rating", "Video view count",
           "Video like count", "Video comment count", "Video license", "Video duration", "Video publish time")
    csv.writer(file_videos).writerow(row)
    file_videos.close()

    for video in videos_list:
        if video["Video id"] != video_id:
            file_videos = open(os.path.join("data", targeted_channel, "videos.csv"), "a", newline="")
            row = (video["Channel name"], video["Video id"], video["Video title"], video["Video description"], video["Video rating"], video["Video view count"], video["Video like count"], video["Video comment count"], video["Video license"], video["Video duration"], video["Video publish time"])
            csv.writer(file_videos).writerow(row)
            file_videos.close()
