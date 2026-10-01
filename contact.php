<?php
// Formulaire de devis — variante PHP (hébergement o2switch/cPanel). Voir references/forms-leads.md
header('Content-Type: application/json');
date_default_timezone_set('Europe/Paris');

$DEST     = 'contact@larenovationdevosreves.fr, renovationdevosreves@outlook.fr';                            // destinataire visible : le client
$BCC      = 'aymeric@cleanibat.fr';                         // Aymeric toujours en copie CACHÉE, jamais en destinataire visible
$FROM     = 'La Renovation de vos reves <no-reply@cleanibat.fr>';               // domaine avec SPF+DKIM valides, sinon Gmail supprime en silence
$SUBJECT  = 'Nouvelle demande de devis - ';
$CSV      = dirname($_SERVER['DOCUMENT_ROOT']) . '/leads_renovation-de-vos-reves.csv';  // hors docroot : filet de sécurité
$THANKS   = 'merci.html';

// ?test=1 : envoi à Aymeric uniquement, pour vérifier la chaîne sans déranger le client
if (isset($_GET['test'])) { $DEST = $BCC; $BCC = ''; }

if ($_SERVER['REQUEST_METHOD'] !== 'POST') { http_response_code(405); echo json_encode(['success'=>false]); exit; }
if (!empty($_POST['_honey'])) { echo json_encode(['success'=>true]); exit; }

function v($keys){ foreach((array)$keys as $k){ if(isset($_POST[$k]) && trim($_POST[$k])!=='') return trim(strip_tags($_POST[$k])); } return ''; }
$nom=v(['Nom','nom','name']); $tel=v(['Téléphone','telephone','tel','phone']); $email=v(['Email','email']);
$ville=v(['Localité','ville','city']); $besoin=v(['Besoin','besoin','need']); $msg=v(['Message','message']); $src=v(['Source']);
if ($nom==='' || !filter_var($email, FILTER_VALIDATE_EMAIL)) { http_response_code(400); echo json_encode(['success'=>false,'message'=>'Données invalides.']); exit; }

// 1) Sauvegarde locale AVANT l'envoi
$fh=@fopen($CSV,'a');
if($fh){ if(filesize($CSV)===0) fputcsv($fh,['date','nom','telephone','email','localite','besoin','message','source','ip'],';');
  fputcsv($fh,[date('Y-m-d H:i:s'),$nom,$tel,$email,$ville,$besoin,str_replace(["\r","\n"],' ',$msg),$src,$_SERVER['REMOTE_ADDR']??''],';'); fclose($fh); @chmod($CSV,0600); }

// 1 bis) Envoi au CRM du client via Make. Configuration hors docroot, jamais dans le dépôt.
$cfg = @json_decode(@file_get_contents(dirname($_SERVER['DOCUMENT_ROOT']) . '/agence_renovation-de-vos-reves.json'), true);
if (is_array($cfg) && !empty($cfg['make_url']) && function_exists('curl_init')) {
  $lead = ['client'=>$cfg['client']??'', 'cle'=>$cfg['cle']??'', 'nom'=>$nom, 'telephone'=>$tel, 'email'=>$email, 'localite'=>$ville, 'besoin'=>$besoin,
    'message'=>str_replace(["\r","\n"],' ',$msg), 'source'=>$cfg['source']??'Site', 'campagne'=>$src, 'id'=>'site-'.date('YmdHis').'-'.substr(md5($email.$tel),0,6)];
  $ch = curl_init($cfg['make_url']);
  curl_setopt_array($ch, [CURLOPT_POST=>true, CURLOPT_RETURNTRANSFER=>true, CURLOPT_CONNECTTIMEOUT=>2, CURLOPT_TIMEOUT=>4,
    CURLOPT_HTTPHEADER=>['Content-Type: application/json'], CURLOPT_POSTFIELDS=>json_encode($lead)]);
  @curl_exec($ch); @curl_close($ch);
}

// 2) E-mail
$body="Nouvelle demande de devis\n\nNom       : $nom\nTéléphone : $tel\nEmail     : $email\nLocalité  : $ville\nBesoin    : $besoin\nSource    : $src\n\nMessage :\n$msg\n";
$headers="From: $FROM\r\nReply-To: $email\r\n".($BCC!=='' ? "Bcc: $BCC\r\n" : '')."Content-Type: text/plain; charset=UTF-8\r\nX-Mailer: PHP/".phpversion();
@mail($DEST, $SUBJECT.($src!=='' ? $src.' - ' : '').$nom, $body, $headers);

// 3) Réponse : redirection (formulaire classique) ou JSON (fetch)
if (empty($_SERVER['HTTP_X_REQUESTED_WITH'])) { header('Location: '.$THANKS.'?lp='.urlencode($src)); exit; }
echo json_encode(['success'=>true]);
