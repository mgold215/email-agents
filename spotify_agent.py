"""
Spotify Track Email Agent
-------------------------
Takes a Spotify track link, uses Claude with web_fetch to read the page,
and generates a promotional email for the song.

Setup required:
  - ANTHROPIC_API_KEY: Your Anthropic API key

All agent actions are logged to agent_actions.log for audit trail.
"""

import sys
import logging
import os
from datetime import datetime
import anthropic

# Audit log — required by project conventions
logging.basicConfig(
    filename="agent_actions.log",
    level=logging.INFO,
    format="%(asctime)s [AGENT] %(message)s"
)


def run_spotify_agent(spotify_url: str):
    """
    Give Claude the Spotify link and the web_fetch tool.
    Claude fetches the page, reads the track info, and writes a promo email.
    """
    logging.info(f"Agent started. URL: {spotify_url}")
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Spotify Email Agent starting...")
    print(f"Track URL: {spotify_url}\n")

    # Load API key from environment — never hardcoded
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY environment variable is not set.")
        print("  export ANTHROPIC_API_KEY=your_key")
        logging.error("Missing ANTHROPIC_API_KEY")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    print("Fetching track info and generating promotional email...\n")
    logging.info("Sending request to Claude with web_fetch tool")

    # Stream the response so we see output as it's generated
    with client.messages.stream(
        model="claude-opus-4-6",
        max_tokens=1024,
        system=(
            "You are a music promotion copywriter. When given a Spotify link:\n"
            "1. Use web_fetch to visit the page and find the song title and artist.\n"
            "2. Write a short, genuine promotional email in first person from the artist. Use this exact structure:\n\n"
            "Subject: [artist name] — '[track title]' (new track)\n\n"
            "Hey [Name],\n\n"
            "I just put out a new track called '[title]' — tech house with a melodic techno edge. "
            "It's one that begs for replays and stays stuck in your head.\n\n"
            "Would love it if you'd add it to your playlist: [hyperlink the Spotify URL with text '[title] by [artist]']\n\n"
            "Happy to send over more info if useful.\n\n"
            "Thanks,\n[artist name]\n\n"
            "Keep it understated, genuine, and short. No hype. First person from the artist."
        ),
        tools=[{"type": "web_fetch_20260209", "name": "web_fetch"}],
        messages=[
            {
                "role": "user",
                "content": (
                    f"Please fetch this Spotify track page and write a promotional email for the song:\n\n"
                    f"{spotify_url}"
                )
            }
        ]
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)

    print("\n")
    logging.info("Agent completed successfully")
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Done. Actions logged to agent_actions.log")


if __name__ == "__main__":
    url = (
        sys.argv[1] if len(sys.argv) > 1
        else "https://open.spotify.com/track/3NMZENmh8Ji1Qb1XjFNaH7?si=iaYccm0WRFiVv5EcspSjQA"
    )
    run_spotify_agent(url)
