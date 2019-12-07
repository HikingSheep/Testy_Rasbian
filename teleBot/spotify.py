# -*- coding: utf-8 -*-

import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

SPOTIPY_CLIENT_ID = '5732bebf2ed9470697dd2fb2e159daef'
SPOTIPY_CLIENT_SECRET = '36fe70e6d78940f79cd67f67c3d4e14c'


client_credentials_manager = SpotifyClientCredentials(SPOTIPY_CLIENT_ID,SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_playlist(keyword):
    playlist_list = sp.search(str(keyword), limit=10, offset=5, type='playlist', market='SG')['playlists']['items']
    
    for pl in playlist_list:
        if pl['public'] is None or pl['public'] == True:
            return pl['external_urls']['spotify']

def get_track(keyword):
    playlist_list = sp.search(keyword, limit=1, type='track')['items']
    
    return str(playlist_list)
