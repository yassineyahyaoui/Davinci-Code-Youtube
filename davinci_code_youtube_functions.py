import csv
import googleapiclient.discovery


api_service_name = "youtube"
api_version = "v3"
developer_key = "AIzaSyCQ7pxDuHY2_bymJf0ZbqUFXIFQ36TLYdo"
youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=developer_key)


def get_videos():
    request_videos = youtube.search().list(
        part="snippet,id",
        channelId="UCJvgF5uUL22U7i9tNlPvduA",
        order="date",
        maxResults=50
    )
    response_videos = request_videos.execute()

    file_videos = open("videos.csv", "r", newline="")
    content = file_videos.read()
    if ("Channel title" or "Video id" or "Video title") not in content:
        file_videos.close()

        file_videos = open("videos.csv", "a", newline="")

        row = ("Channel title", "Video id", "Video title")

        csv.writer(file_videos).writerow(row)

        file_videos.close()

    for video in response_videos["items"]:
        if "videoId" in video["id"]:
            file_videos = open("videos.csv", "r", newline="")

            content = file_videos.read()

            if video["id"]["videoId"] not in content:
                file_videos.close()

                file_videos = open("videos.csv", "a", newline="")

                channel_title = video["snippet"]["channelTitle"]
                video_id = video["id"]["videoId"]
                video_title = video["snippet"]["title"].encode("utf-8")

                row = (channel_title, video_id, video_title)

                csv.writer(file_videos).writerow(row)

                file_videos.close()
            else:
                file_videos.close()
