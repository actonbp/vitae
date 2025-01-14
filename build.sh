#!/bin/bash

# Ensure we're in the right directory
cd "$(dirname "$0")"

# Create output directory if it doesn't exist
mkdir -p output

# Get current date in the desired format
current_date=$(date +"%d_%m_%Y")

# Render the CV
echo "Rendering academic CV..."
cd templates
quarto render academic_cv.qmd
mv academic_cv.pdf "../output/b_acton_cv_${current_date}.pdf"

echo "CV generation complete! Check the output directory for b_acton_cv_${current_date}.pdf" 