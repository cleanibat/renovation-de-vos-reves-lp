# -*- coding: utf-8 -*-
"""Génère le site de La Rénovation de vos rêves : pages de service (aussi utilisées par Google Ads), pages locales,
guides, zones, pages légales, sitemap et robots. Contenus SEO dans seo_content.py.
Usage : python3 build.py
"""
import datetime, html, json, os

# ---------------- Configuration ----------------
GTM_ID = "GTM-T7MVZBMN"
SITE = "https://www.larenovationdevosreves.com/"  # domaine de production (canonical, sitemap, Open Graph)
BRAND = "La Rénovation de vos rêves"
PHONE_DISPLAY = "06 40 23 85 43"
PHONE_INTL = "+33640238543"
EMAIL = "contact@larenovationdevosreves.fr"
FORM_ACTION = "contact.php"  # formulaire HTML classique traité par le script serveur (hébergement PHP requis)
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
    LEVEL=ico('<path d="M3 17h18"/><path d="M3 21h18"/><path d="M12 3v10"/><path d="m8 9 4 4 4-4"/>'),
    LAYERS=ico('<path d="M3 21h18"/><path d="M5 21V11h14v10"/><path d="M3 11 12 4l9 7"/><path d="M5 16h14"/>'),
    GARAGE=ico('<path d="M3 21V9l9-5 9 5v12"/><path d="M7 21v-8h10v8"/><path d="M7 17h10"/>'),
    PIPE=ico('<path d="M2 8h6v8H2z"/><path d="M16 8h6v8h-6z"/><path d="M8 10h8M8 14h8"/>'),
    DROP=ico('<path d="M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11z"/>'),
    POOL=ico('<path d="M2 18c2 0 2-1.5 4-1.5S8 18 10 18s2-1.5 4-1.5 2 1.5 4 1.5 2-1.5 4-1.5"/><path d="M7 14V6a2 2 0 0 1 4 0M13 14V6a2 2 0 0 1 4 0M7 10h6"/>'),
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
    desc="Entreprise de maçonnerie et gros œuvre en Loire-Atlantique et nord Vendée : murs, ouvertures, dalles, extensions, terrassement. Devis gratuit.",
    hero_img="img/hero-maison-pierre-extension.jpg",
    hero_alt="Maison en pierre agrandie par une extension à toit plat, en Loire-Atlantique",
    hero_eyebrow="Loire-Atlantique · Littoral et presqu'île · Nord Vendée",
    h1='Maçonnerie générale et gros œuvre <em>en Loire-Atlantique</em>',
    sub="Murs, dalles, ouvertures dans les murs porteurs, extensions et surélévations, terrassement, rénovation clé en main : nous réalisons vos travaux de maçonnerie en Loire-Atlantique, sur le littoral et la presqu'île, et dans le nord de la Vendée, avec un seul interlocuteur du devis à la réception du chantier.",
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
        ("DIGGER", "Terrassement et assainissement", "Préparation du terrain, décaissement et nivellement, fouilles pour fondations, mise en place ou remplacement de l'assainissement individuel.", "", "terrassement"),
        ("TROWEL", "Reprise et rejointoiement", "Reprise de maçonnerie ancienne, rejointoiement de murs en pierre, finitions, démolition et préparation de chantier avant rénovation lourde.", "Bâti ancien", "reprise"),
        ("HOME", "Rénovation clé en main", "Rénovation complète de maisons, d'appartements et de granges : gros œuvre, second œuvre, isolation, électricité, plomberie, cuisines et salles de bains. Un seul interlocuteur du premier rendez-vous à la remise des clés.", "Du gros œuvre aux finitions", "renovation"),
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
    zone_h2="Loire-Atlantique, littoral et presqu'île, nord de la Vendée",
    zone_lead="Installés à Sainte-Pazanne, nous intervenons dans toute la Loire-Atlantique, sur le littoral et la presqu'île guérandaise, et dans le nord de la Vendée, chez les particuliers, les professionnels et les collectivités.",
    zone_cols=[
        ("Nantes et agglomération", ["Nantes", "Rezé", "Saint-Herblain", "Vertou", "Bouguenais", "Clisson", "Nort-sur-Erdre", "Sainte-Pazanne", "Machecoul-Saint-Même"]),
        ("Littoral et presqu'île", ["Saint-Nazaire", "Guérande", "La Baule-Escoublac", "Pornichet", "Saint-Brevin-les-Pins", "Pornic", "La Bernerie-en-Retz", "La Plaine-sur-Mer", "Saint-Michel-Chef-Chef", "Le Pouliguen", "Le Croisic", "Batz-sur-Mer", "La Turballe"]),
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

RENO_CARD = PAGE["services"][-1]

# ---------------- Contenu de la LP Extension et surélévation ----------------
EXTENSION = dict(PAGE,
    file="extension.html",
    lp="Extension",
    title="Extension de maison en Loire-Atlantique | La Rénovation de vos rêves",
    desc="Extension de maison, surélévation, garage ou annexe en Loire-Atlantique et nord Vendée. Du gros œuvre aux finitions, un seul interlocuteur. Devis gratuit.",
    hero_img="img/hero-extension-maison.jpg",
    hero_alt="Maison agrandie par une extension avec terrasse, en Loire-Atlantique",
    h1='Extension et surélévation de maison <em>en Loire-Atlantique</em>',
    sub="Extension de plain-pied, surélévation, garage ou annexe : nous réalisons votre agrandissement du gros œuvre aux finitions, en continuité avec votre maison, en Loire-Atlantique, sur le littoral et la presqu'île, et dans le nord de la Vendée.",
    services_eyebrow="Nos travaux d'agrandissement",
    services_h2="Agrandir votre maison, du gros œuvre aux finitions",
    services_lead="Une pièce de vie, une chambre, un étage ou un garage en plus : nous construisons votre agrandissement et le raccordons à l'existant.",
    services=[
        ("HOUSEPLUS", "Extension de plain-pied", "Agrandissement latéral ou sur l'arrière de la maison : pièce de vie, suite parentale, cuisine ouverte ou bureau, à toit plat ou à toiture traditionnelle.", "Le plus demandé", "plain-pied"),
        ("LAYERS", "Surélévation de maison", "Création d'un étage ou rehausse de la toiture pour gagner des mètres carrés sans réduire le terrain, avec dépose et reprise de la couverture.", "Gain de surface", "surelevation"),
        ("GARAGE", "Garage et annexe", "Construction d'un garage accolé ou indépendant, d'un atelier, d'une dépendance ou d'un studio de jardin.", "", "garage"),
        ("SLAB", "Fondations et dalle", "Terrassement, fondations et dalle béton de l'extension, adaptés au terrain et à la construction existante.", "", "fondations"),
        ("DOOR", "Ouverture vers l'existant", "Création de l'ouverture entre la maison et l'extension : étaiement, pose de linteau ou de poutre métallique, reprise des finitions.", "Mur porteur", "ouverture"),
        ("TROWEL", "Couverture et finitions", "Couverture, menuiseries extérieures, isolation, enduits, sols et raccords intérieurs : l'extension est livrée terminée.", "Clé en main", "finitions"),
        RENO_CARD,
    ],
    why_lead="Nous intervenons de la conception à la réception des travaux, sur des chantiers d'extension, de surélévation et de construction d'annexes.",
    gallery=[
        ("img/extension-maison.jpg", "Extension contemporaine accolée à une maison"),
        ("img/extension-bois-maison-pierre.jpg", "Extension à toit plat sur une maison en pierre"),
        ("img/maison-pierre-jardin.jpg", "Maison en pierre avec son jardin"),
        ("img/mur-pierre-interieur.jpg", "Pièce de vie ouverte sur un mur en pierre apparente"),
    ],
    faq=[
        ("Faut-il un permis de construire pour une extension ?",
         "Cela dépend de la surface créée et de la commune. En règle générale, une déclaration préalable de travaux suffit jusqu'à 20 m², ou jusqu'à 40 m² en zone urbaine couverte par un plan local d'urbanisme. Au-delà, un permis de construire est nécessaire, et le recours à un architecte devient obligatoire si la surface totale de la maison dépasse 150 m² après travaux. Nous vous indiquons la démarche à suivre lors de la visite."),
        ("Combien coûte une extension ou une surélévation ?",
         "Le prix dépend de la surface, du type d'agrandissement (plain-pied ou étage), des matériaux, du niveau de finition et de l'accès au chantier. Nous nous déplaçons avant de chiffrer : le devis est gratuit, détaillé poste par poste, et sans engagement."),
        ("Peut-on rester dans la maison pendant les travaux ?",
         "Pour une extension de plain-pied, oui dans la plupart des cas : le gros œuvre se fait à l'extérieur et l'ouverture vers la maison est réalisée en fin de chantier. Pour une surélévation, la toiture est déposée par étapes et protégée ; nous voyons avec vous lors de la visite les périodes où certaines pièces ne seront pas utilisables."),
        ("Ma maison peut-elle être surélevée ?",
         "Cela dépend des murs et des fondations existants, de la charpente et des règles d'urbanisme de votre commune (hauteur maximale). Nous regardons ces points sur place lors de la première visite et vous disons ce qui est réalisable."),
        ("Combien de temps durent les travaux ?",
         "La durée dépend de la surface et du niveau de finition. Le planning du chantier, avec la date de démarrage et les grandes étapes, vous est remis avec le devis."),
        ("L'extension sera-t-elle assortie à ma maison ?",
         "Oui. Nous reprenons les matériaux, les enduits et les pentes de toiture de l'existant, ou proposons un contraste assumé (toit plat, bardage) selon votre souhait et ce que permet le règlement d'urbanisme."),
    ],
    cta_lead="Décrivez votre projet d'agrandissement en quelques lignes, nous vous rappelons pour convenir d'une visite sur place.",
    form_needs=["Extension de plain-pied", "Surélévation", "Garage ou annexe", "Extension et rénovation de l'existant", "Rénovation clé en main", "Autre projet"],
    form_msg_ph="Surface souhaitée, usage de la pièce, type de maison, accès au terrain, délai souhaité…",
)

# ---------------- Contenu de la LP Terrassement ----------------
TERRASSEMENT = dict(PAGE,
    file="terrassement.html",
    lp="Terrassement",
    title="Terrassement en Loire-Atlantique | La Rénovation de vos rêves",
    desc="Terrassement de maison, garage, extension ou piscine, décaissement, fouilles et assainissement individuel en Loire-Atlantique et nord Vendée. Devis gratuit.",
    hero_img="img/hero-terrassement-piscine.jpg",
    hero_alt="Jardin aménagé avec piscine et terrasse après terrassement",
    h1='Terrassement et assainissement <em>en Loire-Atlantique</em>',
    sub="Préparation de terrain, décaissement et nivellement, fouilles et fondations, assainissement individuel, terrassement de piscine : nous réalisons vos travaux de terrassement en Loire-Atlantique, sur le littoral et la presqu'île, et dans le nord de la Vendée.",
    reassurance=[
        ("Devis gratuit et sans engagement", "DOC"),
        ("Visite sur place et devis détaillé écrit", "PIN"),
        ("Un seul interlocuteur du début à la fin", "USER"),
        ("Terres évacuées, terrain rendu propre", "BROOM"),
    ],
    services_eyebrow="Nos travaux de terrassement",
    services_h2="Préparer votre terrain avant de construire",
    services_lead="Pour une maison, un garage, une extension, une piscine ou une mise aux normes de l'assainissement, chez les particuliers, les professionnels et les collectivités.",
    services=[
        ("DIGGER", "Terrassement de maison, garage ou extension", "Décapage de la terre végétale, mise à niveau et plateforme prête à recevoir les fondations de votre construction.", "Le plus demandé", "plateforme"),
        ("SLAB", "Fouilles et fondations", "Fouilles en rigole ou en pleine masse, coulage des fondations et de la dalle béton à la suite du terrassement.", "", "fouilles"),
        ("LEVEL", "Décaissement et nivellement", "Décaissement et mise à niveau du terrain pour une terrasse, une allée, un abri de jardin ou un aménagement extérieur.", "", "decaissement"),
        ("DROP", "Assainissement", "Mise en place ou remplacement d'un assainissement individuel, en lien avec le contrôle du SPANC de votre commune.", "Mise aux normes", "assainissement"),
        ("POOL", "Terrassement de piscine", "Creusement du bassin, évacuation des terres, préparation du fond de fouille et des abords avant la pose ou la construction de la piscine.", "", "piscine"),
        ("TROWEL", "Démolition et évacuation", "Démolition d'ouvrages existants, enlèvement des gravats et des terres, remise en état du terrain en fin de chantier.", "", "demolition"),
        RENO_CARD,
    ],
    why_lead="Nous intervenons de la préparation du terrain à la réception des travaux, sur des chantiers de terrassement, d'assainissement et de gros œuvre.",
    process=[
        ("Prise de contact", "Vous nous appelez ou remplissez le formulaire. Nous échangeons sur votre projet, votre terrain et vos délais."),
        ("Visite et devis", "Nous nous déplaçons sur place pour voir le terrain, la pente, la nature du sol et l'accès, puis vous remettons un devis détaillé et gratuit."),
        ("Planification", "Une fois le devis signé, nous planifions les travaux, préparons les démarches si nécessaire et fixons avec vous la date de démarrage."),
        ("Chantier et réception", "Nous réalisons le terrassement, évacuons les terres et vous rendons un terrain propre, prêt pour la suite des travaux."),
    ],
    gallery_h2="Aménagements réalisés",
    gallery_lead="",
    before_after=[],
    gallery=[
        ("img/hero-terrassement-piscine.jpg", "Piscine et terrasse dans un jardin aménagé"),
        ("img/piscine-terrasse-bois.jpg", "Piscine avec terrasse en bois"),
        ("img/facade-pierre-allee.jpg", "Allée dallée le long d'une façade en pierre"),
        ("img/apres-maison.jpg", "Extension et terrasse sur une maison en pierre"),
    ],
    faq=[
        ("Faut-il une autorisation pour des travaux de terrassement ?",
         "Un terrassement lié à une construction est couvert par le permis de construire ou la déclaration préalable du projet. Pour l'assainissement individuel, le service public d'assainissement non collectif (SPANC) de votre commune doit valider le projet puis contrôler l'installation. Nous vous indiquons la démarche à suivre lors de la visite."),
        ("Combien coûte un terrassement ?",
         "Le prix dépend du volume de terre à déplacer, de la nature du sol, de la pente, de l'accès au terrain et de l'évacuation des terres. Nous nous déplaçons avant de chiffrer : le devis est gratuit, détaillé poste par poste, et sans engagement."),
        ("Mon terrain est en pente ou difficile d'accès, pouvez-vous intervenir ?",
         "Oui. Nous regardons sur place la pente, la largeur du passage et la portance du sol, et adaptons le matériel et l'organisation du chantier à votre terrain."),
        ("Que deviennent les terres et les gravats ?",
         "Les terres excavées sont réutilisées sur place en remblai lorsque c'est possible, ou évacuées vers une filière adaptée. Les gravats de démolition sont triés et déposés en déchetterie professionnelle. L'évacuation est prévue dans le devis."),
        ("À quelle période terrasser ?",
         "Un terrassement se fait toute l'année, mais un sol sec facilite le travail et limite les ornières. Après de fortes pluies, nous pouvons décaler le démarrage de quelques jours pour préserver votre terrain."),
        ("Travaillez-vous pour les professionnels et les collectivités ?",
         "Oui. Nous réalisons des travaux de terrassement et d'assainissement individuel pour les particuliers, les entreprises et les collectivités, avec les mêmes étapes : visite, devis détaillé, planification, chantier et réception."),
    ],
    cta_lead="Décrivez votre terrain et votre projet en quelques lignes, nous vous rappelons pour convenir d'une visite sur place.",
    form_needs=["Terrassement pour maison, garage ou extension", "Fouilles et fondations", "Décaissement, nivellement", "Assainissement individuel", "Terrassement de piscine", "Démolition, évacuation", "Autre projet"],
    form_msg_ph="Type de projet, surface ou volume approximatif, pente, accès au terrain, délai souhaité…",
)

PAGES = [PAGE, EXTENSION, TERRASSEMENT]

# ---------------- SEO : villes, guides, données géographiques ----------------
# Structure inspirée d'artipierre.fr (positionné en moins de 7 jours) : adresses propres sans .html, pages service × ville,
# pages département, titres « Service Ville (44) — … », maillage interne dense (villes voisines, autres services, pied de page).
import math, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seo_content import CITIES, GUIDES, SECTEUR_TXT

HERE = os.path.dirname(os.path.abspath(__file__))
_COMMUNES = json.load(open(os.path.join(HERE, "ads", "communes.json"), encoding="utf-8"))
_RAYONS = json.load(open(os.path.join(HERE, "ads", "rayons.json"), encoding="utf-8"))
_IDX = {(c["nom"], c["dep"]): c for c in _COMMUNES}

def _dist(a, b):
    la1, lo1 = map(math.radians, a); la2, lo2 = map(math.radians, b)
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 12742 * math.asin(math.sqrt(h))

def _in_zone(c):
    return any(_dist((c["lat"], c["lon"]), (la, lo)) <= r for la, lo, r in _RAYONS)

_HOME = _IDX[("Sainte-Pazanne", "44")]
CITY_BY_NAME = {c["nom"]: c for c in CITIES}
for c in CITIES:
    x = _IDX[(c["nom"], c["dep"])]
    c["km"] = round(_dist((_HOME["lat"], _HOME["lon"]), (x["lat"], x["lon"])))
    c["xy"] = (x["lat"], x["lon"])
    for radius in (12, 16, 20):
        near = [y for y in _COMMUNES if y["dep"] in ("44", "85") and y is not x and _in_zone(y)
                and _dist((x["lat"], x["lon"]), (y["lat"], y["lon"])) <= radius]
        if len(near) >= 5: break
    c["near"] = [y["nom"] for y in sorted(near, key=lambda y: -y["pop"])[:8]]
    # villes de notre liste les plus proches (pour le maillage « Autour de … »)
    c["near_pages"] = [o["nom"] for o in sorted((o for o in CITIES if o is not c), key=lambda o: _dist(c["xy"] if "xy" in c else (x["lat"], x["lon"]), (_IDX[(o["nom"], o["dep"])]["lat"], _IDX[(o["nom"], o["dep"])]["lon"])))[:6]]

SECTEURS = ["Nantes et agglomération", "Vignoble nantais", "Estuaire et Brière", "Littoral et presqu'île", "Pays de Retz", "Nord Vendée"]
DEPTS = {"44": ("Loire-Atlantique", "macon-loire-atlantique"), "85": ("Vendée", "macon-vendee")}

# Services déclinés par ville : préfixe d'adresse, libellé, page de service
SVC = {
    "macon": dict(prefix="macon", label="Maçon", service_file="index.html", service_name="Maçonnerie générale"),
    "extension": dict(prefix="extension-maison", label="Extension de maison", service_file="extension-maison.html", service_name="Extension et surélévation"),
    "terrassement": dict(prefix="terrassement", label="Terrassement", service_file="terrassement.html", service_name="Terrassement"),
}
def city_file(c, svc="macon"):
    return f"{SVC[svc]['prefix']}-{c['slug']}.html"

for g in GUIDES:
    g["file"] = f"{g['slug']}.html"

# ---------------- Adresses propres ----------------
# Les fichiers restent en .html sur le serveur ; .htaccess sert /page → page.html et redirige /page.html → /page.
# Exceptions : index (→ /), extension.html et terrassement.html (adresses finales Google Ads, jamais redirigées).
CANONICAL_OVERRIDE = {"index.html": "", "extension.html": "extension-maison"}

def slug_of(file):
    if file in CANONICAL_OVERRIDE: return CANONICAL_OVERRIDE[file]
    return file[:-5] if file.endswith(".html") else file

def href(file):
    s = slug_of(file)
    return "./" if s == "" else s

def url_of(file):
    return SITE + slug_of(file)

def city_link(nom, svc="macon"):
    c = CITY_BY_NAME.get(nom)
    return f'<a href="{href(city_file(c, svc))}">{html.escape(nom)}</a>' if c else html.escape(nom)

# ---------------- Images : WebP + repli JPEG ----------------
def make_webp():
    try:
        from PIL import Image
    except ImportError:
        return
    for f in os.listdir(os.path.join(HERE, "img")):
        if not f.endswith(".jpg"): continue
        src = os.path.join(HERE, "img", f); base = src[:-4]
        if not os.path.exists(base + ".webp") or os.path.getmtime(base + ".webp") < os.path.getmtime(src):
            Image.open(src).convert("RGB").save(base + ".webp", "WEBP", quality=78, method=6)
        if not os.path.exists(base + "-800.webp"):
            im = Image.open(src).convert("RGB")
            if im.width > 800:
                im.resize((800, round(im.height * 800 / im.width)), Image.LANCZOS).save(base + "-800.webp", "WEBP", quality=76, method=6)

_SIZES = {}
def _size(name, w, h):
    if name not in _SIZES:
        try:
            from PIL import Image
            _SIZES[name] = Image.open(os.path.join(HERE, "img", name + ".jpg")).size
        except Exception:
            _SIZES[name] = (w, h)
    return _SIZES[name]

def pic(name, alt, w=1200, h=800, cls="", lazy=True, hero=False):
    w, h = _size(name, w, h)
    if hero and os.path.exists(os.path.join(HERE, "img", f"{name}-800.webp")):
        source = f'<source type="image/webp" srcset="img/{name}-800.webp 800w, img/{name}.webp {w}w" sizes="100vw">'
    else:
        source = f'<source type="image/webp" srcset="img/{name}.webp">'
    attrs = f' class="{cls}"' if cls else ""
    load = ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"'
    return f'<picture>{source}<img src="img/{name}.jpg" alt="{html.escape(alt)}" width="{w}" height="{h}"{attrs}{load}></picture>'

def preload_hero(name):
    w = _size(name, 1200, 800)[0]
    if os.path.exists(os.path.join(HERE, "img", f"{name}-800.webp")):
        return f'<link rel="preload" as="image" type="image/webp" href="img/{name}.webp" imagesrcset="img/{name}-800.webp 800w, img/{name}.webp {w}w" imagesizes="100vw" fetchpriority="high">'
    return f'<link rel="preload" as="image" type="image/webp" href="img/{name}.webp" fetchpriority="high">'

def img_name(path):
    return path.split("/")[-1].rsplit(".", 1)[0]

# ---------------- Blocs communs ----------------
def gtm_head():
    s = "<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);})(window,document,'script','dataLayer','%s');</script>" % (GTM_ID or "GTM-XXXXXXX")
    return "<!-- Google Tag Manager -->\n" + (s if GTM_ID else "<!-- " + s + " -->") + "\n<!-- End Google Tag Manager -->"

def gtm_body():
    s = '<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=%s" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>' % (GTM_ID or "GTM-XXXXXXX")
    return s if GTM_ID else "<!-- " + s + " -->"

def ld_json(*objs):
    return "".join(f'<script type="application/ld+json">{json.dumps(o, ensure_ascii=False)}</script>\n' for o in objs if o)

def ld_breadcrumb(items):
    crumbs = [("Accueil", "index.html")] + items
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": url_of(f)} for i, (n, f) in enumerate(crumbs)]}

LD_BUSINESS_ID = SITE + "#entreprise"
def ld_business(area=None):
    return {
        "@context": "https://schema.org", "@type": "HomeAndConstructionBusiness", "@id": LD_BUSINESS_ID, "name": BRAND,
        "url": SITE, "telephone": PHONE_INTL, "email": EMAIL, "image": SITE + "img/hero-maison-pierre-extension.jpg",
        "logo": SITE + "img/logo-renovation-de-vos-reves.png",
        "address": {"@type": "PostalAddress", "streetAddress": "1A impasse des Gatines", "postalCode": "44680", "addressLocality": "Sainte-Pazanne", "addressRegion": "Pays de la Loire", "addressCountry": "FR"},
        "geo": {"@type": "GeoCoordinates", "latitude": round(_HOME["lat"], 4), "longitude": round(_HOME["lon"], 4)},
        "areaServed": area or ([{"@type": "AdministrativeArea", "name": "Loire-Atlantique"}, {"@type": "AdministrativeArea", "name": "Vendée"}] + [{"@type": "City", "name": c["nom"]} for c in CITIES]),
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"], "opens": "07:00", "closes": "20:00"}],
        "sameAs": [SITE_CLIENT, FACEBOOK], "taxID": SIRET.replace(" ", ""),
    }

def head(title, desc, file, og_img="img/hero-maison-pierre-extension.jpg", extra_ld="", noindex=False, preload=""):
    robots = "noindex, follow" if noindex else "index, follow, max-image-preview:large"
    canonical = url_of(file)
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
<meta property="og:site_name" content="{BRAND}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:image" content="{SITE}{og_img}">
<meta property="og:url" content="{canonical}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#141e4f">
<meta name="geo.region" content="FR-44">
<meta name="geo.placename" content="Sainte-Pazanne">
<link rel="icon" href="img/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="img/apple-touch-icon.png">
{preload}
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

NAV = [("index.html", "Maçonnerie"), ("extension-maison.html", "Extension"), ("terrassement.html", "Terrassement"),
       ("zones-intervention.html", "Zones"), ("conseils.html", "Conseils")]

def header(current="", devis="#devis"):
    nav = "".join(f'<a href="{href(f)}"{" aria-current=" + chr(34) + "page" + chr(34) if f == current else ""}>{t}</a>' for f, t in NAV)
    return f'''<header class="header">
  <div class="wrap">
    <a class="logo" href="./" aria-label="{BRAND}, accueil"><img src="img/logo-clair.png" alt="{BRAND}" width="513" height="164"></a>
    <nav class="main-nav" aria-label="Navigation principale">{nav}</nav>
    <div class="header-cta">
      <a class="header-phone" href="tel:{PHONE_INTL}">{I['PHONE']}<span><small>Appelez-nous</small>{PHONE_DISPLAY}</span></a>
      <a class="btn btn-primary" href="{devis}">Devis gratuit</a>
    </div>
  </div>
</header>
'''

def mobile_bar(devis="#devis"):
    return f'''<div class="mobile-bar">
  <a href="tel:{PHONE_INTL}" class="btn btn-outline">{I['PHONE']}Appeler</a>
  <a href="{devis}" class="btn btn-primary">Devis gratuit</a>
</div>
'''

def breadcrumb(items, wrap=True):
    crumbs = [("Accueil", "index.html")] + list(items[:-1])
    parts = "".join(f'<li><a href="{href(f)}">{html.escape(n)}</a></li>' for n, f in crumbs)
    return f'<nav class="breadcrumb{" wrap" if wrap else ""}" aria-label="Fil d\'Ariane"><ol>{parts}<li aria-current="page">{html.escape(items[-1][0])}</li></ol></nav>'

def footer():
    city_cols = ""
    for sect in SECTEURS:
        cs = [c for c in CITIES if c["secteur"] == sect]
        city_cols += f'<p class="footer-sect">{sect}</p><p class="footer-cities">' + " · ".join(f'<a href="{href(city_file(c))}">{html.escape(c["nom"])}</a>' for c in cs) + "</p>"
    guides = "".join(f'<li><a href="{href(g["file"])}">{html.escape(g["title"])}</a></li>' for g in GUIDES)
    return f'''<footer class="footer">
  <div class="wrap footer-grid">
    <div>
      <img src="img/logo-renovation-de-vos-reves.png" alt="{BRAND}" width="513" height="164" class="footer-logo" loading="lazy">
      <p class="footer-role">Entreprise du bâtiment à Sainte-Pazanne · Maçonnerie, gros œuvre, extension, terrassement et rénovation clé en main</p>
      <p><a href="tel:{PHONE_INTL}">{PHONE_DISPLAY}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a><br>{HOURS}</p>
      <p>{ADDRESS}<br>SIRET {SIRET}</p>
      <p><a href="{FACEBOOK}" rel="noopener" class="fb">{I['FB']}Facebook</a></p>
    </div>
    <div>
      <h3>Nos services</h3>
      <ul class="footer-list"><li><a href="./">Maçonnerie générale</a></li><li><a href="{href('extension-maison.html')}">Extension et surélévation</a></li><li><a href="{href('terrassement.html')}">Terrassement et assainissement</a></li><li><a href="./#renovation">Rénovation clé en main</a></li></ul>
      <h3>Départements</h3>
      <ul class="footer-list"><li><a href="{href('macon-loire-atlantique.html')}">Maçon en Loire-Atlantique</a></li><li><a href="{href('macon-vendee.html')}">Maçon en Vendée</a></li></ul>
      <h3>Conseils</h3>
      <ul class="footer-list">{guides}</ul>
    </div>
    <div class="footer-zones">
      <h3><a href="{href('zones-intervention.html')}">Zones d'intervention</a></h3>
      {city_cols}
    </div>
  </div>
  <div class="wrap footer-bottom">
    <p>© <span id="year">{YEAR}</span> {BRAND} · <a href="{href('mentions-legales.html')}">Mentions légales</a> · <a href="{href('confidentialite.html')}">Confidentialité</a></p>
  </div>
</footer>
<script src="main.js" defer></script>
</body>
</html>
'''

ATTR_FIELDS = ["gclid", "gbraid", "wbraid", "fbclid", "msclkid", "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content", "referrer", "landing_page"]

def form(p):
    opts = "".join(f'<option value="{html.escape(o)}">{html.escape(o)}</option>' for o in p["form_needs"])
    hidden = "".join(f'<input type="hidden" name="{k}" value="">' for k in ATTR_FIELDS)
    city_val = f' value="{html.escape(p["city_value"])}"' if p.get("city_value") else ""
    return f'''<form id="devisForm" class="form" action="{FORM_ACTION}" method="POST">
  <input type="hidden" name="Source" value="{html.escape(p.get('source_label', 'LP ' + p['lp']))}">
  {hidden}
  <input type="text" name="_honey" class="honeypot" tabindex="-1" autocomplete="off" aria-hidden="true">
  <div class="grid-2">
    <label>Nom et prénom<input type="text" name="Nom" required autocomplete="name" placeholder="Jean Dupont"></label>
    <label>Téléphone<input type="tel" name="Téléphone" required autocomplete="tel" placeholder="06 12 34 56 78"></label>
    <label>E-mail<input type="email" name="Email" required autocomplete="email" placeholder="jean.dupont@exemple.fr"></label>
    <label>Commune du chantier<input type="text" name="Localité" required autocomplete="address-level2" placeholder="Nantes, Saint-Nazaire, Guérande…"{city_val}></label>
  </div>
  <label>Votre besoin<select name="Besoin" required><option value="" disabled selected>Choisir…</option>{opts}</select></label>
  <label>Décrivez votre projet (facultatif)<textarea name="Message" rows="4" placeholder="{html.escape(p['form_msg_ph'])}"></textarea></label>
  <button type="submit" class="btn btn-primary btn-block" data-sending="Envoi…">{I['ARROW']}Envoyer ma demande de devis</button>
  <p class="form-note">{I['SHIELD']}Vos données restent confidentielles et servent uniquement à traiter votre demande. Aucune revente, aucun démarchage. <a href="{href('confidentialite.html')}">En savoir plus</a></p>
</form>'''

def cta_section(p):
    return f'''<section class="section section-cta" id="devis">
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
</section>'''

# ---------------- Page de service ou page locale ----------------
def build_lp(p):
    hero = img_name(p["hero_img"])
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}} for q, a in p["faq"]]}
    lds = [ld_business(), faq_ld]
    if p["file"] != "index.html":
        lds.append(ld_breadcrumb(p["crumbs"]))
    if p.get("service_ld"):
        lds.append(p["service_ld"])
    svc_links = p.get("zone_svc", "macon")

    reass = "".join(f'<li>{I[ic]}<span>{t}</span></li>' for t, ic in p["reassurance"])
    def card(svc):
        ic, t, d, tag, sid = svc[:5]
        link = svc[5] if len(svc) > 5 else "#devis"
        link_txt = "En savoir plus" if len(svc) > 5 else "Demander un devis"
        return f'''<article class="card{" card-wide" if sid == "renovation" else ""}" id="{sid}">
      <div class="card-icon">{I[ic]}</div>
      {f'<span class="tag">{tag}</span>' if tag else ''}
      <h3>{t}</h3><p>{d}</p>
      <a href="{link}" class="card-link">{link_txt} {I['ARROW']}</a>
    </article>'''
    services = "".join(card(s) for s in p["services"])
    why = "".join(f'<div class="why-item"><div class="why-icon">{I[ic]}</div><div><h3>{t}</h3><p>{d}</p></div></div>' for ic, t, d in p["why"])
    steps = "".join(f'<li><span class="step-n">{n}</span><h3>{t}</h3><p>{d}</p></li>' for n, (t, d) in enumerate(p["process"], 1))
    ba = "".join(f'''<figure class="ba-wrap">
      <div class="ba" data-ba style="--pos:50%">
        {pic(img_name(b), ab)}
        {pic(img_name(a), aa, cls="ba-after")}
        <input type="range" class="ba-range" min="0" max="100" value="50" aria-label="Comparer avant et après">
        <span class="ba-label ba-l">Avant</span><span class="ba-label ba-r">Après</span>
      </div>
      <figcaption>{cap}</figcaption>
    </figure>''' for b, a, cap, ab, aa in p["before_after"])
    gal = "".join(f'<figure>{pic(img_name(s), a)}</figure>' for s, a in p["gallery"])
    stars = I["STAR"] * 5
    reviews = "".join(f'<blockquote class="review"><div class="stars">{stars}</div><p>« {t} »</p><footer>{n}</footer></blockquote>' for n, t in p["reviews"])
    zone = "".join(f'<div class="zone-col"><h3>{I["PIN"]}{t}</h3><ul>{"".join(f"<li>{city_link(c, svc_links)}</li>" for c in cs)}</ul></div>' for t, cs in p["zone_cols"])
    faq = "".join(f'<details{" open" if i == 0 else ""}><summary>{q}</summary><p>{a}</p></details>' for i, (q, a) in enumerate(p["faq"]))
    crumbs = breadcrumb(p["crumbs"]) if p["file"] != "index.html" else ""
    zone_link = f'<p class="zone-more"><a href="{href("zones-intervention.html")}">Voir toutes nos zones d\'intervention</a></p>'
    why_section = "" if p.get("hide_why") else f'''<section class="section section-sand" id="pourquoi">
  <div class="wrap why-grid">
    <div class="why-text">
      <span class="eyebrow">{p['why_eyebrow']}</span>
      <h2>{p['why_h2']}</h2>
      <p class="lead">{p['why_lead']}</p>
      <a href="#devis" class="btn btn-primary">{I['ARROW']}Demander un devis gratuit</a>
    </div>
    <div class="why-list">{why}</div>
  </div>
</section>'''
    steps_section = "" if p.get("hide_steps") else f'''<section class="section" id="methode">
  <div class="wrap">
    <div class="section-head center">
      <span class="eyebrow">{p['process_eyebrow']}</span>
      <h2>{p['process_h2']}</h2>
    </div>
    <ol class="steps">{steps}</ol>
  </div>
</section>'''
    zone_section = "" if p.get("hide_zone") else f'''<section class="section section-sand" id="zone">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">{p['zone_eyebrow']}</span>
      <h2>{p['zone_h2']}</h2>
      <p class="lead">{p['zone_lead']}</p>
    </div>
    <div class="zone-grid">{zone}</div>
    {zone_link}
  </div>
</section>'''

    body = f'''<a id="top"></a>
{header(p.get("nav_current", p["file"]))}
<main>
<section class="hero">
  {pic(hero, p['hero_alt'], cls="hero-bg", lazy=False, hero=True)}
  <div class="wrap hero-inner">
    <div class="hero-text">
      <span class="eyebrow light">{p['hero_eyebrow']}</span>
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
{crumbs}
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
{p.get('local_html', '')}
{why_section}

{steps_section}

<section class="section section-dark" id="realisations">
  <div class="wrap">
    <div class="section-head center">
      <span class="eyebrow gold">{p['gallery_eyebrow']}</span>
      <h2>{p['gallery_h2']}</h2>
      {f"<p class='lead'>{p['gallery_lead']}</p>" if p['gallery_lead'] else ""}
    </div>
    {f'<div class="ba-grid">{ba}</div>' if ba else ""}
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

{zone_section}

<section class="section" id="faq">
  <div class="wrap faq-wrap">
    <div class="section-head center">
      <span class="eyebrow">{p['faq_eyebrow']}</span>
      <h2>{p['faq_h2']}</h2>
    </div>
    <div class="faq">{faq}</div>
  </div>
</section>

{cta_section(p)}
</main>
{mobile_bar()}
{footer()}'''
    return head(p["title"], p["desc"], p["file"], p["hero_img"], ld_json(*lds), preload=preload_hero(hero)) + body

import re

# ---------------- Pages de service ----------------
EXTENSION["file"] = "extension-maison.html"
SERVICE_INFO = {
    "index.html": ("Maçonnerie générale", "Maçonnerie générale et gros œuvre", "macon"),
    "extension-maison.html": ("Extension et surélévation", "Extension et surélévation de maison", "extension"),
    "terrassement.html": ("Terrassement", "Terrassement et assainissement individuel", "terrassement"),
}
for p in PAGES:
    name, svc, key = SERVICE_INFO[p["file"]]
    p["crumbs"] = [(name, p["file"])]
    p["zone_svc"] = key
    p["zone_cols"] = [(sect, [c["nom"] for c in CITIES if c["secteur"] == sect]) for sect in SECTEURS]
    p["zone_h2"] = "Loire-Atlantique, littoral et presqu'île, nord de la Vendée"
    p["service_ld"] = {"@context": "https://schema.org", "@type": "Service", "serviceType": svc, "name": svc + " en Loire-Atlantique",
                       "provider": {"@id": LD_BUSINESS_ID}, "areaServed": [{"@type": "City", "name": c["nom"]} for c in CITIES],
                       "url": url_of(p["file"])}
for p in PAGES:  # les cartes des pages de service renvoient aux autres services
    pass

# Descriptions courtes des cartes sur les pages ville (le détail est sur les pages de service)
SHORT_CARD = {
    "Maçonnerie générale": "Murs, dalles, fondations, ouvertures et reprise de murs anciens.",
    "Extension de plain-pied": "Pièce de vie, suite parentale ou bureau dans le prolongement de la maison.",
    "Surélévation de maison": "Un étage de plus sans réduire le jardin.",
    "Garage et annexe": "Garage accolé ou indépendant, atelier, dépendance.",
    "Fondations et dalle": "Terrassement, fondations et dalle de l'extension.",
    "Ouverture vers l'existant": "Liaison entre la maison et l'extension, linteau ou poutre.",
    "Couverture et finitions": "Extension livrée terminée, couverture et finitions comprises.",
    "Rénovation clé en main": "Gros œuvre, second œuvre et finitions avec un seul interlocuteur.",
    "Terrassement de maison, garage ou extension": "Plateforme prête à recevoir les fondations.",
    "Fouilles et fondations": "Fouilles, fondations et dalle béton à la suite du terrassement.",
    "Décaissement et nivellement": "Terrasse, allée, abri de jardin, aménagement extérieur.",
    "Assainissement": "Assainissement individuel, en lien avec le SPANC.",
    "Terrassement de piscine": "Creusement du bassin, évacuation des terres, abords.",
    "Démolition et évacuation": "Démolition, enlèvement des gravats, remise en état.",
}
def short_cards(cards):
    out = []
    for c in cards:
        t = re.sub(r" à .*$", "", c[1])
        d = SHORT_CARD.get(c[1]) or SHORT_CARD.get(t)
        if not d and t == "Extension": d = "Extension de plain-pied, surélévation, garage ou annexe."
        if not d and t == "Terrassement": d = "Préparation de terrain, décaissement, fouilles, piscine."
        out.append(c[:2] + (d or c[2],) + c[3:])
    return out

# ---------------- Pages service × ville ----------------
SECT_DE = {"Nantes et agglomération": "dans l'agglomération nantaise", "Vignoble nantais": "dans le vignoble nantais",
           "Estuaire et Brière": "dans l'estuaire et la Brière", "Littoral et presqu'île": "sur le littoral et la presqu'île",
           "Pays de Retz": "dans le pays de Retz", "Nord Vendée": "dans le nord de la Vendée"}
def local_aside(c, svc):
    nom = c["nom"]
    dist_txt = "sur place, à Sainte-Pazanne" if c["km"] == 0 else f"à environ {c['km']} km de Sainte-Pazanne, où se trouve notre entreprise"
    near_html = ", ".join(city_link(n, svc) for n in c["near"])
    services = "".join(f'<li><a href="{href(city_file(c, k))}">{SVC[k]["label"]} à {html.escape(nom)}</a></li>' for k in SVC if k != svc)
    around = "".join(f'<li><a href="{href(city_file(CITY_BY_NAME[n], svc))}">{SVC[svc]["label"]} à {html.escape(n)}</a></li>' for n in c["near_pages"])
    return f'''<aside class="local-aside">
      <h3>{I["PIN"]}Infos pratiques</h3>
      <ul>
        <li><strong>Distance :</strong> {html.escape(nom)} est {dist_txt}.</li>
        <li><strong>Visite et devis :</strong> gratuits et sans engagement.</li>
        <li><strong>Disponibilité :</strong> {HOURS}, par téléphone ou par le formulaire.</li>
        <li><strong>Communes voisines :</strong> {near_html}.</li>
      </ul>
      <h3>Nos autres services à {html.escape(nom)}</h3><ul class="city-links">{services}</ul>
      <h3>Autour de {html.escape(nom)}</h3><ul class="city-links">{around}</ul>
    </aside>''', dist_txt

def city_page(c, svc):
    nom, dep, km = c["nom"], c["dep"], c["km"]
    e = html.escape(nom)
    aside, dist_txt = local_aside(c, svc)
    dept_name, dept_slug = DEPTS[dep]
    q_near = (f"Intervenez-vous à {nom} et dans les communes voisines ?",
              f"Oui. {nom} est {dist_txt}. Nous intervenons aussi dans les communes voisines, comme {', '.join(c['near'][:4])}. La visite sur place et le devis sont gratuits.")
    if svc == "macon":
        base = PAGE
        local = f'''<h2>Le bâti à {e} et nos interventions</h2><p>{c["bati"]}</p>
      <h2>Quartiers et secteurs de {e}</h2><p>{c["quartiers"]}</p>
      <h2>Urbanisme et autorisations à {e}</h2><p>{c["urba"]}</p>'''
        cards = [
            ("WALL", "Maçonnerie générale", "Murs, dalles, chapes, fondations, ouvertures dans les murs porteurs, reprise et rejointoiement de murs anciens.", "Le plus demandé", "maconnerie", "#devis"),
            ("HOUSEPLUS", f"Extension à {e}", "Extension de plain-pied, surélévation, garage ou annexe : nous construisons votre agrandissement du gros œuvre aux finitions.", "", "extension", href(city_file(c, "extension"))),
            ("DIGGER", f"Terrassement à {e}", "Préparation de terrain, décaissement et nivellement, fouilles et fondations, assainissement individuel, terrassement de piscine.", "", "terrassement", href(city_file(c, "terrassement"))),
            PAGE["services"][-1][:5] + ("./#renovation",),
        ]
        faq = [q_near, c["faq"], PAGE["faq"][1]]
        title = f"Maçon {nom} ({dep}) — Maçonnerie & extension | {BRAND}"
        desc = f"Maçon à {nom} : maçonnerie, ouverture de mur porteur, extension, terrassement, rénovation clé en main. Visite et devis gratuits."
        h1 = f"Maçon à {e} : <em>maçonnerie, extension et terrassement</em>"
        sub = c["intro"]
        img = c["img"]
        eyebrow = f"Maçonnerie à {e}"
        svc_lead = "Maçonnerie neuve ou reprise sur l'existant, agrandissement, terrassement et rénovation complète, pour les particuliers, les professionnels et les collectivités."
        needs = ["Murs, dalle, fondations", "Ouverture dans un mur porteur", "Extension ou surélévation", "Terrassement, décaissement", "Assainissement individuel", "Reprise de maçonnerie, rejointoiement", "Rénovation clé en main", "Autre projet"]
        stype = "Maçonnerie générale et gros œuvre"
    elif svc == "extension":
        base = EXTENSION
        g = GUIDES[0]
        local = f'''<h2>Agrandir sa maison à {e}</h2><p>{c["ext"]}</p><p>{c["bati"]}</p>
      <h2>Quel agrandissement pour votre maison à {e} ?</h2><p>{c["ext_projets"]}</p>
      <h2>Urbanisme : ce qui s'applique à {e}</h2><p>{c["urba"]}</p>
      <p>Pour savoir quelle autorisation déposer selon la surface créée, consultez notre guide <a href="{href(g["file"])}">déclaration préalable ou permis de construire</a>.</p>'''
        cards = base["services"]
        q_permis = (f"Faut-il un permis de construire pour une extension à {nom} ?",
                    f"Cela dépend de la surface créée. Jusqu'à 20 m², une déclaration préalable suffit en général, et jusqu'à 40 m² en zone urbaine d'un plan local d'urbanisme, sauf si la maison dépasse 150 m² après les travaux. À {nom}, les règles d'implantation et de hauteur sont fixées par {c['plu']}. Nous vous indiquons la démarche lors de la visite.")
        faq = [q_near, q_permis, c["faq"], EXTENSION["faq"][1]]
        title = f"Extension de maison {nom} ({dep}) — Surélévation | {BRAND}"
        desc = f"Extension de maison à {nom} : agrandissement de plain-pied, surélévation, garage, du gros œuvre aux finitions. Devis gratuit."
        h1 = f"Extension de maison à {e} : <em>agrandissement et surélévation</em>"
        sub = f"Extension de plain-pied, surélévation, garage ou annexe : nous construisons votre agrandissement à {e}, du terrassement aux finitions, en continuité avec votre maison. Visite sur place et devis gratuits."
        img = ["hero-extension-maison", "extension-maison", "hero-maison-pierre-extension", "extension-bois-maison-pierre"][CITIES.index(c) % 4]
        eyebrow = f"Extension à {e}"
        svc_lead = base["services_lead"]
        needs = base["form_needs"]
        stype = "Extension et surélévation de maison"
    else:
        base = TERRASSEMENT
        g = GUIDES[2]
        local = f'''<h2>Le terrain à {e}</h2><p>{c["sol"]}</p>
      <h2>Vos projets de terrassement à {e}</h2><p>{c["terr"]}</p>
      <h2>Autorisations à {e}</h2><p>{c["urba"]}</p>
      <p>Pour comprendre les étapes, lisez notre guide <a href="{href(g["file"])}">décaissement de terrain</a>.</p>'''
        cards = base["services"]
        q_sol = (f"Quel est le type de sol à {nom} ?", f"{c['sol']} Nous vérifions votre terrain lors de la visite avant de chiffrer.")
        faq = [q_near, q_sol, c["faq"], TERRASSEMENT["faq"][1]]
        title = f"Terrassement {nom} ({dep}) — Décaissement & fondations | {BRAND}"
        desc = f"Terrassement à {nom} : préparation de terrain, décaissement, fouilles, fondations, assainissement individuel, piscine. Devis gratuit."
        h1 = f"Terrassement à {e} : <em>décaissement, fouilles et fondations</em>"
        sub = f"Préparation de terrain, décaissement et nivellement, fouilles et fondations, assainissement individuel, terrassement de piscine : nous réalisons vos travaux de terrassement à {e}."
        img = ["hero-terrassement-piscine", "piscine-terrasse-bois", "facade-pierre-allee"][CITIES.index(c) % 3]
        eyebrow = f"Terrassement à {e}"
        svc_lead = base["services_lead"]
        needs = base["form_needs"]
        stype = "Terrassement et assainissement individuel"
    label = f"{SVC[svc]['label']} à {nom}"
    local_html = f'''<section class="section section-local" id="local">
  <div class="wrap local-grid">
    <div class="local-main">
      <span class="eyebrow">{SVC[svc]['label']} à {e}</span>
      {local}
      <h2>{SVC[svc]['service_name']} : notre approche {SECT_DE.get(c['secteur'], 'dans le secteur')}</h2><p>{SECTEUR_TXT[c['secteur']][svc]}</p>
    </div>
    {aside}
  </div>
</section>'''
    return dict(base,
        file=city_file(c, svc), lp=f"{SVC[svc]['label']} {nom}", source_label=f"Page {label}",
        title=title, desc=desc, hero_img=f"img/{img}.jpg", hero_alt="Maison rénovée et agrandie, travaux de maçonnerie",
        hero_eyebrow=f"{c['secteur']} · {e}", h1=h1, sub=sub,
        services_eyebrow=f"Nos travaux à {e}", services_h2="Ce que nous réalisons", services_lead=svc_lead,
        services=short_cards(cards), local_html=local_html, hide_zone=True, hide_steps=True, hide_why=True,
        reviews=[base["reviews"][(CITIES.index(c) + k) % len(base["reviews"])] for k in (0, 1)], nav_current=SVC[svc]["service_file"],
        crumbs=[(f"Maçon en {dept_name}", f"{dept_slug}.html"), (label, city_file(c, svc))],
        why_eyebrow=f"Pourquoi nous confier vos travaux à {e}",
        zone_svc=svc, zone_eyebrow="Zone d'intervention", zone_h2=f"Autour de {e} : nos secteurs d'intervention",
        zone_cols=[(sect, [x["nom"] for x in CITIES if x["secteur"] == sect]) for sect in SECTEURS],
        zone_lead=f"Depuis Sainte-Pazanne, nous intervenons à {e} et dans toute la Loire-Atlantique, sur le littoral et la presqu'île, et dans le nord de la Vendée.",
        reviews_h2="Ce que disent nos clients en Loire-Atlantique",
        faq_h2=f"Vos questions sur vos travaux à {e}", faq=faq,
        cta_h2=f"Votre devis gratuit à {e}", city_value=nom, form_needs=needs,
        service_ld={"@context": "https://schema.org", "@type": "Service", "serviceType": stype, "name": label,
                    "provider": {"@id": LD_BUSINESS_ID}, "url": url_of(city_file(c, svc)),
                    "areaServed": [{"@type": "City", "name": nom}] + [{"@type": "City", "name": n} for n in c["near"]]},
    )

# ---------------- Pages département et hub des zones ----------------
def zone_cards(cities):
    out = ""
    for sect in SECTEURS:
        cs = [c for c in cities if c["secteur"] == sect]
        if not cs: continue
        items = "".join(f'''<article class="zone-card"><h3><a href="{href(city_file(c))}">Maçon à {html.escape(c["nom"])}</a></h3>
          <p>{html.escape(c["intro"])}</p>
          <p class="zone-card-links"><a href="{href(city_file(c, "extension"))}">Extension</a> · <a href="{href(city_file(c, "terrassement"))}">Terrassement</a></p>
          <p class="zone-card-near">Aussi : {", ".join(html.escape(n) for n in c["near"][:4])}</p></article>''' for c in cs)
        out += f'<h2 class="zone-sect">{I["PIN"]}{sect}</h2><div class="zone-cards">{items}</div>'
    return out

def hub_page(file, crumbs, title, desc, h1, lead, cities, intro_html="", faq=None, area=None):
    p = dict(PAGE, lp="Zones", source_label=f"Page {crumbs[-1][0]}", cta_h2="Demandez votre devis gratuit")
    lds = [ld_business(area), ld_breadcrumb(crumbs)]
    faq_html = ""
    if faq:
        lds.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]})
        faq_html = '<section class="section section-sand" id="faq"><div class="wrap faq-wrap"><div class="section-head center"><h2>Vos questions</h2></div><div class="faq">' + "".join(f'<details{" open" if i == 0 else ""}><summary>{q}</summary><p>{a}</p></details>' for i, (q, a) in enumerate(faq)) + "</div></div></section>"
    body = f'''<a id="top"></a>
{header("zones-intervention.html")}
<main>
<section class="page-hero">
  <div class="wrap">
    {breadcrumb(crumbs, wrap=False)}
    <h1>{h1}</h1>
    <p class="lead">{lead}</p>
  </div>
</section>
{intro_html}
<section class="section"><div class="wrap">{zone_cards(cities)}</div></section>
{faq_html}
{cta_section(p)}
</main>
{mobile_bar()}
{footer()}'''
    return head(title, desc, file, extra_ld=ld_json(*lds)) + body

def build_dept(dep):
    name, slug = DEPTS[dep]
    cities = [c for c in CITIES if c["dep"] == dep]
    if dep == "44":
        lead = "Installés à Sainte-Pazanne, dans le pays de Retz, nous réalisons maçonnerie, extensions, terrassement et rénovations clé en main dans toute la Loire-Atlantique : agglomération nantaise, vignoble, estuaire et Brière, littoral et presqu'île guérandaise."
        intro = f'''<section class="section"><div class="wrap local-main narrow"><h2>Une entreprise du bâtiment de Loire-Atlantique</h2>
<p>Notre entreprise est installée à Sainte-Pazanne depuis 8 ans. Nous intervenons chez les particuliers, les professionnels et les collectivités, avec un seul interlocuteur du devis à la réception du chantier. Le bâti du département est varié : maisons de ville en tuffeau et pavillons de l'agglomération nantaise, longères du pays de Retz et de la Brière, villas balnéaires de la côte, maisons de vignerons autour de Vallet et Clisson. Nous adaptons les matériaux et les techniques à chacun.</p>
<p>Les règles d'urbanisme varient aussi d'un secteur à l'autre : PLUm de Nantes Métropole, PLUi de la CARENE autour de Saint-Nazaire, loi Littoral sur la côte, secteurs protégés autour des monuments historiques. Nous les vérifions lors de la visite, avant de chiffrer.</p></div></section>'''
        faq = [("Intervenez-vous dans toute la Loire-Atlantique ?", "Nous intervenons de Nantes à Saint-Nazaire et Guérande, de Clisson à Nort-sur-Erdre, dans le pays de Retz et sur toute la côte de Jade. Pour une commune plus éloignée, appelez-nous : nous vous répondons rapidement."),
               ("La visite et le devis sont-ils gratuits partout ?", "Oui. La visite sur place et le devis détaillé sont gratuits et sans engagement, quelle que soit la commune de notre zone d'intervention.")]
    else:
        lead = "Depuis Sainte-Pazanne, nous réalisons maçonnerie, extensions, terrassement et rénovations clé en main dans le nord de la Vendée : Challans, Saint-Jean-de-Monts, Saint-Hilaire-de-Riez, l'île de Noirmoutier et le marais breton-vendéen."
        intro = '''<section class="section"><div class="wrap local-main narrow"><h2>Le nord de la Vendée, entre côte et marais</h2>
<p>Le nord-ouest vendéen réunit stations balnéaires, maisons de vacances, bourrines du marais breton-vendéen et maisons de l'île de Noirmoutier. Les sols y sont très différents : sable des dunes, argile du marais. Nous adaptons les fondations et le terrassement à chaque terrain.</p>
<p>Sur la côte, la loi Littoral encadre les constructions près du rivage ; sur l'île de Noirmoutier, des règles d'aspect préservent le caractère des maisons. Nous vérifions ces règles avant de proposer une extension ou un garage.</p></div></section>'''
        faq = [("Jusqu'où intervenez-vous en Vendée ?", "Dans le nord-ouest vendéen : Challans, Saint-Jean-de-Monts, Notre-Dame-de-Monts, Saint-Hilaire-de-Riez, Beauvoir-sur-Mer et l'île de Noirmoutier, ainsi que les communes voisines."),
               ("Pouvez-vous intervenir sur une résidence secondaire ?", "Oui. Après la visite et la signature du devis, nous organisons l'accès au chantier avec vous et vous tenons informé de l'avancement.")]
    crumbs = [(f"Maçon en {name}", f"{slug}.html")]
    return hub_page(f"{slug}.html", crumbs,
        f"Maçon en {name} ({dep}) — Maçonnerie, extension, terrassement | {BRAND}",
        f"Maçon en {name} : maçonnerie, extension de maison, terrassement et rénovation clé en main dans {len(cities)} villes. Basés à Sainte-Pazanne. Devis gratuit.",
        f"Maçon en {name} : <em>nous couvrons {'tout le département' if dep == '44' else 'le nord du département'}</em>", lead, cities, intro, faq,
        area=[{"@type": "AdministrativeArea", "name": name}] + [{"@type": "City", "name": c["nom"]} for c in cities])

def build_zones():
    crumbs = [("Zones d'intervention", "zones-intervention.html")]
    intro = f'<section class="section"><div class="wrap dept-links"><a class="btn btn-outline" href="{href("macon-loire-atlantique.html")}">Maçon en Loire-Atlantique</a> <a class="btn btn-outline" href="{href("macon-vendee.html")}">Maçon en Vendée</a></div></section>'
    return hub_page("zones-intervention.html", crumbs,
        f"Zones d'intervention en Loire-Atlantique et Vendée | {BRAND}",
        "Maçonnerie, extension et terrassement à Nantes, Saint-Nazaire, Guérande, Pornic, Clisson, Nort-sur-Erdre, Saint-Jean-de-Monts et dans tout le pays de Retz.",
        "Zones d'intervention : <em>Loire-Atlantique, littoral et nord Vendée</em>",
        "Installés à Sainte-Pazanne, nous réalisons vos travaux de maçonnerie, d'extension, de terrassement et de rénovation clé en main de Nantes à Saint-Nazaire et Guérande, de Clisson à Nort-sur-Erdre, dans le pays de Retz et jusqu'à Saint-Jean-de-Monts et l'île de Noirmoutier.",
        CITIES, intro)

# ---------------- Guides ----------------
def render_blocks(blocks):
    out = ""
    for b in blocks:
        if isinstance(b, tuple):
            tag, items = b
            out += f"<{tag}>" + "".join(f"<li>{html.escape(x)}</li>" for x in items) + f"</{tag}>"
        else:
            out += f"<p>{html.escape(b)}</p>"
    return out

def build_guide(g):
    secs = "".join(f'<h2>{html.escape(t)}</h2>{render_blocks(bl)}' for t, bl in g["sections"])
    toc = "".join(f'<li>{html.escape(t)}</li>' for t, _ in g["sections"])
    svc_file, svc_name = g["service"]
    svc_file = "extension-maison.html" if svc_file == "extension.html" else svc_file
    svc_key = {"index.html": "macon", "extension-maison.html": "extension", "terrassement.html": "terrassement"}[svc_file]
    related = "".join(f'<li><a href="{href(x["file"])}">{html.escape(x["title"])}</a></li>' for x in GUIDES if x is not g)
    cities = " · ".join(f'<a href="{href(city_file(c, svc_key))}">{html.escape(c["nom"])}</a>' for c in CITIES[:12])
    p = dict(PAGE, lp=g["lp"], source_label=g["lp"], cta_eyebrow="Un projet ?", cta_h2="Demandez votre devis gratuit",
             cta_lead="Décrivez vos travaux en quelques lignes, nous vous rappelons pour convenir d'une visite sur place.")
    article_ld = {"@context": "https://schema.org", "@type": "Article", "headline": g["title"], "description": g["desc"],
                  "image": SITE + f"img/{g['img']}.jpg", "author": {"@id": LD_BUSINESS_ID}, "publisher": {"@id": LD_BUSINESS_ID},
                  "datePublished": "2026-10-05", "dateModified": TODAY, "mainEntityOfPage": url_of(g["file"]), "inLanguage": "fr-FR"}
    crumbs = [("Conseils", "conseils.html"), (g["title"], g["file"])]
    body = f'''<a id="top"></a>
{header("conseils.html")}
<main>
<section class="page-hero">
  <div class="wrap">
    {breadcrumb(crumbs, wrap=False)}
    <h1>{html.escape(g["title"])}</h1>
    <p class="lead">{html.escape(g["intro"])}</p>
  </div>
</section>
<section class="section article-section">
  <div class="wrap article-grid">
    <article class="article">
      {pic(g["img"], g["title"], cls="article-img")}
      {secs}
      <div class="article-cta">
        <p><strong>Vous avez un projet en Loire-Atlantique ou dans le nord de la Vendée ?</strong> Nous réalisons ces travaux, avec une visite sur place et un devis gratuit.</p>
        <p><a class="btn btn-primary" href="#devis">{I['ARROW']}Demander un devis gratuit</a> <a class="btn btn-outline" href="tel:{PHONE_INTL}">{I['PHONE']}{PHONE_DISPLAY}</a></p>
      </div>
    </article>
    <aside class="article-aside">
      <h3>Dans ce guide</h3><ol class="toc">{toc}</ol>
      <h3>Notre service</h3><p><a href="{href(svc_file)}">{html.escape(svc_name)}</a></p>
      <h3>À lire aussi</h3><ul>{related}</ul>
      <h3>{SVC[svc_key]["label"]} à</h3><p class="aside-cities">{cities}</p>
    </aside>
  </div>
</section>
{cta_section(p)}
</main>
{mobile_bar()}
{footer()}'''
    return head(f'{g["seo_title"]} | {BRAND}', g["desc"], g["file"], f"img/{g['img']}.jpg",
                ld_json(article_ld, ld_breadcrumb(crumbs))) + body

def build_conseils():
    cards = "".join(f'''<article class="guide-card"><a href="{href(g["file"])}">{pic(g["img"], g["title"])}</a>
      <h2><a href="{href(g["file"])}">{html.escape(g["title"])}</a></h2><p>{html.escape(g["desc"])}</p>
      <a class="card-link" href="{href(g["file"])}">Lire le guide {I["ARROW"]}</a></article>''' for g in GUIDES)
    crumbs = [("Conseils", "conseils.html")]
    body = f'''<a id="top"></a>
{header("conseils.html", devis="./#devis")}
<main>
<section class="page-hero">
  <div class="wrap">
    {breadcrumb(crumbs, wrap=False)}
    <h1>Conseils travaux : <em>maçonnerie, extension et terrassement</em></h1>
    <p class="lead">Autorisations d'urbanisme, étapes de chantier, préparation du terrain : nos guides pour préparer votre projet.</p>
  </div>
</section>
<section class="section"><div class="wrap guide-cards">{cards}</div></section>
</main>
{mobile_bar(devis="./#devis")}
{footer()}'''
    return head(f"Conseils travaux de maçonnerie et d'extension | {BRAND}",
                "Guides pratiques : déclaration préalable ou permis pour une extension, ouverture d'un mur porteur, décaissement de terrain.",
                "conseils.html", extra_ld=ld_json(ld_breadcrumb(crumbs))) + body

# ---------------- Pages légales, merci, 404 ----------------
def simple_page(file, title, h1, inner, noindex=True, desc=""):
    body = f'''<a id="top"></a>
{header(devis="./#devis")}
<main>
<section class="page-hero"><div class="wrap"><h1>{h1}</h1></div></section>
<section class="section"><div class="wrap legal">{inner}</div></section>
</main>
{footer()}'''
    return head(title, desc or title, file, noindex=noindex) + body

MENTIONS = f'''<h2>Éditeur du site</h2>
<p>{BRAND}<br>{ADDRESS}<br>Téléphone : <a href="tel:{PHONE_INTL}">{PHONE_DISPLAY}</a><br>E-mail : <a href="mailto:{EMAIL}">{EMAIL}</a><br>SIRET : {SIRET}<br>Directeur de la publication : Corentin Douillard</p>
<h2>Hébergement</h2>
<p>o2switch, Clermont-Ferrand (France) – <a href="https://www.o2switch.fr" rel="noopener">www.o2switch.fr</a></p>
<h2>Propriété intellectuelle</h2>
<p>Les textes, photos et éléments graphiques de ce site sont la propriété de {BRAND} ou utilisés avec autorisation. Toute reproduction sans accord préalable est interdite.</p>
<h2>Données personnelles</h2>
<p>Le traitement des données transmises par le formulaire de devis est décrit dans notre <a href="confidentialite">politique de confidentialité</a>.</p>'''

CONFID = f'''<h2>Données collectées</h2>
<p>Lorsque vous envoyez le formulaire de demande de devis, nous recevons votre nom, votre téléphone, votre e-mail, la commune du chantier, votre besoin et votre message. Pour savoir comment vous nous avez trouvés, nous enregistrons aussi la page d'arrivée sur le site et la provenance de la visite : moteur de recherche, annonce Google Ads (identifiant de clic) ou accès direct.</p>
<h2>Utilisation</h2>
<p>Ces données servent uniquement à répondre à votre demande, à vous recontacter pour organiser une visite et à établir votre devis. Elles ne sont ni vendues ni cédées. Elles sont traitées par {BRAND} et par ses prestataires techniques (hébergement du site, envoi des e-mails, outil de suivi des demandes).</p>
<h2>Durée de conservation</h2>
<p>Les données sont conservées pendant 3 ans à compter de notre dernier échange, sauf si un contrat de travaux est signé, auquel cas elles sont conservées le temps nécessaire à son exécution et aux obligations légales.</p>
<h2>Mesure des annonces</h2>
<p>Ce site utilise Google Tag Manager pour mesurer les demandes de devis et les appels issus des annonces Google Ads. Des cookies de mesure de Google peuvent être déposés à cette occasion.</p>
<h2>Vos droits</h2>
<p>Vous pouvez demander l'accès, la rectification ou la suppression de vos données, ou vous opposer à leur traitement, en écrivant à <a href="mailto:{EMAIL}">{EMAIL}</a>. Vous pouvez aussi adresser une réclamation à la CNIL (<a href="https://www.cnil.fr" rel="noopener">www.cnil.fr</a>).</p>'''

def build_merci():
    body = f'''<a id="top"></a>
{header(devis="./#devis")}
<main class="merci">
  <div class="wrap merci-inner">
    <div class="merci-icon">{I['CHECK']}</div>
    <h1>Merci, votre demande est bien reçue</h1>
    <p class="lead">Nous vous rappelons rapidement pour échanger sur votre projet et convenir d'une visite sur place. Besoin d'une réponse immédiate ? Appelez le <a href="tel:{PHONE_INTL}">{PHONE_DISPLAY}</a> ({HOURS}).</p>
    <a href="./" class="btn btn-primary">{I['ARROW']}Retour à l'accueil</a>
  </div>
</main>
{footer()}'''
    return head("Merci – Demande envoyée | " + BRAND, "Votre demande de devis a bien été envoyée à " + BRAND + ".", "merci.html", noindex=True) + body

def build_404():
    links = "".join(f'<li><a href="/{slug_of(city_file(c))}">Maçon à {html.escape(c["nom"])}</a></li>' for c in CITIES[:8])
    inner = f'''<p class="lead">Cette page n'existe pas ou a été déplacée.</p>
<p><a class="btn btn-primary" href="/">{I['ARROW']}Retour à l'accueil</a></p>
<h2>Nos services</h2><ul><li><a href="/">Maçonnerie générale</a></li><li><a href="/extension-maison">Extension et surélévation</a></li><li><a href="/terrassement">Terrassement</a></li></ul>
<h2>Nos zones</h2><ul>{links}</ul>'''
    return simple_page("404.html", "Page introuvable | " + BRAND, "Page introuvable", inner).replace("<head>", '<head>\n<base href="/">', 1)

# ---------------- Écriture ----------------
os.chdir(HERE)
make_webp()
for old in [f for f in os.listdir(".") if f.startswith("macon-") and f.endswith(".html")]:
    os.remove(old)  # régénérées ci-dessous (évite de laisser d'anciennes pages)
out = {}
for p in PAGES:
    out[p["file"]] = build_lp(p)
out["extension.html"] = out["extension-maison.html"]  # adresse finale Google Ads, canonique vers /extension-maison
for c in CITIES:
    for svc in SVC:
        out[city_file(c, svc)] = build_lp(city_page(c, svc))
out["macon-loire-atlantique.html"] = build_dept("44")
out["macon-vendee.html"] = build_dept("85")
out["zones-intervention.html"] = build_zones()
for g in GUIDES:
    out[g["file"]] = build_guide(g)
out["conseils.html"] = build_conseils()
out["merci.html"] = build_merci()
out["mentions-legales.html"] = simple_page("mentions-legales.html", "Mentions légales | " + BRAND, "Mentions légales", MENTIONS, noindex=False, desc=f"Mentions légales du site de {BRAND}, entreprise du bâtiment à Sainte-Pazanne.")
out["confidentialite.html"] = simple_page("confidentialite.html", "Politique de confidentialité | " + BRAND, "Politique de confidentialité", CONFID, noindex=False, desc=f"Comment {BRAND} traite les données transmises par le formulaire de devis.")
out["404.html"] = build_404()
for f, s in out.items():
    open(f, "w", encoding="utf-8").write(s)

def canonical_in(s):
    m = re.search(r'rel="canonical" href="([^"]+)"', s); return m.group(1) if m else ""
indexables = sorted({canonical_in(s) for f, s in out.items() if 'content="index, follow' in s}, key=lambda u: (u != SITE, u))
def prio(u):
    s = u[len(SITE):]
    if s == "": return "1.0"
    if s in ("extension-maison", "terrassement"): return "0.9"
    if s in ("macon-loire-atlantique", "macon-vendee", "zones-intervention"): return "0.8"
    if s.startswith(("macon-", "extension-maison-", "terrassement-")): return "0.7"
    return "0.5"
urls = "".join(f'  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod><priority>{prio(u)}</priority></url>\n' for u in indexables)
open("sitemap.xml", "w", encoding="utf-8").write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
open("robots.txt", "w").write(f"User-agent: *\nAllow: /\nDisallow: /merci\nDisallow: /contact.php\nDisallow: /ads/\n\nSitemap: {SITE}sitemap.xml\n")
print(f"OK : {len(out)} fichiers, {len(indexables)} adresses dans le sitemap, {len(CITIES)} villes × {len(SVC)} services, {len(GUIDES)} guides — GTM {GTM_ID}")
