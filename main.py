
import csv
import googleapiclient.discovery

def main():

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyCQ7pxDuHY2_bymJf0ZbqUFXIFQ36TLYdo"

    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=DEVELOPER_KEY)

    request = youtube.search().list(
        part="snippet,id",
        channelId="UCJvgF5uUL22U7i9tNlPvduA",
        order="date",
        maxResults=5
    )
    response = request.execute()

    print(response)

    #f = open("channels.csv", "a", newline="")

    #row = (response["items"][0]["id"], response["items"][0]["statistics"]["videoCount"])
    #writer = csv.writer(f)
    #writer.writerow(row)

    #f.close()





if __name__ == "__main__":
    main()
