from googleapiclient.discovery import build
from urllib.parse import parse_qs, urlparse

api_key = 'AIzaSyDXNgeVWIp0iCUa7MV-Lrjxu_KPMo0bGzI'

#extract playlist id from url
url = 'https://www.youtube.com/playlist?list=PLuBNaT1tolOBFqkwFASWHPjww_T8d7ooz'
query = parse_qs(urlparse(url).query, keep_blank_values=True)
playlist_id = query["list"][0]


print(f'get all playlist items links from {playlist_id}')
youtube = build('youtube', 'v3', developerKey=api_key)

request = youtube.playlistItems().list(
    part = "snippet",
    playlistId = playlist_id,
    maxResults = 50
)
response = request.execute()

playlist_items = []
while request is not None:
    response = request.execute()
    playlist_items += response["items"]
    request = youtube.playlistItems().list_next(request, response)

print(f"total: {len(playlist_items)}")
for t in playlist_items:
    print([ 
        f'https://www.youtube.com/watch?v={t["snippet"]["resourceId"]["videoId"]}&list={playlist_id}&t=0s'
        
    ])