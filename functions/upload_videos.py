import os
import pickle
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload
from datetime import date, timedelta


scopes = ["https://www.googleapis.com/auth/youtube.readonly", "https://www.googleapis.com/auth/youtube.upload", "https://www.googleapis.com/auth/youtube.force-ssl"]
api_service_name = "youtube"
api_version = "v3"
developer_key = "AIzaSyCQ7pxDuHY2_bymJf0ZbqUFXIFQ36TLYdo"
client_secrets_file = "client_secret.json"


def upload_videos(targeted_channel, video_id):
    youtube = get_authenticated_service(targeted_channel)

    request = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        id=video_id
    )
    response = request.execute()

    video_title = response["items"][0]["snippet"]["title"]
    video_description = response["items"][0]["snippet"]["description"]
    video_category = response["items"][0]["snippet"]["categoryId"]
    video_publish_time = response["items"][0]["snippet"]["publishedAt"]
    video_tags = []
    if "tags" in response["items"][0]["snippet"]:
        video_tags = response["items"][0]["snippet"]["tags"]

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": video_title,
                "description": video_description,
                "categoryId": video_category,
                "tags": video_tags
            },
            "status": {
                "privacyStatus": "private",
                "publishAt": (date.today() + timedelta(days=1)).strftime("%Y-%m-%d") + video_publish_time[10:]
            }
        },

        media_body=MediaFileUpload(os.getcwd() + "/data/FOOT BALL/videos/" + video_id + "/video.mp4")
    )
    response = request.execute()
    print(response)

    set_thumbnail(targeted_channel, response["id"], video_id)


def set_thumbnail(targeted_channel, targeted_video_id, video_id):
    youtube = get_authenticated_service(targeted_channel)

    request = youtube.thumbnails().set(
        videoId=targeted_video_id,
        media_body=MediaFileUpload(os.getcwd() + "/data/FOOT BALL/videos/" + video_id + "/thumbnail.png")
    )
    response = request.execute()
    print(response)


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
