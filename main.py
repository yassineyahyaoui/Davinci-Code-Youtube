import json
import csv
import googleapiclient.discovery

def main():

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyCQ7pxDuHY2_bymJf0ZbqUFXIFQ36TLYdo"

    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=DEVELOPER_KEY)

    request_videos = youtube.search().list(
        part="snippet,id",
        channelId="UCJvgF5uUL22U7i9tNlPvduA",
        order="date",
        maxResults=5
    )
    response_videos = request_videos.execute()

    print(response_videos)

    for video in response_videos["items"]:
        print(video)

        file_videos = open("videos.csv", "a", newline="")

        channel_id = video["snippet"]["channelId"]
        video_id = video["id"]["videoId"]
        video_title = video["snippet"]["title"].encode("utf-8")

        row = (channel_id, video_id, video_title)

        csv.writer(file_videos).writerow(row)

        file_videos.close()

if __name__ == "__main__":
    main()
