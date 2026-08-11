import requests
import json
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")
API_KEY = os.getenv("API_KEY")

CHANNEL_HANDLE = "MrBeasts"

def get_playlist_id():
    try:
        url = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        channel_id = data["items"][0]
        channel_playlist_id = channel_id["contentDetails"]["relatedPlaylists"]["uploads"]
        print(channel_playlist_id)
        return channel_playlist_id
    except requests.exceptions.RequestException as e:
        raise e

if __name__ == "__main__":
    print("video_stats.py is being run directly")
    get_playlist_id()
