from pytube import extract
import pandas as pd
from pathlib import Path

url_list = []
video_id = []
if __name__=="__main__":
    urls = Path(f'./links.txt').read_text(encoding='utf-8')
    url_list += urls.split("\n")
    for url in url_list:
        id = extract.video_id(url)
        video_id.append(id)
    print(video_id)
    print(len(video_id))