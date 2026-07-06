from PIL import Image

try:
    img = Image.open("profile-photo-new.png")
    
    target_width, target_height = 1200, 630
    target_ratio = target_width / float(target_height)
    img_ratio = img.width / float(img.height)
    
    if img_ratio > target_ratio:
        # Image is wider
        new_width = int(img.height * target_ratio)
        left = (img.width - new_width) / 2
        img = img.crop((left, 0, left + new_width, img.height))
    elif img_ratio < target_ratio:
        # Image is taller
        new_height = int(img.width / target_ratio)
        top = (img.height - new_height) / 2
        img = img.crop((0, top, img.width, top + new_height))
        
    img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
    
    if img.mode != 'RGB':
        img = img.convert('RGB')
        
    img.save("og-image.jpg", quality=90)
    print("Imagen redimensionada y guardada como og-image.jpg con éxito (1200x630).")
except Exception as e:
    print(f"Error procesando la imagen: {e}")
