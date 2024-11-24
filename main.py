from spotify_api import SpotifyAPI
from jellyfin_api import JellyfinAPI
from tqdm import tqdm  # Import tqdm for progress bar
from dotenv import dotenv_values
config = dotenv_values(".env")

def main():
    # Spotify API
    spotify = SpotifyAPI(config["SPOTIFY_CLIENT_ID"], config["SPOTIFY_SECRET"])
    tracks = spotify.fetch_all_tracks(config["SPOTIFY_PLAYLIST_ID"])
    print(f"Fetched {len(tracks)} tracks from Spotify.")
    # Jellyfin API
    jellyfin = JellyfinAPI(config["JELLYFIN_BASE_URL"], config["JELLYFIN_API_KEY"])
    # Initialize counters
    success_count = 0
    failure_count = 0
    failed_tracks = []  # List to store failed tracks with artist names

    # Progress bar with tqdm
    with tqdm(total=len(tracks), desc="Processing Tracks", unit="track", ncols=250) as pbar:
        for track in tracks:
            track_name = track[0]  # Track name
            artist_name = track[1]  # Artist name

            result = jellyfin.find_track_id(track_name, artist_name)
            if result:
                jellyfin.set_track_id_favorite(result, config["JELLYFIN_USER_ID"])
                success_count += 1
                status = "✅ Success"
            else:
                failure_count += 1
                failed_tracks.append((track_name, artist_name))  # Log failed tracks
                status = "❌ Failed"

            pbar.set_postfix(success=success_count, failed=failure_count, status=status)
            pbar.update(1)

    # Print failed tracks at the end
    if failed_tracks:
        print("\nFailed Tracks:")
        for track, artist in failed_tracks:
            print(f"Track: {track}, Artist: {artist}")
    else:
        print("No tracks failed.")
    print(f"\nProcessing complete: {success_count} succeeded, {failure_count} failed.")

if __name__ == "__main__":
    main()
