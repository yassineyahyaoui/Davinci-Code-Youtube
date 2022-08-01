import os
import csv
import pickle
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload
from pytube import YouTube
from datetime import date, timedelta


scopes = ["https://www.googleapis.com/auth/youtube.readonly", "https://www.googleapis.com/auth/youtube.upload"]
api_service_name = "youtube"
api_version = "v3"
developer_key = "AIzaSyCQ7pxDuHY2_bymJf0ZbqUFXIFQ36TLYdo"
client_secrets_file = "client_secret.json"


def upload_videos(targeted_channel, video_id):
    youtube = get_authenticated_service(targeted_channel)

    videos = []
    file_downloaded_videos = open(os.path.join("data", targeted_channel, "downloaded_videos.csv"), "r", newline="")
    content = csv.DictReader(file_downloaded_videos)
    for video in content:
        videos.append(video)
    file_downloaded_videos.close()

    for video in videos:
        if video["Video id"] == video_id:
            yt = YouTube("https://www.youtube.com/" + video_id)
            video_title = yt.streams.get_highest_resolution().title

            request = youtube.videos().insert(
                part="snippet,status",
                body={
                    "snippet": {
                        "title": video_title,
                        "description": video_title,
                        "categoryId": video["Video category"]
                    },
                    "status": {
                        "privacyStatus": "private",
                        "publishAt": date.today() + timedelta(days=1) + video["Video publish time"][10:]
                    }
                },

                media_body=MediaFileUpload(os.getcwd() + "/data/FOOT BALL/videos/" + video_id + "/" + video_title + ".mp4")
            )
            response = request.execute()
            print(response)
            print(video_title)


def get_authenticated_service(targeted_channel):
    if os.path.exists(os.path.join("data", targeted_channel, "CREDENTIALS_PICKLE_FILE")):
        with open(os.path.join("data", targeted_channel, "CREDENTIALS_PICKLE_FILE"), 'rb') as f:
            credentials = pickle.load(f)
    else:
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
        credentials = flow.run_console()
        with open(os.path.join("data", targeted_channel, "CREDENTIALS_PICKLE_FILE"), 'wb') as f:
            pickle.dump(credentials, f)
    return googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)
