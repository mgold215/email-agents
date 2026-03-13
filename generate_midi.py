"""
Rufus Du Sol-style pluck melody in D minor
Generated for Serum 2

Style reference: Innerbloom / No Place / Treat You Better era
- Hypnotic, arpeggiated pluck pattern
- Syncopated rhythm with 8th/16th note variation
- 120 BPM, 4/4 time
- D natural minor scale: D, E, F, G, A, Bb, C
"""

import mido
from mido import MidiFile, MidiTrack, Message, MetaMessage

# ── Constants ──────────────────────────────────────────────────────────────────
BPM = 120
TICKS_PER_BEAT = 480        # standard resolution
TEMPO = mido.bpm2tempo(BPM) # microseconds per beat

# ── MIDI note numbers (D natural minor scale, octave 4-5) ─────────────────────
# D4=62, E4=64, F4=65, G4=67, A4=69, Bb4=70, C5=72, D5=74, E5=76, F5=77, A5=81
D4  = 62
E4  = 64
F4  = 65
G4  = 67
A4  = 69
Bb4 = 70
C5  = 72
D5  = 74
E5  = 76
F5  = 77
A5  = 81

# ── Tick helpers ───────────────────────────────────────────────────────────────
def T(beats):
    """Convert beats to ticks.
    T(1.0) = quarter note, T(0.5) = 8th, T(0.25) = 16th"""
    return int(TICKS_PER_BEAT * beats)

# ── Velocity layers ────────────────────────────────────────────────────────────
VEL_ACCENT = 100  # accented hit
VEL_MID    = 80   # normal note
VEL_SOFT   = 62   # ghost / passing note

# ── Gate ───────────────────────────────────────────────────────────────────────
# 55% gate = notes cut off before next hit, giving that sharp pluck separation
GATE = 0.55

# ── Melody definition ──────────────────────────────────────────────────────────
# Each entry: (note, duration_beats, velocity)
# Rufus Du Sol characteristic: ascending arpeggio fragments, falling resolutions,
# syncopation on the "and" of beats 2 and 4.

# Pattern A — 4 bars, the main hook
pattern_a = [
    # bar 1: ascending arp from F4 with syncopation
    (F4,  0.5,  VEL_MID),
    (A4,  0.25, VEL_SOFT),
    (C5,  0.25, VEL_ACCENT),
    (D5,  0.5,  VEL_ACCENT),
    (C5,  0.25, VEL_MID),
    (A4,  0.25, VEL_SOFT),
    (G4,  0.5,  VEL_MID),
    (F4,  0.5,  VEL_MID),

    # bar 2: resolve then reach up
    (D4,  0.75, VEL_SOFT),
    (F4,  0.25, VEL_MID),
    (G4,  0.5,  VEL_MID),
    (A4,  0.25, VEL_ACCENT),
    (Bb4, 0.25, VEL_ACCENT),
    (C5,  1.0,  VEL_MID),

    # bar 3: the "yearning" phrase — climb toward E5
    (A4,  0.25, VEL_MID),
    (C5,  0.25, VEL_MID),
    (D5,  0.5,  VEL_ACCENT),
    (E5,  0.25, VEL_MID),
    (F5,  0.25, VEL_ACCENT),
    (D5,  0.5,  VEL_MID),
    (C5,  0.5,  VEL_MID),
    (A4,  0.5,  VEL_SOFT),

    # bar 4: falling resolution back to root
    (G4,  0.5,  VEL_MID),
    (F4,  0.25, VEL_MID),
    (E4,  0.25, VEL_SOFT),
    (D4,  1.0,  VEL_ACCENT),
    (F4,  0.5,  VEL_SOFT),
    (A4,  0.5,  VEL_SOFT),
]

# Pattern B — 4 bars, variation / build
pattern_b = [
    # bar 5: same opening, push harder on accent
    (F4,  0.25, VEL_MID),
    (A4,  0.25, VEL_MID),
    (C5,  0.5,  VEL_ACCENT),
    (D5,  0.25, VEL_ACCENT),
    (C5,  0.25, VEL_MID),
    (A4,  0.5,  VEL_MID),
    (G4,  0.25, VEL_SOFT),
    (F4,  0.25, VEL_SOFT),
    (E4,  0.5,  VEL_SOFT),
    (F4,  0.5,  VEL_MID),

    # bar 6: syncopated offbeat hits
    (A4,  0.25, VEL_SOFT),
    (Bb4, 0.5,  VEL_ACCENT),
    (A4,  0.25, VEL_MID),
    (G4,  0.5,  VEL_MID),
    (F4,  0.25, VEL_MID),
    (G4,  0.25, VEL_SOFT),
    (A4,  0.5,  VEL_MID),
    (C5,  0.5,  VEL_ACCENT),
    (D5,  0.25, VEL_MID),
    (C5,  0.25, VEL_SOFT),

    # bar 7: high point of the phrase
    (D5,  0.5,  VEL_ACCENT),
    (F5,  0.5,  VEL_ACCENT),
    (E5,  0.25, VEL_MID),
    (D5,  0.25, VEL_MID),
    (C5,  0.5,  VEL_MID),
    (A4,  0.25, VEL_SOFT),
    (G4,  0.25, VEL_SOFT),
    (F4,  0.5,  VEL_MID),
    (E4,  0.25, VEL_SOFT),
    (F4,  0.25, VEL_MID),

    # bar 8: full landing on D4, echo tail
    (D4,  1.0,  VEL_ACCENT),
    (F4,  0.25, VEL_SOFT),
    (A4,  0.25, VEL_SOFT),
    (D5,  0.5,  VEL_MID),
    (C5,  0.5,  VEL_SOFT),
    (A4,  0.25, VEL_SOFT),
    (G4,  0.25, VEL_SOFT),
    (F4,  0.5,  VEL_SOFT),
]

# Full arrangement: A  A  B  A  (16 bars)
full_melody = pattern_a + pattern_a + pattern_b + pattern_a


# ── Build MIDI file ────────────────────────────────────────────────────────────
mid = MidiFile(ticks_per_beat=TICKS_PER_BEAT)
track = MidiTrack()
mid.tracks.append(track)

# Metadata
track.append(MetaMessage('set_tempo', tempo=TEMPO, time=0))
track.append(MetaMessage('time_signature', numerator=4, denominator=4,
                          clocks_per_click=24, notated_32nd_notes_per_beat=8, time=0))
track.append(MetaMessage('key_signature', key='Dm', time=0))
track.append(MetaMessage('track_name', name='RDS Pluck - Dm', time=0))

# Program 0 = piano placeholder; swap for your Serum 2 instance in the DAW
track.append(Message('program_change', program=0, channel=0, time=0))

# Write notes with staccato gate
for (note, dur_beats, vel) in full_melody:
    dur_ticks  = T(dur_beats)
    gate_ticks = int(dur_ticks * GATE)
    rest_ticks = dur_ticks - gate_ticks

    track.append(Message('note_on',  note=note, velocity=vel, channel=0, time=0))
    track.append(Message('note_off', note=note, velocity=0,   channel=0, time=gate_ticks))
    # small gap between notes preserves the pluck attack on every hit
    if rest_ticks > 0:
        track.append(Message('note_on', note=note, velocity=0, channel=0, time=rest_ticks))

# End of track
track.append(MetaMessage('end_of_track', time=0))

# ── Save ───────────────────────────────────────────────────────────────────────
OUTPUT = 'rds_pluck_d_minor.mid'
mid.save(OUTPUT)

print(f"Saved: {OUTPUT}")
print(f"BPM: {BPM}  |  Key: D minor  |  Arrangement: A A B A (16 bars)")
print(f"Ticks/beat: {TICKS_PER_BEAT}")
print(f"""
Serum 2 patch tips to get the Rufus Du Sol pluck tone:
-------------------------------------------------------
OSC A:
  - Waveform: Saw (or a slightly rounded saw for warmth)
  - Unison: 4 voices, Detune ~0.12, Blend ~50%

ENV 1 (Amplitude):
  - Attack:  0 ms
  - Decay:   180-300 ms  <- the pluck length lives here
  - Sustain: 0%
  - Release: 80 ms

FILTER:
  - Type: Low Pass (MG or Dirty)
  - Cutoff: ~60%  Resonance: ~25%
  - Route ENV 2 -> Cutoff with amount +40

ENV 2 (Filter modulator):
  - Attack:  0 ms
  - Decay:   120-200 ms  <- filter opens then closes fast
  - Sustain: 0%
  - Release: 60 ms

FX chain:
  1. Hyper/Dimension  - mix ~30%, size medium (adds the RDS shimmer)
  2. Chorus           - rate slow (~0.3 Hz), depth ~20%
  3. Reverb           - size large, decay ~2.2s, mix 20-25%
  4. Compressor       - sidechain to kick, ratio 4:1, fast attack
""")
