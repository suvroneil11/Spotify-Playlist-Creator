import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import pylast
from itertools import islice
import sys

#Get Artist and Track name from command line
artist_name = sys.argv[1]
track_name = sys.argv[2]

#Spotify Authentication:
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.environ.get('SPOTIFY_CLIENT_ID'),
                                              client_secret=os.environ.get('SPOTIFY_CLIENT_SECRET'),
                                              redirect_uri="http://example.com/",
                                              scope="playlist-modify-private",
                                               ))

user_id = sp.current_user()["id"]

#Last FM Authentication:
last = pylast.LastFMNetwork(api_key=os.environ.get('LFM_API_KEY'), api_secret=os.environ.get('LFM_API_SECRET'))

track = last.get_track(artist_name, track_name)
song_uri = []

#Ge the recommendations and Look for the recommended songs in spotify and get the URIs of each song
for key in islice(track.get_similar(), 30):
    song = key.item
    artist = str(song).split("-")[0]
    track_title = str(song).split("-")[1]
    searchResults = sp.search(q="artist:" + artist + " track:" + track_title, type="track")

    try:
        uri = searchResults['tracks']['items'][0]['uri']
        song_uri.append((uri))
    except IndexError:
        print(f"Please manually add this track to the playlist: {track_title} by {artist}")

#Create New Playlist
playlist = sp.user_playlist_create(user=user_id, name=f"Songs Similar to {track} ", public=False)

#Add to the Playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uri)

print(f"Playlist Created Successfully with {len(song_uri)} songs!")


