import feedparser
import json

# MAXIMUM SOURCES LIST
SOURCES = [
    "http://feeds.nature.com/nnano/rss/current",
    "https://pubs.acs.org/journal/ancac3/feed",
    "https://pubs.rsc.org/en/journals/journalissues/nr/rss",
    "https://onlinelibrary.wiley.com/feed/16136829/most-recent",
    "https://news.mit.edu/topic/nanotech",
    "https://cnm.anl.gov/pages/news",
    "https://www.nano.gov/rss/news.xml",
    "https://www.nanowerk.com/nwfeedcomplete.xml",
    "https://phys.org/rss-feed/nanotechnology-news/",
    "https://www.sciencedaily.com/rss/matter_energy/nanotechnology.xml",
    "https://www.azonano.com/syndication.axd?format=rss"
]

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
