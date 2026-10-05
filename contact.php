<?php
// Formulaire de devis — variante PHP (hébergement o2switch/cPanel). Voir references/forms-leads.md
header('Content-Type: application/json');
date_default_timezone_set('Europe/Paris');

$DEST     = 'contact@larenovationdevosreves.fr, renovationdevosreves@outlook.fr';                            // destinataire visible : le client
$BCC      = 'aymeric@cleanibat.fr';                         // Aymeric toujours en copie CACHÉE, jamais en destinataire visible
$FROM     = 'La Renovation de vos reves <no-reply@cleanibat.fr>';               // domaine avec SPF+DKIM valides, sinon Gmail supprime en silence
$SUBJECT  = 'Nouvelle demande de devis - ';
$CSV      = dirname($_SERVER['DOCUMENT_ROOT']) . '/leads_renovation-de-vos-reves_v2.csv';  // hors docroot : filet de sécurité (v2 : colonnes d'origine)
$THANKS   = 'merci.html';

// ?test=1 : envoi à Aymeric uniquement, pour vérifier la chaîne sans déranger le client
if (isset($_GET['test'])) { $DEST = $BCC; $BCC = ''; }

if ($_SERVER['REQUEST_METHOD'] !== 'POST') { http_response_code(405); echo json_encode(['success'=>false]); exit; }
if (!empty($_POST['_honey'])) { echo json_encode(['success'=>true]); exit; }

function v($keys){ foreach((array)$keys as $k){ if(isset($_POST[$k]) && trim($_POST[$k])!=='') return trim(strip_tags($_POST[$k])); } return ''; }
$nom=v(['Nom','nom','name']); $tel=v(['Téléphone','telephone','tel','phone']); $email=v(['Email','email']);
$ville=v(['Localité','ville','city']); $besoin=v(['Besoin','besoin','need']); $msg=v(['Message','message']); $src=v(['Source']);
if ($nom==='' || !filter_var($email, FILTER_VALIDATE_EMAIL)) { http_response_code(400); echo json_encode(['success'=>false,'message'=>'Données invalides.']); exit; }

// Origine du lead (champs cachés remplis par main.js, modèle « dernier clic non direct » sur 90 jours)
$A = [];
foreach (['gclid','gbraid','wbraid','fbclid','msclkid','utm_source','utm_medium','utm_campaign','utm_term','utm_content','referrer','landing_page'] as $k) $A[$k] = substr(v([$k]), 0, 300);
$us = strtolower($A['utm_source']); $um = strtolower($A['utm_medium']);
$refHost = $A['referrer'] !== '' ? strtolower((string)parse_url($A['referrer'], PHP_URL_HOST)) : '';
$moteurs = ['google','bing','qwant','duckduckgo','ecosia','yahoo','yandex','startpage','lilo','brave','baidu','ask'];
$moteur = '';
foreach ($moteurs as $m) { if ($refHost !== '' && preg_match('/(^|\.)'.$m.'\./', $refHost)) { $moteur = $m; break; } }
$page = $A['landing_page'] !== '' ? $A['landing_page'] : '?';
if ($A['gclid'] !== '' || $A['gbraid'] !== '' || $A['wbraid'] !== '' || ($us === 'google' && in_array($um, ['cpc','ppc','paid','paid_search','sea']))) {
  $origine = 'Google Ads';
  $id = $A['gclid'] !== '' ? 'gclid:'.$A['gclid'] : ($A['gbraid'] !== '' ? 'gbraid:'.$A['gbraid'] : ($A['wbraid'] !== '' ? 'wbraid:'.$A['wbraid'] : 'utm'));
  $detail = trim(($A['utm_campaign'] !== '' ? $A['utm_campaign'].' · ' : '').$id);
} elseif ($A['fbclid'] !== '' || in_array($us, ['facebook','fb','instagram','ig','meta'])) {
  $origine = 'Meta Ads'; $detail = $A['utm_campaign'] !== '' ? $A['utm_campaign'] : 'fbclid';
} elseif ($moteur !== '' && $A['utm_source'] === '' && $A['msclkid'] === '') {
  $origine = 'SEO'; $detail = 'recherche '.$refHost;
} elseif ($A['msclkid'] !== '' || $A['utm_source'] !== '') {
  $origine = 'Autre'; $detail = $A['msclkid'] !== '' ? 'Microsoft Ads' : 'utm '.$A['utm_source'].'/'.$A['utm_medium'];
} elseif ($refHost !== '') {
  $origine = 'Autre'; $detail = 'lien depuis '.$refHost;
} else {
  $origine = 'Site'; $detail = 'accès direct';
}
$campagne = $src.' · '.$detail.' · arrivée '.$page;

// 1) Sauvegarde locale AVANT l'envoi
$fh=@fopen($CSV,'a');
if($fh){ if(filesize($CSV)===0) fputcsv($fh,array_merge(['date','nom','telephone','email','localite','besoin','message','formulaire','origine','detail'],array_keys($A),['ip']),';');
  fputcsv($fh,array_merge([date('Y-m-d H:i:s'),$nom,$tel,$email,$ville,$besoin,str_replace(["\r","\n"],' ',$msg),$src,$origine,$detail],array_values($A),[$_SERVER['REMOTE_ADDR']??'']),';'); fclose($fh); @chmod($CSV,0600); }

// 1 bis) Envoi au CRM du client via Make. Configuration hors docroot, jamais dans le dépôt.
$cfg = @json_decode(@file_get_contents(dirname($_SERVER['DOCUMENT_ROOT']) . '/agence_renovation-de-vos-reves.json'), true);
if (is_array($cfg) && !empty($cfg['make_url']) && function_exists('curl_init')) {
  $lead = ['client'=>$cfg['client']??'', 'cle'=>$cfg['cle']??'', 'nom'=>$nom, 'telephone'=>$tel, 'email'=>$email, 'localite'=>$ville, 'besoin'=>$besoin,
    'message'=>str_replace(["\r","\n"],' ',$msg), 'source'=>$origine, 'campagne'=>$campagne, 'id'=>'site-'.date('YmdHis').'-'.substr(md5($email.$tel),0,6)];
  $ch = curl_init($cfg['make_url']);
  curl_setopt_array($ch, [CURLOPT_POST=>true, CURLOPT_RETURNTRANSFER=>true, CURLOPT_CONNECTTIMEOUT=>2, CURLOPT_TIMEOUT=>4,
    CURLOPT_HTTPHEADER=>['Content-Type: application/json'], CURLOPT_POSTFIELDS=>json_encode($lead)]);
  @curl_exec($ch); @curl_close($ch);
}

// 2) E-mail
$body="Nouvelle demande de devis\n\nNom       : $nom\nTéléphone : $tel\nEmail     : $email\nLocalité  : $ville\nBesoin    : $besoin\nFormulaire: $src\n\nMessage :\n$msg\n\n--\nOrigine   : $origine ($detail)\nArrivée   : $page\n".($A['referrer']!=='' ? "Référent  : {$A['referrer']}\n" : '');
$headers="From: $FROM\r\nReply-To: $email\r\n".($BCC!=='' ? "Bcc: $BCC\r\n" : '')."Content-Type: text/plain; charset=UTF-8\r\nX-Mailer: PHP/".phpversion();
@mail($DEST, $SUBJECT.$origine.' - '.($src!=='' ? $src.' - ' : '').$nom, $body, $headers);

// 3) Réponse : redirection (formulaire classique) ou JSON (fetch)
if (empty($_SERVER['HTTP_X_REQUESTED_WITH'])) { header('Location: '.$THANKS.'?lp='.urlencode($src)); exit; }
echo json_encode(['success'=>true]);
