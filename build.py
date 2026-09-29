# -*- coding: utf-8 -*-
"""Génère les landing pages Google Ads de La Rénovation de vos rêves (maçonnerie).
Usage : python3 build.py   →   index.html, merci.html, sitemap.xml, robots.txt
"""
import datetime, html, json, os

# ---------------- Configuration ----------------
GTM_ID = ""  # ex. "GTM-XXXXXXX" ; vide = snippet commenté
SITE = "https://cleanibat.github.io/renovation-de-vos-reves-lp/"  # domaine final à remplacer (canonical, _next, sitemap)
BRAND = "La Rénovation de vos rêves"
PHONE_DISPLAY = "06 40 23 85 43"
PHONE_INTL = "+33640238543"
EMAIL = "contact@larenovationdevosreves.fr"
FORM_ACTION = f"https://formsubmit.co/{EMAIL}"
ADDRESS = "1A impasse des Gatines, 44680 Sainte-Pazanne"
HOURS = "7 j/7, de 7 h à 20 h"
SITE_CLIENT = "https://www.larenovationdevosreves.fr"
FACEBOOK = "https://www.facebook.com/Larenovationdevosreves/"
SIRET = "918 123 084 00017"
YEAR = datetime.date.today().year
TODAY = datetime.date.today().isoformat()

# ---------------- Icônes ----------------
def ico(path, sw=2):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{path}</svg>'

I = dict(
    PHONE=ico('<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.8 19.8 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.12 4.18 2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/>'),
    ARROW=ico('<path d="M5 12h14M13 6l6 6-6 6"/>', 2.2),
    CHECK=ico('<path d="M20 6 9 17l-5-5"/>', 2.6),
    PIN=ico('<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>'),
    MAIL=ico('<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 7L2 7"/>'),
    CLOCK=ico('<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>'),
    DOC=ico('<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M16 13H8M16 17H8M10 9H8"/>'),
    USER=ico('<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>'),
    BROOM=ico('<path d="M19 3 9.5 12.5"/><path d="M6 21c-1.5 0-3-1.5-3-3 0-2 3-5 6-6l3 3c-1 3-4 6-6 6z"/>'),
    WALL=ico('<path d="M3 5h18v14H3z"/><path d="M3 10h18M3 15h18M8 5v5M13 10v5M8 15v4M16 5v5M16 15v4"/>'),
    DOOR=ico('<path d="M4 21V5a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v16"/><path d="M2 21h20M9 21V9h6v12"/>'),
    SLAB=ico('<path d="M2 17l10 4 10-4"/><path d="M2 12l10 4 10-4"/><path d="M2 7l10 4 10-4-10-4z"/>'),
    HOME=ico('<path d="M3 11 12 3l9 8"/><path d="M5 10v10h14V10"/><path d="M10 20v-6h4v6"/>'),
    HOUSEPLUS=ico('<path d="M3 11 12 3l9 8"/><path d="M5 10v10h14V10"/><path d="M12 12v6M9 15h6"/>'),
    DIGGER=ico('<path d="M2 20h20"/><path d="M4 20v-5h7l3-6h4l2 4v7"/><path d="M11 15V9l-3-3H5"/><circle cx="7" cy="20" r="0"/>'),
    TROWEL=ico('<path d="m3 3 9 9"/><path d="M12 12l-3 8 8-3 4-9-9 4z"/>'),
    SHIELD=ico('<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>'),
    STAR='<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="m12 2 3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01z"/></svg>',
    FB='<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M13.5 22v-8h2.7l.4-3.2h-3.1V8.8c0-.9.3-1.6 1.6-1.6h1.7V4.4c-.3 0-1.3-.1-2.5-.1-2.5 0-4.1 1.5-4.1 4.2v2.3H7.4V14h2.8v8z"/></svg>',
)

# ---------------- Contenu de la LP Maçonnerie ----------------
PAGE = dict(
    file="index.html",
    lp="Maçonnerie",
    title="Maçonnerie en Loire-Atlantique | La Rénovation de vos rêves",
    desc="Entreprise de maçonnerie et gros œuvre en Loire-Atlantique et nord Vendée : murs, ouvertures, dalles, extensions, terrassement. Devis gratuit, un seul interlocuteur.",
    hero_img="img/hero-maison-pierre-extension.jpg",
    hero_alt="Maison en pierre agrandie par une extension à toit plat, en Loire-Atlantique",
    h1='Maçonnerie générale et gros œuvre <em>en Loire-Atlantique</em>',
    sub="Murs, dalles, ouvertures dans les murs porteurs, extensions et surélévations, terrassement, rénovation clé en main : nous réalisons vos travaux de maçonnerie en Loire-Atlantique et dans le nord de la Vendée, avec un seul interlocuteur du devis à la réception du chantier.",
    reassurance=[
        ("Devis gratuit et sans engagement", "DOC"),
        ("Visite sur place et devis détaillé écrit", "PIN"),
        ("Un seul interlocuteur du début à la fin", "USER"),
        ("Chantier suivi régulièrement et rendu propre", "BROOM"),
    ],
    services_eyebrow="Nos travaux de maçonnerie",
    services_h2="Ce que nous réalisons",
    services_lead="Maçonnerie neuve ou reprise sur l'existant, pour les particuliers, les professionnels et les collectivités.",
    services=[
        ("WALL", "Murs et élévation", "Élévation de murs en parpaings, briques ou béton cellulaire, murs de clôture, murets et piliers, en construction neuve comme en rénovation.", "Le plus demandé", "murs"),
        ("DOOR", "Ouvertures dans les murs porteurs", "Création ou agrandissement d'une baie, d'une porte ou d'une fenêtre, étaiement, pose de linteau ou de poutre métallique et reprise des finitions autour de l'ouverture.", "Mur porteur", "ouverture"),
        ("SLAB", "Dalles, chapes et fondations", "Fondations, dalle béton et chape pour une maison, un garage, une annexe ou une terrasse, avec préparation du sol adaptée au terrain.", "", "dalle"),
        ("HOUSEPLUS", "Extension et surélévation", "Agrandissement latéral ou surélévation de toiture, du gros œuvre à la finition, en continuité avec l'existant.", "Clé en main", "extension"),
        ("HOME", "Rénovation clé en main", "Rénovation complète de maisons, d'appartements et de granges : gros œuvre, second œuvre, isolation, électricité, plomberie, cuisines et salles de bains. Un seul interlocuteur du premier rendez-vous à la remise des clés.", "Du gros œuvre aux finitions", "renovation"),
        ("DIGGER", "Terrassement et assainissement", "Préparation du terrain, fouilles pour fondations, tranchées et réseaux, mise en place ou remplacement de l'assainissement.", "", "terrassement"),
        ("TROWEL", "Reprise et rejointoiement", "Reprise de maçonnerie ancienne, rejointoiement de murs en pierre, finitions, démolition et préparation de chantier avant rénovation lourde.", "Bâti ancien", "reprise"),
    ],
    why_eyebrow="Pourquoi nous confier vos travaux",
    why_h2="Une entreprise du bâtiment installée à Sainte-Pazanne depuis 8 ans",
    why_lead="Nous intervenons de la conception à la réception des travaux, sur des chantiers de maçonnerie neuve, d'agrandissement ou de rénovation lourde.",
    why=[
        ("USER", "Un interlocuteur unique", "Vous n'avez qu'un seul contact : nous établissons le devis, planifions les travaux, réalisons le chantier et le suivons jusqu'à la réception."),
        ("DOC", "Un devis détaillé et écrit", "Chaque poste est chiffré par écrit après la visite sur place : matériaux, main-d'œuvre, évacuation des gravats. Vous savez ce que vous payez avant de signer."),
        ("SHIELD", "Conformité aux normes", "Nous contrôlons la qualité, la sécurité et la conformité des travaux aux normes en vigueur, à chaque étape du chantier."),
        ("CLOCK", "Joignables 7 j/7", "Du lundi au dimanche, de 7 h à 20 h, par téléphone ou par le formulaire. Devis gratuit, sans engagement."),
    ],
    process_eyebrow="Comment ça se passe",
    process_h2="Votre chantier en quatre étapes",
    process=[
        ("Prise de contact", "Vous nous appelez ou remplissez le formulaire. Nous échangeons sur votre projet, vos contraintes et vos délais."),
        ("Visite et devis", "Nous nous déplaçons sur place pour mesurer, vérifier l'existant et l'accès, puis vous remettons un devis détaillé et gratuit."),
        ("Planification", "Une fois le devis signé, nous planifions les travaux, préparons les autorisations si nécessaire et fixons avec vous la date de démarrage du chantier."),
        ("Chantier et réception", "Nous suivons le chantier régulièrement, contrôlons la qualité et la conformité, et vous livrons un chantier propre."),
    ],
    gallery_eyebrow="Réalisations",
    gallery_h2="Avant / après",
    gallery_lead="Faites glisser le curseur pour comparer.",
    before_after=[
        ("img/avant-maison.jpg", "img/apres-maison.jpg", "Extension d'une maison en pierre", "Maison en pierre avant travaux", "Maison en pierre avec son extension bois à toit plat"),
        ("img/avant-grange.jpg", "img/apres-grange.jpg", "Rénovation d'une grange", "Intérieur de grange avant rénovation", "Intérieur de grange rénové avec charpente apparente"),
    ],
    gallery=[
        ("img/maison-pierre-jardin.jpg", "Maison en pierre rénovée avec son jardin"),
        ("img/extension-bois-maison-pierre.jpg", "Extension en ossature bois sur une maison en pierre"),
        ("img/mur-pierre-interieur.jpg", "Mur en pierre apparente rejointoyé dans une cuisine"),
        ("img/facade-pierre-allee.jpg", "Façade en pierre et allée dallée"),
    ],
    reviews_eyebrow="Ils nous ont fait confiance",
    reviews_h2="Témoignages de nos clients",
    reviews_note="Témoignages publiés sur larenovationdevosreves.fr.",
    reviews=[
        ("Machpy", "Nous sommes satisfaits du travail de maçonnerie effectué. De plus, Corentin Douillard est très sympathique."),
        ("Lallement", "Très satisfaite du travail réalisé sur mes deux chantiers de ravalement de façades. Ces derniers ont été menés de main de maître par le chef d'équipe."),
        ("Dupont", "Un excellent conseil, des délais très courts respectés, pour une réalisation et une finition impeccables, avec une finition de chantier parfaite."),
        ("Bohème", "J'ai fait appel à cette entreprise de rénovation-construction pour effectuer un agrandissement, je recommande vivement."),
    ],
    zone_eyebrow="Zone d'intervention",
    zone_h2="Toute la Loire-Atlantique et le nord de la Vendée",
    zone_lead="Installés à Sainte-Pazanne, nous intervenons dans toute la Loire-Atlantique et dans le nord de la Vendée, chez les particuliers, les professionnels et les collectivités.",
    zone_cols=[
        ("Nantes et agglomération", ["Nantes", "Rezé", "Saint-Herblain", "Vertou", "Bouguenais", "Clisson", "Nort-sur-Erdre", "Sainte-Pazanne", "Machecoul-Saint-Même"]),
        ("Littoral et presqu'île", ["Saint-Nazaire", "Guérande", "La Baule-Escoublac", "Pornichet", "Saint-Brevin-les-Pins", "Pornic", "La Bernerie-en-Retz", "La Plaine-sur-Mer", "Saint-Michel-Chef-Chef"]),
        ("Nord Vendée", ["Saint-Jean-de-Monts", "Noirmoutier-en-l'Île", "Challans", "Saint-Hilaire-de-Riez", "Beauvoir-sur-Mer"]),
    ],
    faq_eyebrow="Questions fréquentes",
    faq_h2="Ce que nos clients nous demandent",
    faq=[
        ("Faut-il une autorisation de la mairie pour une extension ou une ouverture ?",
         "Une extension ou une surélévation nécessite une déclaration préalable de travaux ou un permis de construire selon la surface créée et le plan local d'urbanisme de votre commune. Une ouverture en façade demande en général une déclaration préalable. Nous vous indiquons la démarche à suivre lors de la visite et préparons les éléments techniques du dossier."),
        ("Combien coûtent des travaux de maçonnerie ?",
         "Le prix dépend de la nature des travaux (mur, dalle, ouverture, extension), des matériaux, de l'accès au chantier et de l'état de l'existant. C'est pourquoi nous nous déplaçons avant de chiffrer : le devis est gratuit, détaillé poste par poste, et sans engagement."),
        ("Intervenez-vous sur les maisons anciennes en pierre ?",
         "Oui. Reprise de murs, rejointoiement, ouvertures dans des murs en pierre ou en moellons, extension en continuité avec l'existant : nous adaptons les matériaux et les techniques au bâti ancien, fréquent en Loire-Atlantique et sur le littoral."),
        ("Pouvez-vous ouvrir un mur porteur en toute sécurité ?",
         "Oui. Nous étayons le mur pendant les travaux, ouvrons la maçonnerie, posons un linteau ou une poutre métallique adaptés aux charges à reprendre, puis reprenons les finitions. C'est un travail de maçonnerie courant sur les maisons anciennes comme récentes."),
        ("Que deviennent les gravats et les déchets de chantier ?",
         "L'évacuation des gravats et des matériaux de démolition est prévue dans le devis. Ils sont triés et déposés en déchetterie professionnelle ou en filière de recyclage. Le chantier est nettoyé à la fin des travaux."),
        ("Travaillez-vous pour les professionnels et les collectivités ?",
         "Oui. Nous réalisons pour les particuliers, les entreprises (locaux, bureaux, commerces) et les collectivités des travaux de construction, d'agrandissement et de rénovation, avec les mêmes étapes : visite, devis détaillé, planification, chantier et réception."),
    ],
    cta_eyebrow="Parlons de votre projet",
    cta_h2="Demandez votre devis gratuit",
    cta_lead="Décrivez vos travaux en quelques lignes, nous vous rappelons pour convenir d'une visite sur place.",
    form_needs=["Murs, élévation, clôture", "Ouverture dans un mur porteur", "Dalle, chape ou fondations", "Extension ou surélévation", "Rénovation clé en main", "Terrassement, assainissement", "Reprise de maçonnerie, rejointoiement", "Autre projet"],
    form_msg_ph="Type de travaux, surface ou dimensions approximatives, état de l'existant, accès au chantier, délai souhaité…",
)

# ---------------- Blocs communs ----------------
def gtm_head():
    s = "<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);})(window,document,'script','dataLayer','%s');</script>" % (GTM_ID or "GTM-XXXXXXX")
    return "<!-- Google Tag Manager -->\n" + (s if GTM_ID else "<!-- " + s + " -->") + "\n<!-- End Google Tag Manager -->"

def gtm_body():
    s = '<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=%s" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>' % (GTM_ID or "GTM-XXXXXXX")
    return s if GTM_ID else "<!-- " + s + " -->"

def head(title, desc, canonical, og_img, extra_ld="", noindex=True, preload=None):
    robots = "noindex, follow" if noindex else "index, follow"
    pre = f'<link rel="preload" as="image" href="{preload}" fetchpriority="high">' if preload else ""
    return f'''<!DOCTYPE html>
<html lang="fr-FR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:locale" content="fr_FR">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:image" content="{SITE}{og_img}">
<meta property="og:url" content="{canonical}">
<meta name="theme-color" content="#141e4f">
<link rel="icon" href="img/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="img/apple-touch-icon.png">
{pre}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@500;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
{gtm_head()}
{extra_ld}
</head>
<body>
{gtm_body()}
'''

def header():
    return f'''<header class="header">
  <div class="wrap">
    <a class="logo" href="#top" aria-label="{BRAND}"><img src="img/logo-clair.png" alt="{BRAND}" width="513" height="164"></a>
    <div class="header-cta">
      <a class="header-phone" href="tel:{PHONE_INTL}">{I['PHONE']}<span><small>Appelez-nous</small>{PHONE_DISPLAY}</span></a>
      <a class="btn btn-primary" href="#devis">Devis gratuit</a>
    </div>
  </div>
</header>
'''

def mobile_bar():
    return f'''<div class="mobile-bar">
  <a href="tel:{PHONE_INTL}" class="btn btn-outline">{I['PHONE']}Appeler</a>
  <a href="#devis" class="btn btn-primary">Devis gratuit</a>
</div>
'''

def footer():
    return f'''<footer class="footer">
  <div class="wrap footer-grid">
    <div>
      <img src="img/logo-renovation-de-vos-reves.png" alt="{BRAND}" width="513" height="164" class="footer-logo" loading="lazy">
      <p class="footer-role">Entreprise du bâtiment · Gros œuvre, maçonnerie, rénovation et construction</p>
      <p><a href="{SITE_CLIENT}" rel="noopener">larenovationdevosreves.fr</a> · <a href="{FACEBOOK}" rel="noopener" class="fb">{I['FB']}Facebook</a></p>
    </div>
    <div>
      <h3>Contact</h3>
      <p><a href="tel:{PHONE_INTL}">{PHONE_DISPLAY}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p>
      <p>{HOURS}</p>
    </div>
    <div>
      <h3>Adresse</h3>
      <p>{ADDRESS}</p>
      <p>SIRET {SIRET}</p>
    </div>
  </div>
  <div class="wrap footer-bottom">
    <p>© <span id="year">{YEAR}</span> {BRAND} · <a href="{SITE_CLIENT}/mentions" rel="noopener">Mentions légales</a></p>
  </div>
</footer>
<script src="main.js" defer></script>
</body>
</html>
'''

def form(p):
    opts = "".join(f'<option value="{html.escape(o)}">{html.escape(o)}</option>' for o in p["form_needs"])
    return f'''<form id="devisForm" class="form" action="{FORM_ACTION}" method="POST">
  <input type="hidden" name="_subject" value="Nouvelle demande de devis – {p['lp']}">
  <input type="hidden" name="_template" value="table">
  <input type="hidden" name="_captcha" value="false">
  <input type="hidden" name="_next" value="{SITE}merci.html?lp={p['lp'].lower().replace('ç','c')}">
  <input type="hidden" name="Source" value="LP {p['lp']}">
  <input type="text" name="_honey" class="honeypot" tabindex="-1" autocomplete="off" aria-hidden="true">
  <div class="grid-2">
    <label>Nom et prénom<input type="text" name="Nom" required autocomplete="name" placeholder="Jean Dupont"></label>
    <label>Téléphone<input type="tel" name="Téléphone" required autocomplete="tel" placeholder="06 12 34 56 78"></label>
    <label>E-mail<input type="email" name="E-mail" required autocomplete="email" placeholder="jean.dupont@exemple.fr"></label>
    <label>Commune du chantier<input type="text" name="Commune" required placeholder="Nantes, Saint-Nazaire, Guérande…"></label>
  </div>
  <label>Votre besoin<select name="Besoin" required><option value="" disabled selected>Choisir…</option>{opts}</select></label>
  <label>Décrivez votre projet (facultatif)<textarea name="Message" rows="4" placeholder="{html.escape(p['form_msg_ph'])}"></textarea></label>
  <button type="submit" class="btn btn-primary btn-block" data-sending="Envoi…">{I['ARROW']}Envoyer ma demande de devis</button>
  <p class="form-note">{I['SHIELD']}Vos données restent confidentielles et servent uniquement à traiter votre demande. Aucune revente, aucun démarchage.</p>
</form>'''

# ---------------- Page LP ----------------
def build_lp(p):
    ld_business = {
        "@context": "https://schema.org", "@type": "HomeAndConstructionBusiness", "name": BRAND,
        "url": SITE + p["file"], "telephone": PHONE_INTL, "email": EMAIL, "image": SITE + p["hero_img"],
        "address": {"@type": "PostalAddress", "streetAddress": "1A impasse des Gatines", "postalCode": "44680", "addressLocality": "Sainte-Pazanne", "addressCountry": "FR"},
        "areaServed": [c for _, cs in p["zone_cols"] for c in cs],
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"], "opens": "07:00", "closes": "20:00"}],
        "sameAs": [SITE_CLIENT, FACEBOOK],
    }
    ld_faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faq"]]}
    ld = "".join(f'<script type="application/ld+json">{json.dumps(d, ensure_ascii=False)}</script>\n' for d in (ld_business, ld_faq))

    reass = "".join(f'<li>{I[ic]}<span>{t}</span></li>' for t, ic in p["reassurance"])
    services = "".join(f'''<article class="card{" card-wide" if sid == "renovation" else ""}" id="{sid}">
      <div class="card-icon">{I[ic]}</div>
      {f'<span class="tag">{tag}</span>' if tag else ''}
      <h3>{t}</h3><p>{d}</p>
      <a href="#devis" class="card-link">Demander un devis {I['ARROW']}</a>
    </article>''' for ic, t, d, tag, sid in p["services"])
    why = "".join(f'<div class="why-item"><div class="why-icon">{I[ic]}</div><div><h3>{t}</h3><p>{d}</p></div></div>' for ic, t, d in p["why"])
    steps = "".join(f'<li><span class="step-n">{n}</span><h3>{t}</h3><p>{d}</p></li>' for n, (t, d) in enumerate(p["process"], 1))
    ba = "".join(f'''<figure class="ba-wrap">
      <div class="ba" data-ba style="--pos:50%">
        <img src="{b}" alt="{ab}" loading="lazy" width="1000" height="740">
        <img src="{a}" alt="{aa}" loading="lazy" width="1000" height="740" class="ba-after">
        <input type="range" class="ba-range" min="0" max="100" value="50" aria-label="Comparer avant et après">
        <span class="ba-label ba-l">Avant</span><span class="ba-label ba-r">Après</span>
      </div>
      <figcaption>{cap}</figcaption>
    </figure>''' for b, a, cap, ab, aa in p["before_after"])
    gal = "".join(f'<figure><img src="{s}" alt="{a}" loading="lazy" width="900" height="700"></figure>' for s, a in p["gallery"])
    stars = I["STAR"] * 5
    reviews = "".join(f'<blockquote class="review"><div class="stars">{stars}</div><p>« {t} »</p><footer>{n}</footer></blockquote>' for n, t in p["reviews"])
    zone = "".join(f'<div class="zone-col"><h3>{I["PIN"]}{t}</h3><ul>{"".join(f"<li>{c}</li>" for c in cs)}</ul></div>' for t, cs in p["zone_cols"])
    faq = "".join(f'<details{" open" if i == 0 else ""}><summary>{q}</summary><p>{a}</p></details>' for i, (q, a) in enumerate(p["faq"]))

    body = f'''<a id="top"></a>
{header()}
<main>
<section class="hero">
  <img class="hero-bg" src="{p['hero_img']}" alt="{p['hero_alt']}" width="1600" height="900" fetchpriority="high">
  <div class="wrap hero-inner">
    <div class="hero-text">
      <span class="eyebrow light">Loire-Atlantique · Nord Vendée</span>
      <h1>{p['h1']}</h1>
      <p class="hero-sub">{p['sub']}</p>
      <div class="hero-ctas">
        <a href="#devis" class="btn btn-primary btn-lg">{I['ARROW']}Demander un devis gratuit</a>
        <a href="tel:{PHONE_INTL}" class="btn btn-ghost btn-lg">{I['PHONE']}{PHONE_DISPLAY}</a>
      </div>
      <ul class="reassurance">{reass}</ul>
    </div>
  </div>
</section>

<section class="section" id="services">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">{p['services_eyebrow']}</span>
      <h2>{p['services_h2']}</h2>
      <p class="lead">{p['services_lead']}</p>
    </div>
    <div class="cards">{services}</div>
  </div>
</section>

<section class="section section-sand" id="pourquoi">
  <div class="wrap why-grid">
    <div class="why-text">
      <span class="eyebrow">{p['why_eyebrow']}</span>
      <h2>{p['why_h2']}</h2>
      <p class="lead">{p['why_lead']}</p>
      <a href="#devis" class="btn btn-primary">{I['ARROW']}Demander un devis gratuit</a>
    </div>
    <div class="why-list">{why}</div>
  </div>
</section>

<section class="section" id="methode">
  <div class="wrap">
    <div class="section-head center">
      <span class="eyebrow">{p['process_eyebrow']}</span>
      <h2>{p['process_h2']}</h2>
    </div>
    <ol class="steps">{steps}</ol>
  </div>
</section>

<section class="section section-dark" id="realisations">
  <div class="wrap">
    <div class="section-head center">
      <span class="eyebrow gold">{p['gallery_eyebrow']}</span>
      <h2>{p['gallery_h2']}</h2>
      <p class="lead">{p['gallery_lead']}</p>
    </div>
    <div class="ba-grid">{ba}</div>
    <div class="gallery">{gal}</div>
  </div>
</section>

<section class="section" id="avis">
  <div class="wrap">
    <div class="section-head center">
      <span class="eyebrow">{p['reviews_eyebrow']}</span>
      <h2>{p['reviews_h2']}</h2>
    </div>
    <div class="reviews">{reviews}</div>
    <p class="reviews-note center">{p['reviews_note']}</p>
  </div>
</section>

<section class="section section-sand" id="zone">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">{p['zone_eyebrow']}</span>
      <h2>{p['zone_h2']}</h2>
      <p class="lead">{p['zone_lead']}</p>
    </div>
    <div class="zone-grid">{zone}</div>
  </div>
</section>

<section class="section" id="faq">
  <div class="wrap faq-wrap">
    <div class="section-head center">
      <span class="eyebrow">{p['faq_eyebrow']}</span>
      <h2>{p['faq_h2']}</h2>
    </div>
    <div class="faq">{faq}</div>
  </div>
</section>

<section class="section section-cta" id="devis">
  <div class="wrap cta-grid">
    <div class="cta-text">
      <span class="eyebrow gold">{p['cta_eyebrow']}</span>
      <h2>{p['cta_h2']}</h2>
      <p class="lead">{p['cta_lead']}</p>
      <div class="cta-contacts">
        <a href="tel:{PHONE_INTL}" class="cta-contact">{I['PHONE']}<span><strong>{PHONE_DISPLAY}</strong><small>{HOURS}</small></span></a>
        <a href="mailto:{EMAIL}" class="cta-contact">{I['MAIL']}<span><strong>{EMAIL}</strong><small>Réponse rapide par e-mail</small></span></a>
        <div class="cta-contact">{I['PIN']}<span><strong>Sainte-Pazanne (44)</strong><small>Déplacement dans toute la zone d'intervention</small></span></div>
      </div>
    </div>
    <div class="form-card">{form(p)}</div>
  </div>
</section>
</main>
{mobile_bar()}
{footer()}'''
    return head(p["title"], p["desc"], SITE + p["file"], p["hero_img"], ld, preload=p["hero_img"]) + body

# ---------------- Page merci ----------------
def build_merci():
    body = f'''<a id="top"></a>
{header()}
<main class="merci">
  <div class="wrap merci-inner">
    <div class="merci-icon">{I['CHECK']}</div>
    <h1>Merci, votre demande est bien reçue</h1>
    <p class="lead">Nous vous rappelons rapidement pour échanger sur votre projet et convenir d'une visite sur place. Besoin d'une réponse immédiate ? Appelez le <a href="tel:{PHONE_INTL}">{PHONE_DISPLAY}</a> ({HOURS}).</p>
    <a href="index.html" class="btn btn-primary">{I['ARROW']}Retour à la page</a>
  </div>
</main>
{footer()}'''
    return head("Merci – Demande envoyée | " + BRAND, "Votre demande de devis a bien été envoyée à " + BRAND + ".", SITE + "merci.html", PAGE["hero_img"]) + body

# ---------------- Écriture ----------------
os.chdir(os.path.dirname(os.path.abspath(__file__)))
open(PAGE["file"], "w", encoding="utf-8").write(build_lp(PAGE))
open("merci.html", "w", encoding="utf-8").write(build_merci())
open("robots.txt", "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE}sitemap.xml\n")
open("sitemap.xml", "w").write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n  <url><loc>{SITE}{PAGE["file"]}</loc><lastmod>{TODAY}</lastmod></url>\n</urlset>\n')
print("OK :", PAGE["file"], "merci.html, robots.txt, sitemap.xml —", "GTM " + (GTM_ID or "absent (commenté)"))
