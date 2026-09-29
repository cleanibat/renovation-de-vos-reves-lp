# La Rénovation de vos rêves – Landing page Google Ads « Maçonnerie »

Site statique généré par `build.py` (textes dans le dictionnaire `PAGE`, config en tête du fichier).
Aperçu partageable (GitHub Pages) : https://cleanibat.github.io/renovation-de-vos-reves-lp/

```bash
python3 build.py   # régénère index.html, merci.html, sitemap.xml, robots.txt
```

## Pages
- `index.html` : LP Maçonnerie (murs, ouvertures, dalles, extension/surélévation, terrassement, reprise).
- `merci.html` : page de confirmation après envoi du formulaire (FormSubmit, `_next`).

## Hébergement
Le site actuel du client (larenovationdevosreves.fr) est sur un site builder (Cristal'ID / Nexylan) sans accès fichiers :
GitHub Pages sert de mise en ligne. Pour un domaine client, ajouter un `CNAME` (ex. `page.larenovationdevosreves.fr`) et
un enregistrement DNS CNAME vers `cleanibat.github.io`, puis mettre `SITE` à jour dans `build.py`.

## Checklist de lancement
1. E-mail de réception des leads : `contact@larenovationdevosreves.fr` (FormSubmit : activation à cliquer au premier envoi).
2. `GTM_ID` dans `build.py`, conteneur importé (`gtm_container.py`) et publié.
3. Conversions Google Ads créées et importées dans GTM.
4. Domaine final dans `SITE` (canonical, `_next`, sitemap), puis `python3 build.py`.
5. Test de bout en bout du formulaire.

## À faire valider par le client
- Les photos proviennent de son site actuel (photos d'illustration, probablement de banque d'images) : remplacer par des photos de chantiers réels dès que possible.
- Les témoignages sont repris de la page Témoignages de son site.
