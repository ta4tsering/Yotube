from requests_html import HTMLSession
from bs4 import BeautifulSoup as bs
from googleapiclient.discovery import build
from urllib.parse import parse_qs, urlparse

session = HTMLSession()

api_key = 'AIzaSyDXNgeVWIp0iCUa7MV-Lrjxu_KPMo0bGzI'

def get_links_and_title_of_videos():
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

    links = []
    titles = []
    playlist_items = []
    while request is not None:
        response = request.execute()
        playlist_items += response["items"]
        request = youtube.playlistItems().list_next(request, response)

    print(f"total: {len(playlist_items)}")
    for t in playlist_items:
        links += ([f'https://www.youtube.com/watch?v={t["snippet"]["resourceId"]["videoId"]}&list={playlist_id}&t=0s'])
        title = get_title_of_video(f'https://www.youtube.com/watch?v={t["snippet"]["resourceId"]["videoId"]}&list={playlist_id}&t=0s')
        titles += title
    return links, titles

def get_title_of_video(url):
    response = session.get(url)

    response.html.render(sleep = 1)

    soup = bs(response.html.html, "html.parser")

    video_meta = {}

    video_meta['title'] = soup.find("h1").text.strip()

    return(video_meta)

if __name__ == "__main__":
    links, titles = get_links_and_title_of_videos()
    print(links,titles)