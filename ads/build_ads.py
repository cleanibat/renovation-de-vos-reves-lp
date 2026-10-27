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
            "décaissement terrain", "nivellement terrain", "terrassement saint nazaire", "terrassement pornic"],
    exact=["entreprise de terrassement", "terrassement nantes", "terrassement loire atlantique", "terrassement maison"],
    headlines=["Terrassement Loire-Atlantique", "Entreprise de terrassement", "Terrassement de maison", "Terrassement de piscine",
               "Assainissement individuel", "Décaissement de terrain", "Nivellement de terrain", "Fouilles et fondations",
               "Démolition et évacuation", "Devis gratuit et détaillé", "Visite et devis gratuits", "Terrassement Nantes, Pornic",
               "Terres évacuées", "Un seul interlocuteur", "Joignables 7 j/7"],
    descriptions=["Plateforme, décaissement, fouilles, assainissement : nous préparons votre terrain.",
                  "Visite sur place pour voir le sol, la pente et l'accès, puis devis écrit gratuit.",
                  "Terres et gravats évacués, terrain rendu propre, prêt pour la suite du chantier.",
                  "Intervention en Loire-Atlantique, sur le littoral, la presqu'île et le nord Vendée."]),
]

# Groupes façade ajoutés le 2026-10-26 (pages /ravalement-facade et /enduit-imitation-pierre)
FACADE_GROUPS = [
  dict(name="Ravalement de façade", url=SITE + "ravalement-facade", path=("facade", "ravalement"),
    phrase=["ravalement de façade", "ravalement façade", "entreprise ravalement façade", "façadier", "enduit façade",
            "enduit de façade", "rénovation façade", "enduit façade maison neuve", "crépi façade", "ravalement façade nantes",
            "façadier nantes", "ravalement façade loire atlantique", "enduit monocouche", "enduit à la chaux façade",
            "fissure façade", "ravalement façade prix"],
    exact=["ravalement de façade", "façadier", "enduit façade", "ravalement façade nantes"],
    headlines=["Ravalement de façade", "Enduit de façade", "Façadier Loire-Atlantique", "Enduit sur maison neuve",
               "Rénovation de façade", "Traitement des fissures", "Enduit à la chaux", "Rejointoiement de pierre",
               "Façadier à Nantes et Pornic", "Devis gratuit et détaillé", "Visite et devis gratuits", "En neuf comme en rénovation",
               "Finition grattée ou talochée", "Un seul interlocuteur", "Joignables 7 j/7"],
    descriptions=["Enduit sur maison neuve ou ravalement : du support à la finition, teinte au choix.",
                  "Fissures, enduit qui se décolle, façade salie : nous remettons votre façade à neuf.",
                  "Visite sur place et devis écrit détaillé, gratuit et sans engagement. Appelez-nous.",
                  "Intervention en Loire-Atlantique, sur le littoral, la presqu'île et le nord Vendée."]),
  dict(name="Enduit imitation pierre", url=SITE + "enduit-imitation-pierre", path=("enduit", "fausse-pierre"),
    phrase=["enduit imitation pierre", "imitation pierre façade", "fausse pierre façade", "enduit fausse pierre",
            "enduit pierre sculpté", "façade imitation pierre", "enduit imitation pierre prix", "imitation pierre de taille",
            "enduit façon pierre", "enduit imitation pierre nantes", "enduit imitation pierre loire atlantique",
            "habillage façade pierre", "mur imitation pierre", "enduit décoratif façade"],
    exact=["enduit imitation pierre", "imitation pierre façade", "fausse pierre façade", "enduit fausse pierre"],
    headlines=["Enduit imitation pierre", "L'aspect de la pierre", "Fausse pierre sculptée main", "Façon pierre de taille",
               "Façon moellons ou pierre sèche", "Encadrements, soubassements", "Sans démolir ni reconstruire",
               "Imitation pierre à Nantes", "Devis gratuit et détaillé", "Visite et devis gratuits", "Style et teinte au choix",
               "Murs intérieurs, cheminées", "Un seul interlocuteur", "Joignables 7 j/7", "En Loire-Atlantique"],
    descriptions=["Un enduit sculpté à la main qui donne à votre façade l'aspect de la pierre.",
                  "Pierre de taille, moellon, pierre sèche : style, joints et teinte choisis avec vous.",
                  "Visite sur place et devis écrit détaillé, gratuit et sans engagement. Appelez-nous.",
                  "Intervention en Loire-Atlantique, sur le littoral, la presqu'île et le nord Vendée."]),
]
GROUPS += FACADE_GROUPS

# Groupe maîtrise d'œuvre ajouté le 2026-10-27 (page /maitrise-d-oeuvre)
MOE_GROUPS = [
  dict(name="Maîtrise d'œuvre", url=SITE + "maitrise-d-oeuvre", path=("maitrise-oeuvre", "devis-gratuit"),
    phrase=["maître d'œuvre", "maîtrise d'œuvre", "maître d'œuvre nantes", "maître d'œuvre loire atlantique",
            "maître d'œuvre rénovation", "maîtrise d'œuvre rénovation", "maître d'œuvre extension maison",
            "maître d'œuvre agrandissement", "maître d'œuvre saint nazaire", "maître d'œuvre pornic", "maître d'œuvre la baule",
            "maître d'œuvre permis de construire", "tarif maître d'œuvre", "coordination de travaux rénovation",
            "suivi de chantier rénovation"],
    exact=["maître d'œuvre", "maîtrise d'œuvre", "maître d'œuvre nantes", "maître d'œuvre rénovation"],
    headlines=["Maîtrise d'œuvre", "Maître d'œuvre à Nantes", "Maître d'œuvre Saint-Nazaire", "Maître d'œuvre rénovation",
               "Plans et permis de construire", "Consultation des entreprises", "Suivi de chantier",
               "Du plan à la réception", "Devis comparés poste par poste", "Rénovation et extension", "Un seul interlocuteur",
               "Visite et devis gratuits", "En Loire-Atlantique", "Joignables 7 j/7", "8 ans d'expérience"],
    descriptions=["Plans, permis, choix des entreprises et suivi du chantier : nous pilotons votre projet.",
                  "Rénovation, extension, surélévation : un seul interlocuteur de l'idée à la réception.",
                  "Visite sur place et devis écrit détaillé, gratuit et sans engagement. Appelez-nous.",
                  "Intervention en Loire-Atlantique, sur le littoral, la presqu'île et le nord Vendée."]),
]
GROUPS += MOE_GROUPS
# études et métier (recherches d'emploi ou de cours), documents types
MOE_NEGATIVES = ["devenir", "bts", "école", "diplôme", "modèle", "loi mop", "cctp", "dce"]
# bricolage / produits pour l'imitation pierre (achats, pas des chantiers)
FACADE_NEGATIVES = ["plaquette", "panneau", "polystyrène", "pvc", "adhésif", "sticker", "papier peint", "pochoir", "moule",
                    "tampon", "rouleau", "weber", "parex", "sac", "seau", "achat", "acheter", "vente"]

NEGATIVES = ["emploi", "recrutement", "salaire", "formation", "cap", "bac pro", "apprenti", "apprentissage", "stage", "alternance",
             "cours", "tuto", "tutoriel", "soi même", "soi-même", "diy", "bricolage", "leroy merlin", "castorama", "brico",
             "location", "louer", "mini pelle", "occasion", "pdf", "wikipedia", "wiki", "définition", "logiciel", "kit", "plan",
             "dessin", "outil", "jeu", "minecraft", "franc maçon", "franc-maçonnerie", "loge", "fiche métier", "assurance",
             "auto entrepreneur", "sous traitance", "sous-traitance", "matériaux",
             "égout", "tout à l'égout", "vrd", "viabilisation", "voirie"]

SITELINKS = [("Maçonnerie générale", "Murs, dalles, ouvertures", "Neuf et reprise de l'existant", SITE),
             ("Extension et surélévation", "Plain-pied, étage, garage", "Du gros œuvre aux finitions", SITE + "extension.html"),
             ("Terrassement", "Plateforme, fouilles, décaissement", "Assainissement individuel", SITE + "terrassement.html"),
             ("Demander un devis", "Visite sur place gratuite", "Devis écrit et détaillé", SITE + "#devis")]
FACADE_SITELINKS = [("Ravalement de façade", "Enduit neuf ou rénovation", "Fissures, chaux, rejointoiement", SITE + "ravalement-facade"),
                    ("Enduit imitation pierre", "Sculpté à la main", "Façade, encadrements, intérieur", SITE + "enduit-imitation-pierre")]
SITELINKS += FACADE_SITELINKS
MOE_SITELINKS = [("Maîtrise d'œuvre", "Plans, permis, entreprises", "Suivi de chantier, réception", SITE + "maitrise-d-oeuvre")]
SITELINKS += MOE_SITELINKS
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
for n in NEGATIVES + FACADE_NEGATIVES + MOE_NEGATIVES: row(Keyword=n, Criterion_Type="Campaign negative")
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
# ---------------- Fichier 3 : ajout des seuls groupes façade (sans toucher au reste de la campagne) ----------------
names = {g["name"] for g in FACADE_GROUPS}
rows3 = [r for r in rows if r["Ad Group"] in names] + [r for r in rows if r["Criterion Type"] == "Campaign negative" and r["Keyword"] in FACADE_NEGATIVES]
write(os.path.join(here, "3-ajout-groupes-facade.csv"), H1, rows3)
rows4 = [r for r in rows2 if r["Sitelink text"] in {t for t, *_ in FACADE_SITELINKS}]
write(os.path.join(here, "4-ajout-liens-annexes-facade.csv"), H2, rows4)
print(f"Ajout façade : {len(rows3)} lignes (2 groupes, {sum(len(g['phrase'])+len(g['exact']) for g in FACADE_GROUPS)} mots-clés, 2 annonces, {len(FACADE_NEGATIVES)} négatifs) + {len(rows4)} liens annexes")
# ---------------- Fichiers 5 et 6 : ajout du seul groupe maîtrise d'œuvre ----------------
names = {g["name"] for g in MOE_GROUPS}
rows5 = [r for r in rows if r["Ad Group"] in names] + [r for r in rows if r["Criterion Type"] == "Campaign negative" and r["Keyword"] in MOE_NEGATIVES]
write(os.path.join(here, "5-ajout-groupe-maitrise-oeuvre.csv"), H1, rows5)
rows6 = [r for r in rows2 if r["Sitelink text"] in {t for t, *_ in MOE_SITELINKS}]
write(os.path.join(here, "6-ajout-lien-annexe-maitrise-oeuvre.csv"), H2, rows6)
print(f"Ajout maîtrise d'œuvre : {len(rows5)} lignes (1 groupe, {sum(len(g['phrase'])+len(g['exact']) for g in MOE_GROUPS)} mots-clés, 1 annonce, {len(MOE_NEGATIVES)} négatifs) + {len(rows6)} lien annexe")
write(os.path.join(here, "1-campagne-google-ads-editor.csv"), H1, rows)
write(os.path.join(here, "2-composants-google-ads-editor.csv"), H2, rows2)
kw = sum(len(g["phrase"]) + len(g["exact"]) for g in GROUPS)
print(f"OK : budget {BUDGET_JOUR:.2f} €/jour (plafond mensuel {BUDGET_JOUR*30.4:.2f} €), {len(GROUPS)} groupes, {kw} mots-clés, "
      f"{len(NEGATIVES)} négatifs, {len(GROUPS)} annonces, {len(GEO)} rayons, {len(rows)} + {len(rows2)} lignes")
