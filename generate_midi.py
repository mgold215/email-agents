"""
Rufus Du Sol-style pluck melody in C# minor
Generated for Logic Pro

Style reference: Innerbloom / No Place / Treat You Better era
- Hypnotic, arpeggiated pluck pattern
- Syncopated rhythm with 8th/16th note variation
- 120 BPM, 4/4 time
- C# natural minor scale: C#, D#, E, F#, G#, A, B
"""

import mido
from mido import MidiFile, MidiTrack, Message, MetaMessage

# ── Constants ──────────────────────────────────────────────────────────────────
BPM = 120
TICKS_PER_BEAT = 480          # standard resolution for Logic Pro
TEMPO = mido.bpm2tempo(BPM)   # microseconds per beat

# ── MIDI note numbers (C# minor scale, octave 4-5) ────────────────────────────
# C#4=61, D#4=63, E4=64, F#4=66, G#4=68, A4=69, B4=71, C#5=73, D#5=75, E5=76
Cs4 = 61
Ds4 = 63
E4  = 64
Fs4 = 66
Gs4 = 68
A4  = 69
B4  = 71
Cs5 = 73
Ds5 = 75
E5  = 76
Gs5 = 80

# ── Tick helpers ───────────────────────────────────────────────────────────────
def T(beats):
    """Convert beats to ticks. Use fractions for subdivisions.
    e.g. T(0.5) = 8th note, T(0.25) = 16th note"""
    return int(TICKS_PER_BEAT * beats)

# ── Velocity layers ────────────────────────────────────────────────────────────
VEL_ACCENT = 100   # accented hit
VEL_MID    = 80    # normal note
VEL_SOFT   = 62    # ghost / passing note

# ── Melody definition ──────────────────────────────────────────────────────────
# Each entry: (note, duration_beats, velocity)
# The pluck pattern is short and slightly staccato — gate at ~60% of duration.
# Rufus Du Sol characteristic: ascending arpeggio fragments, falling resolutions,
# syncopation on the "and" of beats 2 and 4.

GATE = 0.55  # note on time as fraction of step duration (staccato pluck feel)

# Pattern A — 4 bars, the main hook
pattern_a = [
    # bar 1: ascending arp from E4 with syncopation
    (E4,  0.5,  VEL_MID),
    (Gs4, 0.25, VEL_SOFT),
    (B4,  0.25, VEL_ACCENT),
    (Cs5, 0.5,  VEL_ACCENT),
    (B4,  0.25, VEL_MID),
    (Gs4, 0.25, VEL_SOFT),
    (Fs4, 0.5,  VEL_MID),
    (E4,  0.5,  VEL_MID),

    # bar 2: resolve then reach up
    (Cs4, 0.75, VEL_SOFT),
    (E4,  0.25, VEL_MID),
    (Fs4, 0.5,  VEL_MID),
    (Gs4, 0.25, VEL_ACCENT),
    (A4,  0.25, VEL_ACCENT),
    (B4,  1.0,  VEL_MID),

    # bar 3: the "yearning" phrase — climb toward E5
    (Gs4, 0.25, VEL_MID),
    (B4,  0.25, VEL_MID),
    (Cs5, 0.5,  VEL_ACCENT),
    (Ds5, 0.25, VEL_MID),
    (E5,  0.25, VEL_ACCENT),
    (Cs5, 0.5,  VEL_MID),
    (B4,  0.5,  VEL_MID),
    (Gs4, 0.5,  VEL_SOFT),

    # bar 4: falling resolution back to root
    (Fs4, 0.5,  VEL_MID),
    (E4,  0.25, VEL_MID),
    (Ds4, 0.25, VEL_SOFT),
    (Cs4, 1.0,  VEL_ACCENT),
    (E4,  0.5,  VEL_SOFT),
    (Gs4, 0.5,  VEL_SOFT),
]

# Pattern B — 4 bars, variation / build
pattern_b = [
    # bar 5: same opening, push harder on accent
    (E4,  0.25, VEL_MID),
    (Gs4, 0.25, VEL_MID),
    (B4,  0.5,  VEL_ACCENT),
    (Cs5, 0.25, VEL_ACCENT),
    (B4,  0.25, VEL_MID),
    (Gs4, 0.5,  VEL_MID),
    (Fs4, 0.25, VEL_SOFT),
    (E4,  0.25, VEL_SOFT),
    (Ds4, 0.5,  VEL_SOFT),
    (E4,  0.5,  VEL_MID),

    # bar 6: syncopated offbeat hits
    (Gs4, 0.25, VEL_SOFT),
    (A4,  0.5,  VEL_ACCENT),
    (Gs4, 0.25, VEL_MID),
    (Fs4, 0.5,  VEL_MID),
    (E4,  0.25, VEL_MID),
    (Fs4, 0.25, VEL_SOFT),
    (Gs4, 0.5,  VEL_MID),
    (B4,  0.5,  VEL_ACCENT),
    (Cs5, 0.25, VEL_MID),
    (B4,  0.25, VEL_SOFT),

    # bar 7: high point of the phrase
    (Cs5, 0.5,  VEL_ACCENT),
    (E5,  0.5,  VEL_ACCENT),
    (Ds5, 0.25, VEL_MID),
    (Cs5, 0.25, VEL_MID),
    (B4,  0.5,  VEL_MID),
    (Gs4, 0.25, VEL_SOFT),
    (Fs4, 0.25, VEL_SOFT),
    (E4,  0.5,  VEL_MID),
    (Ds4, 0.25, VEL_SOFT),
    (E4,  0.25, VEL_MID),

    # bar 8: full landing on Cs4, echo tail
    (Cs4, 1.0,  VEL_ACCENT),
    (E4,  0.25, VEL_SOFT),
    (Gs4, 0.25, VEL_SOFT),
    (Cs5, 0.5,  VEL_MID),
    (B4,  0.5,  VEL_SOFT),
    (Gs4, 0.25, VEL_SOFT),
    (Fs4, 0.25, VEL_SOFT),
    (E4,  0.5,  VEL_SOFT),
]

# Full arrangement: A  A  B  A  (16 bars)
full_melody = pattern_a + pattern_a + pattern_b + pattern_a


# ── Build MIDI file ────────────────────────────────────────────────────────────
mid = MidiFile(ticks_per_beat=TICKS_PER_BEAT)
track = MidiTrack()
mid.tracks.append(track)

# Metadata
track.append(MetaMessage('set_tempo',  tempo=TEMPO, time=0))
track.append(MetaMessage('time_signature', numerator=4, denominator=4,
                          clocks_per_click=24, notated_32nd_notes_per_beat=8, time=0))
track.append(MetaMessage('key_signature', key='C#m', time=0))
track.append(MetaMessage('track_name', name='RDS Pluck - C#m', time=0))

# MIDI channel 0, program 0 (General MIDI: Acoustic Grand Piano)
# In Logic you'll swap this for your pluck synth patch
track.append(Message('program_change', program=0, channel=0, time=0))

# Write notes with staccato gate
for (note, dur_beats, vel) in full_melody:
    dur_ticks  = T(dur_beats)
    gate_ticks = int(dur_ticks * GATE)
    rest_ticks = dur_ticks - gate_ticks

    track.append(Message('note_on',  note=note, velocity=vel,  channel=0, time=0))
    track.append(Message('note_off', note=note, velocity=0,    channel=0, time=gate_ticks))
    # silence between notes keeps that plucky separation
    if rest_ticks > 0:
        # zero-duration note_on as a rest carrier (standard MIDI idle)
        track.append(Message('note_on', note=note, velocity=0, channel=0, time=rest_ticks))

# End of track
track.append(MetaMessage('end_of_track', time=0))

# ── Save ───────────────────────────────────────────────────────────────────────
OUTPUT = 'rds_pluck_csharp_minor.mid'
mid.save(OUTPUT)

total_bars = len(full_melody)  # not bars, but we can estimate
print(f"Saved: {OUTPUT}")
print(f"BPM: {BPM}  |  Key: C# minor  |  Arrangement: A A B A (16 bars)")
print(f"Ticks/beat: {TICKS_PER_BEAT}")
print(f"\nLogic Pro tips:")
print("  1. Import via File > Import > MIDI")
print("  2. Assign track to a pluck synth — try ES2 or Alchemy")
print("     Alchemy preset: 'Crystal Pluck' or 'Glass Arp' as a starting point")
print("  3. Add Reverb (ChromaVerb) with long tail ~2.5s, mix ~25%")
print("  4. Chorus / Ensemble effect for the Rufus Du Sol shimmer")
print("  5. Sidechain compress to your kick at ~4:1 for that pumping feel")
