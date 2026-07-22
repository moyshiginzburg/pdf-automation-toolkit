"""
Purpose:
    Generate a print-ready A4 PDF poster for Tisha B'Av 5786 (ט' באב תשפ"ו)
    prayer schedule for 'Kehilat Beit Hashem' (בית ה') synagogue.
    The output PDF mirrors the exact visual style, Jerusalem stone background,
    gold borders, and corner leaf flourishes of the original 5784 poster
    (local_data/photo_2026-07-22_12-21-45.jpg), but with updated 5786 timings,
    the updated Rabbi reference ('ממורנו הרב שליט"א'), and the new logo
    (local_data/__בית ה לוגו-הרב אברמוב.png).

Method of Operation:
    1. Loads the original poster photo and extracts a pristine Jerusalem stone background
       texture patch to cleanly cover old text, date, speaker, and removed footer elements.
    2. Builds an HTML page formatted specifically for A4 portrait print dimensions.
    3. Integrates Google Fonts ('Frank Ruhl Libre' for traditional headlines, 'Heebo' and
       'Rubik' for time schedules and quote typography).
    4. Renders the new community logo, updated times, lecture notice, and quote card.
    5. Uses Playwright (Chromium headless) to convert the HTML page into a 300DPI print-ready
       PDF saved to 'local_data/tisha_bav_5786.pdf'.

Output:
    local_data/tisha_bav_5786.pdf
"""

import asyncio
import base64
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
from playwright.async_api import async_playwright

# ─── Path Setup (CWD-relative per project standards) ────────────────────────
PROJECT_ROOT = Path.cwd()
DATA_DIR = PROJECT_ROOT / "local_data"
TEMP_DIR = PROJECT_ROOT / "temp_cache"

for d in [DATA_DIR, TEMP_DIR]:
    d.mkdir(parents=True, exist_ok=True)

ORIGINAL_PHOTO = DATA_DIR / "photo_2026-07-22_12-21-45.jpg"
NEW_LOGO_PATH = DATA_DIR / "__בית ה לוגו-הרב אברמוב.png"
CLEAN_BG_PATH = TEMP_DIR / "pure_clean_bg.png"
OUTPUT_PDF = DATA_DIR / "tisha_bav_5786.pdf"


def prepare_clean_background():
    """
    Extract a pure stone texture sample from a text-free region of the original photo
    and tile it over old text regions to create a pristine background template.
    Preserves original arch shadow, gold double frame, side circles, and leaf flourishes.
    """
    if not ORIGINAL_PHOTO.exists():
        raise FileNotFoundError(f"Original poster photo not found at {ORIGINAL_PHOTO}")

    img = Image.open(ORIGINAL_PHOTO).convert("RGB")
    w, h = img.size
    bg = img.copy()

    # Crop pure stone sample from (x: 135..220, y: 120..180) inside left frame
    stone_sample = img.crop((135, 120, 220, 180)).filter(ImageFilter.GaussianBlur(radius=1.5))
    sw, sh = stone_sample.size

    def fill_pure_stone(box):
        x1, y1, x2, y2 = box
        bw, bh = x2 - x1, y2 - y1
        patch = Image.new("RGB", (bw, bh))
        for x in range(0, bw, sw):
            for y in range(0, bh, sh):
                patch.paste(stone_sample, (x, y))
        patch = patch.filter(ImageFilter.GaussianBlur(radius=1.5))
        bg.paste(patch, (x1, y1))

    # Clean text regions
    fill_pure_stone((320, 25, 610, 175))   # Old Logo
    fill_pure_stone((260, 180, 670, 310))  # Title & Date
    fill_pure_stone((180, 315, 750, 460))  # Night Times
    fill_pure_stone((180, 465, 750, 605))  # Kinot Notice
    fill_pure_stone((180, 610, 750, 850))  # Day Times
    fill_pure_stone((180, 855, 750, 1220)) # Donation line & Quote box interior

    # Replace footer bar below gold frame with clean background color
    draw = ImageDraw.Draw(bg)
    draw.rectangle([0, 1238, w, h], fill=(246, 242, 232))

    bg.save(CLEAN_BG_PATH)


def load_b64(path: Path) -> str:
    """Load image file and return base64 Data URI."""
    if not path.exists():
        return ""
    raw = path.read_bytes()
    b64 = base64.b64encode(raw).decode("utf-8")
    ext = path.suffix.lower().replace(".", "")
    mime = "image/png" if ext == "png" else "image/jpeg"
    return f"data:{mime};base64,{b64}"


def build_poster_html() -> str:
    """Build full HTML document for Playwright A4 PDF export."""
    logo_b64 = load_b64(NEW_LOGO_PATH)
    bg_b64 = load_b64(CLEAN_BG_PATH)

    return f"""<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
  <meta charset="UTF-8">
  <title>זמני תפילות ט' באב תשפ"ו - קהילת בית ה'</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Frank+Ruhl+Libre:wght@400;700;900&family=Heebo:wght@400;500;700;900&family=Rubik:wght@500;700;900&display=swap" rel="stylesheet">

  <style>
    @page {{
      size: A4 portrait;
      margin: 0;
    }}

    *, *::before, *::after {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    html, body {{
      width: 210mm;
      height: 297mm;
      overflow: hidden;
      direction: rtl;
      font-family: 'Frank Ruhl Libre', serif;
      background: #f6f2e8;
      color: #0d0d0d;
      -webkit-font-smoothing: antialiased;
    }}

    .page-container {{
      width: 210mm;
      height: 297mm;
      position: relative;
      background-image: url('{bg_b64}');
      background-size: 100% 100%;
      background-repeat: no-repeat;
    }}

    /* New Community Logo Header */
    .pos-logo {{
      position: absolute;
      top: 3.2%;
      left: 50%;
      transform: translateX(-50%);
      width: 32%;
      text-align: center;
    }}
    .logo-img {{
      max-height: 38mm;
      width: auto;
      object-fit: contain;
    }}

    /* Header Title & Date */
    .pos-title {{
      position: absolute;
      top: 15.0%;
      left: 50%;
      transform: translateX(-50%);
      width: 60%;
      text-align: center;
    }}

    .main-title {{
      font-family: 'Frank Ruhl Libre', serif;
      font-size: 38pt;
      font-weight: 900;
      color: #000;
      line-height: 1.1;
      letter-spacing: 0.01em;
    }}

    .date-title {{
      font-family: 'Frank Ruhl Libre', serif;
      font-size: 29pt;
      font-weight: 900;
      color: #000;
      display: inline-block;
      border-bottom: 2.5px solid #000;
      padding-bottom: 0.5mm;
      margin-top: 1.5mm;
    }}

    /* Evening Schedule */
    .pos-evening {{
      position: absolute;
      top: 25.5%;
      left: 50%;
      transform: translateX(-50%);
      width: 56%;
    }}

    /* Kinot & Lecture Section */
    .pos-kinot {{
      position: absolute;
      top: 37.2%;
      left: 50%;
      transform: translateX(-50%);
      width: 75%;
      text-align: center;
    }}

    /* Day Schedule */
    .pos-day {{
      position: absolute;
      top: 48.5%;
      left: 50%;
      transform: translateX(-50%);
      width: 56%;
    }}

    .schedule-row {{
      display: flex;
      align-items: baseline;
      justify-content: space-between;
      margin-bottom: 2.8mm;
    }}

    .schedule-label {{
      font-family: 'Frank Ruhl Libre', serif;
      font-size: 22pt;
      font-weight: 700;
      color: #000;
      white-space: nowrap;
    }}

    .dots-line {{
      flex: 1;
      border-bottom: 3.5px dotted #000;
      margin: 0 3mm;
      position: relative;
      top: -5px;
    }}

    .schedule-time {{
      font-family: 'Heebo', 'Rubik', sans-serif;
      font-size: 22pt;
      font-weight: 700;
      color: #000;
      white-space: nowrap;
      direction: ltr;
    }}

    .kinot-header {{
      font-family: 'Frank Ruhl Libre', serif;
      font-size: 24pt;
      font-weight: 700;
      color: #000;
      margin-bottom: 1mm;
    }}

    .kinot-title {{
      font-family: 'Frank Ruhl Libre', serif;
      font-size: 27pt;
      font-weight: 900;
      color: #000;
      margin-bottom: 1.5mm;
    }}

    .kinot-speaker {{
      font-family: 'Frank Ruhl Libre', serif;
      font-size: 24pt;
      font-weight: 900;
      color: #000;
    }}

    /* Blue Quote Card */
    .pos-quote-box {{
      position: absolute;
      top: 71.5%;
      left: 50%;
      transform: translateX(-50%);
      width: 52%;
      background: linear-gradient(180deg, #eef5fc 0%, #d8e6f7 100%);
      border: 3.5px solid #5a7ea8;
      border-radius: 5px;
      padding: 5mm 3mm;
      text-align: center;
      box-shadow: inset 0 0 10px rgba(90, 126, 168, 0.15), 0 2px 6px rgba(0, 0, 0, 0.06);
    }}

    .quote-text {{
      font-family: 'Rubik', 'Heebo', sans-serif;
      font-size: 32pt;
      font-weight: 900;
      color: #1b4478;
      line-height: 1.25;
      letter-spacing: 0.03em;
    }}

  </style>
</head>
<body>
  <div class="page-container">

    <!-- New Logo -->
    <div class="pos-logo">
      <img class="logo-img" src="{logo_b64}" alt="לוגו בית ה'" />
    </div>

    <!-- Titles -->
    <div class="pos-title">
      <div class="main-title">זמני תפילות</div>
      <div><span class="date-title">ט' באב תשפ"ו</span></div>
    </div>

    <!-- Evening Times -->
    <div class="pos-evening">
      <div class="schedule-row">
        <span class="schedule-label">מנחה</span>
        <span class="dots-line"></span>
        <span class="schedule-time">17:45</span>
      </div>
      <div class="schedule-row">
        <span class="schedule-label">שקיעת החמה</span>
        <span class="dots-line"></span>
        <span class="schedule-time">19:45</span>
      </div>
      <div class="schedule-row">
        <span class="schedule-label">מעריב</span>
        <span class="dots-line"></span>
        <span class="schedule-time">20:15</span>
      </div>
    </div>

    <!-- Kinot Announcement -->
    <div class="pos-kinot">
      <div class="kinot-header">לאחר הקינות</div>
      <div class="kinot-title">"הספד וקינה על חורבן הבית"</div>
      <div class="kinot-speaker">ממורנו הרב שליט"א</div>
    </div>

    <!-- Day Times -->
    <div class="pos-day">
      <div class="schedule-row">
        <span class="schedule-label">שחרית</span>
        <span class="dots-line"></span>
        <span class="schedule-time">09:15</span>
      </div>
      <div class="schedule-row">
        <span class="schedule-label">ברכו</span>
        <span class="dots-line"></span>
        <span class="schedule-time">09:45</span>
      </div>
      <div class="schedule-row">
        <span class="schedule-label">מנחה</span>
        <span class="dots-line"></span>
        <span class="schedule-time">19:10</span>
      </div>
      <div class="schedule-row">
        <span class="schedule-label">ערבית</span>
        <span class="dots-line"></span>
        <span class="schedule-time">20:03</span>
      </div>
      <div class="schedule-row">
        <span class="schedule-label">סיום הצום</span>
        <span class="dots-line"></span>
        <span class="schedule-time">20:12</span>
      </div>
    </div>

    <!-- Quote Box Card -->
    <div class="pos-quote-box">
      <div class="quote-text">
        כל המתאבל<br>
        על ירושלים<br>
        זוכה ורואה<br>
        בבניינה
      </div>
    </div>

  </div>
</body>
</html>"""


async def main():
    print("🧹 Preparing clean background template...")
    prepare_clean_background()

    print("🎨 Rendering HTML layout & generating PDF...")
    html_content = build_poster_html()

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1240, "height": 1754})
        await page.set_content(html_content, wait_until="networkidle")
        await page.wait_for_timeout(1500)

        # Export A4 print-ready PDF
        await page.pdf(
            path=str(OUTPUT_PDF),
            format="A4",
            print_background=True,
            margin={"top": "0", "bottom": "0", "left": "0", "right": "0"},
        )
        print(f"🎉 PDF generated successfully at: {OUTPUT_PDF}")

        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
