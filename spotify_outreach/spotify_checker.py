"""
spotify_checker.py
------------------
Checks moodmixformat's Spotify discography for new releases (singles + EPs + albums).
Uses the Spotipy library to talk to the Spotify Web API.

How it works:
  1. Fetches ALL albums/singles/eps from the artist's discography
  2. Compares against the Supabase 'seen_releases' table (not a local file)
  3. Returns any brand-new releases it hasn't seen before
  4. Saves newly seen releases to Supabase so they won't be flagged again next Friday
"""

import os
import logging

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from supabase_client import get_supabase

# --------------------------------------------------------------------------
# Config
# --------------------------------------------------------------------------

# Your Spotify artist ID (extracted from the URL you provided)
ARTIST_ID = "3u85DFNq3xQgj3TMQL0ACi"
ARTIST_NAME = "moodmixformat"

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
    Reads from the Supabase 'seen_releases' table.
    Returns an empty set if nothing has been saved yet.
    """
    supabase = get_supabase()
    # Fetch just the release_id column from every row in the table
    response = supabase.table("seen_releases").select("release_id").execute()
    return {row["release_id"] for row in response.data}


def _save_seen_releases(new_releases: list[dict]) -> None:
    """
    Save newly seen releases to the Supabase 'seen_releases' table.
    Uses upsert so re-running the agent never creates duplicate rows.

    Each row stores: release_id, release_name, release_type, release_date, spotify_url
    """
    if not new_releases:
        return

    supabase = get_supabase()

    # Build the rows to insert — one per new release
    rows = [
        {
            "release_id":   release["id"],
            "release_name": release["name"],
            "release_type": release["type"],
            "release_date": release["release_date"],
            "spotify_url":  release["spotify_url"],
        }
        for release in new_releases
    ]

    # upsert: insert new rows, and if release_id already exists just update it
    supabase.table("seen_releases").upsert(rows).execute()
    logger.info("Saved %d new release(s) to Supabase seen_releases table", len(rows))


def _fetch_all_releases(sp: spotipy.Spotify) -> list[dict]:
    """
    Fetch every release from the artist's discography, including:
      - 'album'  (full-length LPs)
      - 'single' (singles and EPs live here in the Spotify API)

    Spotify's API paginates results, so we loop through all pages.
    """
    all_releases = []

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
    logger.info("Loaded %d already-seen release IDs from Supabase", len(seen_ids))

    # Fetch full discography from Spotify
    all_releases = _fetch_all_releases(sp)
    logger.info("Found %d total releases in discography", len(all_releases))

    new_releases = []

    for release in all_releases:
        release_id = release["id"]

        if release_id in seen_ids:
            # Already processed this one before — skip
            continue

        # This is a new release we haven't seen yet!
        new_release = {
            "id":           release_id,
            "name":         release["name"],
            "type":         release["album_type"],  # 'album', 'single', or 'compilation'
            "release_date": release.get("release_date", "unknown"),
            "spotify_url":  release["external_urls"]["spotify"],
            "spotify_uri":  release["uri"],
            "total_tracks": release.get("total_tracks", 1),
            "images":       release.get("images", []),
        }
        new_releases.append(new_release)
        logger.info("New release found: %s (%s)", new_release["name"], new_release["type"])

    # Save the new releases to Supabase so we don't flag them again next week
    _save_seen_releases(new_releases)

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


def release_from_url(spotify_url: str, release_name: str, release_type: str = "single", release_date: str = None) -> dict:
    """
    Build a release dict directly from a Spotify URL — no API key needed.
    Use this when you want to provide a song link manually instead of
    letting the agent auto-detect new releases from the discography.

    Args:
      spotify_url:   The full Spotify link, e.g. https://open.spotify.com/track/abc123
      release_name:  The name of the song or album, e.g. "Drift"
      release_type:  'single', 'album', or 'ep' (default: 'single')
      release_date:  Date string e.g. '2026-03-20' (default: today)
    """
    from datetime import date as _date

    # Extract the ID from the URL (the part after /track/ or /album/)
    # e.g. https://open.spotify.com/track/3NMZENmh8Ji1Qb1XjFNaH7 → 3NMZENmh8Ji1Qb1XjFNaH7
    parts = spotify_url.rstrip("/").split("/")
    release_id = parts[-1].split("?")[0]  # strip any ?si=... query params

    if not release_date:
        release_date = str(_date.today())

    return {
        "id":           release_id,
        "name":         release_name,
        "type":         release_type,
        "release_date": release_date,
        "spotify_url":  spotify_url,
        "spotify_uri":  f"spotify:track:{release_id}",
        "total_tracks": 1,
        "images":       [],
    }
