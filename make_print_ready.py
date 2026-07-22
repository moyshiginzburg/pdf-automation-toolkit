from PIL import Image

# Open the absolutely final edited image
img = Image.open('local_data/tisha_bav_5786_final.jpg').convert('RGB')

# Standard A4 size at 300 DPI is 2480 x 3508 pixels
# We will resize the image to exactly match this dimension for perfect printing
a4_width = 2480
a4_height = 3508

img_print = img.resize((a4_width, a4_height), Image.Resampling.LANCZOS)

# Save as a pure raster PDF with 300 DPI
# This ensures zero font issues, zero vector rendering issues, and perfect physical sizing
img_print.save('local_data/tisha_bav_5786_final_print_compatible.pdf', "PDF", resolution=300.0)

print("Flattened, print-compatible A4 PDF generated.")
