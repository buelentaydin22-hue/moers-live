import json
import datetime
import re
import feedparser


# ============================================
# Bild-URL aus einem Feed-Eintrag extrahieren
# ============================================
def extract_image(entry):
    """Extrahiert ein Bild aus dem Feed-Eintrag, falls vorhanden."""
    # media_content
    if hasattr(entry, "media_content"):
        try:
            return entry.media_content[0].get("url", "")
        except Exception:
            pass

    # media_thumbnail
    if hasattr(entry, "media_thumbnail"):
        try:
            return entry.media_thumbnail[0].get("url", "")
        except Exception:
            pass

    # enclosures
    if hasattr(entry, "enclosures"):
        try:
            return entry.enclosures[0].get("href", "")
        except Exception:
            pass

    # nichts gefunden
    return ""


# ============================================
# Summary aufräumen (HTML entfernen)
# ============================================
def clean_summary(text):
    """Entfernt HTML (z.B. <img ...>) aus Summary und kürzt Text."""
    if not text:
        return ""
    # <img ...> entfernen
    text = re.sub(r"<img[^>]*>", "", text)
    # alle anderen HTML-Tags entfernen
    text = re.sub(r"<[^>]+>", "", text)
    # Leerzeichen und Länge
    return text.strip()[:300]


# ============================================
# RSS-Quellen (Kategorien)
# ============================================
SOURCES = [

    # --- Allgemeine Nachrichten ---
    {
        "name": "Tagesschau",
        "url": "https://www.tagesschau.de/xml/rss2",
        "category": "news",
    },
    {
        "name": "Spiegel Online",
        "url": "https://www.spiegel.de/schlagzeilen/tops/index.rss",
        "category": "news",
    },

    # --- Wirtschaft ---
    {
        "name": "Handelsblatt",
        "url": "https://www.handelsblatt.com/contentexport/feed/schlagzeilen",
        "category": "business",
    },

    # --- Technik / Digital ---
    {
        "name": "Heise Online",
        "url": "https://www.heise.de/rss/heise-atom.xml",
        "category": "tech",
    },
    {
        "name": "Golem",
        "url": "https://rss.golem.de/rss.php?feed=RSS2.0",
        "category": "tech",
    },

    # --- Lokal / Moers / Niederrhein (funktionierende Quellen) ---
    {
        "name": "LZ NRW",
        "url": "https://www.lz.de/rss",
        "category": "local",
    },
    {
        "name": "Westfalenpost",
        "url": "https://www.wp.de/staedte/rss",
        "category": "local",
    },
    {
        "name": "Neue Westfälische",
        "url": "https://www.nw.de/_export/rss/",
        "category": "local",
    },
    {
        "name": "General-Anzeiger Bonn",
        "url": "https://ga.de/feed.rss",
        "category": "local",
    },
]


# ============================================
# Feeds abrufen und in cache.json speichern
# ============================================
def fetch_posts():
    posts = []

    for src in SOURCES:
        feed = feedparser.parse(src["url"])

        for entry in feed.entries[:10]:
            image_url = extract_image(entry)
            raw_summary = entry.get("summary", "") or entry.get("description", "")
            summary = clean_summary(raw_summary)

            posts.append(
                {
                    "source": src["name"],
                    "category": src["category"],
                    "title": entry.get("title", ""),
                    "summary": summary,
                    "url": entry.get("link", ""),
                    "published": entry.get("published", ""),
                    "image": image_url,
                }
            )

    # nach Datum sortieren (wenn möglich)
    posts.sort(key=lambda p: p.get("published", ""), reverse=True)

    data = {
        "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
        "posts": posts,
    }

    with open("cache.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"{len(posts)} Einträge gespeichert.")


if __name__ == "__main__":
    fetch_posts()
