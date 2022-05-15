import sys
import random
import pprint
import spotipy
import spotipy.util as util

sys.path.append('./secrets')
import SpotifySecrets

CLIENT_ID = SpotifySecrets.SPOTIFY_CLIENT_ID
CLIENT_SECRET = SpotifySecrets.SPOTIFY_CLIENT_SECRET
AUTH_URL = 'https://accounts.spotify.com/api/token'
BASE_URL = 'https://api.spotify.com/v1/'
REDIRECT_URL = 'http://localhost:5500'
USER_TOKEN = None
SPOTIFY: spotipy.Spotify
USER_ID = None

SCOPE = 'user-library-read user-library-modify playlist-read-collaborative playlist-modify-public playlist-read-private playlist-modify-private'

def auth():
    return util.prompt_for_user_token(scope=SCOPE,client_id=CLIENT_ID,client_secret=CLIENT_SECRET,redirect_uri=REDIRECT_URL)

def get_users_liked_tracks(spotify: spotipy.Spotify):
    results = []
    i = 0
    lastPage = False
    while not lastPage:
        nextPage = spotify.current_user_saved_tracks(limit=50, offset=i*50)
        results += nextPage['items']
        i += 1
        if nextPage['next'] == None:
            lastPage = True

    return results

def main():
    USER_TOKEN = auth()
    if USER_TOKEN:
        SPOTIFY = spotipy.Spotify(auth=USER_TOKEN)
        USER_ID = SPOTIFY.me()['id']

        tracks = get_users_liked_tracks(SPOTIFY)
        random.shuffle(tracks)

        pprint.pprint(f"Name: {tracks[0]['track']['name']} | Artist: {tracks[0]['track']['artists'][0]['name']}")
        pprint.pprint(f"Name: {tracks[1]['track']['name']} | Artist: {tracks[1]['track']['artists'][0]['name']}")

if __name__ == '__main__':
    main()