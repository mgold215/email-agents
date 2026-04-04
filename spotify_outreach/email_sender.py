"""
email_sender.py
---------------
Handles sending the personalised pitch emails AND logging every action.

Key safety features:
  1. DRY RUN MODE (default) — prints emails to console WITHOUT sending.
     You must explicitly set OUTREACH_LIVE_MODE=true in your .env to send real emails.

  2. Rate limiting — waits between emails to avoid being flagged as spam.
     Default: 30 seconds between each email.

  3. Audit log — every action (sent, skipped, error) is written to Supabase
     in the 'outreach_log' table for a permanent, queryable audit trail.

  4. Deduplication — checks Supabase to see if this contact was already emailed
     about this release, so you never double-send.

Email is sent via the Brevo API (HTTPS) — works on all cloud platforms
including Railway, which blocks outbound SMTP ports.
"""

import logging
import os
import time
import requests
from datetime import datetime, timezone

from supabase_client import get_supabase

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Config — read from environment variables
# ---------------------------------------------------------------------------

# Your email address (the one you're sending FROM)
SENDER_EMAIL = os.environ.get("SENDER_EMAIL", "")

# Your name as it appears in the "From" field
SENDER_NAME = os.environ.get("SENDER_NAME", "moodmixformat")

# BCC email — you'll receive a blind copy of every outreach email.
# Defaults to SENDER_EMAIL if not set separately. Set BCC_EMAIL in .env to use a different address.
BCC_EMAIL = os.environ.get("BCC_EMAIL", "") or SENDER_EMAIL

# Brevo API key — get a free one at app.brevo.com → Settings → API Keys
# Add this as BREVO_API_KEY in Railway variables
BREVO_API_KEY = os.environ.get("BREVO_API_KEY", "")

# Brevo API endpoint for sending transactional emails
BREVO_API_URL = "https://api.brevo.com/v3/smtp/email"

# When False (default): emails are printed to console but NOT sent.
# Set OUTREACH_LIVE_MODE=true in .env ONLY when you're ready for real sends.
# NOTE: This is read at runtime (not import time) so .env loading works correctly.

# Seconds to wait between each email to avoid spam filters
RATE_LIMIT_SECONDS = int(os.environ.get("EMAIL_RATE_LIMIT_SECONDS", "30"))


# ---------------------------------------------------------------------------
# Supabase audit log helpers
# ---------------------------------------------------------------------------

def _write_audit_entry(entry: dict) -> None:
    """
    Insert one row into the Supabase 'outreach_log' table.
    This is the permanent, append-only audit trail for every email action.

    entry keys: action, contact_name, contact_email, release_name,
                release_id, subject (optional), error_message (optional)
    """
    supabase = get_supabase()
    row = {
        "timestamp":     datetime.now(timezone.utc).isoformat(),
        "action":        entry.get("action"),
        "contact_name":  entry.get("contact"),
        "contact_email": entry.get("email"),
        "release_name":  entry.get("release"),
        "release_id":    entry.get("release_id"),
        "subject":       entry.get("subject"),
        "error_message": entry.get("error"),
    }
    supabase.table("outreach_log").insert(row).execute()


# ---------------------------------------------------------------------------
# Deduplication helpers — check/mark using Supabase outreach_log
# ---------------------------------------------------------------------------

def already_contacted(release_id: str, contact_email: str) -> bool:
    """
    Return True if we've already sent (or logged a 'sent') email to this
    contact about this release. Checks the Supabase outreach_log table.
    """
    supabase = get_supabase()
    response = (
        supabase.table("outreach_log")
        .select("id")
        .eq("release_id", release_id)
        .eq("contact_email", contact_email)
        .eq("action", "sent")
        .limit(1)
        .execute()
    )
    return len(response.data) > 0


# ---------------------------------------------------------------------------
# Email sending
# ---------------------------------------------------------------------------

def send_pitch(
    contact: dict,
    release: dict,
    subject: str,
    body: str,
    refresh_recipients: bool = False,
) -> bool:
    """
    Send (or simulate sending) a single pitch email.

    Args:
      refresh_recipients: When True, bypasses the deduplication check so the
                          email is sent even if this contact was contacted before.

    Returns True if the email was sent (or simulated in dry-run mode),
    False if it was skipped (already contacted) or errored.
    """
    contact_email = contact.get("email")
    contact_name = contact.get("name", "Unknown")
    release_id = release.get("id", "unknown")

    # --- Skip if no email address ---
    if not contact_email:
        logger.warning("Skipping %s — no email address", contact_name)
        return False

    # --- Skip if already contacted about this release (dedup check in Supabase) ---
    # Bypassed when refresh_recipients=True so you can re-send to all contacts.
    if not refresh_recipients and already_contacted(release_id, contact_email):
        logger.info("Skipping %s — already contacted about '%s'", contact_name, release["name"])
        _write_audit_entry({
            "action":     "skipped_duplicate",
            "contact":    contact_name,
            "email":      contact_email,
            "release":    release["name"],
            "release_id": release_id,
        })
        return False

    # Read live mode at runtime so .env is already loaded by this point
    LIVE_MODE = os.environ.get("OUTREACH_LIVE_MODE", "false").lower() == "true"

    # Read BCC at runtime so .env is already loaded
    bcc_email = os.environ.get("BCC_EMAIL", "") or os.environ.get("SENDER_EMAIL", "")

    # --- Dry run: print to console instead of sending ---
    if not LIVE_MODE:
        print("\n" + "=" * 70)
        print(f"[DRY RUN] Would send email to: {contact_name} <{contact_email}>")
        if bcc_email:
            print(f"BCC: {bcc_email}")
        print(f"Subject: {subject}")
        print("-" * 70)
        print(body)
        print("=" * 70)

        _write_audit_entry({
            "action":     "dry_run",
            "contact":    contact_name,
            "email":      contact_email,
            "release":    release["name"],
            "release_id": release_id,
            "subject":    subject,
        })
        # NOTE: We do NOT mark as 'sent' in dry run, so live mode will still send later.
        return True

    # --- Live mode: send via Brevo API (HTTPS, works on Railway) ---
    try:
        # Build the email payload; include BCC if an address is configured
        email_payload = {
            "sender":      {"name": SENDER_NAME, "email": SENDER_EMAIL},
            "to":          [{"name": contact_name, "email": contact_email}],
            "subject":     subject,
            "textContent": body,
        }
        if bcc_email:
            email_payload["bcc"] = [{"email": bcc_email}]

        response = requests.post(
            BREVO_API_URL,
            headers={
                "api-key": BREVO_API_KEY,
                "Content-Type": "application/json",
            },
            json=email_payload,
            timeout=30,
        )

        if response.status_code in (200, 201):
            _write_audit_entry({
                "action":     "sent",
                "contact":    contact_name,
                "email":      contact_email,
                "release":    release["name"],
                "release_id": release_id,
                "subject":    subject,
            })
            logger.info("Email sent to %s <%s>", contact_name, contact_email)
            return True
        else:
            error_msg = f"Brevo API error {response.status_code}: {response.text}"
            logger.error("Failed to send email to %s: %s", contact_name, error_msg)
            _write_audit_entry({
                "action":     "error_send",
                "contact":    contact_name,
                "email":      contact_email,
                "release":    release["name"],
                "release_id": release_id,
                "error":      error_msg,
            })
            return False

    except Exception as e:
        logger.error("Failed to send email to %s: %s", contact_name, e)
        _write_audit_entry({
            "action":     "error_send",
            "contact":    contact_name,
            "email":      contact_email,
            "release":    release["name"],
            "release_id": release_id,
            "error":      str(e),
        })
        return False


def send_all_pitches(pitched_contacts: list[dict], release: dict,
                     refresh_recipients: bool = False) -> dict:
    """
    Send emails to all contacts in the list, with rate limiting between each.

    Args:
        pitched_contacts:   List of dicts from pitch_generator, each with
                            'contact', 'subject', 'body' keys.
        release:            The release dict from spotify_checker.
        refresh_recipients: When True, bypasses deduplication so all contacts
                            are emailed even if they were contacted before.

    Returns:
        A summary dict: { "sent": int, "skipped": int, "errors": int }
    """
    summary = {"sent": 0, "skipped": 0, "errors": 0}
    total = len(pitched_contacts)

    # Read live mode at runtime so .env is already loaded by this point
    LIVE_MODE = os.environ.get("OUTREACH_LIVE_MODE", "false").lower() == "true"

    mode_label = "LIVE" if LIVE_MODE else "DRY RUN"
    logger.info(
        "Starting outreach for '%s' — %d contacts [%s MODE]%s",
        release["name"], total, mode_label,
        " [REFRESH RECIPIENTS — dedup bypassed]" if refresh_recipients else "",
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

        success = send_pitch(contact, release, subject, body,
                             refresh_recipients=refresh_recipients)

        if success:
            summary["sent"] += 1
        elif already_contacted(release["id"], contact.get("email", "")):
            summary["skipped"] += 1
        else:
            summary["errors"] += 1

        # Wait between emails to avoid spam flags
        # Skip the wait after the last email
        if i < total and LIVE_MODE:
            logger.debug("Waiting %d seconds before next email...", RATE_LIMIT_SECONDS)
            time.sleep(RATE_LIMIT_SECONDS)
        elif i < total and not LIVE_MODE:
            time.sleep(0.5)

    logger.info(
        "Outreach complete for '%s': sent=%d, skipped=%d, errors=%d",
        release["name"],
        summary["sent"],
        summary["skipped"],
        summary["errors"],
    )
    return summary
