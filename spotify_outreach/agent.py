"""
agent.py
--------
The main Spotify Outreach Agent for moodmixformat.

What this does every Friday:
  1. Checks Spotify for new releases (singles, EPs, albums)
  2. For each new release, generates a personalised pitch to every contact
  3. Sends (or simulates) the emails with rate limiting
  4. Logs everything for audit trail

How to run:
  - One-time / manual:  python agent.py --run-now
  - Scheduled (cron):   python agent.py           (runs every Friday at 9 AM)
  - Dry run:            Make sure OUTREACH_LIVE_MODE is NOT set to true

Scheduling options:
  - Built-in scheduler: just run `python agent.py` — it checks every Friday
  - Cron (recommended): add to crontab: `0 9 * * 5 cd /path/to/agent && python agent.py --run-now`
    (runs at 9:00 AM every Friday)
"""

import argparse
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

import schedule
import time

# Add parent dir to path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent))

from spotify_checker import check_for_new_releases, release_from_url
from contacts import get_email_contacts
from pitch_generator import generate_pitches_for_release
from email_sender import send_all_pitches

# ---------------------------------------------------------------------------
# Logging setup — logs to both console and a file
# ---------------------------------------------------------------------------

LOG_FILE = Path(__file__).parent / "data" / "agent.log"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),          # print to console
        logging.FileHandler(str(LOG_FILE)),         # write to log file
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
# Core agent logic
# ---------------------------------------------------------------------------

def run_outreach_agent(manual_spotify_url: str = None, manual_release_name: str = None) -> None:
    """
    The main agent function — called every Friday (or manually via --run-now).

    Steps:
      1. Get new releases — either from Spotify API, or from a URL you provide
      2. For each new release, pitch all contacts
      3. Log results

    Args:
      manual_spotify_url:   If provided, skips the Spotify API check and uses this URL directly.
      manual_release_name:  The name of the release (required when manual_spotify_url is set).
    """
    logger.info("=" * 60)
    logger.info("moodmixformat Spotify Outreach Agent starting...")
    logger.info("Run time: %s", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    logger.info("=" * 60)

    # Step 1: Get new releases
    if manual_spotify_url:
        # Manual mode: use the URL the user provided instead of checking the API
        logger.info("Manual mode: using provided Spotify URL instead of API check.")
        new_releases = [release_from_url(manual_spotify_url, manual_release_name)]
        logger.info("Release: '%s' — %s", new_releases[0]["name"], new_releases[0]["spotify_url"])
    else:
        # Auto mode: check Spotify API for new releases this week
        try:
            new_releases = check_for_new_releases()
        except Exception as e:
            logger.error("Failed to check Spotify for releases: %s", e)
            logger.error("Make sure SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET are set.")
            logger.error("Or use --spotify-url to provide a link directly.")
            return

    if not new_releases:
        logger.info("No new releases found this week. Nothing to pitch. See you next Friday!")
        return

    # Step 2: Get the full contacts list
    contacts = get_email_contacts()
    logger.info("Loaded %d email contacts to pitch", len(contacts))

    # Step 3: Process each new release
    for release in new_releases:
        logger.info(
            "Processing release: '%s' (%s) — %s",
            release["name"],
            release["type"],
            release["release_date"],
        )
        logger.info("Spotify URL: %s", release["spotify_url"])

        # Generate personalised pitches for all contacts
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
            continue

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

    # Schedule the job every Friday at 9 AM
    schedule.every().friday.at("09:00").do(run_outreach_agent)

    while True:
        schedule.run_pending()
        time.sleep(60)  # check every minute


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def _check_required_env_vars() -> bool:
    """
    Verify that all required environment variables are set before running.
    Returns True if OK, False if something is missing.
    """
    required = {
        "ANTHROPIC_API_KEY": "Claude API key (get from console.anthropic.com)",
        "SENDER_EMAIL": "Your Gmail address for sending outreach emails",
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
        # Look for .env in the spotify_outreach directory or one level up
        dotenv_path = Path(__file__).parent / ".env"
        if not dotenv_path.exists():
            dotenv_path = Path(__file__).parent.parent / ".env"
        if dotenv_path.exists():
            load_dotenv(dotenv_path)
            logger.info("Loaded .env from %s", dotenv_path)
    except ImportError:
        logger.warning("python-dotenv not installed. Using system environment variables only.")

    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="moodmixformat Spotify Outreach Agent"
    )
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
        help="Provide a Spotify track/album URL directly instead of checking the API",
    )
    parser.add_argument(
        "--release-name",
        type=str,
        default=None,
        help="Name of the release (required when using --spotify-url)",
    )
    args = parser.parse_args()

    # Validate: if a URL is provided, a release name must also be given
    if args.spotify_url and not args.release_name:
        logger.error("--release-name is required when using --spotify-url.")
        logger.error("Example: python agent.py --run-now --spotify-url '...' --release-name 'Song Title'")
        sys.exit(1)

    # Force dry run if requested via CLI flag
    if args.dry_run_only:
        os.environ["OUTREACH_LIVE_MODE"] = "false"
        logger.info("--dry-run-only flag set. No real emails will be sent.")

    # Check all env vars are present
    if not _check_required_env_vars():
        sys.exit(1)

    if args.run_now:
        # Run immediately, with optional manual URL override
        run_outreach_agent(
            manual_spotify_url=args.spotify_url,
            manual_release_name=args.release_name,
        )
    else:
        # Run on schedule (every Friday)
        run_scheduler()
