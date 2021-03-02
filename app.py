import re
from pandas import DataFrame
from pathlib import Path
from pytube import extract
from googleapiclient.discovery import build

api_key = 'AIzaSyDXNgeVWIp0iCUa7MV-Lrjxu_KPMo0bGzI'

youtube = build('youtube', 'v3', developerKey=api_key)

hours_pattern = re.compile(r'(\d+)H')
minutes_pattern = re.compile(r'(\d+)M')
seconds_pattern = re.compile(r'(\d+)S')

durations = []
url_list = []
titles = []

def get_durations(vid_id):
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
        if time:
            return time
        else:
            return 0

def get_titles(vid_id):
    title_request = youtube.videos().list(
        part="snippet",
        id= vid_id
    )
    title_response = title_request.execute()

    for item in title_response['items']:
        if item['snippet']['title']:
            title = item['snippet']['title']
            return title
        else:
            return "No Title"

if __name__=="__main__":
    urls = Path(f'./links.txt').read_text(encoding='utf-8')
    url_list += urls.split("\n")
    for url in url_list:
        id = extract.video_id(url)
        duration = get_durations(id)
        durations.append(duration)
        title = get_titles(id)
        titles.append(title)
    df = DataFrame({'Links':url_list,'Durations':durations, 'Titles':titles})
    df.to_excel('demo.xlsx',sheet_name='Esukhia Work', index=True)