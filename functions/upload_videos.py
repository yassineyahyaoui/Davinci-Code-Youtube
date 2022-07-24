#    To test this code, you must run it locally using your own API credentials.
#    See: https://developers.google.com/explorer-help/code-samples#python
# 2. This example makes a simple upload request. We recommend that you consider
#    using resumable uploads instead, particularly if you are transferring large
#    files or there's a high likelihood of a network interruption or other
#    transmission failure. To learn more about resumable uploads, see:
#    https://developers.google.com/api-client-library/python/guide/media_upload

import os
import pickle
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from googleapiclient.http import MediaFileUpload

scopes = ["https://www.googleapis.com/auth/youtube.readonly", "https://www.googleapis.com/auth/youtube.upload"]
api_service_name = "youtube"
api_version = "v3"
developer_key = "AIzaSyCQ7pxDuHY2_bymJf0ZbqUFXIFQ36TLYdo"
client_secrets_file = "client_secret.json"


def upload_videos(targeted_channel):
    youtube = get_authenticated_service(targeted_channel)

    request = youtube.videos().insert(
        part="snippet",
        body={
            "snippet": {
                "title": "test video"
            }
        },

        # TODO: For this request to work, you must replace "YOUR_FILE"
        #       with a pointer to the actual file you are uploading.
        media_body=MediaFileUpload("C:/Users/DELL/PycharmProjects/Davinci-Code-Youtube/data/FOOT BALL/videos/HjK3sYyYu2w/messi.mp4")
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