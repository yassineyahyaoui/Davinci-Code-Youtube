import os
import csv
import googleapiclient.discovery
import googleapiclient.errors


api_service_name = "youtube"
api_version = "v3"
developer_key = "AIzaSyCQ7pxDuHY2_bymJf0ZbqUFXIFQ36TLYdo"


def get_videos():
    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=developer_key)

    request = youtube.search().list(
        part="snippet,id",
        channelId="UCJvgF5uUL22U7i9tNlPvduA",
        order="date",
        maxResults=50
    )
    response = request.execute()

    file_videos = open(os.path.join("data", "videos.csv"), "r", newline="")
    content = file_videos.read()
    file_videos.close()

    if ("Channel title" or "Video id" or "Video title") not in content:
        file_videos = open(os.path.join("data", "videos.csv"), "w", newline="")

        row = ("Channel title", "Video id", "Video title")
        csv.writer(file_videos).writerow(row)
        file_videos.close()

    for video in response["items"]:
        if "videoId" in video["id"]:
            file_videos = open(os.path.join("data", "videos.csv"), "r", newline="")
            content = file_videos.read()
            file_videos.close()

            if video["id"]["videoId"] not in content:
                file_videos = open(os.path.join("data", "videos.csv"), "a", newline="")

                channel_title = video["snippet"]["channelTitle"]
                video_id = video["id"]["videoId"]
                video_title = video["snippet"]["title"].encode("utf-8")

                row = (channel_title, video_id, video_title)
                csv.writer(file_videos).writerow(row)
                file_videos.close()
