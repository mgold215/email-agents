"""
pitch_generator.py
------------------
Uses the Claude API (claude-opus-4-6) to write a unique, personalised
outreach pitch for each contact.

Why personalise?
  - Generic mass emails get ignored or marked as spam
  - Curators and radio stations respond better when you show you know them
  - A human-sounding email is far more likely to get a placement

Each email:
  - Mentions the curator/station by name
  - References their specific genre focus
  - Includes the Spotify link prominently
  - Is short and professional (under 200 words)
  - Does NOT sound like a bot or template blast

Claude uses adaptive thinking to craft each message thoughtfully.
"""

import logging
import os
import anthropic

logger = logging.getLogger(__name__)

# Client is created on first use (not at import time) so that the .env file
# has already been loaded before we try to read ANTHROPIC_API_KEY.
_client = None


def _get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    return _client


def generate_pitch(
    contact: dict,
    release: dict,
    artist_bio: str,
) -> dict:
    """
    Generate a personalised pitch email for one contact about one release.

    Args:
        contact:    A contact dict from contacts.py (name, type, genre_focus, etc.)
        release:    A release dict from spotify_checker.py (name, type, spotify_url, etc.)
        artist_bio: A short bio of the artist to give Claude context.

    Returns:
        A dict with:
          {
            "subject": "Email subject line",
            "body":    "Full email body text",
          }
    """

    # Map Spotify's release type to a human-readable word
    release_type_label = {
        "album": "album",
        "single": "single",
        "ep": "EP",
        "compilation": "compilation",
    }.get(release.get("type", "single"), "release")

    # Build the prompt we send to Claude
    prompt = f"""
You are helping an independent music artist reach out to playlist curators,
music blogs, and radio stations about their new release.

ARTIST INFO:
- Artist name: moodmixformat
- Bio: {artist_bio}

NEW RELEASE:
- Title: {release['name']}
- Type: {release_type_label}
- Released: {release.get('release_date', 'recently')}
- Link: {release['spotify_url']}
- Number of tracks: {release.get('total_tracks', 1)}

CONTACT TO PITCH:
- Name: {contact['name']}
- Type: {contact['type'].replace('_', ' ')}
- Genre focus: {contact.get('genre_focus', 'various genres')}
- Notes about them: {contact.get('notes', 'N/A')}

TASK:
Write a short, genuine, personalised pitch email from moodmixformat to {contact['name']}.

Requirements:
- Subject line: plain and direct, mentions the release title — no hype or clickbait
- Body: 100-150 words maximum — keep it short
- One brief line showing you know who they are (don't overdo it)
- One or two sentences on the track's sound/vibe — reference the influences naturally, not as a sales pitch
- Include the link
- End simply — no "I would be honoured" or "it would mean the world" type language
- Sound like a person sending an email, not a PR campaign
- Do NOT use phrases like "I hope this email finds you well", "thrilled to share", "excited to announce", "I'd love for you to", or any hype language
- Do NOT oversell — let the music speak, just give them enough context to decide if it's worth a listen
- Do NOT use exclamation marks

Return ONLY a JSON object in this exact format (no markdown, no extra text):
{{
  "subject": "the email subject line here",
  "body": "the full email body here"
}}
"""

    logger.info(
        "Generating pitch for contact '%s' about release '%s'...",
        contact['name'],
        release['name'],
    )

    # Call Claude with adaptive thinking for thoughtful personalisation
    response = _get_client().messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        thinking={"type": "adaptive"},
        messages=[{"role": "user", "content": prompt}],
    )

    # Extract the text response
    raw_text = ""
    for block in response.content:
        if block.type == "text":
            raw_text = block.text.strip()
            break

    # Parse the JSON response
    import json
    try:
        # Strip any accidental markdown code fences Claude might add
        if raw_text.startswith("```"):
            raw_text = raw_text.split("```")[1]
            if raw_text.startswith("json"):
                raw_text = raw_text[4:]

        pitch = json.loads(raw_text)

        # Validate the keys we need exist
        assert "subject" in pitch, "Missing 'subject' key in Claude response"
        assert "body" in pitch, "Missing 'body' key in Claude response"

        logger.info("Pitch generated successfully for '%s'", contact['name'])
        return pitch

    except (json.JSONDecodeError, AssertionError) as e:
        # If Claude's response isn't valid JSON, fall back to a safe default
        logger.error("Failed to parse Claude pitch response: %s\nRaw: %s", e, raw_text)
        return {
            "subject": f"New {release_type_label}: {release['name']} — moodmixformat",
            "body": (
                f"Hi {contact['name']},\n\n"
                f"I just released a new {release_type_label} called '{release['name']}' "
                f"and thought it might be a good fit for your {contact.get('genre_focus', 'playlist')}.\n\n"
                f"Listen here: {release['spotify_url']}\n\n"
                f"Thanks for your time,\nmoodmixformat"
            ),
        }


def generate_pitches_for_release(
    release: dict,
    contacts: list[dict],
    artist_bio: str,
) -> list[dict]:
    """
    Generate pitches for ALL contacts about a single release.

    Returns a list of dicts, each with:
      {
        "contact": { ...contact dict... },
        "subject": "Email subject",
        "body":    "Email body",
      }
    """
    results = []
    total = len(contacts)

    for i, contact in enumerate(contacts, 1):
        logger.info("Generating pitch %d/%d for %s", i, total, contact['name'])
        try:
            pitch = generate_pitch(contact, release, artist_bio)
            results.append({
                "contact": contact,
                "subject": pitch["subject"],
                "body": pitch["body"],
            })
        except Exception as e:
            logger.error("Error generating pitch for %s: %s", contact['name'], e)
            # Skip this contact and continue with the rest
            continue

    logger.info("Generated %d/%d pitches successfully", len(results), total)
    return results
