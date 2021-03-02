import re
from pathlib import Path
from pytube import extract
from googleapiclient.discovery import build
from urllib.parse import parse_qs, urlparse
from pandas import DataFrame

api_key = 'AIzaSyDXNgeVWIp0iCUa7MV-Lrjxu_KPMo0bGzI'
youtube = build('youtube', 'v3', developerKey=api_key)

hours_pattern = re.compile(r'(\d+)H')
minutes_pattern = re.compile(r'(\d+)M')
seconds_pattern = re.compile(r'(\d+)S')

# url = 'https://www.youtube.com/playlist?list=PLuBNaT1tolOBFqkwFASWHPjww_T8d7ooz'
# query = parse_qs(urlparse(url).query, keep_blank_values=True)
# playlist_id = query["list"][0]

all_titles = []
durations = []
def get_durations_of_videos(vid_id):
    # nextPageToken = None
    # while True:
        # pl_request = youtube.playlistItems().list(
        #     part='contentDetails',
        #     playlistId=playlist_id,
        #     maxResults=50,
        #     pageToken=nextPageToken
        # )
        # pl_response = pl_request.execute()

        # vid_ids = []
        # for item in pl_response['items']:
        #     vid_ids.append(item['contentDetails']['videoId'])

    vid_request = youtube.videos().list(
        part="contentDetails",
        id= vid_id
    )

    vid_response = vid_request.execute()
    
    time = []
    for item in vid_response['items']:
        duration = item['contentDetails']['duration']

        hours = hours_pattern.search(duration)
        minutes = minutes_pattern.search(duration)
        seconds = seconds_pattern.search(duration)

        hours = int(hours.group(1)) if hours else 0
        minutes = int(minutes.group(1)) if minutes else 0
        seconds = int(seconds.group(1)) if seconds else 0

        time.append(f'{hours}:{minutes}:{seconds}')


    title_request = youtube.videos().list(
        part="snippet",
        id= vid_id
    )
    title_response = title_request.execute()
    
    for item in title_response['items']:
        title = item['snippet']['title']
    
    return time, title

           
# def get_links_of_videos():
#     request = youtube.playlistItems().list(
#     part = "snippet",
#     playlistId = playlist_id,
#     maxResults = 50
#     )
#     response = request.execute()
#     links = []
#     playlist_items = []
#     while request is not None:
#         response = request.execute()
#         playlist_items += response["items"]
#         request = youtube.playlistItems().list_next(request, response)

#     print(f"total: {len(playlist_items)}")
#     for t in playlist_items:
#         links += ([f'https://www.youtube.com/watch?v={t["snippet"]["resourceId"]["videoId"]}&list={playlist_id}&t=0s'])
    
#     return links

if __name__=="__main__":
    url_list = []
    urls = Path(f'./links.txt').read_text(encoding='utf-8')
    url_list += urls.split("\n")
    for url in url_list:
        id = extract.video_id(url)
        duration, title = get_durations_of_videos(id)
        durations += duration
        all_titles += title
        print(durations, all_titles)
        df = DataFrame({ 'Titles':all_titles[],'Durations':durations[]})
    df.to_excel('EsukhiaYouTubeVideoList.xlsx',sheet_name='Esukhia Work', index=True)
