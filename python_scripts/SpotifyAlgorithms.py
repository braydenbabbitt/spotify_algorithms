import sys
import random
import pprint
from unittest import skip
import spotipy
import spotipy.util as util
from urllib.parse import urlparse
from urllib.parse import parse_qs

sys.path.append('./secrets')
import SpotifySecrets

CLIENT_ID = SpotifySecrets.SPOTIFY_CLIENT_ID
CLIENT_SECRET = SpotifySecrets.SPOTIFY_CLIENT_SECRET
BASE_URL = 'https://api.spotify.com/v1/'
REDIRECT_URL = 'http://localhost:5500'
USER_TOKEN = None
SPOTIFY: spotipy.Spotify
USER_ID = None

SCOPE = 'user-library-read user-library-modify playlist-read-collaborative playlist-modify-public playlist-read-private playlist-modify-private user-read-recently-played'

def auth():
    return util.prompt_for_user_token(scope=SCOPE,client_id=CLIENT_ID,client_secret=CLIENT_SECRET,redirect_uri=REDIRECT_URL)

def get_users_liked_tracks(spotify: spotipy.Spotify):
    page = spotify.current_user_saved_tracks(limit=50)
    results = page['items']
    lastPage = False
    while not lastPage:
        page = spotify.next(page)
        results += page['items']
        if page['next'] == None:
            lastPage = True

    return results

def get_all_track_ids_from_playlist(spotify: spotipy.Spotify, playlist_id):
    page = spotify.playlist_tracks(playlist_id=playlist_id)
    results = page['items']
    if not page['next'] == None:
        lastPage = False
        while not lastPage:
            page = spotify.next(page)
            results += page['items']
            if page['next'] == None:
                lastPage = True

    return [sub['track']['id'] for sub in results]

def get_users_recent_tracks(spotify: spotipy.Spotify):
    results = []
    i = 0
    lastPage = False
    while not lastPage:
        nextPage = spotify.current_user_recently_played()
        results += nextPage['items']
        i += 1
        if nextPage['next'] == None:
            lastPage = True
        
    results = spotify.current_user_recently_played(limit=10)['items']

    return results

def write_tracks_to_playlist(tracks, spotify: spotipy.Spotify, playlist_id, overwrite = True, skip_duplicates = True):
    if skip_duplicates:
        current_track_ids = get_all_track_ids_from_playlist(spotify=spotify, playlist_id=playlist_id)
        new_tracks = []
        for id in tracks:
            if not id in current_track_ids:
                new_tracks.append(id)
        tracks = new_tracks

    if overwrite:
        spotify.playlist_replace_items(playlist_id=playlist_id, items=tracks)
    else:
        spotify.playlist_add_items(playlist_id=playlist_id, items=tracks)
    return True

def get_parameter_from_url(url, key):
    return parse_qs(urlparse(url).query)[key][0]

def main():
    USER_TOKEN = auth()
    if USER_TOKEN:
        SPOTIFY = spotipy.Spotify(auth=USER_TOKEN)
        USER_ID = SPOTIFY.me()['id']

        # Personal save Daily Random and write a new one
        import BraydenCustomFunctions
        BraydenCustomFunctions.save_daily_random_and_write(spotify=SPOTIFY)

if __name__ == '__main__':
    main()