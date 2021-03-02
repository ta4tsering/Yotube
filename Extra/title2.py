import re
from googleapiclient.discovery import build
from pandas import DataFrame

api_key = 'AIzaSyDXNgeVWIp0iCUa7MV-Lrjxu_KPMo0bGzI'

youtube = build('youtube', 'v3', developerKey=api_key)

hours_pattern = re.compile(r'(\d+)H')
minutes_pattern = re.compile(r'(\d+)M')
seconds_pattern = re.compile(r'(\d+)S')

all_titles = []
durations = []
nextPageToken = None
while True:
    for item in pl_response['items']:
        vid_ids.append(item['contentDetails']['videoId'])

    vid_request = youtube.videos().list(
        part="contentDetails",
        id=','.join(vid_ids)
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

    print(len(time))
    durations += time

    title_request = youtube.videos().list(
        part="snippet",
        id=','.join(vid_ids)
    )

    title_response = title_request.execute()
    titles = []
    for item in title_response['items']:
        title = item['snippet']['title']
        titles.append(title)

    print(len(titles))
    all_titles += titles
    
    nextPageToken = pl_response.get('nextPageToken')

    if not nextPageToken:
        print(durations)
        print(all_titles)
        df = DataFrame({'Durations':durations, 'Titles':all_titles})
        df.to_excel('Sheet!title2.xlsx',sheet_name='Esukhia Work', index=True)
        break
    
