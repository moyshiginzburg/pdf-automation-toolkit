# PDF Automation & Editing Toolkit

Welcome to the PDF Automation & Editing Toolkit. This project serves as an experimental workspace and toolkit for generating, editing, and processing high-quality, print-ready PDF documents. 

**Note on the Case Study:** While this toolkit is designed for generic use, the code and assets in this repository are based on a real-world case study for the "Kehilat Beit Hashem" synagogue (e.g., Purim greeting cards and Tisha B'Av posters). This provides a concrete example of how to handle complex layouts, RTL Hebrew text, and pixel-perfect editing. 

---

## 🤖 Directives for AI Agents

**If you are an AI agent reading this repository to perform a task, PAY ATTENTION to the following rules:**

1. **Real-World Case Study:** The code contains hardcoded strings (like "קהילת בית ה׳"), specific bounding boxes, and absolute paths tailored to the original use case. **You MUST adapt** these texts, logos, and coordinates to fit your current client's needs. Do not blindly copy the synagogue's details.
2. **The `local_data` Directory:** The `local_data/` and `temp_cache/` folders are intentionally ignored by git (`.gitignore`). When you clone this repository, these folders will be missing. **You must create `local_data/`** and place the necessary source assets (base images, logos, markdown lists) inside it before running any scripts.
3. **OS & Font Dependencies:** The `edit_tisha_bav_poster.py` script relies on absolute paths to Linux fonts (e.g., `/usr/share/fonts/truetype/culmus/...`). If you are running in a macOS or Windows environment, **you must update the font paths** in the code before execution to prevent crashes.

---

## 🚀 Environment Setup & Execution

To use this toolkit, follow these steps to set up the environment:

1. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Install Playwright Browsers (CRITICAL):**
   The HTML-to-PDF scripts rely on Playwright. You must install the Chromium browser binaries for it to work:
   ```bash
   playwright install chromium
   ```

---

## Workflow Approaches & AI Agent Lessons

During the work on this project, two primary approaches were utilized for handling highly stylized documents. Review these lessons to understand which methods are successful and which pitfalls to avoid:

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
- **Purpose:** Generates multiple A5 greeting cards from a Markdown list.
- **Technology:** HTML/CSS + Playwright.
- **Status:** Highly successful. Generates crisp, vector-based PDFs with beautiful fonts and CSS frames.

### `generate_tisha_bav_pdf.py` (Deprecated / Failed Design Attempt)
- **Purpose:** Attempted to create a schedule poster by extracting a clean background and printing text elements via HTML/Playwright.
- **Status:** **Abandoned**. The resulting output was too flat, losing the original graphic depth.

### `edit_tisha_bav_poster.py` (The Winning Script)
- **Purpose:** Updates a poster while preserving 100% of the original Photoshop design aesthetic.
- **Technology:** Uses `PIL` (Pillow) for pixel-perfect surgical editing directly on the original JPG file. Old text areas are erased using precise bounding boxes filled with sampled stone colors, and new text is drawn with `ImageDraw`.

### `make_print_ready.py`
- **Purpose:** Converts the final successful poster into an absolutely print-compatible, "flattened" PDF to prevent errors on older or cheaper printers.
- **Technology:** Loads the final generated JPG image, scales it up to standard A4 print resolution (2480x3508 pixels at 300 DPI) using high-quality Lanczos resampling, and saves it back as a PDF containing only the raster image.

### `flatten_and_merge.sh`
- **Purpose:** Flattens and merges multiple PDF files into a single, unified print-ready file.
- **Technology:** Uses the Linux `Ghostscript` (`gs`) utility to rasterize text and vector elements into a smooth image format.
