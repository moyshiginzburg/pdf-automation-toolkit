#!/bin/bash
# Flatten all PDFs in the current directory and merge them into one high-quality printable file

OUTPUT_FILE="FINAL_MERGED_PRINT_READY.pdf"

echo "Starting flattening and merging process..."
echo "This may take a few minutes depending on file sizes and CPU."

# Using Ghostscript to rasterize (flatten) and merge sequentially
gs -dSAFER \
   -dBATCH \
   -dNOPAUSE \
   -sDEVICE=pdfimage24 \
   -r600 \
   -dTextAlphaBits=4 \
   -dGraphicsAlphaBits=4 \
   -sOutputFile="$OUTPUT_FILE" \
   *.pdf

echo "Process complete! The output file is: $OUTPUT_FILE"
echo "IMPORTANT: Please open $OUTPUT_FILE and visually verify all elements are present before printing."
