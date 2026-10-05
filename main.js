/* Le suivi des conversions est géré par GTM (déclencheurs natifs Form Submit et clic tel:).
   Ce fichier : année du pied de page, comparateur avant/après, bouton d'envoi, et origine des visites
   (Google Ads, SEO, accès direct…) transmise au formulaire pour le CRM. */
(function () {
  "use strict";
  var y = document.getElementById("year"); if (y) y.textContent = new Date().getFullYear();

  /* Comparateur avant / après */
  document.querySelectorAll("[data-ba]").forEach(function (ba) {
    var r = ba.querySelector(".ba-range"); if (!r) return;
    var set = function () { ba.style.setProperty("--pos", r.value + "%"); }; set(); r.addEventListener("input", set);
  });

  /* Bouton d'envoi : état "Envoi…" après validation HTML5 (aucun effet sur GTM) */
  document.querySelectorAll("form").forEach(function (f) {
    f.addEventListener("submit", function () {
      if (!f.checkValidity()) return;
      var b = f.querySelector("button[type=submit]"); if (b) { b.disabled = true; b.textContent = b.getAttribute("data-sending") || "Envoi…"; }
    });
  });

  /* Origine de la visite : modèle « dernier clic non direct », mémorisé 90 jours (fenêtre de conversion Google Ads).
     - identifiant de clic (gclid, gbraid, wbraid, fbclid, msclkid) ou paramètres utm → nouvelle origine ;
     - arrivée depuis un autre site (moteur de recherche, lien) → nouvelle origine ;
     - navigation interne ou accès direct → on garde l'origine mémorisée. */
  var KEY = "rdvr_origine", TTL = 90 * 864e5;
  var PARAMS = ["gclid", "gbraid", "wbraid", "fbclid", "msclkid", "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content"];
  var FIELDS = PARAMS.concat(["referrer", "landing_page"]);
  var q, cur = {}, has = false, ref = "", st = null;
  try { q = new URLSearchParams(location.search); } catch (e) { q = null; }
  if (q) PARAMS.forEach(function (k) { var v = q.get(k); if (v) { cur[k] = v.slice(0, 300); has = true; } });
  try {
    if (document.referrer) {
      var h = new URL(document.referrer).hostname;
      if (h && h.indexOf("larenovationdevosreves") === -1) ref = document.referrer.slice(0, 300);
    }
  } catch (e) {}
  try { st = JSON.parse(localStorage.getItem(KEY) || "null"); } catch (e) { st = null; }
  if (st && (!st.ts || Date.now() - st.ts > TTL)) st = null;
  if (has || ref || !st) {
    st = cur; st.referrer = ref; st.landing_page = location.pathname; st.ts = Date.now();
    try { localStorage.setItem(KEY, JSON.stringify(st)); } catch (e) {}
  }
  /* Repli : identifiant de clic laissé par le Conversion Linker (cookie _gcl_aw), seulement pour un accès direct */
  if (!st.gclid && !st.gbraid && !st.wbraid && !st.referrer && !st.utm_source) {
    var m = document.cookie.match(/(?:^|; )_gcl_aw=([^;]+)/);
    if (m) { var parts = decodeURIComponent(m[1]).split("."); if (parts.length >= 3) st.gclid = parts.slice(2).join("."); }
  }
  document.querySelectorAll("form").forEach(function (f) {
    FIELDS.forEach(function (k) {
      var i = f.querySelector('input[name="' + k + '"]');
      if (i && st[k]) i.value = st[k];
    });
  });
})();
