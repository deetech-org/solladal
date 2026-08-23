import os
from PIL import Image

def process_screenshots():
    src_dir = r"C:\Users\pethuraj\Desktop\solladal-screens"
    target_w, target_h = 1080, 1920 # Exact 9:16 aspect ratio
    
    files = ["tab-10inch-1.png", "tab-10inch-2.png", "tab-10inch-3.png"]
    
    for fname in files:
        fpath = os.path.join(src_dir, fname)
        if not os.path.exists(fpath):
            continue
            
        with Image.open(fpath) as img:
            img = img.convert("RGBA")
            w, h = img.size
            
            # Crop 6px from each edge to remove any DevTools border / rounded-corner artifacts
            crop_box = (6, 6, w - 6, h - 6)
            cropped = img.crop(crop_box)
            cw, ch = cropped.size
            
            # Sample clean background color from near the top-center edge
            bg_color = cropped.getpixel((cw // 2, 8))
            
            # Scale proportionally to fit 1080 width or 1920 height
            scale = min(target_w / cw, target_h / ch)
            new_w = int(cw * scale)
            new_h = int(ch * scale)
            
            resized_img = cropped.resize((new_w, new_h), Image.Resampling.LANCZOS)
            
            # Create full-bleed 1080x1920 canvas
            canvas = Image.new("RGBA", (target_w, target_h), bg_color)
            
            # Paste centered
            paste_x = (target_w - new_w) // 2
            paste_y = (target_h - new_h) // 2
            canvas.paste(resized_img, (paste_x, paste_y), resized_img)
            
            final_img = canvas.convert("RGB")
            final_img.save(fpath, format="PNG", optimize=True)
            
            file_size_kb = os.path.getsize(fpath) / 1024
            print(f"Refined {fname}: Size = {final_img.size} (9:16), File Size = {file_size_kb:.1f} KB")

if __name__ == "__main__":
    process_screenshots()
