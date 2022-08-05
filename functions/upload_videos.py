import os
import csv
import pickle
import pandas
from datetime import date, timedelta
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload


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

    set_thumbnail(targeted_channel, response["id"], video_id)

    check_uploaded_videos_file(targeted_channel)
    update_uploaded_videos_file(targeted_channel, video_id)
    sort_uploaded_videos_by_rating(targeted_channel)
    update_downloaded_videos_file(targeted_channel, video_id)


def set_thumbnail(targeted_channel, targeted_video_id, video_id):
    youtube = get_authenticated_service(targeted_channel)

    request = youtube.thumbnails().set(
        videoId=targeted_video_id,
        media_body=MediaFileUpload(os.getcwd() + "/data/FOOT BALL/videos/" + video_id + "/thumbnail.png")
    )
    response = request.execute()
    print(response)


def check_uploaded_videos_file(targeted_channel):
    if not os.path.exists(os.path.join("data", targeted_channel, "uploaded_videos.csv")):
        file_uploaded_videos = open(os.path.join("data", targeted_channel, "uploaded_videos.csv"), "w", newline="")
        file_uploaded_videos.close()

    file_uploaded_videos = open(os.path.join("data", targeted_channel, "uploaded_videos.csv"), "r", newline="")
    content = file_uploaded_videos.read()
    file_uploaded_videos.close()

    if ("Channel name" or "Video id" or "Video title" or "Video description" or "Video thumbnail" or "Video rating" or "Video view count" or "Video like count" or "Video comment count" or "Video license" or "Video duration" or "Video publish time") not in content:
        file_uploaded_videos = open(os.path.join("data", targeted_channel, "uploaded_videos.csv"), "w", newline="")
        row = ("Channel name", "Video id", "Video title", "Video description", "Video thumbnail", "Video category", "Video rating", "Video view count", "Video like count", "Video comment count", "Video license", "Video duration", "Video publish time")
        csv.writer(file_uploaded_videos).writerow(row)
        file_uploaded_videos.close()


def update_uploaded_videos_file(targeted_channel, video_id):
    downloaded_videos_list = []
    file_downloaded_videos = open(os.path.join("data", targeted_channel, "downloaded_videos.csv"), "r", newline="")
    content = csv.DictReader(file_downloaded_videos)
    for video in content:
        downloaded_videos_list.append(video)
    file_downloaded_videos.close()

    for video in downloaded_videos_list:
        if video["Video id"] == video_id:
            file_uploaded_videos = open(os.path.join("data", targeted_channel, "uploaded_videos.csv"), "a", newline="")
            row = (video["Channel name"], video["Video id"], video["Video title"], video["Video description"], video["Video thumbnail"], video["Video category"],
                   video["Video rating"], video["Video view count"], video["Video like count"],
                   video["Video comment count"], video["Video license"], video["Video duration"],
                   video["Video publish time"])
            csv.writer(file_uploaded_videos).writerow(row)
            file_uploaded_videos.close()


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


def sort_uploaded_videos_by_rating(targeted_channel):
    data = pandas.read_csv(os.path.join("data", targeted_channel, "uploaded_videos.csv"))
    data.sort_values(["Video rating"], axis=0, ascending=[False], inplace=True)

    downloaded_videos_list = []
    file_uploaded_videos = open(os.path.join("data", targeted_channel, "uploaded_videos.csv"), "r", newline="")
    content = csv.DictReader(file_uploaded_videos)
    for row in content:
        downloaded_videos_list.append(row)
    file_uploaded_videos.close()

    file_uploaded_videos = open(os.path.join("data", targeted_channel, "uploaded_videos.csv"), "w", newline="")
    row = ("Channel name", "Video id", "Video title", "Video description", "Video thumbnail", "Video category", "Video rating", "Video view count",
           "Video like count", "Video comment count", "Video license", "Video duration", "Video publish time")
    csv.writer(file_uploaded_videos).writerow(row)
    for index, item in data.iterrows():
        for video in downloaded_videos_list:
            if item["Video id"] == video["Video id"]:
                row = (video["Channel name"], video["Video id"], video["Video title"], video["Video description"], video["Video thumbnail"], video["Video category"], video["Video rating"], video["Video view count"], video["Video like count"], video["Video comment count"], video["Video license"], video["Video duration"], video["Video publish time"])
                csv.writer(file_uploaded_videos).writerow(row)
    file_uploaded_videos.close()


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
