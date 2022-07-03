from functions.get_videos import get_videos
from functions.get_subscriptions import get_subscriptions

import csv
import os


def main():
    channels = []
    file = open(os.path.join("data", "my_channels.csv"), "r", newline="")
    content = csv.DictReader(file)
    for row in content:
        channels.append(row)
    file.close()

    for channel in channels:
        if not os.path.exists(os.path.join("data", channel["Channel name"])):
            os.mkdir(os.path.join("data", channel["Channel name"]))

    get_subscriptions("FOOT BALL")


if __name__ == "__main__":
    main()
