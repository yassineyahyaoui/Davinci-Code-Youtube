import os
import csv


def add_cracked_videos(targeted_channel, video_id):
    update_cracked_videos_file(targeted_channel, video_id)
    update_downloaded_videos_file(targeted_channel, video_id)


def update_cracked_videos_file(targeted_channel, video_id):
    downloaded_videos_list = []
    file_downloaded_videos = open(os.path.join("data", targeted_channel, "downloaded_videos.csv"), "r", newline="")
    content = csv.DictReader(file_downloaded_videos)
    for video in content:
        downloaded_videos_list.append(video)
    file_downloaded_videos.close()

    for video in downloaded_videos_list:
        if video["Video id"] == video_id:
            file_cracked_videos = open(os.path.join("data", targeted_channel, "cracked_videos.csv"), "a", newline="")
            row = (video["Channel name"], video["Video id"], video["Video title"], video["Video description"], video["Video thumbnail"], video["Video category"],
                   video["Video rating"], video["Video view count"], video["Video like count"],
                   video["Video comment count"], video["Video license"], video["Video duration"],
                   video["Video publish time"])
            csv.writer(file_cracked_videos).writerow(row)
            file_cracked_videos.close()


def update_downloaded_videos_file(targeted_channel, video_id):
    downloaded_videos_list = []
    file_downloaded_videos = open(os.path.join("data", targeted_channel, "downloaded_videos.csv"), "r", newline="")
    content = csv.DictReader(file_downloaded_videos)
    for video in content:
        downloaded_videos_list.append(video)
    file_downloaded_videos.close()

    file_downloaded_videos = open(os.path.join("data", targeted_channel, "downloaded_videos.csv"), "w", newline="")
    row = ("Channel name", "Video id", "Video title", "Video description", "Video thumbnail", "Video category", "Video rating", "Video view count",
           "Video like count", "Video comment count", "Video license", "Video duration", "Video publish time")
    csv.writer(file_downloaded_videos).writerow(row)
    file_downloaded_videos.close()

    for video in downloaded_videos_list:
        if video["Video id"] != video_id:
            file_videos = open(os.path.join("data", targeted_channel, "downloaded_videos.csv"), "a", newline="")
            row = (video["Channel name"], video["Video id"], video["Video title"], video["Video description"], video["Video thumbnail"], video["Video category"], video["Video rating"], video["Video view count"], video["Video like count"], video["Video comment count"], video["Video license"], video["Video duration"], video["Video publish time"])
            csv.writer(file_videos).writerow(row)
            file_downloaded_videos.close()
