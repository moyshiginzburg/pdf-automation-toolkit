import numpy as np
from PIL import Image, ImageDraw, ImageFont

# Load image and fonts
img = Image.open('local_data/photo_2026-07-22_12-21-45.jpg').convert('RGB')
draw = ImageDraw.Draw(img)

# Get average color from a clean central stone patch
patch = img.crop((400, 320, 450, 350))
avg_color = tuple(np.array(patch).mean(axis=(0,1)).astype(int))

font_times = ImageFont.truetype("/usr/share/fonts/truetype/culmus/FrankRuehlCLM-Bold.ttf", 30)
font_year = ImageFont.truetype("/usr/share/fonts/truetype/culmus/FrankRuehlCLM-Bold.ttf", 36)
font_speaker = ImageFont.truetype("/usr/share/fonts/truetype/culmus/FrankRuehlCLM-Bold.ttf", 34)

boxes = {
    "Logo": (280, 20, 650, 185), 
    "17:30": (200, 320, 310, 355), 
    "19:29": (200, 365, 310, 400),
    "20:10": (200, 405, 310, 440),
    "ט באב": (340, 250, 580, 290), 
    "Speaker": (150, 570, 780, 630), # THE GOLDEN COORDINATE 
    "09:30": (200, 680, 310, 715),
    "18:55": (200, 725, 310, 760),
    "19:48": (200, 770, 310, 805),
    "19:53": (200, 810, 310, 845),
    "Donations": (170, 855, 790, 895),
    "Footer": (0, 1220, 930, 1280)
}

# 1. Erase boxes with solid color
for name, box in boxes.items():
    draw.rectangle(box, fill=avg_color)

# 2. Draw new text
# Times (left aligned to x=210)
draw.text((210, 320), "17:45", fill=(0,0,0), font=font_times)
draw.text((210, 365), "19:45", fill=(0,0,0), font=font_times)
draw.text((210, 405), "20:15", fill=(0,0,0), font=font_times)

draw.text((210, 680), "09:45", fill=(0,0,0), font=font_times)
draw.text((210, 725), "19:10", fill=(0,0,0), font=font_times)
draw.text((210, 770), "20:03", fill=(0,0,0), font=font_times)
draw.text((210, 810), "20:12", fill=(0,0,0), font=font_times)

# Year - centered in the space
draw.text((460, 250), "ט' באב תשפ\"ו", fill=(0,0,0), font=font_year, anchor="ma", direction="rtl")

# Speaker - centered
draw.text((465, 580), "ממורנו הרב שליט\"א", fill=(0,0,0), font=font_speaker, anchor="ma", direction="rtl")

# 3. Paste Logo
logo = Image.open('local_data/__בית ה לוגו-הרב אברמוב.png').convert("RGBA")
l_w, l_h = logo.size
new_h = 160
new_w = int(l_w * (new_h / l_h))
logo = logo.resize((new_w, new_h), Image.Resampling.LANCZOS)
logo_x = 465 - (new_w // 2)
logo_y = 22
img.paste(logo, (logo_x, logo_y), logo)

# Final save
img.save('local_data/tisha_bav_5786_final.pdf', "PDF", resolution=100.0)
img.save('local_data/tisha_bav_5786_final.jpg', quality=95)
print("Final PDF and JPG generated.")
