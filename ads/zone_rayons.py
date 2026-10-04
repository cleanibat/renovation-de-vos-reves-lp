# -*- coding: utf-8 -*-
"""Calcule les rayons Google Ads (cercles qui se chevauchent) couvrant le secteur du client.
Usage : python3 ads/zone_rayons.py [pénalité par cercle=4000] [marge km=2.5]  →  ads/rayons.json, lu par build_ads.py
Méthode : toutes les communes de 44, 85, 49, 35, 56 (geo.api.gouv.fr, centre + population). Le secteur est le polygone POLY.
Chaque commune du secteur doit être à moins de (rayon - marge) d'un cercle ; on minimise la population hors secteur touchée.
"""
import json, os, urllib.request
HERE=os.path.dirname(os.path.abspath(__file__))
CACHE=os.path.join(HERE,"communes.json")
if not os.path.exists(CACHE):
    allc=[]
    for dep in ["44","85","49","35","56"]:
        r=json.load(urllib.request.urlopen(f"https://geo.api.gouv.fr/departements/{dep}/communes?fields=nom,centre,population",timeout=60))
        allc+=[{"nom":x["nom"],"dep":dep,"lat":x["centre"]["coordinates"][1],"lon":x["centre"]["coordinates"][0],"pop":x.get("population",0)} for x in r if x.get("centre")]
    json.dump(allc,open(CACHE,"w"),ensure_ascii=False)
import math, sys
C=json.load(open(CACHE))
MUST=["Nantes","Saint-Nazaire","Guérande","Clisson","Nort-sur-Erdre","Saint-Jean-de-Monts","Pornic","Noirmoutier-en-l'Île","La Baule-Escoublac","Le Croisic","Saint-Hilaire-de-Riez","Sainte-Pazanne"]
NOT=["Ancenis-Saint-Géréon","Châteaubriant","Cholet","La Roche-sur-Yon","Montaigu-Vendée","Redon","Nozay"]
G={"cover":{c["nom"]:(c["lat"],c["lon"]) for c in C if c["nom"] in MUST and c["dep"] in ("44","85")},"exclude":{c["nom"]:(c["lat"],c["lon"]) for c in C if c["nom"] in NOT}}
POLY=[(47.30,-2.57),(47.41,-2.56),(47.49,-2.32),(47.48,-2.08),(47.52,-1.76),(47.48,-1.46),(47.31,-1.40),(47.18,-1.21),
      (47.05,-1.23),(47.02,-1.48),(46.97,-1.68),(46.80,-1.83),(46.69,-1.93),(46.75,-2.13),(46.88,-2.22),(47.01,-2.37),
      (47.07,-2.29),(47.13,-2.27),(47.20,-2.30),(47.24,-2.56)]
def inside(lat,lon):
    n=len(POLY); ins=False; j=n-1
    for i in range(n):
        yi,xi=POLY[i]; yj,xj=POLY[j]
        if (yi>lat)!=(yj>lat) and lon < (xj-xi)*(lat-yi)/(yj-yi)+xi: ins=not ins
        j=i
    return ins
def d(a,b):
    la1,lo1=map(math.radians,a); la2,lo2=map(math.radians,b)
    h=math.sin((la2-la1)/2)**2+math.cos(la1)*math.cos(la2)*math.sin((lo2-lo1)/2)**2
    return 12742*math.asin(math.sqrt(h))
IN=[c for c in C if inside(c["lat"],c["lon"])]; OUT=[c for c in C if not inside(c["lat"],c["lon"])]
bad=[n for n,p in G["cover"].items() if not inside(*p)]; badx=[n for n,p in G["exclude"].items() if inside(*p)]
print(len(IN),"communes dans le secteur (",sum(c["pop"] for c in IN),"hab.)", "| villes demandées hors polygone:",bad,"| exclues dedans:",badx)
if bad or badx: sys.exit()
PEN=float(sys.argv[1]) if len(sys.argv)>1 else 4000; MARG=float(sys.argv[2]) if len(sys.argv)>2 else 2.5
centres=[(c["lat"],c["lon"]) for c in IN]+[(46.65+i*0.03,-2.6+j*0.03) for i in range(30) for j in range(48) if inside(46.65+i*0.03,-2.6+j*0.03)]
NIN=len(IN); cands=[]
for c in centres:
    din=sorted((d(c,(x["lat"],x["lon"])),k) for k,x in enumerate(IN)); dout=sorted((d(c,(x["lat"],x["lon"])),k) for k,x in enumerate(OUT))
    for r in range(5,36):
        pts=frozenset(k for dd,k in din if dd<=r-MARG)
        outs=frozenset(k for dd,k in dout if dd<=r)
        cands.append((c,r,pts,outs))
todo=set(range(NIN)); chosen=[]; outc=set()
while todo:
    best=max(cands,key=lambda x: len(x[2]&todo)/(sum(OUT[k]["pop"] for k in x[3]-outc)+PEN))
    chosen.append(best); todo-=best[2]; outc|=best[3]
for c in sorted(chosen,key=lambda x:-sum(OUT[k]["pop"] for k in x[3])):
    rest=[x for x in chosen if x is not c]
    if rest and set(range(NIN))<=set().union(*[x[2] for x in rest]): chosen=rest
final=[]
for c in chosen:
    others=set().union(*[x[2] for x in chosen if x is not c]) if len(chosen)>1 else set()
    own=[k for k in c[2] if k not in others] or list(c[2])
    final.append((c[0],math.ceil(max(d(c[0],(IN[k]["lat"],IN[k]["lon"])) for k in own)+MARG)))
def report(circ,label):
    cov_in=[x for x in IN if any(d(c,(x["lat"],x["lon"]))<=r for c,r in circ)]
    cov_out=[x for x in OUT if any(d(c,(x["lat"],x["lon"]))<=r for c,r in circ)]
    print(f"{label}: {len(circ)} cercles | secteur couvert {len(cov_in)}/{len(IN)} communes | hors secteur touché : {len(cov_out)} communes, {sum(x['pop'] for x in cov_out)} hab.")
    return cov_out
report([((47.172,-1.902),51)],"Cercle unique 51 km")
co=report(final,f"Multi-cercles (pénalité {PEN:.0f})")
for c,r in sorted(final,key=lambda x:-x[0][0]):
    nm=min(IN,key=lambda x:d(c,(x["lat"],x["lon"])))["nom"]; print(f"   ({r}km:{c[0]:.4f}:{c[1]:.4f})  {nm}")
print("   hors secteur touchées (>2000 hab.):",sorted([(x["nom"],x["pop"]) for x in co if x["pop"]>2000],key=lambda t:-t[1]))
json.dump([[round(c[0],4),round(c[1],4),r] for c,r in final],open(os.path.join(HERE,"rayons.json"),"w"))
print("→ ads/rayons.json")
