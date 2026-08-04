import pandas as pd
import requests
from tqdm import tqdm
import time

# Load your dataset
df = pd.read_csv("spotify_enhanced.csv")

cover_urls = []

for _, row in tqdm(df.iterrows(), total=len(df)):

    song = str(row["track_name"])
    artist = str(row["artists"])

    url = "https://itunes.apple.com/search"

    params = {
        "term": f"{song} {artist}",
        "entity": "song",
        "limit": 1
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        if data["resultCount"] > 0:
            artwork = data["results"][0]["artworkUrl100"]

            # Higher quality image
            artwork = artwork.replace("100x100", "600x600")

            cover_urls.append(artwork)

        else:
            cover_urls.append(None)

    except:
        cover_urls.append(None)

    time.sleep(0.1)

df["album_cover_url"] = cover_urls

df.to_csv(
    "spotify_enhanced_with_cover.csv",
    index=False
)

print("Done!")