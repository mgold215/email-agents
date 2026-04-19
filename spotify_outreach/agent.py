"""
agent.py
--------
The main Outreach Agent for moodmixformat.

What this does every Friday:
  1. Gets the release — from CLI flags, env vars, or the Spotify API
  2. Generates a personalised pitch to every contact
  3. Sends (or simulates) the emails with rate limiting
  4. Logs everything for audit trail

How to run:
  - Manual (CLI):    python agent.py --run-now --spotify-url "https://..." --release-name "ABACUS"
  - Manual (env):    Set RELEASE_URL and RELEASE_NAME in .env, then python agent.py --run-now
  - Scheduled:       python agent.py  (runs every Friday at 9 AM)
  - Dry run:         Make sure OUTREACH_LIVE_MODE is NOT set to true

Scheduling options:
  - Built-in scheduler: just run `python agent.py` — it checks every Friday
  - Cron (recommended): `0 9 * * 5 cd /path/to/agent && python agent.py --run-now`
  - Railway: set RUN_NOW=true in Railway Variables to trigger a one-off run
"""

import argparse
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

import schedule
import time

# Add parent dir to path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent))

from supabase_client import get_supabase
from pitch_generator import generate_pitches_for_release
from email_sender import send_all_pitches

# ---------------------------------------------------------------------------
# Supabase-backed contact functions (replaces hardcoded contacts.py)
# ---------------------------------------------------------------------------

def get_active_contacts() -> list:
    """Load active contacts from Supabase, respecting cooldown periods.

    A contact is eligible if:
      - active = True
      - releases_since_last_pitch >= cooldown_releases (enough releases have passed)
      - OR last_pitched_date is NULL (never been pitched)
    """
    client = get_supabase()

    # Get all active contacts from the curators table
    response = (
        client.table('curators')
        .select('*')
        .eq('active', True)
        .execute()
    )

    all_active = response.data

    # Filter by cooldown — only include contacts who are ready for a new pitch
    eligible = []
    for c in all_active:
        never_pitched = c.get('last_pitched_date') is None
        cooldown_met = (c.get('releases_since_last_pitch', 0) >= c.get('cooldown_releases', 2))
        if never_pitched or cooldown_met:
            eligible.append(c)

    return eligible


def update_curator_after_pitch(email: str, release_name: str) -> None:
    """Update curator metadata after a successful pitch.

    Sets last_pitched_date to today, records the release name,
    resets releases_since_last_pitch to 0, and increments total_pitches.
    """
    from datetime import date
    client = get_supabase()

    # Get current total_pitches so we can increment it
    response = client.table('curators').select('total_pitches').eq('email', email).execute()
    current_pitches = response.data[0]['total_pitches'] if response.data else 0

    client.table('curators').update({
        'last_pitched_date': str(date.today()),
        'last_pitched_release': release_name,
        'releases_since_last_pitch': 0,
        'total_pitches': (current_pitches or 0) + 1,
    }).eq('email', email).execute()


def increment_cooldown_for_skipped(release_name: str, pitched_emails: set) -> None:
    """For curators NOT pitched this release, increment their releases_since_last_pitch.

    This way, after enough releases pass without being pitched,
    a curator becomes eligible again based on their cooldown_releases setting.
    """
    client = get_supabase()

    # Get all active curators
    response = client.table('curators').select('email, releases_since_last_pitch').eq('active', True).execute()

    for curator in response.data:
        if curator['email'] not in pitched_emails:
            new_count = (curator.get('releases_since_last_pitch') or 0) + 1
            client.table('curators').update({
                'releases_since_last_pitch': new_count,
            }).eq('email', curator['email']).execute()


# ---------------------------------------------------------------------------
# Logging setup — logs to both console and a file
# ---------------------------------------------------------------------------

LOG_FILE = Path(__file__).parent / "data" / "agent.log"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(str(LOG_FILE)),
    ],
)
logger = logging.getLogger("spotify_outreach_agent")

# ---------------------------------------------------------------------------
# Artist bio — used in all pitches so Claude has context
# ---------------------------------------------------------------------------
# Edit this to describe your sound. The more specific, the better the pitches.

ARTIST_BIO = """
moodmixformat is an independent tech house and melodic techno artist.
The sound sits somewhere between the groove-led tension of Liquid Lab (Kream),
the textured atmosphere of Drove, and the cinematic energy of DeVault —
driving but melodic, functional but with depth. Releases are independent,
focused on quality over quantity, with each track built as a complete idea
rather than a formula.
"""

# ---------------------------------------------------------------------------
# Release config helpers
# ---------------------------------------------------------------------------

def _extract_spotify_id(url: str) -> str:
    """Pull the track/album ID out of a Spotify URL."""
    path_parts = urlparse(url).path.strip("/").split("/")
    return path_parts[-1].split("?")[0] if path_parts else url


def get_release_from_args(spotify_url: str, release_name: str,
                          release_type: str = "single") -> dict:
    """
    Build a release dict from CLI arguments.
    Used when you pass --spotify-url and --release-name on the command line.
    """
    release_id = _extract_spotify_id(spotify_url)
    return {
        "id":           release_id,
        "name":         release_name,
        "type":         release_type,
        "release_date": datetime.now().strftime("%Y-%m-%d"),
        "spotify_url":  spotify_url,
        "total_tracks": 1,
    }


def get_release_from_env() -> Optional[dict]:
    """
    Build a release dict from environment variables.
    Used for Railway deployments or when you want to configure the release
    without CLI flags.

    Set these in your .env or Railway Variables before running:
      RELEASE_URL   — full Spotify link, e.g. https://open.spotify.com/track/...
      RELEASE_NAME  — song/EP/album title, e.g. "ABACUS"
      RELEASE_TYPE  — single | album | ep  (defaults to "single")
      RELEASE_DATE  — e.g. "2026-03-21"  (defaults to today)

    Returns None if RELEASE_URL or RELEASE_NAME is not set.
    """
    url  = os.environ.get("RELEASE_URL",  "").strip()
    name = os.environ.get("RELEASE_NAME", "").strip()

    if not url or not name:
        return None

    release_id = _extract_spotify_id(url)
    return {
        "id":           release_id,
        "name":         name,
        "type":         os.environ.get("RELEASE_TYPE", "single").lower(),
        "release_date": os.environ.get("RELEASE_DATE", datetime.now().strftime("%Y-%m-%d")),
        "spotify_url":  url,
        "total_tracks": int(os.environ.get("RELEASE_TOTAL_TRACKS", "1")),
    }


# ---------------------------------------------------------------------------
# Core agent logic
# ---------------------------------------------------------------------------

def run_outreach_agent(spotify_url: str = None, release_name: str = None) -> None:
    """
    The main agent function.

    Release priority:
      1. CLI args (--spotify-url / --release-name)
      2. Env vars (RELEASE_URL / RELEASE_NAME)
      3. Nothing to do — logs and exits cleanly

    Args:
      spotify_url:   Spotify track/album URL (from --spotify-url flag)
      release_name:  Release title (from --release-name flag)
    """
    logger.info("=" * 60)
    logger.info("moodmixformat Outreach Agent starting...")
    logger.info("Run time: %s", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    logger.info("=" * 60)

    # Determine release — CLI args take priority over env vars
    if spotify_url and release_name:
        release = get_release_from_args(spotify_url, release_name)
        logger.info("Release from CLI: '%s' — %s", release["name"], release["spotify_url"])
    else:
        release = get_release_from_env()
        if release:
            logger.info("Release from env vars: '%s' — %s", release["name"], release["spotify_url"])
        else:
            logger.info("No release configured. Set RELEASE_URL + RELEASE_NAME, or use --spotify-url.")
            logger.info("Nothing to pitch. See you next Friday!")
            return

    logger.info("Type: %s | Date: %s", release["type"], release["release_date"])

    # Get contacts from Supabase (filtered by active status and cooldown)
    contacts = get_active_contacts()
    logger.info("Loaded %d eligible contacts (cooldown-filtered) to pitch", len(contacts))

    # Generate personalised pitches
    logger.info("Generating personalised pitches...")
    try:
        pitched_contacts = generate_pitches_for_release(
            release=release,
            contacts=contacts,
            artist_bio=ARTIST_BIO.strip(),
        )
    except Exception as e:
        logger.error("Failed to generate pitches for '%s': %s", release["name"], e)
        logger.error("Make sure ANTHROPIC_API_KEY is set.")
        return

    # Send (or dry-run) the emails
    summary = send_all_pitches(
        pitched_contacts=pitched_contacts,
        release=release,
    )

    logger.info(
        "Release '%s' complete — sent: %d, skipped: %d, errors: %d",
        release["name"],
        summary["sent"],
        summary["skipped"],
        summary["errors"],
    )

    # Update cooldown tracking in Supabase for curators who were pitched
    pitched_emails = {item['contact']['email'] for item in pitched_contacts}
    for item in pitched_contacts:
        try:
            update_curator_after_pitch(item['contact']['email'], release['name'])
        except Exception as e:
            logger.warning("Could not update curator %s: %s", item['contact']['email'], e)

    # Increment cooldown counter for curators who were NOT pitched this time
    try:
        increment_cooldown_for_skipped(release['name'], pitched_emails)
    except Exception as e:
        logger.warning("Could not update skipped curators: %s", e)

    logger.info("All releases processed. Agent run complete.")


# ---------------------------------------------------------------------------
# Scheduler — runs every Friday at 9 AM local time
# ---------------------------------------------------------------------------

def run_scheduler() -> None:
    """
    Keep the script running and fire the agent every Friday at 09:00.
    Good for running on a server or always-on machine.
    For one-off / cron use, use --run-now instead.
    """
    logger.info("Scheduler started. Agent will run every Friday at 09:00.")
    logger.info("Keep this process running, or use --run-now for a one-off run.")

    schedule.every().friday.at("09:00").do(run_outreach_agent)

    while True:
        schedule.run_pending()
        time.sleep(60)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def _check_required_env_vars() -> bool:
    """Check all required env vars are set. Returns True if OK."""
    required = {
        "ANTHROPIC_API_KEY":   "Claude API key (get from console.anthropic.com)",
        "SENDER_EMAIL":        "Your Gmail address for sending outreach emails",
        "SENDER_APP_PASSWORD": "Your Gmail App Password (not your regular password)",
    }

    missing = []
    for var, description in required.items():
        if not os.environ.get(var):
            missing.append(f"  - {var}: {description}")

    if missing:
        logger.error("Missing required environment variables:")
        for line in missing:
            logger.error(line)
        logger.error("Set these in your .env file. See .env.example for a template.")
        return False

    return True


if __name__ == "__main__":
    # Load .env file if present (for local development)
    try:
        from dotenv import load_dotenv
        dotenv_path = Path(__file__).parent / ".env"
        if not dotenv_path.exists():
            dotenv_path = Path(__file__).parent.parent / ".env"
        if dotenv_path.exists():
            load_dotenv(dotenv_path)
            logger.info("Loaded .env from %s", dotenv_path)
    except ImportError:
        logger.warning("python-dotenv not installed. Using system environment variables only.")

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="moodmixformat Outreach Agent")
    parser.add_argument(
        "--run-now",
        action="store_true",
        help="Run the outreach agent immediately (instead of waiting for Friday)",
    )
    parser.add_argument(
        "--dry-run-only",
        action="store_true",
        help="Override: force dry run mode even if OUTREACH_LIVE_MODE=true",
    )
    parser.add_argument(
        "--spotify-url",
        type=str,
        default=None,
        help="Spotify track/album URL (bypasses env vars)",
    )
    parser.add_argument(
        "--release-name",
        type=str,
        default=None,
        help="Release title — required when using --spotify-url",
    )
    args = parser.parse_args()

    # Validate: if a URL is provided, a name must also be given
    if args.spotify_url and not args.release_name:
        logger.error("--release-name is required when using --spotify-url.")
        sys.exit(1)

    # Force dry run if requested
    if args.dry_run_only:
        os.environ["OUTREACH_LIVE_MODE"] = "false"
        logger.info("--dry-run-only flag set. No real emails will be sent.")

    if not _check_required_env_vars():
        sys.exit(1)

    # RUN_NOW env var lets Railway trigger a one-off run without changing
    # the start command. Set RUN_NOW=true in Railway Variables to fire immediately.
    run_now = args.run_now or os.environ.get("RUN_NOW", "").lower() == "true"

    if run_now:
        run_outreach_agent(
            spotify_url=args.spotify_url,
            release_name=args.release_name,
        )
    else:
        run_scheduler()
