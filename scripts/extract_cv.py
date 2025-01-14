#!/usr/bin/env python3

import os
from pathlib import Path
import yaml
import json
import re
import pdf2image
import pytesseract
from PIL import Image
import tempfile
import shutil
from tqdm import tqdm
import time

def convert_pdf_to_images(pdf_path):
    """Convert PDF pages to images."""
    try:
        temp_dir = tempfile.mkdtemp()
        print("\nStep 1: Converting PDF to images...")
        
        # First get number of pages
        images = pdf2image.convert_from_path(pdf_path)
        total_pages = len(images)
        
        # Now convert with progress bar
        image_paths = []
        for i, image in tqdm(enumerate(images), total=total_pages, desc="Converting pages", unit="page"):
            image_path = os.path.join(temp_dir, f'page_{i+1}.png')
            image.save(image_path, 'PNG')
            image_paths.append(image_path)
            
        return temp_dir, image_paths
    except Exception as e:
        print(f"Error converting PDF to images: {e}")
        return None, []

def extract_text_from_images(image_paths):
    """Extract text from images using OCR."""
    print("\nStep 2: Extracting text using OCR...")
    full_text = ""
    
    for image_path in tqdm(image_paths, desc="Processing pages", unit="page"):
        try:
            text = pytesseract.image_to_string(Image.open(image_path))
            full_text += text + "\n"
        except Exception as e:
            print(f"Error processing image {image_path}: {e}")
    
    return full_text

def find_all_sections(text):
    """Find all sections in the CV."""
    print("\nStep 3: Identifying CV sections...")
    # Common section headers in academic CVs
    headers = [
        r'EDUCATION',
        r'ACADEMIC POSITIONS?',
        r'EMPLOYMENT',
        r'RESEARCH( INTERESTS?)?',
        r'PUBLICATIONS?',
        r'PEER[- ]REVIEWED',
        r'JOURNAL ARTICLES?',
        r'CONFERENCE PRESENTATIONS?',
        r'PRESENTATIONS?',
        r'POSTERS?',
        r'INVITED TALKS?',
        r'TEACHING',
        r'COURSES?',
        r'AWARDS?',
        r'HONORS?',
        r'GRANTS?',
        r'FUNDING',
        r'SERVICE',
        r'PROFESSIONAL ACTIVITIES?',
        r'SKILLS?',
        r'TECHNICAL',
        r'LANGUAGES?',
        r'CERTIFICATIONS?',
        r'PROFESSIONAL DEVELOPMENT',
        r'MEMBERSHIPS?',
        r'AFFILIATIONS?',
        r'MEDIA',
        r'PRESS',
        r'COVERAGE',
        r'INDUSTRY',
        r'WORK EXPERIENCE'
    ]
    
    # Create regex pattern for finding sections
    pattern = '|'.join(f"({h})" for h in headers)
    matches = list(re.finditer(pattern, text, re.IGNORECASE))
    
    # Get positions of all section headers
    positions = []
    for match in matches:
        section_name = match.group().strip().upper()
        start = match.start()
        positions.append((section_name, start))
    positions.sort(key=lambda x: x[1])
    
    # Extract content between sections
    sections = {}
    for i, (section_name, start) in enumerate(tqdm(positions, desc="Processing sections", unit="section")):
        end = positions[i+1][1] if i < len(positions)-1 else len(text)
        content = text[start:end].strip()
        
        # Clean up the content
        lines = content.split('\n')
        cleaned_lines = []
        for line in lines:
            line = line.strip()
            if line and not line.isupper():  # Skip section headers
                cleaned_lines.append(line)
        
        sections[section_name] = cleaned_lines
    
    return sections

def extract_structured_data(sections):
    """Extract structured data from sections."""
    print("\nStep 4: Structuring section data...")
    structured_data = {}
    
    for section_name, lines in tqdm(sections.items(), desc="Processing entries", unit="section"):
        entries = []
        current_entry = ""
        
        for line in lines:
            # If line starts with a year or has a year in parentheses, it might be a new entry
            if re.match(r'^\d{4}', line) or re.search(r'\(\d{4}\)', line):
                if current_entry:
                    entries.append(current_entry.strip())
                current_entry = line
            else:
                if current_entry:
                    current_entry += " " + line
                else:
                    current_entry = line
        
        if current_entry:
            entries.append(current_entry.strip())
        
        # Clean up entries
        cleaned_entries = []
        for entry in entries:
            # Remove multiple spaces
            entry = re.sub(r'\s+', ' ', entry)
            # Remove bullet points and dashes at the start
            entry = re.sub(r'^[•\-∙]\s*', '', entry)
            if entry:
                cleaned_entries.append(entry)
        
        if cleaned_entries:
            structured_data[section_name] = cleaned_entries
    
    return structured_data

def save_structured_data(data, base_filename):
    """Save structured data in both JSON and YAML formats."""
    print("\nStep 5: Saving extracted data...")
    
    # Save as JSON
    json_file = os.path.join('sources', f'{base_filename}.json')
    with open(json_file, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"✓ Saved JSON data to {json_file}")
    
    # Save as YAML
    yaml_file = os.path.join('sources', f'{base_filename}.yaml')
    with open(yaml_file, 'w') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)
    print(f"✓ Saved YAML data to {yaml_file}")
    
    # Print a summary of found sections
    print("\n📊 Summary of extracted sections:")
    for section, entries in data.items():
        print(f"  ▪ {section}: {len(entries)} entries")

def main():
    print("🔍 CV Data Extraction Tool")
    print("=" * 50)
    
    # Automatically find PDF in sources directory
    sources_dir = os.path.join(os.getcwd(), 'sources')
    pdf_files = [f for f in os.listdir(sources_dir) if f.endswith('.pdf')]
    
    if not pdf_files:
        print("❌ Error: No PDF files found in sources directory")
        return
    
    if len(pdf_files) > 1:
        print("⚠️  Multiple PDF files found. Using the first one.")
    
    pdf_filename = pdf_files[0]
    pdf_path = os.path.join(sources_dir, pdf_filename)
    print(f"\n📄 Found CV: {pdf_filename}")
    
    # Get base filename without extension
    base_filename = os.path.splitext(pdf_filename)[0]
    
    start_time = time.time()
    
    # Convert PDF to images
    temp_dir, image_paths = convert_pdf_to_images(pdf_path)
    if not image_paths:
        return
    
    try:
        # Extract text from images
        text = extract_text_from_images(image_paths)
        
        # Find all sections
        sections = find_all_sections(text)
        
        # Extract structured data
        structured_data = extract_structured_data(sections)
        
        # Save the structured data
        save_structured_data(structured_data, f"{base_filename}_extracted")
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"\n✨ Processing completed in {duration:.1f} seconds!")
        print("\n📋 Next steps:")
        print("  1. Review the extracted data in the JSON and YAML files")
        print("  2. Compare with your current CV to identify missing information")
        print("  3. Use the structured data to update your current CV as needed")
            
    finally:
        # Clean up temporary directory
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

if __name__ == "__main__":
    main() 