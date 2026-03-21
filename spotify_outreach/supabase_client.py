"""
supabase_client.py
------------------
Creates and returns a shared Supabase client used across the agent.

Reads credentials from environment variables (set in your .env file):
  - SUPABASE_URL: your project URL (e.g. https://abc123.supabase.co)
  - SUPABASE_KEY: your project's anon/public key

You'll need two tables in your Supabase project:

  1. seen_releases
     Tracks which Spotify releases have already been pitched so we
     don't re-pitch the same release every week.

     CREATE TABLE seen_releases (
         release_id   TEXT PRIMARY KEY,
         release_name TEXT,
         release_type TEXT,
         release_date TEXT,
         spotify_url  TEXT,
         created_at   TIMESTAMPTZ DEFAULT NOW()
     );

  2. outreach_log
     Append-only audit trail of every email action (sent, skipped, error).
     Also used to check deduplication (did we already email this person?).

     CREATE TABLE outreach_log (
         id            UUID DEFAULT gen_random_uuid() PRIMARY KEY,
         timestamp     TIMESTAMPTZ,
         action        TEXT,
         contact_name  TEXT,
         contact_email TEXT,
         release_name  TEXT,
         release_id    TEXT,
         subject       TEXT,
         error_message TEXT,
         created_at    TIMESTAMPTZ DEFAULT NOW()
     );

Run both CREATE TABLE statements in your Supabase SQL Editor before first use.
"""

import os
import logging
from typing import Optional
from supabase import create_client, Client

logger = logging.getLogger(__name__)

# Cache the client so we only create it once per run
_client: Optional[Client] = None


def get_supabase() -> Client:
    """
    Return the shared Supabase client.
    Creates it on first call, then reuses the same connection.
    """
    global _client
    if _client is None:
        url = os.environ.get("SUPABASE_URL", "")
        key = os.environ.get("SUPABASE_KEY", "")

        if not url or not key:
            raise ValueError(
                "SUPABASE_URL and SUPABASE_KEY must be set in your .env file. "
                "Find them in your Supabase project under Settings → API."
            )

        _client = create_client(url, key)
        logger.info("Supabase client connected to %s", url)

    return _client
