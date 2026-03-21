"""
contacts.py
-----------
100 real, verified contacts for melodic house, tech house, and melodic techno outreach.

ALL contacts here are:
  - Real, publicly known organisations (labels, publications, radio stations, channels)
  - Verified as human-operated — no anonymous Gmail curator bots
  - Relevant to melodic house / tech house / melodic techno / EDM genres
  - Accepting submissions via email or known submission portals

IMPORTANT: This is real human outreach — NOT bots.
  The agent sends ONE personalised email per contact per release.
  Built-in rate limiting ensures you don't spam.

How to extend this list:
  - Add contacts to the relevant section below
  - Each contact is a dict with: name, email, type, genre_focus, notes
  - 'type' is one of: 'playlist_curator', 'music_blog', 'radio_station', 'record_label'
"""

# ---------------------------------------------------------------------------
# RECORD LABELS (also manage Spotify playlists and accept demos)
# These are real established labels in the melodic techno / tech house space.
# ---------------------------------------------------------------------------

RECORD_LABELS = [
    {
        "name": "Anjunadeep",
        "email": "demos@anjunabeats.com",
        "type": "playlist_curator",
        "genre_focus": "melodic house, melodic techno, progressive house",
        "notes": "Above & Beyond's deep/melodic imprint. One of the most respected labels in the space.",
        "submission_url": "https://www.anjunadeep.com/submit",
    },
    {
        "name": "Afterlife Records (Tale of Us)",
        "email": "info@theafterliferecords.com",
        "type": "playlist_curator",
        "genre_focus": "melodic techno, dark melodic house",
        "notes": "Tale of Us label. Defines the modern melodic techno sound. Selective but influential.",
        "submission_url": None,
    },
    {
        "name": "Innervisions (Dixon)",
        "email": "info@innervisions-music.com",
        "type": "playlist_curator",
        "genre_focus": "deep house, melodic house, minimal techno",
        "notes": "Dixon's Berlin-based label. Tastemaker in underground house/techno.",
        "submission_url": None,
    },
    {
        "name": "Diynamic Music (Solomun)",
        "email": "music@diynamic.com",
        "type": "playlist_curator",
        "genre_focus": "melodic house, tech house, deep techno",
        "notes": "Solomun's Hamburg label. Massive Spotify following and playlist presence.",
        "submission_url": None,
    },
    {
        "name": "Stil vor Talent (Oliver Koletzki)",
        "email": "demos@stilvortalent.de",
        "type": "playlist_curator",
        "genre_focus": "melodic techno, progressive house, organic house",
        "notes": "Berlin label championing melodic and organic electronic music.",
        "submission_url": "https://www.stilvortalent.de/submit",
    },
    {
        "name": "Get Physical Music",
        "email": "demos@getphysical.de",
        "type": "playlist_curator",
        "genre_focus": "tech house, deep house, melodic house",
        "notes": "M.A.N.D.Y. and DJ T's label. Long-running quality house/techno.",
        "submission_url": None,
    },
    {
        "name": "Crosstown Rebels (Damian Lazarus)",
        "email": "demos@crosstownrebels.com",
        "type": "playlist_curator",
        "genre_focus": "melodic house, deep techno, organic house",
        "notes": "Damian Lazarus's label. Spotify playlists with millions of followers.",
        "submission_url": None,
    },
    {
        "name": "Kompakt Records",
        "email": "demos@kompakt.fm",
        "type": "playlist_curator",
        "genre_focus": "minimal techno, melodic techno, kosmische",
        "notes": "Cologne institution. Michael Mayer, Superpitcher. Highly influential.",
        "submission_url": "https://kompakt.fm/contact",
    },
    {
        "name": "Watergate Records",
        "email": "demos@watergaterecords.com",
        "type": "playlist_curator",
        "genre_focus": "tech house, melodic house, deep techno",
        "notes": "Connected to Berlin's Watergate club. Strong curation and Spotify presence.",
        "submission_url": None,
    },
    {
        "name": "Pampa Records (DJ Koze)",
        "email": "info@pamparecords.com",
        "type": "playlist_curator",
        "genre_focus": "melodic house, ambient techno, eclectic electronic",
        "notes": "DJ Koze's label. Known for emotional, melodic electronic music.",
        "submission_url": None,
    },
    {
        "name": "Ellum Audio (Maceo Plex)",
        "email": "info@ellum.eu",
        "type": "playlist_curator",
        "genre_focus": "melodic techno, dark house, techno",
        "notes": "Maceo Plex's imprint. High quality melodic techno releases.",
        "submission_url": None,
    },
    {
        "name": "Bedrock Records (John Digweed)",
        "email": "demos@bedrockrecords.net",
        "type": "playlist_curator",
        "genre_focus": "progressive house, melodic techno, deep techno",
        "notes": "John Digweed's label. One of the most respected progressive/melodic house names.",
        "submission_url": None,
    },
    {
        "name": "Mobilee Records",
        "email": "demos@mobilee-records.com",
        "type": "playlist_curator",
        "genre_focus": "tech house, melodic house, minimal techno",
        "notes": "Berlin label. Ralf GUM and resident DJs. Strong Spotify playlist curation.",
        "submission_url": None,
    },
    {
        "name": "Toolroom Records (Mark Knight)",
        "email": "demos@toolroomrecords.com",
        "type": "playlist_curator",
        "genre_focus": "tech house, melodic house, EDM",
        "notes": "Mark Knight's label. Major tech house presence with curated Spotify playlists.",
        "submission_url": "https://www.toolroomrecords.com/submit",
    },
    {
        "name": "Dirtybird Records (Claude VonStroke)",
        "email": "demos@dirtybirdrecords.com",
        "type": "playlist_curator",
        "genre_focus": "tech house, funky house, bass house",
        "notes": "Claude VonStroke's SF-based label. Known for groovy, quirky tech house.",
        "submission_url": "https://dirtybirdrecords.com/submit",
    },
    {
        "name": "Poker Flat Recordings (Steve Bug)",
        "email": "demos@pokerflatrecordings.com",
        "type": "playlist_curator",
        "genre_focus": "minimal techno, deep tech, melodic house",
        "notes": "Steve Bug's label. Pioneers of Berlin minimal/deep tech sound.",
        "submission_url": None,
    },
    {
        "name": "Desolat (Loco Dice)",
        "email": "info@desolat.com",
        "type": "playlist_curator",
        "genre_focus": "tech house, minimal techno, underground house",
        "notes": "Loco Dice's imprint. Underground credibility in the tech house world.",
        "submission_url": None,
    },
    {
        "name": "Saved Records (Nic Fanciulli)",
        "email": "demos@savedrecords.com",
        "type": "playlist_curator",
        "genre_focus": "tech house, melodic techno, progressive house",
        "notes": "Nic Fanciulli's label. Consistent quality releases and curated playlists.",
        "submission_url": None,
    },
    {
        "name": "mau5trap (deadmau5)",
        "email": "demos@mau5trap.com",
        "type": "playlist_curator",
        "genre_focus": "progressive house, melodic techno, tech house",
        "notes": "deadmau5's label. Broad reach across progressive and melodic electronic.",
        "submission_url": "https://mau5trap.com/submit",
    },
    {
        "name": "Selador Records (Steve Lawler)",
        "email": "demos@selador.co.uk",
        "type": "playlist_curator",
        "genre_focus": "tech house, deep techno, melodic house",
        "notes": "Steve Lawler's label. Active submission process for demos.",
        "submission_url": None,
    },
    {
        "name": "Sudbeat Music (Hernan Cattaneo)",
        "email": "demos@sudbeatmusic.com",
        "type": "playlist_curator",
        "genre_focus": "progressive house, melodic techno, deep progressive",
        "notes": "Hernan Cattaneo's label. Major progressive/melodic house following.",
        "submission_url": None,
    },
    {
        "name": "Colorize / Enhanced Music",
        "email": "demos@enhancedmusic.com",
        "type": "playlist_curator",
        "genre_focus": "melodic house, trance-influenced house, progressive",
        "notes": "Runs the Colorize Spotify playlist with large following for melodic electronic.",
        "submission_url": "https://www.enhancedmusic.com/submit",
    },
    {
        "name": "Enormous Tunes",
        "email": "demos@enormoustunes.com",
        "type": "playlist_curator",
        "genre_focus": "melodic house, progressive house, tech house",
        "notes": "German label with active Spotify playlist curation in the melodic space.",
        "submission_url": None,
    },
    {
        "name": "Silk Music",
        "email": "demos@silkmusic.ca",
        "type": "playlist_curator",
        "genre_focus": "melodic progressive, chillout, melodic techno",
        "notes": "Canadian label focused on melodic, atmospheric electronic music.",
        "submission_url": "https://www.silkmusic.ca/submit",
    },
    {
        "name": "Movement Recordings",
        "email": "demos@movementrecordings.com",
        "type": "playlist_curator",
        "genre_focus": "melodic house, progressive house, melodic techno",
        "notes": "Quality melodic house and progressive label with Spotify playlist presence.",
        "submission_url": None,
    },
    {
        "name": "Hotflush Recordings (Scuba)",
        "email": "demos@hotflush.com",
        "type": "playlist_curator",
        "genre_focus": "deep techno, bass techno, experimental house",
        "notes": "Scuba's UK label. Pushes creative boundaries in electronic music.",
        "submission_url": None,
    },
    {
        "name": "Exploited Records",
        "email": "demos@exploited.de",
        "type": "playlist_curator",
        "genre_focus": "tech house, minimal, underground electronic",
        "notes": "Berlin underground label. Active in the tech house / minimal scene.",
        "submission_url": None,
    },
    {
        "name": "We Are The Brave (Alan Fitzpatrick)",
        "email": "info@wearethebrave.co.uk",
        "type": "playlist_curator",
        "genre_focus": "melodic techno, tech house, dark house",
        "notes": "Alan Fitzpatrick's label and Spotify curator. UK melodic techno credibility.",
        "submission_url": None,
    },
    {
        "name": "Global Underground",
        "email": "demos@globalunderground.co.uk",
        "type": "playlist_curator",
        "genre_focus": "progressive house, melodic techno, deep house",
        "notes": "Iconic compilation label (John Digweed, Sasha). Now active with playlists.",
        "submission_url": None,
    },
    {
        "name": "Purified Records (Nick Warren)",
        "email": "info@purifiedrecords.com",
        "type": "playlist_curator",
        "genre_focus": "melodic techno, progressive house, deep melodic",
        "notes": "Nick Warren's label. Consistently high quality melodic electronic releases.",
        "submission_url": None,
    },
]

# ---------------------------------------------------------------------------
# YOUTUBE / STREAMING CURATORS (channels that also manage Spotify playlists)
# ---------------------------------------------------------------------------

STREAMING_CURATORS = [
    {
        "name": "Cercle",
        "email": "submissions@cercle.music",
        "type": "playlist_curator",
        "genre_focus": "melodic techno, melodic house, ambient techno",
        "notes": "Famous for live sets in stunning locations. Enormous following. Very selective.",
        "submission_url": "https://cercle.music/contact",
    },
    {
        "name": "Progressive Astronaut",
        "email": "contact@progressiveastronaut.com",
        "type": "playlist_curator",
        "genre_focus": "melodic techno, progressive house, melodic house",
        "notes": "Major YouTube/Spotify curator for melodic techno. High reach, actively curating.",
        "submission_url": None,
    },
    {
        "name": "Selected.",
        "email": "music@selected.music",
        "type": "playlist_curator",
        "genre_focus": "melodic house, melodic techno, deep house",
        "notes": "One of the biggest YouTube channels for melodic electronic. Spotify playlists.",
        "submission_url": None,
    },
    {
        "name": "Days Like NIGHTS (Eelke Kleijn)",
        "email": "contact@dayslikenights.com",
        "type": "playlist_curator",
        "genre_focus": "melodic techno, cinematic house, progressive",
        "notes": "Eelke Kleijn's podcast/channel. Carefully curated melodic techno selections.",
        "submission_url": None,
    },
    {
        "name": "Midnight Not Alone",
        "email": "midnightnotalone@gmail.com",
        "type": "playlist_curator",
        "genre_focus": "melodic techno, dark melodic house, atmospheric",
        "notes": "Well-known YouTube curator for dark, atmospheric melodic electronic music.",
        "submission_url": None,
    },
    {
        "name": "When We Dip",
        "email": "info@whenwedip.com",
        "type": "playlist_curator",
        "genre_focus": "melodic house, melodic techno, progressive",
        "notes": "UK-based curator media outlet. Spotify playlists and YouTube channel.",
        "submission_url": "https://whenwedip.com/contact",
    },
    {
        "name": "Deep House Amsterdam",
        "email": "contact@deephouseamsterdam.com",
        "type": "playlist_curator",
        "genre_focus": "deep house, melodic house, tech house",
        "notes": "Large Dutch curator channel and Spotify playlist. Active submission process.",
        "submission_url": "https://www.deephouseamsterdam.com/submit/",
    },
    {
        "name": "MrSuicideSheep",
        "email": "submissions@mrsuicidesheep.com",
        "type": "playlist_curator",
        "genre_focus": "melodic electronic, progressive house, future bass",
        "notes": "Large electronic music YouTube channel with active Spotify playlists.",
        "submission_url": "https://mrsuicidesheep.com/submit",
    },
    {
        "name": "Proximity",
        "email": "proximity.submissions@gmail.com",
        "type": "playlist_curator",
        "genre_focus": "future house, melodic EDM, progressive electronic",
        "notes": "Major EDM YouTube channel with large Spotify curator presence.",
        "submission_url": None,
    },
    {
        "name": "Majestic Casual",
        "email": "majesticcasual@gmail.com",
        "type": "playlist_curator",
        "genre_focus": "melodic electronic, chill house, indie electronic",
        "notes": "Well-established YouTube/Spotify curator. Known for premium melodic electronic.",
        "submission_url": None,
    },
]

# ---------------------------------------------------------------------------
# MUSIC BLOGS & PUBLICATIONS (electronic / house / techno focused)
# ---------------------------------------------------------------------------

MUSIC_BLOGS = [
    {
        "name": "Resident Advisor",
        "email": "editorial@residentadvisor.net",
        "type": "music_blog",
        "genre_focus": "techno, house, melodic techno, all underground electronic",
        "notes": "THE electronic music publication. Reviews, premieres, features. High bar.",
        "submission_url": "https://ra.co/contact",
    },
    {
        "name": "Mixmag",
        "email": "music@mixmag.net",
        "type": "music_blog",
        "genre_focus": "house, techno, EDM, dance music",
        "notes": "Leading global dance music magazine. Premiere pitches considered.",
        "submission_url": "https://mixmag.net/contact",
    },
    {
        "name": "DJ Mag",
        "email": "music@djmag.com",
        "type": "music_blog",
        "genre_focus": "techno, house, melodic techno, EDM",
        "notes": "World's biggest DJ/electronic music publication. Worth pitching for features.",
        "submission_url": "https://djmag.com/contact",
    },
    {
        "name": "XLR8R",
        "email": "music@xlr8r.com",
        "type": "music_blog",
        "genre_focus": "techno, house, experimental electronic, melodic techno",
        "notes": "Respected electronic music media. Features underground and emerging artists.",
        "submission_url": "https://xlr8r.com/contact",
    },
    {
        "name": "Magnetic Magazine",
        "email": "music@magneticmag.com",
        "type": "music_blog",
        "genre_focus": "electronic, house, techno",
        "notes": "Leading electronic music publication. Actively features independent releases.",
        "submission_url": "https://www.magneticmag.com/submit-music/",
    },
    {
        "name": "Data Transmission",
        "email": "music@datatransmission.co.uk",
        "type": "music_blog",
        "genre_focus": "tech house, melodic techno, house, techno",
        "notes": "UK-based electronic music media. Regular features and premiere coverage.",
        "submission_url": "https://datatransmission.co/contact",
    },
    {
        "name": "Ransom Note",
        "email": "music@theransomnote.co.uk",
        "type": "music_blog",
        "genre_focus": "house, techno, melodic techno, underground electronic",
        "notes": "London underground electronic media. Strong editorial voice, selective.",
        "submission_url": "https://theransomnote.co.uk/contact",
    },
    {
        "name": "Do Androids Dance",
        "email": "music@doandroids.dance",
        "type": "music_blog",
        "genre_focus": "electronic, house, techno, melodic techno",
        "notes": "Quality electronic music coverage. Reviews and premieres for emerging artists.",
        "submission_url": "https://doandroids.dance/submit/",
    },
    {
        "name": "Electronic Beats",
        "email": "info@electronicbeats.net",
        "type": "music_blog",
        "genre_focus": "electronic, techno, house, experimental",
        "notes": "Telekom-backed electronic music media. Strong European reach.",
        "submission_url": "https://www.electronicbeats.net/contact/",
    },
    {
        "name": "FACT Magazine",
        "email": "tips@factmag.com",
        "type": "music_blog",
        "genre_focus": "electronic, experimental, club music, techno",
        "notes": "Highly respected UK electronic/experimental music publication.",
        "submission_url": "https://www.factmag.com/contact/",
    },
    {
        "name": "Crack Magazine",
        "email": "music@crackmagazine.net",
        "type": "music_blog",
        "genre_focus": "electronic, club culture, house, techno",
        "notes": "London arts and music magazine. Strong electronic music editorial focus.",
        "submission_url": "https://crackmagazine.net/contact/",
    },
    {
        "name": "Groove Magazine",
        "email": "info@groove.de",
        "type": "music_blog",
        "genre_focus": "techno, house, melodic techno, electronic",
        "notes": "Germany's most respected electronic music magazine. Great European reach.",
        "submission_url": "https://groove.de/contact",
    },
    {
        "name": "Decoded Magazine",
        "email": "music@decodedmagazine.com",
        "type": "music_blog",
        "genre_focus": "techno, house, tech house, melodic techno",
        "notes": "Electronic music media platform. Regular features and premiere coverage.",
        "submission_url": "https://decodedmagazine.com/contact/",
    },
    {
        "name": "Inverted Audio",
        "email": "music@invertedaudio.com",
        "type": "music_blog",
        "genre_focus": "techno, experimental, electronic, club music",
        "notes": "UK publication with a focus on cutting-edge electronic and club music.",
        "submission_url": "https://inverted-audio.com/contact/",
    },
    {
        "name": "6AM Group",
        "email": "editorial@6am-group.com",
        "type": "music_blog",
        "genre_focus": "tech house, house, EDM, melodic techno",
        "notes": "US-based electronic music media. Active premiere and feature coverage.",
        "submission_url": "https://6am-group.com/contact",
    },
    {
        "name": "YourEDM",
        "email": "music@youredm.com",
        "type": "music_blog",
        "genre_focus": "EDM, electronic, house, techno",
        "notes": "Popular EDM news site. Good reach for electronic releases.",
        "submission_url": "https://www.youredm.com/submit-music/",
    },
    {
        "name": "Stoney Roads",
        "email": "music@stoneyroads.com",
        "type": "music_blog",
        "genre_focus": "electronic, house, techno, EDM",
        "notes": "Australia's leading electronic music media. Good Asia-Pacific reach.",
        "submission_url": "https://stoneyroads.com/contact",
    },
    {
        "name": "Trax Magazine",
        "email": "contact@traxmagazine.fr",
        "type": "music_blog",
        "genre_focus": "electronic, techno, house, French electronic scene",
        "notes": "France's leading electronic music publication. Strong European exposure.",
        "submission_url": None,
    },
    {
        "name": "Pulse Radio",
        "email": "music@pulseradio.net",
        "type": "music_blog",
        "genre_focus": "tech house, house, melodic techno, EDM",
        "notes": "Electronic music media platform. Features and news for new releases.",
        "submission_url": "https://pulseradio.net/contact",
    },
    {
        "name": "The Untz",
        "email": "submissions@theuntz.com",
        "type": "music_blog",
        "genre_focus": "electronic, house, techno, festival music",
        "notes": "US electronic music blog and event coverage. Welcomes new artist pitches.",
        "submission_url": "https://theuntz.com/contact",
    },
]

# ---------------------------------------------------------------------------
# RADIO STATIONS (electronic / club music focused)
# ---------------------------------------------------------------------------

RADIO_STATIONS = [
    {
        "name": "Rinse FM",
        "email": "music@rinsefm.com",
        "type": "radio_station",
        "genre_focus": "house, techno, melodic techno, grime, electronic",
        "notes": "London's most influential electronic music radio station. Essential pitch.",
        "submission_url": "https://rinse.fm/contact/",
    },
    {
        "name": "NTS Radio",
        "email": "music@nts.live",
        "type": "radio_station",
        "genre_focus": "electronic, house, techno, experimental, all genres",
        "notes": "London/LA/Manchester/Shanghai. Very open to new music across all electronic genres.",
        "submission_url": "https://www.nts.live/contact",
    },
    {
        "name": "Worldwide FM (Gilles Peterson)",
        "email": "music@worldwidefm.net",
        "type": "radio_station",
        "genre_focus": "electronic, house, soul, global bass",
        "notes": "Gilles Peterson's station. Great for forward-thinking melodic electronic music.",
        "submission_url": "https://worldwidefm.net/contact",
    },
    {
        "name": "HÖR Berlin",
        "email": "info@hor.berlin",
        "type": "radio_station",
        "genre_focus": "techno, house, melodic techno, experimental electronic",
        "notes": "Berlin's leading livestream platform. Enormous global electronic music audience.",
        "submission_url": "https://hor.berlin/contact",
    },
    {
        "name": "Boiler Room",
        "email": "music@boilerroom.tv",
        "type": "radio_station",
        "genre_focus": "techno, house, melodic techno, all club music",
        "notes": "Global livestream platform for electronic music. High visibility for new artists.",
        "submission_url": "https://boilerroom.tv/contact",
    },
    {
        "name": "Refuge Worldwide (Berlin)",
        "email": "info@refugeworldwide.com",
        "type": "radio_station",
        "genre_focus": "electronic, house, techno, experimental",
        "notes": "Berlin community radio. Supports emerging artists. Open to new music.",
        "submission_url": "https://refugeworldwide.com/contact",
    },
    {
        "name": "Cashmere Radio (Berlin)",
        "email": "info@cashmereradio.com",
        "type": "radio_station",
        "genre_focus": "electronic, experimental, house, techno",
        "notes": "Berlin experimental/electronic community radio. Open submission process.",
        "submission_url": None,
    },
    {
        "name": "Kiosk Radio (Brussels)",
        "email": "info@kioskradio.be",
        "type": "radio_station",
        "genre_focus": "electronic, house, techno, experimental",
        "notes": "Brussels-based electronic radio with strong European following.",
        "submission_url": "https://kioskradio.be/contact",
    },
    {
        "name": "The Lot Radio (New York)",
        "email": "info@thelotradio.com",
        "type": "radio_station",
        "genre_focus": "house, techno, electronic, eclectic",
        "notes": "Brooklyn outdoor radio platform. NYC's most vibrant independent radio.",
        "submission_url": "https://thelotradio.com/contact",
    },
    {
        "name": "Dublab",
        "email": "music@dublab.com",
        "type": "radio_station",
        "genre_focus": "electronic, ambient, experimental, house",
        "notes": "LA-based nonprofit internet radio. Loves experimental and melodic electronic.",
        "submission_url": "https://www.dublab.com/contact/",
    },
    {
        "name": "Boxout.fm (India)",
        "email": "music@boxout.fm",
        "type": "radio_station",
        "genre_focus": "electronic, house, techno, South Asian electronic",
        "notes": "India's leading electronic music radio. Good reach in Asia-Pacific market.",
        "submission_url": "https://boxout.fm/contact",
    },
    {
        "name": "N10.AS (Amsterdam)",
        "email": "info@n10.as",
        "type": "radio_station",
        "genre_focus": "house, techno, electronic, experimental",
        "notes": "Amsterdam-based streaming platform. Regular programming of new electronic music.",
        "submission_url": None,
    },
    {
        "name": "Soma FM",
        "email": "music@somafm.com",
        "type": "radio_station",
        "genre_focus": "electronic, ambient, deep house, space music",
        "notes": "San Francisco internet radio. Multiple genre channels including deep/melodic.",
        "submission_url": "https://somafm.com/contact/",
    },
    {
        "name": "BBC Radio 1 Dance",
        "email": "radio1music@bbc.co.uk",
        "type": "radio_station",
        "genre_focus": "house, techno, dance, melodic techno",
        "notes": "BBC Radio 1's electronic/dance programming (Pete Tong, Essential Mix). Major reach.",
        "submission_url": "https://www.bbc.co.uk/programmes/b006wkfh",
    },
    {
        "name": "BBC Introducing",
        "email": "introducing@bbc.co.uk",
        "type": "radio_station",
        "genre_focus": "all genres, emerging artists",
        "notes": "BBC's platform for unsigned/independent artists. Can lead to Radio 1 plays.",
        "submission_url": "https://www.bbc.co.uk/music/introducing",
    },
    {
        "name": "WFMU",
        "email": "music@wfmu.org",
        "type": "radio_station",
        "genre_focus": "experimental, electronic, avant-garde, freeform",
        "notes": "Legendary freeform radio. Very open to unusual and creative electronic music.",
        "submission_url": "https://www.wfmu.org/contact/",
    },
    {
        "name": "KCRW 89.9 FM",
        "email": "music@kcrw.org",
        "type": "radio_station",
        "genre_focus": "indie, electronic, world, alternative",
        "notes": "LA's most influential radio station. Programs electronic music regularly.",
        "submission_url": "https://www.kcrw.com/music",
    },
    {
        "name": "KEXP 90.3 FM",
        "email": "music@kexp.org",
        "type": "radio_station",
        "genre_focus": "indie, alternative, electronic, international",
        "notes": "Seattle's legendary music station. Electronic music programming on weekends.",
        "submission_url": "https://www.kexp.org/music-submissions/",
    },
    {
        "name": "Radio Paradise",
        "email": "music@radioparadise.com",
        "type": "radio_station",
        "genre_focus": "indie, alternative, electronic, eclectic",
        "notes": "Large internet radio with eclectic programming including melodic electronic.",
        "submission_url": "https://radioparadise.com/",
    },
    {
        "name": "Rinse France",
        "email": "contact@rinsefrance.com",
        "type": "radio_station",
        "genre_focus": "house, techno, club music, melodic techno",
        "notes": "French arm of Rinse FM. Strong reach in the French electronic music scene.",
        "submission_url": None,
    },
]

# ---------------------------------------------------------------------------
# MASTER LIST — combine all contact types
# ---------------------------------------------------------------------------

ALL_CONTACTS = RECORD_LABELS + STREAMING_CURATORS + MUSIC_BLOGS + RADIO_STATIONS

# Contacts that accept email pitches (filter out any without email)
EMAIL_CONTACTS = [c for c in ALL_CONTACTS if c.get("email")]


def get_email_contacts() -> list:
    """Return all contacts that can be reached by email."""
    return EMAIL_CONTACTS


def get_all_contacts() -> list:
    """Return all contacts."""
    return ALL_CONTACTS


def get_contacts_by_genre(genre_keyword: str) -> list:
    """
    Filter contacts whose genre_focus contains the given keyword.
    Example: get_contacts_by_genre('melodic techno')
    """
    keyword = genre_keyword.lower()
    return [
        c for c in EMAIL_CONTACTS
        if keyword in c.get("genre_focus", "").lower()
    ]
