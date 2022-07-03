import os
import csv
import pickle
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors


scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
api_service_name = "youtube"
api_version = "v3"
developer_key = "AIzaSyCQ7pxDuHY2_bymJf0ZbqUFXIFQ36TLYdo"
client_secrets_file = "client_secret.json"


def get_subscriptions(targeted_channel):
    youtube = get_authenticated_service(targeted_channel)

    request = youtube.subscriptions().list(
        part="snippet,contentDetails",
        mine=True
    )
    response = request.execute()

    file_channels = open(os.path.join("data", targeted_channel, "channels.csv"), "r", newline="")
    content = file_channels.read()
    file_channels.close()

    if ("Channel name" or "Channel id") not in content:
        file_channels = open(os.path.join("data", targeted_channel, "channels.csv"), "w", newline="")
        row = ("Channel name", "Channel id")
        csv.writer(file_channels).writerow(row)
        file_channels.close()

    for channel in response["items"]:
        file_channels = open(os.path.join("data", targeted_channel, "channels.csv"), "r", newline="")
        content = file_channels.read()

        if channel["snippet"]["resourceId"]["channelId"] not in content:
            file_channels = open(os.path.join("data", targeted_channel, "channels.csv"), "a", newline="")

            channel_name = channel["snippet"]["title"].encode("utf-8")
            channel_id = channel["snippet"]["resourceId"]["channelId"]

            row = (channel_name, channel_id)
            csv.writer(file_channels).writerow(row)
            file_channels.close()


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
