"""
Spotify Track Email Agent
-------------------------
Takes a Spotify track link, fetches track info using the Spotify API,
and uses Claude to generate a promotional email for the song.

Setup required:
  - ANTHROPIC_API_KEY: Your Anthropic API key
  - SPOTIFY_CLIENT_ID: From https://developer.spotify.com/dashboard
  - SPOTIFY_CLIENT_SECRET: From https://developer.spotify.com/dashboard

All agent actions are logged to agent_actions.log for audit trail.
"""

import sys
import re
import logging
import os
import json
from datetime import datetime
import urllib.request
import urllib.parse
import urllib.error
import base64
import anthropic

# Audit log — required by project conventions
logging.basicConfig(
    filename="agent_actions.log",
    level=logging.INFO,
    format="%(asctime)s [AGENT] %(message)s"
)


def get_spotify_token(client_id: str, client_secret: str) -> str:
    """Get a Spotify API access token using client credentials flow."""
    credentials = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    data = urllib.parse.urlencode({"grant_type": "client_credentials"}).encode()
    req = urllib.request.Request(
        "https://accounts.spotify.com/api/token",
        data=data,
        headers={
            "Authorization": f"Basic {credentials}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
    )
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())
    return result["access_token"]


def get_track_info(track_id: str, token: str) -> dict:
    """Fetch track metadata from the Spotify API."""
    req = urllib.request.Request(
        f"https://api.spotify.com/v1/tracks/{track_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def extract_track_id(spotify_url: str) -> str:
    """Pull the track ID out of a Spotify URL."""
    # Handles: open.spotify.com/track/TRACK_ID or spotify:track:TRACK_ID
    match = re.search(r"track[/:]([A-Za-z0-9]+)", spotify_url)
    if not match:
        raise ValueError(f"Could not extract track ID from URL: {spotify_url}")
    return match.group(1)


def generate_promo_email(track: dict, api_key: str) -> str:
    """
    Use Claude to write a promotional email for the given track.
    Returns the email text.
    """
    client = anthropic.Anthropic(api_key=api_key)

    # Build a short summary of the track for Claude to work with
    artists = ", ".join(a["name"] for a in track["artists"])
    album = track["album"]["name"]
    release_date = track["album"]["release_date"]
    duration_sec = track["duration_ms"] // 1000
    duration_fmt = f"{duration_sec // 60}:{duration_sec % 60:02d}"

    track_summary = (
        f"Song: {track['name']}\n"
        f"Artist(s): {artists}\n"
        f"Album: {album}\n"
        f"Released: {release_date}\n"
        f"Duration: {duration_fmt}\n"
        f"Spotify URL: https://open.spotify.com/track/{track['id']}"
    )

    logging.info(f"Generating promo email for: {track['name']} by {artists}")

    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        system=(
            "You are a music promotion copywriter. Write enthusiastic, "
            "concise promotional emails for songs. Always include:\n"
            "- A compelling subject line\n"
            "- A short email body (3-4 paragraphs)\n"
            "- A clear call to action with the Spotify link\n"
            "Keep it friendly and suitable for a music newsletter."
        ),
        messages=[
            {
                "role": "user",
                "content": (
                    f"Write a promotional email for this track:\n\n{track_summary}"
                )
            }
        ]
    )

    return response.content[0].text


def run_spotify_agent(spotify_url: str):
    """Main agent entry point."""
    logging.info(f"Agent started. URL: {spotify_url}")
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Spotify Email Agent starting...")
    print(f"Track URL: {spotify_url}\n")

    # Load credentials from environment — never hardcoded
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
    spotify_id = os.environ.get("SPOTIFY_CLIENT_ID")
    spotify_secret = os.environ.get("SPOTIFY_CLIENT_SECRET")

    missing = []
    if not anthropic_key:
        missing.append("ANTHROPIC_API_KEY")
    if not spotify_id:
        missing.append("SPOTIFY_CLIENT_ID")
    if not spotify_secret:
        missing.append("SPOTIFY_CLIENT_SECRET")

    if missing:
        print(f"ERROR: Missing required environment variables: {', '.join(missing)}")
        print("\nSetup instructions:")
        print("  export ANTHROPIC_API_KEY=your_key")
        print("  export SPOTIFY_CLIENT_ID=your_client_id    # from developer.spotify.com/dashboard")
        print("  export SPOTIFY_CLIENT_SECRET=your_secret")
        logging.error(f"Missing env vars: {missing}")
        sys.exit(1)

    # Step 1: Extract track ID from URL
    try:
        track_id = extract_track_id(spotify_url)
        print(f"Track ID: {track_id}")
        logging.info(f"Extracted track ID: {track_id}")
    except ValueError as e:
        print(f"ERROR: {e}")
        logging.error(str(e))
        sys.exit(1)

    # Step 2: Authenticate with Spotify and fetch track info
    print("Fetching track info from Spotify API...")
    try:
        token = get_spotify_token(spotify_id, spotify_secret)
        track = get_track_info(track_id, token)
        artists = ", ".join(a["name"] for a in track["artists"])
        print(f"Found: \"{track['name']}\" by {artists}")
        logging.info(f"Track fetched: {track['name']} by {artists}")
    except Exception as e:
        print(f"ERROR fetching from Spotify: {e}")
        logging.error(f"Spotify API error: {e}")
        sys.exit(1)

    # Step 3: Generate promotional email with Claude
    print("\nGenerating promotional email with Claude...\n")
    print("=" * 60)
    try:
        email = generate_promo_email(track, anthropic_key)
        print(email)
    except Exception as e:
        print(f"ERROR generating email: {e}")
        logging.error(f"Claude API error: {e}")
        sys.exit(1)

    print("=" * 60)
    logging.info("Agent completed successfully")
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Done. Actions logged to agent_actions.log")


if __name__ == "__main__":
    url = (
        sys.argv[1] if len(sys.argv) > 1
        else "https://open.spotify.com/track/3NMZENmh8Ji1Qb1XjFNaH7?si=iaYccm0WRFiVv5EcspSjQA"
    )
    run_spotify_agent(url)
