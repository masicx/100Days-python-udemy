import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
from bs4 import BeautifulSoup

date_to_travel = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
response = requests.get(f"https://www.billboard.com/charts/hot-100/{date_to_travel}/")
soup = BeautifulSoup(response.text, "html.parser")
song_names_spans = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_names_spans]

artists_spans = soup.select("li ul li h3 + span")
artists = [artist.getText().strip() for artist in artists_spans]

song_and_artist = {song: artist for song, artist in zip(song_names, artists)}

load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

spotify = spotipy.Spotify( auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="https://example.com",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path=r"C:\Code\100DaysCourse\46. Spotify playlist\token.txt"
    ))

# playlist = spotify.user_playlist_create(user=spotify.current_user()["id"], name=f"{date_to_travel} Billboard 100", public=False)
playlists = spotify.current_user_playlists()
print(playlists)

