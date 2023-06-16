from flask import Flask, render_template
import spotipy
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)


client_id = "e0708753ab60499c89ce263de9b4f57a"
client_secret = "80c927166c664ee98a43a2c0e2981b4a"
redirect_uri = "https://fuccsoc.com/"

scope = (
    "user-read-playback-state playlist-read-private playlist-read-collaborative"
    " app-remote-control user-modify-playback-state user-library-modify"
    " user-library-read"
)
auth_manager = SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope=scope,
)

sp = spotipy.Spotify(auth_manager=auth_manager)

@app.route("/")
def now_playing():
    current_track = sp.current_user_playing_track()

    if current_track is None:
        return render_template("index.html")

    track_name = current_track["item"]["name"]
    artists = ", ".join([artist["name"] for artist in current_track["item"]["artists"]])
    album = current_track["item"]["album"]["name"]
    duration_ms = current_track["item"]["duration_ms"]
    release_date = current_track["item"]["album"]["release_date"]
    image_url = current_track["item"]["album"]["images"][0]["url"]

    return render_template(
        "index.html",
        track_name=track_name,
        artists=artists,
        album=album,
        duration_ms=duration_ms,
        release_date=release_date,
        image_url=image_url,
    )


if __name__ == "__main__":
    app.run(port=1929)
