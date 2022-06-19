import os
import pickle
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors


scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
client_secrets_file = "client_secret.json"
api_service_name = "youtube"
api_version = "v3"
developer_key = "AIzaSyCQ7pxDuHY2_bymJf0ZbqUFXIFQ36TLYdo"


def get_subscriptions():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    youtube = get_authenticated_service()
    request = youtube.channels().list(
        part="contentDetails",
        mine=True
    )
    response = request.execute()
    print(response)


def get_authenticated_service():
    if os.path.exists("CREDENTIALS_PICKLE_FILE"):
        with open("CREDENTIALS_PICKLE_FILE", 'rb') as f:
            credentials = pickle.load(f)
    else:
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
        credentials = flow.run_console()
        with open("CREDENTIALS_PICKLE_FILE", 'wb') as f:
            pickle.dump(credentials, f)
    return googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)
