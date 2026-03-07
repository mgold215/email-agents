"""
email_sender.py
---------------
Handles sending the personalised pitch emails AND logging every action.

Key safety features:
  1. DRY RUN MODE (default) — prints emails to console WITHOUT sending.
     You must explicitly set OUTREACH_LIVE_MODE=true in your .env to send real emails.

  2. Rate limiting — waits between emails to avoid being flagged as spam.
     Default: 30 seconds between each email.

  3. Audit log — every action (sent, skipped, error) is written to a log file.

  4. Deduplication — tracks who has been contacted per release so you never
     double-email the same person about the same release.

Email is sent via Gmail SMTP using an App Password.
(You must enable 2FA on your Google account and create an App Password.)
"""

import json
import logging
import os
import smtplib
import time
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Config — read from environment variables
# ---------------------------------------------------------------------------

# Your Gmail address (the one you're sending FROM)
SENDER_EMAIL = os.environ.get("SENDER_EMAIL", "")

# Gmail App Password (NOT your regular Gmail password)
# Generate at: myaccount.google.com/apppasswords
SENDER_APP_PASSWORD = os.environ.get("SENDER_APP_PASSWORD", "")

# Your name as it appears in the "From" field
SENDER_NAME = os.environ.get("SENDER_NAME", "moodmixformat")

# When False (default): emails are printed to console but NOT sent.
# Set OUTREACH_LIVE_MODE=true in .env ONLY when you're ready for real sends.
LIVE_MODE = os.environ.get("OUTREACH_LIVE_MODE", "false").lower() == "true"

# Seconds to wait between each email to avoid spam filters
RATE_LIMIT_SECONDS = int(os.environ.get("EMAIL_RATE_LIMIT_SECONDS", "30"))

# File that tracks who has already been contacted per release
CONTACTED_LOG_FILE = Path(__file__).parent / "data" / "contacted_log.json"

# Audit log file for all send actions
AUDIT_LOG_FILE = Path(__file__).parent / "data" / "audit_log.jsonl"


# ---------------------------------------------------------------------------
# Deduplication helpers
# ---------------------------------------------------------------------------

def _load_contacted_log() -> dict:
    """
    Load the dict of {release_id: [list of contact emails already sent]}.
    Returns empty dict if the file doesn't exist.
    """
    if CONTACTED_LOG_FILE.exists():
        return json.loads(CONTACTED_LOG_FILE.read_text())
    return {}


def _save_contacted_log(log: dict) -> None:
    """Save the contacted log back to disk."""
    CONTACTED_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    CONTACTED_LOG_FILE.write_text(json.dumps(log, indent=2))


def already_contacted(release_id: str, contact_email: str) -> bool:
    """Return True if we've already emailed this contact about this release."""
    log = _load_contacted_log()
    return contact_email in log.get(release_id, [])


def mark_as_contacted(release_id: str, contact_email: str) -> None:
    """Record that we've emailed this contact about this release."""
    log = _load_contacted_log()
    if release_id not in log:
        log[release_id] = []
    if contact_email not in log[release_id]:
        log[release_id].append(contact_email)
    _save_contacted_log(log)


# ---------------------------------------------------------------------------
# Audit logging
# ---------------------------------------------------------------------------

def _write_audit_entry(entry: dict) -> None:
    """
    Append one line to the audit log file.
    Each line is a JSON object — this is the "append-only" log for compliance.
    """
    AUDIT_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(AUDIT_LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")


# ---------------------------------------------------------------------------
# Email sending
# ---------------------------------------------------------------------------

def _build_email_message(
    to_email: str,
    to_name: str,
    subject: str,
    body: str,
) -> MIMEMultipart:
    """
    Build the MIME email message object.
    Sends as plain text (no HTML) — simpler and less likely to hit spam.
    """
    msg = MIMEMultipart()
    msg["From"] = f"{SENDER_NAME} <{SENDER_EMAIL}>"
    msg["To"] = f"{to_name} <{to_email}>"
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))
    return msg


def send_pitch(
    contact: dict,
    release: dict,
    subject: str,
    body: str,
) -> bool:
    """
    Send (or simulate sending) a single pitch email.

    Returns True if the email was sent (or would have been in dry-run mode),
    False if it was skipped (already contacted) or errored.
    """
    contact_email = contact.get("email")
    contact_name = contact.get("name", "Unknown")
    release_id = release.get("id", "unknown")

    # --- Skip if no email address ---
    if not contact_email:
        logger.warning("Skipping %s — no email address", contact_name)
        return False

    # --- Skip if already contacted about this release ---
    if already_contacted(release_id, contact_email):
        logger.info("Skipping %s — already contacted about '%s'", contact_name, release["name"])
        _write_audit_entry({
            "timestamp": datetime.utcnow().isoformat(),
            "action": "skipped_duplicate",
            "contact": contact_name,
            "email": contact_email,
            "release": release["name"],
            "release_id": release_id,
        })
        return False

    # --- Dry run: print to console instead of sending ---
    if not LIVE_MODE:
        print("\n" + "=" * 70)
        print(f"[DRY RUN] Would send email to: {contact_name} <{contact_email}>")
        print(f"Subject: {subject}")
        print("-" * 70)
        print(body)
        print("=" * 70)

        _write_audit_entry({
            "timestamp": datetime.utcnow().isoformat(),
            "action": "dry_run",
            "contact": contact_name,
            "email": contact_email,
            "release": release["name"],
            "release_id": release_id,
            "subject": subject,
        })
        # Mark as contacted even in dry-run, so we don't re-send in the next real run
        # (Comment this out if you want to re-send to everyone when you go live)
        # mark_as_contacted(release_id, contact_email)
        return True

    # --- Live mode: actually send the email ---
    try:
        msg = _build_email_message(contact_email, contact_name, subject, body)

        # Connect to Gmail SMTP over TLS (port 587)
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_APP_PASSWORD)
            server.send_message(msg)

        # Record in dedup log and audit log
        mark_as_contacted(release_id, contact_email)
        _write_audit_entry({
            "timestamp": datetime.utcnow().isoformat(),
            "action": "sent",
            "contact": contact_name,
            "email": contact_email,
            "release": release["name"],
            "release_id": release_id,
            "subject": subject,
        })
        logger.info("Email sent to %s <%s>", contact_name, contact_email)
        return True

    except smtplib.SMTPAuthenticationError:
        logger.error(
            "Gmail authentication failed. Check SENDER_EMAIL and SENDER_APP_PASSWORD."
        )
        _write_audit_entry({
            "timestamp": datetime.utcnow().isoformat(),
            "action": "error_auth",
            "contact": contact_name,
            "email": contact_email,
            "release": release["name"],
            "release_id": release_id,
        })
        return False

    except Exception as e:
        logger.error("Failed to send email to %s: %s", contact_name, e)
        _write_audit_entry({
            "timestamp": datetime.utcnow().isoformat(),
            "action": "error_send",
            "contact": contact_name,
            "email": contact_email,
            "release": release["name"],
            "release_id": release_id,
            "error": str(e),
        })
        return False


def send_all_pitches(pitched_contacts: list[dict], release: dict) -> dict:
    """
    Send emails to all contacts in the list, with rate limiting between each.

    Args:
        pitched_contacts: List of dicts from pitch_generator, each with
                          'contact', 'subject', 'body' keys.
        release:          The release dict from spotify_checker.

    Returns:
        A summary dict: { "sent": int, "skipped": int, "errors": int }
    """
    summary = {"sent": 0, "skipped": 0, "errors": 0}
    total = len(pitched_contacts)

    mode_label = "LIVE" if LIVE_MODE else "DRY RUN"
    logger.info(
        "Starting outreach for '%s' — %d contacts [%s MODE]",
        release["name"], total, mode_label
    )

    if not LIVE_MODE:
        logger.info(
            "DRY RUN MODE is ON. No real emails will be sent. "
            "Set OUTREACH_LIVE_MODE=true in your .env to send for real."
        )

    for i, item in enumerate(pitched_contacts, 1):
        contact = item["contact"]
        subject = item["subject"]
        body = item["body"]

        logger.info("Processing %d/%d: %s", i, total, contact["name"])

        success = send_pitch(contact, release, subject, body)

        if success:
            summary["sent"] += 1
        elif already_contacted(release["id"], contact.get("email", "")):
            summary["skipped"] += 1
        else:
            summary["errors"] += 1

        # Wait between emails to be a good citizen (avoid spam flags)
        # Skip the wait after the last email
        if i < total and LIVE_MODE:
            logger.debug("Waiting %d seconds before next email...", RATE_LIMIT_SECONDS)
            time.sleep(RATE_LIMIT_SECONDS)
        elif i < total and not LIVE_MODE:
            # In dry run, still show a shorter pause
            time.sleep(0.5)

    logger.info(
        "Outreach complete for '%s': sent=%d, skipped=%d, errors=%d",
        release["name"],
        summary["sent"],
        summary["skipped"],
        summary["errors"],
    )
    return summary
