import requests
import json

class JellyfinAPI:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.headers = {"Authorization": f'Mediabrowser Token="{api_key}"'}

    def find_track_id(self, track, artist):
        # Example method to interact with Jellyfin
        # Modify as per your Jellyfin API needs
        url = f"{self.base_url}/Search/Hints?searchTerm={track}&mediaTypes=Audio&includeItemTypes=Audio"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()["SearchHints"]
            output_dict = [x for x in data if x.get("AlbumArtist", []) in artist]
            #print(f"output dict: {output_dict}")
            count = len(output_dict)
            if count > 1:
                #print("Multiple possible Tracks found. Skipping")
                return None
            if count == 1:
                item_id = response.json()["SearchHints"][0]["ItemId"]
                return item_id

        except requests.exceptions.RequestException as e:
            #print(f"Error during Jellyfin API request: {e}")
            return None

    def set_track_id_favorite(self, track_id, user_id):
        url = f"{self.base_url}/UserFavoriteItems/{track_id}?userId={user_id}"
        try:
            response = requests.post(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            #print(data)
        except requests.exceptions.RequestException as e:
            print(f"Error while favoring item: {e}")
            return None
