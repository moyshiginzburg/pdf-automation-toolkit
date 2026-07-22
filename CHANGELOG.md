# CHANGELOG

All notable changes to this project are documented in this file.

## [1.2.0] - 2026-07-22

### Added
- `edit_tisha_bav_poster.py`: Python script utilizing Pillow (PIL) for surgical, pixel-perfect updates to the highly stylized Tisha B'Av 5784 poster. This script preserves the exact textures, shadows, and artistic depth of the original image by painting background-matched rectangles over outdated text, and inserting updated times, dates ("ט' באב תשפ"ו"), speaker ("ממורנו הרב שליט"א"), and logo.
- `make_print_ready.py`: Python script to generate a maximally compatible, flattened A4 PDF at 300 DPI (`tisha_bav_5786_final_print_compatible.pdf`), bypassing any potential rendering or font issues on older or less capable printers.
- Comprehensive `README.md` documentation explaining the differing use cases for HTML/Playwright vs. Surgical Image Editing approaches for future AI agent reference.

## [1.1.0] - 2026-07-22

### Added
- `generate_tisha_bav_pdf.py`: Python production script to generate a high-fidelity, print-ready A4 PDF poster for Tisha B'Av 5786 (`local_data/tisha_bav_5786.pdf`).
  - Re-uses genuine Jerusalem stone wall background, gold frame, side circle ornaments, and corner leaf flourishes from the 5784 poster (`local_data/photo_2026-07-22_12-21-45.jpg`).
  - Embedded new synagogue logo (`local_data/__בית ה לוגו-הרב אברמוב.png`).
  - Updated dates for 5786 (תשפ"ו) and updated prayer timings.
  - Updated lecture notice speaker to 'ממורנו הרב שליט"א'.
  - Styled blue quote card ('כל המתאבל על ירושלים זוכה ורואה בבניינה').
  - Removed outdated donation line and footer bar per user requirements.

## [1.0.0] - 2026-03-02

### Added
- `generate_purim_pdfs.py`: Python script that generates 9 Purim greeting PDFs using
  Playwright (Chromium headless) for high-fidelity HTML→PDF conversion.
  - Full RTL (right-to-left) Hebrew layout
  - Google Fonts integration: Heebo (body) + Frank Ruhl Libre (headings)
  - A5 print-ready dimensions (148×210 mm)
  - Royal design: gold gradients, navy blue tones, ornamental border frames
  - Decorative corner ornaments, dual accent strips (top/bottom)
  - Greeting number badge, stylized 'פורים שמח' header
  - 'קהילת בית ה׳' footer with 'פורים תשפ"ו' date
- `local_data/pdfs/`: Output directory containing 9 generated PDFs:
  - `purim_01_abrahamov.pdf` — הרב ישראל אברמוב
  - `purim_02_fisher.pdf` — הרב נתנאל פישר
  - `purim_03_peleg.pdf` — הרב עימנואל פלג
  - `purim_04_admakr.pdf` — יקי אדמקר
  - `purim_05_lubliner.pdf` — משה לובלינר
  - `purim_06_grinstein.pdf` — רפאל גרינשטיין
  - `purim_07_stern.pdf` — דוד ואביבה שטרן
  - `purim_08_reiter.pdf` — נתנאל ואביבה רייטר
  - `purim_09_horvitz.pdf` — שלומי ואביגיל הורביץ

### Dependencies
- `playwright` >= 1.58.0 (pip install playwright)
- Chromium browser binary (playwright install chromium)

## 2026-04-15
- Migrated environment from direnv/.venv to venv.
- Regenerated requirements.txt from project imports and existing dependency manifests.
- Updated .gitignore to ignore venv/ and removed obsolete direnv/.venv ignore rules.

