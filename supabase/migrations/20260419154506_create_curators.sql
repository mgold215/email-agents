CREATE TABLE IF NOT EXISTS curators (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    type TEXT NOT NULL,
    genre_focus TEXT,
    notes TEXT,
    submission_url TEXT,
    active BOOLEAN DEFAULT TRUE,
    cooldown_releases INTEGER DEFAULT 2,
    releases_since_last_pitch INTEGER DEFAULT 0,
    last_pitched_date DATE,
    last_pitched_release TEXT,
    total_pitches INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_curators_active ON curators (active) WHERE active = TRUE;
CREATE INDEX IF NOT EXISTS idx_curators_email ON curators (email);
