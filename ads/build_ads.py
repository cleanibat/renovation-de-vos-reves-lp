# -*- coding: utf-8 -*-
"""Génère les fichiers d'import Google Ads Editor de la campagne Search « La Rénovation de vos rêves ».
Usage : python3 ads/build_ads.py  →  ads/1-campagne-google-ads-editor.csv et ads/2-composants-google-ads-editor.csv
Format : tabulations, UTF-16 (format natif de Google Ads Editor). Import : Compte > Importer > À partir d'un fichier.
"""
import csv, io, json, math, os, sys

SITE = "https://www.larenovationdevosreves.com/"
CAMPAIGN = "Search - Rénovation de vos rêves - Loire-Atlantique"
BUDGET_MENSUEL = 500
BUDGET_JOUR = math.floor(BUDGET_MENSUEL / 30.4 * 100) / 100   # Google plafonne le mois à 30,4 × budget quotidien : 16,44 € → 499,78 €
STATUS = "Enabled"                                     # « Paused » pour importer sans diffuser
# Rayons qui se chevauchent, calculés par ads/zone_rayons.py sur les 152 communes du secteur (geo.api.gouv.fr) :
# chaque commune du secteur est couverte avec 2,5 km de marge, la population hors secteur touchée est minimisée.
GEO = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "rayons.json")))   # [[lat, lon, rayon_km], ...]

GROUPS = [
  dict(name="Maçonnerie", url=SITE, path=("maconnerie", "devis-gratuit"),
    phrase=["entreprise de maçonnerie", "artisan maçon", "maçonnerie générale", "maçon loire atlantique", "maçon nantes",
            "maçon saint nazaire", "maçon pornic", "maçon la baule", "maçon guérande", "entreprise maçonnerie nantes",
            "ouverture mur porteur", "création ouverture mur porteur", "dalle béton", "mur de clôture", "rejointoiement mur pierre"],
    exact=["maçon nantes", "entreprise de maçonnerie", "maçon loire atlantique", "ouverture mur porteur"],
    headlines=["Maçon en Loire-Atlantique", "Entreprise de maçonnerie", "Maçonnerie générale", "Devis gratuit et détaillé",
               "Visite et devis gratuits", "Ouverture de mur porteur", "Murs, dalles et fondations", "Extension et surélévation",
               "Maçon à Nantes et Pornic", "Maçon Saint-Nazaire, La Baule", "Reprise de maçonnerie", "Un seul interlocuteur",
               "8 ans d'expérience", "Joignables 7 j/7", "Particuliers et pros"],
    descriptions=["Murs, dalles, ouvertures, extensions : nous réalisons vos travaux de maçonnerie.",
                  "Visite sur place et devis écrit détaillé, gratuit et sans engagement. Appelez-nous.",
                  "Intervention en Loire-Atlantique, sur le littoral, la presqu'île et le nord Vendée.",
                  "Entreprise du bâtiment à Sainte-Pazanne depuis 8 ans. Chantier suivi et rendu propre."]),
  dict(name="Extension et surélévation", url=SITE + "extension.html", path=("extension", "surelevation"),
    phrase=["extension maison", "agrandissement maison", "surélévation maison", "extension maison nantes",
            "entreprise extension maison", "extension maison loire atlantique", "agrandir sa maison", "surélévation toiture",
            "construction garage", "extension garage", "extension maison prix", "agrandissement maison nantes",
            "extension maison saint nazaire", "extension maison pornic"],
    exact=["extension maison", "agrandissement maison", "surélévation maison", "extension maison nantes"],
    headlines=["Extension de maison", "Agrandissement de maison", "Surélévation de maison", "Extension en Loire-Atlantique",
               "Garage et annexe", "Extension clé en main", "Du gros œuvre aux finitions", "Devis gratuit et détaillé",
               "Visite et devis gratuits", "Extension à Nantes et Pornic", "Gagnez des mètres carrés", "Un seul interlocuteur",
               "8 ans d'expérience", "Joignables 7 j/7", "Extension de plain-pied"],
    descriptions=["Extension de plain-pied, surélévation, garage : nous construisons votre agrandissement.",
                  "Du terrassement aux finitions, l'extension est raccordée à la maison et livrée terminée.",
                  "Visite sur place et devis écrit détaillé, gratuit et sans engagement. Appelez-nous.",
                  "Intervention en Loire-Atlantique, sur le littoral, la presqu'île et le nord Vendée."]),
  dict(name="Terrassement", url=SITE + "terrassement.html", path=("terrassement", "devis-gratuit"),
    phrase=["terrassement", "entreprise de terrassement", "terrassement nantes", "terrassement loire atlantique",
            "terrassement maison", "terrassement piscine", "terrassier", "assainissement individuel", "installation fosse septique",
            "raccordement tout à l'égout", "viabilisation terrain", "terrassement saint nazaire", "terrassement pornic"],
    exact=["entreprise de terrassement", "terrassement nantes", "terrassement loire atlantique", "terrassement maison"],
    headlines=["Terrassement Loire-Atlantique", "Entreprise de terrassement", "Terrassement de maison", "Terrassement de piscine",
               "Assainissement individuel", "Raccordement tout-à-l'égout", "Tranchées et réseaux", "Fouilles et fondations",
               "Démolition et évacuation", "Devis gratuit et détaillé", "Visite et devis gratuits", "Terrassement Nantes, Pornic",
               "Terres évacuées", "Un seul interlocuteur", "Joignables 7 j/7"],
    descriptions=["Plateforme, fouilles, tranchées, assainissement : nous préparons votre terrain.",
                  "Visite sur place pour voir le sol, la pente et l'accès, puis devis écrit gratuit.",
                  "Terres et gravats évacués, terrain rendu propre, prêt pour la suite du chantier.",
                  "Intervention en Loire-Atlantique, sur le littoral, la presqu'île et le nord Vendée."]),
]

NEGATIVES = ["emploi", "recrutement", "salaire", "formation", "cap", "bac pro", "apprenti", "apprentissage", "stage", "alternance",
             "cours", "tuto", "tutoriel", "soi même", "soi-même", "diy", "bricolage", "leroy merlin", "castorama", "brico",
             "location", "louer", "mini pelle", "occasion", "pdf", "wikipedia", "wiki", "définition", "logiciel", "kit", "plan",
             "dessin", "outil", "jeu", "minecraft", "franc maçon", "franc-maçonnerie", "loge", "fiche métier", "assurance",
             "auto entrepreneur", "sous traitance", "sous-traitance", "matériaux"]

SITELINKS = [("Maçonnerie générale", "Murs, dalles, ouvertures", "Neuf et reprise de l'existant", SITE),
             ("Extension et surélévation", "Plain-pied, étage, garage", "Du gros œuvre aux finitions", SITE + "extension.html"),
             ("Terrassement", "Plateforme, fouilles, réseaux", "Assainissement individuel", SITE + "terrassement.html"),
             ("Demander un devis", "Visite sur place gratuite", "Devis écrit et détaillé", SITE + "#devis")]
CALLOUTS = ["Devis gratuit", "Visite sur place", "Joignables 7 j/7", "Un seul interlocuteur", "8 ans d'expérience",
            "Chantier rendu propre", "Particuliers et pros", "Rénovation clé en main"]
SNIPPET = ("Services", ["Maçonnerie", "Extension", "Surélévation", "Terrassement", "Assainissement", "Rénovation clé en main"])
PHONE = ("+33640238543", "FR")

# ---------------- Contrôles des limites Google Ads ----------------
errors = []
def lim(txt, n, what):
    if len(txt) > n: errors.append(f"{what} > {n} caractères ({len(txt)}) : {txt}")
    if "!" in txt and what.startswith("Titre"): errors.append(f"Point d'exclamation interdit dans un titre : {txt}")
for g in GROUPS:
    if len(g["headlines"]) != 15 or len(set(g["headlines"])) != 15: errors.append(f"{g['name']} : il faut 15 titres distincts")
    if len(g["descriptions"]) != 4: errors.append(f"{g['name']} : il faut 4 descriptions")
    for h in g["headlines"]: lim(h, 30, f"Titre {g['name']}")
    for d in g["descriptions"]: lim(d, 90, f"Description {g['name']}")
    for p in g["path"]: lim(p, 15, f"Chemin {g['name']}")
    for k in g["phrase"] + g["exact"]: lim(k, 80, "Mot-clé")
for t, d1, d2, _ in SITELINKS: lim(t, 25, "Lien annexe"); lim(d1, 35, "Description lien"); lim(d2, 35, "Description lien")
for c in CALLOUTS: lim(c, 25, "Accroche")
for v in SNIPPET[1]: lim(v, 25, "Extrait")
if errors: sys.exit("\n".join(errors))

# ---------------- Fichier 1 : campagne, zone, groupes, mots-clés, annonces ----------------
H1 = ["Campaign", "Campaign Type", "Networks", "Budget", "Budget type", "Bid Strategy Type", "Languages",
      "Targeting method", "Exclusion method", "Campaign Status", "Location", "Ad Group", "Ad Group Status",
      "Keyword", "Criterion Type", "Status", "Ad type"] + [f"Headline {i}" for i in range(1, 16)] + \
     [f"Description {i}" for i in range(1, 5)] + ["Path 1", "Path 2", "Final URL"]
rows = []
def row(**kw):
    r = {h: "" for h in H1}; r["Campaign"] = CAMPAIGN
    for k, v in kw.items(): r[k.replace("_", " ")] = v
    rows.append(r)
row(Campaign_Type="Search", Networks="Google search", Budget=f"{BUDGET_JOUR:.2f}", Budget_type="Daily",
    Bid_Strategy_Type="Maximize conversions", Languages="fr", Targeting_method="Location of presence",
    Exclusion_method="Location of presence", Campaign_Status=STATUS)
for lat, lon, r in GEO: row(Location=f"({r}km:{lat:.6f}:{lon:.6f})")
for n in NEGATIVES: row(Keyword=n, Criterion_Type="Campaign negative")
for g in GROUPS:
    row(Ad_Group=g["name"], Ad_Group_Status="Enabled")
    for k in g["phrase"]: row(Ad_Group=g["name"], Keyword=k, Criterion_Type="Phrase", Status="Enabled")
    for k in g["exact"]: row(Ad_Group=g["name"], Keyword=k, Criterion_Type="Exact", Status="Enabled")
    ad = {f"Headline {i+1}": h for i, h in enumerate(g["headlines"])}
    ad.update({f"Description {i+1}": d for i, d in enumerate(g["descriptions"])})
    r = {h: "" for h in H1}; r.update(ad); r.update({"Campaign": CAMPAIGN, "Ad Group": g["name"], "Ad type": "Responsive search ad",
        "Path 1": g["path"][0], "Path 2": g["path"][1], "Final URL": g["url"], "Status": "Enabled"}); rows.append(r)

# ---------------- Fichier 2 : composants (liens annexes, accroches, extraits, appel) ----------------
H2 = ["Campaign", "Sitelink text", "Description line 1", "Description line 2", "Final URL", "Callout text",
      "Header", "Snippet values", "Phone Number", "Country code", "Status"]
rows2 = []
def row2(**kw):
    r = {h: "" for h in H2}; r["Campaign"] = CAMPAIGN; r["Status"] = "Enabled"
    for k, v in kw.items(): r[k.replace("_", " ")] = v
    rows2.append(r)
for t, d1, d2, u in SITELINKS: row2(Sitelink_text=t, Description_line_1=d1, Description_line_2=d2, Final_URL=u)
for c in CALLOUTS: row2(Callout_text=c)
row2(Header=SNIPPET[0], Snippet_values=";".join(SNIPPET[1]))
row2(Phone_Number=PHONE[0], Country_code=PHONE[1])

def write(path, header, data):
    buf = io.StringIO(); w = csv.DictWriter(buf, fieldnames=header, delimiter="\t", lineterminator="\r\n"); w.writeheader(); w.writerows(data)
    open(path, "w", encoding="utf-16", newline="").write(buf.getvalue())

here = os.path.dirname(os.path.abspath(__file__))
write(os.path.join(here, "1-campagne-google-ads-editor.csv"), H1, rows)
write(os.path.join(here, "2-composants-google-ads-editor.csv"), H2, rows2)
kw = sum(len(g["phrase"]) + len(g["exact"]) for g in GROUPS)
print(f"OK : budget {BUDGET_JOUR:.2f} €/jour (plafond mensuel {BUDGET_JOUR*30.4:.2f} €), {len(GROUPS)} groupes, {kw} mots-clés, "
      f"{len(NEGATIVES)} négatifs, {len(GROUPS)} annonces, {len(GEO)} rayons, {len(rows)} + {len(rows2)} lignes")
