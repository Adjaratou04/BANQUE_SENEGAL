# =============================================================================
# callbacks.py
# Logique interactive du dashboard — graphiques, filtres, exports
# Secteur Bancaire Sénégalais · Données BCEAO
# =============================================================================

from dash import dcc, Input, Output, State
import sys
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
import numpy as np

# Ajout du répertoire parent au path pour les imports relatifs
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from database.mongo_connection import get_database

# =============================================================================
# PALETTE DE COULEURS — une couleur fixe et unique par banque
# =============================================================================
COLOR_PALETTE = [
    "#4FC3F7", "#81C784", "#F48FB1", "#E8C96A",
    "#CE93D8", "#FFAB76", "#80DEEA", "#F06292",
    "#90CAF9", "#FFD54F", "#A5D6A7", "#B39DDB",
    "#FF8A65", "#4DB6AC", "#DCE775", "#FF7043",
    "#26C6DA", "#EC407A", "#66BB6A", "#AB47BC",
]

# =============================================================================
# COORDONNÉES GPS — sièges sociaux réels des banques à Dakar
# =============================================================================
BANK_LOCATIONS = {
    "CBAO":    {"lat": 14.6928, "lon": -17.4467, "ville": "Dakar - Plateau"},
    "SGBS":    {"lat": 14.6892, "lon": -17.4390, "ville": "Dakar - Plateau"},
    "BICIS":   {"lat": 14.6915, "lon": -17.4380, "ville": "Dakar - Plateau"},
    "ECOBANK": {"lat": 14.7167, "lon": -17.4677, "ville": "Dakar - Almadies"},
    "ATW":     {"lat": 14.6950, "lon": -17.4420, "ville": "Dakar - Plateau"},
    "BIS":     {"lat": 14.6870, "lon": -17.4350, "ville": "Dakar - Medina"},
    "BOA":     {"lat": 14.7012, "lon": -17.4580, "ville": "Dakar - Mermoz"},
    "BHM":     {"lat": 14.6830, "lon": -17.4280, "ville": "Dakar - Grand Yoff"},
    "BNDE":    {"lat": 14.6940, "lon": -17.4500, "ville": "Dakar - Plateau"},
    "BRS":     {"lat": 14.6960, "lon": -17.4440, "ville": "Dakar - Plateau"},
    "CAB":     {"lat": 14.7080, "lon": -17.4620, "ville": "Dakar - Liberte"},
    "CBI":     {"lat": 14.6880, "lon": -17.4410, "ville": "Dakar - Plateau"},
    "CNCAS":   {"lat": 14.7200, "lon": -17.4700, "ville": "Dakar - Point E"},
    "CNI":     {"lat": 14.6905, "lon": -17.4395, "ville": "Dakar - Plateau"},
    "UBA":     {"lat": 14.6945, "lon": -17.4460, "ville": "Dakar - Plateau"},
    "GIM":     {"lat": 14.7100, "lon": -17.4640, "ville": "Dakar - Liberte"},
    "ORA":     {"lat": 14.6898, "lon": -17.4425, "ville": "Dakar - Plateau"},
    "SAR":     {"lat": 14.7050, "lon": -17.4600, "ville": "Dakar - Fann"},
    "MBK":     {"lat": 14.6910, "lon": -17.4370, "ville": "Dakar - Plateau"},
    "DGB":     {"lat": 14.6935, "lon": -17.4415, "ville": "Dakar - Plateau"},
}

# =============================================================================
# LAYOUT VIDE — affiché quand aucune donnée n'est disponible
# =============================================================================
EMPTY_LAYOUT = dict(
    plot_bgcolor="#080B12",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#8A8070"),
    xaxis=dict(visible=False),
    yaxis=dict(visible=False),
    annotations=[dict(
        text="Aucune donnée disponible",
        xref="paper", yref="paper", x=0.5, y=0.5,
        showarrow=False, font=dict(color="#8A8070", size=14)
    )]
)

def empty_fig():
    """Retourne un graphique vide avec message d'information."""
    return go.Figure(layout=EMPTY_LAYOUT)


# =============================================================================
# UTILITAIRES
# =============================================================================

def get_bank_coords(sigle):
    """
    Retourne les coordonnées GPS d'une banque à partir de son sigle.
    Si le sigle n'est pas trouvé, génère des coordonnées pseudo-aléatoires
    basées sur un hash MD5 pour assurer la reproductibilité.
    """
    if sigle in BANK_LOCATIONS:
        return BANK_LOCATIONS[sigle]
    for key in BANK_LOCATIONS:
        if key in sigle or sigle in key:
            return BANK_LOCATIONS[key]
    import hashlib
    h = int(hashlib.md5(sigle.encode()).hexdigest(), 16)
    return {
        "lat": 14.680 + (h % 100) * 0.0004,
        "lon": -17.460 + (h % 137) * 0.0003,
        "ville": "Dakar"
    }


def get_data():
    """
    Récupère toutes les données bancaires depuis MongoDB Atlas.
    Base de données : Baqnues_senegal
    Collection      : banque  ⚠️ (sans 's' — nom exact dans Atlas)
    Retourne un DataFrame pandas.
    """
    db = get_database()
    collection = db["banque"]  # ⚠️ Nom exact de la collection dans MongoDB Atlas
    data = list(collection.find())
    df = pd.DataFrame(data)
    return df


def fmt(val):
    """
    Formate un nombre en valeur lisible avec unité FCFA.
    Exemples : 1 500 000 000 → '1.5 Md FCFA' | 500 000 → '500 M FCFA'
    """
    try:
        if pd.isna(val):
            return "N/A"
        val = float(val)
        if abs(val) >= 1e9:
            return f"{val/1e9:.1f} Md FCFA"
        elif abs(val) >= 1e6:
            return f"{val/1e6:.0f} M FCFA"
        return f"{val:,.0f} FCFA"
    except Exception:
        return "N/A"


def pct(val):
    """Formate un ratio décimal en pourcentage. Ex : 0.085 → '8.50%'"""
    try:
        if pd.isna(val):
            return "N/A"
        return f"{float(val)*100:.2f}%"
    except Exception:
        return "N/A"


def safe_div(num, den):
    """
    Division sécurisée entre deux Series pandas.
    Remplace les 0 au dénominateur par NaN pour éviter ZeroDivisionError.
    """
    return num / den.replace(0, np.nan)


def safe_max(series):
    """
    Retourne le maximum d'une Series en ignorant les NaN.
    Retourne 1 si la série est vide ou nulle (pour éviter les divisions par 0).
    """
    try:
        m = series.dropna().max()
        return m if (m and m != 0) else 1
    except Exception:
        return 1


# =============================================================================
# INTERPRÉTATIONS AUTOMATIQUES
# Chaque fonction génère un texte pédagogique expliquant les données.
# Toutes sont protégées par try/except pour éviter les erreurs en cascade.
# =============================================================================

def interpret_bilan(df_year):
    """Interprétation du graphique Bilan — taille financière des banques."""
    try:
        df_v = df_year.dropna(subset=["BILAN"])
        if df_v.empty: return "Aucune donnée disponible."
        top   = df_v.nlargest(1, "BILAN").iloc[0]
        bot   = df_v.nsmallest(1, "BILAN").iloc[0]
        moy   = df_v["BILAN"].mean()
        ratio = top["BILAN"] / bot["BILAN"] if bot["BILAN"] > 0 else 0
        return (f"Le bilan mesure la taille d'une banque. {top['Sigle']} domine avec {fmt(top['BILAN'])}, "
                f"soit {ratio:.1f}x le bilan de {bot['Sigle']} ({fmt(bot['BILAN'])}). "
                f"Moyenne sectorielle : {fmt(moy)}. "
                f"{'Forte concentration du marché.' if ratio > 3 else 'Répartition relativement équilibrée.'}")
    except Exception as e: return f"Interprétation indisponible ({e})."


def interpret_resultat(df_year):
    """Interprétation du graphique Résultat Net — rentabilité des banques."""
    try:
        df_v = df_year.dropna(subset=["RESULTAT.NET"])
        if df_v.empty: return "Aucune donnée disponible."
        top = df_v.nlargest(1, "RESULTAT.NET").iloc[0]
        neg = df_v[df_v["RESULTAT.NET"] < 0]
        return (f"Le résultat net mesure le bénéfice ou la perte après toutes charges. "
                f"{top['Sigle']} mène avec {fmt(top['RESULTAT.NET'])}. "
                f"Résultat cumulé : {fmt(df_v['RESULTAT.NET'].sum())}. "
                + (f"{len(neg)} banque(s) en perte : {', '.join(neg['Sigle'].tolist())}."
                   if not neg.empty else "Aucune banque en perte sur cette période."))
    except Exception as e: return f"Interprétation indisponible ({e})."


def interpret_evolution(df):
    """Interprétation du graphique d'évolution du bilan sur plusieurs années."""
    try:
        if df.empty: return "Aucune donnée disponible."
        years = sorted(df["ANNEE"].dropna().unique())
        if len(years) < 2: return "Il faut au moins deux années de données."
        bp = df.groupby("ANNEE")["BILAN"].sum()
        c  = (bp.iloc[-1] - bp.iloc[0]) / bp.iloc[0] * 100 if bp.iloc[0] != 0 else 0
        return (f"Sur {int(years[0])}–{int(years[-1])}, le bilan agrégé a "
                f"{'progressé' if c > 0 else 'reculé'} de {abs(c):.1f}%. "
                f"Observez les banques dont la courbe accélère en fin de période.")
    except Exception as e: return f"Interprétation indisponible ({e})."


def interpret_ranking(df_year):
    """Interprétation du classement par résultat net."""
    try:
        df_v = df_year.dropna(subset=["RESULTAT.NET"])
        if df_v.empty: return "Aucune donnée disponible."
        top3 = df_v.nlargest(min(3, len(df_v)), "RESULTAT.NET")["Sigle"].tolist()
        return (f"Classement par bénéfice net — premières places : {', '.join(top3)}. "
                f"Un bon classement ne signifie pas forcément une grande taille.")
    except Exception as e: return f"Interprétation indisponible ({e})."


def interpret_score(df_year):
    """Interprétation du score global composite (bilan + résultat + fonds propres + ROA)."""
    try:
        if df_year.empty: return "Aucune donnée disponible."
        df_s = df_year.copy()
        df_s["ROA"] = safe_div(df_s["RESULTAT.NET"], df_s["BILAN"])
        for col in ["BILAN", "RESULTAT.NET", "FONDS.PROPRE", "ROA"]:
            df_s[col + "_n"] = df_s[col].fillna(0) / safe_max(df_s[col])
        df_s["Score"] = df_s[["BILAN_n","RESULTAT.NET_n","FONDS.PROPRE_n","ROA_n"]].sum(axis=1)
        top = df_s.nlargest(1, "Score").iloc[0]
        return (f"Score global = taille + rentabilité + solidité + efficacité (max 4). "
                f"{top['Sigle']} obtient {top['Score']:.2f}/4 — banque la plus équilibrée.")
    except Exception as e: return f"Interprétation indisponible ({e})."


def interpret_roa(df_year):
    """Interprétation du ROA — efficacité d'utilisation des actifs."""
    try:
        df_r = df_year.copy()
        df_r["ROA"] = safe_div(df_r["RESULTAT.NET"], df_r["BILAN"])
        df_v = df_r.dropna(subset=["ROA"])
        if df_v.empty: return "Aucune donnée disponible."
        top = df_v.nlargest(1, "ROA").iloc[0]
        return (f"ROA = résultat net / total actifs. "
                f"{top['Sigle']} est la plus efficace ({pct(top['ROA'])}), "
                f"moyenne : {pct(df_v['ROA'].mean())}.")
    except Exception as e: return f"Interprétation indisponible ({e})."


def interpret_solvency(df_year):
    """Interprétation de la solvabilité — capacité à absorber les pertes."""
    try:
        df_s = df_year.copy()
        df_s["Solvency"] = safe_div(df_s["FONDS.PROPRE"], df_s["BILAN"])
        df_v = df_s.dropna(subset=["Solvency"])
        if df_v.empty: return "Aucune donnée disponible."
        top      = df_v.nlargest(1, "Solvency").iloc[0]
        fragiles = df_v[df_v["Solvency"] < 0.08]["Sigle"].tolist()
        return (f"Solvabilité = fonds propres / bilan. Norme BCEAO minimale : 8%. "
                f"{top['Sigle']} est le mieux capitalisé ({pct(top['Solvency'])}). "
                + (f"⚠️ Sous le seuil : {', '.join(fragiles)}."
                   if fragiles else "✅ Toutes les banques respectent la norme BCEAO."))
    except Exception as e: return f"Interprétation indisponible ({e})."


def interpret_emploi(df_year):
    """Interprétation des emplois bancaires — crédits, placements, investissements."""
    try:
        df_v = df_year.dropna(subset=["EMPLOI"])
        if df_v.empty: return "Aucune donnée disponible."
        top = df_v.nlargest(1, "EMPLOI").iloc[0]
        return (f"Emplois = crédits + placements + investissements. "
                f"{top['Sigle']} est le plus actif avec {fmt(top['EMPLOI'])} "
                f"sur {fmt(df_v['EMPLOI'].sum())} au total.")
    except Exception as e: return f"Interprétation indisponible ({e})."


def interpret_ressources(df_year):
    """Interprétation des ressources bancaires — dépôts, emprunts, financements."""
    try:
        df_v = df_year.dropna(subset=["RESSOURCES"])
        if df_v.empty: return "Aucune donnée disponible."
        top = df_v.nlargest(1, "RESSOURCES").iloc[0]
        return (f"Ressources = dépôts + emprunts + financements. "
                f"{top['Sigle']} collecte le plus : {fmt(top['RESSOURCES'])} "
                f"sur {fmt(df_v['RESSOURCES'].sum())} au total.")
    except Exception as e: return f"Interprétation indisponible ({e})."


def interpret_positioning(df_year):
    """Interprétation du positionnement stratégique — taille vs rentabilité."""
    try:
        if df_year.empty: return "Aucune donnée disponible."
        df_p = df_year.copy()
        df_p["ROA"] = safe_div(df_p["RESULTAT.NET"], df_p["BILAN"])
        leaders = df_p[(df_p["ROA"] >= df_p["ROA"].median()) &
                       (df_p["BILAN"] >= df_p["BILAN"].median())]["Sigle"].tolist()
        return (f"Axe X : efficacité (ROA) · Axe Y : taille (bilan). "
                f"En haut à droite : grandes ET rentables. "
                + (f"Leaders : {', '.join(leaders)}." if leaders else ""))
    except Exception as e: return f"Interprétation indisponible ({e})."


def interpret_matrix(df_year):
    """Interprétation de la matrice stratégique."""
    try:
        if df_year.empty: return "Aucune donnée disponible."
        df_m = df_year.copy()
        df_m["ROA"] = safe_div(df_m["RESULTAT.NET"], df_m["BILAN"])
        df_v = df_m.dropna(subset=["ROA","BILAN"])
        if df_v.empty: return "Aucune donnée disponible."
        tr = df_v.nlargest(1,"ROA").iloc[0]
        tb = df_v.nlargest(1,"BILAN").iloc[0]
        return (f"{tb['Sigle']} est la plus grande banque ; {tr['Sigle']} est la plus efficace. "
                f"{'La taille ne garantit pas la rentabilité.' if tb['Sigle'] != tr['Sigle'] else ''}")
    except Exception as e: return f"Interprétation indisponible ({e})."


def interpret_marketshare(df_year):
    """Interprétation des parts de marché par bilan."""
    try:
        df_v  = df_year.dropna(subset=["BILAN"])
        total = df_v["BILAN"].sum()
        if total == 0: return "Données insuffisantes."
        top = df_v.nlargest(1,"BILAN").iloc[0]
        p3  = df_v.nlargest(3,"BILAN")["BILAN"].sum() / total * 100
        return (f"{top['Sigle']} détient {top['BILAN']/total*100:.1f}% du marché. "
                f"Top 3 : {p3:.1f}%. "
                f"{'Marché très concentré.' if p3 > 60 else 'Marché diversifié.'}")
    except Exception as e: return f"Interprétation indisponible ({e})."


def interpret_map(df_year):
    """Interprétation de la carte géographique des banques."""
    try:
        return (f"{len(df_year)} banque(s) localisée(s) à Dakar. "
                f"Taille des bulles proportionnelle au bilan.")
    except Exception as e: return f"Interprétation indisponible ({e})."


def interpret_prediction(df):
    """Interprétation de la prévision par régression linéaire."""
    try:
        bp = df.groupby("ANNEE")["BILAN"].sum().reset_index()
        if len(bp) < 2: return "Données insuffisantes pour une projection."
        mdl = LinearRegression().fit(bp["ANNEE"].values.reshape(-1,1), bp["BILAN"].values)
        am  = int(bp["ANNEE"].max())
        p1  = mdl.predict([[am+1]])[0]
        p3  = mdl.predict([[am+3]])[0]
        t   = "croissance" if mdl.coef_[0] > 0 else "décroissance"
        return (f"Projection : {fmt(p1)} en {am+1}, {fmt(p3)} en {am+3}. "
                f"Tendance : {t} de {fmt(abs(mdl.coef_[0]))} par an. "
                f"⚠️ Estimation indicative — conditions économiques supposées stables.")
    except Exception as e: return f"Interprétation indisponible ({e})."


# =============================================================================
# ENREGISTREMENT DES CALLBACKS DASH
# =============================================================================

def register_callbacks(app):
    """
    Enregistre tous les callbacks Dash sur l'instance de l'application.
    5 callbacks :
      1. load_filters     — options des filtres Banque et Année
      2. switch_tab       — navigation entre les 11 onglets
      3. update_dashboard — mise à jour de tous les graphiques (44 sorties)
      4. download_excel   — export des données en Excel
      5. download_pdf     — génération du rapport PDF
    """

    # ─────────────────────────────────────────────────────
    # CALLBACK 1 — Chargement des filtres
    # ─────────────────────────────────────────────────────
    @app.callback(
        Output("bank-filter","options"),
        Output("year-filter","options"),
        Input("bank-filter","id")
    )
    def load_filters(_):
        """Charge les listes déroulantes Banque et Année depuis MongoDB."""
        df    = get_data()
        banks = sorted(df["Sigle"].dropna().unique())
        years = sorted(df["ANNEE"].dropna().unique())
        return ([{"label":b,"value":b} for b in banks],
                [{"label":y,"value":y} for y in years])

    # ─────────────────────────────────────────────────────
    # CALLBACK 2 — Navigation entre onglets
    # ─────────────────────────────────────────────────────
    TABS = ["tab-kpi","tab-bilan","tab-evolution","tab-classement","tab-ratios",
            "tab-positionnement","tab-marche","tab-comparaison",
            "tab-carte","tab-prevision","tab-synthese"]

    @app.callback(*[Output(t,"style") for t in TABS], Input("main-tabs","value"))
    def switch_tab(active):
        """Affiche l'onglet actif et masque tous les autres."""
        V = {"display":"block","animation":"sectionIn .4s ease forwards"}
        H = {"display":"none"}
        return [V if t == active else H for t in TABS]

    # ─────────────────────────────────────────────────────
    # CALLBACK 3 — Mise à jour du dashboard complet (44 sorties)
    # Déclenché à chaque changement de filtre Année ou Banque
    # ─────────────────────────────────────────────────────
    @app.callback(
        Output("bilan-chart","figure"),          # 1  — Bilan
        Output("resultat-chart","figure"),        # 2  — Résultat net
        Output("evolution-chart","figure"),       # 3  — Évolution temporelle
        Output("ratio-chart","figure"),           # 4  — ROA
        Output("ranking-chart","figure"),         # 5  — Classement
        Output("positioning-chart","figure"),     # 6  — Positionnement
        Output("score-chart","figure"),           # 7  — Score global
        Output("map-chart","figure"),             # 8  — Carte
        Output("marketshare-chart","figure"),     # 9  — Parts de marché
        Output("solvency-chart","figure"),        # 10 — Solvabilité
        Output("emploi-chart","figure"),          # 11 — Emplois
        Output("ressources-chart","figure"),      # 12 — Ressources
        Output("matrix-chart","figure"),          # 13 — Matrice
        Output("prediction-chart","figure"),      # 14 — Prévision
        Output("kpi-bilan","children"),           # 15 — KPI Bilan
        Output("kpi-resultat","children"),        # 16 — KPI Résultat
        Output("kpi-fonds","children"),           # 17 — KPI Fonds propres
        Output("kpi-pnb","children"),             # 18 — KPI PNB
        Output("analysis-text","children"),       # 19 — Analyse secteur (KPI)
        Output("bank-analysis","children"),       # 20 — Analyse banque (KPI)
        Output("interp-bilan","children"),        # 21 — Interp. bilan
        Output("interp-resultat","children"),     # 22 — Interp. résultat
        Output("interp-evolution","children"),    # 23 — Interp. évolution
        Output("interp-ranking","children"),      # 24 — Interp. classement
        Output("interp-score","children"),        # 25 — Interp. score
        Output("interp-roa","children"),          # 26 — Interp. ROA
        Output("interp-solvency","children"),     # 27 — Interp. solvabilité
        Output("interp-emploi","children"),       # 28 — Interp. emplois
        Output("interp-ressources","children"),   # 29 — Interp. ressources
        Output("interp-positioning","children"),  # 30 — Interp. positionnement
        Output("interp-matrix","children"),       # 31 — Interp. matrice
        Output("interp-marketshare","children"),  # 32 — Interp. parts de marché
        Output("interp-map","children"),          # 33 — Interp. carte
        Output("interp-prediction","children"),   # 34 — Interp. prévision
        Output("analysis-text-2","children"),     # 35 — Analyse secteur (Synthèse)
        Output("bank-analysis-2","children"),     # 36 — Analyse banque (Synthèse)
        Output("comp-chart-bilan-resultat","figure"),    # 37 — Comp. bilan/résultat
        Output("comp-chart-roa-solvency","figure"),      # 38 — Comp. ROA/solvabilité
        Output("comp-chart-emploi-ressources","figure"), # 39 — Comp. emplois/ressources
        Output("comp-chart-score-bilan","figure"),       # 40 — Comp. score/bilan
        Output("interp-comp-bilan","children"),   # 41 — Interp. comp. bilan
        Output("interp-comp-roa","children"),     # 42 — Interp. comp. ROA
        Output("interp-comp-emploi","children"),  # 43 — Interp. comp. emplois
        Output("interp-comp-score","children"),   # 44 — Interp. comp. score
        Input("year-filter","value"),
        Input("bank-filter","value")
    )
    def update_dashboard(year, bank):
        """Mise à jour complète du dashboard selon les filtres sélectionnés."""

        # ── Chargement et filtrage des données ───────────
        df = get_data()
        df_year = df[df["ANNEE"] == year].copy() if year else df.copy()
        if bank:
            df_year = df_year[df_year["Sigle"] == bank].copy()

        # Palette cohérente : une couleur fixe par banque
        toutes = sorted(df["Sigle"].dropna().unique())
        cmap   = {b: COLOR_PALETTE[i % len(COLOR_PALETTE)] for i, b in enumerate(toutes)}

        # ── Calcul des KPI ────────────────────────────────
        def col_sum(col):
            """Somme sécurisée d'une colonne (retourne 0 si absente)."""
            return df_year[col].sum() if col in df_year.columns else 0

        bilan_total    = col_sum("BILAN")
        resultat_total = col_sum("RESULTAT.NET")
        fonds_total    = col_sum("FONDS.PROPRE")
        pnb_total      = col_sum("PRODUIT.NET.BANCAIRE")

        # ── Calcul des ratios financiers ──────────────────
        if not df_year.empty:
            df_year["ROA"]      = safe_div(df_year["RESULTAT.NET"], df_year["BILAN"])
            df_year["Solvency"] = safe_div(df_year["FONDS.PROPRE"], df_year["BILAN"])
            # Score composite normalisé sur 4 dimensions (max = 4)
            df_year["Score"] = (
                df_year["BILAN"].fillna(0)          / safe_max(df_year["BILAN"])
                + df_year["RESULTAT.NET"].fillna(0) / safe_max(df_year["RESULTAT.NET"])
                + df_year["FONDS.PROPRE"].fillna(0) / safe_max(df_year["FONDS.PROPRE"])
                + df_year["ROA"].fillna(0)           / safe_max(df_year["ROA"].fillna(0))
            )

        def bl(**kw):
            """Layout de base sombre pour tous les graphiques Plotly."""
            d = dict(plot_bgcolor="#080B12", paper_bgcolor="rgba(0,0,0,0)",
                     font=dict(color="#E8DCC8"), margin=dict(l=20,r=20,t=50,b=60))
            d.update(kw)
            return d

        def bar(col, title, sort=False):
            """
            Crée un bar chart coloré par banque.
            Retourne empty_fig() si les données sont absentes ou vides.
            """
            if df_year.empty or col not in df_year.columns:
                return empty_fig()
            src = df_year.sort_values(col, ascending=False) if sort else df_year
            f = px.bar(src, x="Sigle", y=col, color="Sigle",
                       color_discrete_map=cmap, title=title)
            f.update_layout(showlegend=False, **bl())
            f.update_traces(marker_line_width=0)
            return f

        # ── Graphiques simples ────────────────────────────
        fig_bilan      = bar("BILAN",        "Bilan des banques")
        fig_resultat   = bar("RESULTAT.NET", "Résultat net")
        fig_ratio      = bar("ROA",          "Rentabilité des actifs (ROA)")
        fig_ranking    = bar("RESULTAT.NET", "Classement par résultat", sort=True)
        fig_score      = bar("Score",        "Score global de performance", sort=True)
        fig_solvency   = bar("Solvency",     "Ratio de solvabilité")
        fig_emploi     = bar("EMPLOI",       "Emplois bancaires")
        fig_ressources = bar("RESSOURCES",   "Ressources bancaires")

        # Ligne BCEAO 8% sur le graphique de solvabilité
        if not df_year.empty:
            fig_solvency.add_hline(y=0.08, line_dash="dot", line_color="#C39B48",
                                   annotation_text="Norme BCEAO 8%",
                                   annotation_font_color="#C39B48", annotation_font_size=11)

        # ── Évolution temporelle (courbes multi-banques) ──
        if df.empty:
            fig_evolution = empty_fig()
        else:
            fig_evolution = px.line(df, x="ANNEE", y="BILAN", color="Sigle",
                                    color_discrete_map=cmap, markers=True,
                                    title="Évolution du bilan dans le temps")
            fig_evolution.update_layout(**bl())
            fig_evolution.update_traces(line_width=2.5, marker_size=7)

        # ── Positionnement stratégique (scatter) ─────────
        if df_year.empty or df_year["ROA"].isna().all():
            fig_position = empty_fig()
        else:
            fig_position = px.scatter(df_year, x="ROA", y="BILAN",
                                      text="Sigle", size="BILAN",
                                      color="Sigle", color_discrete_map=cmap,
                                      title="Positionnement — taille vs efficacité")
            fig_position.update_traces(textposition="top center",
                                       textfont=dict(color="#E8DCC8", size=11),
                                       marker=dict(line=dict(color="#080B12", width=1.5)))
            fig_position.update_layout(showlegend=False, **bl())

        # ── Carte géographique (OpenStreetMap) ───────────
        if df_year.empty:
            fig_map = empty_fig()
        else:
            lats = [get_bank_coords(str(s))["lat"] for s in df_year["Sigle"]]
            lons = [get_bank_coords(str(s))["lon"] for s in df_year["Sigle"]]
            fig_map = px.scatter_mapbox(df_year, lat=lats, lon=lons,
                                        size="BILAN", hover_name="Sigle",
                                        color="Sigle", color_discrete_map=cmap,
                                        zoom=12, size_max=45)
            fig_map.update_layout(mapbox_style="open-street-map",
                                  mapbox_center={"lat":14.693,"lon":-17.447},
                                  paper_bgcolor="rgba(0,0,0,0)",
                                  font=dict(color="#333333"),
                                  margin=dict(l=0,r=0,t=30,b=0), height=500)

        # ── Parts de marché (donut chart) ─────────────────
        if df_year.empty:
            fig_market = empty_fig()
        else:
            fig_market = px.pie(df_year, names="Sigle", values="BILAN",
                                color="Sigle", color_discrete_map=cmap,
                                title="Parts de marché par bilan", hole=0.4)
            fig_market.update_traces(textfont=dict(color="#E8DCC8", size=11),
                                     marker=dict(line=dict(color="#080B12", width=2)))
            fig_market.update_layout(paper_bgcolor="rgba(0,0,0,0)",
                                     font=dict(color="#E8DCC8"))

        # ── Matrice stratégique (scatter avec légende) ────
        if df_year.empty or df_year["ROA"].isna().all():
            fig_matrix = empty_fig()
        else:
            fig_matrix = px.scatter(df_year, x="ROA", y="BILAN",
                                    text="Sigle", size="BILAN",
                                    color="Sigle", color_discrete_map=cmap,
                                    title="Matrice stratégique")
            fig_matrix.update_traces(textposition="top center",
                                     textfont=dict(color="#E8DCC8", size=10),
                                     marker=dict(line=dict(color="#080B12", width=1.5)))
            fig_matrix.update_layout(showlegend=True, height=550,
                                     **bl(margin=dict(l=60,r=60,t=80,b=80)))

        # ── Prévision par régression linéaire ─────────────
        if df.empty or len(df.groupby("ANNEE")) < 2:
            fig_prediction = empty_fig()
        else:
            dp  = df.groupby("ANNEE")["BILAN"].sum().reset_index()
            mdl = LinearRegression().fit(dp["ANNEE"].values.reshape(-1,1), dp["BILAN"].values)
            am  = dp["ANNEE"].max()
            fut = np.arange(am+1, am+4).reshape(-1,1)
            # Concaténation historique + projections futures
            dt  = pd.concat([dp, pd.DataFrame({"ANNEE":fut.flatten(),"BILAN":mdl.predict(fut)})])
            fig_prediction = px.line(dt, x="ANNEE", y="BILAN",
                                     title="Prévision du bilan sectoriel (3 ans)")
            fig_prediction.update_layout(**bl())
            fig_prediction.update_traces(line_color="#C39B48", line_width=2.5)

        # ── Analyses textuelles automatiques ─────────────
        if df_year.empty:
            analysis = "Aucune donnée disponible."
            bank_analysis = ""
        else:
            tb = df_year.sort_values("BILAN",       ascending=False).iloc[0]["Sigle"]
            tr = df_year.sort_values("RESULTAT.NET", ascending=False).iloc[0]["Sigle"]
            analysis = (f"Analyse du secteur :\n\n"
                        f"· Banque dominante        : {tb}\n"
                        f"· Plus rentable           : {tr}\n"
                        f"· Bilan cumulé            : {fmt(bilan_total)}\n"
                        f"· Résultat net cumulé     : {fmt(resultat_total)}\n"
                        f"· Fonds propres agrégés   : {fmt(fonds_total)}\n"
                        f"· PNB agrégé              : {fmt(pnb_total)}\n")
            bank_analysis = ""
            if bank:
                # Analyse individuelle si une banque est sélectionnée
                r = df_year.iloc[0]
                b = r["BILAN"]; res = r["RESULTAT.NET"]; fp = r["FONDS.PROPRE"]
                bank_analysis = (f"Analyse détaillée — {bank} :\n\n"
                                 f"· Bilan         : {fmt(b)}\n"
                                 f"· Résultat net  : {fmt(res)}\n"
                                 f"· Fonds propres : {fmt(fp)}\n"
                                 f"· ROA           : {pct(res/b if b else 0)}\n"
                                 f"· Solvabilité   : {pct(fp/b if b else 0)}\n")

        # ── Graphiques onglet Comparaison ─────────────────
        # ⚠️ xaxis/yaxis retirés de CL pour éviter "multiple values for keyword argument"
        CL = dict(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#080B12",
                  font=dict(family="DM Sans", color="#E8DCC8", size=11),
                  legend=dict(bgcolor="rgba(13,16,24,0.85)", bordercolor="#C39B48",
                              borderwidth=0.5, font=dict(color="#E8DCC8", size=10)),
                  margin=dict(l=20,r=20,t=50,b=60), barmode="group", height=420)

        # Props d'axes réutilisables (fusionnés avec {**_ax, ...} dans chaque figure)
        _ax = dict(gridcolor="rgba(255,255,255,0.06)",
                   tickfont=dict(color="#8A8070", size=10), automargin=True)

        if df_year.empty:
            fc1 = fc2 = fc3 = fc4 = empty_fig()
        else:
            dc = df_year.sort_values("BILAN", ascending=False)

            # Comp1 : Bilan vs Résultat Net — double axe Y
            fc1 = go.Figure()
            fc1.add_trace(go.Bar(name="Bilan", x=dc["Sigle"], y=dc["BILAN"], yaxis="y",
                                 marker_color=[cmap.get(s,"#C39B48") for s in dc["Sigle"]],
                                 marker_line_width=0, opacity=0.9))
            fc1.add_trace(go.Bar(name="Résultat Net", x=dc["Sigle"], y=dc["RESULTAT.NET"],
                                 yaxis="y2",
                                 marker_color=[cmap.get(s,"#E8C96A") for s in dc["Sigle"]],
                                 marker_line_width=0, opacity=0.65))
            fc1.update_layout(**CL, xaxis={**_ax},
                              yaxis={**_ax,"title":"Bilan","title_font":dict(color="#4FC3F7")},
                              yaxis2=dict(title="Résultat",overlaying="y",side="right",
                                          title_font=dict(color="#81C784"),
                                          tickfont=dict(color="#8A8070",size=10),
                                          gridcolor="rgba(0,0,0,0)"))

            # Comp2 : ROA vs Solvabilité — avec ligne norme BCEAO
            dr = dc.sort_values("ROA", ascending=False)
            fc2 = go.Figure()
            fc2.add_trace(go.Bar(name="ROA", x=dr["Sigle"], y=dr["ROA"],
                                 marker_color=[cmap.get(s,"#C39B48") for s in dr["Sigle"]],
                                 marker_line_width=0, opacity=0.9))
            fc2.add_trace(go.Bar(name="Solvabilité", x=dr["Sigle"], y=dr["Solvency"],
                                 marker_color=[cmap.get(s,"#E8C96A") for s in dr["Sigle"]],
                                 marker_line_width=0, opacity=0.65))
            fc2.add_hline(y=0.08, line_dash="dot", line_color="#F48FB1",
                          annotation_text="Norme BCEAO 8%",
                          annotation_font_color="#F48FB1", annotation_font_size=10)
            fc2.update_layout(**CL, xaxis={**_ax}, yaxis={**_ax,"title":"Ratio"})

            # Comp3 : Emplois vs Ressources
            if "EMPLOI" in dc.columns and "RESSOURCES" in dc.columns:
                de = dc.sort_values("EMPLOI", ascending=False)
                fc3 = go.Figure()
                fc3.add_trace(go.Bar(name="Emplois", x=de["Sigle"], y=de["EMPLOI"],
                                     marker_color=[cmap.get(s,"#C39B48") for s in de["Sigle"]],
                                     marker_line_width=0, opacity=0.9))
                fc3.add_trace(go.Bar(name="Ressources", x=de["Sigle"], y=de["RESSOURCES"],
                                     marker_color=[cmap.get(s,"#E8C96A") for s in de["Sigle"]],
                                     marker_line_width=0, opacity=0.65))
                fc3.update_layout(**CL, xaxis={**_ax}, yaxis={**_ax,"title":"FCFA"})
            else:
                fc3 = empty_fig()

            # Comp4 : Score Global vs Bilan — bubble chart
            ds = dc.sort_values("Score", ascending=False)
            bm = safe_max(ds["BILAN"])
            fc4 = go.Figure()
            for _, row in ds.iterrows():
                # Taille de bulle proportionnelle au bilan (min 14, max 50)
                fc4.add_trace(go.Scatter(
                    x=[row["Score"]], y=[row["BILAN"]],
                    mode="markers+text", name=row["Sigle"],
                    text=[row["Sigle"]], textposition="top center",
                    textfont=dict(color="#E8DCC8", size=10),
                    marker=dict(size=max(14, min(50, row["BILAN"]/bm*50)),
                                color=cmap.get(row["Sigle"],"#C39B48"),
                                line=dict(color="#080B12",width=1.5), opacity=0.9)
                ))
            fc4.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#080B12",
                              font=dict(color="#E8DCC8"), showlegend=False, height=420,
                              margin=dict(l=60,r=40,t=50,b=60),
                              xaxis=dict(title="Score /4", range=[0,4.5],
                                         gridcolor="rgba(255,255,255,0.06)",
                                         tickfont=dict(color="#8A8070",size=10),
                                         title_font=dict(color="#C39B48"), automargin=True),
                              yaxis=dict(title="Bilan (FCFA)",
                                         gridcolor="rgba(255,255,255,0.06)",
                                         tickfont=dict(color="#8A8070",size=10),
                                         title_font=dict(color="#C39B48"), automargin=True))

        # ── Retour des 44 valeurs dans l'ordre exact des Output ──
        return (
            fig_bilan, fig_resultat, fig_evolution, fig_ratio,          # 1-4
            fig_ranking, fig_position, fig_score, fig_map,              # 5-8
            fig_market, fig_solvency, fig_emploi, fig_ressources,       # 9-12
            fig_matrix, fig_prediction,                                 # 13-14
            fmt(bilan_total), fmt(resultat_total),                      # 15-16
            fmt(fonds_total), fmt(pnb_total),                           # 17-18
            analysis, bank_analysis,                                    # 19-20
            interpret_bilan(df_year),                                   # 21
            interpret_resultat(df_year),                                # 22
            interpret_evolution(df),                                    # 23
            interpret_ranking(df_year),                                 # 24
            interpret_score(df_year),                                   # 25
            interpret_roa(df_year),                                     # 26
            interpret_solvency(df_year),                                # 27
            interpret_emploi(df_year),                                  # 28
            interpret_ressources(df_year),                              # 29
            interpret_positioning(df_year),                             # 30
            interpret_matrix(df_year),                                  # 31
            interpret_marketshare(df_year),                             # 32
            interpret_map(df_year),                                     # 33
            interpret_prediction(df),                                   # 34
            analysis, bank_analysis,                                    # 35-36
            fc1, fc2, fc3, fc4,                                         # 37-40
            interpret_bilan(df_year),                                   # 41 interp-comp-bilan
            interpret_roa(df_year),                                     # 42 interp-comp-roa
            interpret_emploi(df_year),                                  # 43 interp-comp-emploi
            interpret_score(df_year),                                   # 44 interp-comp-score
        )

    # ─────────────────────────────────────────────────────
    # CALLBACK 4 — Export Excel
    # Télécharge toutes les données en fichier .xlsx
    # ─────────────────────────────────────────────────────
    @app.callback(
        Output("download-excel","data"),
        Input("download-excel-button","n_clicks"),
        prevent_initial_call=True
    )
    def download_excel(n):
        """Exporte toutes les données MongoDB en fichier Excel."""
        return dcc.send_data_frame(get_data().to_excel, "donnees_banques.xlsx", index=False)

    # ─────────────────────────────────────────────────────
    # CALLBACK 5 — Export PDF
    # ⚠️ year et bank utilisent State (pas Input) pour que le callback
    # ne se déclenche QUE sur le clic bouton, pas à chaque changement de filtre.
    # ─────────────────────────────────────────────────────
    @app.callback(
        Output("download-pdf","data"),
        Input("download-report","n_clicks"),
        State("year-filter","value"),
        State("bank-filter","value"),
        prevent_initial_call=True
    )
    def download_pdf(n, year, bank):
        """
        Génère un rapport PDF avec :
        - En-tête titre + filtres appliqués
        - 4 cartes KPI (bilan, résultat, fonds propres, PNB)
        - Tableau détaillé des établissements (bilan, résultat, ROA...)
        - Analyse automatique (banque dominante, plus rentable, source BCEAO)
        """
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        import io

        # Chargement et filtrage
        df = get_data()
        dy = df[df["ANNEE"] == year].copy() if year else df.copy()
        if bank: dy = dy[dy["Sigle"] == bank].copy()

        # Totaux KPI
        bt = dy["BILAN"].sum(); rt = dy["RESULTAT.NET"].sum()
        ft = dy["FONDS.PROPRE"].sum(); pt = dy["PRODUIT.NET.BANCAIRE"].sum()

        buf  = io.BytesIO()
        c    = canvas.Canvas(buf, pagesize=letter)
        W, H = letter

        # Fond sombre
        c.setFillColorRGB(0.031,0.043,0.071); c.rect(0,0,W,H,fill=1,stroke=0)

        # Titre
        c.setFillColorRGB(0.910,0.788,0.408); c.setFont("Helvetica-Bold",20)
        c.drawCentredString(W/2,H-60,"Rapport Bancaire - Sénégal")

        # Sous-titre (filtres)
        c.setFillColorRGB(0.545,0.502,0.439); c.setFont("Helvetica",11)
        p   = f"Année : {int(year)}" if year else "Toutes années"
        bt_ = f"Banque : {bank}" if bank else "Toutes banques"
        c.drawCentredString(W/2,H-82,f"{p}   |   {bt_}")

        # Ligne dorée
        c.setStrokeColorRGB(0.910,0.788,0.408); c.setLineWidth(1)
        c.line(60,H-95,W-60,H-95)

        # Cartes KPI (2×2)
        kpis = [("Bilan Total",fmt(bt)),("Résultat Net",fmt(rt)),
                ("Fonds Propres",fmt(ft)),("PNB",fmt(pt))]
        y0=H-140; cw=(W-120)/2

        for i,(lb,vl) in enumerate(kpis):
            col=i%2; row=i//2; x=60+col*(cw+20); yy=y0-row*70
            c.setFillColorRGB(0.051,0.063,0.094)
            c.roundRect(x,yy-45,cw,55,6,fill=1,stroke=0)
            c.setStrokeColorRGB(0.910,0.788,0.408); c.setLineWidth(0.5)
            c.roundRect(x,yy-45,cw,55,6,fill=0,stroke=1)
            c.setFillColorRGB(0.545,0.502,0.439); c.setFont("Helvetica",8)
            c.drawString(x+12,yy+2,lb.upper())
            c.setFillColorRGB(0.910,0.820,0.408); c.setFont("Helvetica-Bold",13)
            c.drawString(x+12,yy-24,vl)

        # Séparateur
        y2=y0-160; c.setStrokeColorRGB(0.910,0.788,0.408); c.setLineWidth(0.5)
        c.line(60,y2,W-60,y2)

        # Titre tableau
        c.setFillColorRGB(0.910,0.788,0.408); c.setFont("Helvetica-Bold",12)
        c.drawString(60,y2-20,"Détail par Établissement")

        # En-têtes tableau
        hdrs=["Banque","Bilan","Résultat Net","Fonds Propres","ROA"]
        cws=[120,100,100,100,70]; xs=60; yt=y2-45
        c.setFillColorRGB(0.910,0.788,0.408); c.setFont("Helvetica-Bold",9)
        xc=xs
        for h,cw2 in zip(hdrs,cws): c.drawString(xc+4,yt,h); xc+=cw2
        c.setStrokeColorRGB(0.910,0.788,0.408)
        c.line(xs,yt-4,xs+sum(cws),yt-4)

        # Lignes de données (triées par bilan décroissant)
        dy["_ROA"] = safe_div(dy["RESULTAT.NET"], dy["BILAN"])
        ds = dy.sort_values("BILAN",ascending=False)
        c.setFont("Helvetica",8); yr=yt-18

        for idx,(_,row) in enumerate(ds.iterrows()):
            if yr<80: break  # Arrêt si bas de page atteint
            if idx%2==0:     # Fond alterné pour la lisibilité
                c.setFillColorRGB(0.063,0.075,0.106)
                c.rect(xs,yr-4,sum(cws),16,fill=1,stroke=0)
            c.setFillColorRGB(0.910,0.867,0.784)
            vals=[str(row["Sigle"]),fmt(row["BILAN"]),fmt(row["RESULTAT.NET"]),
                  fmt(row["FONDS.PROPRE"]),pct(row["_ROA"]) if not pd.isna(row["_ROA"]) else "N/A"]
            xc=xs
            for v,cw2 in zip(vals,cws): c.drawString(xc+4,yr,v[:18]); xc+=cw2
            yr-=18

        # Analyse automatique
        ya=max(yr-20,120)
        c.setStrokeColorRGB(0.910,0.788,0.408); c.line(60,ya,W-60,ya)
        if not dy.empty:
            tbl=dy.nlargest(1,"BILAN").iloc[0]["Sigle"]
            trl=dy.nlargest(1,"RESULTAT.NET").iloc[0]["Sigle"]
            c.setFillColorRGB(0.910,0.788,0.408); c.setFont("Helvetica-Bold",10)
            c.drawString(60,ya-18,"Analyse automatique")
            c.setFillColorRGB(0.784,0.722,0.541); c.setFont("Helvetica",9)
            for i,lg in enumerate([f"Banque dominante : {tbl}",
                                   f"Plus rentable    : {trl}",
                                   "Source           : BCEAO"]):
                c.drawString(60,ya-36-i*14,lg)

        # Footer
        c.setFillColorRGB(0.231,0.188,0.145); c.setFont("Helvetica",7)
        c.drawCentredString(W/2,30,"Plateforme d'Analyse Sectorielle · Secteur Bancaire Sénégalais · BCEAO")

        c.save(); buf.seek(0)
        return dcc.send_bytes(buf.read(), f"rapport_{year or 'all'}_{bank or 'all'}.pdf")
