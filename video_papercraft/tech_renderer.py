import os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import imageio_ffmpeg
import subprocess

OUTPUT_DIR = "video_papercraft"
ASSETS_DIR = os.path.join(OUTPUT_DIR, "assets")
TEMP_VIDEO = os.path.join(OUTPUT_DIR, "temp_tech_nicolabs.mp4")
FINAL_VIDEO = os.path.join(OUTPUT_DIR, "nicolabs_papercraft_animacion.mp4")
SOUNDTRACK = os.path.join(OUTPUT_DIR, "tech_soundtrack.wav")

WIDTH, HEIGHT = 1080, 1920
FPS = 30
DURATION = 12.0
TOTAL_FRAMES = int(FPS * DURATION) # 360 frames

# -------------------------------------------------------------
# LOAD ASSETS
# -------------------------------------------------------------
bg_cyber = Image.open(os.path.join(ASSETS_DIR, "bg_cyber.jpg")).convert("RGB")
master_logo_card = Image.open(os.path.join(ASSETS_DIR, "master_logo_card.png")).convert("RGBA")
hook_glass_card = Image.open(os.path.join(ASSETS_DIR, "hook_glass_card.png")).convert("RGBA")
tech_hud_ribbon = Image.open(os.path.join(ASSETS_DIR, "tech_hud_ribbon.png")).convert("RGBA")
node_chat = Image.open(os.path.join(ASSETS_DIR, "tech_node_chatbot.png")).convert("RGBA")
node_n8n = Image.open(os.path.join(ASSETS_DIR, "tech_node_n8n.png")).convert("RGBA")
node_eco = Image.open(os.path.join(ASSETS_DIR, "tech_node_eco.png")).convert("RGBA")
tech_pill = Image.open(os.path.join(ASSETS_DIR, "tech_pill_pricing.png")).convert("RGBA")
vip_pass = Image.open(os.path.join(ASSETS_DIR, "tech_vip_pass.png")).convert("RGBA")
holo_seal = Image.open(os.path.join(ASSETS_DIR, "tech_holo_seal.png")).convert("RGBA")

# -------------------------------------------------------------
# NEURAL NETWORK REASONING ENGINE (Flujo Dinámico de Razonamiento)
# -------------------------------------------------------------
np.random.seed(101)
NUM_NODES = 28
nodes_data = []

# Distribute nodes across the screen with natural clustering
for i in range(NUM_NODES):
    nodes_data.append({
        "id": i,
        "base_x": np.random.uniform(70, WIDTH - 70),
        "base_y": np.random.uniform(90, HEIGHT - 90),
        "drift_phase": np.random.uniform(0, math.pi * 2),
        "r": np.random.uniform(3.5, 6.0),
        "last_flash_frame": -100
    })

# Build network edge graph (nodes within distance < 250px)
edges = []
for i in range(NUM_NODES):
    for j in range(i + 1, NUM_NODES):
        dx = nodes_data[i]["base_x"] - nodes_data[j]["base_x"]
        dy = nodes_data[i]["base_y"] - nodes_data[j]["base_y"]
        d = math.hypot(dx, dy)
        if 80 < d < 250:
            edges.append((i, j))

# Synaptic Reasoning Streams: 7 continuous thinking paths
COLOR_PALETTE = [
    np.array([0, 240, 255]),    # Electric Cyan
    np.array([255, 0, 190]),    # Neon Magenta
    np.array([185, 75, 255]),   # Electric Violet
    np.array([245, 250, 255])   # Pure Silver White
]

def get_synaptic_color(val):
    v = (val % 1.0) * len(COLOR_PALETTE)
    idx1 = int(v) % len(COLOR_PALETTE)
    idx2 = (idx1 + 1) % len(COLOR_PALETTE)
    frac = v - int(v)
    c = (1.0 - frac) * COLOR_PALETTE[idx1] + frac * COLOR_PALETTE[idx2]
    return int(c[0]), int(c[1]), int(c[2])

# Pre-generate reasoning flow steps
NUM_STREAMS = 7
STREAM_SPEED = 18 # frames per jump
streams = []
for s_id in range(NUM_STREAMS):
    # Pick a random starting edge
    edge = edges[s_id % len(edges)]
    streams.append({
        "from_node": edge[0],
        "to_node": edge[1],
        "phase_offset": s_id * (TOTAL_FRAMES // NUM_STREAMS),
        "color_shift": s_id * 0.22
    })

# -------------------------------------------------------------
# EASING FUNCTIONS
# -------------------------------------------------------------
def ease_out_back(x, c1=1.4):
    c3 = c1 + 1.0
    return 1.0 + c3 * ((x - 1.0) ** 3) + c1 * ((x - 1.0) ** 2)

def ease_out_elastic(x):
    if x <= 0: return 0
    if x >= 1: return 1
    c4 = (2.0 * math.pi) / 3.0
    return (2.0 ** (-10.0 * x)) * math.sin((x * 10.0 - 0.75) * c4) + 1.0

def ease_in_out(x):
    return -(math.cos(math.pi * x) - 1.0) / 2.0

# -------------------------------------------------------------
# HIGH-TECH SHADOW / GLOW MAKER
# -------------------------------------------------------------
def paste_tech_card(canvas, img, x, y, glow_color=(0, 180, 216), glow_radius=18, elevation=15):
    alpha = img.split()[-1]
    if alpha.getextrema() == (0, 0):
        return
    
    pad = elevation * 2 + 25
    dx = int(elevation * 0.4)
    dy = int(elevation * 0.9)
    sw = img.width + abs(dx) + pad
    sh = img.height + abs(dy) + pad
    
    shadow = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    black_shape = Image.new("RGBA", img.size, (4, 10, 18, 140))
    black_shape.putalpha(alpha)
    
    paste_x = pad // 2 + max(0, dx)
    paste_y = pad // 2 + max(0, dy)
    shadow.paste(black_shape, (paste_x, paste_y), black_shape)
    shadow_blur = shadow.filter(ImageFilter.GaussianBlur(max(2, int(elevation * 0.8))))
    
    canvas.paste(shadow_blur, (x - paste_x + dx, y - paste_y + dy), shadow_blur)
    
    if glow_radius > 0:
        glow_layer = Image.new("RGBA", (img.width + 40, img.height + 40), (0, 0, 0, 0))
        glow_shape = Image.new("RGBA", img.size, (glow_color[0], glow_color[1], glow_color[2], 65))
        glow_shape.putalpha(alpha)
        glow_layer.paste(glow_shape, (20, 20), glow_shape)
        glow_blurred = glow_layer.filter(ImageFilter.GaussianBlur(glow_radius))
        canvas.paste(glow_blurred, (x - 20, y - 20), glow_blurred)
        
    canvas.paste(img, (x, y), img)

# -------------------------------------------------------------
# SPECULAR LIGHT SWEEP (Metal & Glass Shimmer effect)
# -------------------------------------------------------------
def apply_shimmer(img, sweep_progress):
    if sweep_progress < 0.0 or sweep_progress > 1.0:
        return img
    
    w, h = img.size
    shimmer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d_sh = ImageDraw.Draw(shimmer)
    
    beam_center_x = int((w + h) * sweep_progress - h * 0.5)
    beam_w = 90
    
    points = [
        (beam_center_x - beam_w, 0),
        (beam_center_x + beam_w, 0),
        (beam_center_x + beam_w - h * 0.6, h),
        (beam_center_x - beam_w - h * 0.6, h)
    ]
    d_sh.polygon(points, fill=(255, 255, 255, 75))
    shimmer = shimmer.filter(ImageFilter.GaussianBlur(18))
    
    alpha = img.split()[-1]
    shimmer.putalpha(Image.composite(shimmer.split()[-1], Image.new("L", (w, h), 0), alpha))
    
    out = img.copy()
    out.paste(shimmer, (0, 0), shimmer)
    return out

# -------------------------------------------------------------
# MAIN FRAME RENDERER
# -------------------------------------------------------------
def render_frame(f):
    canvas = bg_cyber.copy()
    draw_main = ImageDraw.Draw(canvas)

    # 1. COMPUTE POSITIONS OF DRIFTING NEURAL NODES
    t = f / float(FPS)
    current_node_coords = {}
    for n in nodes_data:
        cur_x = int(n["base_x"] + math.sin(t * 0.9 + n["drift_phase"]) * 18)
        cur_y = int(n["base_y"] + math.cos(t * 0.7 + n["drift_phase"]) * 18)
        current_node_coords[n["id"]] = (cur_x, cur_y)

    # 2. DRAW BASE RESTING CONNECTIONS (Soft subtle cyber web)
    for n1_id, n2_id in edges:
        p1 = current_node_coords[n1_id]
        p2 = current_node_coords[n2_id]
        dist = math.hypot(p1[0] - p2[0], p1[1] - p2[1])
        alpha_base = int(max(10, (1.0 - dist / 250.0) * 40))
        draw_main.line([p1, p2], fill=(0, 180, 220, alpha_base), width=1)

    # 3. DRAW DYNAMIC SYNAPTIC REASONING STREAMS (Flujo de Razonamiento)
    for s_idx, stream in enumerate(streams):
        # Progress of current jump (0.0 to 1.0)
        local_f = (f + stream["phase_offset"]) % (STREAM_SPEED * 8)
        jump_idx = int(local_f // STREAM_SPEED)
        progress = (local_f % STREAM_SPEED) / float(STREAM_SPEED)
        
        # Determine edge for current step
        edge_idx = (s_idx * 3 + jump_idx) % len(edges)
        node_a, node_b = edges[edge_idx]
        pa = current_node_coords[node_a]
        pb = current_node_coords[node_b]
        
        # Color evolution: cyan -> magenta -> violet -> silver
        color_val = (t * 0.25 + stream["color_shift"]) % 1.0
        c_rgb = get_synaptic_color(color_val)
        
        # A) Line illuminating from pa to current position
        head_x = int(pa[0] + (pb[0] - pa[0]) * progress)
        head_y = int(pa[1] + (pb[1] - pa[1]) * progress)
        
        # Glowing illuminated line segment
        draw_main.line([pa, (head_x, head_y)], fill=(c_rgb[0], c_rgb[1], c_rgb[2], 160), width=2)
        
        # B) Glowing Spark / Energy Packet at head
        spark_r = 5.5
        draw_main.ellipse([head_x - spark_r - 2, head_y - spark_r - 2, head_x + spark_r + 2, head_y + spark_r + 2], 
                          fill=(c_rgb[0], c_rgb[1], c_rgb[2], 90))
        draw_main.ellipse([head_x - spark_r, head_y - spark_r, head_x + spark_r, head_y + spark_r], 
                          fill=(255, 255, 255, 240))
        
        # C) When progress is close to 1.0, destination node flashes!
        if progress > 0.85:
            flash_mult = (progress - 0.85) / 0.15
            ring_r = int(12 + flash_mult * 18)
            draw_main.ellipse([pb[0] - ring_r, pb[1] - ring_r, pb[0] + ring_r, pb[1] + ring_r], 
                              outline=(c_rgb[0], c_rgb[1], c_rgb[2], int((1.0 - flash_mult) * 200)), width=2)

    # 4. DRAW NODES (Glowing hubs with halos)
    for n in nodes_data:
        nx, ny = current_node_coords[n["id"]]
        r = n["r"]
        # Ambient node dot
        draw_main.ellipse([nx - r - 2, ny - r - 2, nx + r + 2, ny + r + 2], fill=(0, 200, 240, 50))
        draw_main.ellipse([nx - r, ny - r, nx + r, ny + r], fill=(0, 240, 255, 210))
        # White center core
        draw_main.ellipse([nx - 1.5, ny - 1.5, nx + 1.5, ny + 1.5], fill=(255, 255, 255, 240))

    # ---------------------------------------------------------
    # SCENE 1: HOOK GLASSMORPHIC CARD (Frames 0 to 74, 0.0s - 2.5s)
    # "¿Tu negocio sigue frenado por planillas y procesos manuales?"
    # ---------------------------------------------------------
    if f < 75:
        if f < 25:
            p = f / 25.0
            p_e = ease_out_back(p, c1=1.2)
            cur_w = max(10, int(hook_glass_card.width * p_e))
            cur_h = max(10, int(hook_glass_card.height * p_e))
            active_hk = hook_glass_card.resize((cur_w, cur_h), Image.Resampling.LANCZOS)
            hk_x = (WIDTH - cur_w) // 2
            hk_y = int(580 - (cur_h // 2))
            glow_r = int(28 * p)
            elev = int(20 * p)
        elif f >= 65:
            p = (f - 65) / 10.0
            scale_out = 1.0 + p * 0.15
            cur_w = int(hook_glass_card.width * scale_out)
            cur_h = int(hook_glass_card.height * scale_out)
            active_hk = hook_glass_card.resize((cur_w, cur_h), Image.Resampling.BILINEAR)
            alpha_hk = active_hk.split()[-1]
            fade_mask = Image.fromarray((np.array(alpha_hk) * (1.0 - p)).astype(np.uint8))
            active_hk.putalpha(fade_mask)
            hk_x = (WIDTH - cur_w) // 2
            hk_y = int(580 - (cur_h // 2))
            glow_r = int(20 * (1.0 - p))
            elev = 15
        else:
            active_hk = hook_glass_card
            hk_x = (WIDTH - hook_glass_card.width) // 2
            hk_y = 400 + int(math.sin((f - 25) * 0.12) * 4)
            glow_r = 24
            elev = 18

        if 25 <= f < 65:
            scan_p = (f - 25) / 40.0
            scan_y = int(hk_y + active_hk.height * scan_p)
            draw_main.line([(hk_x + 20, scan_y), (hk_x + active_hk.width - 20, scan_y)], fill=(0, 245, 255, 160), width=2)

        paste_tech_card(canvas, active_hk, hk_x, hk_y, glow_color=(0, 200, 240), glow_radius=glow_r, elevation=elev)

    # ---------------------------------------------------------
    # SCENE 2: MASTER 3D LOGO & CYBER HUD (Frames 72 to 360)
    # ---------------------------------------------------------
    if f >= 72:
        if f < 96:
            p = (f - 72) / 24.0
            p_e = ease_out_back(min(1.0, p), c1=1.3)
            scale_l = 0.5 + 0.5 * p_e
            target_w = int(master_logo_card.width * scale_l)
            target_h = int(master_logo_card.height * scale_l)
            active_logo = master_logo_card.resize((target_w, target_h), Image.Resampling.LANCZOS)
            logo_y = int(100 + (280 - 100) * p_e)
            logo_elev = int(25 * min(1.0, p))
            glow_l = int(32 * min(1.0, p))
        elif f < 155:
            active_logo = master_logo_card
            logo_y = 280 + int(math.sin((f - 96) * 0.09) * 4)
            logo_elev = 22
            glow_l = 30
        elif f < 185:
            p_up = ease_in_out((f - 155) / 30.0)
            scale_l = 1.0 - 0.35 * p_up
            target_w = int(master_logo_card.width * scale_l)
            target_h = int(master_logo_card.height * scale_l)
            active_logo = master_logo_card.resize((target_w, target_h), Image.Resampling.LANCZOS)
            logo_y = int(280 - (280 - 80) * p_up)
            logo_elev = 18
            glow_l = 22
        else:
            scale_l = 0.65
            target_w = int(master_logo_card.width * scale_l)
            target_h = int(master_logo_card.height * scale_l)
            active_logo = master_logo_card.resize((target_w, target_h), Image.Resampling.LANCZOS)
            logo_y = 80 + int(math.sin((f - 185) * 0.08) * 3)
            logo_elev = 18
            glow_l = 20

        logo_x = (WIDTH - active_logo.width) // 2

        if 95 <= f <= 135:
            shimmer_p = (f - 95) / 40.0
            active_logo = apply_shimmer(active_logo, shimmer_p)

        paste_tech_card(canvas, active_logo, logo_x, logo_y, glow_color=(0, 210, 255), glow_radius=glow_l, elevation=logo_elev)

        if 94 <= f < 165:
            p_rib = min(1.0, (f - 94) / 18.0)
            rib_w = max(10, int(tech_hud_ribbon.width * ease_out_back(p_rib, c1=1.2)))
            active_rib = tech_hud_ribbon.resize((rib_w, tech_hud_ribbon.height), Image.Resampling.BILINEAR)
            rib_x = (WIDTH - active_rib.width) // 2
            rib_y = logo_y + active_logo.height + 30
            paste_tech_card(canvas, active_rib, rib_x, rib_y, glow_color=(0, 220, 255), glow_radius=20, elevation=14)

    # ---------------------------------------------------------
    # SCENE 3: THREE SOLUTION TECH NODES (Frames 155 to 360)
    # Chatbot 24/7, Flujos n8n, Ecosistemas 360°
    # ---------------------------------------------------------
    nodes_cfg = [
        (node_chat, 158, 45),
        (node_n8n, 180, 380),
        (node_eco, 202, 715)
    ]

    if f >= 255:
        p_lift = min(1.0, (f - 255) / 22.0)
        base_node_y = int(660 - 70 * ease_in_out(p_lift))
    else:
        base_node_y = 660

    rendered_node_centers = []
    for node_img, start_f, target_x in nodes_cfg:
        if f >= start_f:
            p = min(1.0, (f - start_f) / 18.0)
            p_scale = ease_out_elastic(p)
            tilt = math.sin((f - start_f) * 0.12) * 1.5 if p >= 1.0 else (1.0 - p) * -8.0
            
            nw = max(10, int(node_img.width * p_scale))
            nh = max(10, int(node_img.height * p_scale))
            node_scaled = node_img.resize((nw, nh), Image.Resampling.LANCZOS)
            
            if abs(tilt) > 0.4:
                node_rot = node_scaled.rotate(tilt, resample=Image.Resampling.BICUBIC, expand=True)
            else:
                node_rot = node_scaled
                
            cur_nx = target_x - (node_rot.width - node_img.width) // 2
            cur_ny = base_node_y - (node_rot.height - node_img.height) // 2
            
            paste_tech_card(canvas, node_rot, cur_nx, cur_ny, glow_color=(0, 200, 240), glow_radius=18, elevation=16)
            rendered_node_centers.append((target_x + node_img.width // 2, base_node_y + 180))

    if len(rendered_node_centers) >= 2:
        for k in range(len(rendered_node_centers) - 1):
            p_a = rendered_node_centers[k]
            p_b = rendered_node_centers[k + 1]
            draw_main.line([p_a, p_b], fill=(0, 240, 255, 120), width=2)
            dot_p = ((f * 3 + k * 30) % 60) / 60.0
            dot_x = int(p_a[0] + (p_b[0] - p_a[0]) * dot_p)
            dot_y = int(p_a[1] + (p_b[1] - p_a[1]) * dot_p)
            draw_main.ellipse([dot_x - 5, dot_y - 5, dot_x + 5, dot_y + 5], fill=(255, 255, 255, 240))

    if f >= 225:
        p_pill = min(1.0, (f - 225) / 16.0)
        pill_y = base_node_y + 495
        pill_w = max(10, int(tech_pill.width * ease_out_back(p_pill, c1=1.2)))
        active_pill = tech_pill.resize((pill_w, tech_pill.height), Image.Resampling.BILINEAR)
        pill_x = (WIDTH - active_pill.width) // 2
        paste_tech_card(canvas, active_pill, pill_x, pill_y, glow_color=(0, 210, 255), glow_radius=16, elevation=12)

    # ---------------------------------------------------------
    # SCENE 4: VIP TECH PASS & WHATSAPP RADAR CTA (Frames 255 to 360)
    # ---------------------------------------------------------
    if f >= 255:
        p_vip = min(1.0, (f - 255) / 24.0)
        p_vip_ease = ease_out_back(p_vip, c1=1.25)
        
        target_vip_y = 1270
        vip_y = int(HEIGHT + 40 - (HEIGHT + 40 - target_vip_y) * p_vip_ease)
        vip_x = (WIDTH - vip_pass.width) // 2
        
        if p_vip >= 1.0:
            vip_y += int(math.sin((f - 280) * 0.1) * 3)
            
        paste_tech_card(canvas, vip_pass, vip_x, vip_y, glow_color=(37, 211, 102), glow_radius=28, elevation=24)

        # Dynamic glowing radar scanline on the WhatsApp button
        btn_local_x = 195
        btn_local_y = 125
        btn_w = vip_pass.width - 35 - btn_local_x
        btn_h = 85
        btn_abs_x = vip_x + btn_local_x
        btn_abs_y = vip_y + btn_local_y
        
        scan_offset = ((f * 6) % int(btn_w + 60)) - 30
        scan_x1 = int(btn_abs_x + scan_offset)
        if btn_abs_x <= scan_x1 <= btn_abs_x + btn_w:
            draw_main.line([(scan_x1, btn_abs_y + 4), (scan_x1, btn_abs_y + btn_h - 4)], fill=(255, 255, 255, 180), width=3)

        # MINTED METALLIC GOLD SEAL (Compact, elegantly framed in upper right corner, no text overlap!)
        if f >= 282:
            p_seal = min(1.0, (f - 282) / 12.0)
            
            # Compact display size: 145x145
            seal_disp_w, seal_disp_h = 145, 145
            compact_seal = holo_seal.resize((seal_disp_w, seal_disp_h), Image.Resampling.LANCZOS)
            
            # Position at top-right edge of the pass (X=840, Y=1235) perfectly clear of any text!
            seal_target_x = vip_x + vip_pass.width - seal_disp_w - 20
            seal_target_y = vip_y - 25
            
            if p_seal < 1.0:
                scale_s = 1.8 - 0.8 * ease_out_elastic(p_seal)
                cur_sw = int(seal_disp_w * scale_s)
                cur_sh = int(seal_disp_h * scale_s)
                active_seal = compact_seal.resize((cur_sw, cur_sh), Image.Resampling.LANCZOS)
                rot_deg = (1.0 - p_seal) * 120
                active_seal = active_seal.rotate(rot_deg, resample=Image.Resampling.BICUBIC, expand=True)
                sx = seal_target_x - (active_seal.width - seal_disp_w) // 2
                sy = seal_target_y - (active_seal.height - seal_disp_h) // 2
                paste_tech_card(canvas, active_seal, sx, sy, glow_color=(255, 215, 60), glow_radius=25, elevation=22)
            else:
                paste_tech_card(canvas, compact_seal, seal_target_x, seal_target_y, glow_color=(255, 215, 60), glow_radius=18, elevation=14)

    return canvas

# -------------------------------------------------------------
# VIDEO COMPILATION
# -------------------------------------------------------------
def render_full_video():
    print(f"Starting rendering of {TOTAL_FRAMES} high-tech frames ({WIDTH}x{HEIGHT} at {FPS} FPS)...")
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    
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
    
    thumb_frames = {
        20: "tech_thumb_01_hook_glass.jpg",
        110: "tech_thumb_02_master_3d_shimmer.jpg",
        185: "tech_thumb_03_solution_nodes.jpg",
        240: "tech_thumb_04_pricing_pill.jpg",
        315: "tech_thumb_05_vip_whatsapp_pass.jpg"
    }
    os.makedirs(os.path.join(OUTPUT_DIR, "thumbnails"), exist_ok=True)

    for f in range(TOTAL_FRAMES):
        frame_img = render_frame(f)
        pipe.stdin.write(frame_img.tobytes())
        
        if f in thumb_frames:
            thumb_path = os.path.join(OUTPUT_DIR, "thumbnails", thumb_frames[f])
            frame_img.save(thumb_path, quality=92)
            print(f"Saved keyframe snapshot: {thumb_frames[f]}")
            
        if (f + 1) % 45 == 0 or f == TOTAL_FRAMES - 1:
            print(f"Rendered {f + 1}/{TOTAL_FRAMES} frames ({((f+1)/TOTAL_FRAMES)*100:.1f}%)")

    pipe.stdin.close()
    pipe.wait()
    print(f"Video stream finished: {TEMP_VIDEO}")

    # Merge Video with High-Tech Soundtrack
    print("Merging video with tech soundtrack...")
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
    print(f"FINAL HIGH-TECH VIDEO CREATED: {FINAL_VIDEO}")

    size_mb = os.path.getsize(FINAL_VIDEO) / (1024 * 1024)
    print(f"Final video size: {size_mb:.2f} MB")

if __name__ == "__main__":
    render_full_video()
