import pandas as pd

columns = [
'Sigle','Goupe_Bancaire','ANNEE','EMPLOI','BILAN','RESSOURCES','FONDS.PROPRE',
'EFFECTIF','AGENCE','COMPTE',
'INTERETS.ET.PRODUITS.ASSIMILES','NTERETS.ET.CHARGES.ASSIMILEES',
'GAINS.OU.PERTES.NETS.SUR.OPERATIONS.DES.PORTEFEUILLES.DE.NEGOCIATION',
'GAINS.OU.PERTES.NETS.SUR.OPERATIONS.DES.PORTEFEUILLES.DE.PLACEMENT.ET.ASSIMILES',
"AUTRES.PRODUITS.D'EXPLOITATION.BANCAIRE",
"AUTRES.CHARGES.D'EXPLOITATION.BANCAIRE",
'PRODUIT.NET.BANCAIRE',
"SUBVENTIONS.D'INVESTISSEMENT",
"CHARGES.GENERALES.D'EXPLOITATION",
'DOTATIONS.AUX.AMORTISSEMENTS.ET.AUX.DEPRECIATIONS.DES.IMMOBILISATIONS.INCORPORELLES.ET.CORPORELLES',
"RESULTAT.BRUT.D'EXPLOITATION",
'COÛT.DU.RISQUE',
"RESULTAT.D'EXPLOITATION",
'GAINS.OU.PERTES.NETS.SUR.ACTIFS.IMMOBILISES',
"RESULTAT.AVANT.IMPÔT",
'IMPÔTS.SUR.LES.BENEFICES',
'RESULTAT.NET'
]

data = []

def add_bank(sigle, annee,
             caisse, effets, interbancaire,
             clientele, obligations, actions, autres,
             interets_produits, interets_charges, gains_negociation):

    bilan = caisse + effets + interbancaire + clientele + obligations + actions + autres

    emploi = interbancaire + clientele + obligations + actions

    ressources = bilan * 0.8
    fonds_propres = bilan * 0.2

    data.append({
        "Sigle": sigle,
        "ANNEE": annee,
        "EMPLOI": emploi,
        "BILAN": bilan,
        "RESSOURCES": ressources,
        "FONDS.PROPRE": fonds_propres,
        "INTERETS.ET.PRODUITS.ASSIMILES": interets_produits,
        "NTERETS.ET.CHARGES.ASSIMILEES": interets_charges,
        "GAINS.OU.PERTES.NETS.SUR.OPERATIONS.DES.PORTEFEUILLES.DE.NEGOCIATION": gains_negociation
    })


# -------------------------
# BICIS
# -------------------------

add_bank("BICIS",2022,195035,113782,2406,324279,0,0,10000,25326,4105,2535)
add_bank("BICIS",2021,134817,81324,3454,301622,0,0,8000,24926,4073,2599)

# -------------------------
# CBAO
# -------------------------

add_bank("CBAO",2022,114036,240477,36619,871980,5313,14737,20000,70592,9404,1884)
add_bank("CBAO",2021,85025,208073,34628,754858,5381,21071,18000,65478,10438,1659)

# -------------------------
# CREDIT DU SENEGAL
# -------------------------

add_bank("CDS",2022,4217,85073,10384,178816,0,86,841,16475,3609,345)
add_bank("CDS",2021,4409,74106,3277,155004,0,76,780,14200,2911,242)

# -------------------------
# BHS
# -------------------------

add_bank("BHS",2022,26318,75266,15672,419539,1120,0,2000,34208,11406,-479)
add_bank("BHS",2021,26684,61679,26561,376905,1673,0,1800,29593,12575,283)

# -------------------------
# ECOBANK
# -------------------------

add_bank("ECOBANK",2022,86627,381768,57710,387406,103,12093,20000,40230,23954,5404)
add_bank("ECOBANK",2021,91395,5044,52084,352174,460,11958,18000,43503,17219,5032)

# -------------------------
# ORABANK
# -------------------------

add_bank("ORABANK",2022,73382,211281,56826,464870,0,0,10000,41828,20785,2392)
add_bank("ORABANK",2021,33470,178831,38066,367558,0,0,9000,33042,16387,1891)

# -------------------------
# BOA SENEGAL
# -------------------------

add_bank("BOA",2022,28619,205602,27188,358939,0,6905,10000,39947,14542,0)
add_bank("BOA",2021,50226,172761,33448,321621,1711,6136,9000,36655,13521,8)


df = pd.DataFrame(data)

for col in columns:
    if col not in df.columns:
        df[col] = None

df = df[columns]

df.to_excel("data/extracted_tables/banques_senegal_2021_2022.xlsx", index=False)

print("Dataset créé")