#    To test this code, you must run it locally using your own API credentials.
#    See: https://developers.google.com/explorer-help/code-samples#python
# 2. This example makes a simple upload request. We recommend that you consider
#    using resumable uploads instead, particularly if you are transferring large
#    files or there's a high likelihood of a network interruption or other
#    transmission failure. To learn more about resumable uploads, see:
#    https://developers.google.com/api-client-library/python/guide/media_upload

import os
import csv
import pickle
import struct
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload


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

            request = youtube.videos().insert(
                part="snippet,status",
                body={
                    "snippet": {
                        "title": convert_to_bytes(video["Video title"]).decode(),
                        "description": convert_to_bytes(video["Video description"]).decode()
                    },
                    "status": {
                        "privacyStatus": "private",
                        "publishAt": "2022-08-01T10:31:31Z"
                    }
                },

                media_body=MediaFileUpload(os.getcwd() + "/data/FOOT BALL/videos/" + video_id + "/" + convert_to_bytes(video["Video title"]).decode() + ".mp4")
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


def convert_to_bytes(string):
    s = string[2:-1]
    outlist = []
    for cp in s:
        num = ord(cp)
        if num < 255:
            outlist.append(struct.pack('B', num))
        elif num < 65535:
            outlist.append(struct.pack('>H', num))
        else:
            b = (num & 0xFF0000) >> 16
            H = num & 0xFFFF
            outlist.append(struct.pack('>bH', b, H))
    return b''.join(outlist)
