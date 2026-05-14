import feedparser
import json

# MAXIMUM TOP-TIER SOURCES
SOURCES = [
    "http://feeds.nature.com/nnano/rss/current",        # Nature Nanotechnology
    "https://pubs.acs.org/journal/ancac3/feed",         # ACS Nano
    "https://pubs.rsc.org/en/journals/journalissues/nr/rss", # RSC Nanoscale
    "https://onlinelibrary.wiley.com/feed/16136829/most-recent", # Small (Wiley)
    "https://news.mit.edu/topic/nanotech",              # MIT Nano
    "https://www.nano.gov/rss/news.xml",                # National Nano Initiative
    "https://www.nanowerk.com/nwfeedcomplete.xml",      # Nanowerk
    "https://phys.org/rss-feed/nanotechnology-news/",   # Phys.org
    "https://www.sciencedaily.com/rss/matter_energy/nanotechnology.xml", # ScienceDaily
    "https://www.azonano.com/syndication.axd?format=rss" # AZoNano
]

def fetch_news():
    all_articles = []
    seen_links = set()

    for url in SOURCES:
        try:
            feed = feedparser.parse(url)
            # Clean up the source name for display
            source_label = feed.feed.get('title', 'Nanotech News').split('|')[0].split(' - ')[0].strip()
            
            for entry in feed.entries[:10]:
                if entry.link not in seen_links:
                    all_articles.append({
                        "title": entry.title,
                        "link": entry.link,
                        "source": source_label,
                        "date": entry.get('published', 'Latest')
                    })
                    seen_links.add(entry.link)
        except:
            continue

    with open('data.json', 'w') as f:
        json.dump(all_articles, f, indent=4)

if __name__ == "__main__":
    fetch_news()
