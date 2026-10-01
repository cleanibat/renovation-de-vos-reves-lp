# La Rénovation de vos rêves – Landing pages Google Ads

Site statique généré par `build.py` (textes dans le dictionnaire `PAGE`, config en tête du fichier).
Aperçu partageable (GitHub Pages) : https://cleanibat.github.io/renovation-de-vos-reves-lp/

```bash
python3 build.py   # régénère index.html, extension.html, terrassement.html, merci.html, sitemap.xml, robots.txt
```

## Pages
- `index.html` : LP Maçonnerie.
- `extension.html` : LP Extension et surélévation.
- `terrassement.html` : LP Terrassement et assainissement.
- `merci.html` : page de confirmation après envoi du formulaire.

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
- Configuration CRM : `/home/riay4008/agence_renovation-de-vos-reves.json` ; sauvegarde des demandes : `/home/riay4008/leads_renovation-de-vos-reves.csv`.
- GitHub Pages reste un aperçu (formulaire inactif).

## Checklist de lancement
1. Fait : hébergement, domaine, SSL, formulaire testé (`?test=1`), CRM alimenté.
2. Fait : GTM-T7MVZBMN sur toutes les pages, conteneur publié (Conversion Linker, formulaire envoyé, clic téléphone).
3. Fait : conversions Google Ads « Demande de devis » et « Appel téléphonique » (ID 18427796482) reliées à GTM, testées.
4. Supprimer les lignes de test dans le CRM.
5. Construire la campagne Google Ads (une URL finale par page).

## Règles de rédaction fixées par Aymeric
- Ne jamais sous-entendre de sous-traitance : l'entreprise réalise les travaux.
- Pas de mention d'étude de structure : société de maçonnerie, pas bureau d'études.
- Zone : « en Loire-Atlantique », avec littoral et presqu'île, et nord Vendée.
- La rénovation clé en main figure dans les services.

## À faire valider par le client
- Les photos proviennent de son site actuel (photos d'illustration, probablement de banque d'images) : remplacer par des photos de chantiers réels dès que possible, en particulier sur la page Terrassement qui n'a aucune photo de terrassement.
- Les témoignages sont repris de la page Témoignages de son site.
