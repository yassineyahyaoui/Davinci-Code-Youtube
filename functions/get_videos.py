import os
import csv
import googleapiclient.discovery
import googleapiclient.errors


api_service_name = "youtube"
api_version = "v3"
developer_key = "AIzaSyCQ7pxDuHY2_bymJf0ZbqUFXIFQ36TLYdo"


def get_videos(targeted_channel, video_id):
    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=developer_key)

    request = youtube.search().list(
        part="snippet,id",
        channelId=video_id,
        order="date",
        maxResults=5
    )
    response = request.execute()

    if not os.path.exists(os.path.join("data", targeted_channel, "videos.csv")):
        file_videos = open(os.path.join("data", targeted_channel, "videos.csv"), "w", newline="")
        file_videos.close()

    file_videos = open(os.path.join("data", targeted_channel, "videos.csv"), "r", newline="")
    content = file_videos.read()
    file_videos.close()

    if ("Channel name" or "Video id" or "Video title" or "Video publish time") not in content:
        file_videos = open(os.path.join("data", targeted_channel, "videos.csv"), "w", newline="")

        row = ("Channel name", "Video id", "Video title", "Video publish time")
        csv.writer(file_videos).writerow(row)
        file_videos.close()

    for video in response["items"]:
        if "videoId" in video["id"]:
            file_videos = open(os.path.join("data", targeted_channel, "videos.csv"), "r", newline="")
            content = file_videos.read()
            file_videos.close()

            if video["id"]["videoId"] not in content:
                file_videos = open(os.path.join("data", targeted_channel, "videos.csv"), "a", newline="")

                channel_title = video["snippet"]["channelTitle"].encode("utf-8")
                video_id = video["id"]["videoId"]
                video_title = video["snippet"]["title"].encode("utf-8")
                video_publish_time = video["snippet"]["publishTime"]

                row = (channel_title, video_id, video_title, video_publish_time)
                csv.writer(file_videos).writerow(row)
                file_videos.close()
