import json
import csv
import googleapiclient.discovery
import googleapiclient.errors
import google_auth_oauthlib.flow


scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

api_service_name = "youtube"
api_version = "v3"
developer_key = "AIzaSyCQ7pxDuHY2_bymJf0ZbqUFXIFQ36TLYdo"


def get_videos():
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=developer_key)

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

        file_videos = open("videos.csv", "w", newline="")

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


def get_channels():
    with open('client_secret.json', 'r', encoding='utf-8') as client_secrets_file:
        client_secrets_file = client_secrets_file.read()

    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)

    credentials = flow.run_console()

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    request = youtube.subscriptions().list(
        part="snippet,contentDetails",
        mine=True
    )
    response = request.execute()

    print(response)


get_channels()
