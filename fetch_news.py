import feedparser
import json
import re
from datetime import datetime

# MAXIMUM SOURCES LIST (2026 TOP TIER)
SOURCES = [
    # Top Journals
    "http://feeds.nature.com/nnano/rss/current",        # Nature Nanotechnology
    "https://pubs.acs.org/journal/ancac3/feed",         # ACS Nano
    "https://pubs.rsc.org/en/journals/journalissues/nr/rss", # RSC Nanoscale
    "https://onlinelibrary.wiley.com/feed/16136829/most-recent", # Small (Wiley)
    "https://onlinelibrary.wiley.com/feed/15214095/most-recent", # Advanced Materials
    
    # Research Institutes
    "https://news.mit.edu/topic/nanotech",              # MIT
    "https://cnm.anl.gov/pages/news",                   # Argonne National Lab
    "https://www.nano.gov/rss/news.xml",                # US NNI
    
    # Industry & High-Volume
    "https://www.nanowerk.com/nwfeedcomplete.xml",      # Nanowerk
    "https://phys.org/rss-feed/nanotechnology-news/",   # Phys.org
    "https://www.sciencedaily.com/rss/matter_energy/nanotechnology.xml", # ScienceDaily
    "https://www.azonano.com/syndication.axd?format=rss", # AZoNano
    "https://www.nanotechnologyworld.org/blog-feed.xml" # Nanotechnology World
]

def extract_image(entry):
    """Tries to find an image URL in the RSS entry (media tags or HTML content)."""
    # 1. Look for media:content or enclosures
    if 'links' in entry:
        for link in entry.links:
            if 'image' in link.get('type', ''):
                return link.get('href')
    
    # 2. Look for images in the description/summary HTML
    content = entry.get('summary', '') + entry.get('description', '')
    img_match = re.search(r'<img [^>]*src="([^"]+)"', content)
    if img_match:
        return img_match.group(1)
    
    # 3. Default placeholder if no image found
    return "https://images.unsplash.com/photo-1532187875460-1454f776473d?auto=format&fit=crop&q=80&w=400"

def get_category(title):
    t = title.lower()
    if any(x in t for x in ['cancer', 'bio', 'medical', 'drug', 'health']): return 'Nanomedicine'
    if any(x in t for x in ['battery', 'solar', 'energy', 'carbon', 'climate']): return 'Energy'
    if any(x in t for x in ['quantum', 'chip', 'sensor', 'electronics', 'semiconductor']): return 'Electronics'
    return 'Materials'

def fetch_news():
    all_articles = []
    seen_links = set()

    for url in SOURCES:
        try:
            feed = feedparser.parse(url)
            source_name = feed.feed.get('title', 'Nano Source').split(' - ')[0].split('|')[0].strip()
            
            for entry in feed.entries[:8]:
                if entry.link not in seen_links:
                    all_articles.append({
                        "title": entry.title,
                        "link": entry.link,
                        "source": source_name,
                        "image": extract_image(entry),
                        "category": get_category(entry.title),
                        "date": entry.get('published', 'Recent')
                    })
                    seen_links.add(entry.link)
        except Exception as e:
            print(f"Error fetching {url}: {e}")

    with open('data.json', 'w') as f:
        json.dump(all_articles, f, indent=4)

if __name__ == "__main__":
    fetch_news()
