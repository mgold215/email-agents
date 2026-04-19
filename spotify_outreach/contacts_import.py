"""
contacts_import.py
------------------
One-time script to import hardcoded contacts from contacts.py into the Supabase curators table.
Safe to re-run — uses upsert on email (unique key), so existing rows get updated, not duplicated.

Usage:
    cd spotify_outreach && python3 contacts_import.py
"""

import os
import sys

# Add this directory to the Python path so we can import our modules
sys.path.insert(0, os.path.dirname(__file__))

from contacts import get_email_contacts
from supabase_client import get_supabase


def import_contacts():
    """Import all hardcoded contacts into the Supabase curators table."""
    contacts = get_email_contacts()
    client = get_supabase()

    print(f"Importing {len(contacts)} contacts into Supabase curators table...")

    imported = 0
    skipped = 0
    for contact in contacts:
        # Build a row matching the curators table schema
        row = {
            'name': contact['name'],
            'email': contact['email'],
            'type': contact.get('type', 'playlist_curator'),
            'genre_focus': contact.get('genre_focus', ''),
            'notes': contact.get('notes', ''),
            'submission_url': contact.get('submission_url'),
            'active': True,
        }
        try:
            # Upsert = insert if new, update if email already exists
            client.table('curators').upsert(row, on_conflict='email').execute()
            imported += 1
            print(f"  [{imported}] {contact['name']} ({contact['email']})")
        except Exception as e:
            print(f"  SKIP {contact['name']}: {e}")
            skipped += 1

    print(f"\nDone. Imported: {imported}, Skipped: {skipped}")


if __name__ == '__main__':
    # Load .env file if present (for local development)
    try:
        from dotenv import load_dotenv
        from pathlib import Path
        dotenv_path = Path(__file__).parent / ".env"
        if dotenv_path.exists():
            load_dotenv(dotenv_path)
    except ImportError:
        pass

    import_contacts()
