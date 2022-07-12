client_access_token = 'DMVaKYEmgvp1tTOz2foDNmkJF2I90b3pKSxmxIhO7uY_5i1XxIAOCThL2m6nN2R0'
client_id = '--i-Idk6cQUxxdTPjrIX6jPId11b2IzIz38Zp6GfhkxPy-OsdJLHwruAK7p-DmAg'

import pandas as pd
from requests.exceptions import HTTPError, Timeout
import requests
import csv
from tqdm import tqdm
from bs4 import BeautifulSoup
from lyricsgenius import Genius
import pickle

base_url = "http://api.genius.com"
headers = {'Authorization': 'Bearer  ' + client_access_token}
genius = Genius(client_access_token)

artist_id = None
song_title = None
artist_name = None


def getLyrics(song_id):
    retries = 0
    while retries < 3:
        try:
            lyrics = genius.lyrics(song_id, remove_section_headers=True)
            break
        except Timeout as e:
            retries += 1
            continue

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

#todo: refactor get function for artist search
def _get(path, params=None, headers=None):

    # generate request URL
    requrl = '/'.join([base_url, path])
    token = "Bearer {}".format(client_access_token)
    if headers:
        headers['Authorization'] = token
    else:
        headers = {"Authorization": token}

    response = requests.get(url=requrl, params=params, headers=headers)
    response.raise_for_status()

    return response.json()

#todo: refactor this function
def get_artist_songs(artist_id):
    # initialize variables & a list.
    current_page = 1
    next_page = True
    songs = []
    #count = 0

    # main loop
    while next_page:
        print("getting songs")

        path = "artists/{}/songs/".format(artist_id)
        params = {'page': current_page}
        data = _get(path=path, params=params)

        page_songs = data['response']['songs']

        if page_songs:
            # add all the songs of current page,
            # and increment current_page value for next loop.
            songs += page_songs
            current_page += 1
        else:
            # if page_songs is empty, quit.
            next_page = False



    # get all the song ids, excluding not-primary-artist songs.
    songs = [song["id"] for song in songs
             if song["primary_artist"]["id"] == artist_id]
    #urls = [song["url"] for song in songs
            #if song["primary_artist"]["id"]==artist_id]
    print("got all songs")
    with open('song_ids.pkl', 'wb') as f:
        pickle.dump(songs, f)
    print('dumped all song ids in pickle file')
    return songs

#todo: refactor getting artist id
def get_artistId(artistName):
    find_id = _get("search", {'q': artistName})
    for hit in find_id["response"]["hits"]:
        if hit["result"]["primary_artist"]["name"] == artistName:
            artist_id = hit["result"]["primary_artist"]["id"]
            break
    print("got artist id")
    return artist_id


def get_allLyrics():
    songs_file = open('song_ids.pkl', 'rb')
    songs = pickle.load(songs_file)

    # artist_name = input("Enter artist name ")
    # artist_id = get_artistId(artist_name)
    # #songs = get_artist_songs(artist_id)
    all_lyrics = []
    csv_details = ["song_id", "lyrics"]

    with open("idiotlyrics.csv", "w+") as f:
        write = csv.writer(f)
        write.writerow(csv_details)
        for song_id in tqdm(songs):
            lyrics = getLyrics(song_id)
            all_lyrics.append(lyrics)
            row = [song_id, lyrics]
            write.writerow(row)

    lyric_data = list(zip(songs, all_lyrics))
    return lyric_data


lyr = get_allLyrics()