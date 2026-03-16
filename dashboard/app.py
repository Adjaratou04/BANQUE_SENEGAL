import sys
import os

# ajouter le dossier dashboard au path
sys.path.append(os.path.dirname(__file__))

from dash import Dash
from layout import create_layout
from callbacks import register_callbacks


app = Dash(__name__)

app.layout = create_layout()

register_callbacks(app)


if __name__ == "__main__":
    app.run(debug=True)