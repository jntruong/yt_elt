import requests
import json
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")
API_KEY = os.getenv("API_KEY")
maxResults = 50

CHANNEL_HANDLE = "MrBeast"

def get_playlist_id():
    try:
        url = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        channel_id = data["items"][0]
        channel_playlist_id = channel_id["contentDetails"]["relatedPlaylists"]["uploads"]
        # print(channel_playlist_id)
        return channel_playlist_id
    except requests.exceptions.RequestException as e:
        raise e


def get_video_id(playlist_id):
    video_ids = []
    pageToken = None
    
    base_url =f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={50}&playlistId={playlist_id}&key={API_KEY}"
    try:
        while True:
            url = base_url
            if pageToken:
                url += f"&pageToken={pageToken}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            for item in data.get("items", []):
                video_id = item["contentDetails"]["videoId"]
                video_ids.append(video_id)
                
            pageToken = data.get("nextPageToken")
            if not pageToken:
                    break
        return video_ids
    except requests.exceptions.RequestException as e:
        raise e
    


def extract_video_data(video_ids):
    extracted_data =[]
    def batch_list(video_ids_list,batch_size):
        for video_id in range(0, len(video_ids_list), batch_size):
            yield video_ids_list[video_id: video_id + batch_size]
    
    try:
        for batch in batch_list(video_ids,maxResults):
            video_ids_str = ",".join(batch)
            
            url=f"https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=snippet&part=statistics&id={video_ids_str}&key={API_KEY}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            for item in data.get("items", []):
                video_id = item["id"]
                snippet = item["snippet"]
                contentDetails = item["contentDetails"]
                statistics = item["statistics"]
                
                video_data = {
                    "video_id": video_id,
                    "title": snippet["title"],
                    "published_at": snippet["publishedAt"],
                    "duration": contentDetails["duration"],
                    "view_count": statistics.get("viewCount", 0),
                    "like_count": statistics.get("likeCount", 0),
                    "commentCount": statistics.get("commentCount", 0)
                }
                extracted_data.append(video_data)
        return extracted_data
    
    except requests.exceptions.RequestException as e:
        raise e




if __name__ == "__main__":
    playlist_id = get_playlist_id()
    video_ids = get_video_id(playlist_id)
    extracted_data = extract_video_data(video_ids)
    print(json.dumps(extracted_data, indent=4))