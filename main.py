# -*- coding: utf-8 -*-

# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os
import json
import csv
import googleapiclient.discovery

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyCQ7pxDuHY2_bymJf0ZbqUFXIFQ36TLYdo"

    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey = DEVELOPER_KEY)

    request = youtube.channels().list(
        part="statistics",
        id="UCc3yC3OMNYw-DEME69MVt_Q"
    )
    response = request.execute()

    print(response)

    f = open("channels.csv", "a", newline="")

    row = (response["items"][0]["id"], response["items"][0]["statistics"]["videoCount"])
    writer = csv.writer(f)
    writer.writerow(row)

    f.close()





if __name__ == "__main__":
    main()


