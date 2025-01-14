#!/usr/bin/env python3
import yaml
import os

def ensure_directory(path):
    """Create directory if it doesn't exist."""
    if not os.path.exists(path):
        os.makedirs(path)

def save_yaml(data, filename):
    """Save data to a YAML file."""
    with open(filename, 'w') as f:
        yaml.dump(data, f, sort_keys=False, allow_unicode=True)

def import_info():
    """Import information from template and split into separate files."""
    # Read the template file
    with open('data/my_info_template.yaml', 'r') as f:
        data = yaml.safe_load(f)
    
    # Ensure data directory exists
    ensure_directory('data')
    
    # Save personal information
    if 'personal' in data:
        save_yaml(data['personal'], 'data/personal.yaml')
        print("✓ Created personal.yaml")
    
    # Save education information
    if 'education' in data:
        save_yaml(data['education'], 'data/education.yaml')
        print("✓ Created education.yaml")
    
    # Save publications
    if 'publications' in data:
        save_yaml(data['publications'], 'data/publications.yaml')
        print("✓ Created publications.yaml")
    
    # Save teaching experience
    if 'teaching' in data:
        save_yaml(data['teaching'], 'data/teaching.yaml')
        print("✓ Created teaching.yaml")
    
    # Save service information
    if 'service' in data:
        save_yaml(data['service'], 'data/service.yaml')
        print("✓ Created service.yaml")
    
    # Save awards
    if 'awards' in data:
        save_yaml(data['awards'], 'data/awards.yaml')
        print("✓ Created awards.yaml")
    
    # Save additional sections
    if 'grants_funding' in data:
        save_yaml(data['grants_funding'], 'data/grants.yaml')
        print("✓ Created grants.yaml")
    
    if 'media_coverage' in data:
        save_yaml(data['media_coverage'], 'data/media.yaml')
        print("✓ Created media.yaml")
    
    if 'industry_experience' in data:
        save_yaml(data['industry_experience'], 'data/industry.yaml')
        print("✓ Created industry.yaml")

if __name__ == "__main__":
    print("Importing CV information...")
    import_info()
    print("\nDone! Your information has been split into individual YAML files in the data/ directory.")
    print("You can now run ./build.sh to generate your CV.") 