-- ============================================================
-- supabase_setup.sql
-- Run this in your Supabase SQL Editor (supabase.com → SQL Editor)
-- It creates the two tables AND enables Row Level Security (RLS).
--
-- WHY RLS MATTERS:
--   Supabase exposes a public REST API using the "anon" key.
--   Without RLS, anyone who finds that key can read, insert,
--   update, or delete ALL rows in your tables.  Enabling RLS
--   blocks all access through the anon key by default.
--   Our server-side agent uses the service_role key, which
--   bypasses RLS — so the agent still works normally.
-- ============================================================

-- 1. seen_releases — tracks which Spotify releases have been pitched
CREATE TABLE IF NOT EXISTS seen_releases (
    release_id   TEXT PRIMARY KEY,
    release_name TEXT,
    release_type TEXT,
    release_date TEXT,
    spotify_url  TEXT,
    created_at   TIMESTAMPTZ DEFAULT NOW()
);

-- Enable RLS so the anon key cannot access this table
ALTER TABLE seen_releases ENABLE ROW LEVEL SECURITY;

-- No policies = no access via anon key (service_role bypasses RLS)


-- 2. outreach_log — append-only audit trail of every email action
CREATE TABLE IF NOT EXISTS outreach_log (
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

-- Enable RLS so the anon key cannot access this table
ALTER TABLE outreach_log ENABLE ROW LEVEL SECURITY;

-- No policies = no access via anon key (service_role bypasses RLS)


-- ============================================================
-- VERIFICATION: after running this script, confirm RLS is on:
--   SELECT tablename, rowsecurity
--   FROM pg_tables
--   WHERE schemaname = 'public';
-- Both tables should show rowsecurity = true.
-- ============================================================
