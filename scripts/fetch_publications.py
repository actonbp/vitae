#!/usr/bin/env python3
import requests
import yaml
import json
from datetime import datetime
import os

# Known journal articles that might be missing venue information
KNOWN_ARTICLES = {
    "Do you remember? Rater memory systems and leadership measurement": {
        "journal": "Leadership Quarterly",
        "year": 2020,
        "doi": "10.1016/j.leaqua.2020.101455",
        "pages": "101455"
    },
    "Rethinking authentic leadership: An alternative approach based on dynamic processes of active identity, self-regulation, and ironic processes of mental control": {
        "journal": "Journal of Management & Organization",
        "year": 2024,
        "doi": ""
    },
    "Leader Identity on the Fly: Intra-personal Leader Identity Dynamics in Response to Strong Events": {
        "journal": "Journal of Business and Psychology",
        "year": 2023,
        "doi": ""
    }
}

def fetch_publications(author_id="116198395"):
    """Fetch publications for an author from Semantic Scholar."""
    base_url = "https://api.semanticscholar.org/graph/v1"
    
    # Fetch author's papers
    papers_url = f"{base_url}/author/{author_id}/papers"
    params = {
        "fields": "title,year,authors,venue,publicationTypes,citationCount,externalIds,publicationVenue"
    }
    
    # Add headers for API request
    headers = {
        'User-Agent': 'Mozilla/5.0 Academic CV Builder (bryan.p.acton@durham.ac.uk)',
        'Accept': 'application/json'
    }
    
    print("Fetching publications from Semantic Scholar...")
    try:
        response = requests.get(papers_url, params=params, headers=headers)
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()
        print(f"Found {len(data.get('data', []))} publications")
        return data.get('data', [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching papers: {str(e)}")
        if hasattr(response, 'text'):
            print(f"Response: {response.text}")
        return None

def format_authors(authors):
    """Format author names in APA style (Last, F. M.)."""
    def format_name(name):
        parts = name.split()
        if len(parts) < 2:
            return name
        last = parts[-1]
        initials = ''.join(p[0] + '.' for p in parts[:-1])
        return f"{last}, {initials}"
    
    if len(authors) == 1:
        return format_name(authors[0]['name'])
    elif len(authors) == 2:
        return f"{format_name(authors[0]['name'])} & {format_name(authors[1]['name'])}"
    else:
        names = [format_name(author['name']) for author in authors]
        return f"{', '.join(names[:-1])}, & {names[-1]}"

def format_apa_citation(pub):
    """Format a publication in APA style."""
    # Authors and year
    citation = f"{pub['authors']} ({pub['year']}). "
    
    # Title (no italics in the data file, will be handled in the template)
    citation += f"{pub['title']}"
    
    # Journal name and publication details
    citation += f". {pub['journal']}"
    
    # Add pages if available
    if pub.get('pages'):
        citation += f", {pub['pages']}"
    
    # Add DOI as a clickable link
    if pub.get('doi'):
        citation += f". [doi:{pub['doi']}](https://doi.org/{pub['doi']})"
    
    return citation

def is_journal_article(paper):
    """Check if the paper is a proper journal article (not a conference proceeding)."""
    # Check if it's a known journal article
    if paper.get('title') in KNOWN_ARTICLES:
        return True
    
    venue = paper.get('venue', '').lower()
    return (
        venue and 
        'proceedings' not in venue and 
        'conference' not in venue and
        'academy of management proceedings' not in venue
    )

def update_publications_yaml(papers):
    """Update the publications.yaml file with fetched data."""
    if not papers:
        print("No papers to process")
        return
    
    # Initialize publications structure with only peer-reviewed articles
    publications = {
        'peer_reviewed': []
    }
    
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    
    # Process papers from Semantic Scholar
    for paper in papers:
        # Debug information
        print(f"\nProcessing paper: {paper.get('title', 'No title')}")
        print(f"Publication types: {paper.get('publicationTypes', [])}")
        print(f"Venue: {paper.get('venue', 'No venue')}")
        
        title = paper.get('title', '')
        
        # Check if this is a known article
        known_info = KNOWN_ARTICLES.get(title)
        if known_info:
            print("Found known journal article")
            pub_entry = {
                'authors': format_authors(paper['authors']),
                'year': known_info['year'],
                'title': title,
                'journal': known_info['journal'],
                'pages': known_info.get('pages', ''),
                'doi': known_info.get('doi', '')
            }
        else:
            # Skip papers without a venue or title, or if it's not a journal article
            if not paper.get('venue') or not paper.get('title') or not is_journal_article(paper):
                print("Skipping paper: Not a journal article or missing information")
                continue
            
            pub_entry = {
                'authors': format_authors(paper['authors']),
                'year': paper.get('year', ''),
                'title': paper.get('title', ''),
                'journal': paper.get('venue', '')
            }
            
            # Get DOI if available
            external_ids = paper.get('externalIds', {})
            if external_ids and 'DOI' in external_ids:
                pub_entry['doi'] = external_ids['DOI']
        
        # Get citation count if available
        if paper.get('citationCount'):
            pub_entry['citations'] = paper['citationCount']
        
        # Add formatted APA citation
        pub_entry['citation'] = format_apa_citation(pub_entry)
        
        publications['peer_reviewed'].append(pub_entry)
    
    # Sort by year (descending) and then by title
    publications['peer_reviewed'].sort(key=lambda x: (-int(x['year']) if x['year'] else 0, x['title']))
    
    # Save to YAML file
    with open('data/publications.yaml', 'w') as f:
        yaml.dump(publications, f, sort_keys=False, allow_unicode=True)
    
    print(f"\nUpdated publications.yaml with {len(publications['peer_reviewed'])} peer-reviewed articles")

def main():
    # Change to the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(os.path.dirname(script_dir))  # Move up one level to the project root
    
    # Fetch publications using your Semantic Scholar ID
    papers = fetch_publications()
    if papers:
        # Update YAML file
        update_publications_yaml(papers)
        print("\nDone! You can now run ./build.sh to update your CV.")
    else:
        print("Failed to fetch publications.")

if __name__ == "__main__":
    main() 