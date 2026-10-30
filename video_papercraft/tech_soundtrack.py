import numpy as np
import wave
import math
import os

OUTPUT_WAV = "video_papercraft/tech_soundtrack.wav"
DURATION = 12.0
SR = 44100

def generate_soundtrack():
    total_samples = int(SR * DURATION)
    audio_l = np.zeros(total_samples, dtype=np.float32)
    audio_r = np.zeros(total_samples, dtype=np.float32)

    def add_sound(snd, start_time, pan=0.0):
        s_idx = int(start_time * SR)
        e_idx = min(s_idx + len(snd), total_samples)
        if s_idx < total_samples and e_idx > s_idx:
            chunk = snd[:e_idx - s_idx]
            gain_l = math.cos((pan + 1.0) * math.pi / 4.0)
            gain_r = math.sin((pan + 1.0) * math.pi / 4.0)
            audio_l[s_idx:e_idx] += chunk * gain_l
            audio_r[s_idx:e_idx] += chunk * gain_r

    # 1. Futuristic Sci-Fi Whoosh / Energy Riser
    def make_sci_fi_whoosh(dur=0.6, pitch_start=120.0, pitch_end=950.0, intensity=0.6):
        n = int(SR * dur)
        t = np.linspace(0, dur, n, endpoint=False)
        freq = np.geomspace(pitch_start, pitch_end, n)
        phase = 2 * np.pi * np.cumsum(freq) / SR
        sine = np.sin(phase)
        # filtered noise swell
        noise = np.random.uniform(-1, 1, n)
        noise = np.diff(np.pad(noise, (1, 0)))
        env = (np.sin(np.pi * t / dur)) ** 1.8
        return ((sine * 0.4 + noise * 0.6) * env * intensity).astype(np.float32)

    # 2. Modern Sub-Bass Impact / Drop
    def make_sub_drop(pitch=95.0, dur=0.65, intensity=0.85):
        n = int(SR * dur)
        t = np.linspace(0, dur, n, endpoint=False)
        freq = pitch * np.exp(-t * 9.0)
        phase = 2 * np.pi * np.cumsum(freq) / SR
        sub = np.sin(phase) * np.exp(-t * 5.5)
        # crisp digital click
        click = np.random.uniform(-1, 1, n) * np.exp(-t * 120.0) * 0.3
        return ((sub * 0.85 + click * 0.15) * intensity).astype(np.float32)

    # 3. High-Tech UI Laser Tap / Digital Confirmation
    def make_digital_tap(freq=1800.0, dur=0.12, intensity=0.5):
        n = int(SR * dur)
        t = np.linspace(0, dur, n, endpoint=False)
        f = freq * np.exp(-t * 45.0)
        phase = 2 * np.pi * np.cumsum(f) / SR
        tone = np.sin(phase) * np.exp(-t * 32.0)
        return (tone * intensity).astype(np.float32)

    # 4. Lush Ambient Synth Chords (Cyber Harmony: Dm9 -> G -> Cmaj7)
    def make_synth_chord(freqs, dur=2.0, intensity=0.4):
        n = int(SR * dur)
        t = np.linspace(0, dur, n, endpoint=False)
        chord = np.zeros(n, dtype=np.float32)
        for f in freqs:
            tone = (np.sin(2 * np.pi * f * t) + 
                    0.3 * np.sin(2 * np.pi * f * 2.0 * t) + 
                    0.15 * np.sin(2 * np.pi * f * 3.0 * t))
            chord += tone
        chord /= len(freqs)
        # Slow attack, smooth decay envelope
        attack = int(SR * 0.25)
        decay = n - attack
        env = np.concatenate([np.linspace(0, 1, attack), np.exp(-np.linspace(0, 3.5, decay))])
        return (chord * env * intensity).astype(np.float32)

    # 5. Crystal Hologram Bell / Chime
    def make_holo_bell(freq=1318.51, dur=2.2, intensity=0.45): # E6
        n = int(SR * dur)
        t = np.linspace(0, dur, n, endpoint=False)
        tone = (np.sin(2 * np.pi * freq * t) + 
                0.35 * np.sin(2 * np.pi * freq * 2.01 * t) + 
                0.15 * np.sin(2 * np.pi * freq * 3.02 * t))
        env = np.exp(-t * 2.6)
        return (tone * env * intensity).astype(np.float32)

    # -------------------------------------------------------------
    # TIMELINE COMPOSITION (12.0 Seconds)
    # -------------------------------------------------------------
    # Scene 1: Booting / Cyber grid activation
    add_sound(make_sci_fi_whoosh(0.7, 80, 750, 0.65), 0.05, pan=-0.2)
    add_sound(make_sub_drop(110, 0.5, 0.7), 0.45, pan=0.0)
    add_sound(make_digital_tap(1600, 0.12, 0.6), 0.48, pan=0.0)
    add_sound(make_synth_chord([293.66, 349.23, 440.00, 523.25], 2.2, 0.4), 0.6, pan=0.0) # Dm7 chord

    # Scene 2: 3D Master Logo Reveal (2.5s)
    add_sound(make_sci_fi_whoosh(0.65, 120, 1100, 0.8), 2.3, pan=-0.3)
    add_sound(make_sub_drop(85, 0.7, 0.95), 2.65, pan=0.0) # Heavy bass slam
    add_sound(make_digital_tap(2200, 0.15, 0.7), 2.68, pan=0.1)
    add_sound(make_synth_chord([392.00, 493.88, 587.33, 659.25], 2.5, 0.45), 2.7, pan=0.0) # G6 chord
    add_sound(make_digital_tap(1900, 0.12, 0.5), 3.4, pan=0.2) # Ribbon laser scan

    # Scene 3: Solution Tech Nodes (5.3s to 8.5s)
    # Node 1: Chatbot 24/7
    add_sound(make_sci_fi_whoosh(0.35, 300, 1200, 0.5), 5.25, pan=-0.35)
    add_sound(make_digital_tap(2400, 0.12, 0.6), 5.4, pan=-0.35)
    add_sound(make_holo_bell(1046.5, 1.2, 0.35), 5.42, pan=-0.35) # C6

    # Node 2: Flujos n8n
    add_sound(make_sci_fi_whoosh(0.35, 350, 1400, 0.5), 6.15, pan=0.0)
    add_sound(make_digital_tap(2600, 0.12, 0.6), 6.3, pan=0.0)
    add_sound(make_holo_bell(1174.66, 1.2, 0.35), 6.32, pan=0.0) # D6

    # Node 3: Ecosistema 360°
    add_sound(make_sci_fi_whoosh(0.35, 400, 1600, 0.5), 7.05, pan=0.35)
    add_sound(make_digital_tap(2800, 0.12, 0.6), 7.2, pan=0.35)
    add_sound(make_holo_bell(1318.51, 1.2, 0.35), 7.22, pan=0.35) # E6

    # Price pill snap
    add_sound(make_digital_tap(2100, 0.12, 0.55), 7.9, pan=0.0)

    # Scene 4: VIP Tech Pass & WhatsApp CTA (8.5s to 12.0s)
    add_sound(make_sci_fi_whoosh(0.8, 100, 1500, 0.85), 8.5, pan=0.0)
    add_sound(make_sub_drop(75, 0.8, 1.0), 8.95, pan=0.0) # Epic sub-bass impact
    add_sound(make_digital_tap(3200, 0.16, 0.8), 9.0, pan=0.0)
    add_sound(make_holo_bell(1567.98, 2.5, 0.6), 9.05, pan=0.1) # G6 triumph bell

    # Stamp Hit / Verification badge at 9.6s
    add_sound(make_sub_drop(120, 0.4, 0.8), 9.55, pan=0.25)
    add_sound(make_digital_tap(3500, 0.18, 0.75), 9.58, pan=0.25)
    add_sound(make_holo_bell(2093.00, 2.5, 0.5), 9.6, pan=0.25) # C7 crystal

    # Normalization & Master Limiter
    max_val = max(np.max(np.abs(audio_l)), np.max(np.abs(audio_r)))
    if max_val > 0.01:
        norm = 0.90 / max_val
        audio_l = np.clip(audio_l * norm, -0.98, 0.98)
        audio_r = np.clip(audio_r * norm, -0.98, 0.98)

    stereo = np.empty((total_samples * 2,), dtype=np.int16)
    stereo[0::2] = (audio_l * 32767).astype(np.int16)
    stereo[1::2] = (audio_r * 32767).astype(np.int16)

    with wave.open(OUTPUT_WAV, "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(stereo.tobytes())

    print(f"Tech Soundtrack saved: {OUTPUT_WAV} ({DURATION}s, stereo, 44.1kHz)")

if __name__ == "__main__":
    generate_soundtrack()
