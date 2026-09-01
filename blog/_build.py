#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generator baze znanja za adventurespirit.hr - statican HTML, bez build alata."""
import io, os, re, html, json

ROOT = "/Users/dbara/adventurespirit-website"
BLOG = os.path.join(ROOT, "blog")
SITE = "https://adventurespirit.hr"
AUTHOR = "Daniel Bara, dr. sc."

# ══════════════════════════════════════════════════════════════════
# Zajednicki dijelovi
# ══════════════════════════════════════════════════════════════════
LOGO_SVG = '''<svg width="40" height="40" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
      <circle cx="50" cy="50" r="44" stroke="#EF653F" stroke-width="1.5" opacity=".25"/>
      <line x1="50" y1="6" x2="50" y2="14" stroke="#EF653F" stroke-width="2.5" opacity=".4"/>
      <line x1="50" y1="86" x2="50" y2="94" stroke="#EF653F" stroke-width="2" opacity=".3"/>
      <line x1="6" y1="50" x2="14" y2="50" stroke="#EF653F" stroke-width="2" opacity=".3"/>
      <line x1="86" y1="50" x2="94" y2="50" stroke="#EF653F" stroke-width="2" opacity=".3"/>
      <path d="M50 12 L40 45 L50 41 L60 45 Z" fill="#EF653F"/>
      <line x1="44" y1="36" x2="56" y2="36" stroke="#c14b28" stroke-width="2.5"/>
      <path d="M50 88 L45 70 L55 70 Z" fill="#EF653F" opacity=".75"/>
      <path d="M88 50 L70 45 L70 55 Z" fill="#EF653F" opacity=".65"/>
      <path d="M12 50 L30 45 L30 55 Z" fill="#EF653F" opacity=".65"/>
      <circle cx="50" cy="50" r="5" fill="#EF653F"/>
      <circle cx="50" cy="50" r="2.5" fill="#c14b28"/>
    </svg>'''
FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E"
  "%3Cpath d='M50 6L44 42h12Z' fill='%23EF653F'/%3E%3Cline x1='44' y1='33' x2='56' y2='33' stroke='%23EF653F' stroke-width='3'/%3E"
  "%3Cpath d='M50 94L44 68h12Z' fill='%23EF653F'/%3E%3Cpath d='M94 50L68 44v12Z' fill='%23EF653F'/%3E"
  "%3Cpath d='M6 50L32 44v12Z' fill='%23EF653F'/%3E%3Ccircle cx='50' cy='50' r='7' fill='%23EF653F'/%3E"
  "%3Ccircle cx='50' cy='50' r='4' fill='%23c14b28'/%3E%3C/svg%3E")
ICON_MAIL = '<svg viewBox="0 0 24 24"><path d="M4 4h16v16H4z"/><path d="M4 7l8 6 8-6"/></svg>'
ICON_PHONE = '<svg viewBox="0 0 24 24"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.4 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/></svg>'
ICON_LOCK = '<svg viewBox="0 0 24 24"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>'


def header(depth, active_blog=True):
    up = "../" * depth
    home = SITE + "/"
    return '''<div id="topwrap">
<div class="topbar">
  <span class="tb-legal">Adventure Spirit d.o.o. &middot; Zagreb</span>
  <span class="tb-contact">
    <a href="tel:+385955041496">''' + ICON_PHONE + '''+385 95 504 1496</a>
    <a href="mailto:info@adventurespirit.hr">''' + ICON_MAIL + '''info@adventurespirit.hr</a>
    <a href="https://app.adventurespirit.hr" target="_blank" rel="noopener">''' + ICON_LOCK + '''GRC Portal</a>
  </span>
</div>
<nav>
  <a href="/" class="nav-logo">
    ''' + LOGO_SVG + '''
    <div class="nav-logo-text">
      <span class="nav-logo-name">Adventure <span>Spirit</span></span>
      <span class="nav-logo-sub">Consulting</span>
    </div>
  </a>
  <ul class="nav-links" id="nav-links">
    <li><a href="/#onama">O nama</a></li>
    <li><a href="/#sigurnost">Usluge</a></li>
    <li><a href="/#sektori">Sektori</a></li>
    <li><a href="/blog/"''' + (' class="active"' if active_blog else '') + '''>Baza znanja</a></li>
    <li><a href="/#reference">Reference</a></li>
    <li><a href="/#faq">Česta pitanja</a></li>
    <li><a href="/#kontakt">Kontakt</a></li>
    <li><a href="https://app.adventurespirit.hr" target="_blank" rel="noopener" class="nav-cta">Portal</a></li>
  </ul>
  <button class="nav-toggle" onclick="document.getElementById('nav-links').classList.toggle('open')" aria-label="Izbornik">
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M3 12h18M3 6h18M3 18h18"/></svg>
  </button>
</nav>
</div>'''


FOOTER = '''<footer>
  <div class="container">
    <div class="footer-inner">
      <div class="footer-brand">
        <a href="/" style="display:flex;align-items:center;gap:10px;text-decoration:none">
          <svg width="32" height="32" viewBox="0 0 100 100" fill="none">
            <circle cx="50" cy="50" r="44" stroke="#EF653F" stroke-width="1.5" opacity=".2"/>
            <path d="M50 12 L41 46 L50 41 L59 46 Z" fill="#EF653F"/>
            <line x1="44" y1="37" x2="56" y2="37" stroke="#c14b28" stroke-width="3"/>
            <path d="M50 88 L45 70 L55 70 Z" fill="#EF653F" opacity=".7"/>
            <circle cx="50" cy="50" r="5" fill="#EF653F"/>
          </svg>
          <span style="font-size:16px;font-weight:800;color:#fff">Adventure <span style="color:#EF653F">Spirit</span></span>
        </a>
        <p>Kibernetička sigurnost, GRC compliance i upravljanje rizicima - preko 20 godina iskustva u službi vašeg poslovanja.</p>
        <p class="footer-legal">
          Adventure Spirit d.o.o.<br>
          Tržišni naziv: Adventure Spirit Consulting<br>
          Zagreb, Republika Hrvatska<br>
          <!-- TODO: upisati punu adresu, OIB, MBS i PDV broj -->
          OIB: dostupno na zahtjev<br>
          <a href="tel:+385955041496">+385 95 504 1496</a><br>
          <a href="mailto:info@adventurespirit.hr">info@adventurespirit.hr</a>
        </p>
      </div>
      <div class="footer-col">
        <h4>Baza znanja</h4>
        __KBLINKS__
      </div>
      <div class="footer-col">
        <h4>Usluge</h4>
        <a href="/#sigurnost">ZKS / NIS2</a>
        <a href="/#sigurnost">GDPR</a>
        <a href="/#sigurnost">ISO 27001</a>
        <a href="/#sigurnost">DORA</a>
        <a href="/#sektori">Sektori</a>
      </div>
      <div class="footer-col">
        <h4>Tvrtka</h4>
        <a href="/#onama">O konzultantu</a>
        <a href="/#reference">Reference</a>
        <a href="/#faq">Česta pitanja</a>
        <a href="/#kontakt">Kontakt</a>
        <a href="https://app.adventurespirit.hr" target="_blank" rel="noopener">GRC Portal</a>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; 2026 Adventure Spirit d.o.o. - Sva prava pridržana</span>
      <span style="display:flex;gap:16px">
        <a href="/blog/feed.xml">RSS</a>
        <a href="/uvjeti/">Uvjeti korištenja</a>
        <a href="/privatnost/">Privatnost</a>
      </span>
    </div>
  </div>
</footer>'''


def page(title, desc, body, canonical, extra_head="", og_type="website", ld=None):
    ldjs = ""
    if ld:
        ldjs = "\n".join('<script type="application/ld+json">\n%s\n</script>'
                         % json.dumps(o, ensure_ascii=False, indent=2) for o in ld)
    return '''<!DOCTYPE html>
<html lang="hr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>%s</title>
<meta name="description" content="%s">
<link rel="canonical" href="%s">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
<meta name="theme-color" content="#0f1117">
<meta name="author" content="%s">
<meta property="og:type" content="%s">
<meta property="og:site_name" content="Adventure Spirit Consulting">
<meta property="og:locale" content="hr_HR">
<meta property="og:url" content="%s">
<meta property="og:title" content="%s">
<meta property="og:description" content="%s">
<meta property="og:image" content="%s/mmew/img/og.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="%s">
<meta name="twitter:description" content="%s">
<link rel="alternate" type="application/rss+xml" title="Baza znanja - Adventure Spirit Consulting" href="/blog/feed.xml">
<link rel="icon" type="image/svg+xml" href="%s">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/blog/assets/blog.css">
%s
</head>
<body>
%s
%s
%s
<script>
document.querySelectorAll('#nav-links a').forEach(function(a){
  a.addEventListener('click', function(){ document.getElementById('nav-links').classList.remove('open'); });
});
</script>
</body>
</html>
''' % (html.escape(title), html.escape(desc), canonical, AUTHOR, og_type, canonical,
       html.escape(title), html.escape(desc), SITE, html.escape(title), html.escape(desc),
       FAVICON, extra_head, body, ldjs, "")


# ══════════════════════════════════════════════════════════════════
# 13 mjera - sluzbeni nazivi iz Priloga II. Uredbe / Priloga B ZSIS-a
# ══════════════════════════════════════════════════════════════════
MJERE = [
 (1, "Predanost i odgovornost osoba odgovornih za provedbu mjera upravljanja kibernetičkim sigurnosnim rizicima", 11,
     "Uprava odobrava politiku, imenuje odgovorne osobe, osigurava resurse i redovito se izvještava. Bez ovoga ostale mjere nemaju vlasnika."),
 (2, "Upravljanje programskom i sklopovskom imovinom", 9,
     "Inventar sve imovine, izdvajanje kritične imovine, klasifikacija podataka i pravila za uklanjanje i ponovnu upotrebu opreme."),
 (3, "Upravljanje rizicima", 8,
     "Dokumentiran proces procjene rizika po all-hazards načelu, razina i kritičnost svakog rizika, vlasnik rizika i plan obrade."),
 (4, "Sigurnost ljudskih potencijala i digitalnih identiteta", 12,
     "Provjere pri zapošljavanju, ugovorne obveze, upravljanje pravima pristupa kroz cijeli životni ciklus i odvojeni računi za administratore."),
 (5, "Osnovne prakse kibernetičke higijene", 11,
     "Zakrpe, sigurnosne kopije, zaštita krajnjih točaka, sigurnost e-pošte i preglednika, edukacija i podizanje svijesti zaposlenika."),
 (6, "Osiguravanje kibernetičke sigurnosti mreže", 5,
     "Segmentacija, zaštita perimetra, nadzor mrežnog prometa i sigurna konfiguracija mrežne opreme."),
 (7, "Kontrola fizičkog i logičkog pristupa mrežnim i informacijskim sustavima", 6,
     "Načelo najmanje privilegije, višefaktorska autentifikacija, upravljanje povlaštenim pristupom i evidencija pristupa."),
 (8, "Sigurnost lanca opskrbe", 6,
     "Minimalni sigurnosni zahtjevi za dobavljače, ugovorne klauzule, procjena rizika trećih strana i praćenje kroz vrijeme."),
 (9, "Sigurnost u razvoju i održavanju mrežnih i informacijskih sustava", 6,
     "Sigurnosni zahtjevi u razvoju, odvojena okruženja, upravljanje promjenama i testiranje prije puštanja u rad."),
 (10, "Kriptografija", 6,
     "Pravila primjene kriptografije, zaštita podataka u prijenosu i mirovanju, upravljanje ključevima i priprema na kvantno otpornu kriptografiju."),
 (11, "Postupanje s incidentima", 6,
     "Detekcija, klasifikacija i eskalacija, plan odgovora, prijava nadležnom CSIRT-u u propisanim rokovima i analiza nakon incidenta."),
 (12, "Kontinuitet poslovanja i upravljanje kibernetičkim krizama", 8,
     "Analiza poslovnog utjecaja, planovi kontinuiteta i oporavka, upravljanje krizom i redovito testiranje planova."),
 (13, "Fizička sigurnost", 5,
     "Zaštita prostora s opremom, kontrola ulaska, zaštita od požara i vode te sigurnost napajanja i kabliranja."),
]


def mjere_tablica():
    rows = "\n".join(
      '      <tr><td class="num">%02d</td><td><strong>%s</strong><br><span style="color:#94a3b8;font-size:13.5px">%s</span></td><td class="num">%d</td></tr>'
      % (br, naziv, opis, pod) for br, naziv, pod, opis in MJERE)
    return '''<div class="tbl-wrap">
  <table>
    <thead><tr><th>Mjera</th><th>Naziv i što traži u praksi</th><th>Podmjera</th></tr></thead>
    <tbody>
%s
      <tr><td class="num">&Sigma;</td><td><strong>Ukupno</strong></td><td class="num">99</td></tr>
    </tbody>
  </table>
</div>''' % rows


# ══════════════════════════════════════════════════════════════════
# Clanci
# ══════════════════════════════════════════════════════════════════
CTA = '''<div class="art-cta">
  <h3>Ne znate gdje stojite?</h3>
  <p>Pola sata razgovora i ništa vas ne obvezuje. Kad završimo, znate što trebate napraviti i kojim redom.</p>
  <div class="cta-btns">
    <a href="/#kontakt" class="btn-primary">Dogovorite razgovor</a>
    <a href="/#sigurnost" class="btn-outline">Pogledajte usluge</a>
  </div>
</div>'''

ARTICLES = []

# ─── 1 ────────────────────────────────────────────────────────────
ARTICLES.append(dict(
 slug="kategorizacija-prema-zks-u",
 cat="ZKS / NIS2",
 catkey="zks",
 date="2026-09-01",
 read=7,
 title="Kategorizacija prema ZKS-u: ključni ili važni subjekt, i što iz toga slijedi",
 lead="Kategoriju ne birate i ne prijavljujete se za nju. Dobit ćete je pismom, a od dana dostave teče rok. Objašnjavamo tko odlučuje, po čemu, i što se konkretno mijenja ovisno o tome u koju ste skupinu svrstani.",
 desc="Kako se određuje jeste li ključni ili važni subjekt prema Zakonu o kibernetičkoj sigurnosti, koji rokovi teku od obavijesti o kategorizaciji i po čemu se obveze dviju skupina razlikuju.",
 body='''
<p>Zakon o kibernetičkoj sigurnosti (NN 14/2024) dijeli obveznike u dvije skupine: <strong>ključne</strong> i <strong>važne subjekte</strong>. Razlika nije kozmetička. Ona određuje razinu na kojoj morate provesti mjere, tko provjerava jeste li ih proveli, i koliko vas ta provjera košta.</p>

<h2>Kategoriju određuju sektor i veličina, uz iznimke</h2>
<p>Polazište su prilozi Zakona koji nabrajaju sektore. Unutar sektora, kategorija se u pravilu izvodi iz veličine subjekta prema kriterijima za srednje i velike poduzetnike. To je pravilo. Zanimljive su iznimke.</p>
<p>Kod <strong>tijela državne uprave</strong> i kod <strong>određenih kritičnih zdravstvenih djelatnosti</strong> veličina nije mjerilo. Ondje kategorija proizlazi iz same djelatnosti, pa mala ustanova može biti ključni subjekt jednako kao i velika. To je najčešći izvor iznenađenja: organizacija koja se po broju zaposlenih smatra malom otvori pismo i pročita da je ključni subjekt.</p>
<div class="callout">
  <div class="c-label">Praktična posljedica</div>
  <p>Ne pokušavajte sami zaključiti u koju kategoriju spadate i na temelju toga planirati proračun. Sektorska iznimka može promijeniti cijeli scenarij. Planirajte za nepovoljniji ishod dok ne dobijete pisanu obavijest.</p>
</div>

<h2>Što se stvarno mijenja s kategorijom</h2>
<p>Obje skupine provode <strong>istih 13 mjera</strong> iz Priloga II. Uredbe o kibernetičkoj sigurnosti (NN 135/2024). Ono što se razlikuje su dvije stvari: razina provedbe i način provjere.</p>
<div class="tbl-wrap">
  <table>
    <thead><tr><th></th><th>Važni subjekt</th><th>Ključni subjekt</th></tr></thead>
    <tbody>
      <tr><td><strong>Mjere</strong></td><td>Istih 13 mjera</td><td>Istih 13 mjera</td></tr>
      <tr><td><strong>Razina provedbe</strong></td><td>U pravilu niža razina</td><td>U pravilu viša razina</td></tr>
      <tr><td><strong>Provjera usklađenosti</strong></td><td>Samoprocjena</td><td>Neovisna revizija</td></tr>
      <tr><td><strong>Tko provjerava</strong></td><td>Subjekt sam, prema smjernicama</td><td>Ovlašteni vanjski pružatelj, kod tijela državne uprave nadležno tijelo</td></tr>
      <tr><td><strong>Trošak provjere</strong></td><td>Interni rad</td><td>Vanjski angažman</td></tr>
    </tbody>
  </table>
</div>
<p>Napomena koja se često previdi: <strong>i samoprocjena je formalni postupak</strong>. Nije riječ o internom mišljenju nego o bodovanju prema propisanom okviru, s dokazima koji moraju postojati u trenutku procjene. Razlika prema reviziji je u tome tko drži olovku, ne u tome je li potrebna dokazna baza.</p>

<h2>Rokovi teku od obavijesti, ne od stupanja Zakona na snagu</h2>
<p>Ovo je najskuplji nesporazum u praksi. Zakon je na snazi od 2024., ali vaš rok ne teče od tada.</p>
<ul>
  <li><strong>30 dana</strong> - rok u kojem vas nadležno tijelo mora obavijestiti o provedenoj kategorizaciji ili njezinoj izmjeni.</li>
  <li><strong>12 mjeseci</strong> - rok za usklađivanje, računa se od dostave te obavijesti.</li>
  <li><strong>Do dvije dodatne godine</strong> - okvir unutar kojeg se provodi provjera usklađenosti, neovisnom revizijom ili samoprocjenom, ovisno o kategoriji.</li>
  <li><strong>60 dana do 6 mjeseci</strong> - rok koji nadležno tijelo određuje kad se kategorija promijeni, razmjerno opsegu i složenosti novih obveza.</li>
</ul>
<div class="callout">
  <div class="c-label">Gdje se gubi vrijeme</div>
  <p>Prvo tromjesečje se u pravilu potroši na interno imenovanje osobe koja će voditi posao. Rok u međuvremenu teče. Ako je obavijest stigla, gap analiza može krenuti prije nego što je imenovanje formalizirano - popis imovine i registar rizika trebaju vam u svakom slučaju.</p>
</div>

<h2>Što napraviti u prvom tjednu nakon obavijesti</h2>
<ol>
  <li><strong>Zabilježite datum dostave.</strong> Ne datum pisma, nego datum dostave. Od njega računate svih dvanaest mjeseci.</li>
  <li><strong>Utvrdite razinu provedbe</strong> koja se na vas primjenjuje i koje ste sektorske obveze dobili uz kategorizaciju.</li>
  <li><strong>Imenujte odgovornu osobu</strong> i osigurajte joj pristup upravi. Mjera 1 iz Priloga II. traži upravo to, i ocjenjuje se.</li>
  <li><strong>Napravite popis imovine.</strong> Bez inventara ne možete napraviti procjenu rizika, a bez procjene rizika ne prolazi gotovo nijedna druga mjera.</li>
  <li><strong>Provjerite preklapanja.</strong> Ako imate ISO 27001, DORA obveze ili uspostavljen GDPR sustav, dio dokazne baze već postoji. Mapirajte prije nego što počnete pisati nove dokumente.</li>
</ol>

<h2>Ako mislite da ste pogrešno kategorizirani</h2>
<p>Kategorizacija se temelji na podacima o sektoru i veličini koje tijelo ima. Ako ti podaci nisu točni, ili se vaša djelatnost promijenila, to je pitanje za nadležno tijelo, a ne razlog da se rok ignorira. Do rješenja, rok teče prema zaprimljenoj obavijesti.</p>
''',
 sources=[
   ('Zakon o kibernetičkoj sigurnosti, NN 14/2024', 'https://narodne-novine.nn.hr/clanci/sluzbeni/2024_02_14_222.html'),
   ('Uredba o kibernetičkoj sigurnosti, NN 135/2024', 'https://narodne-novine.nn.hr/clanci/sluzbeni/2024_11_135_2217.html'),
   ('NCSC-HR - kategorizacija subjekata obveznika', 'https://ncsc.hr/hr/zapoceo-proces-kategorizacije-subjekata-obveznika-zakona-o-kibernetickoj-sigurnosti'),
 ]))

# ─── 2 ────────────────────────────────────────────────────────────
ARTICLES.append(dict(
 slug="trinaest-mjera-priloga-ii",
 cat="ZKS / NIS2",
 catkey="zks",
 date="2026-09-01",
 read=9,
 featured=True,
 title="13 mjera, 99 podmjera, 132 kontrole: anatomija Priloga II. Uredbe",
 lead="Uredba o kibernetičkoj sigurnosti ne govori o deset NIS2 mjera nego o trinaest svojih. Ispod njih je 99 podmjera, a iza njih katalog od 132 kontrole s bodovnim pragovima. Ovo je karta cijele strukture, mjeru po mjeru.",
 desc="Potpun pregled 13 mjera upravljanja kibernetičkim sigurnosnim rizicima iz Priloga II. Uredbe NN 135/2024: broj podmjera po mjeri, što svaka traži u praksi i kako je povezana s katalogom kontrola.",
 body='''
<p>Najčešća greška u pripremi za ZKS počinje na krivom popisu. Direktiva NIS2 u članku 21. stavku 2. nabraja deset skupina mjera, pa se u prezentacijama i ponudama i dalje vrti brojka deset. <strong>Hrvatska Uredba o kibernetičkoj sigurnosti (NN 135/2024) razrađuje ih u trinaest mjera</strong>, i po njima ćete biti ocijenjeni.</p>
<p>Razlika nije samo u brojanju. Uredba je mjere raspisala u podmjere, a Zavod za sigurnost informacijskih sustava je uz njih objavio okvir za evaluaciju s konkretnim kontrolama i bodovnim pragovima. Ako pripremate dokazne baze prema NIS2 popisu od deset točaka, dio dokaza neće imati gdje sjesti.</p>

<div class="callout">
  <div class="c-label">Struktura u tri razine</div>
  <p><strong>Mjera</strong> ima cilj i naziv. Unutar nje su <strong>podmjere</strong> - konkretne obveze formulirane glagolom (razviti, dokumentirati, implementirati, ažurirati). Uz svaku podmjeru ide <strong>set kontrola</strong> iz kataloga, a svaka kontrola ima propisan minimalni bodovni prag za osnovnu, srednju i naprednu razinu.</p>
</div>

<h2>Svih trinaest mjera</h2>
<p>Nazivi su službeni, iz Priloga II. Uredbe odnosno Priloga B ZSIS-ovog okvira za evaluaciju. Broj podmjera je prebrojan iz tog okvira i zbraja se na točno 99.</p>
__TABLICA__
<p>Zbroj kontrola po mjerama veći je od 132 jer se pojedine kontrole koriste u više mjera. Katalog kontrola sadrži 132 jedinstvene oznake, grupirane u trinaest prefiksa (POL, INV, RIZ, DID, EDU, UPR, NAD, RES, ORG, SKM, POD, SRZ, FIZ).</p>

<h2>Gdje je najviše posla</h2>
<p>Ako gledate samo broj podmjera, težište je jasno: <strong>mjera 4 (Sigurnost ljudskih potencijala i digitalnih identiteta)</strong> s dvanaest podmjera, te <strong>mjere 1 i 5</strong> s po jedanaest. To nije slučajno. Sve tri su organizacijske, ne tehničke.</p>
<p>Praktična posljedica je neugodna za timove koji ZKS shvate kao IT projekt: najveći dio dokazne baze ne nastaje u serverskoj sobi nego u kadrovskoj službi, na sjednicama uprave i u evidencijama edukacija. Vatrozid se konfigurira u jednom danu. Dokaz da je uprava odobrila politiku, dobila izvješće i osigurala resurse ne može se retroaktivno proizvesti.</p>

<h2>Tri razine provedbe</h2>
<p>Svaka mjera se ocjenjuje na jednoj od tri razine: <strong>osnovnoj, srednjoj ili naprednoj</strong>. Razina se ne bira slobodno - proizlazi iz kategorije subjekta i iz procjene rizika. Ista podmjera na naprednoj razini traži viši rezultat na istim kontrolama, a ponekad i dodatne kontrole koje se na osnovnoj razini uopće ne primjenjuju.</p>
<p>U okviru za evaluaciju te uvjetne kontrole označene su zvjezdicom. Primjer je podmjera 10.6, koja traži primjenu kvantno otporne kriptografije razmjerno procijenjenom riziku. Na svim je razinama označena kao uvjetna, što znači da vas procjena rizika može dovesti do obveze koju biste po samoj kategoriji preskočili.</p>

<h2>Kako to izgleda kad se prevede u plan</h2>
<p>Devedeset devet podmjera zvuči kao nesavladiv popis dok se ne posloži po tri kriterija:</p>
<ul>
  <li><strong>Što već imate.</strong> Organizacija s ISO 27001 sustavom u pravilu ima pokriven znatan dio mjera 2, 3, 7, 8 i 12. To se mapira, ne piše ispočetka.</li>
  <li><strong>Što nema vlasnika.</strong> Podmjera bez imenovanog vlasnika neće biti napravljena bez obzira na to koliko je jednostavna.</li>
  <li><strong>Što ima najduže vrijeme dozrijevanja.</strong> Politika se napiše u tjedan dana. Godišnji ciklus izvještavanja uprave, testiranje plana kontinuiteta i evidencija edukacija zahtijevaju kalendarsko vrijeme koje se ne može stisnuti.</li>
</ul>
<p>Zadnja stavka objašnjava zašto rok od dvanaest mjeseci nije velikodušan. Nekoliko mjera dokazuje se zapisima koji nastaju tek kad ciklus jednom prođe.</p>

<div class="note">
  <p><strong>Napomena o verzijama.</strong> Brojke u ovom tekstu odnose se na Prilog B ZSIS-ovog okvira za evaluaciju, verzija 1.0. Katalog kontrola i pragovi mogu se mijenjati kroz nove verzije smjernica, pa prije formalne samoprocjene provjerite koja je verzija na snazi.</p>
</div>
''',
 sources=[
   ('Uredba o kibernetičkoj sigurnosti, NN 135/2024, Prilog II.', 'https://narodne-novine.nn.hr/clanci/sluzbeni/2024_11_135_2217.html'),
   ('ZSIS - Prilog B, Okvir za evaluaciju mjera upravljanja kibernetičkim sigurnosnim rizicima, v1.0', 'https://www.zsis.hr/UserDocsImages/Samoprocjena/Prilog%20B%20-%20Okvir%20za%20evaluaciju.pdf'),
   ('Direktiva (EU) 2022/2555 (NIS2), čl. 21.', 'https://eur-lex.europa.eu/legal-content/HR/TXT/?uri=CELEX:32022L2555'),
 ]))

# ─── 3 ────────────────────────────────────────────────────────────
ARTICLES.append(dict(
 slug="kako-se-boduje-samoprocjena",
 cat="Samoprocjena",
 catkey="samoprocjena",
 date="2026-09-01",
 read=6,
 title="Kako se zapravo boduje samoprocjena: pragovi Pi i T",
 lead="Možete zadovoljiti svaku pojedinačnu kontrolu i svejedno pasti na podmjeri. Okvir za evaluaciju ima dva praga, a drugi je onaj koji iznenađuje. Evo kako formula radi i što to znači za planiranje.",
 desc="Objašnjenje bodovnog sustava iz ZSIS-ovog okvira za evaluaciju: minimalni prag po kontroli, dodatni prag prosjeka po podmjeri i zašto formalno ispunjavanje kriterija nije dovoljno.",
 body='''
<p>Samoprocjena prema Uredbi nije upitnik s odgovorima da i ne. Riječ je o bodovanju s dva praga koja moraju biti zadovoljena istovremeno, a organizacije koje to shvate kasno u pravilu otkriju da su posao radile prema krivom cilju.</p>

<h2>Dva praga, ne jedan</h2>
<p>Svaka podmjera ima svoj set kontrola. Za svaku kontrolu okvir propisuje minimalni bodovni prag za prolaz, ovisno o razini provedbe. Ali to nije sve.</p>
<div class="callout">
  <div class="c-label">Uvjet za prolaz podmjere</div>
  <p><strong>1.</strong> Svaka pojedina kontrola mora dosegnuti svoj minimalni prag (O<sub>i</sub> &ge; P<sub>i</sub>, za svaku kontrolu i).</p>
  <p><strong>2.</strong> Prosječna ocjena svih kontrola unutar podmjere mora dosegnuti dodatni prag (&sum;O<sub>i</sub> / n &ge; T).</p>
  <p>Oba uvjeta moraju vrijediti. Ako prosjek ne prolazi, podmjera nije zadovoljena bez obzira na to što je svaka kontrola pojedinačno prošla.</p>
</div>
<p>Primjer iz okvira: podmjera 3.2, procjena rizika nad kritičnom imovinom. Na osnovnoj razini kontrole imaju pragove &ge;3, &ge;2, &ge;2 i &ge;2, a dodatni prag prosjeka je &gt;2,5. Organizacija koja svaku kontrolu dovede točno na minimum dobiva prosjek od 2,25 i <strong>pada podmjeru</strong> unatoč tome što je formalno zadovoljila svaki pojedinačni kriterij.</p>

<h2>Zašto je drugi prag uopće uveden</h2>
<p>Okvir to izrijekom obrazlaže: dodatni prag služi kao završna provjera stvarne primjene i integracije kontrola, a ne samo formalnog ispunjavanja kriterija. Cilj je spriječiti sustav u kojem svaka kutijica ima kvačicu, a mjera u praksi ne funkcionira.</p>
<p>Ista logika ide i korak dalje. Ako se utvrdi da mjera unatoč formalno zadovoljenim kontrolama nije djelotvorna ili nije integrirana u sustav upravljanja rizicima, može biti ocijenjena kao nezadovoljavajuća. To je prostor za prosudbu, i on postoji namjerno.</p>

<h2>Što to mijenja u planiranju</h2>
<ul>
  <li><strong>Ne ciljajte minimum.</strong> Planiranje "taman koliko treba" po pojedinačnoj kontroli matematički vodi u pad na prosjeku. Ciljajte prag prosjeka, pa unatrag rasporedite kontrole.</li>
  <li><strong>Jedna slaba kontrola ruši podmjeru dvaput.</strong> Ne prolazi sama i istovremeno vuče prosjek. Kontrole s najnižom ocjenom najisplativije su za popravljanje.</li>
  <li><strong>Prosjek se računa unutar podmjere, ne unutar mjere.</strong> Dobar rezultat na jednoj podmjeri ne kompenzira lošu drugu.</li>
  <li><strong>Ocjene dodjeljujete prema katalogu kontrola.</strong> Ocjenjivanje "po osjećaju" ne prolazi provjeru jer se svaka ocjena mora moći obrazložiti dokazom.</li>
</ul>

<h2>Razine mijenjaju pragove, ne kontrole</h2>
<p>Prijelaz s osnovne na srednju razinu u pravilu ne donosi novi popis kontrola nego više pragove na istima. Tipičan uzorak je pomak s &ge;2 na &ge;3, uz dodatni prag prosjeka koji se pomiče s 2,0 na 3,0. To je važno jer znači da organizacija koja se pripremala za osnovnu razinu, pa je prekategorizirana, ne mora graditi novi sustav - mora produbiti postojeći.</p>
<p>Iznimka su kontrole označene zvjezdicom, koje se primjenjuju uvjetno, ovisno o procjeni rizika. Njih procjena rizika može aktivirati i na osnovnoj razini.</p>

<h2>Praktična provjera prije formalne samoprocjene</h2>
<p>Prije nego što se samoprocjena preda, isplati se napraviti internu provjeru koja simulira postupak: ocijeniti svaku kontrolu, izračunati prosjeke po podmjerama i pogledati koje podmjere padaju na drugom pragu. Popis će gotovo uvijek biti kraći nego što se očekuje, i gotovo uvijek će sadržavati podmjere za koje je tim bio siguran da su gotove.</p>

<div class="note">
  <p><strong>Napomena o verzijama.</strong> Formula i pragovi iz ovog teksta odnose se na Prilog B, verzija 1.0. Prije formalne samoprocjene provjerite koja je verzija okvira na snazi.</p>
</div>
''',
 sources=[
   ('ZSIS - Prilog B, Okvir za evaluaciju mjera upravljanja kibernetičkim sigurnosnim rizicima, v1.0', 'https://www.zsis.hr/UserDocsImages/Samoprocjena/Prilog%20B%20-%20Okvir%20za%20evaluaciju.pdf'),
   ('Uredba o kibernetičkoj sigurnosti, NN 135/2024, čl. 42. i 51. do 54.', 'https://narodne-novine.nn.hr/clanci/sluzbeni/2024_11_135_2217.html'),
 ]))

# ─── 4 ────────────────────────────────────────────────────────────
ARTICLES.append(dict(
 slug="rokovi-prijave-incidenta",
 cat="Incidenti",
 catkey="incidenti",
 date="2026-09-01",
 read=6,
 title="24 sata, 72 sata, 30 dana: rokovi koji teku paralelno",
 lead="Rokovi prijave značajnog incidenta ne zbrajaju se i ne čekaju jedan drugoga. A ako je incidentom zahvaćena i povreda osobnih podataka, uz njih usporedno teče i četvrti rok, prema drugom propisu i drugom tijelu.",
 desc="Rokovi prijave značajnog kibernetičkog incidenta prema ZKS-u: rano upozorenje u 24 sata, obavijest u 72 sata, završno izvješće u 30 dana, te usporedna prijava AZOP-u prema članku 33. Opće uredbe.",
 body='''
<p>Prijava incidenta je mjera koja se najlakše opiše i najteže izvede. Razlog je jednostavan: sve ostale mjere radite u radno vrijeme, a ovu u tri ujutro, dok istovremeno pokušavate zaustaviti ono što se događa.</p>

<h2>Tri roka prema ZKS-u</h2>
<div class="tbl-wrap">
  <table>
    <thead><tr><th>Rok</th><th>Što se šalje</th><th>Sadržaj</th></tr></thead>
    <tbody>
      <tr><td class="num">24 sata</td><td>Rano upozorenje</td><td>Da se dogodio značajan incident, prva procjena je li posljedica protupravne radnje i može li imati prekogranični učinak.</td></tr>
      <tr><td class="num">72 sata</td><td>Obavijest o incidentu</td><td>Ažurirana procjena, pokazatelji ugroženosti, ozbiljnost i utjecaj.</td></tr>
      <tr><td class="num">30 dana</td><td>Završno izvješće</td><td>Detaljan opis, vrsta prijetnje i uzrok, primijenjene i planirane mjere, prekogranični učinak.</td></tr>
    </tbody>
  </table>
</div>
<p>Rokovi se računaju <strong>od saznanja o incidentu</strong>, ne od njegovog nastanka i ne od trenutka kad je istraga završena. To je razlika koja odlučuje jeste li u roku.</p>

<div class="callout">
  <div class="c-label">Najčešća pogreška</div>
  <p>Rok od 24 sata nije rok za objašnjenje što se dogodilo. To je rok da javite <em>da</em> se nešto dogodilo. Timovi koji čekaju da razumiju incident prije nego što pošalju rano upozorenje redovito probiju prvi rok, a nisu ništa dobili zauzvrat.</p>
</div>

<h2>Četvrti rok koji teče usporedno</h2>
<p>Ako je incidentom zahvaćena i povreda osobnih podataka, uz rokove iz ZKS-a <strong>usporedno teče rok od 72 sata za prijavu Agenciji za zaštitu osobnih podataka</strong>, prema članku 33. Opće uredbe o zaštiti podataka. Riječ je o zasebnoj prijavi, drugom tijelu, s drugim sadržajem.</p>
<p>Ta dva roka ne poništavaju jedan drugoga i ne teku jedan za drugim. Ransomware koji je zaustavio proizvodnju i istovremeno iznio kadrovsku bazu proizvodi obje obveze u istom satu.</p>

<h2>Što mora biti spremno prije, a ne poslije</h2>
<p>Rokovi su izvediviji nego što izgledaju, ali samo ako se pripreme unaprijed. Konkretno:</p>
<ul>
  <li><strong>Kriterij značajnosti.</strong> Netko mora moći u roku od sat vremena reći je li ovo značajan incident. Ako se to pitanje prvi put postavlja tijekom incidenta, sat već teče.</li>
  <li><strong>Imenovana osoba i zamjena.</strong> Incidenti se ne događaju samo radnim danom. Ako prijavu može poslati jedna osoba, imate rizik dostupnosti u samoj mjeri.</li>
  <li><strong>Pripremljeni obrasci.</strong> Predložak ranog upozorenja s poljima koja se popunjavaju, ne dokument koji se piše.</li>
  <li><strong>Kontaktni podaci nadležnog CSIRT-a</strong> i pristupni podaci za kanal prijave, provjereni prije nego što zatrebaju.</li>
  <li><strong>Odluka o paralelnoj prijavi.</strong> Tko procjenjuje je li zahvaćena i povreda osobnih podataka i tko onda šalje prijavu AZOP-u.</li>
  <li><strong>Zapisi.</strong> Vrijeme saznanja, tko je što odlučio i kad je što poslano. To je dokaz da ste bili u roku.</li>
</ul>

<h2>Test koji vrijedi više od plana</h2>
<p>Plan odgovora na incident koji nikad nije isproban dokumentira namjeru, ne sposobnost. Vježba na stolu u trajanju od dva sata, sa scenarijem i stvarnim mjerenjem vremena do pripremljenog ranog upozorenja, otkrit će više nego još jedan krug uređivanja dokumenta. U praksi se najčešće otkrije da nitko nije siguran tko donosi odluku o značajnosti.</p>

<div class="note">
  <p>Prijava incidenta pokriva mjeru 11 iz Priloga II. Uredbe, ali dokazna baza se preklapa s mjerom 12 (kontinuitet poslovanja i upravljanje kibernetičkim krizama). Ako plan odgovora na incident i plan kontinuiteta pišete kao dva nepovezana dokumenta, posao radite dvaput.</p>
</div>
''',
 sources=[
   ('Zakon o kibernetičkoj sigurnosti, NN 14/2024', 'https://narodne-novine.nn.hr/clanci/sluzbeni/2024_02_14_222.html'),
   ('Uredba o kibernetičkoj sigurnosti, NN 135/2024', 'https://narodne-novine.nn.hr/clanci/sluzbeni/2024_11_135_2217.html'),
   ('Uredba (EU) 2016/679 (Opća uredba o zaštiti podataka), čl. 33.', 'https://eur-lex.europa.eu/legal-content/HR/TXT/?uri=CELEX:32016R0679'),
 ]))

# ─── 5 ────────────────────────────────────────────────────────────
ARTICLES.append(dict(
 slug="iso-27001-i-zks",
 cat="ISO norme",
 catkey="iso",
 date="2026-09-01",
 read=7,
 title="Imate ISO 27001. Koliko vam to vrijedi kod ZKS-a?",
 lead="Certifikat vas ne oslobađa obveze, ali vas ozbiljno skraćuje put. Pitanje je samo koje mjere pokriva, koje dodiruje, a koje ne dira uopće - i kako to dokazati bez pisanja druge dokumentacije paralelno.",
 desc="Koliko ISO/IEC 27001:2022 pokriva od 13 mjera Uredbe o kibernetičkoj sigurnosti, gdje su stvarne praznine i kako mapirati postojeće kontrole umjesto pisanja nove dokumentacije.",
 body='''
<p>Prva stvar koju treba raščistiti: <strong>ISO 27001 certifikat ne zamjenjuje usklađenost sa ZKS-om</strong>. Nema odredbe koja kaže da certificirani subjekt ne provodi mjere iz Priloga II. Ali odnos nije ni beskoristan - suprotno, organizacija s uhodanim ISMS-om u pravilu ima najveći dio potrebnog materijala, samo u drugom rasporedu.</p>

<h2>Gdje se preklapa jako</h2>
<p>Norma i Uredba dijele istu logiku upravljanja: znaj što imaš, znaj što ti prijeti, odluči što ćeš s tim, zapiši i preispitaj. To se odražava na nekoliko mjera gdje ISO organizacija u pravilu ima gotovo sve:</p>
<ul>
  <li><strong>Mjera 2, upravljanje imovinom.</strong> Inventar, vlasništvo, klasifikacija - postoji.</li>
  <li><strong>Mjera 3, upravljanje rizicima.</strong> Metodologija, registar rizika, plan obrade, vlasnici - postoji, uz jednu napomenu niže.</li>
  <li><strong>Mjera 7, kontrola pristupa.</strong> Politika pristupa, načelo najmanje privilegije, povlašteni pristup - postoji.</li>
  <li><strong>Mjera 8, sigurnost lanca opskrbe.</strong> Kontrole odnosa s dobavljačima - postoji, u pravilu na višoj razini nego u organizacijama bez norme.</li>
  <li><strong>Mjera 12, kontinuitet poslovanja.</strong> Ako je uz 27001 uspostavljen i ISO 22301, praktički je pokrivena.</li>
  <li><strong>Mjera 1, predanost uprave.</strong> Vodstvo, politika, uloge i odgovornosti, upravljački pregled - postoji kao struktura, ali sadržaj treba proširiti.</li>
</ul>

<h2>Gdje se preklapa djelomično</h2>
<p>Ovdje nastaje najviše nesporazuma, jer izgleda kao da je gotovo, a nije.</p>
<h3>Procjena rizika po all-hazards načelu</h3>
<p>Uredba traži procjenu koja obuhvaća sve vrste opasnosti - uključujući požar, poplavu, nestanak struje, ispad komunikacijske infrastrukture i neovlašteni fizički pristup. Mnogi ISMS-ovi procjenu rizika drže u granicama informacijskih prijetnji. Metodologija je ista, opseg nije.</p>
<h3>Fizička sigurnost</h3>
<p>Mjera 13 je zasebna mjera s vlastitim podmjerama. U normi je to skup kontrola unutar Priloga A. Materijal postoji, ali ga treba izdvojiti i dokazati po podmjerama, a ne pokazati kao dio šireg skupa.</p>
<h3>Kriptografija</h3>
<p>Mjera 10 traži pravila primjene, zaštitu podataka u prijenosu i mirovanju, upravljanje ključevima i - razmjerno riziku - pripremu na kvantno otpornu kriptografiju. Zadnje je novije od većine ISMS dokumentacije koju viđamo.</p>

<h2>Gdje norma ne pomaže</h2>
<p>Tri skupine obveza nemaju odgovarajući ekvivalent u normi jer proizlaze iz propisa, ne iz upravljačke prakse:</p>
<ol>
  <li><strong>Kategorizacija i sve što iz nje slijedi.</strong> Razina provedbe, nadležno tijelo, rokovi.</li>
  <li><strong>Prijava incidenata u propisanim rokovima.</strong> Norma traži proces upravljanja incidentima, ali ne poznaje rokove od 24, 72 sata i 30 dana ni prijavu nadležnom CSIRT-u.</li>
  <li><strong>Format i postupak provjere.</strong> Samoprocjena po bodovnom okviru, odnosno neovisna revizija, nemaju veze s certifikacijskim auditom prema normi.</li>
</ol>

<div class="callout">
  <div class="c-label">Praktičan zaključak</div>
  <p>ISO 27001 vam skraćuje put, ali ne mijenja odredište. Realno očekivanje: uhodan ISMS pokriva znatan dio dokazne baze, a ostatak se dopunjuje. Neuhodan ISMS - onaj koji je napravljen za certifikat i od tada se ne koristi - ne pomaže gotovo ništa, jer nedostaju upravo zapisi koji dokazuju da sustav živi.</p>
</div>

<h2>Kako to napraviti bez dupliranja</h2>
<p>Redoslijed koji funkcionira:</p>
<ol>
  <li><strong>Mapirajte prije nego što pišete.</strong> Svaka podmjera dobiva referencu na postojeći dokument, zapis ili kontrolu iz Izjave o primjenjivosti. Praznine su ono što ostane bez reference.</li>
  <li><strong>Proširite, ne preslikavajte.</strong> Ako postojeća metodologija rizika ne pokriva sve vrste opasnosti, proširite opseg u postojećem dokumentu. Druga metodologija znači dva registra rizika koja se razilaze.</li>
  <li><strong>Jedan registar imovine.</strong> Ako popis informacijske imovine za ISMS i inventar za ZKS vodite odvojeno, jedan će zastarjeti, a nećete znati koji.</li>
  <li><strong>Dopunite ono što nedostaje.</strong> Prijava incidenata, kategorizacija, priprema samoprocjene.</li>
</ol>
<p>Isti pristup vrijedi i za DORA obveznike i za organizacije s uspostavljenim GDPR sustavom. Dokazna baza se preklapa mnogo više nego što se čini iz naziva propisa.</p>
''',
 sources=[
   ('Uredba o kibernetičkoj sigurnosti, NN 135/2024, Prilog II.', 'https://narodne-novine.nn.hr/clanci/sluzbeni/2024_11_135_2217.html'),
   ('ZSIS - Prilog B, Okvir za evaluaciju, v1.0', 'https://www.zsis.hr/UserDocsImages/Samoprocjena/Prilog%20B%20-%20Okvir%20za%20evaluaciju.pdf'),
   ('HRN EN ISO/IEC 27001:2022 - Sustavi upravljanja informacijskom sigurnošću', None),
 ]))

# ─── 6 ────────────────────────────────────────────────────────────
ARTICLES.append(dict(
 slug="registar-rizika-koji-prolazi-provjeru",
 cat="Upravljanje rizicima",
 catkey="rizici",
 date="2026-09-01",
 read=6,
 title="Registar rizika koji prolazi provjeru: pet grešaka koje se ponavljaju",
 lead="Registar rizika je dokument koji svi imaju i rijetko tko koristi. Pet obrazaca se ponavlja iz organizacije u organizaciju, i svih pet je vidljivo na prvo čitanje.",
 desc="Najčešće greške u registru rizika koje se pojavljuju u provjerama usklađenosti: nepovezanost s imovinom, rizici bez vlasnika, ocjene bez obrazloženja, plan obrade bez rokova i registar koji se ne mijenja.",
 body='''
<p>Mjera 3 iz Priloga II. Uredbe traži dokumentiran proces upravljanja rizicima s procjenom, razinama, vlasnicima i planom obrade. Većina organizacija ima dokument koji tako izgleda. Manjina ima dokument koji izdrži pitanja.</p>
<p>Ovo su obrasci koji se ponavljaju, poredani po tome koliko brzo se primijete.</p>

<h2>1. Registar nije povezan s inventarom imovine</h2>
<p>Rizik glasi "gubitak podataka" ili "kibernetički napad", bez naznake na kojoj imovini. Takav zapis ne može se ni tretirati ni verificirati - ne zna se što se štiti, ni kad je rizik prestao postojati.</p>
<p>Uredba procjenu rizika izrijekom veže uz imovinu iz inventara kritične imovine. Ako registar rizika i registar imovine nemaju zajedničku referencu, dvije mjere koje trebaju stajati jedna na drugoj stoje jedna pored druge.</p>
<div class="callout">
  <div class="c-label">Provjera u jednoj rečenici</div>
  <p>Uzmite nasumičan redak iz registra rizika i pokušajte pronaći odgovarajuću stavku u inventaru imovine. Ako to traje dulje od minute, veza ne postoji.</p>
</div>

<h2>2. Rizici nemaju vlasnika, nego odjel</h2>
<p>U stupcu vlasnika piše "IT" ili "Informatika". Odjel ne može donijeti odluku o prihvaćanju rizika, ne može biti pozvan na odgovornost i ne može izvijestiti upravu. Uredba traži identifikaciju vlasnika rizika i njihovo područje odgovornosti - to znači osobu s imenom.</p>
<p>Posljedica je predvidljiva: rizik čiji je vlasnik odjel ostaje otvoren godinama jer nitko pojedinačno ne kasni.</p>

<h2>3. Ocjena postoji, obrazloženje ne</h2>
<p>Vjerojatnost 3, utjecaj 4, razina visoka. Zašto 3, a ne 2? Kad je zadnji put preispitano? Bez traga rasuđivanja, ocjena je broj koji se ne može ni obraniti ni osporiti.</p>
<p>Ovo posebno smeta kod samoprocjene, gdje se svaka ocjena mora moći obrazložiti dokazom. Registar rizika u kojem su ocjene nastale na sastanku bez zapisnika stvara isti problem na višoj razini.</p>

<h2>4. Plan obrade je popis želja</h2>
<p>Mjere obrade formulirane su kao "unaprijediti nadzor" ili "razmotriti dodatnu zaštitu", bez roka, vlasnika i procjene resursa. To nije plan obrade nego evidencija dobrih namjera.</p>
<p>Uredba traži da odgovor na rizik bude razmjeran razini i kritičnosti, uz odgovarajuće tehničke, operativne i organizacijske mjere. Razmjernost se ne može ocijeniti ako mjera nije konkretna.</p>
<ul>
  <li>Loše: "poboljšati upravljanje pristupom"</li>
  <li>Dobro: "uvesti višefaktorsku autentifikaciju za sve administratorske račune, vlasnik M. K., rok 31. 3., procjena 12 radnih dana"</li>
</ul>

<h2>5. Registar se ne mijenja</h2>
<p>Najjasniji signal da sustav ne živi. Ista trideset i dva rizika, iste ocjene, jedina promjena je datum u zaglavlju. Uredba traži ažuriranje procesa na godišnjoj osnovi, ali sadržajno ažuriranje znači nešto drugo: novi rizici ulaze, riješeni se zatvaraju, ocjene se mijenjaju kad se promijeni okolnost.</p>
<p>Registar koji se nije promijenio nakon uvođenja novog sustava, nakon promjene dobavljača ili nakon incidenta govori da se ne koristi u odlučivanju, nego se održava zbog provjere.</p>

<h2>Što razlikuje registar koji prolazi</h2>
<p>Ne opseg. Vidjeli smo registre sa stotinu redaka koji ne prolaze i registre s dvadeset pet koji prolaze bez primjedbe. Razlikuje ih pet stvari:</p>
<ol>
  <li>Svaki rizik pokazuje na imovinu iz inventara.</li>
  <li>Svaki rizik ima osobu kao vlasnika.</li>
  <li>Svaka ocjena ima kratko obrazloženje i datum.</li>
  <li>Svaka mjera obrade ima rok, vlasnika i procjenu resursa.</li>
  <li>Postoji trag da se registar mijenjao, s razlogom promjene.</li>
</ol>
<p>Peta stavka je ujedno i najteža za retroaktivno proizvesti, što je i razlog zašto se registar rizika ne isplati ostavljati za kraj projekta usklađivanja.</p>

<div class="note">
  <p>Registar rizika je ulaz u nekoliko drugih mjera: određuje razinu provedbe kod uvjetnih kontrola, utemeljuje odabir mjera u planu usklađivanja i povezuje se s procjenom rizika trećih strana iz mjere 8. Slab registar rizika ne pada sam - povuče za sobom sve što se na njega poziva.</p>
</div>
''',
 sources=[
   ('Uredba o kibernetičkoj sigurnosti, NN 135/2024, Prilog II., mjera 3', 'https://narodne-novine.nn.hr/clanci/sluzbeni/2024_11_135_2217.html'),
   ('ZSIS - Prilog B, Okvir za evaluaciju, v1.0, mjera 3', 'https://www.zsis.hr/UserDocsImages/Samoprocjena/Prilog%20B%20-%20Okvir%20za%20evaluaciju.pdf'),
 ]))

# ══════════════════════════════════════════════════════════════════
HR_MJ = ["siječnja","veljače","ožujka","travnja","svibnja","lipnja",
         "srpnja","kolovoza","rujna","listopada","studenoga","prosinca"]
def hr_date(iso):
    y, m, d = iso.split("-")
    return "%d. %s %s." % (int(d), HR_MJ[int(m)-1], y)

RFC_MJ = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
def rfc_date(iso):
    y, m, d = iso.split("-")
    return "%s, %s %s %s 09:00:00 +0200" % ("Tue", d, RFC_MJ[int(m)-1], y)


def card(a, featured=False):
    return '''<a class="post-card%s" href="/blog/%s/" data-cat="%s">
      <div class="post-cat">%s</div>
      <div class="post-title">%s</div>
      <div class="post-lead">%s</div>
      <div class="post-meta"><span>%s</span><span class="read">%d min čitanja</span></div>
    </a>''' % (" featured" if featured else "", a["slug"], a["catkey"], a["cat"],
               html.escape(a["title"]), html.escape(a["lead"]), hr_date(a["date"]), a["read"])


def kb_links():
    return "\n".join('        <a href="/blog/%s/">%s</a>' % (a["slug"], html.escape(a["cat"]))
                     for a in ARTICLES[:4]) + '\n        <a href="/blog/">Svi članci</a>'

FOOTER_R = FOOTER.replace("__KBLINKS__", kb_links())

# ══════════════════════════════════════════════════════════════════
# Generiranje clanaka
# ══════════════════════════════════════════════════════════════════
for i, a in enumerate(ARTICLES):
    body_html = a["body"].replace("__TABLICA__", mjere_tablica())
    srcs = "\n".join(
      '    <li>%s</li>' % (('<a href="%s" target="_blank" rel="noopener">%s</a>' % (u, html.escape(t)))
                           if u else html.escape(t))
      for t, u in a["sources"])
    rel = [x for x in ARTICLES if x["slug"] != a["slug"]][:3]
    related = "\n".join(card(x) for x in rel)
    url = "%s/blog/%s/" % (SITE, a["slug"])

    body = header(2) + '''
<main>
  <div class="container narrow">
    <div class="crumbs">
      <a href="/">Početna</a><span>&rsaquo;</span><a href="/blog/">Baza znanja</a><span>&rsaquo;</span>%s
    </div>
    <header class="art-head">
      <div class="eyebrow">%s</div>
      <h1>%s</h1>
      <p class="art-lead">%s</p>
      <div class="art-meta">
        <span><strong>%s</strong></span>
        <span>%s</span>
        <span>%d min čitanja</span>
      </div>
    </header>
    <article>
%s
      <div class="sources">
        <h4>Izvori</h4>
        <ul>
%s
        </ul>
      </div>
      %s
    </article>
    <div class="related">
      <h3>Povezano iz baze znanja</h3>
      <div class="related-grid">
%s
      </div>
    </div>
  </div>
</main>
''' % (html.escape(a["cat"]), html.escape(a["cat"]), html.escape(a["title"]),
       html.escape(a["lead"]), AUTHOR, hr_date(a["date"]), a["read"],
       body_html, srcs, CTA, related) + FOOTER_R

    ld = [{
      "@context": "https://schema.org", "@type": "BlogPosting",
      "headline": a["title"], "description": a["desc"],
      "datePublished": a["date"], "dateModified": a["date"],
      "inLanguage": "hr-HR", "articleSection": a["cat"],
      "author": {"@type": "Person", "name": "Daniel Bara", "honorificSuffix": "dr. sc.",
                 "url": SITE + "/#onama"},
      "publisher": {"@type": "Organization", "name": "Adventure Spirit d.o.o.",
                    "url": SITE + "/"},
      "mainEntityOfPage": {"@type": "WebPage", "@id": url},
      "url": url,
    }, {
      "@context": "https://schema.org", "@type": "BreadcrumbList",
      "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Početna", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": "Baza znanja", "item": SITE + "/blog/"},
        {"@type": "ListItem", "position": 3, "name": a["title"], "item": url},
      ]}]

    out = page(a["title"] + " | Adventure Spirit Consulting", a["desc"], body, url,
               og_type="article", ld=ld)
    d = os.path.join(BLOG, a["slug"])
    os.makedirs(d, exist_ok=True)
    io.open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(out)

# ══════════════════════════════════════════════════════════════════
# Popisna stranica
# ══════════════════════════════════════════════════════════════════
cats = []
for a in ARTICLES:
    if (a["catkey"], a["cat"]) not in cats:
        cats.append((a["catkey"], a["cat"]))
catbtns = '<button class="cat-btn active" data-f="all">Sve teme</button>\n      ' + \
          "\n      ".join('<button class="cat-btn" data-f="%s">%s</button>' % (k, html.escape(v)) for k, v in cats)

feat = [a for a in ARTICLES if a.get("featured")]
rest = [a for a in ARTICLES if not a.get("featured")]
cards = "\n".join([card(a, True) for a in feat] + [card(a) for a in rest])

listing = header(1) + '''
<main>
  <section class="kb-hero">
    <div class="container">
      <div class="eyebrow">Baza znanja</div>
      <h1>Što propis traži i čime se to dokazuje</h1>
      <p>Tekstovi o Zakonu o kibernetičkoj sigurnosti, ISO normama, zaštiti podataka i upravljanju rizicima. Bez uopćavanja: uz svaku tvrdnju stoji članak propisa ili norme ondje gdje ga ima.</p>
      <div class="cat-bar">
      ''' + catbtns + '''
      </div>
    </div>
  </section>
  <div class="container">
    <div class="post-grid" id="posts">
''' + cards + '''
    </div>
  </div>
</main>
<script>
document.querySelectorAll('.cat-btn').forEach(function (b) {
  b.addEventListener('click', function () {
    document.querySelectorAll('.cat-btn').forEach(function (x) { x.classList.remove('active'); });
    b.classList.add('active');
    var f = b.dataset.f;
    document.querySelectorAll('.post-card').forEach(function (c) {
      c.classList.toggle('hidden', f !== 'all' && c.dataset.cat !== f);
    });
  });
});
</script>
''' + FOOTER_R

ld_list = [{
  "@context": "https://schema.org", "@type": "Blog",
  "@id": SITE + "/blog/#blog",
  "name": "Baza znanja - Adventure Spirit Consulting",
  "description": "Tekstovi o Zakonu o kibernetičkoj sigurnosti, ISO normama, zaštiti podataka i upravljanju rizicima.",
  "url": SITE + "/blog/", "inLanguage": "hr-HR",
  "publisher": {"@type": "Organization", "name": "Adventure Spirit d.o.o.", "url": SITE + "/"},
  "blogPost": [{"@type": "BlogPosting", "headline": a["title"], "url": "%s/blog/%s/" % (SITE, a["slug"]),
                "datePublished": a["date"], "description": a["desc"]} for a in ARTICLES],
}]
io.open(os.path.join(BLOG, "index.html"), "w", encoding="utf-8").write(
  page("Baza znanja - ZKS, NIS2, ISO i upravljanje rizicima | Adventure Spirit Consulting",
       "Stručni tekstovi o Zakonu o kibernetičkoj sigurnosti, 13 mjera Uredbe, samoprocjeni, prijavi incidenata, ISO normama i upravljanju rizicima.",
       listing, SITE + "/blog/", ld=ld_list))

# ══════════════════════════════════════════════════════════════════
# RSS
# ══════════════════════════════════════════════════════════════════
items = "\n".join('''  <item>
    <title>%s</title>
    <link>%s/blog/%s/</link>
    <guid isPermaLink="true">%s/blog/%s/</guid>
    <category>%s</category>
    <pubDate>%s</pubDate>
    <description>%s</description>
  </item>''' % (html.escape(a["title"]), SITE, a["slug"], SITE, a["slug"],
                html.escape(a["cat"]), rfc_date(a["date"]), html.escape(a["desc"]))
  for a in ARTICLES)
io.open(os.path.join(BLOG, "feed.xml"), "w", encoding="utf-8").write(
'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
  <title>Baza znanja - Adventure Spirit Consulting</title>
  <link>%s/blog/</link>
  <atom:link href="%s/blog/feed.xml" rel="self" type="application/rss+xml"/>
  <description>Tekstovi o Zakonu o kibernetičkoj sigurnosti, ISO normama, zaštiti podataka i upravljanju rizicima.</description>
  <language>hr</language>
%s
</channel>
</rss>
''' % (SITE, SITE, items))

# ══════════════════════════════════════════════════════════════════
# 404 stranica
# ══════════════════════════════════════════════════════════════════
nf_cards = "\n".join(card(a) for a in ARTICLES[:3])
nf_body = header(0, active_blog=False) + '''
<main>
  <section class="kb-hero">
    <div class="container">
      <div class="nf-code">404</div>
      <h1>Ova stranica nije pronađena</h1>
      <p>Adresa je možda promijenjena ili u poveznici nedostaje dio. Ispod su najčešća odredišta, a ako ste tražili nešto konkretno, javite nam se i uputit ćemo vas.</p>
      <div class="nf-links">
        <a href="/" class="btn-primary">Natrag na početnu</a>
        <a href="/#kontakt" class="btn-outline">Kontakt</a>
      </div>
      <div class="nf-nav">
        <a href="/#sigurnost">Usluge</a>
        <a href="/#sektori">Sektori</a>
        <a href="/#okvir">Pravni okvir</a>
        <a href="/blog/">Baza znanja</a>
        <a href="/#faq">Česta pitanja</a>
        <a href="/#reference">Reference</a>
        <a href="https://app.adventurespirit.hr" target="_blank" rel="noopener">GRC Portal</a>
      </div>
    </div>
  </section>
  <div class="container">
    <div style="padding:44px 0 12px"><div class="eyebrow">Iz baze znanja</div></div>
    <div class="post-grid" style="padding-top:0">
''' + nf_cards + '''
    </div>
  </div>
</main>
''' + FOOTER_R

NF_CSS = '''<style>
.nf-code { font-size: clamp(64px, 11vw, 132px); font-weight: 900; line-height: .9; letter-spacing: -4px;
  color: transparent; -webkit-text-stroke: 2px rgba(239,101,63,.5); margin-bottom: 18px; }
.nf-links { display: flex; gap: 12px; flex-wrap: wrap; margin-top: 30px; }
.nf-nav { display: flex; gap: 10px; flex-wrap: wrap; margin-top: 34px; padding-top: 26px; border-top: 1px solid var(--line); }
.nf-nav a { font-size: 13px; font-weight: 600; color: var(--text-muted); text-decoration: none;
  background: rgba(255,255,255,.04); border: 1px solid var(--line); border-radius: 8px; padding: 8px 14px; transition: .2s; }
.nf-nav a:hover { color: #fff; border-color: rgba(239,101,63,.45); }
@media (max-width: 600px) { .nf-links .btn-primary, .nf-links .btn-outline { width: 100%; } }
</style>'''

io.open(os.path.join(ROOT, "404.html"), "w", encoding="utf-8").write(
  page("Stranica nije pronađena (404) | Adventure Spirit Consulting",
       "Tražena stranica ne postoji. Pogledajte usluge, sektore, pravni okvir ili bazu znanja.",
       nf_body, SITE + "/404.html", extra_head=NF_CSS + '\n<meta name="robots" content="noindex, follow">'))

# ══════════════════════════════════════════════════════════════════
# sitemap.xml + robots.txt
# ══════════════════════════════════════════════════════════════════
urls = [(SITE + "/", "1.0", "weekly"), (SITE + "/blog/", "0.9", "weekly")]
urls += [("%s/blog/%s/" % (SITE, a["slug"]), "0.8", "monthly") for a in ARTICLES]
urls += [(SITE + "/uvjeti/", "0.3", "yearly"), (SITE + "/privatnost/", "0.3", "yearly"),
         (SITE + "/mmew/", "0.5", "monthly")]
io.open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write(
'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
''' + "\n".join('  <url><loc>%s</loc><lastmod>2026-09-01</lastmod><changefreq>%s</changefreq><priority>%s</priority></url>'
                % (u, c, p) for u, p, c in urls) + '''
</urlset>
''')
io.open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8").write(
'''User-agent: *
Allow: /

Sitemap: %s/sitemap.xml
''' % SITE)

print("Generirano: %d članaka + popis + feed + sitemap + robots" % len(ARTICLES))
