import numpy as np
import wave
import math
import os

OUTPUT_WAV = "video_papercraft/soundtrack.wav"
DURATION = 12.0
SR = 44100

def generate_soundtrack():
    total_samples = int(SR * DURATION)
    audio_l = np.zeros(total_samples, dtype=np.float32)
    audio_r = np.zeros(total_samples, dtype=np.float32)

    def add_sound(snd, start_time, pan=0.0):
        # pan: -1.0 (left) to 1.0 (right)
        s_idx = int(start_time * SR)
        e_idx = min(s_idx + len(snd), total_samples)
        if s_idx < total_samples and e_idx > s_idx:
            chunk = snd[:e_idx - s_idx]
            gain_l = math.cos((pan + 1.0) * math.pi / 4.0)
            gain_r = math.sin((pan + 1.0) * math.pi / 4.0)
            audio_l[s_idx:e_idx] += chunk * gain_l
            audio_r[s_idx:e_idx] += chunk * gain_r

    # 1. Paper rustle / slide sound
    def make_paper_rustle(dur=0.45, intensity=0.5):
        n = int(SR * dur)
        t = np.linspace(0, dur, n, endpoint=False)
        noise = np.random.uniform(-1, 1, n)
        noise = np.diff(np.pad(noise, (1, 0))) # bandpass filtering
        env = (np.sin(np.pi * t / dur)) ** 1.6
        return (noise * env * intensity).astype(np.float32)

    # 2. Tactile Cardstock Thud / Pop
    def make_paper_thud(pitch=170.0, dur=0.22, click_intensity=0.55):
        n = int(SR * dur)
        t = np.linspace(0, dur, n, endpoint=False)
        freq = pitch * np.exp(-t * 26.0)
        phase = 2 * np.pi * np.cumsum(freq) / SR
        body = np.sin(phase) * np.exp(-t * 19.0)
        click = np.random.uniform(-1, 1, n) * np.exp(-t * 90.0) * click_intensity
        return ((body * 0.7 + click * 0.45) * 0.75).astype(np.float32)

    # 3. Acoustic Kalimba / Marimba Pluck
    def make_kalimba(freq, dur=0.55, intensity=0.45):
        n = int(SR * dur)
        t = np.linspace(0, dur, n, endpoint=False)
        tone = (np.sin(2 * np.pi * freq * t) + 
                0.28 * np.sin(2 * np.pi * freq * 2.76 * t) +
                0.12 * np.sin(2 * np.pi * freq * 5.42 * t))
        env = np.exp(-t * 6.8)
        strike = np.random.uniform(-1, 1, n) * np.exp(-t * 110.0) * 0.18
        return ((tone * env + strike) * intensity).astype(np.float32)

    # 4. Finger Snap / Paper Tap
    def make_snap(intensity=0.45):
        dur = 0.14
        n = int(SR * dur)
        t = np.linspace(0, dur, n, endpoint=False)
        freq = 1350.0 * np.exp(-t * 45.0)
        phase = 2 * np.pi * np.cumsum(freq) / SR
        tone = np.sin(phase) * np.exp(-t * 38.0)
        noise = np.random.uniform(-1, 1, n) * np.exp(-t * 55.0)
        return ((tone * 0.4 + noise * 0.6) * intensity).astype(np.float32)

    # 5. Grand Paper Stamp (Wax Seal hit)
    def make_stamp(dur=0.65, intensity=0.85):
        n = int(SR * dur)
        t = np.linspace(0, dur, n, endpoint=False)
        sub = np.sin(2 * np.pi * (82.0 * np.exp(-t * 11.0)) * t) * np.exp(-t * 7.5)
        snap = np.random.uniform(-1, 1, n) * np.exp(-t * 38.0) * 0.65
        return ((sub * 0.82 + snap * 0.52) * intensity).astype(np.float32)

    # 6. Glass Bell / Chime (Tech & Elegance)
    def make_bell(freq=1046.5, dur=1.8, intensity=0.38): # C6
        n = int(SR * dur)
        t = np.linspace(0, dur, n, endpoint=False)
        tone = np.sin(2 * np.pi * freq * t) * np.exp(-t * 2.8)
        harm1 = np.sin(2 * np.pi * freq * 2.004 * t) * np.exp(-t * 4.2) * 0.32
        harm2 = np.sin(2 * np.pi * freq * 3.01 * t) * np.exp(-t * 6.0) * 0.15
        return ((tone + harm1 + harm2) * intensity).astype(np.float32)

    # -------------------------------------------------------------
    # SCORE TIMING
    # -------------------------------------------------------------
    # 0.0s - 0.7s: Origami Flap Opening
    add_sound(make_paper_rustle(0.7, 0.75), 0.05, pan=-0.2)
    add_sound(make_paper_rustle(0.6, 0.65), 0.20, pan=0.2)
    add_sound(make_kalimba(392.0, 0.5), 0.35, pan=-0.1) # G4

    # Hook card drop & question
    add_sound(make_paper_thud(150, 0.2), 0.5, pan=0.0)
    add_sound(make_snap(0.4), 0.52, pan=0.0)
    add_sound(make_kalimba(440.0, 0.5), 0.8, pan=0.1) # A4
    add_sound(make_kalimba(523.25, 0.5), 1.2, pan=-0.1) # C5
    add_sound(make_kalimba(659.25, 0.5), 1.6, pan=0.2) # E5

    # 2.4s: Transition to Logo Reveal (Origami Fold Whoosh)
    add_sound(make_paper_rustle(0.5, 0.7), 2.35, pan=-0.3)
    
    # 2.7s: NL Logo Emblem Drop with Big Thud + Chime
    add_sound(make_paper_thud(190, 0.35, 0.75), 2.72, pan=0.0)
    add_sound(make_kalimba(587.33, 0.6, 0.6), 2.72, pan=0.0) # D5
    add_sound(make_snap(0.6), 2.75, pan=0.0)

    # 3.4s: Ribbon "SOLUCIONES 100% A MEDIDA" unfolds
    add_sound(make_paper_rustle(0.35, 0.5), 3.35, pan=0.0)
    add_sound(make_kalimba(783.99, 0.5), 3.45, pan=0.2) # G5

    # 4.0s: Brand text cutout settles
    add_sound(make_paper_thud(160, 0.18), 3.95, pan=0.0)
    add_sound(make_kalimba(880.0, 0.5), 4.10, pan=-0.1) # A5

    # 5.3s - 7.5s: 3 Pop-up Badges appear in sync
    # Badge 1: Chatbots 24/7
    add_sound(make_paper_rustle(0.25, 0.4), 5.25, pan=-0.35)
    add_sound(make_paper_thud(175, 0.18), 5.35, pan=-0.35)
    add_sound(make_kalimba(659.25, 0.5), 5.38, pan=-0.35) # E5
    add_sound(make_snap(0.4), 5.42, pan=-0.35)

    # Badge 2: Flujos n8n
    add_sound(make_paper_rustle(0.25, 0.4), 6.15, pan=0.0)
    add_sound(make_paper_thud(185, 0.18), 6.25, pan=0.0)
    add_sound(make_kalimba(783.99, 0.5), 6.28, pan=0.0) # G5
    add_sound(make_snap(0.4), 6.32, pan=0.0)

    # Badge 3: Ecosistema IA
    add_sound(make_paper_rustle(0.25, 0.4), 7.05, pan=0.35)
    add_sound(make_paper_thud(200, 0.18), 7.15, pan=0.35)
    add_sound(make_kalimba(987.77, 0.5), 7.18, pan=0.35) # B5
    add_sound(make_snap(0.4), 7.22, pan=0.35)

    # 7.9s: Benefit Pill slide
    add_sound(make_paper_rustle(0.3, 0.45), 7.85, pan=0.0)
    add_sound(make_kalimba(1046.5, 0.6), 7.95, pan=0.0) # C6

    # 8.7s: WhatsApp Ticket Slide-in
    add_sound(make_paper_rustle(0.55, 0.8), 8.65, pan=0.0)
    add_sound(make_paper_thud(140, 0.25), 9.05, pan=0.0)

    # 9.5s: Stamp Hit (Seal of Approval)
    add_sound(make_stamp(0.65, 0.95), 9.45, pan=0.2)
    add_sound(make_bell(1046.5, 2.4, 0.55), 9.48, pan=0.1) # C6 crystal bell
    add_sound(make_bell(1318.51, 2.2, 0.35), 9.75, pan=-0.1) # E6 crystal bell

    # Master normalization & limiter
    max_val = max(np.max(np.abs(audio_l)), np.max(np.abs(audio_r)))
    if max_val > 0.01:
        norm = 0.88 / max_val
        audio_l = np.clip(audio_l * norm, -0.98, 0.98)
        audio_r = np.clip(audio_r * norm, -0.98, 0.98)

    # Interleave stereo 16-bit PCM
    stereo = np.empty((total_samples * 2,), dtype=np.int16)
    stereo[0::2] = (audio_l * 32767).astype(np.int16)
    stereo[1::2] = (audio_r * 32767).astype(np.int16)

    with wave.open(OUTPUT_WAV, "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(stereo.tobytes())

    print(f"Soundtrack saved to {OUTPUT_WAV} ({DURATION}s, stereo, 44.1kHz)")

if __name__ == "__main__":
    generate_soundtrack()
