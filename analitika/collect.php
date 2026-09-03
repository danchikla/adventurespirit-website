<?php
/**
 * Prvostrana analitika bez kolačića - Adventure Spirit d.o.o.
 *
 * Ne postavlja kolačiće, ne pohranjuje IP adresu i ne stvara identifikator
 * koji traje dulje od jednog dana. Posjetitelj se broji preko otiska koji
 * nastaje iz dnevne tajne, IP adrese i preglednika, pa se svakog dana u
 * ponoć isti posjetitelj više ne može povezati s jučerašnjim posjetom.
 *
 * Zbog toga za ovu obradu nije potrebna privola za kolačiće. Zadržava se
 * samo agregirana statistika.
 */

header('Content-Type: application/json; charset=utf-8');
header('X-Content-Type-Options: nosniff');
header('Cache-Control: no-store');

// Samo POST, samo s vlastite domene
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    exit('{"ok":false}');
}
$origin = isset($_SERVER['HTTP_ORIGIN']) ? $_SERVER['HTTP_ORIGIN'] : '';
$rawHost = isset($_SERVER['HTTP_HOST']) ? $_SERVER['HTTP_HOST'] : '';
$host = strtolower(preg_replace('/:\d+$/', '', $rawHost));   // bez porta
if ($origin !== '') {
    $oh = strtolower((string)parse_url($origin, PHP_URL_HOST));
    if ($oh !== $host) {
        http_response_code(403);
        exit('{"ok":false,"reason":"origin"}');
    }
}

// Poštuj Do Not Track i Global Privacy Control
if ((isset($_SERVER['HTTP_DNT']) && $_SERVER['HTTP_DNT'] === '1')
    || (isset($_SERVER['HTTP_SEC_GPC']) && $_SERVER['HTTP_SEC_GPC'] === '1')) {
    exit('{"ok":true,"skipped":"dnt"}');
}

$raw = file_get_contents('php://input', false, null, 0, 4096);
$in  = json_decode($raw, true);
if (!is_array($in)) { http_response_code(400); exit('{"ok":false}'); }

// ── Dnevni otisak posjetitelja ───────────────────────────────────
$dataDir = __DIR__ . '/podaci';
if (!is_dir($dataDir)) { @mkdir($dataDir, 0750, true); }

$saltFile = $dataDir . '/.sol';
$today    = gmdate('Y-m-d');
$salt     = '';
if (is_readable($saltFile)) {
    $stored = json_decode((string)@file_get_contents($saltFile), true);
    if (is_array($stored) && isset($stored['d']) && $stored['d'] === $today) {
        $salt = $stored['s'];
    }
}
if ($salt === '') {
    $salt = bin2hex(random_bytes(32));
    @file_put_contents($saltFile, json_encode(array('d' => $today, 's' => $salt)), LOCK_EX);
    @chmod($saltFile, 0640);
}

$ip = isset($_SERVER['REMOTE_ADDR']) ? $_SERVER['REMOTE_ADDR'] : '';
$ua = isset($_SERVER['HTTP_USER_AGENT']) ? $_SERVER['HTTP_USER_AGENT'] : '';
$visitor = substr(hash('sha256', $salt . '|' . $ip . '|' . $ua), 0, 16);
unset($ip); // dalje se ne koristi i nigdje se ne zapisuje

// ── Odbaci očite robote ──────────────────────────────────────────
if ($ua === '' || preg_match('/bot|crawler|spider|crawling|headless|preview|monitor|curl|wget|python-requests/i', $ua)) {
    exit('{"ok":true,"skipped":"bot"}');
}

// ── Očisti ulaz ──────────────────────────────────────────────────
function clean($v, $max = 180) {
    $v = is_string($v) ? $v : '';
    $v = preg_replace('/[\x00-\x1F\x7F]/u', '', $v);
    $v = str_replace(array('"', "\n", "\r", "\t"), ' ', $v);
    return trim(mb_substr($v, 0, $max));
}

$path = clean(isset($in['p']) ? $in['p'] : '/', 200);
if ($path === '' || $path[0] !== '/') { $path = '/'; }
$path = preg_replace('/\?.*$/', '', $path);   // makni upitne parametre

$refHost = '';
if (!empty($in['r'])) {
    $h = parse_url(clean($in['r'], 300), PHP_URL_HOST);
    if ($h && strcasecmp($h, $host) !== 0) { $refHost = strtolower(preg_replace('/^www\./', '', $h)); }
}

$lang  = clean(isset($in['l']) ? $in['l'] : '', 8);
$w     = isset($in['w']) ? (int)$in['w'] : 0;
$device = $w >= 1200 ? 'desktop' : ($w >= 700 ? 'tablet' : ($w > 0 ? 'mobile' : '-'));
$event = clean(isset($in['e']) ? $in['e'] : '', 40);
$value = isset($in['v']) && $in['v'] !== '' ? (int)$in['v'] : '';
$site  = (strpos($path, '/en/') === 0) ? 'en' : 'hr';

// ── Zapiši ───────────────────────────────────────────────────────
$file = $dataDir . '/' . gmdate('Y-m') . '.csv';
$new  = !file_exists($file);
$fh   = @fopen($file, 'a');
if ($fh) {
    if (flock($fh, LOCK_EX)) {
        if ($new) {
            fwrite($fh, "vrijeme,posjetitelj,putanja,jezik,izvor,uredaj,dogadaj,vrijednost\n");
        }
        fwrite($fh, sprintf("%s,%s,\"%s\",%s,\"%s\",%s,\"%s\",%s\n",
            gmdate('Y-m-d H:i:s'), $visitor, $path, $site . ($lang ? '/' . $lang : ''),
            $refHost, $device, $event, $value));
        flock($fh, LOCK_UN);
    }
    fclose($fh);
    @chmod($file, 0640);
}

exit('{"ok":true}');
