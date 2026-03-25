"""
supabase_client.py
------------------
Creates and returns a shared Supabase client used across the agent.

Reads credentials from environment variables (set in your .env file):
  - SUPABASE_URL: your project URL (e.g. https://abc123.supabase.co)
  - SUPABASE_SERVICE_ROLE_KEY: your project's service_role (secret) key

IMPORTANT — we use the service_role key (NOT the anon/public key) because
this is a server-side automation script that runs in a trusted environment.
The service_role key bypasses Row Level Security, which is what we want for
our own backend.  Meanwhile, RLS stays enabled on the tables so that if the
anon key is ever exposed, no one can read or modify the data through it.

You'll need two tables in your Supabase project.  Run the SQL in
supabase_setup.sql in the Supabase SQL Editor before first use.
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
    Uses the service_role key so the agent can bypass RLS server-side.
    """
    global _client
    if _client is None:
        url = os.environ.get("SUPABASE_URL", "")
        # Prefer the new service-role variable; fall back to the old
        # SUPABASE_KEY for backwards compatibility during migration.
        key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "") or os.environ.get("SUPABASE_KEY", "")

        if not url or not key:
            raise ValueError(
                "SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set in "
                "your .env file.  Find the service_role key in your Supabase "
                "project under Settings → API → Project API Keys."
            )

        _client = create_client(url, key)
        # Log connection without exposing the full project URL
        logger.info("Supabase client connected successfully")

    return _client


def sanitize_text(value: str, max_length: int = 1000) -> str:
    """
    Basic input sanitization for text going into the database.
    Strips leading/trailing whitespace and truncates to max_length.
    """
    if not isinstance(value, str):
        return ""
    return value.strip()[:max_length]
