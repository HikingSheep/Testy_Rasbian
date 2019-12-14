# -*- coding: utf-8 -*-

import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials


client_credentials_manager = SpotifyClientCredentials(SPOTIPY_CLIENT_ID,SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_playlist(keyword):
    playlist_list = sp.search(str(keyword), limit=10, offset=0, type='playlist', market='SG')['playlists']['items']
    
    for pl in playlist_list:
        if pl['public'] is None or pl['public'] == True:
            return pl['external_urls']['spotify']

def get_track(keyword):
    track = sp.search(keyword, limit=5, offset=0, type='track', market='SG')['tracks']['items']

    for t in track:
         return t['external_urls']['spotify']
