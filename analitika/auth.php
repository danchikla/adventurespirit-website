<?php
/**
 * Zaštita nadzorne ploče lozinkom - Adventure Spirit d.o.o.
 *
 * Ne ovisi o cPanelu. Pri prvom otvaranju traži da postavite lozinku,
 * a njezin sažetak sprema u config.php koji ostaje samo na poslužitelju.
 * Lozinka se nigdje ne pohranjuje u čitljivom obliku.
 */

if (session_status() === PHP_SESSION_NONE) {
    session_set_cookie_params(array(
        'lifetime' => 0,
        'path'     => '/analitika/',
        'httponly' => true,
        'samesite' => 'Strict',
        'secure'   => (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off'),
    ));
    session_name('as_analitika');
    session_start();
}

$cfgFile = __DIR__ . '/config.php';
$cfg = is_readable($cfgFile) ? include $cfgFile : array();
$hash = isset($cfg['hash']) ? $cfg['hash'] : '';

$err = '';
$mode = ($hash === '') ? 'setup' : 'login';

// ── Odjava ───────────────────────────────────────────────────────
if (isset($_GET['odjava'])) {
    $_SESSION = array();
    session_destroy();
    header('Location: ' . strtok($_SERVER['REQUEST_URI'], '?'));
    exit;
}

// ── Postavljanje lozinke pri prvom otvaranju ─────────────────────
if ($mode === 'setup' && $_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['nova'])) {
    $p1 = (string)$_POST['nova'];
    $p2 = isset($_POST['ponovi']) ? (string)$_POST['ponovi'] : '';
    if (mb_strlen($p1) < 12) {
        $err = 'Lozinka mora imati najmanje 12 znakova.';
    } elseif ($p1 !== $p2) {
        $err = 'Lozinke se ne podudaraju.';
    } else {
        $new = "<?php\nreturn array('hash' => " . var_export(password_hash($p1, PASSWORD_DEFAULT), true) . ");\n";
        if (@file_put_contents($cfgFile, $new, LOCK_EX) === false) {
            $err = 'Ne mogu zapisati config.php. Provjerite prava na mapu analitika (755).';
        } else {
            @chmod($cfgFile, 0640);
            $_SESSION['ok'] = true;
            $_SESSION['t']  = time();
            header('Location: ' . strtok($_SERVER['REQUEST_URI'], '?'));
            exit;
        }
    }
}

// ── Prijava ──────────────────────────────────────────────────────
if ($mode === 'login' && $_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['lozinka'])) {
    // Usporavanje pokusaja pogadanja
    usleep(400000);
    if (password_verify((string)$_POST['lozinka'], $hash)) {
        session_regenerate_id(true);
        $_SESSION['ok'] = true;
        $_SESSION['t']  = time();
        header('Location: ' . strtok($_SERVER['REQUEST_URI'], '?'));
        exit;
    }
    $err = 'Pogrešna lozinka.';
}

// ── Provjera sjednice ────────────────────────────────────────────
$prijavljen = !empty($_SESSION['ok']) && isset($_SESSION['t']) && (time() - $_SESSION['t']) < 43200; // 12 h
if ($prijavljen) {
    $_SESSION['t'] = time();
    return;
}

// ── Obrazac ──────────────────────────────────────────────────────
header('Content-Type: text/html; charset=utf-8');
header('X-Robots-Tag: noindex, nofollow');
?><!DOCTYPE html>
<html lang="hr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex, nofollow">
<title><?= $mode === 'setup' ? 'Postavljanje lozinke' : 'Prijava' ?> &middot; Analitika</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{font-family:Inter,system-ui,-apple-system,sans-serif;background:#0f1117;color:#e2e8f0;
 line-height:1.6;min-height:100vh;display:flex;align-items:center;justify-content:center;padding:24px}
.box{width:100%;max-width:400px;background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.08);
 border-radius:16px;padding:34px}
h1{font-size:19px;font-weight:800;color:#fff;margin-bottom:8px}
p.s{font-size:13.5px;color:#94a3b8;line-height:1.7;margin-bottom:24px}
label{display:block;font-size:12.5px;font-weight:600;color:#fff;margin-bottom:7px}
input{width:100%;font-family:inherit;font-size:15px;color:#fff;background:rgba(255,255,255,.05);
 border:1px solid rgba(255,255,255,.14);border-radius:9px;padding:11px 13px;margin-bottom:16px;color-scheme:dark}
input:focus{outline:none;border-color:#EF653F}
button{width:100%;font-family:inherit;font-size:14.5px;font-weight:700;color:#fff;background:#EF653F;
 border:none;border-radius:9px;padding:12px;cursor:pointer;transition:background .2s}
button:hover{background:#c14b28}
.err{font-size:13px;color:#f87171;font-weight:600;margin-bottom:16px}
.note{font-size:12px;color:#6b7488;line-height:1.7;margin-top:20px;padding-top:16px;border-top:1px solid rgba(255,255,255,.08)}
</style>
</head>
<body>
<div class="box">
<?php if ($mode === 'setup'): ?>
  <h1>Postavite lozinku</h1>
  <p class="s">Nadzorna ploča još nije zaštićena. Postavite lozinku sada - dok to ne učinite, stranica je dostupna svakome tko zna adresu.</p>
  <?php if ($err): ?><p class="err"><?= htmlspecialchars($err, ENT_QUOTES, 'UTF-8') ?></p><?php endif; ?>
  <form method="post" autocomplete="off">
    <label for="nova">Nova lozinka</label>
    <input type="password" id="nova" name="nova" required minlength="12" autofocus autocomplete="new-password">
    <label for="ponovi">Ponovite lozinku</label>
    <input type="password" id="ponovi" name="ponovi" required minlength="12" autocomplete="new-password">
    <button type="submit">Postavi i uđi</button>
  </form>
  <p class="note">Najmanje 12 znakova. Sprema se samo kriptografski sažetak u <code>analitika/config.php</code>, nikad sama lozinka. Za promjenu lozinke obrišite tu datoteku i ponovno otvorite ovu stranicu.</p>
<?php else: ?>
  <h1>Analitika</h1>
  <p class="s">Unesite lozinku za pristup nadzornoj ploči.</p>
  <?php if ($err): ?><p class="err"><?= htmlspecialchars($err, ENT_QUOTES, 'UTF-8') ?></p><?php endif; ?>
  <form method="post" autocomplete="off">
    <label for="lozinka">Lozinka</label>
    <input type="password" id="lozinka" name="lozinka" required autofocus autocomplete="current-password">
    <button type="submit">Prijava</button>
  </form>
  <p class="note">Sjednica traje 12 sati neaktivnosti. Zaboravljenu lozinku ne možemo vratiti - obrišite <code>analitika/config.php</code> preko cPanel File Managera i postavite novu.</p>
<?php endif; ?>
</div>
</body>
</html>
<?php
exit;
