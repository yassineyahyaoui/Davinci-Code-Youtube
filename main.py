from functions.get_videos import get_videos
from functions.get_subscriptions import get_subscriptions

import csv
import os


def main():
    channels = []
    channels2 = []
    file_my_channels = open(os.path.join("data", "my_channels.csv"), "r", newline="")
    content = csv.DictReader(file_my_channels)
    for row in content:
        channels.append(row)
    file_my_channels.close()

    for channel in channels:
        if not os.path.exists(os.path.join("data", channel["Channel name"])):
            os.mkdir(os.path.join("data", channel["Channel name"]))
        get_subscriptions(channel["Channel name"])

        file_videos = open(os.path.join("data", channel["Channel name"], "channels.csv"), "r", newline="")
        content = csv.DictReader(file_videos)
        for row in content:
            print(row)
            channels2.append(row)
            get_videos(channel["Channel name"], row["Channel id"], True)
        file_videos.close()


if __name__ == "__main__":
    main()