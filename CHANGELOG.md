# CHANGELOG

All notable changes to this project are documented in this file.

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
