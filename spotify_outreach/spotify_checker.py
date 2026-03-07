"""
spotify_checker.py
------------------
Checks moodmixformat's Spotify discography for new releases (singles + EPs + albums).
Uses the Spotipy library to talk to the Spotify Web API.

How it works:
  1. Fetches ALL albums/singles/eps from the artist's discography
  2. Compares against a local JSON "seen releases" cache
  3. Returns any brand-new releases it hasn't seen before
  4. Saves newly seen releases so they won't be flagged again next Friday
"""

import json
import os
import logging
from datetime import datetime, date
from pathlib import Path

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# --------------------------------------------------------------------------
# Config
# --------------------------------------------------------------------------

# Your Spotify artist ID (extracted from the URL you provided)
ARTIST_ID = "3u85DFNq3xQgj3TMQL0ACi"
ARTIST_NAME = "moodmixformat"

# Local file that stores release IDs we've already seen, so we don't re-pitch
SEEN_RELEASES_FILE = Path(__file__).parent / "data" / "seen_releases.json"

logger = logging.getLogger(__name__)


def _get_spotify_client() -> spotipy.Spotify:
    """
    Create and return an authenticated Spotify client.
    Reads SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET from environment variables.
    """
    client_credentials_manager = SpotifyClientCredentials(
        client_id=os.environ["SPOTIFY_CLIENT_ID"],
        client_secret=os.environ["SPOTIFY_CLIENT_SECRET"],
    )
    return spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def _load_seen_releases() -> set:
    """
    Load the set of Spotify release IDs we have already processed.
    Returns an empty set if the file doesn't exist yet.
    """
    if SEEN_RELEASES_FILE.exists():
        data = json.loads(SEEN_RELEASES_FILE.read_text())
        return set(data.get("seen_ids", []))
    return set()


def _save_seen_releases(seen_ids: set) -> None:
    """
    Save the updated set of seen release IDs back to disk so we don't
    re-process them on the next run.
    """
    SEEN_RELEASES_FILE.parent.mkdir(parents=True, exist_ok=True)
    SEEN_RELEASES_FILE.write_text(
        json.dumps({"seen_ids": list(seen_ids), "last_updated": str(date.today())}, indent=2)
    )


def _fetch_all_releases(sp: spotipy.Spotify) -> list[dict]:
    """
    Fetch every release from the artist's discography, including:
      - 'album'  (full-length LPs)
      - 'single' (singles and EPs live here in the Spotify API)
      - 'compilation' (just in case)

    Spotify's API paginates results, so we loop through all pages.
    """
    all_releases = []

    # album_type can be a comma-separated string: 'album,single,compilation'
    results = sp.artist_albums(
        ARTIST_ID,
        album_type="album,single",  # singles covers both singles AND EPs
        limit=50,
    )

    while results:
        all_releases.extend(results["items"])
        # If there's a next page, fetch it; otherwise stop
        if results["next"]:
            results = sp.next(results)
        else:
            break

    return all_releases


def check_for_new_releases() -> list[dict]:
    """
    Main function called every Friday by the scheduler.

    Returns a list of new release dicts, each containing:
      {
        "id": "spotify_release_id",
        "name": "Release Title",
        "type": "single" | "album",
        "release_date": "2024-03-15",
        "spotify_url": "https://open.spotify.com/album/...",
        "spotify_uri": "spotify:album:...",
        "total_tracks": 3,
        "images": [...],  # album art URLs
      }

    Returns an empty list if nothing new is found.
    """
    logger.info("Checking Spotify for new releases by %s...", ARTIST_NAME)

    sp = _get_spotify_client()
    seen_ids = _load_seen_releases()

    # Fetch full discography
    all_releases = _fetch_all_releases(sp)
    logger.info("Found %d total releases in discography", len(all_releases))

    new_releases = []
    updated_seen_ids = set(seen_ids)  # copy so we can add to it

    for release in all_releases:
        release_id = release["id"]

        if release_id in seen_ids:
            # Already processed this one before — skip
            continue

        # This is a new release we haven't seen yet!
        new_release = {
            "id": release_id,
            "name": release["name"],
            "type": release["album_type"],  # 'album', 'single', or 'compilation'
            "release_date": release.get("release_date", "unknown"),
            "spotify_url": release["external_urls"]["spotify"],
            "spotify_uri": release["uri"],
            "total_tracks": release.get("total_tracks", 1),
            "images": release.get("images", []),
        }
        new_releases.append(new_release)
        updated_seen_ids.add(release_id)
        logger.info("New release found: %s (%s)", new_release["name"], new_release["type"])

    # Save the updated seen list so we don't flag these again next week
    _save_seen_releases(updated_seen_ids)

    if not new_releases:
        logger.info("No new releases found for %s this week.", ARTIST_NAME)
    else:
        logger.info("Found %d new release(s)!", len(new_releases))

    return new_releases


def get_release_details(release_id: str) -> dict:
    """
    Fetch full details for a specific release by ID.
    Useful for getting track listing, label info, etc.
    """
    sp = _get_spotify_client()
    album = sp.album(release_id)
    return album
