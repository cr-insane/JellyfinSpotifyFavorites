import requests

class SpotifyAPI:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.headers = None
        try:
            data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
            response = requests.post("https://accounts.spotify.com/api/token", data)
            response.raise_for_status()
            data = response.json()
            self.headers = {"Authorization": f"Bearer {data["access_token"]}"}
            print("Authenticated!")
        except requests.exceptions.RequestException as e:
            print(f"Error during request: {e}")


    def fetch_all_tracks(self, playlist_id):
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        all_tracks = []

        try:
            print("Fetching Tracks from Spotify")
            while url:
                response = requests.get(url, headers=self.headers)
                response.raise_for_status()
                data = response.json()

                # Extract song name and artist(s)
                tracks = [
                    (
                        item["track"]["name"],
                        ", ".join(artist["name"] for artist in item["track"]["artists"])  # Combine artist names
                    )
                    for item in data["items"]
                    if "track" in item and "name" in item["track"] and "artists" in item["track"]
                ]

                all_tracks.extend(tracks)
                url = data.get("next")
            return all_tracks

        except requests.exceptions.RequestException as e:
            print(f"Error during request: {e}")
            return []
