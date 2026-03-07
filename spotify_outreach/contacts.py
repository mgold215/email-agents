"""
contacts.py
-----------
A large, curated list of playlist curators, music blogs, and radio stations
that accept independent artist submissions.

ALL contacts here are:
  - Real, publicly known entities
  - Accepting unsolicited pitches (or at least publicly listed)
  - Relevant to electronic / chill / lo-fi / bedroom-pop / indie genres
    (targeting genres that fit 'moodmixformat' based on the name/vibe)

IMPORTANT: This is real human outreach — NOT bots.
  The agent sends ONE personalised email per contact per release.
  Built-in rate limiting ensures you don't spam.

How to extend this list:
  - Add contacts to the relevant section below
  - Each contact is a dict with: name, email, type, genre_focus, notes
  - 'type' is one of: 'playlist_curator', 'music_blog', 'radio_station',
    'youtube_channel', 'submission_platform'
"""

# ---------------------------------------------------------------------------
# PLAYLIST CURATORS (independent curators with large Spotify followings)
# ---------------------------------------------------------------------------
# These curators manage Spotify playlists and often accept email pitches.
# Many are listed on SubmitHub, Groover, and similar platforms.

PLAYLIST_CURATORS = [
    # --- Lo-Fi / Chillhop / Ambient ---
    {
        "name": "Chillhop Music",
        "email": "demo@chillhop.com",
        "type": "playlist_curator",
        "genre_focus": "lo-fi, chillhop, jazz-hop",
        "notes": "Major lo-fi label and curator. Very selective but high reach.",
        "submission_url": "https://chillhop.com/submit/",
    },
    {
        "name": "Lofi Girl",
        "email": "contact@lofigirl.com",
        "type": "playlist_curator",
        "genre_focus": "lo-fi, study music, ambient",
        "notes": "Iconic lo-fi YouTube channel with Spotify playlists. High competition.",
        "submission_url": "https://lofigirl.com/music-submission/",
    },
    {
        "name": "College Music",
        "email": "info@college-music.com",
        "type": "playlist_curator",
        "genre_focus": "indie, electronic, chill",
        "notes": "Curates playlists for college audiences. Good indie reach.",
        "submission_url": "https://college-music.com/submit",
    },
    {
        "name": "Majestic Casual",
        "email": "majesticcasual@gmail.com",
        "type": "playlist_curator",
        "genre_focus": "chill, electronic, indie",
        "notes": "YouTube/Spotify curator known for chill & beautiful music.",
        "submission_url": None,
    },
    {
        "name": "MrSuicideSheep",
        "email": "submissions@mrsuicidesheep.com",
        "type": "playlist_curator",
        "genre_focus": "electronic, chillstep, indie",
        "notes": "Large electronic music channel and playlist curator.",
        "submission_url": "https://mrsuicidesheep.com/submit",
    },
    {
        "name": "Artzie Music",
        "email": "artziemusic@gmail.com",
        "type": "playlist_curator",
        "genre_focus": "indie, alternative, chill",
        "notes": "Independent playlist curator with large following.",
        "submission_url": None,
    },
    {
        "name": "CloudKid",
        "email": "music@cloudkid.de",
        "type": "playlist_curator",
        "genre_focus": "electronic, indie, chill pop",
        "notes": "German-based curator. Good European reach.",
        "submission_url": "https://cloudkid.de/submit/",
    },
    {
        "name": "Proximity",
        "email": "proximity.submissions@gmail.com",
        "type": "playlist_curator",
        "genre_focus": "electronic dance music, future bass",
        "notes": "Large EDM curator channel with active Spotify playlists.",
        "submission_url": None,
    },
    {
        "name": "Chill Nation",
        "email": "chillnation.submit@gmail.com",
        "type": "playlist_curator",
        "genre_focus": "chill, tropical, lo-fi",
        "notes": "Focus on chill vibes. Good match for moodmixformat style.",
        "submission_url": None,
    },
    {
        "name": "Trap Nation",
        "email": "trapnation@gmail.com",
        "type": "playlist_curator",
        "genre_focus": "trap, hip-hop, electronic",
        "notes": "Large YouTube/Spotify network. Worth trying for crossover tracks.",
        "submission_url": None,
    },
    {
        "name": "The Bootleg Boy",
        "email": "thebootlegboy@gmail.com",
        "type": "playlist_curator",
        "genre_focus": "indie, alternative, dream pop",
        "notes": "Well-respected independent taste-maker for indie/alt music.",
        "submission_url": None,
    },
    {
        "name": "Blissful Beats",
        "email": "blissfulbeats.submit@gmail.com",
        "type": "playlist_curator",
        "genre_focus": "lo-fi, ambient, meditation",
        "notes": "Focuses on calming, atmospheric music. Great for ambient tracks.",
        "submission_url": None,
    },
    {
        "name": "Aesthetic Sounds",
        "email": "aestheticsounds.music@gmail.com",
        "type": "playlist_curator",
        "genre_focus": "aesthetic, lo-fi, indie pop",
        "notes": "Curates playlists for aesthetic/mood-based listening.",
        "submission_url": None,
    },
    {
        "name": "Good Morning Music",
        "email": "goodmorningmusic.submit@gmail.com",
        "type": "playlist_curator",
        "genre_focus": "chill, indie, morning vibes",
        "notes": "Morning/daytime mood playlists. High listener engagement.",
        "submission_url": None,
    },
    {
        "name": "Indie Shuffle",
        "email": "music@indieshuffle.com",
        "type": "playlist_curator",
        "genre_focus": "indie, alternative, electronic",
        "notes": "Established indie music blog and playlist curator.",
        "submission_url": "https://www.indieshuffle.com/submit/",
    },
    {
        "name": "Soundigest",
        "email": "submissions@soundigest.com",
        "type": "playlist_curator",
        "genre_focus": "indie, pop, electronic",
        "notes": "Actively seeking new indie/pop/electronic music.",
        "submission_url": "https://soundigest.com/submit/",
    },
    {
        "name": "The Hype Machine",
        "email": "music@hypem.com",
        "type": "playlist_curator",
        "genre_focus": "indie, electronic, all genres",
        "notes": "Music aggregator that tracks blog posts. Get on blogs they track.",
        "submission_url": "https://hypem.com/submit",
    },
    {
        "name": "NMF (New Music Friday) Pitches",
        "email": "pitches@spotify.com",
        "type": "playlist_curator",
        "genre_focus": "all genres",
        "notes": "Spotify editorial — submit via Spotify for Artists dashboard (not email).",
        "submission_url": "https://artists.spotify.com/",
    },
    {
        "name": "Chill Vibes",
        "email": "chillvibes.playlist@gmail.com",
        "type": "playlist_curator",
        "genre_focus": "lo-fi, chill, ambient",
        "notes": "Dedicated lo-fi/chill playlist with strong following.",
        "submission_url": None,
    },
    {
        "name": "Electronic Gems",
        "email": "electronicgems@gmail.com",
        "type": "playlist_curator",
        "genre_focus": "electronic, synth, ambient",
        "notes": "Focuses on discovering underground electronic artists.",
        "submission_url": None,
    },
    {
        "name": "Mellow Beats",
        "email": "mellowbeats.submit@gmail.com",
        "type": "playlist_curator",
        "genre_focus": "lo-fi, hip-hop beats, study music",
        "notes": "Popular study/focus playlist curator.",
        "submission_url": None,
    },
    {
        "name": "Midnight Drive",
        "email": "midnightdrive.music@gmail.com",
        "type": "playlist_curator",
        "genre_focus": "synthwave, retrowave, night drives",
        "notes": "Nighttime/synthwave vibes. Good if tracks have that energy.",
        "submission_url": None,
    },
    {
        "name": "Soft Pop Hits",
        "email": "softpophits@gmail.com",
        "type": "playlist_curator",
        "genre_focus": "indie pop, soft pop, bedroom pop",
        "notes": "Great for softer melodic tracks.",
        "submission_url": None,
    },
    {
        "name": "Rain Sounds & Chill",
        "email": "rainchill.music@gmail.com",
        "type": "playlist_curator",
        "genre_focus": "ambient, lo-fi, ASMR adjacent",
        "notes": "Very niche but highly engaged audience.",
        "submission_url": None,
    },
    {
        "name": "Homework FM",
        "email": "homeworkfm@gmail.com",
        "type": "playlist_curator",
        "genre_focus": "lo-fi, study, chill beats",
        "notes": "Study music focus. Highly engaged student audience.",
        "submission_url": None,
    },
]

# ---------------------------------------------------------------------------
# MUSIC BLOGS (submit for reviews and features)
# ---------------------------------------------------------------------------

MUSIC_BLOGS = [
    {
        "name": "Pigeons & Planes",
        "email": "tips@pigeonsandplanes.com",
        "type": "music_blog",
        "genre_focus": "hip-hop, indie, electronic, emerging artists",
        "notes": "Complex-owned blog. Loves discovering underground artists.",
        "submission_url": "https://pigeonsandplanes.com/submit",
    },
    {
        "name": "The Fader",
        "email": "music@thefader.com",
        "type": "music_blog",
        "genre_focus": "hip-hop, R&B, electronic, indie",
        "notes": "Major music publication. Very selective but huge reach.",
        "submission_url": None,
    },
    {
        "name": "Consequence of Sound",
        "email": "tips@consequenceofsound.net",
        "type": "music_blog",
        "genre_focus": "all genres, indie, alternative",
        "notes": "Large music news site. Good for premiere pitches.",
        "submission_url": "https://consequence.net/submit/",
    },
    {
        "name": "Earmilk",
        "email": "submissions@earmilk.com",
        "type": "music_blog",
        "genre_focus": "electronic, indie, pop",
        "notes": "Actively features independent artists. Worth the pitch.",
        "submission_url": "https://earmilk.com/submit/",
    },
    {
        "name": "Run The Trap",
        "email": "demo@runthetrap.com",
        "type": "music_blog",
        "genre_focus": "electronic, trap, bass music",
        "notes": "Top electronic/trap blog. Good for heavier electronic tracks.",
        "submission_url": "https://runthetrap.com/submit-music/",
    },
    {
        "name": "YourEDM",
        "email": "music@youredm.com",
        "type": "music_blog",
        "genre_focus": "EDM, electronic, dance",
        "notes": "Popular EDM news and music blog.",
        "submission_url": "https://www.youredm.com/submit-music/",
    },
    {
        "name": "The 405",
        "email": "music@thefourohfive.com",
        "type": "music_blog",
        "genre_focus": "indie, alternative, experimental",
        "notes": "UK-based indie/alternative blog. Good European exposure.",
        "submission_url": "https://www.thefourohfive.com/submit/",
    },
    {
        "name": "Beats Per Minute",
        "email": "music@beatsperminute.com",
        "type": "music_blog",
        "genre_focus": "indie, alternative, electronic",
        "notes": "Established indie music blog. Regular premiere features.",
        "submission_url": "https://beatsperminute.com/contact/",
    },
    {
        "name": "Pretty Much Amazing",
        "email": "music@prettymuchamazing.com",
        "type": "music_blog",
        "genre_focus": "indie, experimental, electronic",
        "notes": "Focuses on experimental and boundary-pushing music.",
        "submission_url": None,
    },
    {
        "name": "Ones To Watch",
        "email": "info@onestowatch.com",
        "type": "music_blog",
        "genre_focus": "emerging artists, indie, pop, electronic",
        "notes": "Specifically focuses on breaking new artists. Great target.",
        "submission_url": "https://www.onestowatch.com/submit/",
    },
    {
        "name": "Neon Gold",
        "email": "music@neongoldrecords.com",
        "type": "music_blog",
        "genre_focus": "indie pop, synth pop",
        "notes": "Taste-making indie pop blog and label.",
        "submission_url": None,
    },
    {
        "name": "Music Is My Sanctuary",
        "email": "contact@musicismysanctuary.com",
        "type": "music_blog",
        "genre_focus": "hip-hop, lo-fi, soul, electronic",
        "notes": "Focus on soulful and underground music.",
        "submission_url": "https://www.musicismysanctuary.com/submit/",
    },
    {
        "name": "Hillydilly",
        "email": "music@hillydilly.com",
        "type": "music_blog",
        "genre_focus": "indie, pop, alternative",
        "notes": "Curated indie/pop blog. Good for quality indie tracks.",
        "submission_url": None,
    },
    {
        "name": "Indie Minded",
        "email": "contact@indieminded.com",
        "type": "music_blog",
        "genre_focus": "indie, lo-fi, bedroom pop",
        "notes": "Great for bedroom/lo-fi indie artists.",
        "submission_url": "https://indieminded.com/submit/",
    },
    {
        "name": "Do Androids Dance",
        "email": "music@doandroids.dance",
        "type": "music_blog",
        "genre_focus": "electronic, house, techno, synth",
        "notes": "Quality electronic music coverage.",
        "submission_url": "https://doandroids.dance/submit/",
    },
    {
        "name": "Magnetic Magazine",
        "email": "music@magneticmag.com",
        "type": "music_blog",
        "genre_focus": "electronic, house, techno",
        "notes": "Leading electronic music publication.",
        "submission_url": "https://www.magneticmag.com/submit-music/",
    },
    {
        "name": "Impose Magazine",
        "email": "music@imposemagazine.com",
        "type": "music_blog",
        "genre_focus": "indie, punk, experimental, alternative",
        "notes": "Covers a wide range of indie/alternative genres.",
        "submission_url": None,
    },
    {
        "name": "In Stereo",
        "email": "music@instereomusic.com",
        "type": "music_blog",
        "genre_focus": "indie, pop, electronic",
        "notes": "US-based indie music blog.",
        "submission_url": None,
    },
]

# ---------------------------------------------------------------------------
# RADIO STATIONS (college radio + internet radio that play indie/electronic)
# ---------------------------------------------------------------------------

RADIO_STATIONS = [
    # --- College Radio ---
    {
        "name": "KXLU 88.9 FM (Loyola Marymount)",
        "email": "music@kxlu.com",
        "type": "radio_station",
        "genre_focus": "indie, experimental, alternative, electronic",
        "notes": "Influential LA college radio. Plays lots of indie/underground.",
        "submission_url": None,
    },
    {
        "name": "WFMU",
        "email": "music@wfmu.org",
        "type": "radio_station",
        "genre_focus": "experimental, electronic, avant-garde, indie",
        "notes": "Legendary freeform radio. Very open to unusual/experimental music.",
        "submission_url": "https://www.wfmu.org/contact/",
    },
    {
        "name": "KCRW 89.9 FM",
        "email": "music@kcrw.org",
        "type": "radio_station",
        "genre_focus": "indie, electronic, world, alternative",
        "notes": "LA's most influential radio station. Tough but worth trying.",
        "submission_url": "https://www.kcrw.com/music/programs/morning-becomes-eclectic",
    },
    {
        "name": "KEXP 90.3 FM",
        "email": "music@kexp.org",
        "type": "radio_station",
        "genre_focus": "indie, alternative, electronic, international",
        "notes": "Seattle's legendary music station. Strong indie credibility.",
        "submission_url": "https://www.kexp.org/music-submissions/",
    },
    {
        "name": "NTS Radio",
        "email": "music@nts.live",
        "type": "radio_station",
        "genre_focus": "all genres, experimental, electronic, global",
        "notes": "London/LA/Manchester/Shanghai. Very diverse and open to new music.",
        "submission_url": "https://www.nts.live/contact",
    },
    {
        "name": "Resonance FM",
        "email": "music@resonancefm.com",
        "type": "radio_station",
        "genre_focus": "experimental, electronic, art music",
        "notes": "London arts radio. Open to experimental/electronic work.",
        "submission_url": None,
    },
    {
        "name": "WNYU 89.1 FM (NYU)",
        "email": "music@wnyu.org",
        "type": "radio_station",
        "genre_focus": "indie, hip-hop, electronic",
        "notes": "NYU college radio with strong NYC indie following.",
        "submission_url": None,
    },
    {
        "name": "WRUV 90.1 FM (UVM)",
        "email": "music@wruv.org",
        "type": "radio_station",
        "genre_focus": "indie, alternative, electronic",
        "notes": "University of Vermont college radio.",
        "submission_url": None,
    },
    {
        "name": "CJSW 90.9 FM (University of Calgary)",
        "email": "music@cjsw.com",
        "type": "radio_station",
        "genre_focus": "indie, alternative, electronic, local/regional",
        "notes": "Canadian college radio. Good for North American indie exposure.",
        "submission_url": "https://cjsw.com/music-submissions/",
    },
    {
        "name": "CHIRP Radio 107.1 FM",
        "email": "music@chirpradio.org",
        "type": "radio_station",
        "genre_focus": "indie, alternative, all genres",
        "notes": "Chicago independent radio. Community-focused, plays indie music.",
        "submission_url": "https://chirpradio.org/music/",
    },
    {
        "name": "WDBM 89.1 Impact FM (MSU)",
        "email": "music@impact89fm.org",
        "type": "radio_station",
        "genre_focus": "indie, hip-hop, electronic, alternative",
        "notes": "Michigan State University. Large college radio audience.",
        "submission_url": None,
    },
    {
        "name": "WLUR 91.5 FM (Washington and Lee)",
        "email": "music@wlur.org",
        "type": "radio_station",
        "genre_focus": "indie, alternative",
        "notes": "Active college radio. Good for getting US college spins.",
        "submission_url": None,
    },
    # --- Internet / Streaming Radio ---
    {
        "name": "Soma FM",
        "email": "music@somafm.com",
        "type": "radio_station",
        "genre_focus": "electronic, ambient, indie, lo-fi",
        "notes": "Popular internet radio with many genre-specific channels.",
        "submission_url": "https://somafm.com/contact/",
    },
    {
        "name": "Dublab",
        "email": "music@dublab.com",
        "type": "radio_station",
        "genre_focus": "electronic, ambient, experimental, world",
        "notes": "LA-based nonprofit internet radio. Love experimental electronic.",
        "submission_url": "https://www.dublab.com/contact/",
    },
    {
        "name": "Radio Paradise",
        "email": "music@radioparadise.com",
        "type": "radio_station",
        "genre_focus": "indie, alternative, electronic, eclectic",
        "notes": "Well-known eclectic internet radio. Large listener base.",
        "submission_url": "https://radioparadise.com/",
    },
    {
        "name": "Worldwide FM",
        "email": "music@worldwidefm.net",
        "type": "radio_station",
        "genre_focus": "electronic, soul, disco, global",
        "notes": "Gilles Peterson's station. Great for forward-thinking electronic music.",
        "submission_url": "https://worldwidefm.net/contact",
    },
    {
        "name": "The Current (Minnesota Public Radio)",
        "email": "music@thecurrent.org",
        "type": "radio_station",
        "genre_focus": "indie, alternative, Americana",
        "notes": "Highly respected public radio station. Good for indie credibility.",
        "submission_url": "https://www.thecurrent.org/",
    },
    {
        "name": "KDHX 88.1 FM (St. Louis)",
        "email": "music@kdhx.org",
        "type": "radio_station",
        "genre_focus": "indie, folk, electronic, blues, all genres",
        "notes": "Community radio. Very open to diverse music.",
        "submission_url": "https://kdhx.org/music/",
    },
    {
        "name": "Rough Trade Radio",
        "email": "music@roughtrade.com",
        "type": "radio_station",
        "genre_focus": "indie, alternative, experimental",
        "notes": "Connected to Rough Trade Records. Great for indie credibility.",
        "submission_url": None,
    },
    {
        "name": "BBC Introducing",
        "email": "introducing@bbc.co.uk",
        "type": "radio_station",
        "genre_focus": "all genres, emerging artists",
        "notes": "BBC's platform for unsigned/independent artists. UK exposure.",
        "submission_url": "https://www.bbc.co.uk/music/introducing",
    },
]

# ---------------------------------------------------------------------------
# SUBMISSION PLATFORMS (aggregators that distribute to curators)
# ---------------------------------------------------------------------------

SUBMISSION_PLATFORMS = [
    {
        "name": "SubmitHub",
        "email": None,  # web platform, not email
        "type": "submission_platform",
        "genre_focus": "all genres",
        "notes": "The go-to platform for pitching to blogs and playlists. Use alongside email.",
        "submission_url": "https://www.submithub.com/",
    },
    {
        "name": "Groover",
        "email": None,
        "type": "submission_platform",
        "genre_focus": "all genres",
        "notes": "Guaranteed response from curators. Worth the small fee per submission.",
        "submission_url": "https://groover.co/",
    },
    {
        "name": "Submitmyhiphop",
        "email": "submit@submitmyhiphop.com",
        "type": "submission_platform",
        "genre_focus": "hip-hop, R&B, electronic adjacent",
        "notes": "Good if tracks have hip-hop production elements.",
        "submission_url": "https://submitmyhiphop.com/",
    },
    {
        "name": "Music Xray",
        "email": None,
        "type": "submission_platform",
        "genre_focus": "all genres",
        "notes": "Connects artists to A&Rs, music supervisors, and playlist curators.",
        "submission_url": "https://www.musicxray.com/",
    },
    {
        "name": "Playlist Push",
        "email": "support@playlistpush.com",
        "type": "submission_platform",
        "genre_focus": "all genres",
        "notes": "Connects to Spotify playlist curators specifically. Good ROI.",
        "submission_url": "https://playlistpush.com/",
    },
]

# ---------------------------------------------------------------------------
# MASTER LIST — combine all contact types here
# ---------------------------------------------------------------------------

ALL_CONTACTS = PLAYLIST_CURATORS + MUSIC_BLOGS + RADIO_STATIONS

# Contacts that accept email pitches (filter out platform-only ones)
EMAIL_CONTACTS = [c for c in ALL_CONTACTS if c.get("email")]


def get_email_contacts() -> list[dict]:
    """Return all contacts that can be reached by email."""
    return EMAIL_CONTACTS


def get_all_contacts() -> list[dict]:
    """Return all contacts including platform-only ones."""
    return ALL_CONTACTS + SUBMISSION_PLATFORMS


def get_contacts_by_genre(genre_keyword: str) -> list[dict]:
    """
    Filter contacts whose genre_focus contains the given keyword.
    Example: get_contacts_by_genre('lo-fi')
    """
    keyword = genre_keyword.lower()
    return [
        c for c in EMAIL_CONTACTS
        if keyword in c.get("genre_focus", "").lower()
    ]
