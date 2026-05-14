import feedparser
import json
from datetime import datetime

# Prestigious 2026 Nanotech Sources
SOURCES = [
    "http://feeds.nature.com/nnano/rss/current",        # Nature Nanotechnology
    "https://pubs.acs.org/journal/ancac3/feed",         # ACS Nano
    "https://www.nanowerk.com/nwfeedcomplete.xml",      # Nanowerk Industry News
    "https://phys.org/rss-feed/nanotechnology-news/",   # Phys.org Nanotechnology
]

def fetch_and_clean():
    all_articles = []
    seen_links = set()

    for url in SOURCES:
        feed = feedparser.parse(url)
        source_name = feed.feed.get('title', 'Nanotech Source')
        
        for entry in feed.entries[:10]:
            if entry.link not in seen_links:
                all_articles.append({
                    "title": entry.title,
                    "link": entry.link,
                    "source": source_name.split('|')[0].strip(), # Clean name
                    "updated": entry.get('published', 'Recently')
                })
                seen_links.add(entry.link)

    # Save as JSON for the website to read
    with open('data.json', 'w') as f:
        json.dump(all_articles, f, indent=4)

if __name__ == "__main__":
    fetch_and_clean()