import os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ASSETS_DIR = "video_papercraft/assets"
os.makedirs(ASSETS_DIR, exist_ok=True)

# -------------------------------------------------------------
# 1. DEEP SLATE NAVY CARDSTOCK PAPER BACKGROUND (1080x1920)
# -------------------------------------------------------------
w, h = 1080, 1920
# Base color: deep slate navy petroleum (matches the 3D logo ambient)
base_col = np.array([24, 52, 74], dtype=np.float32)

# Paper fiber texture
np.random.seed(101)
fiber = np.random.normal(0, 6.5, (h, w, 3))

# Subtle gradient from top-center light source to bottom
yy, xx = np.mgrid[0:h, 0:w]
rad = np.sqrt(((xx - w/2) / (w * 0.75))**2 + ((yy - h*0.35) / (h * 0.75))**2)
vignette = np.clip(1.08 - 0.28 * rad, 0.78, 1.15)[:, :, np.newaxis]

paper_arr = np.clip((base_col + fiber) * vignette, 0, 255).astype(np.uint8)
bg_paper = Image.fromarray(paper_arr)

# Origami crease lines & folds
draw_crease = ImageDraw.Draw(bg_paper, "RGBA")
# Center fold lines (giving pop-up book spine feel)
draw_crease.line([(0, h//2), (w, h//2)], fill=(0, 0, 0, 30), width=2)
draw_crease.line([(0, h//2 + 2), (w, h//2 + 2)], fill=(255, 255, 255, 22), width=1)
# Diagonal origami folds
draw_crease.line([(0, 0), (w, h)], fill=(255, 255, 255, 12), width=1)
draw_crease.line([(w, 0), (0, h)], fill=(0, 0, 0, 20), width=1)
# Quarter folds
draw_crease.line([(0, int(h*0.25)), (w, int(h*0.25))], fill=(255, 255, 255, 10), width=1)
draw_crease.line([(0, int(h*0.75)), (w, int(h*0.75))], fill=(0, 0, 0, 15), width=1)

bg_paper.save(os.path.join(ASSETS_DIR, "bg_cardstock.jpg"), quality=95)
print("1. bg_cardstock.jpg saved.")

# -------------------------------------------------------------
# 2. LOGO CUTOUT / DIE-CUT EMBLEM
# -------------------------------------------------------------
user_logo_path = r"C:\Users\nicoa\.gemini\antigravity-ide\brain\155f3af1-54ea-47ed-8072-0d5901d220be\.user_uploaded\media_1789734342821.jpg"
orig_logo = Image.open(user_logo_path).convert("RGB")

# Crop NL emblem (NL 3D letters)
nl_crop = orig_logo.crop((140, 150, 884, 650))
# Let's create an alpha mask by measuring difference from the surrounding navy background
nl_arr = np.array(nl_crop).astype(float)
# Ambient background color inside crop corners
bg_sample = nl_arr[0:25, 0:25].mean(axis=(0,1))
color_dist = np.sqrt(np.sum((nl_arr - bg_sample)**2, axis=2))

# Smooth cut-out mask with soft die-cut edge
alpha_mask = np.clip((color_dist - 16) * 10.0, 0, 255).astype(np.uint8)
mask_img = Image.fromarray(alpha_mask).filter(ImageFilter.GaussianBlur(1.0))

nl_cutout = nl_crop.convert("RGBA")
nl_cutout.putalpha(mask_img)

# Add a subtle white papercraft die-cut border around the emblem
border_mask = mask_img.filter(ImageFilter.MaxFilter(7))
border_card = Image.new("RGBA", nl_cutout.size, (245, 248, 252, 230))
border_card.putalpha(border_mask)
# Composite cutout over border
emblem_final = Image.new("RGBA", nl_cutout.size, (0, 0, 0, 0))
emblem_final.paste(border_card, (0, 0), border_card)
emblem_final.paste(nl_cutout, (0, 0), nl_cutout)
emblem_final.save(os.path.join(ASSETS_DIR, "logo_emblem.png"))
print("2. logo_emblem.png saved:", emblem_final.size)

# Also extract the text "NICO LABS" & "Automatizaciones con IA" as a die-cut badge
text_crop = orig_logo.crop((120, 670, 904, 880))
t_arr = np.array(text_crop).astype(float)
t_bg_sample = t_arr[0:20, 0:20].mean(axis=(0,1))
t_dist = np.sqrt(np.sum((t_arr - t_bg_sample)**2, axis=2))
t_alpha = np.clip((t_dist - 14) * 12.0, 0, 255).astype(np.uint8)
t_mask = Image.fromarray(t_alpha).filter(ImageFilter.GaussianBlur(1.0))
text_cutout = text_crop.convert("RGBA")
text_cutout.putalpha(t_mask)

t_border_mask = t_mask.filter(ImageFilter.MaxFilter(5))
t_border_card = Image.new("RGBA", text_cutout.size, (245, 248, 252, 220))
t_border_card.putalpha(t_border_mask)
brand_text_final = Image.new("RGBA", text_cutout.size, (0, 0, 0, 0))
brand_text_final.paste(t_border_card, (0, 0), t_border_card)
brand_text_final.paste(text_cutout, (0, 0), text_cutout)
brand_text_final.save(os.path.join(ASSETS_DIR, "brand_text_cutout.png"))
print("2b. brand_text_cutout.png saved.")

# -------------------------------------------------------------
# 3. HOOK CARD: "¿Seguís perdiendo horas en tareas manuales?"
# -------------------------------------------------------------
hook_w, hook_h = 880, 260
hook_card = Image.new("RGBA", (hook_w, hook_h), (0, 0, 0, 0))
d_hook = ImageDraw.Draw(hook_card)
# Cardstock paper body (ivory / textured cream)
d_hook.rounded_rectangle([0, 0, hook_w, hook_h], radius=24, fill=(248, 246, 238, 255), outline=(220, 210, 190, 255), width=3)
# Stitched inner border
for x in range(18, hook_w - 18, 12):
    d_hook.line([(x, 14), (x + 6, 14)], fill=(180, 160, 130, 200), width=2)
    d_hook.line([(x, hook_h - 14), (x + 6, hook_h - 14)], fill=(180, 160, 130, 200), width=2)
for y in range(18, hook_h - 18, 12):
    d_hook.line([(14, y), (14, y + 6)], fill=(180, 160, 130, 200), width=2)
    d_hook.line([(hook_w - 14, y), (hook_w - 14, y + 6)], fill=(180, 160, 130, 200), width=2)

f_hook_top = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 26)
f_hook_main = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 36)
f_hook_sub = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 25)

def draw_centered_text(draw, y, text, font, fill, width):
    bb = draw.textbbox((0, 0), text, font=font)
    tw = bb[2] - bb[0]
    draw.text(((width - tw)/2, y), text, font=font, fill=fill)

draw_centered_text(d_hook, 32, "DEL LÁPIZ Y PAPEL A LA AUTOMATIZACIÓN", f_hook_top, (180, 90, 35), hook_w)
draw_centered_text(d_hook, 80, "¿Seguís perdiendo horas en", f_hook_main, (24, 45, 60), hook_w)
draw_centered_text(d_hook, 130, "planillas y tareas repetitivas?", f_hook_main, (24, 45, 60), hook_w)
draw_centered_text(d_hook, 195, "💡 En Nico Labs creamos el cerebro digital de tu empresa", f_hook_sub, (50, 115, 85), hook_w)

hook_card.save(os.path.join(ASSETS_DIR, "hook_card.png"))
print("3. hook_card.png saved.")

# -------------------------------------------------------------
# 4. PAPER RIBBON: "SOLUCIONES 100% A MEDIDA"
# -------------------------------------------------------------
rib_w, rib_h = 860, 110
ribbon = Image.new("RGBA", (rib_w, rib_h), (0, 0, 0, 0))
d_rib = ImageDraw.Draw(ribbon)
rx1, rx2 = 30, rib_w - 30
d_rib.rectangle([rx1, 12, rx2, rib_h - 12], fill=(246, 248, 252, 255))
# Dashed stitching in cyan/navy
for x in range(rx1 + 10, rx2 - 10, 14):
    d_rib.line([(x, 18), (x + 7, 18)], fill=(0, 160, 220, 220), width=2)
    d_rib.line([(x, rib_h - 18), (x + 7, rib_h - 18)], fill=(0, 160, 220, 220), width=2)

f_rib = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 36)
rib_text = "✦ SOLUCIONES 100% A MEDIDA ✦"
draw_centered_text(d_rib, 34, rib_text, f_rib, (18, 44, 68), rib_w)
ribbon.save(os.path.join(ASSETS_DIR, "paper_ribbon.png"))
print("4. paper_ribbon.png saved.")

# -------------------------------------------------------------
# 5. SOLUTION BADGES (SCRAPBOOK CIRCULAR POP-UPS)
# -------------------------------------------------------------
def make_circular_badge(img_path, title, subtitle, accent_color=(0, 180, 216)):
    b_size = 280
    badge = Image.new("RGBA", (b_size, b_size + 70), (0, 0, 0, 0))
    d_badge = ImageDraw.Draw(badge)
    
    # Outer die-cut cardstock circle
    cx, cy, r = b_size // 2, b_size // 2, (b_size // 2) - 10
    d_badge.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(250, 250, 252, 255), outline=accent_color, width=4)
    # Stitched dashed ring
    dash_r = r - 8
    for deg in range(0, 360, 12):
        rad1 = math.radians(deg)
        rad2 = math.radians(deg + 6)
        x1 = cx + dash_r * math.cos(rad1)
        y1 = cy + dash_r * math.sin(rad1)
        x2 = cx + dash_r * math.cos(rad2)
        y2 = cy + dash_r * math.sin(rad2)
        d_badge.line([(x1, y1), (x2, y2)], fill=(120, 135, 150, 220), width=2)
        
    # Crop source image into circle
    inner_r = r - 18
    src_img = Image.open(img_path).convert("RGB")
    sw, sh = src_img.size
    min_dim = min(sw, sh)
    crop_src = src_img.crop(((sw - min_dim)//2, (sh - min_dim)//2, (sw + min_dim)//2, (sh + min_dim)//2))
    crop_src = crop_src.resize((inner_r * 2, inner_r * 2), Image.Resampling.LANCZOS)
    
    circle_mask = Image.new("L", (inner_r * 2, inner_r * 2), 0)
    d_mask = ImageDraw.Draw(circle_mask)
    d_mask.ellipse([0, 0, inner_r * 2, inner_r * 2], fill=255)
    
    badge.paste(crop_src, (cx - inner_r, cy - inner_r), circle_mask)
    
    # Bottom paper banner ribbon for text
    ban_w = b_size
    ban_h = 62
    ban_y = b_size - 18
    d_badge.rounded_rectangle([10, ban_y, ban_w - 10, ban_y + ban_h], radius=14, fill=(248, 250, 252, 255), outline=accent_color, width=2)
    
    f_t = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 22)
    f_st = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 17)
    draw_centered_text(d_badge, ban_y + 8, title, f_t, (18, 42, 64), b_size)
    draw_centered_text(d_badge, ban_y + 34, subtitle, f_st, (60, 90, 115), b_size)
    
    return badge

badge_chatbot = make_circular_badge("project-chatbot-new.jpg", "🤖 Chatbots 24/7", "WhatsApp & Ventas", (0, 180, 216))
badge_chatbot.save(os.path.join(ASSETS_DIR, "badge_chatbot.png"))

badge_n8n = make_circular_badge("project-pro-new.jpg", "⚡ Flujos n8n", "Procesos Automáticos", (245, 150, 40))
badge_n8n.save(os.path.join(ASSETS_DIR, "badge_n8n.png"))

badge_eco = make_circular_badge("project-gym-new.jpg", "📊 Ecosistema IA", "Control & Finanzas", (40, 195, 110))
badge_eco.save(os.path.join(ASSETS_DIR, "badge_ecosystem.png"))
print("5. Solution badges saved.")

# -------------------------------------------------------------
# 6. BENEFIT PILL: "Pagás por uso real • Sin costos de software"
# -------------------------------------------------------------
pill_w, pill_h = 760, 80
pill = Image.new("RGBA", (pill_w, pill_h), (0, 0, 0, 0))
d_pill = ImageDraw.Draw(pill)
d_pill.rounded_rectangle([0, 0, pill_w, pill_h], radius=40, fill=(245, 248, 254, 250), outline=(0, 180, 216), width=2)
f_pill = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 24)
draw_centered_text(d_pill, 24, "✨ Modalidad Pay-As-You-Use • Sin costos de software", f_pill, (14, 40, 62), pill_w)
pill.save(os.path.join(ASSETS_DIR, "pill_benefits.png"))
print("6. pill_benefits.png saved.")

# -------------------------------------------------------------
# 7. WHATSAPP CRAFT TICKET (CTA)
# -------------------------------------------------------------
tag_w, tag_h = 920, 260
ticket = Image.new("RGBA", (tag_w, tag_h), (0, 0, 0, 0))
d_ticket = ImageDraw.Draw(ticket)

# Cardstock body
d_ticket.rounded_rectangle([0, 0, tag_w, tag_h], radius=32, fill=(252, 250, 244, 255), outline=(240, 200, 120), width=3)

# Perforation punch-out holes on left & right edge to look like a tear-off stub ticket
for y in range(35, tag_h - 20, 28):
    d_ticket.ellipse([-12, y - 8, 12, y + 8], fill=(0, 0, 0, 0))
    d_ticket.ellipse([tag_w - 12, y - 8, tag_w + 12, y + 8], fill=(0, 0, 0, 0))

# Inner dashed divider line between WhatsApp badge and message
d_ticket.line([(180, 25), (180, tag_h - 25)], fill=(210, 180, 130, 200), width=2)

# WhatsApp Icon Circle on left
cx_wa, cy_wa = 90, tag_h // 2
d_ticket.ellipse([cx_wa - 60, cy_wa - 60, cx_wa + 60, cy_wa + 60], fill=(37, 211, 102, 255), outline=(255, 255, 255, 220), width=4)
wa_icon_path = r"c:\Users\nicoa\OneDrive\Documentos\9 - Nico Labs\Nicolabs Fotos\logo_whatsapp_icon_181638.png"
if os.path.exists(wa_icon_path):
    wa_ico = Image.open(wa_icon_path).convert("RGBA").resize((76, 76), Image.Resampling.LANCZOS)
    ticket.paste(wa_ico, (cx_wa - 38, cy_wa - 38), wa_ico)

# Ticket Copy
f_t_small = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 22)
f_t_big = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 36)
f_t_btn = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 28)
f_t_footer = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 20)

d_ticket.text((215, 25), "¿QUERÉS VER TU SOLUCIÓN A MEDIDA?", font=f_t_small, fill=(180, 95, 30))
d_ticket.text((215, 58), "¡Pedí tu Demo Gratis!", font=f_t_big, fill=(18, 42, 65))

# Interactive CTA button cutout
btn_box = [215, 118, tag_w - 35, 185]
d_ticket.rounded_rectangle(btn_box, radius=18, fill=(37, 211, 102, 255), outline=(20, 160, 75, 255), width=2)
btn_text = "TOCÁ O RESPONDÉ A ESTE ESTADO 💬"
bb_btn = d_ticket.textbbox((0, 0), btn_text, font=f_t_btn)
btn_tw = bb_btn[2] - bb_btn[0]
d_ticket.text((btn_box[0] + (btn_box[2] - btn_box[0] - btn_tw)/2, 132), btn_text, font=f_t_btn, fill=(255, 255, 255))

d_ticket.text((215, 205), "📞 +598 99 075 509   •   🌐 nicolabs.nico-family.com", font=f_t_footer, fill=(90, 115, 135))

ticket.save(os.path.join(ASSETS_DIR, "wa_ticket.png"))
print("7. wa_ticket.png saved.")

# -------------------------------------------------------------
# 8. GOLD FOIL PAPER WAX SEAL (STAMP OF APPROVAL)
# -------------------------------------------------------------
seal_size = 280
seal = Image.new("RGBA", (seal_size, seal_size), (0, 0, 0, 0))
d_seal = ImageDraw.Draw(seal)
cx, cy = seal_size // 2, seal_size // 2
scallop_r = seal_size // 2 - 12
points = []
num_petals = 28
for i in range(num_petals * 2):
    angle = i * math.pi / num_petals
    r = scallop_r if i % 2 == 0 else scallop_r - 10
    points.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))

d_seal.polygon(points, fill=(235, 175, 45, 255), outline=(255, 225, 130, 255))
d_seal.ellipse([cx - 95, cy - 95, cx + 95, cy + 95], outline=(175, 115, 18, 255), width=3)
d_seal.ellipse([cx - 88, cy - 88, cx + 88, cy + 88], fill=(218, 150, 25, 255))

f_seal_star = ImageFont.truetype("C:/Windows/Fonts/georgiab.ttf", 26)
f_seal_bold = ImageFont.truetype("C:/Windows/Fonts/georgiab.ttf", 36)
f_seal_sub = ImageFont.truetype("C:/Windows/Fonts/georgiab.ttf", 24)

draw_centered_text(d_seal, cy - 54, "★ NICO LABS ★", f_seal_star, (255, 245, 220), seal_size)
draw_centered_text(d_seal, cy - 18, "100%", f_seal_bold, (255, 255, 240), seal_size)
draw_centered_text(d_seal, cy + 24, "A MEDIDA", f_seal_sub, (255, 245, 220), seal_size)

seal.save(os.path.join(ASSETS_DIR, "seal_stamp.png"))
print("8. seal_stamp.png saved.")

print("All PaperCraft assets successfully created!")
