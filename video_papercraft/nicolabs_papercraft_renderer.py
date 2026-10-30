import os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import imageio_ffmpeg
import subprocess

OUTPUT_DIR = "video_papercraft"
ASSETS_DIR = os.path.join(OUTPUT_DIR, "assets")
TEMP_VIDEO = os.path.join(OUTPUT_DIR, "temp_nicolabs.mp4")
FINAL_VIDEO = os.path.join(OUTPUT_DIR, "nicolabs_papercraft_animacion.mp4")
SOUNDTRACK = os.path.join(OUTPUT_DIR, "soundtrack.wav")

WIDTH, HEIGHT = 1080, 1920
FPS = 30
DURATION = 12.0
TOTAL_FRAMES = int(FPS * DURATION) # 360 frames

# -------------------------------------------------------------
# LOAD ASSETS
# -------------------------------------------------------------
bg_cardstock = Image.open(os.path.join(ASSETS_DIR, "bg_cardstock.jpg")).convert("RGB")
logo_emblem = Image.open(os.path.join(ASSETS_DIR, "logo_emblem.png")).convert("RGBA")
brand_text_cutout = Image.open(os.path.join(ASSETS_DIR, "brand_text_cutout.png")).convert("RGBA")
hook_card = Image.open(os.path.join(ASSETS_DIR, "hook_card.png")).convert("RGBA")
paper_ribbon = Image.open(os.path.join(ASSETS_DIR, "paper_ribbon.png")).convert("RGBA")
badge_chatbot = Image.open(os.path.join(ASSETS_DIR, "badge_chatbot.png")).convert("RGBA")
badge_n8n = Image.open(os.path.join(ASSETS_DIR, "badge_n8n.png")).convert("RGBA")
badge_eco = Image.open(os.path.join(ASSETS_DIR, "badge_ecosystem.png")).convert("RGBA")
pill_benefits = Image.open(os.path.join(ASSETS_DIR, "pill_benefits.png")).convert("RGBA")
wa_ticket = Image.open(os.path.join(ASSETS_DIR, "wa_ticket.png")).convert("RGBA")
seal_stamp = Image.open(os.path.join(ASSETS_DIR, "seal_stamp.png")).convert("RGBA")

# -------------------------------------------------------------
# CONFETTI PARTICLES SETUP
# -------------------------------------------------------------
np.random.seed(88)
NUM_CONFETTI = 48
confetti_colors = [
    (0, 180, 216),    # Cyan
    (245, 175, 45),   # Gold
    (250, 250, 255),  # White cardstock
    (40, 195, 110),   # Emerald green
    (245, 150, 40)    # Orange
]
confetti_data = []
for i in range(NUM_CONFETTI):
    angle = np.random.uniform(0, 2 * math.pi)
    speed = np.random.uniform(12, 38)
    confetti_data.append({
        "vx": math.cos(angle) * speed,
        "vy": math.sin(angle) * speed - 6.0,
        "rot": np.random.uniform(0, 360),
        "v_rot": np.random.uniform(-14, 14),
        "size": np.random.uniform(12, 22),
        "shape": np.random.choice(["rect", "circle", "tri"]),
        "color": confetti_colors[i % len(confetti_colors)]
    })

# -------------------------------------------------------------
# EASING FUNCTIONS
# -------------------------------------------------------------
def ease_out_back(x, c1=1.70158):
    c3 = c1 + 1.0
    return 1.0 + c3 * ((x - 1.0) ** 3) + c1 * ((x - 1.0) ** 2)

def ease_out_elastic(x):
    if x == 0: return 0
    if x >= 1: return 1
    c4 = (2.0 * math.pi) / 3.0
    return (2.0 ** (-10.0 * x)) * math.sin((x * 10.0 - 0.75) * c4) + 1.0

def ease_in_out(x):
    return -(math.cos(math.pi * x) - 1.0) / 2.0

# -------------------------------------------------------------
# PAPERCRAFT SHADOW MAKER
# -------------------------------------------------------------
def make_paper_shadow(alpha_channel, elevation=15, blur_mult=0.7, shadow_alpha=120):
    dx = int(elevation * 0.55)
    dy = int(elevation * 0.90)
    
    pad = int(elevation * 2) + 20
    sw = alpha_channel.width + abs(dx) + pad
    sh = alpha_channel.height + abs(dy) + pad
    
    shadow = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    black_shape = Image.new("RGBA", alpha_channel.size, (10, 18, 25, shadow_alpha))
    black_shape.putalpha(alpha_channel)
    
    paste_x = pad // 2 + max(0, dx)
    paste_y = pad // 2 + max(0, dy)
    shadow.paste(black_shape, (paste_x, paste_y), black_shape)
    
    blur_r = max(1, int(elevation * blur_mult))
    return shadow.filter(ImageFilter.GaussianBlur(blur_r)), paste_x - dx, paste_y - dy

def paste_with_shadow(canvas, img, x, y, elevation=15, shadow_alpha=120):
    alpha = img.split()[-1]
    if alpha.getextrema() == (0, 0):
        return
    shadow, off_x, off_y = make_paper_shadow(alpha, elevation=elevation, shadow_alpha=shadow_alpha)
    canvas.paste(shadow, (x - off_x, y - off_y), shadow)
    canvas.paste(img, (x, y), img)

# -------------------------------------------------------------
# CONFETTI DRAWER
# -------------------------------------------------------------
def draw_confetti(draw, f, start_frame=10):
    if f < start_frame: return
    t = f - start_frame
    for c in confetti_data:
        cx = (WIDTH // 2) + c["vx"] * t * 0.75
        cy = (HEIGHT // 2 - 150) + c["vy"] * t * 0.75 + 0.38 * (t ** 1.6)
        if cy > HEIGHT + 40 or cx < -40 or cx > WIDTH + 40:
            continue
        s = c["size"]
        # Drop shadow
        draw.ellipse([cx - s/2 + 3, cy - s/2 + 4, cx + s/2 + 3, cy + s/2 + 4], fill=(0, 0, 0, 45))
        if c["shape"] == "circle":
            draw.ellipse([cx - s/2, cy - s/2, cx + s/2, cy + s/2], fill=c["color"])
        elif c["shape"] == "rect":
            draw.rectangle([cx - s/2, cy - s/3, cx + s/2, cy + s/3], fill=c["color"])
        else:
            p1 = (cx, cy - s/2)
            p2 = (cx - s/2, cy + s/2)
            p3 = (cx + s/2, cy + s/2)
            draw.polygon([p1, p2, p3], fill=c["color"])

# -------------------------------------------------------------
# MAIN FRAME RENDERER
# -------------------------------------------------------------
def render_frame(f):
    canvas = bg_cardstock.copy()
    draw_main = ImageDraw.Draw(canvas)

    # 1. ORIGAMI FLAPS OPENING (Frames 0 to 22)
    if f < 22:
        flap_p = f / 22.0
        flap_layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        d_flap = ImageDraw.Draw(flap_layer)
        # Left triangle flap folding away
        lx = int((1.0 - flap_p) * (WIDTH // 2))
        d_flap.polygon([(0, 0), (lx, HEIGHT // 2), (0, HEIGHT)], fill=(20, 45, 65, int((1.0 - flap_p) * 255)))
        # Right triangle flap
        rx = WIDTH - int((1.0 - flap_p) * (WIDTH // 2))
        d_flap.polygon([(WIDTH, 0), (rx, HEIGHT // 2), (WIDTH, HEIGHT)], fill=(26, 56, 80, int((1.0 - flap_p) * 255)))
        canvas.paste(flap_layer, (0, 0), flap_layer)

    # 2. CONFETTI BURST (Frames 10 to 80)
    draw_confetti(draw_main, f, start_frame=10)

    # ---------------------------------------------------------
    # SCENE 1: HOOK CARD (Frames 12 to 74)
    # "¿Seguís perdiendo horas en planillas y tareas repetitivas?"
    # ---------------------------------------------------------
    if 12 <= f < 75:
        # Drop in from top
        if f < 35:
            p = (f - 12) / 23.0
            y_curr = int(-hook_card.height + (360 + hook_card.height) * ease_out_elastic(p))
            alpha_mult = min(1.0, p * 2.0)
            elev = int(8 + 25 * (1.0 - p))
        elif f >= 65:
            # Slide out up
            p = (f - 65) / 10.0
            y_curr = int(360 - 550 * (p ** 2))
            alpha_mult = max(0.0, 1.0 - p)
            elev = 15
        else:
            y_curr = 360 + int(math.sin((f - 35) * 0.15) * 3) # subtle float
            alpha_mult = 1.0
            elev = 18

        hk_x = (WIDTH - hook_card.width) // 2
        paste_with_shadow(canvas, hook_card, hk_x, y_curr, elevation=elev, shadow_alpha=int(120 * alpha_mult))

    # ---------------------------------------------------------
    # SCENE 2: LOGO EMBLEM & BRAND (Frames 72 to 360)
    # ---------------------------------------------------------
    if f >= 72:
        # Determine base vertical position of logo
        # In Scene 2 (72 to 155), logo is prominent in center: Y = 320
        # In Scene 3 (155+), logo slides up to Y = 130 to give space to Badges and Ticket!
        if f < 96:
            p = (f - 72) / 24.0
            p_e = ease_out_back(min(1.0, p), c1=1.4)
            logo_y = int(-logo_emblem.height + (320 + logo_emblem.height) * p_e)
            logo_elev = int(12 + 35 * (1.0 - min(1.0, p)))
        elif f < 155:
            logo_y = 320 + int(math.sin((f - 96) * 0.12) * 4)
            logo_elev = 22
        elif f < 185:
            p_up = ease_in_out((f - 155) / 30.0)
            logo_y = int(320 - (320 - 130) * p_up)
            logo_elev = 20
        else:
            logo_y = 130 + int(math.sin((f - 185) * 0.08) * 3)
            logo_elev = 20

        # When logo slides up, we can scale it down slightly (85%) so it fits beautifully
        if f >= 155:
            scale_fac = max(0.82, 1.0 - 0.18 * ((f - 155) / 30.0)) if f < 185 else 0.82
            cur_logo_w = int(logo_emblem.width * scale_fac)
            cur_logo_h = int(logo_emblem.height * scale_fac)
            active_logo = logo_emblem.resize((cur_logo_w, cur_logo_h), Image.Resampling.LANCZOS)
        else:
            active_logo = logo_emblem

        logo_x = (WIDTH - active_logo.width) // 2
        paste_with_shadow(canvas, active_logo, logo_x, logo_y, elevation=logo_elev, shadow_alpha=130)

        # PAPER RIBBON ("SOLUCIONES 100% A MEDIDA")
        # Appears at frame 94
        if f >= 94 and f < 165:
            p_rib = min(1.0, (f - 94) / 18.0)
            rib_w = int(paper_ribbon.width * ease_out_back(p_rib, c1=1.2))
            if rib_w > 10:
                cur_rib = paper_ribbon.resize((rib_w, paper_ribbon.height), Image.Resampling.BILINEAR)
                rib_x = (WIDTH - cur_rib.width) // 2
                rib_y = logo_y + active_logo.height + 25
                paste_with_shadow(canvas, cur_rib, rib_x, rib_y, elevation=14, shadow_alpha=110)

        # BRAND TEXT CUTOUT ("NICO LABS - Automatizaciones con IA")
        # Appears at frame 110
        if f >= 110 and f < 165:
            p_bt = min(1.0, (f - 110) / 16.0)
            bt_y = int(logo_y + active_logo.height + paper_ribbon.height + 35)
            bt_x = (WIDTH - brand_text_cutout.width) // 2
            paste_with_shadow(canvas, brand_text_cutout, bt_x, bt_y, elevation=12, shadow_alpha=100)

    # ---------------------------------------------------------
    # SCENE 3: SOLUTION BADGES (Frames 158 to 360)
    # Chatbots 24/7, Flujos n8n, Ecosistemas IA
    # ---------------------------------------------------------
    badge_list = [
        (badge_chatbot, 160, 185), # (badge, start_f, target_cx)
        (badge_n8n, 185, 540),
        (badge_eco, 210, 895)
    ]

    # Target Y for badges
    # Between 160 and 260: badges at Y = 710
    # From 260+: badges slightly lift to Y = 620 to let the WhatsApp ticket have focus
    if f >= 260:
        p_b_lift = min(1.0, (f - 260) / 20.0)
        badge_base_y = int(710 - 75 * ease_in_out(p_b_lift))
    else:
        badge_base_y = 710

    for badge_img, start_f, target_cx in badge_list:
        if f >= start_f:
            p = min(1.0, (f - start_f) / 18.0)
            p_scale = ease_out_elastic(p)
            
            # Wobble angle
            angle = math.sin((1.0 - p) * math.pi * 3.0) * 12.0
            
            bw = max(10, int(badge_img.width * p_scale))
            bh = max(10, int(badge_img.height * p_scale))
            
            b_scaled = badge_img.resize((bw, bh), Image.Resampling.LANCZOS)
            if abs(angle) > 0.5:
                b_rot = b_scaled.rotate(angle, resample=Image.Resampling.BICUBIC, expand=True)
            else:
                b_rot = b_scaled
                
            bx = int(target_cx - b_rot.width // 2)
            by = int(badge_base_y - b_rot.height // 2)
            paste_with_shadow(canvas, b_rot, bx, by, elevation=16, shadow_alpha=120)

    # BENEFIT PILL: "Pagás por uso real • Sin costos de software"
    # Appears at frame 230
    if f >= 230:
        p_pill = min(1.0, (f - 230) / 16.0)
        pill_y = int(badge_base_y + 195)
        pill_x = (WIDTH - pill_benefits.width) // 2
        
        # Scale in horizontally
        cur_pw = max(10, int(pill_benefits.width * ease_out_back(p_pill, c1=1.1)))
        pill_scaled = pill_benefits.resize((cur_pw, pill_benefits.height), Image.Resampling.BILINEAR)
        cur_px = (WIDTH - pill_scaled.width) // 2
        paste_with_shadow(canvas, pill_scaled, cur_px, pill_y, elevation=12, shadow_alpha=100)

    # ---------------------------------------------------------
    # SCENE 4: WHATSAPP CTA TICKET & GOLD SEAL (Frames 255 to 360)
    # ---------------------------------------------------------
    if f >= 255:
        p_ticket = min(1.0, (f - 255) / 25.0)
        p_t_ease = ease_out_back(p_ticket, c1=1.2)
        
        # Slide in from bottom
        target_t_y = 1260
        t_y = int(HEIGHT + 50 - (HEIGHT + 50 - target_t_y) * p_t_ease)
        t_x = (WIDTH - wa_ticket.width) // 2
        
        # Subtle rope pendulum wobble as it hangs
        t_wobble = math.sin((f - 255) * 0.14) * 2.0 if f < 310 else math.sin((f - 255) * 0.08) * 0.8
        ticket_rot = wa_ticket.rotate(t_wobble, resample=Image.Resampling.BICUBIC, expand=True)
        tx_corr = t_x - (ticket_rot.width - wa_ticket.width) // 2
        ty_corr = t_y - (ticket_rot.height - wa_ticket.height) // 2
        
        # Two hanging suspension threads from top cardstock
        thread_color = (240, 200, 120, 180)
        draw_main.line([(t_x + 90, 0), (t_x + 90, t_y)], fill=thread_color, width=2)
        draw_main.line([(t_x + wa_ticket.width - 90, 0), (t_x + wa_ticket.width - 90, t_y)], fill=thread_color, width=2)
        
        paste_with_shadow(canvas, ticket_rot, tx_corr, ty_corr, elevation=24, shadow_alpha=140)

        # GOLD FOIL WAX SEAL STAMP (Hits ticket at frame 285 / 9.5s)
        if f >= 282:
            p_seal = min(1.0, (f - 282) / 10.0)
            seal_target_x = t_x + wa_ticket.width - seal_stamp.width + 45
            seal_target_y = t_y - 65
            
            if p_seal < 1.0:
                # Stamp dropping with impact bounce
                scale_s = 2.4 - 1.4 * ease_out_elastic(p_seal)
                cur_sw = int(seal_stamp.width * scale_s)
                cur_sh = int(seal_stamp.height * scale_s)
                active_seal = seal_stamp.resize((cur_sw, cur_sh), Image.Resampling.LANCZOS)
                sx = seal_target_x - (cur_sw - seal_stamp.width) // 2
                sy = seal_target_y - (cur_sh - seal_stamp.height) // 2
                paste_with_shadow(canvas, active_seal, sx, sy, elevation=35, shadow_alpha=160)
            else:
                paste_with_shadow(canvas, seal_stamp, seal_target_x, seal_target_y, elevation=18, shadow_alpha=130)

    # ---------------------------------------------------------
    # FINAL POLISH: Subtle light shimmer or vignette
    # ---------------------------------------------------------
    return canvas

# -------------------------------------------------------------
# VIDEO COMPILATION
# -------------------------------------------------------------
def render_full_video():
    print(f"Starting rendering of {TOTAL_FRAMES} frames ({WIDTH}x{HEIGHT} at {FPS} FPS)...")
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    
    # 1. Render frames to temp MP4 via FFmpeg pipe
    cmd = [
        ffmpeg_exe,
        "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}",
        "-pix_fmt", "rgb24",
        "-r", str(FPS),
        "-i", "-",
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        TEMP_VIDEO
    ]
    
    pipe = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    
    # Also save a few thumbnails for inspection
    thumb_frames = {
        18: "thumb_01_origami.jpg",
        45: "thumb_02_hook_card.jpg",
        125: "thumb_03_logo_reveal.jpg",
        225: "thumb_04_badges_popup.jpg",
        320: "thumb_05_ticket_whatsapp_cta.jpg"
    }
    os.makedirs(os.path.join(OUTPUT_DIR, "thumbnails"), exist_ok=True)

    for f in range(TOTAL_FRAMES):
        frame_img = render_frame(f)
        pipe.stdin.write(frame_img.tobytes())
        
        if f in thumb_frames:
            thumb_path = os.path.join(OUTPUT_DIR, "thumbnails", thumb_frames[f])
            frame_img.save(thumb_path, quality=90)
            print(f"Saved keyframe snapshot: {thumb_frames[f]}")
            
        if (f + 1) % 45 == 0 or f == TOTAL_FRAMES - 1:
            print(f"Rendered {f + 1}/{TOTAL_FRAMES} frames ({((f+1)/TOTAL_FRAMES)*100:.1f}%)")

    pipe.stdin.close()
    pipe.wait()
    print(f"Video stream finished: {TEMP_VIDEO}")

    # 2. Merge Video with Audio Soundtrack into FINAL_VIDEO
    print("Merging video with soundtrack...")
    merge_cmd = [
        ffmpeg_exe,
        "-y",
        "-i", TEMP_VIDEO,
        "-i", SOUNDTRACK,
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        FINAL_VIDEO
    ]
    subprocess.run(merge_cmd, check=True)
    print(f"FINAL VIDEO CREATED: {FINAL_VIDEO}")

    # Print final size
    size_mb = os.path.getsize(FINAL_VIDEO) / (1024 * 1024)
    print(f"Final video size: {size_mb:.2f} MB")

if __name__ == "__main__":
    render_full_video()
