from dash import html, dcc

GOLD       = "#C39B48"
GOLD_LIGHT = "#E8C96A"
DARK_BG    = "#080B12"
CARD_BG    = "#0D1018"
CARD_BG2   = "#111620"
TEXT_MAIN  = "#E8DCC8"
TEXT_MUTED = "#8A8070"
BORDER     = "rgba(195,155,72,0.18)"

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,600;1,400&family=DM+Sans:wght@300;400;500&display=swap');
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html,body,#react-entry-point,#_dash-app-content{background:#080B12!important;margin:0!important;padding:0!important;min-height:100vh;font-family:'DM Sans',sans-serif;color:#E8DCC8}
body::before{content:'';position:fixed;inset:0;background:radial-gradient(ellipse 80% 40% at 50% -5%,rgba(195,155,72,.07) 0%,transparent 65%),radial-gradient(ellipse 40% 30% at 95% 85%,rgba(195,155,72,.04) 0%,transparent 55%);pointer-events:none;z-index:0}
::-webkit-scrollbar{width:4px}::-webkit-scrollbar-track{background:#0D1018}::-webkit-scrollbar-thumb{background:#C39B48;border-radius:2px}
.Select-control{background:#0D1018!important;border:1px solid rgba(195,155,72,.3)!important;border-radius:10px!important;color:#E8DCC8!important;min-height:44px!important}
.Select-value-label{color:#E8DCC8!important}.Select-placeholder{color:#8A8070!important}
.Select-menu-outer{background:#0D1018!important;border:1px solid rgba(195,155,72,.3)!important;border-radius:10px!important;z-index:9999!important}
.VirtualizedSelectOption{color:#E8DCC8!important;background:#0D1018!important}.VirtualizedSelectFocusedOption{background:rgba(195,155,72,.12)!important}
.Select-arrow{border-color:#C39B48 transparent transparent!important}
.js-plotly-plot .plotly .modebar{background:transparent!important}
.js-plotly-plot .plotly .modebar-btn path{fill:rgba(195,155,72,.5)!important}
.js-plotly-plot .plotly .modebar-btn:hover path{fill:#C39B48!important}

/* ── Tabs ── */
.dash-tabs-content{background:transparent!important;border:none!important;padding:0!important}

/* Conteneur sticky des onglets */
#main-tabs{
    position:sticky!important;
    top:0!important;
    z-index:200!important;
    background:#080B12!important;
    border-bottom:1px solid rgba(195,155,72,0.25)!important;
    padding:14px 34px!important;
    display:flex!important;
    flex-wrap:wrap!important;
    gap:8px!important;
    box-shadow:0 4px 24px rgba(0,0,0,0.6)!important;
}

/* Chaque onglet */
#main-tabs .dash-tab{
    background: rgba(13,16,24,0.8) !important;
    border: 1px solid rgba(195,155,72,0.2) !important;
    border-radius: 50px !important;
    color: #8A8070 !important;
    padding: 9px 20px !important;
    font-size: 0.78rem !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 400 !important;
    letter-spacing: 0.06em !important;
    cursor: pointer !important;
    transition: all 0.22s ease !important;
    white-space: nowrap !important;
    margin: 0 !important;
}

#main-tabs .dash-tab:hover{
    border-color: rgba(195,155,72,0.55) !important;
    color: #C39B48 !important;
    background: rgba(195,155,72,0.08) !important;
    transform: translateY(-1px) !important;
}

/* Onglet actif */
#main-tabs .dash-tab--selected{
    background: linear-gradient(135deg, #C39B48 0%, #E8C96A 100%) !important;
    border-color: transparent !important;
    color: #080B12 !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 20px rgba(195,155,72,0.4), 0 0 0 1px rgba(232,201,106,0.3) !important;
    transform: translateY(-1px) !important;
}

/* ── Sections ── */
.tab-section{display:none}
.tab-section.visible{display:block;animation:sectionIn .4s ease forwards}
@keyframes sectionIn{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:translateY(0)}}

/* ── Cards ── */
@keyframes cardIn{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}
.chart-card{animation:cardIn .45s ease both}

/* ── KPI ── */
@keyframes goldPulse{0%,100%{box-shadow:0 0 0 0 rgba(195,155,72,0)}50%{box-shadow:0 0 20px 3px rgba(195,155,72,.12)}}
.kpi-card{animation:goldPulse 3s ease-in-out infinite}

/* ── Tableaux comparatifs ── */
.comp-table{width:100%;border-collapse:collapse}
.comp-table th{background:rgba(195,155,72,.08);color:#C39B48;font-size:.73rem;letter-spacing:.08em;text-transform:uppercase;padding:11px 14px;text-align:left;border-bottom:1px solid rgba(195,155,72,.2);font-weight:500}
.comp-table td{padding:10px 14px;font-size:.82rem;color:#E8DCC8;border-bottom:1px solid rgba(195,155,72,.05)}
.comp-table tr:hover td{background:rgba(195,155,72,.04)}
.bar-mini{display:inline-block;height:5px;border-radius:3px;background:linear-gradient(90deg,#C39B48,#E8C96A);margin-right:8px;vertical-align:middle}
.badge-good{background:rgba(129,199,132,.15);color:#81C784;padding:2px 8px;border-radius:50px;font-size:.70rem}
.badge-warn{background:rgba(255,171,118,.15);color:#FFAB76;padding:2px 8px;border-radius:50px;font-size:.70rem}
.badge-bad{background:rgba(240,98,146,.15);color:#F06292;padding:2px 8px;border-radius:50px;font-size:.70rem}
.medal-1{color:#E8C96A;font-weight:600}.medal-2{color:#C39B48;font-weight:500}.medal-3{color:#A07830}
button{cursor:pointer;font-family:'DM Sans',sans-serif}
/* Fallback pour toutes versions Dash */
.dash-tab-strip{background:#080B12!important;border-bottom:1px solid rgba(195,155,72,0.25)!important;padding:14px 34px!important;position:sticky!important;top:0!important;z-index:200!important}
.rc-tabs-tab{background:rgba(13,16,24,0.8)!important;border:1px solid rgba(195,155,72,0.2)!important;border-radius:50px!important;color:#8A8070!important;padding:9px 20px!important;margin:0 4px!important;font-size:0.78rem!important;cursor:pointer!important;transition:all 0.22s!important}
.rc-tabs-tab-active,.rc-tabs-tab:hover{color:#C39B48!important;border-color:rgba(195,155,72,0.5)!important}
.rc-tabs-tab-active{background:linear-gradient(135deg,#C39B48,#E8C96A)!important;color:#080B12!important;font-weight:600!important;box-shadow:0 4px 20px rgba(195,155,72,0.4)!important}
.rc-tabs-ink-bar{background:#C39B48!important;height:2px!important}
.rc-tabs-content{background:transparent!important;border:none!important}
"""

# ── Composants ─────────────────────────────────────────────

def gold_sep():
    return html.Div(style={"height":"1px","background":"linear-gradient(90deg,transparent,rgba(195,155,72,.5),transparent)","margin":"8px 0 28px"})

def section_title(text, sub=None):
    kids = [html.Div(style={"display":"flex","alignItems":"center","gap":"12px","marginBottom":"4px"},children=[
        html.Div(style={"width":"3px","height":"26px","background":"linear-gradient(180deg,#E8C96A,#C39B48)","borderRadius":"2px","flexShrink":"0"}),
        html.H2(text,style={"fontFamily":"'Cormorant Garamond',serif","fontSize":"1.45rem","fontWeight":"600","color":TEXT_MAIN,"letterSpacing":"0.03em"})
    ])]
    if sub:
        kids.append(html.P(sub,style={"color":TEXT_MUTED,"fontSize":"0.80rem","paddingLeft":"15px","marginBottom":"18px"}))
    return html.Div(kids,style={"marginBottom":"20px"})

def interp_box(interp_id):
    return html.Div(style={"marginTop":"14px","background":"rgba(195,155,72,.04)","borderLeft":"3px solid #C39B48","border":"1px solid rgba(195,155,72,.15)","borderRadius":"0 8px 8px 0","padding":"12px 16px"},
        children=[html.Div(id=interp_id,style={"color":"#C8B88A","fontSize":"0.82rem","lineHeight":"1.65"})])

def corner():
    return html.Div(style={"position":"absolute","top":0,"left":0,"width":"50px","height":"50px","borderTop":"1px solid rgba(195,155,72,.4)","borderLeft":"1px solid rgba(195,155,72,.4)","borderRadius":"16px 0 0 0","pointerEvents":"none"})

def chart_card(graph_id, interp_id, title, sub=None):
    kids=[corner(),html.H3(title,style={"fontFamily":"'Cormorant Garamond',serif","fontSize":"1.10rem","fontWeight":"600","color":GOLD,"marginBottom":"2px","letterSpacing":"0.03em"})]
    if sub: kids.append(html.P(sub,style={"color":TEXT_MUTED,"fontSize":"0.76rem","marginBottom":"12px"}))
    kids.append(dcc.Graph(id=graph_id,config={"scrollZoom":True,"displayModeBar":True,"modeBarButtonsToRemove":["lasso2d","select2d","autoScale2d","toggleSpikelines"],"displaylogo":False}))
    kids.append(interp_box(interp_id))
    return html.Div(className="chart-card",style={"background":f"linear-gradient(145deg,{CARD_BG},{CARD_BG2})","border":f"1px solid {BORDER}","borderRadius":"16px","padding":"24px","marginBottom":"24px","position":"relative","overflow":"hidden"},children=kids)

def kpi_card(kpi_id, label):
    return html.Div(className="kpi-card",style={"background":f"linear-gradient(135deg,{CARD_BG},{CARD_BG2})","border":f"1px solid {BORDER}","borderRadius":"14px","padding":"22px 24px","flex":"1","minWidth":"140px","position":"relative","overflow":"hidden"},children=[
        html.Div(style={"position":"absolute","top":"-20px","right":"-20px","width":"80px","height":"80px","background":"radial-gradient(circle,rgba(195,155,72,.07) 0%,transparent 70%)","borderRadius":"50%"}),
        html.P(label,style={"color":TEXT_MUTED,"fontSize":"0.70rem","textTransform":"uppercase","letterSpacing":"0.10em","marginBottom":"8px"}),
        html.H2(id=kpi_id,style={"fontFamily":"'Cormorant Garamond',serif","fontSize":"1.65rem","fontWeight":"600","color":GOLD_LIGHT})
    ])

def card_wrap(title, sub, content_id):
    return html.Div(style={"background":f"linear-gradient(145deg,{CARD_BG},{CARD_BG2})","border":f"1px solid {BORDER}","borderRadius":"16px","padding":"26px","marginBottom":"24px","position":"relative","overflow":"hidden"},children=[
        corner(),
        html.H3(title,style={"fontFamily":"'Cormorant Garamond',serif","color":GOLD,"fontSize":"1.10rem","fontWeight":"600","marginBottom":"4px"}),
        html.P(sub,style={"color":TEXT_MUTED,"fontSize":"0.76rem","marginBottom":"18px"}),
        html.Div(id=content_id)
    ])

def text_card(title, content_id):
    return html.Div(style={"background":f"linear-gradient(145deg,{CARD_BG},{CARD_BG2})","border":f"1px solid {BORDER}","borderRadius":"14px","padding":"24px"},children=[
        html.H3(title,style={"fontFamily":"'Cormorant Garamond',serif","color":GOLD,"fontSize":"1.05rem","marginBottom":"12px","fontWeight":"600"}),
        html.Div(id=content_id,style={"color":"#C8B88A","fontSize":"0.82rem","lineHeight":"1.75","whiteSpace":"pre-line"})
    ])

def section(sid, children, visible=False):
    return html.Div(
        id=sid,
        style={"display": "block", "animation": "sectionIn .4s ease forwards"} if visible else {"display": "none"},
        children=children
    )

def pad(children):
    return html.Div(style={"maxWidth":"1360px","margin":"0 auto","padding":"36px 34px 50px"},children=children)

# ── Layout ─────────────────────────────────────────────────

def create_layout():
    return html.Div(style={"background":DARK_BG,"minHeight":"100vh","position":"relative"},children=[

        html.Script(f"(function(){{var s=document.createElement('style');s.textContent=`{CSS}`;document.head.appendChild(s);}})()" ),

        # HEADER
        html.Div(style={"background":"linear-gradient(180deg,rgba(195,155,72,.07) 0%,transparent 100%)","borderBottom":"1px solid rgba(195,155,72,.12)","padding":"36px 56px 28px","textAlign":"center"},children=[
            html.Div("Plateforme d'Analyse · Secteur Bancaire · Sénégal",style={"display":"inline-block","background":"rgba(195,155,72,.08)","border":"1px solid rgba(195,155,72,.25)","borderRadius":"50px","padding":"4px 18px","fontSize":"0.68rem","letterSpacing":"0.13em","textTransform":"uppercase","color":GOLD,"marginBottom":"16px"}),
            html.H1("Positionnement des Banques au Sénégal",style={"fontFamily":"'Cormorant Garamond',serif","fontSize":"clamp(1.7rem,3.5vw,2.8rem)","fontWeight":"300","color":TEXT_MAIN,"letterSpacing":"0.04em","lineHeight":"1.2","marginBottom":"12px"}),
            html.P(["Données issues des rapports financiers publiés par la ",html.Strong("BCEAO",style={"color":GOLD})," · Analyse interactive des performances et du positionnement concurrentiel"],style={"color":TEXT_MUTED,"fontSize":"0.86rem","maxWidth":"580px","margin":"0 auto","lineHeight":"1.6"}),
            html.Div(style={"height":"1px","marginTop":"28px","background":"linear-gradient(90deg,transparent,rgba(195,155,72,.35),transparent)"})
        ]),

        # FILTRES
        html.Div(style={"background":f"linear-gradient(135deg,{CARD_BG},{CARD_BG2})","borderBottom":f"1px solid {BORDER}","padding":"16px 34px","display":"flex","gap":"20px","flexWrap":"wrap","alignItems":"flex-end"},children=[
            html.Div([html.Label("Banque",style={"color":TEXT_MUTED,"fontSize":"0.68rem","textTransform":"uppercase","letterSpacing":"0.10em","display":"block","marginBottom":"6px"}),dcc.Dropdown(id="bank-filter",placeholder="Toutes les banques",style={"width":"260px"})]),
            html.Div([html.Label("Année",style={"color":TEXT_MUTED,"fontSize":"0.68rem","textTransform":"uppercase","letterSpacing":"0.10em","display":"block","marginBottom":"6px"}),dcc.Dropdown(id="year-filter",placeholder="Toutes les années",style={"width":"180px"})]),
            html.Div(style={"marginLeft":"auto","display":"flex","gap":"10px","alignItems":"center"},children=[
                html.Button("Télécharger Excel",id="download-excel-button",n_clicks=0,style={"background":"transparent","border":"1px solid rgba(195,155,72,.35)","color":GOLD,"borderRadius":"8px","padding":"9px 18px","fontSize":"0.78rem"}),
                html.Button("Rapport PDF",id="download-report",n_clicks=0,style={"background":"linear-gradient(135deg,#C39B48,#E8C96A)","border":"none","color":DARK_BG,"borderRadius":"8px","padding":"9px 20px","fontSize":"0.78rem","fontWeight":"500"})
            ])
        ]),
        dcc.Download(id="download-pdf"),
        dcc.Download(id="download-excel"),

        # ONGLETS
        dcc.Tabs(id="main-tabs", value="tab-kpi",
            className="dash-tabs",
            style={
                "position": "sticky",
                "top": "0",
                "zIndex": "200",
                "background": "#080B12",
                "borderBottom": "1px solid rgba(195,155,72,0.25)",
                "padding": "14px 34px",
                "display": "flex",
                "flexWrap": "wrap",
                "gap": "8px",
                "boxShadow": "0 4px 24px rgba(0,0,0,0.6)"
            },
            children=[
            dcc.Tab(label="KPI", value="tab-kpi",
                className="dash-tab", selected_className="dash-tab--selected",
                style={"background":"rgba(13,16,24,0.85)","border":"1px solid rgba(195,155,72,0.2)","borderRadius":"50px","color":"#8A8070","padding":"9px 20px","fontSize":"0.78rem","fontFamily":"'DM Sans', sans-serif","letterSpacing":"0.06em","cursor":"pointer","margin":"0","whiteSpace":"nowrap"},
                selected_style={"background":"linear-gradient(135deg, #C39B48, #E8C96A)","border":"none","borderRadius":"50px","color":"#080B12","padding":"9px 20px","fontSize":"0.78rem","fontFamily":"'DM Sans', sans-serif","fontWeight":"600","letterSpacing":"0.06em","cursor":"pointer","margin":"0","whiteSpace":"nowrap","boxShadow":"0 4px 20px rgba(195,155,72,0.4)"}),
            dcc.Tab(label="Bilan & Résultat", value="tab-bilan",
                className="dash-tab", selected_className="dash-tab--selected",
                style={"background":"rgba(13,16,24,0.85)","border":"1px solid rgba(195,155,72,0.2)","borderRadius":"50px","color":"#8A8070","padding":"9px 20px","fontSize":"0.78rem","fontFamily":"'DM Sans', sans-serif","letterSpacing":"0.06em","cursor":"pointer","margin":"0","whiteSpace":"nowrap"},
                selected_style={"background":"linear-gradient(135deg, #C39B48, #E8C96A)","border":"none","borderRadius":"50px","color":"#080B12","padding":"9px 20px","fontSize":"0.78rem","fontFamily":"'DM Sans', sans-serif","fontWeight":"600","letterSpacing":"0.06em","cursor":"pointer","margin":"0","whiteSpace":"nowrap","boxShadow":"0 4px 20px rgba(195,155,72,0.4)"}),
            dcc.Tab(label="Évolution", value="tab-evolution",
                className="dash-tab", selected_className="dash-tab--selected",
                style={"background":"rgba(13,16,24,0.85)","border":"1px solid rgba(195,155,72,0.2)","borderRadius":"50px","color":"#8A8070","padding":"9px 20px","fontSize":"0.78rem","fontFamily":"'DM Sans', sans-serif","letterSpacing":"0.06em","cursor":"pointer","margin":"0","whiteSpace":"nowrap"},
                selected_style={"background":"linear-gradient(135deg, #C39B48, #E8C96A)","border":"none","borderRadius":"50px","color":"#080B12","padding":"9px 20px","fontSize":"0.78rem","fontFamily":"'DM Sans', sans-serif","fontWeight":"600","letterSpacing":"0.06em","cursor":"pointer","margin":"0","whiteSpace":"nowrap","boxShadow":"0 4px 20px rgba(195,155,72,0.4)"}),
            dcc.Tab(label="Classement", value="tab-classement",
                className="dash-tab", selected_className="dash-tab--selected",
                style={"background":"rgba(13,16,24,0.85)","border":"1px solid rgba(195,155,72,0.2)","borderRadius":"50px","color":"#8A8070","padding":"9px 20px","fontSize":"0.78rem","fontFamily":"'DM Sans', sans-serif","letterSpacing":"0.06em","cursor":"pointer","margin":"0","whiteSpace":"nowrap"},
                selected_style={"background":"linear-gradient(135deg, #C39B48, #E8C96A)","border":"none","borderRadius":"50px","color":"#080B12","padding":"9px 20px","fontSize":"0.78rem","fontFamily":"'DM Sans', sans-serif","fontWeight":"600","letterSpacing":"0.06em","cursor":"pointer","margin":"0","whiteSpace":"nowrap","boxShadow":"0 4px 20px rgba(195,155,72,0.4)"}),
            dcc.Tab(label="Ratios", value="tab-ratios",
                className="dash-tab", selected_className="dash-tab--selected",
                style={"background":"rgba(13,16,24,0.85)","border":"1px solid rgba(195,155,72,0.2)","borderRadius":"50px","color":"#8A8070","padding":"9px 20px","fontSize":"0.78rem","fontFamily":"'DM Sans', sans-serif","letterSpacing":"0.06em","cursor":"pointer","margin":"0","whiteSpace":"nowrap"},
                selected_style={"background":"linear-gradient(135deg, #C39B48, #E8C96A)","border":"none","borderRadius":"50px","color":"#080B12","padding":"9px 20px","fontSize":"0.78rem","fontFamily":"'DM Sans', sans-serif","fontWeight":"600","letterSpacing":"0.06em","cursor":"pointer","margin":"0","whiteSpace":"nowrap","boxShadow":"0 4px 20px rgba(195,155,72,0.4)"}),
            dcc.Tab(label="Positionnement", value="tab-positionnement",
                className="dash-tab", selected_className="dash-tab--selected",
                style={"background":"rgba(13,16,24,0.85)","border":"1px solid rgba(195,155,72,0.2)","borderRadius":"50px","color":"#8A8070","padding":"9px 20px","fontSize":"0.78rem","fontFamily":"'DM Sans', sans-serif","letterSpacing":"0.06em","cursor":"pointer","margin":"0","whiteSpace":"nowrap"},
                selected_style={"background":"linear-gradient(135deg, #C39B48, #E8C96A)","border":"none","borderRadius":"50px","color":"#080B12","padding":"9px 20px","fontSize":"0.78rem","fontFamily":"'DM Sans', sans-serif","fontWeight":"600","letterSpacing":"0.06em","cursor":"pointer","margin":"0","whiteSpace":"nowrap","boxShadow":"0 4px 20px rgba(195,155,72,0.4)"}),
            dcc.Tab(label="Parts de Marché", value="tab-marche",
                className="dash-tab", selected_className="dash-tab--selected",
                style={"background":"rgba(13,16,24,0.85)","border":"1px solid rgba(195,155,72,0.2)","borderRadius":"50px","color":"#8A8070","padding":"9px 20px","fontSize":"0.78rem","fontFamily":"'DM Sans', sans-serif","letterSpacing":"0.06em","cursor":"pointer","margin":"0","whiteSpace":"nowrap"},
                selected_style={"background":"linear-gradient(135deg, #C39B48, #E8C96A)","border":"none","borderRadius":"50px","color":"#080B12","padding":"9px 20px","fontSize":"0.78rem","fontFamily":"'DM Sans', sans-serif","fontWeight":"600","letterSpacing":"0.06em","cursor":"pointer","margin":"0","whiteSpace":"nowrap","boxShadow":"0 4px 20px rgba(195,155,72,0.4)"}),
            dcc.Tab(label="Comparaison", value="tab-comparaison",
                className="dash-tab", selected_className="dash-tab--selected",
                style={"background":"rgba(13,16,24,0.85)","border":"1px solid rgba(195,155,72,0.2)","borderRadius":"50px","color":"#8A8070","padding":"9px 20px","fontSize":"0.78rem","fontFamily":"'DM Sans', sans-serif","letterSpacing":"0.06em","cursor":"pointer","margin":"0","whiteSpace":"nowrap"},
                selected_style={"background":"linear-gradient(135deg, #C39B48, #E8C96A)","border":"none","borderRadius":"50px","color":"#080B12","padding":"9px 20px","fontSize":"0.78rem","fontFamily":"'DM Sans', sans-serif","fontWeight":"600","letterSpacing":"0.06em","cursor":"pointer","margin":"0","whiteSpace":"nowrap","boxShadow":"0 4px 20px rgba(195,155,72,0.4)"}),
            dcc.Tab(label="Carte", value="tab-carte",
                className="dash-tab", selected_className="dash-tab--selected",
                style={"background":"rgba(13,16,24,0.85)","border":"1px solid rgba(195,155,72,0.2)","borderRadius":"50px","color":"#8A8070","padding":"9px 20px","fontSize":"0.78rem","fontFamily":"'DM Sans', sans-serif","letterSpacing":"0.06em","cursor":"pointer","margin":"0","whiteSpace":"nowrap"},
                selected_style={"background":"linear-gradient(135deg, #C39B48, #E8C96A)","border":"none","borderRadius":"50px","color":"#080B12","padding":"9px 20px","fontSize":"0.78rem","fontFamily":"'DM Sans', sans-serif","fontWeight":"600","letterSpacing":"0.06em","cursor":"pointer","margin":"0","whiteSpace":"nowrap","boxShadow":"0 4px 20px rgba(195,155,72,0.4)"}),
            dcc.Tab(label="Prévision", value="tab-prevision",
                className="dash-tab", selected_className="dash-tab--selected",
                style={"background":"rgba(13,16,24,0.85)","border":"1px solid rgba(195,155,72,0.2)","borderRadius":"50px","color":"#8A8070","padding":"9px 20px","fontSize":"0.78rem","fontFamily":"'DM Sans', sans-serif","letterSpacing":"0.06em","cursor":"pointer","margin":"0","whiteSpace":"nowrap"},
                selected_style={"background":"linear-gradient(135deg, #C39B48, #E8C96A)","border":"none","borderRadius":"50px","color":"#080B12","padding":"9px 20px","fontSize":"0.78rem","fontFamily":"'DM Sans', sans-serif","fontWeight":"600","letterSpacing":"0.06em","cursor":"pointer","margin":"0","whiteSpace":"nowrap","boxShadow":"0 4px 20px rgba(195,155,72,0.4)"}),
            dcc.Tab(label="Synthèse", value="tab-synthese",
                className="dash-tab", selected_className="dash-tab--selected",
                style={"background":"rgba(13,16,24,0.85)","border":"1px solid rgba(195,155,72,0.2)","borderRadius":"50px","color":"#8A8070","padding":"9px 20px","fontSize":"0.78rem","fontFamily":"'DM Sans', sans-serif","letterSpacing":"0.06em","cursor":"pointer","margin":"0","whiteSpace":"nowrap"},
                selected_style={"background":"linear-gradient(135deg, #C39B48, #E8C96A)","border":"none","borderRadius":"50px","color":"#080B12","padding":"9px 20px","fontSize":"0.78rem","fontFamily":"'DM Sans', sans-serif","fontWeight":"600","letterSpacing":"0.06em","cursor":"pointer","margin":"0","whiteSpace":"nowrap","boxShadow":"0 4px 20px rgba(195,155,72,0.4)"}),
        ]),

        # TOUTES LES SECTIONS — toujours dans le DOM, display:none par défaut
        html.Div(id="all-sections", children=[

            # ── KPI ──────────────────────────────────
            section("tab-kpi", pad([
                section_title("Indicateurs Clés de Performance","Vue synthétique des grandeurs financières du secteur"),
                html.Div(style={"display":"flex","gap":"16px","flexWrap":"wrap","marginBottom":"32px"},children=[
                    kpi_card("kpi-bilan","Bilan Total"),kpi_card("kpi-resultat","Résultat Net"),
                    kpi_card("kpi-fonds","Fonds Propres"),kpi_card("kpi-pnb","Produit Net Bancaire"),
                ]),
                html.Div(style={"display":"grid","gridTemplateColumns":"1fr 1fr","gap":"20px"},children=[
                    text_card("Analyse du Secteur","analysis-text"),
                    text_card("Analyse de la Banque Sélectionnée","bank-analysis"),
                ])
            ])),

            # ── BILAN & RÉSULTAT ─────────────────────
            section("tab-bilan", pad([
                section_title("Bilan & Résultat Net","Taille financière et rentabilité de chaque établissement"),
                html.Div(style={"display":"grid","gridTemplateColumns":"1fr 1fr","gap":"20px"},children=[
                    chart_card("bilan-chart",    "interp-bilan",    "Bilan des Banques","Total actif — reflet de la taille financière"),
                    chart_card("resultat-chart", "interp-resultat", "Résultat Net","Bénéfice ou perte enregistré sur la période"),
                ]),
            ])),

            # ── ÉVOLUTION ────────────────────────────
            section("tab-evolution", pad([
                section_title("Évolution Temporelle","Trajectoire de croissance du bilan sur plusieurs exercices"),
                chart_card("evolution-chart","interp-evolution","Évolution du Bilan dans le Temps","Une courbe ascendante = banque en croissance"),
            ])),

            # ── CLASSEMENT ───────────────────────────
            section("tab-classement", pad([
                section_title("Classement & Score Global","Les véritables leaders du secteur bancaire sénégalais"),
                html.Div(style={"display":"grid","gridTemplateColumns":"1fr 1fr","gap":"20px"},children=[
                    chart_card("ranking-chart","interp-ranking","Classement par Résultat Net","Du plus rentable au moins rentable"),
                    chart_card("score-chart",  "interp-score",  "Score Global de Performance","Indice composite : bilan + résultat + fonds propres + ROA"),
                ]),
            ])),

            # ── RATIOS ───────────────────────────────
            section("tab-ratios", pad([
                section_title("Ratios Financiers","Rentabilité, solvabilité et utilisation des ressources"),
                html.Div(style={"display":"grid","gridTemplateColumns":"1fr 1fr","gap":"20px"},children=[
                    chart_card("ratio-chart",     "interp-roa",       "Rentabilité des Actifs (ROA)","Résultat net / total bilan"),
                    chart_card("solvency-chart",  "interp-solvency",  "Ratio de Solvabilité","Fonds propres / bilan — norme BCEAO 8%"),
                ]),
                html.Div(style={"display":"grid","gridTemplateColumns":"1fr 1fr","gap":"20px"},children=[
                    chart_card("emploi-chart",    "interp-emploi",    "Emplois des Banques","Crédits, placements et investissements"),
                    chart_card("ressources-chart","interp-ressources","Ressources des Banques","Dépôts, emprunts et financements"),
                ]),
            ])),

            # ── POSITIONNEMENT ───────────────────────
            section("tab-positionnement", pad([
                section_title("Positionnement Stratégique","Cartographie concurrentielle — taille vs rentabilité"),
                chart_card("positioning-chart","interp-positioning","Positionnement Stratégique","Taille de la bulle = importance du bilan"),
                chart_card("matrix-chart",     "interp-matrix",     "Matrice Stratégique","Leaders / challengers / suiveurs"),
            ])),

            # ── PARTS DE MARCHÉ ──────────────────────
            section("tab-marche", pad([
                section_title("Parts de Marché","Concentration et répartition du secteur bancaire"),
                chart_card("marketshare-chart","interp-marketshare","Part de Marché par Bilan","Chaque tranche = part d'une banque dans le total"),
            ])),

            # ── COMPARAISON ──────────────────────────
            # IDs prefixés "interp-comp-*" pour éviter tout doublon avec les autres sections
            section("tab-comparaison", pad([
                section_title("Tableau de Bord Comparatif","Toutes les métriques côte à côte — identifiez les leaders sur chaque dimension"),
                html.Div(style={"display":"grid","gridTemplateColumns":"1fr 1fr","gap":"20px"},children=[
                    chart_card("comp-chart-bilan-resultat",    "interp-comp-bilan",   "Bilan vs Résultat Net","Taille financière et rentabilité — double axe"),
                    chart_card("comp-chart-roa-solvency",      "interp-comp-roa",     "ROA vs Solvabilité","Efficacité et résistance aux chocs — norme BCEAO 8%"),
                ]),
                html.Div(style={"display":"grid","gridTemplateColumns":"1fr 1fr","gap":"20px"},children=[
                    chart_card("comp-chart-emploi-ressources", "interp-comp-emploi",  "Emplois vs Ressources","Capacité de financement et base de collecte"),
                    chart_card("comp-chart-score-bilan",       "interp-comp-score",   "Score Global vs Bilan","Performance multidimensionnelle — score sur 4"),
                ]),
            ])),

            # ── CARTE ────────────────────────────────
            section("tab-carte", pad([
                section_title("Géographie Bancaire","Sièges sociaux sur la carte réelle du Sénégal"),
                chart_card("map-chart","interp-map","Carte des Banques au Sénégal","Bulles proportionnelles au bilan — sièges sociaux réels"),
            ])),

            # ── PRÉVISION ────────────────────────────
            section("tab-prevision", pad([
                section_title("Prévision & Tendances","Projection de l'évolution future par régression linéaire"),
                html.Div(style={"background":"rgba(195,155,72,.04)","border":f"1px solid {BORDER}","borderRadius":"10px","padding":"10px 16px","marginBottom":"16px"},children=[
                    html.P("Modèle de régression linéaire — estimation indicative supposant la stabilité des conditions économiques.",style={"color":TEXT_MUTED,"fontSize":"0.78rem","lineHeight":"1.55"})
                ]),
                chart_card("prediction-chart","interp-prediction","Prévision du Bilan Sectoriel (3 ans)","Ligne pleine = historique · Pointillé = projection"),
            ])),

            # ── SYNTHÈSE ─────────────────────────────
            section("tab-synthese", pad([
                section_title("Synthèse Narrative","Lecture automatique et pédagogique de tous les indicateurs"),
                html.Div(style={"display":"grid","gridTemplateColumns":"1fr 1fr","gap":"20px"},children=[
                    text_card("Analyse du Secteur","analysis-text-2"),
                    text_card("Analyse de la Banque Sélectionnée","bank-analysis-2"),
                ])
            ])),

        ]),

        # FOOTER
        html.Div(style={"textAlign":"center","borderTop":"1px solid rgba(195,155,72,.08)","padding":"26px 0 40px","color":"#3A3025","fontSize":"0.72rem","letterSpacing":"0.07em"},children=[
            html.P("Plateforme d'Analyse Sectorielle · Secteur Bancaire Sénégalais · Données BCEAO"),
            html.P("Visualisation interactive",style={"marginTop":"3px"})
        ])
    ])