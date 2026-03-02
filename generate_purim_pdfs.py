"""
Purpose:
    Generate 9 beautiful, print-ready Purim greeting PDFs for 'Kehilat Beit Hashem' (בית ה')
    synagogue to be distributed as Mishloach Manot cards. Each greeting from purim.md gets
    its own separate A5 PDF with a stunning Hebrew-compatible design.

Method of Operation:
    1. Reads and parses 'purim.md', splitting content by '#N' markers to extract 9 greetings.
    2. For each greeting, builds a fully-styled HTML document:
       - Royal color palette: deep blue/navy + gold gradients
       - Hebrew fonts loaded from Google Fonts: Heebo (body) + Frank Ruhl Libre (headings)
       - Full RTL (right-to-left) layout for Hebrew text
       - Decorative elements: ornamental border, gold title, stylized footer
       - A5 page size (148 x 210 mm) optimized for print
    3. Uses Playwright (Chromium headless) to render each HTML page and export it as a PDF.
    4. Saves all 9 PDFs into 'local_data/pdfs/' directory.

Output:
    local_data/pdfs/purim_01_abrahamov.pdf ... purim_09_horvitz.pdf
"""

import asyncio
import base64
import re
from pathlib import Path
from playwright.async_api import async_playwright

# ─── Path Setup (always CWD-relative per project conventions) ──────────────
PROJECT_ROOT = Path.cwd()
DATA_DIR = PROJECT_ROOT / "local_data"
PDF_DIR = DATA_DIR / "pdfs"
PURIM_MD = DATA_DIR / "purim.md"
LOGO_PATH = DATA_DIR / "בית ה לוגו-01.png"

for d in [DATA_DIR, PDF_DIR]:
    d.mkdir(parents=True, exist_ok=True)


def load_logo_base64() -> str:
    """
    Load the community logo PNG and encode it as a base64 data URI.
    This allows embedding the image directly in the HTML without
    relying on file:// paths, which may not work in headless Chromium.
    Returns an empty string if the logo file is not found.
    """
    if not LOGO_PATH.exists():
        print(f"  ⚠️  Logo not found at: {LOGO_PATH}")
        return ""
    raw = LOGO_PATH.read_bytes()
    b64 = base64.b64encode(raw).decode("utf-8")
    return f"data:image/png;base64,{b64}"

# ─── Blessing Metadata (name for file naming) ──────────────────────────────
GREETING_META = [
    {"slug": "01_abrahamov",  "icon": "✡"},
    {"slug": "02_fisher",     "icon": "📖"},
    {"slug": "03_peleg",      "icon": "🕎"},
    {"slug": "04_admakr",     "icon": "⭐"},
    {"slug": "05_lubliner",   "icon": "🏛"},
    {"slug": "06_grinstein",  "icon": "🕍"},
    {"slug": "07_stern",      "icon": "🌟"},
    {"slug": "08_reiter",     "icon": "✨"},
    {"slug": "09_horvitz",    "icon": "🎊"},
]


def parse_greetings(md_path: Path) -> list[dict]:
    """
    Parse purim.md and extract the 9 greetings.
    Each greeting starts with '#N' (e.g., #1, #2 ...) on its own line.
    Returns a list of dicts with 'number' and 'body' (raw Hebrew text).
    """
    content = md_path.read_text(encoding="utf-8")
    # Split on lines that are exactly '#N' (section markers)
    sections = re.split(r"(?m)^#\d+\s*$", content)
    # First element is empty (before #1), skip it
    greetings = []
    for i, section in enumerate(sections[1:], start=1):
        body = section.strip()
        greetings.append({"number": i, "body": body})
    return greetings


def extract_recipient(body: str) -> str:
    """
    Extract the recipient name from the first line of the greeting.
    Typically: 'לכבוד ...'  or  'לכבוד הרב ...'
    Returns the full first line (the salutation).
    """
    first_line = body.split("\n")[0].strip()
    return first_line


def extract_greeting_body(body: str) -> str:
    """
    Return all lines after the first (recipient) line, joined as paragraphs.
    Each non-empty line becomes a separate <p> element candidate.
    """
    lines = body.split("\n")
    # Skip first line (recipient), join rest
    rest = "\n".join(lines[1:]).strip()
    return rest


def body_to_html_paragraphs(body_text: str) -> str:
    """
    Convert plain text body into styled HTML paragraphs.
    Blank lines separate paragraphs; non-blank lines within a block are joined.
    """
    paragraphs = re.split(r"\n\s*\n", body_text)
    html_parts = []
    for para in paragraphs:
        para = para.strip()
        if para:
            # Replace single newlines inside a paragraph with <br> for line breaks
            para_html = para.replace("\n", "<br>")
            html_parts.append(f"<p>{para_html}</p>")
    return "\n".join(html_parts)


def build_html(greeting: dict, meta: dict, logo_b64: str = "") -> str:
    """
    Build a complete, self-contained HTML document for a single Purim greeting.
    The design features:
      - Royal navy + gold color scheme
      - Hebrew RTL layout
      - Google Fonts: Heebo (body) + Frank Ruhl Libre (headings)
      - Decorative ornamental border
      - Elegant header with community logo + 'פורים שמח' in gold gradient
      - Styled recipient name
      - Body paragraphs with generous line-height
      - Synagogue signature footer
    """
    recipient_line = extract_recipient(body=greeting["body"])
    body_text = extract_greeting_body(body=greeting["body"])
    body_html = body_to_html_paragraphs(body_text)
    number = greeting["number"]

    # Build the logo HTML block — only rendered if logo is available
    logo_html = ""
    if logo_b64:
        logo_html = f'<div class="logo-block"><img class="logo-img" src="{logo_b64}" alt="קהילת בית ה׳" /></div>'

    return f"""<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ברכת פורים - {recipient_line}</title>

  <!-- Google Fonts: Heebo (body) + Frank Ruhl Libre (headings) -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Frank+Ruhl+Libre:wght@300;400;500;700;900&family=Heebo:wght@300;400;500;700&display=swap" rel="stylesheet">

  <style>
    /* ═══════════════════════════════════════════
       PAGE SETUP — A5 print dimensions
       ═══════════════════════════════════════════ */
    @page {{
      size: A5;
      margin: 0;
    }}

    *, *::before, *::after {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    html, body {{
      width: 148mm;
      height: 210mm;
      overflow: hidden;
      direction: rtl;
      font-family: 'Heebo', sans-serif;
      background: #f9f5eb;
    }}

    /* ═══════════════════════════════════════════
       FULL-PAGE CARD
       ═══════════════════════════════════════════ */
    .card {{
      width: 148mm;
      height: 210mm;
      position: relative;
      background: linear-gradient(160deg, #fdfaf0 0%, #f5ead5 40%, #ede0c4 100%);
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }}

    /* ─── Decorative background texture ── */
    .card::before {{
      content: '';
      position: absolute;
      inset: 0;
      background-image:
        radial-gradient(circle at 15% 15%, rgba(180, 140, 50, 0.08) 0%, transparent 50%),
        radial-gradient(circle at 85% 85%, rgba(30, 60, 120, 0.06) 0%, transparent 50%),
        radial-gradient(circle at 50% 50%, rgba(180, 140, 50, 0.04) 0%, transparent 70%);
      pointer-events: none;
      z-index: 0;
    }}

    /* ─── Top accent strip ── */
    .top-accent {{
      position: relative;
      z-index: 1;
      height: 6mm;
      background: linear-gradient(90deg, #1a3a6b 0%, #2a5298 30%, #b8960a 60%, #d4a80c 80%, #1a3a6b 100%);
      flex-shrink: 0;
    }}

    /* ─── Outer ornamental border ── */
    .border-frame {{
      position: absolute;
      inset: 8mm;
      border: 1.5pt solid rgba(180, 140, 20, 0.55);
      border-radius: 3px;
      z-index: 1;
      pointer-events: none;
    }}

    .border-frame::before {{
      content: '';
      position: absolute;
      inset: 3px;
      border: 0.5pt solid rgba(180, 140, 20, 0.3);
      border-radius: 2px;
    }}

    /* ─── Corner ornaments ── */
    .corner {{
      position: absolute;
      width: 14px;
      height: 14px;
      z-index: 2;
    }}
    .corner-tl {{ top: 8mm; right: 8mm; border-top: 2.5pt solid #b8960a; border-right: 2.5pt solid #b8960a; border-radius: 0 4px 0 0; }}
    .corner-tr {{ top: 8mm; left: 8mm;  border-top: 2.5pt solid #b8960a; border-left:  2.5pt solid #b8960a; border-radius: 4px 0 0 0; }}
    .corner-bl {{ bottom: 8mm; right: 8mm; border-bottom: 2.5pt solid #b8960a; border-right: 2.5pt solid #b8960a; border-radius: 0 0 0 4px; }}
    .corner-br {{ bottom: 8mm; left: 8mm;  border-bottom: 2.5pt solid #b8960a; border-left:  2.5pt solid #b8960a; border-radius: 0 0 4px 0; }}

    /* ═══════════════════════════════════════════
       CONTENT LAYOUT
       ═══════════════════════════════════════════ */
    .content {{
      position: relative;
      z-index: 2;
      flex: 1;
      display: flex;
      flex-direction: column;
      padding: 12mm 14mm 10mm 14mm;
      gap: 0;
    }}

    /* ─── HEADER: Title + subtitle ── */
    .header {{
      text-align: center;
      margin-bottom: 4mm;
      flex-shrink: 0;
    }}

    .purim-title {{
      font-family: 'Frank Ruhl Libre', serif;
      font-size: 22pt;
      font-weight: 900;
      line-height: 1.1;
      background: linear-gradient(135deg, #b8960a 0%, #d4a80c 25%, #f0c844 50%, #d4a80c 75%, #9a7a08 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      letter-spacing: 0.05em;
      text-shadow: none;
      margin-bottom: 0;
    }}

    /* ─── Logo block ── */
    .logo-block {{
      display: flex;
      justify-content: center;
      align-items: center;
      margin-bottom: 2mm;
      flex-shrink: 0;
    }}

    .logo-img {{
      height: 20mm;
      width: auto;
      object-fit: contain;
      filter: drop-shadow(0px 1px 3px rgba(180, 140, 20, 0.25));
    }}

    /* ─── Decorative divider ── */
    .divider {{
      display: flex;
      align-items: center;
      gap: 3mm;
      margin: 3mm 0;
      flex-shrink: 0;
    }}

    .divider-line {{
      flex: 1;
      height: 1px;
      background: linear-gradient(90deg, transparent, #b8960a 30%, #b8960a 70%, transparent);
    }}

    .divider-diamond {{
      width: 5px;
      height: 5px;
      background: #b8960a;
      transform: rotate(45deg);
      flex-shrink: 0;
    }}

    /* ─── Recipient block ── */
    .recipient-block {{
      text-align: right;
      flex-shrink: 0;
      margin-bottom: 3mm;
    }}

    .recipient-name {{
      font-family: 'Frank Ruhl Libre', serif;
      font-size: 13pt;
      font-weight: 700;
      color: #1a3a6b;
      line-height: 1.3;
    }}

    /* ─── Body text ── */
    .body-text {{
      flex: 1;
      overflow: hidden;
    }}

    .body-text p {{
      font-family: 'Heebo', sans-serif;
      font-size: 9.5pt;
      font-weight: 300;
      color: #2c2c2c;
      line-height: 1.75;
      text-align: right;
      margin-bottom: 3mm;
    }}

    .body-text p:last-child {{
      margin-bottom: 0;
    }}

    /* ─── Small decorative star pattern between sections ── */
    .star-sep {{
      text-align: center;
      font-size: 8pt;
      color: #b8960a;
      opacity: 0.6;
      margin: 2mm 0;
      letter-spacing: 0.3em;
      flex-shrink: 0;
    }}

    /* ─── Footer: Synagogue signature ── */
    .footer {{
      flex-shrink: 0;
      text-align: center;
      padding-top: 3mm;
      border-top: 0.5pt solid rgba(180, 140, 20, 0.4);
    }}

    .footer-community {{
      font-family: 'Frank Ruhl Libre', serif;
      font-size: 10pt;
      font-weight: 700;
      color: #1a3a6b;
      letter-spacing: 0.05em;
    }}

    .footer-blessing {{
      font-family: 'Heebo', sans-serif;
      font-size: 7pt;
      font-weight: 300;
      color: #6b5a2a;
      margin-top: 1mm;
      letter-spacing: 0.1em;
    }}

    /* ─── Bottom accent strip ── */
    .bottom-accent {{
      position: relative;
      z-index: 1;
      height: 4mm;
      background: linear-gradient(90deg, #1a3a6b 0%, #2a5298 30%, #b8960a 60%, #d4a80c 80%, #1a3a6b 100%);
      flex-shrink: 0;
    }}

  </style>
</head>
<body>
  <div class="card">

    <!-- Top accent strip -->
    <div class="top-accent"></div>

    <!-- Ornamental border frame -->
    <div class="border-frame"></div>
    <div class="corner corner-tl"></div>
    <div class="corner corner-tr"></div>
    <div class="corner corner-bl"></div>
    <div class="corner corner-br"></div>

    <!-- Main content -->
    <div class="content">

      <!-- Header -->
      {logo_html}
      <div class="header">
        <div class="purim-title">פורים שמח!</div>
      </div>

      <!-- Top divider -->
      <div class="divider">
        <div class="divider-line"></div>
        <div class="divider-diamond"></div>
        <div class="divider-line"></div>
      </div>

      <!-- Recipient block -->
      <div class="recipient-block">
        <div class="recipient-name">{recipient_line}</div>
      </div>

      <!-- Body text -->
      <div class="body-text">
        {body_html}
      </div>

      <!-- Divider before footer -->
      <div class="divider" style="margin-top: 3mm;">
        <div class="divider-line"></div>
        <div class="divider-diamond"></div>
        <div class="divider-line"></div>
      </div>

      <!-- Footer -->
      <div class="footer">
        <div class="footer-community">קהילת בית ה׳</div>
        <div class="footer-blessing">בברכת פורים שמח ♦ פורים תשפ״ו</div>
      </div>

    </div><!-- /.content -->

    <!-- Bottom accent strip -->
    <div class="bottom-accent"></div>

  </div><!-- /.card -->
</body>
</html>"""


async def generate_pdfs():
    """
    Main async function:
      1. Load the community logo as base64 (for inline embedding)
      2. Parse greetings from purim.md
      3. For each greeting, build HTML → launch Playwright → save PDF
    """
    print("🖼  Loading community logo...")
    logo_b64 = load_logo_base64()
    if logo_b64:
        print("   Logo loaded successfully.")

    print("📖 Reading purim.md...")
    greetings = parse_greetings(PURIM_MD)
    print(f"   Found {len(greetings)} greetings.")

    async with async_playwright() as pw:
        # Launch headless Chromium
        browser = await pw.chromium.launch(headless=True)
        context = await browser.new_context()

        for i, (greeting, meta) in enumerate(zip(greetings, GREETING_META), start=1):
            slug = meta["slug"]
            output_path = PDF_DIR / f"purim_{slug}.pdf"

            print(f"  🎨 Generating PDF {i}/9: {slug}...")

            # Build HTML content (pass logo for inline embedding)
            html_content = build_html(greeting, meta, logo_b64=logo_b64)

            # Create a new page and set content
            page = await context.new_page()

            # Set content and wait for fonts to load
            await page.set_content(html_content, wait_until="networkidle")

            # Give extra time for Google Fonts to fully render
            await page.wait_for_timeout(1500)

            # Export as PDF — A5 size in mm → points (1mm ≈ 2.8346 pt)
            await page.pdf(
                path=str(output_path),
                width="148mm",
                height="210mm",
                print_background=True,
                margin={"top": "0", "bottom": "0", "left": "0", "right": "0"},
            )

            await page.close()
            file_size_kb = output_path.stat().st_size // 1024
            print(f"     ✅ Saved: {output_path.name} ({file_size_kb} KB)")

        await context.close()
        await browser.close()

    print(f"\n🎉 Done! All 9 PDFs saved to: {PDF_DIR}")
    print("   Files:")
    for f in sorted(PDF_DIR.glob("purim_*.pdf")):
        print(f"   • {f.name}")


if __name__ == "__main__":
    asyncio.run(generate_pdfs())
