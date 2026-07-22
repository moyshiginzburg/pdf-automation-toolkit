# Formatted PDF Creation & Editing

Welcome to the `creating a formatted pdf` workspace. 
This project serves as a toolkit and experimental workspace for generating, editing, and processing high-quality, print-ready PDF documents for the "Kehilat Beit Hashem" synagogue.

Throughout the development of this project, several technological approaches were tested to achieve perfect graphic design results. **This documentation is intended for future AI agents** tasked with similar assignments. Review these lessons to understand which methods are successful and which pitfalls to avoid.

---

## Workflow Approaches & AI Agent Lessons

During the work on this project, two primary approaches were utilized for handling highly stylized documents. **Please note the following lessons before beginning a new task:**

### 1. The HTML/CSS + Playwright Approach (Building from Scratch)
**When to use:** Whenever the goal is to create a **completely new** design from the ground up, or when the design relies on clean typography, vector shapes, and CSS gradients.
**How it works:** A complex HTML page is built with advanced CSS, and Playwright is used to render the page directly to a PDF.
**Success Example:** The script `generate_purim_pdfs.py` successfully used this approach to generate beautiful Purim greeting cards with rich backgrounds and CSS borders.

### 2. The Surgical Editing Approach - Image Manipulation / Pillow (Updating Existing Posters)
**When to use:** **Always** use this when the goal is to update details (dates, times, names) inside a **pre-existing, highly complex graphical poster** (e.g., a poster originally designed in Photoshop with stone textures, subtle shadows, and delicate lighting).
**What NOT to do:** **Do NOT attempt** to extract a "clean" background and rebuild the entire poster in HTML (as attempted in `generate_tisha_bav_pdf.py`). This approach fails because it loses the authenticity of the original image's textures, shadows, and subtle graphical depth.
**The Winning Strategy:** Use the Python `Pillow` (PIL) library to:
1. Open the original JPEG image.
2. Sample the exact background color in the immediate vicinity of the text to be replaced.
3. Draw a solid colored rectangle (or paste a sampled texture patch) precisely over the bounding box of the old text to erase it cleanly.
4. Draw the new text using the exact same TTF font directly in the same location using `ImageDraw`.
*Stunning Success Example:* `edit_tisha_bav_poster.py`.

---

## Core Project Scripts

### `generate_purim_pdfs.py`
- **Purpose:** Generates 9 separate A5 greeting cards for Purim, each customized with a different name (parsed from a Markdown file).
- **Technology:** HTML/CSS + Playwright.
- **Status:** Highly successful. Generates crisp, vector-based PDFs with beautiful fonts and CSS frames.

### `generate_tisha_bav_pdf.py` (Deprecated / Failed Design Attempt)
- **Purpose:** Attempted to create the Tisha B'Av prayer schedule poster based on a previous year's design.
- **Technology:** Tried to extract a clean background and print all text elements via HTML/Playwright.
- **Status:** **Abandoned**. The resulting output was too flat, losing the original graphic depth, and the text looked "pasted on" rather than naturally blending into the stone background.

### `edit_tisha_bav_poster.py` (The Winning Script)
- **Purpose:** Updates the Tisha B'Av poster while preserving 100% of the original Photoshop design aesthetic.
- **Technology:** Uses `PIL` (Pillow) for pixel-perfect surgical editing directly on the original JPG file. Old text areas are erased using precise bounding boxes filled with sampled stone colors, and new text is drawn with `ImageDraw`.
- **Status:** Perfect success.

### `make_print_ready.py`
- **Purpose:** Converts the final successful poster into an absolutely print-compatible, "flattened" PDF to prevent errors on older or cheaper printers.
- **Technology:** Loads the final generated JPG image, scales it up to standard A4 print resolution (2480x3508 pixels at 300 DPI) using high-quality Lanczos resampling, and saves it back as a PDF containing only the raster image. This eliminates any potential vector scaling or font rendering issues at print time.

### `flatten_and_merge.sh`
- **Purpose:** Flattens and merges multiple PDF files into a single, unified print-ready file (`FINAL_MERGED_PRINT_READY.pdf`).
- **Technology:** Uses the Linux `Ghostscript` (`gs`) utility to rasterize text and vector elements into a smooth image format.
