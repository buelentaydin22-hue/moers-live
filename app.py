from flask import Flask, render_template
import json
from pathlib import Path

app = Flask(__name__)

BASE_DIR = Path(__file__).parent
CACHE_FILE = BASE_DIR / "cache.json"

def load_posts():
    if CACHE_FILE.exists():
        try:
            with open(CACHE_FILE, encoding="utf-8") as f:
                data = json.load(f)
            return data.get("posts", [])
        except:
            return []
    return []

@app.route("/")
def index():
    posts = load_posts()
    return render_template("index.html", posts=posts)

@app.route("/events")
def events():
    # vorerst alle Beiträge anzeigen – später können wir echte Event-Quellen einbauen
    posts = load_posts()
    return render_template("index.html", posts=posts)

@app.route("/local")
def local():
    # nur Einträge mit category == "local"
    posts = [p for p in load_posts() if p.get("category") == "local"]
    return render_template("index.html", posts=posts)

@app.route("/kontakt")
def kontakt():
    return render_template("kontakt.html", page_title="Kontakt")

@app.route("/impressum")
def impressum():
    return render_template("impressum.html", page_title="Impressum")

@app.route("/datenschutz")
def datenschutz():
    return render_template("datenschutz.html", page_title="Datenschutzerklärung")
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
