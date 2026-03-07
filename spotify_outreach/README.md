# moodmixformat — Spotify Outreach Agent

Automatically checks your Spotify discography every Friday, then sends
personalised pitch emails to a large list of playlist curators, music blogs,
and radio stations whenever you drop a new single, EP, or album.

---

## How It Works

```
Every Friday at 9 AM
        │
        ▼
Check Spotify artist discography
(singles + EPs + albums)
        │
        ▼
Any new releases since last check?
  No → done, see you next Friday
  Yes ↓
        │
        ▼
For each new release:
  → Claude generates a personalised email for each contact
  → Emails are sent with 30s gap between each (rate limiting)
  → Every action is logged to data/audit_log.jsonl
  → Dedup check: never email same contact twice about same release
```

---

## Setup (Step by Step)

### 1. Install Dependencies

```bash
cd spotify_outreach
pip install -r requirements.txt
```

### 2. Set Up Spotify API

1. Go to [developer.spotify.com/dashboard](https://developer.spotify.com/dashboard)
2. Log in → **Create App**
3. Fill in any name/description, set Redirect URI to `http://localhost`
4. Copy the **Client ID** and **Client Secret**

### 3. Get Your Anthropic API Key

1. Go to [console.anthropic.com](https://console.anthropic.com)
2. API Keys → **Create Key**
3. Copy it

### 4. Set Up Gmail App Password

1. Go to [myaccount.google.com](https://myaccount.google.com)
2. **Security** → **2-Step Verification** (enable if not already)
3. **Security** → **App passwords**
4. Select **Mail** + **Other (Custom name)** → type `Outreach Agent`
5. Copy the 16-character password

### 5. Configure Environment

```bash
cp .env.example .env
# Edit .env with your real values
```

### 6. Test in Dry Run Mode (No Emails Sent)

Make sure `OUTREACH_LIVE_MODE=false` in your `.env`, then:

```bash
python agent.py --run-now
```

This will:
- Check Spotify for your latest releases
- Generate all pitches using Claude
- **Print** the emails to your terminal (no sending)
- Log everything to `data/`

Review the output. When you're happy with how it looks, move to step 7.

### 7. Go Live

Once you've verified everything looks right in dry-run:

1. Edit `.env`: change `OUTREACH_LIVE_MODE=false` → `OUTREACH_LIVE_MODE=true`
2. Run again: `python agent.py --run-now`

Real emails will now be sent.

---

## Running on a Schedule

### Option A: Built-in Scheduler (keep process running)

```bash
python agent.py
```

Runs every Friday at 9 AM. Keep the terminal/process alive.

### Option B: Cron Job (recommended — more reliable)

Add to your crontab (`crontab -e`):

```cron
# Run moodmixformat outreach every Friday at 9:00 AM
0 9 * * 5 cd /home/user/email-agents/spotify_outreach && python agent.py --run-now >> data/cron.log 2>&1
```

---

## Files & Folders

```
spotify_outreach/
├── agent.py              ← Main script (run this)
├── spotify_checker.py    ← Checks Spotify for new releases
├── contacts.py           ← List of all curators, blogs, radio stations
├── pitch_generator.py    ← Uses Claude to write personalised pitches
├── email_sender.py       ← Sends emails with rate limiting + logging
├── requirements.txt      ← Python dependencies
├── .env.example          ← Copy to .env and fill in your keys
├── .env                  ← Your secrets (NOT in Git)
└── data/                 ← Auto-created at runtime
    ├── seen_releases.json    ← Tracks which Spotify releases you've already pitched
    ├── contacted_log.json    ← Tracks who has been emailed per release (no double-sends)
    ├── audit_log.jsonl       ← Full audit trail of every action
    └── agent.log             ← Human-readable run logs
```

---

## Contacts List

The agent pitches to **~60 contacts** across three categories:

| Category | Count | Examples |
|---|---|---|
| Playlist Curators | 25 | Chillhop Music, Lofi Girl, Majestic Casual, MrSuicideSheep |
| Music Blogs | 18 | Pigeons & Planes, Earmilk, Ones To Watch, Consequence of Sound |
| Radio Stations | 20 | KEXP, KCRW, BBC Introducing, NTS Radio, Soma FM |

To add more contacts, edit `contacts.py` — just follow the existing format.

---

## Customising Your Artist Bio

In `agent.py`, find the `ARTIST_BIO` variable and update it with your actual sound description. The more specific you are, the better Claude's pitches will be.

---

## Safety & Anti-Spam

- **Rate limiting**: 30 seconds between each email (configurable)
- **Deduplication**: Never emails the same contact about the same release twice
- **Dry run default**: No real emails until you explicitly set `OUTREACH_LIVE_MODE=true`
- **Audit log**: Every send is logged to `data/audit_log.jsonl`
- **One pitch per person per release**: Respectful, not spammy

---

## Submission Platforms (Use Alongside This Agent)

These platforms let you reach even more curators but require manual submission:

| Platform | URL | Notes |
|---|---|---|
| SubmitHub | submithub.com | Industry standard. Get feedback + placement. |
| Groover | groover.co | Paid but guaranteed response. |
| Playlist Push | playlistpush.com | Spotify-focused curator network. |
| Spotify for Artists | artists.spotify.com | Submit to Spotify editorial playlists directly. |

---

## Troubleshooting

**"Missing required environment variables"**
→ Make sure your `.env` file exists and is in the `spotify_outreach/` folder.

**"Failed to check Spotify for releases"**
→ Check `SPOTIFY_CLIENT_ID` and `SPOTIFY_CLIENT_SECRET` are correct in `.env`.

**"Gmail authentication failed"**
→ Make sure you're using an App Password (not your regular Gmail password).
→ Check that 2-Step Verification is enabled on your Google account.

**"No new releases found"**
→ The agent checks for releases it hasn't seen before. If you just set it up,
   run it once to let it scan your existing discography. New releases after
   that will trigger pitches.

**Want to reset and re-pitch everything?**
→ Delete `data/seen_releases.json` and `data/contacted_log.json`.
   The agent will treat all your releases as new on the next run.
