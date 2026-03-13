"""
2-bar pluck chord loop in D minor — Rufus Du Sol style
Progression: Dm - C - Bb - Am  (i - VII - VI - v)
120 BPM, 4/4, each chord = 2 beats, syncopated pluck rhythm
"""

import mido
from mido import MidiFile, MidiTrack, Message, MetaMessage

BPM             = 120
TICKS_PER_BEAT  = 480
TEMPO           = mido.bpm2tempo(BPM)
GATE            = 0.50   # short gate = punchy pluck chords

def T(beats):
    return int(TICKS_PER_BEAT * beats)

# ── Chord voicings (mid-range, good for pluck timbre) ─────────────────────────
# Dm7  — D4, F4, A4, C5
# Csus2 — C4, D4, G4   (VII, open voicing, avoids E natural clash)
# BbMaj7 — Bb3, D4, F4, A4
# Am7  — A3, C4, E4, G4  (v chord, natural minor)

Bb3 = 58
A3  = 57
C4  = 60
D4  = 62
E4  = 64
F4  = 65
G4  = 67
A4  = 69
Bb4 = 70
C5  = 72

chords = {
    "Dm7":    [D4, F4, A4, C5],
    "Csus2":  [C4, D4, G4],
    "BbMaj7": [Bb3, D4, F4, A4],
    "Am7":    [A3, C4, E4, G4],
}

# ── Rhythm pattern ─────────────────────────────────────────────────────────────
# Each chord gets a rhythmic hit pattern within its 2-beat window.
# Hits: beat 1 (accent), and-of-1 (soft), beat 2 (mid), and-of-2 (soft accent)
# This gives the syncopated RDS groove rather than straight quarter hits.
#
# (chord_name, hits_as_beat_offsets_and_velocities)
# offsets are relative to the chord's start, in beats

VEL_A = 100   # accent
VEL_M = 78    # mid
VEL_S = 60    # soft

rhythm = [
    # (chord name, [(offset_beats, velocity), ...], window_beats)
    ("Dm7",    [(0.0, VEL_A), (0.5, VEL_S), (1.0, VEL_M), (1.5, VEL_S)], 2.0),
    ("Csus2",  [(0.0, VEL_M), (0.5, VEL_S), (1.0, VEL_A), (1.75, VEL_S)], 2.0),
    ("BbMaj7", [(0.0, VEL_A), (0.5, VEL_S), (1.0, VEL_M), (1.5, VEL_S)], 2.0),
    ("Am7",    [(0.0, VEL_M), (0.75, VEL_S), (1.0, VEL_A), (1.5, VEL_M)], 2.0),
]

# ── Build absolute event list ──────────────────────────────────────────────────
# events: list of (abs_tick, 'on'/'off', notes_list, velocity)
events = []
cursor = 0  # ticks

for (chord_name, hits, window_beats) in rhythm:
    notes = chords[chord_name]
    window_ticks = T(window_beats)

    for (offset_beats, vel) in hits:
        abs_on  = cursor + T(offset_beats)
        # gate: note off at fixed short duration after on
        abs_off = abs_on + int(T(0.25) * GATE)  # 16th-note gate, very punchy

        for n in notes:
            events.append((abs_on,  'on',  n, vel))
            events.append((abs_off, 'off', n, 0))

    cursor += window_ticks

# Sort by tick then off-before-on at same tick
events.sort(key=lambda e: (e[0], 0 if e[1] == 'off' else 1))

# ── Convert to delta-time MIDI messages ───────────────────────────────────────
mid   = MidiFile(ticks_per_beat=TICKS_PER_BEAT)
track = MidiTrack()
mid.tracks.append(track)

track.append(MetaMessage('set_tempo', tempo=TEMPO, time=0))
track.append(MetaMessage('time_signature', numerator=4, denominator=4,
                          clocks_per_click=24, notated_32nd_notes_per_beat=8, time=0))
track.append(MetaMessage('key_signature', key='Dm', time=0))
track.append(MetaMessage('track_name', name='RDS Pluck Chords - Dm', time=0))
track.append(Message('program_change', program=0, channel=0, time=0))

prev_tick = 0
for (abs_tick, kind, note, vel) in events:
    delta = abs_tick - prev_tick
    prev_tick = abs_tick
    if kind == 'on':
        track.append(Message('note_on',  note=note, velocity=vel, channel=0, time=delta))
    else:
        track.append(Message('note_off', note=note, velocity=0,   channel=0, time=delta))

track.append(MetaMessage('end_of_track', time=0))

OUTPUT = 'rds_pluck_chords_d_minor.mid'
mid.save(OUTPUT)

print(f"Saved: {OUTPUT}")
print(f"BPM: {BPM}  |  Key: D minor  |  2-bar loop")
print(f"Progression: Dm7 - Csus2 - BbMaj7 - Am7  (i - VII - VI - v)")
print(f"""
Serum 2 tips for chords:
  - Same ENV 1/2 pluck patch as the melody track
  - Layer a second Serum 2 instance an octave DOWN (sub body)
  - Detune OSC A +7 cents, OSC B -7 cents for width
  - High-pass the chord track at ~150 Hz so it doesn't clash with bass
  - Try a slightly longer decay on ENV 1 (~350-450 ms) for chords vs melody
""")
