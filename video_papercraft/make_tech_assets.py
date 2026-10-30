import os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ASSETS_DIR = "video_papercraft/assets"
os.makedirs(ASSETS_DIR, exist_ok=True)

WIDTH, HEIGHT = 1080, 1920

# -------------------------------------------------------------
# 1. DEEP CYBER TECH BACKGROUND (1080x1920)
# Deep slate navy/black with futuristic isometric tech grid and circuit lines
# -------------------------------------------------------------
print("1. Generating Cyber Tech Background...")
bg_arr = np.zeros((HEIGHT, WIDTH, 3), dtype=np.float32)

# Radial gradient from center-top (energy hub)
yy, xx = np.mgrid[0:HEIGHT, 0:WIDTH]
# Hub center around (WIDTH/2, 450)
dist_hub = np.sqrt(((xx - WIDTH/2) / (WIDTH * 0.7))**2 + ((yy - 480) / (HEIGHT * 0.6))**2)
# Core color: electric petroleum cyan (20, 55, 85) fading to deep midnight void (6, 12, 18)
for c, (c_high, c_low) in enumerate([(22, 6), (58, 12), (90, 20)]):
    bg_arr[:, :, c] = c_high * np.exp(-dist_hub * 1.5) + c_low

bg_img = Image.fromarray(np.clip(bg_arr, 0, 255).astype(np.uint8))
d_bg = ImageDraw.Draw(bg_img, "RGBA")

# Draw high-tech perspective grid lines
grid_color = (0, 180, 216, 22)
grid_color_bright = (0, 220, 255, 45)

# Horizontal grid lines (perspective spaced)
for y in range(0, HEIGHT, 45):
    d_bg.line([(0, y), (WIDTH, y)], fill=grid_color if y % 90 != 0 else grid_color_bright, width=1)

# Vertical grid lines
for x in range(0, WIDTH, 45):
    d_bg.line([(x, 0), (x, HEIGHT)], fill=grid_color if x % 90 != 0 else grid_color_bright, width=1)

# Tech circuit traces with glowing junction dots
np.random.seed(42)
circuit_lines = [
    # Top-left circuit
    [(0, 280), (180, 280), (280, 380), (280, 600)],
    # Top-right circuit
    [(WIDTH, 320), (WIDTH - 200, 320), (WIDTH - 300, 420), (WIDTH - 300, 700)],
    # Bottom circuits
    [(120, 1920), (120, 1600), (220, 1500), (450, 1500)],
    [(WIDTH - 150, 1920), (WIDTH - 150, 1650), (WIDTH - 260, 1540), (WIDTH - 480, 1540)]
]

for path in circuit_lines:
    d_bg.line(path, fill=(0, 180, 216, 75), width=2)
    # Junction dots
    for pt in path:
        d_bg.ellipse([pt[0]-4, pt[1]-4, pt[0]+4, pt[1]+4], fill=(0, 240, 255, 180), outline=(255, 255, 255, 220))

bg_img.save(os.path.join(ASSETS_DIR, "bg_cyber.jpg"), quality=95)
print("   bg_cyber.jpg saved.")

# -------------------------------------------------------------
# 2. MASTER 3D LOGO CARD (Using user uploaded original master artwork)
# -------------------------------------------------------------
print("2. Preparing Master 3D Logo Card...")
orig_logo_path = r"C:\Users\nicoa\.gemini\antigravity-ide\brain\155f3af1-54ea-47ed-8072-0d5901d220be\.user_uploaded\media_1789734342821.jpg"
orig_logo = Image.open(orig_logo_path).convert("RGBA")

# Create a sleek rounded glassmorphic frame for the 3D logo
# Crop around the entire artwork (NL + Nico Labs + Automatizaciones con IA)
# The artwork is in (100, 120, 924, 910)
logo_crop = orig_logo.crop((95, 130, 929, 900))
lw, lh = logo_crop.size

# Build a rounded glass tech card for it
card_mask = Image.new("L", (lw, lh), 0)
d_cmask = ImageDraw.Draw(card_mask)
d_cmask.rounded_rectangle([0, 0, lw, lh], radius=44, fill=255)

master_logo_card = Image.new("RGBA", (lw, lh), (0, 0, 0, 0))
master_logo_card.paste(logo_crop, (0, 0), card_mask)

# Add a glowing cyan/metallic rim border
d_mcard = ImageDraw.Draw(master_logo_card)
d_mcard.rounded_rectangle([2, 2, lw - 2, lh - 2], radius=44, outline=(0, 180, 216, 180), width=3)
d_mcard.rounded_rectangle([5, 5, lw - 5, lh - 5], radius=41, outline=(255, 255, 255, 90), width=1)

# Tech corner accents
for cx, cy in [(14, 14), (lw - 14, 14), (14, lh - 14), (lw - 14, lh - 14)]:
    d_mcard.ellipse([cx-4, cy-4, cx+4, cy+4], fill=(0, 240, 255, 240))

master_logo_card.save(os.path.join(ASSETS_DIR, "master_logo_card.png"))
print(f"   master_logo_card.png saved: {master_logo_card.size}")

# -------------------------------------------------------------
# 3. HOOK GLASSMORPHIC CARD (0.0s - 2.5s)
# Futuristic glass diagnostic card with glowing cyan rim
# -------------------------------------------------------------
print("3. Generating Glassmorphic Hook Card...")
hw, hh = 940, 360
hook_card = Image.new("RGBA", (hw, hh), (0, 0, 0, 0))
d_hk = ImageDraw.Draw(hook_card)

# Dark smoked glass background
d_hk.rounded_rectangle([0, 0, hw, hh], radius=32, fill=(12, 24, 38, 235), outline=(0, 180, 216, 220), width=3)
# Inner neon laser highlight
d_hk.rounded_rectangle([4, 4, hw - 4, hh - 4], radius=28, outline=(0, 240, 255, 80), width=1)

# Tech HUD badge at top
badge_w = 420
badge_h = 42
bx = (hw - badge_w) // 2
d_hk.rounded_rectangle([bx, 22, bx + badge_w, 22 + badge_h], radius=21, fill=(0, 180, 216, 40), outline=(0, 220, 255, 180), width=2)

f_mono = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 20)
f_h_main = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 38)
f_h_sub = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 26)

def draw_centered(draw, y, text, font, fill, width):
    bb = draw.textbbox((0, 0), text, font=font)
    tw = bb[2] - bb[0]
    draw.text(((width - tw)/2, y), text, font=font, fill=fill)

draw_centered(d_hk, 32, "⚡ SISTEMA // DIAGNÓSTICO OPERATIVO", f_mono, (0, 240, 255), hw)

draw_centered(d_hk, 95, "¿Tu negocio sigue frenado por", f_h_main, (255, 255, 255), hw)
draw_centered(d_hk, 145, "planillas y procesos manuales?", f_h_main, (0, 210, 255), hw)

# Divider line with center cyan node
d_hk.line([(60, 225), (hw - 60, 225)], fill=(0, 180, 216, 90), width=1)
d_hk.ellipse([hw//2 - 6, 225 - 6, hw//2 + 6, 225 + 6], fill=(0, 240, 255, 255))

draw_centered(d_hk, 252, "En Nico Labs diseñamos el cerebro digital de tu empresa.", f_h_sub, (200, 235, 255), hw)
draw_centered(d_hk, 292, "Ecosistemas autónomos e inteligentes que escalan tu tiempo.", f_mono, (110, 175, 210), hw)

hook_card.save(os.path.join(ASSETS_DIR, "hook_glass_card.png"))
print("   hook_glass_card.png saved.")

# -------------------------------------------------------------
# 4. TECH HUD RIBBON / BANNER: "✦ ARQUITECTURA DIGITAL A MEDIDA ✦"
# -------------------------------------------------------------
print("4. Generating Tech HUD Ribbon...")
rw, rh = 880, 110
tech_ribbon = Image.new("RGBA", (rw, rh), (0, 0, 0, 0))
d_tr = ImageDraw.Draw(tech_ribbon)

# Brushed titanium / dark glass capsule
d_tr.rounded_rectangle([0, 0, rw, rh], radius=24, fill=(10, 22, 35, 240), outline=(0, 195, 235, 240), width=3)
d_tr.rounded_rectangle([4, 4, rw - 4, rh - 4], radius=20, outline=(255, 255, 255, 75), width=1)

# Left and right cyan LED status dots
for x in [28, 48, rw - 48, rw - 28]:
    d_tr.ellipse([x - 5, rh//2 - 5, x + 5, rh//2 + 5], fill=(0, 240, 255, 255))

f_tr = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 34)
f_tr_sub = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 20)
draw_centered(d_tr, 22, "✦ SOLUCIONES DE IA 100% A MEDIDA ✦", f_tr, (255, 255, 255), rw)
draw_centered(d_tr, 68, "SIN COSTOS OCULTOS • ARQUITECTURA FULL-STACK", f_tr_sub, (0, 210, 255), rw)

tech_ribbon.save(os.path.join(ASSETS_DIR, "tech_hud_ribbon.png"))
print("   tech_hud_ribbon.png saved.")

# -------------------------------------------------------------
# 5. THREE SOLUTION TECH CARDS (Live Glassmorphic UI Nodes)
# -------------------------------------------------------------
print("5. Generating Solution Tech Cards...")

def make_tech_node(src_img_path, tag, title, subtitle, stat_label, stat_val, neon_color=(0, 210, 255)):
    nw, nh = 320, 480
    node = Image.new("RGBA", (nw, nh), (0, 0, 0, 0))
    d_node = ImageDraw.Draw(node)
    
    # Smoked glass container
    d_node.rounded_rectangle([0, 0, nw, nh], radius=28, fill=(11, 23, 36, 245), outline=neon_color, width=3)
    d_node.rounded_rectangle([4, 4, nw - 4, nh - 4], radius=24, outline=(255, 255, 255, 60), width=1)
    
    # Header tag pill
    d_node.rounded_rectangle([20, 16, nw - 20, 52], radius=14, fill=(neon_color[0], neon_color[1], neon_color[2], 45), outline=neon_color, width=1)
    f_tag = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 17)
    draw_centered(d_node, 24, tag, f_tag, (255, 255, 255), nw)
    
    # Image visual preview (centered with rounded corners)
    src_im = Image.open(src_img_path).convert("RGB")
    sw, sh = src_im.size
    min_dim = min(sw, sh)
    crop_src = src_im.crop(((sw - min_dim)//2, (sh - min_dim)//2, (sw + min_dim)//2, (sh + min_dim)//2))
    img_size = 230
    crop_src = crop_src.resize((img_size, img_size), Image.Resampling.LANCZOS)
    
    # Mask for rounded preview
    mask_p = Image.new("L", (img_size, img_size), 0)
    d_mp = ImageDraw.Draw(mask_p)
    d_mp.rounded_rectangle([0, 0, img_size, img_size], radius=20, fill=255)
    
    img_x = (nw - img_size) // 2
    img_y = 66
    node.paste(crop_src, (img_x, img_y), mask_p)
    # Image border outline
    d_node.rounded_rectangle([img_x, img_y, img_x + img_size, img_y + img_size], radius=20, outline=neon_color, width=2)
    
    # Titles
    f_t = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 26)
    f_st = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 19)
    draw_centered(d_node, 312, title, f_t, (255, 255, 255), nw)
    draw_centered(d_node, 348, subtitle, f_st, (160, 195, 220), nw)
    
    # Stat box at bottom (KPI indicator)
    d_node.rounded_rectangle([20, 395, nw - 20, 455], radius=16, fill=(0, 0, 0, 140), outline=(neon_color[0], neon_color[1], neon_color[2], 120), width=1)
    f_stat_lbl = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 16)
    f_stat_val = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 21)
    d_node.text((32, 405), stat_label, font=f_stat_lbl, fill=(170, 200, 220))
    d_node.text((32, 426), stat_val, font=f_stat_val, fill=neon_color)
    
    return node

node_chat = make_tech_node("project-chatbot-new.jpg", "🤖 AGENTE IA 24/7", "Chatbots WhatsApp", "Ventas & Turnos Autónomos", "TIEMPO RESPUESTA", "< 2 SEGUNDOS", (0, 210, 255))
node_chat.save(os.path.join(ASSETS_DIR, "tech_node_chatbot.png"))

node_n8n = make_tech_node("project-pro-new.jpg", "⚡ PROCESOS & N8N", "Flujos Automáticos", "Conexión Total de Sistemas", "PROCESAMIENTO", "100% AUTOMATIZADO", (255, 160, 40))
node_n8n.save(os.path.join(ASSETS_DIR, "tech_node_n8n.png"))

node_eco = make_tech_node("project-gym-new.jpg", "📊 GESTIÓN & CONTROL", "Ecosistemas 360°", "Finanzas y Clientes en Vivo", "EFICIENCIA OPERATIVA", "+150% RENTABILIDAD", (35, 215, 125))
node_eco.save(os.path.join(ASSETS_DIR, "tech_node_eco.png"))

print("   3 Solution Tech Nodes saved.")

# -------------------------------------------------------------
# 6. BENEFIT TECH CAPSULE ("Modalidad Pay-As-You-Use")
# -------------------------------------------------------------
pw, ph = 820, 84
tech_pill = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
d_tp = ImageDraw.Draw(tech_pill)
d_tp.rounded_rectangle([0, 0, pw, ph], radius=42, fill=(8, 20, 32, 235), outline=(0, 210, 255, 220), width=2)
# Glow indicator light
d_tp.ellipse([26, ph//2 - 9, 44, ph//2 + 9], fill=(0, 240, 255, 255))
f_tp = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 26)
draw_centered(d_tp, 24, "⚡ Modalidad Pay-As-You-Use • Pagás solo por uso real", f_tp, (240, 250, 255), pw)
tech_pill.save(os.path.join(ASSETS_DIR, "tech_pill_pricing.png"))
print("   tech_pill_pricing.png saved.")

# -------------------------------------------------------------
# 7. VIP TECH ACCESS PASS (WhatsApp CTA)
# Dark futuristic VIP Glassmorphic card with neon WhatsApp button
# -------------------------------------------------------------
print("7. Generating VIP Tech Pass...")
vw, vh = 960, 320
vip_pass = Image.new("RGBA", (vw, vh), (0, 0, 0, 0))
d_vip = ImageDraw.Draw(vip_pass)

# High-tech card body
d_vip.rounded_rectangle([0, 0, vw, vh], radius=36, fill=(10, 22, 34, 250), outline=(37, 211, 102, 240), width=3)
d_vip.rounded_rectangle([4, 4, vw - 4, vh - 4], radius=32, outline=(255, 255, 255, 75), width=1)

# Left VIP Holographic Chip & WhatsApp Logo
chip_x, chip_y = 35, 35
chip_w, chip_h = 135, vh - 70
d_vip.rounded_rectangle([chip_x, chip_y, chip_x + chip_w, chip_y + chip_h], radius=24, fill=(18, 38, 52, 255), outline=(0, 180, 216, 180), width=2)

# WhatsApp glowing circular badge
wa_cx, wa_cy = chip_x + chip_w // 2, chip_y + chip_h // 2
d_vip.ellipse([wa_cx - 45, wa_cy - 45, wa_cx + 45, wa_cy + 45], fill=(37, 211, 102, 255), outline=(255, 255, 255, 220), width=3)
wa_icon_path = r"c:\Users\nicoa\OneDrive\Documentos\9 - Nico Labs\Nicolabs Fotos\logo_whatsapp_icon_181638.png"
if os.path.exists(wa_icon_path):
    wa_ico = Image.open(wa_icon_path).convert("RGBA").resize((60, 60), Image.Resampling.LANCZOS)
    vip_pass.paste(wa_ico, (wa_cx - 30, wa_cy - 30), wa_ico)

# Right Text area
tx_start = 195
f_vip_tag = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 20)
f_vip_title = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 36)
f_vip_btn = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 30)
f_vip_ft = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 21)

d_vip.text((tx_start, 28), "[ NICO LABS // DEMO EXCLUSIVA ]", font=f_vip_tag, fill=(0, 220, 255))
d_vip.text((tx_start, 62), "¿Querés ver tu Solución a Medida?", font=f_vip_title, fill=(255, 255, 255))

# Glowing WhatsApp Action Button
btn_rect = [tx_start, 125, vw - 35, 210]
d_vip.rounded_rectangle(btn_rect, radius=22, fill=(37, 211, 102, 255), outline=(255, 255, 255, 220), width=2)
btn_txt = "👉 PEDÍ TU DEMO GRATIS 💬"
bb_vbtn = d_vip.textbbox((0, 0), btn_txt, font=f_vip_btn)
vbtn_tw = bb_vbtn[2] - bb_vbtn[0]
d_vip.text((btn_rect[0] + (btn_rect[2] - btn_rect[0] - vbtn_tw)//2, 148), btn_txt, font=f_vip_btn, fill=(10, 24, 16))

# Footer info
d_vip.text((tx_start, 245), "TOCÁ O RESPONDÉ A ESTE ESTADO • +598 99 075 509", font=f_vip_ft, fill=(0, 210, 255))
d_vip.text((tx_start, 275), "🌐 nicolabs.nico-family.com", font=f_vip_tag, fill=(160, 195, 220))

vip_pass.save(os.path.join(ASSETS_DIR, "tech_vip_pass.png"))
print("   tech_vip_pass.png saved.")

# -------------------------------------------------------------
# 8. MINTED METALLIC GOLD SEAL (Sello de Oro Pulido de Calidad)
# -------------------------------------------------------------
print("8. Generating Minted Metallic Gold Seal...")
sw, sh = 200, 200
seal = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
d_sl = ImageDraw.Draw(seal)

cx, cy = sw // 2, sh // 2
r_outer = 94

# Generate radial metallic gold gradient
yy, xx = np.mgrid[0:sh, 0:sw]
dist = np.sqrt((xx - cx)**2 + (yy - cy)**2)
angle = np.arctan2(yy - cy, xx - cx)

# Metallic sheen angle modulation
sheen = 0.5 + 0.5 * np.cos(angle * 2.0 - 0.6)
gold_r = np.clip(215 + sheen * 40, 0, 255)
gold_g = np.clip(165 + sheen * 55, 0, 255)
gold_b = np.clip(40 + sheen * 70, 0, 255)

gold_arr = np.dstack([gold_r, gold_g, gold_b]).astype(np.uint8)
gold_base = Image.fromarray(gold_arr)

# Circular mask
seal_mask = Image.new("L", (sw, sh), 0)
d_smask = ImageDraw.Draw(seal_mask)
d_smask.ellipse([cx - r_outer, cy - r_outer, cx + r_outer, cy + r_outer], fill=255)

seal.paste(gold_base, (0, 0), seal_mask)

# Minted coin borders & engraved rings
d_sl = ImageDraw.Draw(seal)
# Outer polished rim
d_sl.ellipse([cx - r_outer, cy - r_outer, cx + r_outer, cy + r_outer], outline=(255, 240, 160, 255), width=3)
d_sl.ellipse([cx - r_outer + 5, cy - r_outer + 5, cx + r_outer - 5, cy + r_outer - 5], outline=(140, 95, 15, 230), width=2)
# Notched / beaded coin ring
bead_r = r_outer - 10
for deg in range(0, 360, 10):
    rad = math.radians(deg)
    bx = cx + bead_r * math.cos(rad)
    by = cy + bead_r * math.sin(rad)
    d_sl.ellipse([bx - 1.5, by - 1.5, bx + 1.5, by + 1.5], fill=(255, 245, 180, 255))

# Inner sunken core
d_sl.ellipse([cx - 68, cy - 68, cx + 68, cy + 68], fill=(175, 125, 20, 255), outline=(255, 230, 130, 255), width=2)
d_sl.ellipse([cx - 64, cy - 64, cx + 64, cy + 64], outline=(120, 80, 10, 255), width=1)

f_sl_top = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 19)
f_sl_mid = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 30)
f_sl_bot = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 17)

# Embossed text with 3D shadow
def draw_embossed(draw, y, text, font, fill_light, fill_dark):
    bb = draw.textbbox((0, 0), text, font=font)
    tw = bb[2] - bb[0]
    tx = (sw - tw) // 2
    # Shadow
    draw.text((tx + 1, y + 1), text, font=font, fill=fill_dark)
    # Highlight
    draw.text((tx, y), text, font=font, fill=fill_light)

draw_embossed(d_sl, cy - 44, "NICO LABS", f_sl_top, (255, 250, 230), (80, 50, 5))
draw_embossed(d_sl, cy - 15, "100%", f_sl_mid, (255, 255, 255), (90, 60, 10))
draw_embossed(d_sl, cy + 19, "A MEDIDA", f_sl_bot, (255, 245, 210), (80, 50, 5))

seal.save(os.path.join(ASSETS_DIR, "tech_holo_seal.png"))
print("   tech_holo_seal.png saved (minted gold edition).")

print("All High-Tech Assets generated successfully!")
