<?php
/**
 * Nadzorna ploča prvostrane analitike - Adventure Spirit d.o.o.
 * Zaštićeno lozinkom preko .htaccess (HTTP Basic). Ne postavlja kolačiće.
 */
// Ne prikazuj PHP poruke posjetitelju; greske idu u zapisnik posluzitelja
@ini_set('display_errors', '0');

$dataDir = __DIR__ . '/podaci';
$months = array();
foreach (glob($dataDir . '/*.csv') as $f) { $months[] = basename($f, '.csv'); }
rsort($months);
$month = isset($_GET['m']) && in_array($_GET['m'], $months, true) ? $_GET['m'] : (count($months) ? $months[0] : gmdate('Y-m'));

$rows = array();
$file = $dataDir . '/' . $month . '.csv';
if (is_readable($file)) {
    $fh = fopen($file, 'r');
    fgetcsv($fh, 0, ',', '"', '\\'); // zaglavlje
    while (($r = fgetcsv($fh, 0, ',', '"', '\\')) !== false) {
        if (count($r) < 8) { continue; }
        $rows[] = array('t' => $r[0], 'v' => $r[1], 'p' => $r[2], 'l' => $r[3],
                        'ref' => $r[4], 'd' => $r[5], 'e' => $r[6], 'val' => $r[7]);
    }
    fclose($fh);
}

$views = 0; $visitors = array(); $pages = array(); $refs = array();
$devices = array(); $sites = array(); $events = array(); $days = array();
foreach ($rows as $r) {
    $day = substr($r['t'], 0, 10);
    if ($r['e'] === '') {
        $views++;
        $pages[$r['p']] = (isset($pages[$r['p']]) ? $pages[$r['p']] : 0) + 1;
        $days[$day] = (isset($days[$day]) ? $days[$day] : 0) + 1;
        $d = $r['d']; $devices[$d] = (isset($devices[$d]) ? $devices[$d] : 0) + 1;
        $s = substr($r['l'], 0, 2); $sites[$s] = (isset($sites[$s]) ? $sites[$s] : 0) + 1;
        if ($r['ref'] !== '') { $refs[$r['ref']] = (isset($refs[$r['ref']]) ? $refs[$r['ref']] : 0) + 1; }
    } else {
        $key = $r['e'];
        if (!isset($events[$key])) { $events[$key] = array('n' => 0, 'sum' => 0, 'cnt' => 0); }
        $events[$key]['n']++;
        if ($r['val'] !== '' && is_numeric($r['val'])) { $events[$key]['sum'] += (int)$r['val']; $events[$key]['cnt']++; }
    }
    $visitors[$r['v']] = true;
}
arsort($pages); arsort($refs); arsort($devices); ksort($days);
uasort($events, function ($a, $b) { return $b['n'] - $a['n']; });
$uniq = count($visitors);
$maxDay = $days ? max($days) : 1;

function pct($n, $t) { return $t > 0 ? round($n / $t * 100) : 0; }
function e($s) { return htmlspecialchars((string)$s, ENT_QUOTES, 'UTF-8'); }
?><!DOCTYPE html>
<html lang="hr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex, nofollow">
<title>Analitika &middot; adventurespirit.hr</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{--o:#EF653F;--bg:#0f1117;--bg2:#1a1e2e;--tx:#e2e8f0;--mu:#94a3b8;--ln:rgba(255,255,255,.08)}
body{font-family:Inter,system-ui,-apple-system,sans-serif;background:var(--bg);color:var(--tx);line-height:1.6;padding:32px 20px}
.wrap{max-width:1060px;margin:0 auto}
h1{font-size:22px;font-weight:800;color:#fff;letter-spacing:-.3px}
.sub{font-size:13px;color:var(--mu);margin-top:4px}
.top{display:flex;justify-content:space-between;align-items:flex-end;gap:16px;flex-wrap:wrap;margin-bottom:28px;padding-bottom:20px;border-bottom:1px solid var(--ln)}
select{font-family:inherit;font-size:14px;color:#fff;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.14);border-radius:8px;padding:8px 12px;color-scheme:dark}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:14px;margin-bottom:28px}
.kpi{background:rgba(255,255,255,.03);border:1px solid var(--ln);border-radius:14px;padding:20px}
.kpi b{display:block;font-size:32px;font-weight:900;color:var(--o);line-height:1;font-variant-numeric:tabular-nums}
.kpi span{display:block;font-size:11px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:var(--mu);margin-top:8px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:18px}
.card{background:rgba(255,255,255,.03);border:1px solid var(--ln);border-radius:14px;padding:22px;margin-bottom:18px}
.card h2{font-size:11px;font-weight:700;letter-spacing:1.2px;text-transform:uppercase;color:var(--o);margin-bottom:16px}
table{width:100%;border-collapse:collapse;font-size:13.5px}
td{padding:8px 0;border-bottom:1px solid rgba(255,255,255,.05);vertical-align:top}
tr:last-child td{border-bottom:none}
td.n{text-align:right;color:#fff;font-weight:700;font-variant-numeric:tabular-nums;white-space:nowrap;padding-left:14px}
td.p{color:var(--mu);word-break:break-all}
.bar{position:relative}
.bar i{position:absolute;left:0;top:0;bottom:0;background:rgba(239,101,63,.14);border-radius:3px;z-index:0}
.bar span{position:relative;z-index:1;padding-left:6px}
.spark{display:flex;align-items:flex-end;gap:3px;height:70px;margin-top:6px}
.spark div{flex:1;background:var(--o);border-radius:2px 2px 0 0;min-height:2px;opacity:.85}
.spark div:hover{opacity:1}
.days{display:flex;gap:3px;font-size:9px;color:#5b6478;margin-top:6px}
.days span{flex:1;text-align:center}
.empty{font-size:13.5px;color:var(--mu)}
.note{font-size:12px;color:#6b7488;line-height:1.7;margin-top:26px;padding-top:18px;border-top:1px solid var(--ln)}
@media(max-width:600px){body{padding:20px 14px}.kpi b{font-size:26px}}
</style>
</head>
<body>
<div class="wrap">
  <div class="top">
    <div>
      <h1>Analitika &middot; adventurespirit.hr</h1>
      <p class="sub">Prvostrana, bez kolačića i bez pohrane IP adrese</p>
    </div>
    <form method="get">
      <select name="m" onchange="this.form.submit()">
        <?php foreach ($months as $m): ?>
        <option value="<?= e($m) ?>"<?= $m === $month ? ' selected' : '' ?>><?= e($m) ?></option>
        <?php endforeach; ?>
        <?php if (!$months): ?><option><?= e($month) ?></option><?php endif; ?>
      </select>
    </form>
  </div>

  <div class="kpis">
    <div class="kpi"><b><?= number_format($views, 0, ',', '.') ?></b><span>Pregleda stranica</span></div>
    <div class="kpi"><b><?= number_format($uniq, 0, ',', '.') ?></b><span>Posjetitelja (dnevno)</span></div>
    <div class="kpi"><b><?= $uniq ? round($views / $uniq, 1) : 0 ?></b><span>Stranica po posjetu</span></div>
    <div class="kpi"><b><?= array_sum(array_map(function ($x) { return $x['n']; }, $events)) ?></b><span>Događaja</span></div>
  </div>

  <div class="card">
    <h2>Pregledi po danima</h2>
    <?php if ($days): ?>
    <div class="spark">
      <?php foreach ($days as $d => $n): ?>
      <div style="height:<?= max(2, round($n / $maxDay * 70)) ?>px" title="<?= e($d) ?>: <?= $n ?>"></div>
      <?php endforeach; ?>
    </div>
    <div class="days">
      <?php $i = 0; $step = max(1, intval(count($days) / 8)); foreach ($days as $d => $n): ?>
      <span><?= ($i++ % $step === 0) ? e(substr($d, 8, 2)) : '' ?></span>
      <?php endforeach; ?>
    </div>
    <?php else: ?><p class="empty">Još nema podataka za ovaj mjesec.</p><?php endif; ?>
  </div>

  <div class="grid">
    <div>
      <div class="card">
        <h2>Najgledanije stranice</h2>
        <?php if ($pages): ?>
        <table>
          <?php $top = array_slice($pages, 0, 15, true); $mx = max($top); foreach ($top as $p => $n): ?>
          <tr><td class="p bar"><i style="width:<?= pct($n, $mx) ?>%"></i><span><?= e($p) ?></span></td><td class="n"><?= $n ?></td></tr>
          <?php endforeach; ?>
        </table>
        <?php else: ?><p class="empty">Nema podataka.</p><?php endif; ?>
      </div>

      <div class="card">
        <h2>Izvori posjeta</h2>
        <?php if ($refs): ?>
        <table>
          <?php foreach (array_slice($refs, 0, 12, true) as $r => $n): ?>
          <tr><td class="p"><?= e($r) ?></td><td class="n"><?= $n ?></td></tr>
          <?php endforeach; ?>
        </table>
        <?php else: ?><p class="empty">Sav promet je izravan ili bez zaglavlja izvora.</p><?php endif; ?>
      </div>
    </div>

    <div>
      <div class="card">
        <h2>Događaji</h2>
        <?php if ($events): ?>
        <table>
          <?php foreach ($events as $k => $v): ?>
          <tr>
            <td class="p"><?= e($k) ?><?php if ($v['cnt']): ?><br><span style="font-size:11.5px;color:#6b7488">prosjek <?= round($v['sum'] / $v['cnt']) ?></span><?php endif; ?></td>
            <td class="n"><?= $v['n'] ?></td>
          </tr>
          <?php endforeach; ?>
        </table>
        <?php else: ?><p class="empty">Nema zabilježenih događaja.</p><?php endif; ?>
      </div>

      <div class="card">
        <h2>Uređaji</h2>
        <table>
          <?php foreach ($devices as $d => $n): ?>
          <tr><td class="p"><?= e($d) ?></td><td class="n"><?= $n ?> &middot; <?= pct($n, $views) ?> %</td></tr>
          <?php endforeach; ?>
          <?php if (!$devices): ?><tr><td class="empty">Nema podataka.</td></tr><?php endif; ?>
        </table>
      </div>

      <div class="card">
        <h2>Jezična verzija</h2>
        <table>
          <?php foreach ($sites as $s => $n): ?>
          <tr><td class="p"><?= e(strtoupper($s)) ?></td><td class="n"><?= $n ?> &middot; <?= pct($n, $views) ?> %</td></tr>
          <?php endforeach; ?>
          <?php if (!$sites): ?><tr><td class="empty">Nema podataka.</td></tr><?php endif; ?>
        </table>
      </div>
    </div>
  </div>

  <p class="note">
    Podaci se prikupljaju bez kolačića. IP adresa se ne pohranjuje - koristi se samo za izračun
    dnevnog otiska posjetitelja, koji se svakodnevno mijenja jer se tajna rotira svaki dan u ponoć
    po UTC-u. Zbog toga se posjetitelj ne može pratiti kroz dane, pa za ovu obradu nije potrebna
    privola za kolačiće. Poštuju se zaglavlja Do Not Track i Global Privacy Control.
    Podaci se čuvaju u mjesečnim CSV datotekama u mapi <code>podaci/</code>.
  </p>
</div>
</body>
</html>
