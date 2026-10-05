# La Rénovation de vos rêves – Site (LP Google Ads + SEO local)

Site statique généré par `build.py` (textes des LP dans `PAGE`, `EXTENSION`, `TERRASSEMENT` ; contenus SEO des villes et guides dans `seo_content.py`).
Aperçu partageable (GitHub Pages) : https://cleanibat.github.io/renovation-de-vos-reves-lp/

```bash
python3 build.py   # régénère toutes les pages, sitemap.xml et robots.txt
```

## Pages
- `index.html` : LP Maçonnerie.
- `extension.html` : LP Extension et surélévation.
- `terrassement.html` : LP Terrassement et assainissement.
- `merci.html` : page de confirmation après envoi du formulaire (noindex).
- `extension-maison.html` : version SEO de la LP Extension (canonique de `extension.html`, qui reste l'URL finale Google Ads).

## SEO (modèle artipierre.fr)
- URL propres sans `.html` (réécriture dans `.htaccess`) ; `extension.html`, `terrassement.html`, `merci.html` et `404.html` restent servies telles quelles.
- 31 villes × 3 services : `macon-<ville>`, `extension-maison-<ville>`, `terrassement-<ville>`. Textes propres à chaque ville (bâti, quartiers, urbanisme, sol, projets, FAQ) dans `seo_content.py` ; communes voisines et distances calculées depuis `ads/communes.json`.
- Pages hub : `macon-loire-atlantique`, `macon-vendee`, `zones-intervention` ; guides dans `conseils`.
- Données structurées : HomeAndConstructionBusiness, Service, FAQPage, BreadcrumbList. Sitemap et robots générés.
- Ajouter une ville : une entrée dans `CITIES`/`MORE_CITIES` (+ `EXTRA` et les textes locaux), puis `python3 build.py`.

## Cookies et consentement (CNIL, Mode Consentement v2)
- Bandeau maison (pas d'outil tiers) : « Tout refuser » et « Tout accepter » au même niveau, choix conservé 6 mois dans `rdvr_consent`, lien « Gestion des cookies » en pied de page.
- Dans le `<head>`, avant GTM : `gtag('consent','default', …)` refusé par défaut (ou accordé si choix mémorisé). Au clic : `consent update` + événement dataLayer `consent_update`.
- Mode avancé, réglage « minimum CNIL » choisi par Aymeric : sans accord, pas de cookies Google Ads (_gcl_*) ni de `rdvr_origine`, mais signaux sans cookie avec identifiant de clic (pas d'`ads_data_redaction`) et `url_passthrough` (le gclid suit dans les URL internes, ce qui garde aussi la Source du CRM).
- Polices Outfit et Inter hébergées dans `fonts/` (aucun appel à Google Fonts).

## Origine des leads (Google Ads / SEO)
`main.js` mémorise 90 jours (si les cookies sont acceptés) la dernière origine non directe (gclid/gbraid/wbraid, fbclid, utm, référent) et remplit des champs cachés du formulaire.
`contact.php` en déduit la Source du CRM : `Google Ads` (identifiant de clic ou utm google/cpc), `Meta Ads`, `SEO` (arrivée depuis un moteur de recherche sans identifiant publicitaire), `Autre` (autre site, utm), `Site` (accès direct).
Le détail (page, gclid complet, moteur, page d'arrivée) va dans la colonne « Campagne ou page » et dans l'e-mail.

## Formulaire
Formulaire HTML classique envoyé à `contact.php` (e-mail au client, Aymeric en copie cachée, sauvegarde CSV hors docroot, redirection vers `merci.html`).
Sur GitHub Pages, le formulaire est illustratif : il ne fonctionne qu'une fois le site déployé sur un hébergement PHP.
Test sans déranger le client : poster vers `contact.php?test=1` (envoi à Aymeric uniquement).

## CRM
Chaque demande est aussi envoyée par `contact.php` au CRM Google Sheets du client via Make (slug `renovation-de-vos-reves`).
Le fichier `agence_renovation-de-vos-reves.json` (clé du client) se dépose sur le serveur, dans le dossier parent du docroot, jamais dans ce dépôt.

## Hébergement et déploiement
Production : https://www.larenovationdevosreves.com/ sur l'o2switch d'Aymeric (compte `riay4008`, serveur `clavier.o2switch.net`).
- Docroot : `/home/riay4008/larenovationdevosreves.com/` (droits 755). Certificat Let's Encrypt émis via l'outil o2switch.
- Déploiement : le dépôt est cloné dans `/home/riay4008/repos/renovation-de-vos-reves-lp`. Une tâche cron fait `git pull` puis `rsync` vers le docroot toutes les 5 minutes. Un push sur `main` est donc en ligne en 5 minutes au plus, sans clé ni mot de passe (o2switch bloque le SSH entrant depuis GitHub).
- Journal des erreurs de déploiement : `/home/riay4008/logs/deploy_rdvr.log` (vide = tout va bien).
- Configuration CRM : `/home/riay4008/agence_renovation-de-vos-reves.json` ; sauvegarde des demandes : `/home/riay4008/leads_renovation-de-vos-reves_v2.csv` (avec les colonnes d'origine ; l'ancien fichier sans `_v2` contient les demandes antérieures).
- GitHub Pages reste un aperçu (formulaire inactif).

## Checklist de lancement
1. Fait : hébergement, domaine, SSL, formulaire testé (`?test=1`), CRM alimenté.
2. Fait : GTM-T7MVZBMN sur toutes les pages, conteneur publié (Conversion Linker, formulaire envoyé, clic téléphone).
3. Fait : conversions Google Ads « Demande de devis » et « Appel téléphonique » (ID 18427796482) reliées à GTM, testées.
4. Fait : lignes de test supprimées du CRM.
5. Fait : campagne Google Ads publiée (une URL finale par LP).
6. SEO : Search Console, sitemap soumis.

## Règles de rédaction fixées par Aymeric
- Ne jamais sous-entendre de sous-traitance : l'entreprise réalise les travaux.
- Pas de mention d'étude de structure : société de maçonnerie, pas bureau d'études.
- Zone : « en Loire-Atlantique », avec littoral et presqu'île, et nord Vendée.
- La rénovation clé en main figure dans les services.
- Terrassement : jamais de tout-à-l'égout ni de VRD.
- Aucun chiffre, chantier ou avis inventé ; pas de superlatifs.

## À faire valider par le client
- Les photos proviennent de son site actuel (photos d'illustration, probablement de banque d'images) : remplacer par des photos de chantiers réels dès que possible, en particulier sur la page Terrassement qui n'a aucune photo de terrassement.
- Les témoignages sont repris de la page Témoignages de son site.
