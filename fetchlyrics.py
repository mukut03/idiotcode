client_access_token = 'DMVaKYEmgvp1tTOz2foDNmkJF2I90b3pKSxmxIhO7uY_5i1XxIAOCThL2m6nN2R0'
client_id = '--i-Idk6cQUxxdTPjrIX6jPId11b2IzIz38Zp6GfhkxPy-OsdJLHwruAK7p-DmAg'

import requests
from bs4 import BeautifulSoup
from lyricsgenius import Genius

base_url = "http://api.genius.com"
headers = {'Authorization': 'Bearer  ' + client_access_token}
genius = Genius(client_access_token)



song_title = "Echoes"
artist_name = "Pink Floyd"


def getLyrics(song_id):
    lyrics = genius.lyrics(song_id)
    return lyrics


def search_song():
    genius_search_url = f"http://api.genius.com/search?q={song_title}&access_token={client_access_token}"
    response = requests.get(genius_search_url)
    json = response.json()
    song_info = None

    for hit in json["response"]["hits"]:
        if hit["result"]["primary_artist"]["name"] == artist_name:
            song_info = hit
            break
    if song_info:
        song_id = song_info["result"]["id"]
        print(getLyrics(song_id))




search_song()
