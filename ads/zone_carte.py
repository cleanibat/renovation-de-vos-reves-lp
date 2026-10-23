# -*- coding: utf-8 -*-
"""Génère img/carte-zone.svg : carte de la zone d'intervention (Loire-Atlantique + nord Vendée).
Contours : france-geojson (gregoiredavid, version simplifiée) ; villes : ads/communes.json (geo.api.gouv.fr).
Usage : python3 ads/zone_carte.py
"""
import json, math, os
D = os.path.dirname(os.path.abspath(__file__))
deps = {f["properties"]["code"]: f["geometry"] for f in json.load(open(os.path.join(D, "departements-simplifies.geojson")))["features"]}
communes = {c["nom"]: c for c in json.load(open(os.path.join(D, "communes.json"))) if c["dep"] in ("44", "85")}

LON0, LON1, LAT0, LAT1 = -2.72, -0.88, 46.52, 47.88   # cadrage
K = 400                                                 # pixels par degré de latitude
CL = math.cos(math.radians((LAT0 + LAT1) / 2))
W, H = (LON1 - LON0) * CL * K, (LAT1 - LAT0) * K
def xy(lon, lat): return ((lon - LON0) * CL * K, (LAT1 - lat) * K)

def path(geom):
    polys = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
    d = ""
    for poly in polys:
        for ring in poly:
            pts = [xy(*p) for p in ring]
            d += "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + "Z"
    return d

VILLES = [("Nantes", "r"), ("Saint-Nazaire", "rb"), ("Guérande", "l"), ("Pornic", "l"), ("Clisson", "r"),
          ("Nort-sur-Erdre", "r"), ("Saint-Jean-de-Monts", "l"), ("Challans", "r"), ("Noirmoutier-en-l'Île", "l"),
          ("La Baule-Escoublac", "lb"), ("Machecoul-Saint-Même", "r"), ("Vallet", "r")]
LABEL = {"Noirmoutier-en-l'Île": "Noirmoutier", "La Baule-Escoublac": "La Baule", "Machecoul-Saint-Même": "Machecoul"}

out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H:.0f}" class="zone-map-svg" role="img" aria-label="Carte de la zone d\'intervention : Loire-Atlantique et nord de la Vendée">',
       '<style>.zm-dep{font:700 15px Outfit,system-ui,sans-serif;letter-spacing:.12em;fill:#141e4f;opacity:.75}.zm-city{font:600 13px Inter,system-ui,sans-serif;fill:#141e4f;paint-order:stroke;stroke:#fff;stroke-width:3px;stroke-linejoin:round}.zm-hq{font:700 14px Outfit,system-ui,sans-serif;fill:#141e4f;paint-order:stroke;stroke:#fff;stroke-width:3.5px;stroke-linejoin:round}.zm-sea{font:italic 500 13px Inter,system-ui,sans-serif;fill:#7d97ab;letter-spacing:.08em}</style>',
       '<defs><clipPath id="cv"><path d="' + path(deps["85"]) + '"/></clipPath></defs>',
       f'<rect width="{W:.0f}" height="{H:.0f}" fill="#e6eef4"/>']
for code in ("56", "35", "49", "79"):
    out.append(f'<path d="{path(deps[code])}" fill="#f4f1ea" stroke="#d6d0c3" stroke-width="1.5"/>')
out.append(f'<path d="{path(deps["85"])}" fill="#f4f1ea" stroke="#c9b98f" stroke-width="1.5"/>')
# nord-ouest de la Vendée : secteur des rayons Google Ads (POLY de zone_rayons.py) limité à la Vendée
POLY = [(47.30,-2.57),(47.41,-2.56),(47.49,-2.32),(47.48,-2.08),(47.52,-1.76),(47.48,-1.46),(47.31,-1.40),(47.18,-1.21),
        (47.05,-1.23),(47.02,-1.48),(46.97,-1.68),(46.80,-1.83),(46.69,-1.93),(46.75,-2.13),(46.88,-2.22),(47.01,-2.37),
        (47.07,-2.29),(47.13,-2.27),(47.20,-2.30),(47.24,-2.56)]
# élargi vers la mer pour couvrir le littoral et Noirmoutier (le polygone Ads suit les communes, pas le trait de côte)
SEA = [(46.66,-2.75),(47.10,-2.75)]
pts = [xy(lon, lat) for lat, lon in POLY[:13]] + [xy(lon, lat) for lat, lon in SEA] + [xy(lon, lat) for lat, lon in POLY[17:]]
out.append('<path d="M' + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + 'Z" fill="#f3d27a" clip-path="url(#cv)"/>')
out.append(f'<path d="{path(deps["44"])}" fill="#ebae01" fill-opacity=".85" stroke="#b98a00" stroke-width="2"/>')
# libellés départements
for txt, lon, lat in (("LOIRE-ATLANTIQUE", -1.66, 47.57), ("VENDÉE", -1.25, 46.62)):
    x, y = xy(lon, lat)
    out.append(f'<text x="{x:.0f}" y="{y:.0f}" class="zm-dep" text-anchor="middle">{txt}</text>')
for nom, side in VILLES:
    c = communes[nom]; x, y = xy(c["lon"], c["lat"])
    lab = LABEL.get(nom, nom)
    dx, anchor, dy = {"r": (9, "start", 4), "l": (-9, "end", 4), "b": (0, "middle", 18), "lb": (-7, "end", 16), "rb": (7, "start", 16)}[side]
    out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.5" fill="#141e4f" stroke="#fff" stroke-width="1.5"/>')
    out.append(f'<text x="{x+dx:.1f}" y="{y+dy:.1f}" class="zm-city" text-anchor="{anchor}">{lab}</text>')
c = communes["Sainte-Pazanne"]; x, y = xy(c["lon"], c["lat"])
out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="9" fill="#141e4f" stroke="#fff" stroke-width="2.5"/>'
           f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.2" fill="#ebae01"/>'
           f'<text x="{x+13:.1f}" y="{y+5:.1f}" class="zm-hq">Sainte-Pazanne</text>')
x, y = xy(-2.47, 46.68)
out.append(f'<text x="{x:.0f}" y="{y:.0f}" class="zm-sea" text-anchor="middle">Océan</text><text x="{x:.0f}" y="{y+18:.0f}" class="zm-sea" text-anchor="middle">Atlantique</text>')
out.append("</svg>")
open(os.path.join(D, "..", "img", "carte-zone.svg"), "w", encoding="utf-8").write("".join(out))
print(f"img/carte-zone.svg : {W:.0f}x{H:.0f}, {len(''.join(out))//1024} Ko")
