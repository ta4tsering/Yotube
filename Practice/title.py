from requests_html import HTMLSession
from bs4 import BeautifulSoup as bs

session = HTMLSession()

def get_title_of_video(url):
    response = session.get(url)

    response.html.render(sleep = 1)

    soup = bs(response.html.html, "html.parser")

    video_meta = {}

    video_meta['title'] = soup.find("h1").text.strip()

    print(video_meta)

if __name__ =="__main__":
    get_title_of_video("https://www.youtube.com/watch?v=KS3o-IcnPHM&")
