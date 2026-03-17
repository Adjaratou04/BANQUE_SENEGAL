from flask import Flask, render_template
from dash import Dash

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from dashboard.layout import create_layout
from dashboard.callbacks import register_callbacks

# Chemins explicites
BASE_DIR     = os.path.dirname(__file__)
template_dir = os.path.join(BASE_DIR, "templates")
assets_dir   = os.path.join(os.path.dirname(BASE_DIR), "dashboard", "assets")

# ── Serveur Flask ──────────────────────────────────────────
server = Flask(__name__, template_folder=template_dir)

# ── Page d'accueil ─────────────────────────────────────────
@server.route("/")
def home():
    return render_template("home.html")

# ── Route de test MongoDB ──────────────────────────────────
@server.route("/test-mongo")
def test_mongo():
    try:
        from database.mongo_connection import get_database
        db = get_database()
        collections = db.list_collection_names()
        count = db["banque"].count_documents({})
        return f"Collections: {collections} | Documents: {count}"
    except Exception as e:
        return f"ERREUR: {str(e)}"

# ── Dashboard Bancaire ─────────────────────────────────────
app = Dash(
    __name__,
    server=server,
    url_base_pathname="/banques/",
    assets_folder=assets_dir
)

app.layout = create_layout()
register_callbacks(app)

if __name__ == "__main__":
    server.run(debug=True)