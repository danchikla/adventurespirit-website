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



# ── SVG ikone usluga ──────────────────────────────────────────────
SVG = {
 "shield":   '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>',
 "lock":     '<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
 "award":    '<circle cx="12" cy="8" r="6"/><path d="M8.2 13.9 7 23l5-3 5 3-1.2-9.1"/>',
 "gear":     '<path d="M4 21v-7M4 10V3M12 21v-9M12 8V3M20 21v-5M20 12V3M1 14h6M9 8h6M17 16h6"/>',
 "leaf":     '<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.5 19 2c1 2 2 4.2 2 8 0 5.5-4.8 10-10 10z"/><path d="M2 21c0-3 1.9-5.4 5.1-6C9.5 14.5 12 13 13 12"/>',
 "cycle":    '<path d="M23 4v6h-6M1 20v-6h6"/><path d="M20.5 9A9 9 0 0 0 5.6 5.6L1 10m22 4-4.6 4.4A9 9 0 0 1 3.5 15"/>',
 "bank":     '<path d="M3 21h18M3 10h18M5 6l7-4 7 4M6 10v11M18 10v11M10 14v3M14 14v3"/>',
 "chain":    '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8"/>',
 "scan":     '<circle cx="11" cy="11" r="7"/><path d="M21 21l-4.4-4.4M11 8v6M8 11h6"/>',
}
def svg(key):
    return '<svg viewBox="0 0 24 24">%s</svg>' % SVG[key]

def strip_html(x):
    return re.sub(r'<[^>]+>', '', x).replace('&middot;', '·').replace('&nbsp;', ' ').replace('&rarr;', '->').strip()


# ══════════════════════════════════════════════════════════════════
# Dvojezicna navigacija, podnozje i predlozak stranice
# ══════════════════════════════════════════════════════════════════
L = {
 "hr": dict(
   lang="hr", base="", blog="/blog/", other="/en/", other_label="EN", self_label="HR",
   nav=[("/#onama","O nama"),("/#sigurnost","Usluge"),("/#sektori","Sektori"),
        ("/blog/","Baza znanja"),("/#platforma","Platforma"),("/#reference","Reference"),
        ("/#faq","FAQ"),("/#kontakt","Kontakt")],
   legal_line="Adventure Spirit d.o.o. &middot; Zagreb",
   brand_line="Tržišni naziv: Adventure Spirit Consulting",
   addr="Antuna Šoljana 22, 10000 Zagreb, Hrvatska", oib="OIB / PDV ID: 72169598754 &middot; MBS: 4845552<br>Trgovački sud u Zagrebu",
   tagline="Kibernetička sigurnost, GRC compliance i upravljanje rizicima - preko 20 godina iskustva u službi vašeg poslovanja.",
   f_kb="Baza znanja", f_all="Svi članci", f_svc="Usluge", f_co="Tvrtka",
   f_links=[("/#sigurnost","ZKS / NIS2"),("/#sigurnost","GDPR"),("/#sigurnost","ISO 27001"),
            ("/#sigurnost","DORA"),("/#sektori","Sektori")],
   f_co_links=[("/#onama","O konzultantu"),("/#reference","Reference"),("/#faq","Česta pitanja"),
               ("/#kontakt","Kontakt"),("/en/","English version")],
   rights="Sva prava pridržana", terms="Uvjeti korištenja", privacy="Privatnost",
   terms_url="/uvjeti/", privacy_url="/privatnost/",
   kb_title="Baza znanja", kb_h1="Što propis traži i čime se to dokazuje",
   kb_intro="Tekstovi o Zakonu o kibernetičkoj sigurnosti, ISO normama, zaštiti podataka i upravljanju rizicima. Bez uopćavanja: uz svaku tvrdnju stoji članak propisa ili norme ondje gdje ga ima.",
   kb_desc="Stručni tekstovi o Zakonu o kibernetičkoj sigurnosti, 13 mjera Uredbe, samoprocjeni, prijavi incidenata, ISO normama i upravljanju rizicima.",
   all_topics="Sve teme", read="min čitanja", home="Početna",
   sources="Izvori", related="Povezano iz baze znanja",
   nf_h1="Ova stranica nije pronađena",
   nf_p="Adresa je možda promijenjena ili u poveznici nedostaje dio. Ispod su najčešća odredišta, a ako ste tražili nešto konkretno, javite nam se i uputit ćemo vas.",
   nf_home="Natrag na početnu", nf_contact="Kontakt", nf_from_kb="Iz baze znanja",
   nf_title="Stranica nije pronađena (404)",
   nf_desc="Tražena stranica ne postoji. Pogledajte usluge, sektore, pravni okvir ili bazu znanja.",
   nf_nav=[("/#sigurnost","Usluge"),("/#sektori","Sektori"),("/#okvir","Pravni okvir"),
           ("/blog/","Baza znanja"),("/#faq","Česta pitanja"),("/#reference","Reference")],
   cta_h="Ne znate gdje stojite?",
   cta_p="Pola sata razgovora i ništa vas ne obvezuje. Kad završimo, znate što trebate napraviti i kojim redom.",
   cta_b1="Dogovorite razgovor", cta_b2="Pogledajte usluge", cta_b2_url="/#sigurnost",
   feed_title="Baza znanja - Adventure Spirit Consulting",
 ),
 "en": dict(
   lang="en", base="/en", blog="/en/blog/", other="/", other_label="HR", self_label="EN",
   nav=[("/en/#about","About"),("/en/#services","Services"),("/en/#sectors","Sectors"),
        ("/en/blog/","Insights"),("/en/#platform","Platform"),("/en/#clients","Clients"),
        ("/en/#faq","FAQ"),("/en/#contact","Contact")],
   legal_line="Adventure Spirit d.o.o. &middot; Zagreb, Croatia",
   brand_line="Trading as: Adventure Spirit Consulting",
   addr="Antuna Šoljana 22, 10000 Zagreb, Croatia", oib="OIB / VAT ID: 72169598754 &middot; Reg. no. (MBS): 4845552<br>Commercial Court in Zagreb",
   tagline="Cyber security, GRC compliance and risk management - over 20 years of experience in the service of your business.",
   f_kb="Insights", f_all="All articles", f_svc="Services", f_co="Company",
   f_links=[("/en/#services","CSA / NIS2"),("/en/#services","GDPR"),("/en/#services","ISO 27001"),
            ("/en/#services","DORA"),("/en/#sectors","Sectors")],
   f_co_links=[("/en/#about","About the consultant"),("/en/#clients","Clients"),("/en/#faq","FAQ"),
               ("/en/#contact","Contact"),("/","Hrvatska verzija")],
   rights="All rights reserved", terms="Terms (HR)", privacy="Privacy (HR)",
   terms_url="/uvjeti/", privacy_url="/privatnost/",
   kb_title="Knowledge base", kb_h1="What the rules ask for and what proves it",
   kb_intro="Articles on the Croatian Cybersecurity Act, ISO standards, data protection and risk management. No generalities: every claim carries the article of the law or standard behind it, where one exists.",
   kb_desc="Expert articles on the Croatian Cybersecurity Act, the 13 measures of the Regulation, self-assessment scoring, incident reporting, ISO standards and risk management.",
   all_topics="All topics", read="min read", home="Home",
   sources="Sources", related="Related reading",
   nf_h1="This page could not be found",
   nf_p="The address may have changed, or part of the link is missing. The most common destinations are below - and if you were looking for something specific, get in touch and we will point you to it.",
   nf_home="Back to home", nf_contact="Contact", nf_from_kb="From the knowledge base",
   nf_title="Page not found (404)",
   nf_desc="The page you requested does not exist. Browse our services, sectors, legal framework or knowledge base.",
   nf_nav=[("/en/#services","Services"),("/en/#sectors","Sectors"),("/en/#framework","Legal framework"),
           ("/en/blog/","Knowledge base"),("/en/#faq","FAQ"),("/en/#clients","Clients")],
   cta_h="Not sure where you stand?",
   cta_p="Half an hour of conversation, with no obligation. By the end you know what needs doing and in what order.",
   cta_b1="Book a conversation", cta_b2="See our services", cta_b2_url="/en/#services",
   feed_title="Insights - Adventure Spirit Consulting",
 ),
}


def header(lang, active_blog=True):
    t = L[lang]
    links = "\n".join('    <li><a href="%s"%s>%s</a></li>'
                      % (u, ' class="active"' if (active_blog and u == t["blog"]) else '', n)
                      for u, n in t["nav"])
    return '''<div id="topwrap">

<div class="topbar">
  <span class="tb-legal">''' + t["legal_line"] + '''</span>
  <span class="tb-contact">
    <a href="tel:+385955041496">''' + ICON_PHONE + '''+385 95 504 1496</a>
    <a href="mailto:info@adventurespirit.hr">''' + ICON_MAIL + '''info@adventurespirit.hr</a>
    <a href="https://app.adventurespirit.hr" target="_blank" rel="noopener">''' + ICON_LOCK + '''GRC Portal</a>
  </span>
</div>

<nav id="navbar">
  <a href="''' + (t["base"] or "/") + '''" class="nav-logo">
    ''' + LOGO_SVG + '''
    <div class="nav-logo-text">
      <span class="nav-logo-name">Adventure <span>Spirit</span></span>
      <span class="nav-logo-sub">Consulting</span>
    </div>
  </a>

  <ul class="nav-links" id="nav-links">
''' + links + '''
    <li class="lang-switch"><span>''' + t["self_label"] + '''</span><a href="''' + t["other"] + '''" hreflang="''' + ("en" if lang == "hr" else "hr") + '''">''' + t["other_label"] + '''</a></li>
    <li><a href="https://app.adventurespirit.hr" target="_blank" rel="noopener" class="nav-cta">Portal</a></li>
  </ul>

  <button class="nav-toggle" onclick="toggleNav()" aria-label="Menu">
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M3 12h18M3 6h18M3 18h18"/></svg>
  </button>
</nav>

</div><!-- /#topwrap -->'''


def footer(lang, articles):
    t = L[lang]
    kb = "\n".join('        <a href="%s%s/">%s</a>' % (t["blog"], a["slug"], html.escape(a["cat"]))
                   for a in articles[:4]) + '\n        <a href="%s">%s</a>' % (t["blog"], t["f_all"])
    svc = "\n".join('        <a href="%s">%s</a>' % (u, n) for u, n in t["f_links"])
    co = "\n".join('        <a href="%s">%s</a>' % (u, n) for u, n in t["f_co_links"])
    return '''<footer>
  <div class="container">
    <div class="footer-inner">
      <div class="footer-brand">
        <a href="''' + (t["base"] or "/") + '''" style="display:flex;align-items:center;gap:10px;text-decoration:none">
          <svg width="32" height="32" viewBox="0 0 100 100" fill="none">
            <circle cx="50" cy="50" r="44" stroke="#EF653F" stroke-width="1.5" opacity=".2"/>
            <path d="M50 12 L41 46 L50 41 L59 46 Z" fill="#EF653F"/>
            <line x1="44" y1="37" x2="56" y2="37" stroke="#c14b28" stroke-width="3"/>
            <path d="M50 88 L45 70 L55 70 Z" fill="#EF653F" opacity=".7"/>
            <circle cx="50" cy="50" r="5" fill="#EF653F"/>
          </svg>
          <span style="font-size:16px;font-weight:800;color:#fff">Adventure <span style="color:#EF653F">Spirit</span></span>
        </a>
        <p>''' + t["tagline"] + '''</p>
        <p class="footer-legal">
          Adventure Spirit d.o.o.<br>
          ''' + t["brand_line"] + '''<br>
          ''' + t["addr"] + '''<br>
          ''' + t["oib"] + '''<br>
          <a href="tel:+385955041496">+385 95 504 1496</a><br>
          <a href="mailto:info@adventurespirit.hr">info@adventurespirit.hr</a>
        </p>
      </div>
      <div class="footer-col">
        <h4>''' + t["f_kb"] + '''</h4>
''' + kb + '''
      </div>
      <div class="footer-col">
        <h4>''' + t["f_svc"] + '''</h4>
''' + svc + '''
      </div>
      <div class="footer-col">
        <h4>''' + t["f_co"] + '''</h4>
''' + co + '''
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; 2026 Adventure Spirit d.o.o. - ''' + t["rights"] + '''</span>
      <span style="display:flex;gap:16px">
        <a href="''' + t["blog"] + '''feed.xml">RSS</a>
        <a href="''' + t["terms_url"] + '''">''' + t["terms"] + '''</a>
        <a href="''' + t["privacy_url"] + '''">''' + t["privacy"] + '''</a>
      </span>
    </div>
  </div>
</footer>'''


def hreflang(hr_url, en_url):
    return ('<link rel="alternate" hreflang="hr" href="%s">\n'
            '<link rel="alternate" hreflang="en" href="%s">\n'
            '<link rel="alternate" hreflang="x-default" href="%s">' % (hr_url, en_url, hr_url))


def page(title, desc, body, canonical, lang="hr", extra_head="", og_type="website", ld=None,
         css_link=True, feed=None):
    ldjs = ""
    if ld:
        ldjs = "\n".join('<script type="application/ld+json">\n%s\n</script>'
                         % json.dumps(o, ensure_ascii=False, indent=2) for o in ld)
    feed = feed or L[lang]["blog"] + "feed.xml"
    css = '<link rel="stylesheet" href="/blog/assets/blog.css">\n' if css_link else ''
    return '''<!DOCTYPE html>
<html lang="%s">
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
<meta property="og:locale" content="%s">
<meta property="og:url" content="%s">
<meta property="og:title" content="%s">
<meta property="og:description" content="%s">
<meta property="og:image" content="%s/mmew/img/og.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="%s">
<meta name="twitter:description" content="%s">
<link rel="alternate" type="application/rss+xml" title="%s" href="%s">
<link rel="icon" type="image/svg+xml" href="%s">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
%s%s
</head>
<body>
%s
%s
<script>
function toggleNav() { document.getElementById('nav-links').classList.toggle('open'); }
document.querySelectorAll('#nav-links a').forEach(function (a) {
  a.addEventListener('click', function () { document.getElementById('nav-links').classList.remove('open'); });
});
</script>
</body>
</html>
''' % (lang, html.escape(title), html.escape(desc), canonical, AUTHOR, og_type,
       "hr_HR" if lang == "hr" else "en_GB", canonical, html.escape(title), html.escape(desc),
       SITE, html.escape(title), html.escape(desc), html.escape(L[lang]["feed_title"]), feed,
       FAVICON, css, extra_head, body, ldjs)

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
ARTICLES = []

# ─── 1 ────────────────────────────────────────────────────────────
ARTICLES.append(dict(
 slug="kategorizacija-prema-zks-u",
 cat="ZKS / NIS2",
 catkey="zks",
 date="2026-01-20",
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
 date="2026-02-10",
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
 date="2026-04-14",
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
 date="2026-03-03",
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
 date="2026-03-24",
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

# ══════════════════════════════════════════════════════════════════
# ENGLESKA VERZIJA - /en/
# ══════════════════════════════════════════════════════════════════
# CSS se preuzima iz index.html pa EN stranica automatski prati
# svaku promjenu stila na hrvatskoj naslovnici.

_hr_index = io.open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
_m = re.search(r'<style>(.*?)</style>', _hr_index, re.S)
if not _m:
    raise SystemExit("Ne mogu pronaci <style> blok u index.html")
SHARED_CSS = _m.group(1)

# Matrica zrelosti - isti podaci kao na hrvatskoj naslovnici
def maturity_chart(t):
    cols = []
    for i, v in enumerate(SNAPSHOT, 1):
        cls = "ok" if v >= 3 else "low"
        cells = "".join('<div class="mcell%s"></div>' % (" on" if k < v else "") for k in range(5))
        cols.append('            <div class="mcol %s"><div class="mnum">%02d</div>%s</div>' % (cls, i, cells))
    return '''      <div class="mchart-card">
        <div class="mchart-eyebrow">%s</div>
        <div class="mchart-title">%s</div>
        <div class="mchart-sub">%s</div>
        <div class="mchart-wrap">
          <div class="mchart">
%s
          </div>
          <div class="mthresh"><span>%s</span></div>
        </div>
        <div class="mchart-legend">%s</div>
        <div class="mchart-stats">
          <div class="mstat"><div class="mstat-num">20<sup>+</sup></div><div class="mstat-label">%s</div></div>
          <div class="mstat"><div class="mstat-num">50<sup>+</sup></div><div class="mstat-label">%s</div></div>
          <div class="mstat"><div class="mstat-num">40<sup>+</sup></div><div class="mstat-label">%s</div></div>
          <div class="mstat"><div class="mstat-num">9</div><div class="mstat-label">%s</div></div>
        </div>
      </div>''' % (t["eyebrow"], t["title"], t["sub"], "\n".join(cols), t["thresh"],
                   t["legend"], t["s1"], t["s2"], t["s3"], t["s4"])

SNAPSHOT = [4, 3, 2, 3, 1, 2, 2, 4, 4, 3, 5, 2, 4]

EN_CHART = maturity_chart(dict(
  eyebrow="Readiness snapshot &middot; 13 CSA measures",
  title="Sample output of a gap assessment",
  sub="Categorised important entity, food industry",
  thresh="THRESHOLD 60 %",
  legend="One block is 20 % of the requirements within a measure for which evidence exists. Grey columns are measures below the readiness threshold. The threshold is our internal indicator, not a statutory one.",
  s1="years in information security", s2="GRC and ISO projects delivered",
  s3="organisations in our references", s4="modules in the GRC platform"))

# ── Navigacija i podnozje na engleskom ────────────────────────────
def en_header():
    return '''<div id="topwrap">

<div class="topbar">
  <span class="tb-legal">Adventure Spirit d.o.o. &middot; Zagreb, Croatia</span>
  <span class="tb-contact">
    <a href="tel:+385955041496">''' + ICON_PHONE + '''+385 95 504 1496</a>
    <a href="mailto:info@adventurespirit.hr">''' + ICON_MAIL + '''info@adventurespirit.hr</a>
    <a href="https://app.adventurespirit.hr" target="_blank" rel="noopener">''' + ICON_LOCK + '''GRC Portal</a>
  </span>
</div>

<nav id="navbar">
  <a href="/en/" class="nav-logo">
    ''' + LOGO_SVG + '''
    <div class="nav-logo-text">
      <span class="nav-logo-name">Adventure <span>Spirit</span></span>
      <span class="nav-logo-sub">Consulting</span>
    </div>
  </a>

  <ul class="nav-links" id="nav-links">
    <li><a href="#about">About</a></li>
    <li><a href="#services">Services</a></li>
    <li><a href="#sectors">Sectors</a></li>
    <li><a href="/en/blog/">Insights</a></li>
    <li><a href="#platform">Platform</a></li>
    <li><a href="#clients">Clients</a></li>
    <li><a href="#faq">FAQ</a></li>
    <li><a href="#contact">Contact</a></li>
    <li class="lang-switch"><a href="/" hreflang="hr" title="Hrvatska verzija">HR</a><span>EN</span></li>
    <li><a href="https://app.adventurespirit.hr" target="_blank" rel="noopener" class="nav-cta">Portal</a></li>
  </ul>

  <button class="nav-toggle" onclick="toggleNav()" aria-label="Menu">
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M3 12h18M3 6h18M3 18h18"/></svg>
  </button>
</nav>

</div><!-- /#topwrap -->'''

EN_FOOTER = '''<footer>
  <div class="container">
    <div class="footer-inner">
      <div class="footer-brand">
        <a href="/en/" style="display:flex;align-items:center;gap:10px;text-decoration:none">
          <svg width="32" height="32" viewBox="0 0 100 100" fill="none">
            <circle cx="50" cy="50" r="44" stroke="#EF653F" stroke-width="1.5" opacity=".2"/>
            <path d="M50 12 L41 46 L50 41 L59 46 Z" fill="#EF653F"/>
            <line x1="44" y1="37" x2="56" y2="37" stroke="#c14b28" stroke-width="3"/>
            <path d="M50 88 L45 70 L55 70 Z" fill="#EF653F" opacity=".7"/>
            <circle cx="50" cy="50" r="5" fill="#EF653F"/>
          </svg>
          <span style="font-size:16px;font-weight:800;color:#fff">Adventure <span style="color:#EF653F">Spirit</span></span>
        </a>
        <p>Cyber security, GRC compliance and risk management - over 20 years of experience in the service of your business.</p>
        <p class="footer-legal">
          Adventure Spirit d.o.o.<br>
          Trading as: Adventure Spirit Consulting<br>
          Zagreb, Republic of Croatia<br>
          Company ID (OIB): available on request<br>
          <a href="tel:+385955041496" style="color:var(--orange);text-decoration:none">+385 95 504 1496</a><br>
          <a href="mailto:info@adventurespirit.hr" style="color:var(--orange);text-decoration:none">info@adventurespirit.hr</a>
        </p>
      </div>
      <div class="footer-col">
        <h4>Insights</h4>
        <a href="/en/blog/">Knowledge base</a>
        <a href="#framework">Legal framework</a>
        <a href="#sectors">Sectors</a>
        <a href="#faq">FAQ</a>
        <a href="#process">How we work</a>
      </div>
      <div class="footer-col">
        <h4>Services</h4>
        <a href="#services">CSA / NIS2</a>
        <a href="#services">GDPR</a>
        <a href="#services">ISO 27001</a>
        <a href="#services">DORA</a>
        <a href="#services">Vendor risk</a>
      </div>
      <div class="footer-col">
        <h4>Company</h4>
        <a href="#about">About the consultant</a>
        <a href="#clients">Clients</a>
        <a href="#contact">Contact</a>
        <a href="/">Hrvatska verzija</a>
        <a href="https://app.adventurespirit.hr" target="_blank" rel="noopener">GRC Portal</a>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; 2026 Adventure Spirit d.o.o. - All rights reserved</span>
      <span style="display:flex;gap:16px">
        <a href="/en/blog/feed.xml" style="color:var(--text-muted);text-decoration:none">RSS</a>
        <a href="/uvjeti/" style="color:var(--text-muted);text-decoration:none">Terms (HR)</a>
        <a href="/privatnost/" style="color:var(--text-muted);text-decoration:none">Privacy (HR)</a>
      </span>
    </div>
  </div>
</footer>'''

# Dodatni CSS koji postoji samo na engleskoj strani
LANG_CSS = '''
    .lang-switch { display: flex; align-items: center; gap: 2px; margin-left: 6px; padding-left: 10px; border-left: 1px solid rgba(255,255,255,.12); }
    .lang-switch a, .lang-switch span { font-size: 12px; font-weight: 700; letter-spacing: .5px; padding: 5px 8px; border-radius: 6px; }
    .lang-switch span { color: var(--white); background: rgba(255,255,255,.08); }
    .lang-switch a { color: var(--text-muted); text-decoration: none; }
    .lang-switch a:hover { color: var(--orange); background: rgba(239,101,63,.1); }
    @media (max-width: 960px) {
      .nav-links.open .lang-switch { border-left: none; padding-left: 0; margin: 8px 0 0; justify-content: center; gap: 8px; }
      .nav-links.open .lang-switch a, .nav-links.open .lang-switch span { padding: 10px 20px; font-size: 14px; }
    }
    .legal-note { font-size: 12.5px; color: #6b7488; line-height: 1.7; margin-top: 18px; text-align: center; }
'''

# ══════════════════════════════════════════════════════════════════
# Sadrzaj engleske naslovnice
# ══════════════════════════════════════════════════════════════════
EN_LEGAL = [
 ("Cybersecurity Act", "OG 14/2024", "Croatian implementation of NIS2. Entity categorisation, risk management measures, incident reporting, audit and self-assessment.", "https://narodne-novine.nn.hr/clanci/sluzbeni/2024_02_14_222.html"),
 ("Cybersecurity Regulation", "OG 135/2024", "Breaks the statutory duties down into 13 measures with sub-measures and controls, across three levels of implementation.", "https://narodne-novine.nn.hr/clanci/sluzbeni/2024_11_135_2217.html"),
 ("NIS2", "EU 2022/2555", "Directive on measures for a high common level of cybersecurity across the Union.", "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32022L2555"),
 ("DORA", "EU 2022/2554", "Digital operational resilience for the financial sector - ICT risk, resilience testing, third-party providers.", "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32022R2554"),
 ("GDPR", "EU 2016/679", "Personal data protection - records of processing, DPIA, DPO, breach notification to the supervisory authority.", "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679"),
 ("AI Act", "EU 2024/1689", "Risk-based classification of AI systems, obligations for providers and deployers, governance and oversight.", "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689"),
 ("ISO/IEC 27001", "2022", "Information security management system - 93 Annex A controls and the Statement of Applicability.", None),
 ("ISO 22301", "2019", "Business continuity management system - BIA, RTO/RPO, plans and exercising.", None),
]

EN_SECTORS = [
 ("Banking and finance", "CSA AND DORA, PARALLEL OBLIGATIONS &middot; CNB AND HANFA"),
 ("Insurance", "DORA FOR ICT RISK &middot; ISO 27001 AND BUSINESS CONTINUITY"),
 ("Energy", "GENERATION, TRANSMISSION, DISTRIBUTION, GAS AND OIL"),
 ("Healthcare and pharma", "ESSENTIAL ENTITY REGARDLESS OF SIZE FOR CRITICAL ACTIVITIES"),
 ("Food industry", "PRODUCTION, PROCESSING AND DISTRIBUTION &middot; IMPORTANT ENTITIES"),
 ("Digital infrastructure and ICT", "DATA CENTRES, CLOUD, NETWORKS, MANAGED ICT SERVICES"),
 ("Public administration", "STATE ADMINISTRATION BODIES ESSENTIAL REGARDLESS OF SIZE"),
 ("Transport and logistics", "AIR, RAIL, WATER AND ROAD TRANSPORT &middot; LOGISTICS"),
]

EN_SERVICES = [
 ("shield", "CSA / NIS2 compliance", "Statutory duty",
  "Implementation of all 13 risk management measures from Annex II of the Croatian Cybersecurity Regulation (OG 135/2024), at the level of implementation prescribed for your entity category - from gap assessment to a complete evidence base."),
 ("lock", "GDPR compliance", "EU regulation",
  "All personal data protection processes established - records of processing activities, DPIA, legitimate interest assessments, data subject request handling, DPO support and breach notification to the Croatian supervisory authority."),
 ("award", "ISO/IEC 27001 - Information security", "International standard",
  "Gap assessment, ISMS implementation, risk assessment, Statement of Applicability and full preparation for the certification audit against ISO/IEC 27001:2022."),
 ("gear", "ISO 9001 - Quality management", "Quality management",
  "QMS implementation, process documentation, definition of quality objectives and KPIs, internal audit programme and preparation for certification."),
 ("leaf", "ISO 14001 - Environmental management", "Environmental standard",
  "EMS implementation - identification of environmental aspects and impacts, legal compliance register, carbon footprint reduction and certification readiness."),
 ("cycle", "ISO 22301 - Business continuity", "Business continuity",
  "Business impact analysis, RTO and RPO definition, business continuity and disaster recovery plans, exercising and preparation for certification against ISO 22301:2019."),
 ("bank", "DORA - Digital operational resilience", "Financial sector",
  "Compliance with the EU DORA regulation - ICT risk management framework, third-party risk and the register of information, resilience testing and regulatory reporting."),
 ("chain", "Vendor risk management", "Supply chain",
  "Third-party risk assessment, due diligence questionnaires, automated risk scoring, continuous monitoring and contractual security clauses across the supply chain."),
 ("scan", "Security audits and testing", "Offensive security",
  "Penetration testing, vulnerability assessment, configuration review, social engineering simulations and reports written for both technical and board-level audiences."),
]

EN_DELIVERABLES = [
 "Gap assessment report with scoring by measure, sub-measure and control",
 "Information asset register and a threat catalogue tailored to your sector",
 "Risk register, assessment matrix and a risk treatment plan with defined risk appetite",
 "Policies and procedures behind every measure, ready for board approval",
 "Compliance roadmap with priorities, owners, deadlines and resource estimates",
 "Internal review report that simulates the audit or certification process",
 "Mapping of your existing certifications and standards onto CSA, DORA and GDPR requirements",
 "Every deliverable recorded in the GRC platform, with an audit trail and deadline tracking",
]

EN_PROCESS = [
 ("01", "Gap assessment", "We score the current state against every measure and control and list the evidence that is missing. The result is a number, not an impression.", "2 to 3 weeks"),
 ("02", "Remediation plan", "A prioritised compliance roadmap with owners, deadlines, resource estimates and a measurable target for each requirement.", "1 to 2 weeks"),
 ("03", "Implementation", "Policies, procedures, risk register and the records that stand behind each measure, together with staff training and management review.", "3 to 9 months"),
 ("04", "Platform and certification", "We walk through the documentation the way an auditor or certification body will, before they arrive. Everything lives in the GRC platform for continuous monitoring.", "Ongoing"),
]

EN_FAQ = [
 ("Who is an essential and who is an important entity under the Croatian Cybersecurity Act?",
  "The category is determined by sector and by the size of the entity, subject to exceptions. Essential entities are subject to an independent cybersecurity audit, while important entities carry out a self-assessment. You are notified of the categorisation in writing by the competent authority. For critical healthcare activities and for state administration bodies size is not the criterion - the category follows from the activity itself.",
  "Cybersecurity Act, OG 14/2024"),
 ("What are the 13 measures and where do they come from?",
  "The Croatian Cybersecurity Regulation breaks the statutory duties down into 13 cyber risk management measures, set out in 99 sub-measures across three levels of implementation: basic, medium and advanced. The level that applies to you depends on your entity category and on your risk assessment. The scope runs from security policy and risk management through to cryptography, supply chain security and physical protection. Every control requires written evidence.",
  "Cybersecurity Regulation, OG 135/2024, Annex II"),
 ("What is the deadline for becoming compliant?",
  "A twelve-month period runs from the delivery of the categorisation notice, not from the date the Act entered into force. The competent authority must deliver that notice within 30 days of the categorisation. After the compliance period ends, conformity is verified - by independent audit for essential entities, by self-assessment for important ones. In practice organisations lose the first quarter waiting for an internal owner to be appointed, so we recommend starting the gap assessment as soon as the notice arrives.",
  "Cybersecurity Act, OG 14/2024, Art. 26"),
 ("What are the incident reporting deadlines?",
  "An early warning to the competent CSIRT within 24 hours of becoming aware, an incident notification within 72 hours and a final report within 30 days. If the incident also involves a personal data breach, a parallel notification to the Croatian data protection authority runs within 72 hours under Article 33 GDPR. The deadlines do not add up - they run in parallel, so the reporting process has to be prepared in advance rather than improvised during the incident.",
  "Cybersecurity Act, OG 14/2024 &middot; GDPR, Art. 33"),
 ("How does the Croatian Cybersecurity Act relate to DORA?",
  "For the financial sector DORA is the more specific regime governing ICT risk management, resilience testing and oversight of ICT service providers. Entities subject to DORA do not thereby cease to be subject to other rules. The good news is that the evidence base overlaps heavily: the same asset register, the same risk register, the same register of third-party contracts and the same incident records. You do the work once and report it in several directions.",
  "DORA, EU 2022/2554"),
 ("Does an ISO 27001 certificate cover our obligations under the Act?",
  "Not automatically, but a large part of the work is already done. ISO/IEC 27001:2022 covers a substantial share of the 13 measures - security policy, risk management, asset management, access control, supply chain security and business continuity. What ISO does not cover are the specifics of the Act: entity categorisation, the deadlines and format for reporting incidents to the competent CSIRT, and the content of the self-assessment. We therefore map your existing controls onto the measures and only fill the gap, instead of building a second set of documentation in parallel.",
  "ISO/IEC 27001:2022, Annex A"),
 ("How long does a gap assessment take and what do we get?",
  "Two to three weeks for a mid-sized organisation. The result is a scored assessment against every measure and control, a list of the evidence that is missing, a risk register and a compliance roadmap with priorities, owners and resource estimates. Everything is recorded in our GRC platform straight away, so you track progress continuously and with an audit trail rather than once a year in a spreadsheet.",
  None),
 ("Do you also perform the audit or the certification?",
  "No. We prepare you for it. The independent cybersecurity audit of essential entities is carried out by an authorised provider, and for state administration bodies by the competent authority. ISO certification is carried out by an accredited certification body. Whoever built the management system should not also assess it - that separation is not a formality, it protects you.",
  None),
]

EN_AUTHORITIES = [
 ("SOA", "central cybersecurity authority"),
 ("NCSC-HR", "incident reporting"),
 ("ZSIS / UVNS", "state administration bodies"),
 ("AZOP", "personal data breaches"),
 ("CNB / HANFA", "DORA, financial sector"),
 ("HAKOM", "digital infrastructure sector"),
]

EN_CLIENTS = [
 ("Banking and finance", ["Zagreb Stock Exchange", "Šted banka", "Partner banka", "Euroleasing", "Fintastic", "Krypto Investment Partners"]),
 ("Insurance", ["Croatia osiguranje", "Adriatic osiguranje", "Sunce osiguranje", "UNIQA osiguranje", "ANO Insurance Solutions"]),
 ("Energy and industry", ["HROTE", "E.ON", "INA", "IHC Engineering Croatia", "TEHMA", "MCZ"]),
 ("IT and digital services", ["APIS-IT", "Rocket DBS", "SmartGroup HR Solutions", "SmartGroup Recruitment", "BCC Services", "Digital Assembly", "AMODO", "Cooperante", "TPA Hrvatska"]),
 ("Food industry", ["Franck d.d.", "Pan-pek", "Mlinar", "Adria Snack Company", "Offertissima"]),
 ("Health and pharma", ["Medika d.d.", "Biovega", "Delmerion Natural Beauty"]),
 ("Business services", ["EOS Matrix", "Log Adria", "Kompas", "Travel Experience Museum", "Hrvatski Telekom", "Hajduk Split"]),
]

# ══════════════════════════════════════════════════════════════════
# Engleski clanci
# ══════════════════════════════════════════════════════════════════
MJERE_EN = [
 (1, "Commitment and accountability of those responsible for implementing cyber risk management measures", 11,
     "The board approves the policy, appoints responsible people, provides resources and is reported to regularly. Without this the other measures have no owner."),
 (2, "Management of software and hardware assets", 9,
     "An inventory of all assets, identification of critical assets, data classification and rules for disposal and reuse of equipment."),
 (3, "Risk management", 8,
     "A documented risk assessment process on an all-hazards basis, the level and criticality of each risk, a named risk owner and a treatment plan."),
 (4, "Security of human resources and digital identities", 12,
     "Pre-employment checks, contractual duties, access rights across the full lifecycle and separate accounts for administrators."),
 (5, "Basic cyber hygiene practices", 11,
     "Patching, backups, endpoint protection, email and browser security, staff training and awareness."),
 (6, "Securing network cyber security", 5,
     "Segmentation, perimeter protection, network traffic monitoring and secure configuration of network equipment."),
 (7, "Physical and logical access control to network and information systems", 6,
     "Least privilege, multi-factor authentication, privileged access management and access records."),
 (8, "Supply chain security", 6,
     "Minimum security requirements for suppliers, contractual clauses, third-party risk assessment and monitoring over time."),
 (9, "Security in the development and maintenance of network and information systems", 6,
     "Security requirements in development, separated environments, change management and testing before go-live."),
 (10, "Cryptography", 6,
     "Rules on the use of cryptography, protection of data in transit and at rest, key management and preparation for quantum-resistant cryptography."),
 (11, "Incident handling", 6,
     "Detection, classification and escalation, a response plan, notification to the competent CSIRT within the prescribed deadlines and post-incident analysis."),
 (12, "Business continuity and cyber crisis management", 8,
     "Business impact analysis, continuity and recovery plans, crisis management and regular exercising of the plans."),
 (13, "Physical security", 5,
     "Protection of areas holding equipment, entry control, fire and water protection, and power and cabling security."),
]

def mjere_tablica_en():
    rows = "\n".join(
      '      <tr><td class="num">%02d</td><td><strong>%s</strong><br><span style="color:#94a3b8;font-size:13.5px">%s</span></td><td class="num">%d</td></tr>'
      % (br, naziv, opis, pod) for br, naziv, pod, opis in MJERE_EN)
    return '''<div class="tbl-wrap">
  <table>
    <thead><tr><th>Measure</th><th>Name and what it asks for in practice</th><th>Sub-measures</th></tr></thead>
    <tbody>
%s
      <tr><td class="num">&Sigma;</td><td><strong>Total</strong></td><td class="num">99</td></tr>
    </tbody>
  </table>
</div>''' % rows

ARTICLES_EN = []

ARTICLES_EN.append(dict(
 slug="entity-categorisation-croatian-cybersecurity-act", cat="CSA / NIS2", catkey="csa",
 date="2026-01-20", read=7,
 title="Entity categorisation under the Croatian Cybersecurity Act, and what follows from it",
 lead="You do not choose your category and you do not apply for it. It arrives by letter, and from that day a deadline runs. Here is who decides, on what basis, and what actually changes depending on which group you land in.",
 desc="How it is determined whether you are an essential or an important entity under the Croatian Cybersecurity Act, which deadlines run from the categorisation notice, and how the duties of the two groups differ.",
 body='''
<p>The Croatian Cybersecurity Act (Official Gazette 14/2024), which transposes NIS2, splits those in scope into two groups: <strong>essential</strong> and <strong>important</strong> entities. The difference is not cosmetic. It determines the level at which you must implement the measures, who checks that you have, and what that check costs you.</p>

<h2>Sector and size decide, subject to exceptions</h2>
<p>The starting point is the annexes to the Act, which list the sectors in scope. Within a sector, the category is as a rule derived from the size of the entity against the criteria for medium and large undertakings. That is the rule. The exceptions are what matter.</p>
<p>For <strong>state administration bodies</strong> and for <strong>certain critical healthcare activities</strong>, size is not the criterion. There the category follows from the activity itself, so a small institution can be an essential entity just as a large one is. This is the most common source of surprise: an organisation that considers itself small by headcount opens the letter and reads that it is an essential entity.</p>
<div class="callout">
  <div class="c-label">What this means in practice</div>
  <p>Do not try to work out your own category and budget against it. A sectoral exception can change the whole scenario. Plan for the less favourable outcome until the written notice arrives.</p>
</div>

<h2>What the category actually changes</h2>
<p>Both groups implement <strong>the same 13 measures</strong> from Annex II of the Cybersecurity Regulation (OG 135/2024). What differs is the level of implementation and the method of verification.</p>
<div class="tbl-wrap">
  <table>
    <thead><tr><th></th><th>Important entity</th><th>Essential entity</th></tr></thead>
    <tbody>
      <tr><td><strong>Measures</strong></td><td>The same 13 measures</td><td>The same 13 measures</td></tr>
      <tr><td><strong>Level of implementation</strong></td><td>As a rule lower</td><td>As a rule higher</td></tr>
      <tr><td><strong>Verification</strong></td><td>Self-assessment</td><td>Independent audit</td></tr>
      <tr><td><strong>Who verifies</strong></td><td>The entity itself, following the guidance</td><td>An authorised external provider; for state bodies, the competent authority</td></tr>
      <tr><td><strong>Cost of verification</strong></td><td>Internal effort</td><td>External engagement</td></tr>
    </tbody>
  </table>
</div>
<p>One point that is regularly missed: <strong>a self-assessment is also a formal procedure</strong>. It is not an internal opinion but a scoring exercise against a prescribed framework, with evidence that has to exist at the time of assessment. The difference from an audit is who holds the pen, not whether an evidence base is needed.</p>

<h2>The clock starts with the notice, not with the Act</h2>
<p>This is the most expensive misunderstanding in practice. The Act has been in force since 2024, but your deadline did not start then.</p>
<ul>
  <li><strong>30 days</strong> - the period within which the competent authority must notify you of the categorisation or a change to it.</li>
  <li><strong>12 months</strong> - the compliance period, running from the delivery of that notice.</li>
  <li><strong>Up to two further years</strong> - the window within which conformity is verified, by independent audit or self-assessment depending on category.</li>
  <li><strong>60 days to 6 months</strong> - the period the competent authority sets when a category changes, proportionate to the scope and complexity of the new duties.</li>
</ul>
<div class="callout">
  <div class="c-label">Where the time goes</div>
  <p>The first quarter is usually spent internally appointing someone to own the work. The deadline runs in the meantime. If the notice has arrived, the gap assessment can start before that appointment is formalised - you need the asset inventory and the risk register either way.</p>
</div>

<h2>What to do in the first week after the notice</h2>
<ol>
  <li><strong>Record the date of delivery.</strong> Not the date on the letter, the date of delivery. All twelve months are counted from it.</li>
  <li><strong>Establish the level of implementation</strong> that applies to you and any sectoral duties that came with the categorisation.</li>
  <li><strong>Appoint a responsible person</strong> and give them access to the board. Measure 1 of Annex II asks for exactly that, and it is scored.</li>
  <li><strong>Build the asset inventory.</strong> Without it you cannot produce a risk assessment, and without a risk assessment almost no other measure passes.</li>
  <li><strong>Check the overlaps.</strong> If you hold ISO 27001, are subject to DORA or have a working GDPR programme, part of the evidence base already exists. Map before you start writing new documents.</li>
</ol>

<h2>If you believe you have been miscategorised</h2>
<p>Categorisation is based on the sector and size data the authority holds. If that data is wrong, or your activity has changed, that is a matter to raise with the competent authority - it is not a reason to let the deadline run unattended. Until it is resolved, the clock runs on the notice you received.</p>
''',
 sources=[('Cybersecurity Act, OG 14/2024 (Croatian)', 'https://narodne-novine.nn.hr/clanci/sluzbeni/2024_02_14_222.html'),
          ('Cybersecurity Regulation, OG 135/2024 (Croatian)', 'https://narodne-novine.nn.hr/clanci/sluzbeni/2024_11_135_2217.html'),
          ('Directive (EU) 2022/2555 (NIS2)', 'https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32022L2555')]))

ARTICLES_EN.append(dict(
 slug="thirteen-measures-annex-ii", cat="CSA / NIS2", catkey="csa",
 date="2026-02-10", read=9, featured=True,
 title="13 measures, 99 sub-measures, 132 controls: the anatomy of Annex II",
 lead="The Croatian Cybersecurity Regulation does not speak of ten NIS2 measures but of thirteen of its own. Beneath them sit 99 sub-measures, and behind those a catalogue of 132 controls with scoring thresholds. This is the map of the whole structure, measure by measure.",
 desc="A complete overview of the 13 cyber risk management measures from Annex II of the Croatian Cybersecurity Regulation: sub-measures per measure, what each asks for in practice, and how they connect to the control catalogue.",
 body='''
<p>The most common mistake in preparing for the Croatian Cybersecurity Act starts from the wrong list. NIS2 Article 21(2) enumerates ten groups of measures, so the figure ten keeps circulating in presentations and proposals. <strong>The Croatian Cybersecurity Regulation (OG 135/2024) breaks them down into thirteen measures</strong>, and those are what you will be assessed against.</p>
<p>The difference is not only in the counting. The Regulation sets the measures out in sub-measures, and the Croatian Information Systems Security Bureau (ZSIS) has published an evaluation framework alongside them with specific controls and scoring thresholds. If you are preparing evidence against the ten-point NIS2 list, some of that evidence will have nowhere to sit.</p>

<div class="callout">
  <div class="c-label">A three-level structure</div>
  <p>A <strong>measure</strong> has a name and an objective. Within it sit <strong>sub-measures</strong> - concrete duties phrased as verbs (develop, document, implement, update). Each sub-measure carries a <strong>set of controls</strong> from the catalogue, and each control has a prescribed minimum score for the basic, medium and advanced levels.</p>
</div>

<h2>All thirteen measures</h2>
<p>The names are official, translated from Annex II of the Regulation and the ZSIS evaluation framework. The sub-measure counts are taken from that framework and add up to exactly 99.</p>
__TABLICA__
<p>The controls per measure add up to more than 132 because individual controls are reused across measures. The control catalogue contains 132 unique identifiers, grouped into thirteen prefixes (POL, INV, RIZ, DID, EDU, UPR, NAD, RES, ORG, SKM, POD, SRZ, FIZ).</p>

<h2>Where most of the work sits</h2>
<p>Judging by sub-measure count alone, the weight is clear: <strong>measure 4 (security of human resources and digital identities)</strong> with twelve, and <strong>measures 1 and 5</strong> with eleven each. That is not an accident. All three are organisational rather than technical.</p>
<p>The consequence is uncomfortable for teams that treat this as an IT project: most of the evidence base is not produced in the server room but in HR, in board meetings and in training records. A firewall is configured in a day. Evidence that the board approved the policy, received a report and allocated resources cannot be manufactured retrospectively.</p>

<h2>Three levels of implementation</h2>
<p>Each measure is assessed at one of three levels: <strong>basic, medium or advanced</strong>. The level is not freely chosen - it follows from the entity category and from the risk assessment. The same sub-measure at the advanced level demands a higher result on the same controls, and sometimes additional controls that do not apply at the basic level at all.</p>
<p>In the evaluation framework those conditional controls are marked with an asterisk. Sub-measure 10.6 is an example: it requires quantum-resistant cryptography proportionate to assessed risk. It is marked conditional at every level, which means your risk assessment can create an obligation you would otherwise have skipped on category alone.</p>

<h2>What this looks like once it becomes a plan</h2>
<p>Ninety-nine sub-measures sounds unmanageable until they are sorted on three criteria:</p>
<ul>
  <li><strong>What you already have.</strong> An organisation with a working ISO 27001 system typically has substantial coverage of measures 2, 3, 7, 8 and 12. That gets mapped, not rewritten.</li>
  <li><strong>What has no owner.</strong> A sub-measure without a named owner will not get done, however simple it is.</li>
  <li><strong>What has the longest lead time.</strong> A policy takes a week to write. An annual board reporting cycle, a continuity plan exercise and a training record all need calendar time that cannot be compressed.</li>
</ul>
<p>That last point explains why twelve months is not generous. Several measures are evidenced by records that only come into existence once a cycle has run.</p>

<div class="note">
  <p><strong>A note on versions.</strong> The control catalogue and thresholds are published by ZSIS and revised through new versions of the guidance. Check which version is current before a formal self-assessment.</p>
</div>
''',
 sources=[('Cybersecurity Regulation, OG 135/2024, Annex II (Croatian)', 'https://narodne-novine.nn.hr/clanci/sluzbeni/2024_11_135_2217.html'),
          ('ZSIS - Annex B, Framework for the evaluation of cyber risk management measures', 'https://www.zsis.hr/UserDocsImages/Samoprocjena/Prilog%20B%20-%20Okvir%20za%20evaluaciju.pdf'),
          ('ZSIS - Annex C, Control catalogue', 'https://www.zsis.hr/UserDocsImages/Samoprocjena/Prilog%20C%20-%20Katalog%20kontrola.pdf'),
          ('Directive (EU) 2022/2555 (NIS2), Art. 21', 'https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32022L2555')]))

ARTICLES_EN.append(dict(
 slug="how-self-assessment-is-scored", cat="Self-assessment", catkey="selfassessment",
 date="2026-09-01", read=6,
 title="How the self-assessment is actually scored: the Pi and T thresholds",
 lead="You can satisfy every individual control and still fail the sub-measure. The evaluation framework has two thresholds, and the second one is the surprise. Here is how the formula works and what it means for planning.",
 desc="An explanation of the scoring system in the ZSIS evaluation framework: the minimum threshold per control, the additional average threshold per sub-measure, and why formal compliance is not enough.",
 body='''
<p>The self-assessment under the Croatian Cybersecurity Regulation is not a yes/no questionnaire. It is a scoring exercise with two thresholds that must be met simultaneously, and organisations that realise this late usually find they have been working towards the wrong target.</p>

<h2>Two thresholds, not one</h2>
<p>Every sub-measure has its own set of controls. For each control the framework prescribes a minimum score to pass, depending on the level of implementation. But that is not all.</p>
<div class="callout">
  <div class="c-label">The condition for passing a sub-measure</div>
  <p><strong>1.</strong> Every individual control must reach its minimum threshold (O<sub>i</sub> &ge; P<sub>i</sub>, for every control i).</p>
  <p><strong>2.</strong> The average score across all controls in the sub-measure must reach an additional threshold (&sum;O<sub>i</sub> / n &ge; T).</p>
  <p>Both conditions must hold. If the average does not pass, the sub-measure fails regardless of every control having passed individually.</p>
</div>
<p>An example from the framework: sub-measure 3.2, risk assessment over critical assets. At the basic level the controls carry thresholds of &ge;3, &ge;2, &ge;2 and &ge;2, with an additional average threshold of &gt;2.5. An organisation that brings each control to exactly its minimum scores an average of 2.25 and <strong>fails the sub-measure</strong>, despite having formally satisfied every individual criterion.</p>

<h2>Why the second threshold exists</h2>
<p>The framework says so explicitly: the additional threshold acts as a final check on whether the controls are genuinely applied and integrated, rather than merely formally satisfied. The aim is to prevent a system in which every box is ticked while the measure does not work in practice.</p>
<p>The same logic goes one step further. If a measure is found not to be effective or not integrated into the risk management system, it can be assessed as unsatisfactory even where the controls formally pass. That room for judgement exists deliberately.</p>

<h2>What this changes in planning</h2>
<ul>
  <li><strong>Do not aim at the minimum.</strong> Planning to "just about enough" on each individual control leads mathematically to failure on the average. Aim at the average threshold and work the controls back from there.</li>
  <li><strong>One weak control damages the sub-measure twice.</strong> It fails on its own and it drags the average down. The lowest-scoring controls are the most economical to fix.</li>
  <li><strong>The average is computed within a sub-measure, not within a measure.</strong> A strong result on one sub-measure does not compensate for a weak one elsewhere.</li>
  <li><strong>Scores are assigned against the control catalogue.</strong> Scoring by feel does not survive verification, because every score has to be defensible with evidence.</li>
</ul>

<h2>Levels change the thresholds, not the controls</h2>
<p>Moving from the basic to the medium level generally does not bring a new list of controls but higher thresholds on the same ones. The typical pattern is a shift from &ge;2 to &ge;3, with the average threshold moving from 2.0 to 3.0. That matters, because an organisation preparing for the basic level and then recategorised does not have to build a new system - it has to deepen the one it has.</p>
<p>The exception is the controls marked with an asterisk, which apply conditionally depending on the risk assessment. Those can be triggered even at the basic level.</p>

<h2>A practical check before the formal exercise</h2>
<p>Before the self-assessment is submitted, it is worth running an internal review that simulates the process: score every control, compute the averages per sub-measure, and look at which sub-measures fail on the second threshold. The list is almost always shorter than expected, and it almost always contains sub-measures the team was confident were finished.</p>

<div class="note">
  <p><strong>A note on versions.</strong> The formula and thresholds are published by ZSIS and revised through new versions of the guidance. Check which version is current before a formal self-assessment.</p>
</div>
''',
 sources=[('ZSIS - Annex B, Framework for the evaluation of cyber risk management measures', 'https://www.zsis.hr/UserDocsImages/Samoprocjena/Prilog%20B%20-%20Okvir%20za%20evaluaciju.pdf'),
          ('Cybersecurity Regulation, OG 135/2024, Art. 42 and 51-54 (Croatian)', 'https://narodne-novine.nn.hr/clanci/sluzbeni/2024_11_135_2217.html')]))

ARTICLES_EN.append(dict(
 slug="incident-reporting-deadlines", cat="Incidents", catkey="incidents",
 date="2026-04-14", read=6,
 title="24 hours, 72 hours, 30 days: deadlines that run in parallel",
 lead="The deadlines for reporting a significant incident do not add up and do not wait for one another. And if the incident also involves a personal data breach, a fourth deadline runs alongside them, under a different instrument and to a different authority.",
 desc="Deadlines for reporting a significant cyber incident under the Croatian Cybersecurity Act: early warning within 24 hours, notification within 72 hours, final report within 30 days, and the parallel notification under Article 33 GDPR.",
 body='''
<p>Incident reporting is the measure that is easiest to describe and hardest to execute. The reason is simple: every other measure gets done in working hours, and this one at three in the morning, while you are simultaneously trying to stop what is happening.</p>

<h2>Three deadlines under the Act</h2>
<div class="tbl-wrap">
  <table>
    <thead><tr><th>Deadline</th><th>What is sent</th><th>Content</th></tr></thead>
    <tbody>
      <tr><td class="num">24 hours</td><td>Early warning</td><td>That a significant incident has occurred, an initial view on whether it results from an unlawful act and whether it may have cross-border impact.</td></tr>
      <tr><td class="num">72 hours</td><td>Incident notification</td><td>Updated assessment, indicators of compromise, severity and impact.</td></tr>
      <tr><td class="num">30 days</td><td>Final report</td><td>Detailed description, threat type and root cause, measures applied and planned, cross-border effect.</td></tr>
    </tbody>
  </table>
</div>
<p>The deadlines run <strong>from becoming aware of the incident</strong>, not from when it occurred and not from when the investigation concludes. That distinction decides whether you are within the deadline.</p>

<div class="callout">
  <div class="c-label">The most common mistake</div>
  <p>The 24-hour deadline is not a deadline for explaining what happened. It is a deadline for reporting <em>that</em> something happened. Teams that wait to understand the incident before sending the early warning routinely miss the first deadline, and have gained nothing in return.</p>
</div>

<h2>The fourth deadline, running alongside</h2>
<p>If the incident also involves a personal data breach, a <strong>separate 72-hour deadline for notifying the data protection authority</strong> runs alongside the ones under the Act, under Article 33 GDPR. It is a separate notification, to a different authority, with different content.</p>
<p>The two do not cancel each other out and they do not run in sequence. Ransomware that halted production and simultaneously exfiltrated an HR database creates both obligations in the same hour.</p>

<h2>What has to be ready beforehand, not afterwards</h2>
<ul>
  <li><strong>A significance criterion.</strong> Someone has to be able to say within the hour whether this is a significant incident. If that question is being asked for the first time during the incident, the clock is already running.</li>
  <li><strong>A named person and a deputy.</strong> Incidents do not confine themselves to working days. If only one person can send the notification, you have an availability risk inside the measure itself.</li>
  <li><strong>Prepared forms.</strong> An early warning template with fields to fill in, not a document to be written.</li>
  <li><strong>Contact details for the competent CSIRT</strong> and credentials for the reporting channel, verified before they are needed.</li>
  <li><strong>A decision path for the parallel notification.</strong> Who assesses whether a personal data breach is involved, and who then notifies the data protection authority.</li>
  <li><strong>Records.</strong> Time of awareness, who decided what, and when each item was sent. That is your evidence of being within the deadline.</li>
</ul>

<h2>The exercise is worth more than the plan</h2>
<p>An incident response plan that has never been tested documents intent, not capability. A two-hour tabletop exercise with a scenario and real measurement of the time to a prepared early warning will reveal more than another round of editing the document. In practice it usually reveals that nobody is sure who makes the significance call.</p>

<div class="note">
  <p>Incident reporting sits under measure 11 of Annex II, but the evidence base overlaps with measure 12 (business continuity and cyber crisis management). If the incident response plan and the continuity plan are written as two unconnected documents, the work is being done twice.</p>
</div>
''',
 sources=[('Cybersecurity Act, OG 14/2024 (Croatian)', 'https://narodne-novine.nn.hr/clanci/sluzbeni/2024_02_14_222.html'),
          ('Cybersecurity Regulation, OG 135/2024 (Croatian)', 'https://narodne-novine.nn.hr/clanci/sluzbeni/2024_11_135_2217.html'),
          ('Regulation (EU) 2016/679 (GDPR), Art. 33', 'https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679')]))

ARTICLES_EN.append(dict(
 slug="iso-27001-and-the-cybersecurity-act", cat="ISO standards", catkey="iso",
 date="2026-03-03", read=7,
 title="You hold ISO 27001. How much is it worth under the Cybersecurity Act?",
 lead="The certificate does not release you from the obligation, but it shortens the path considerably. The question is only which measures it covers, which it touches, and which it does not reach at all - and how to prove that without writing a second set of documentation in parallel.",
 desc="How much of the 13 measures of the Croatian Cybersecurity Regulation is covered by ISO/IEC 27001:2022, where the real gaps are, and how to map existing controls instead of writing new documentation.",
 body='''
<p>First, to be clear: <strong>an ISO 27001 certificate does not substitute for compliance with the Croatian Cybersecurity Act</strong>. There is no provision exempting a certified entity from implementing the measures in Annex II. But the relationship is far from useless - on the contrary, an organisation with a working ISMS usually holds most of the required material, just in a different arrangement.</p>

<h2>Where the overlap is strong</h2>
<p>The standard and the Regulation share the same management logic: know what you have, know what threatens it, decide what to do about it, record it and review it. That shows up in several measures where an ISO organisation typically has nearly everything:</p>
<ul>
  <li><strong>Measure 2, asset management.</strong> Inventory, ownership, classification - present.</li>
  <li><strong>Measure 3, risk management.</strong> Methodology, risk register, treatment plan, owners - present, with one caveat below.</li>
  <li><strong>Measure 7, access control.</strong> Access policy, least privilege, privileged access - present.</li>
  <li><strong>Measure 8, supply chain security.</strong> Supplier relationship controls - present, usually at a higher level than in organisations without the standard.</li>
  <li><strong>Measure 12, business continuity.</strong> If ISO 22301 is in place alongside 27001, effectively covered.</li>
  <li><strong>Measure 1, management commitment.</strong> Leadership, policy, roles and responsibilities, management review - present as a structure, though the content needs extending.</li>
</ul>

<h2>Where the overlap is partial</h2>
<p>This is where most of the misunderstanding arises, because it looks finished and is not.</p>
<h3>All-hazards risk assessment</h3>
<p>The Regulation requires an assessment covering all categories of hazard - including fire, flood, power loss, failure of communications infrastructure and unauthorised physical access. Many ISMS risk assessments stay within the bounds of information threats. The methodology is the same; the scope is not.</p>
<h3>Physical security</h3>
<p>Measure 13 is a standalone measure with its own sub-measures. In the standard it is a set of controls inside Annex A. The material exists, but it has to be pulled out and evidenced sub-measure by sub-measure, rather than shown as part of a wider set.</p>
<h3>Cryptography</h3>
<p>Measure 10 requires rules on use, protection of data in transit and at rest, key management and - proportionate to risk - preparation for quantum-resistant cryptography. The last of these is newer than most ISMS documentation we see.</p>

<h2>Where the standard does not help</h2>
<p>Three groups of obligations have no equivalent in the standard, because they come from legislation rather than management practice:</p>
<ol>
  <li><strong>Categorisation and everything that follows from it.</strong> Level of implementation, competent authority, deadlines.</li>
  <li><strong>Incident reporting within prescribed deadlines.</strong> The standard requires an incident management process, but knows nothing of 24-hour, 72-hour and 30-day deadlines or notification to a competent CSIRT.</li>
  <li><strong>The format and procedure of verification.</strong> A self-assessment against a scoring framework, or an independent audit, has nothing to do with a certification audit against the standard.</li>
</ol>

<div class="callout">
  <div class="c-label">The practical conclusion</div>
  <p>ISO 27001 shortens the path but does not change the destination. A realistic expectation: a working ISMS covers a substantial part of the evidence base, and the remainder is filled in. An ISMS that is not working - built for the certificate and unused since - helps almost not at all, because exactly the records that prove the system is alive are what is missing.</p>
</div>

<h2>How to do this without duplication</h2>
<ol>
  <li><strong>Map before you write.</strong> Every sub-measure gets a reference to an existing document, record or control from the Statement of Applicability. The gaps are whatever is left without a reference.</li>
  <li><strong>Extend, do not copy.</strong> If the existing risk methodology does not cover all hazard categories, widen the scope in the existing document. A second methodology means two risk registers that will diverge.</li>
  <li><strong>One asset register.</strong> If the ISMS information asset list and the inventory for the Act are maintained separately, one of them will go stale and you will not know which.</li>
  <li><strong>Fill what is genuinely missing.</strong> Incident reporting, categorisation, self-assessment preparation.</li>
</ol>
<p>The same approach applies to entities subject to DORA and to organisations with an established GDPR programme. The evidence base overlaps far more than the names of the instruments suggest.</p>
''',
 sources=[('Cybersecurity Regulation, OG 135/2024, Annex II (Croatian)', 'https://narodne-novine.nn.hr/clanci/sluzbeni/2024_11_135_2217.html'),
          ('ZSIS - Annex B, Framework for the evaluation of measures', 'https://www.zsis.hr/UserDocsImages/Samoprocjena/Prilog%20B%20-%20Okvir%20za%20evaluaciju.pdf'),
          ('ISO/IEC 27001:2022 - Information security management systems', None)]))

ARTICLES_EN.append(dict(
 slug="risk-register-that-passes-review", cat="Risk management", catkey="risk",
 date="2026-03-24", read=6,
 title="A risk register that passes review: five recurring mistakes",
 lead="The risk register is the document everyone has and almost nobody uses. Five patterns repeat from organisation to organisation, and all five are visible on a first reading.",
 desc="The most common mistakes in risk registers that surface during compliance reviews: no link to the asset inventory, risks without owners, scores without reasoning, treatment plans without deadlines, and a register that never changes.",
 body='''
<p>Measure 3 of Annex II of the Croatian Cybersecurity Regulation requires a documented risk management process with assessment, levels, owners and a treatment plan. Most organisations have a document that looks like that. A minority have one that survives questioning.</p>
<p>These are the recurring patterns, ordered by how quickly they are spotted.</p>

<h2>1. The register is not linked to the asset inventory</h2>
<p>The risk reads "data loss" or "cyber attack", with no indication of which asset. Such an entry can be neither treated nor verified - it is not clear what is being protected, nor when the risk has ceased to exist.</p>
<p>The Regulation explicitly ties the risk assessment to assets from the critical asset inventory. If the risk register and the asset register share no common reference, two measures that should stand on one another are standing next to one another instead.</p>
<div class="callout">
  <div class="c-label">A one-sentence check</div>
  <p>Take a random row from the risk register and try to find the corresponding entry in the asset inventory. If that takes longer than a minute, the link does not exist.</p>
</div>

<h2>2. Risks have a department, not an owner</h2>
<p>The owner column says "IT". A department cannot decide to accept a risk, cannot be held accountable and cannot report to the board. The Regulation requires identification of risk owners and their area of responsibility - which means a person with a name.</p>
<p>The consequence is predictable: a risk owned by a department stays open for years because nobody individually is late.</p>

<h2>3. The score exists, the reasoning does not</h2>
<p>Likelihood 3, impact 4, level high. Why 3 and not 2? When was it last reviewed? Without a trace of reasoning, a score is a number that can be neither defended nor challenged.</p>
<p>This bites particularly in a self-assessment, where every score has to be defensible with evidence. A risk register whose scores were produced in a meeting without minutes creates the same problem one level up.</p>

<h2>4. The treatment plan is a wish list</h2>
<p>Treatment measures are phrased as "improve monitoring" or "consider additional protection", with no deadline, owner or resource estimate. That is not a treatment plan but a record of good intentions.</p>
<p>The Regulation requires the response to a risk to be proportionate to its level and criticality, through appropriate technical, operational and organisational measures. Proportionality cannot be assessed if the measure is not specific.</p>
<ul>
  <li>Poor: "improve access management"</li>
  <li>Good: "enforce multi-factor authentication on all administrator accounts, owner M. K., due 31 March, estimated 12 working days"</li>
</ul>

<h2>5. The register never changes</h2>
<p>The clearest signal that the system is not alive. The same thirty-two risks, the same scores, the only change being the date in the header. The Regulation requires the process to be updated annually, but substantive updating means something else: new risks come in, resolved ones are closed, scores change when circumstances do.</p>
<p>A register that has not changed after a new system went live, after a change of supplier or after an incident is telling you it is not used in decision-making but maintained for review.</p>

<h2>What distinguishes a register that passes</h2>
<p>Not size. We have seen hundred-row registers that fail and twenty-five-row registers that pass without comment. Five things separate them:</p>
<ol>
  <li>Every risk points to an asset in the inventory.</li>
  <li>Every risk has a person as its owner.</li>
  <li>Every score carries a short justification and a date.</li>
  <li>Every treatment measure has a deadline, an owner and a resource estimate.</li>
  <li>There is a trace of the register changing, with a reason for the change.</li>
</ol>
<p>The fifth is also the hardest to produce retrospectively, which is why the risk register is not something to leave until the end of a compliance project.</p>

<div class="note">
  <p>The risk register is an input to several other measures: it determines the level of implementation for conditional controls, it justifies the selection of measures in the compliance roadmap, and it connects to third-party risk assessment under measure 8. A weak risk register does not fail alone - it takes down everything that relies on it.</p>
</div>
''',
 sources=[('Cybersecurity Regulation, OG 135/2024, Annex II, measure 3 (Croatian)', 'https://narodne-novine.nn.hr/clanci/sluzbeni/2024_11_135_2217.html'),
          ('ZSIS - Annex B, Framework for the evaluation of measures, measure 3', 'https://www.zsis.hr/UserDocsImages/Samoprocjena/Prilog%20B%20-%20Okvir%20za%20evaluaciju.pdf')]))

# ══════════════════════════════════════════════════════════════════
# Sklapanje engleske naslovnice
# ══════════════════════════════════════════════════════════════════
def en_index():
    legal = "\n".join(
      ('        <a class="legal-item" href="%s" target="_blank" rel="noopener">%s</a>' % (u, inner)) if u
      else ('        <div class="legal-item">%s</div>' % inner)
      for code, ref, desc, u in EN_LEGAL
      for inner in ['<div class="legal-code">%s</div><div class="legal-ref">%s</div><div class="legal-desc">%s</div>' % (code, ref, desc)])

    services = "\n".join('''      <div class="service-card">
        <div class="card-icon">%s</div>
        <div class="card-title">%s</div>
        <div class="card-desc">%s</div>
        <div class="card-footer"><span class="card-badge">%s</span><a class="card-more" href="#contact">Ask about this &rarr;</a></div>
      </div>''' % (svg(ic), name, desc, badge) for ic, name, badge, desc in EN_SERVICES)

    sectors = "\n".join('        <div class="sector-card"><div class="sector-name">%s</div><div class="sector-note">%s</div></div>'
                        % (a, b) for a, b in EN_SECTORS)
    authorities = "\n".join('      <span class="authority"><strong>%s</strong> &middot; %s</span>' % (a, b)
                            for a, b in EN_AUTHORITIES)
    steps = "\n".join('      <div class="step"><div class="step-num">%s</div><div class="step-title">%s</div><div class="step-desc">%s</div><span class="step-dur">%s</span></div>'
                      % s for s in EN_PROCESS)
    CHK = '<svg viewBox="0 0 24 24"><path d="M20 6 9 17l-5-5"/></svg>'
    deliverables = "\n".join('        <div class="deliver-item">%s<span>%s</span></div>' % (CHK, d)
                             for d in EN_DELIVERABLES)
    clients = "\n".join('''      <div class="ref-category">
        <div class="ref-cat-label">%s</div>
        <div class="ref-logos">%s</div>
      </div>''' % (cat, "".join('<span class="ref-chip">%s</span>' % c for c in items))
      for cat, items in EN_CLIENTS)
    faq = "\n".join('''      <div class="faq-item">
        <button class="faq-q" type="button" aria-expanded="false" onclick="toggleFaq(this)">%s</button>
        <div class="faq-a"><p>%s</p>%s</div>
      </div>''' % (q, a, ('<span class="faq-cite">%s</span>' % c) if c else '')
      for q, a, c in EN_FAQ)

    posts_en = "\n".join('''      <a class="kb-card" href="/en/blog/%s/">
        <div class="kb-cat">%s</div>
        <div class="kb-title">%s</div>
        <div class="kb-lead">%s</div>
        <div class="kb-meta">%d min read</div>
      </a>''' % (a["slug"], a["cat"], a["title"], a["lead"], a["read"]) for a in ARTICLES_EN[:3])

    body = en_header() + '''

<!-- ═══ HERO ═══ -->
<section class="hero">
  <div class="hero-inner">
    <div class="hero-left">
      <div class="hero-tag">CSA / NIS2 &middot; GDPR &middot; DORA &middot; ISO</div>
      <h1 class="hero-h1">Risk management.<br>Compliance.<br><em>Security.</em></h1>
      <p class="hero-sub">We know what the regulator asks for and what proves it. We work with essential and important entities on the Croatian Cybersecurity Act, on data protection and on ISO standards - and we tell you who does what, in what order, and which piece of evidence stands behind each measure.</p>
      <div class="hero-btns">
        <a href="#services" class="btn-primary">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
          Our services
        </a>
        <a href="#contact" class="btn-outline">Request a proposal &rarr;</a>
      </div>
      <div class="compliance-badges">
        <span class="cbadge">CSA / NIS2</span><span class="cbadge">GDPR</span>
        <span class="cbadge">ISO 27001</span><span class="cbadge">ISO 9001</span>
        <span class="cbadge">ISO 14001</span><span class="cbadge">ISO 22301</span>
        <span class="cbadge">DORA</span><span class="cbadge">Vendor Risk</span>
        <span class="cbadge">Pen Testing</span>
      </div>
    </div>
    <div class="hero-right">
''' + EN_CHART + '''
    </div>
  </div>
  <svg class="hero-bg-icon" width="600" height="600" viewBox="0 0 100 100" fill="none">
    <path d="M50 5 L90 27.5 L90 72.5 L50 95 L10 72.5 L10 27.5 Z" stroke="white" stroke-width=".5"/>
    <path d="M50 16 L80 33 L80 67 L50 84 L20 67 L20 33 Z" stroke="white" stroke-width=".4"/>
    <path d="M50 27 L70 38.5 L70 61.5 L50 73 L30 61.5 L30 38.5 Z" stroke="white" stroke-width=".3"/>
  </svg>
</section>

<!-- ═══ LEGAL FRAMEWORK ═══ -->
<section class="legal-strip" id="framework">
  <div class="container">
    <div class="legal-head">
      <h2>The legal framework we work in</h2>
      <p>Six instruments and two standards that keep overlapping in practice: the same asset inventory, the same risk register, the same records.</p>
    </div>
    <div class="legal-grid">
''' + legal + '''
    </div>
  </div>
</section>

<div class="section-divider"></div>

<!-- ═══ ABOUT ═══ -->
<section id="about" class="onama-section">
  <div class="container">
    <div class="section-header">
      <div class="section-tag">About us</div>
      <h2 class="section-h2">Expertise that produces results</h2>
      <p class="section-desc">More than two decades at the intersection of information security, business processes and regulatory requirements.</p>
    </div>
    <div class="onama-grid">
      <div class="onama-left">
        <div class="onama-portrait">
          <svg width="100" height="100" viewBox="0 0 100 100" fill="none">
            <path d="M50 4 L91 27 L91 73 L50 96 L9 73 L9 27 Z" stroke="#f4a070" stroke-width="2.5" fill="rgba(239,101,63,.06)"/>
            <path d="M50 16 L80 33 L80 67 L50 84 L20 67 L20 33 Z" stroke="#EF653F" stroke-width="1.8" fill="none" opacity=".6"/>
            <path d="M50 26 L65 35 L65 65 L50 74 L35 65 L35 35 Z" stroke="#EF653F" stroke-width="1.2" fill="rgba(239,101,63,.1)"/>
            <circle cx="50" cy="50" r="8" fill="#EF653F" opacity=".9"/>
            <circle cx="50" cy="50" r="4" fill="#c14b28"/>
          </svg>
          <div>
            <div class="onama-name">Daniel Bara, PhD</div>
            <div class="onama-title">Founder and Principal Consultant</div>
          </div>
        </div>
        <ul class="onama-meta-list">
          <li><span>&#9656;</span>PhD - Faculty of Economics, Osijek</li>
          <li><span>&#9656;</span>MBA - Zagreb School of Economics and Management</li>
          <li><span>&#9656;</span>MSc in Transport Engineering</li>
          <li><span>&#9656;</span>PMP - Project Management Professional</li>
          <li><span>&#9656;</span>Lecturer at RIT Croatia since 2017 (IST, Strategic Management, PM)</li>
          <li><span>&#9656;</span>Guest lectures: ZSEM, VERN, Libertas</li>
          <li><span>&#9656;</span>PMI Croatia - active member</li>
          <li><span>&#9656;</span>HAMAG-BICRO evaluator (300+ EU projects)</li>
        </ul>
      </div>
      <div class="onama-right">
        <h2>Over 20 years in <em>information security and GRC</em></h2>
        <p class="onama-lead">Adventure Spirit Consulting grew out of a simple proposition: organisations deserve cybersecurity and risk management expertise fitted to real operations, not to generic templates. We work with clients who know what they want, and we know what they need.<br><br>
        We run projects one at a time, without unnecessary exposure. What shows are the results: information security management systems in operation, business continuity plans that have actually been exercised, data protection processes that hold, and organisations that walk into certification audits with confidence. Our experience spans banking, insurance, energy, healthcare, the food industry and the public sector - everywhere data and operational resilience are a question of survival.<br><br>
        Principal consultant Daniel Bara, PhD, brings more than 20 years of work in information security, a doctorate in business intelligence, an MBA, the PMP certification and experience as an external evaluator on more than 300 EU-funded projects. He has lectured at RIT Croatia since 2017, with guest lectures at ZSEM, VERN and Libertas.</p>
        <div class="onama-expertise">
          <h3>Areas of expertise</h3>
          <div class="expertise-tags">
            <span class="expertise-tag">ISO 27001:2022</span><span class="expertise-tag">ISO 9001:2015</span>
            <span class="expertise-tag">ISO 14001:2015</span><span class="expertise-tag">ISO 22301:2019</span>
            <span class="expertise-tag">GDPR / DPO</span><span class="expertise-tag">NIS2 / CSA</span>
            <span class="expertise-tag">DORA</span><span class="expertise-tag">Vendor Risk</span>
            <span class="expertise-tag">Penetration testing</span><span class="expertise-tag">BIA / BCP / DRP</span>
            <span class="expertise-tag">Business Intelligence</span><span class="expertise-tag">Data Architecture</span>
            <span class="expertise-tag">PL/SQL</span><span class="expertise-tag">PMP</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<div class="section-divider"></div>

<!-- ═══ SERVICES ═══ -->
<section id="services" style="background: var(--dark2)">
  <div class="container">
    <div class="section-header">
      <div class="section-tag">Advisory services</div>
      <h2 class="section-h2">End-to-end risk and compliance management</h2>
      <p class="section-desc">Nine service lines, one evidence base. Where the requirements overlap, the documentation is written once.</p>
    </div>
    <div class="cards-grid">
''' + services + '''
    </div>
  </div>
</section>

<div class="section-divider"></div>

<!-- ═══ SECTORS ═══ -->
<section id="sectors">
  <div class="container">
    <div class="section-header">
      <div class="section-tag">Sectors</div>
      <h2 class="section-h2">Sectors we cover</h2>
      <p class="section-desc">Entity category is determined by sector and size, subject to exceptions. In healthcare and public administration size is not the criterion - the activity is.</p>
    </div>
    <div class="sector-grid">
''' + sectors + '''
    </div>
    <div class="authority-row">
''' + authorities + '''
    </div>
  </div>
</section>

<div class="section-divider"></div>

<!-- ═══ PLATFORM ═══ -->
<section id="platform" class="grc-cta-section">
  <div class="container">
    <div class="grc-cta-inner">
      <div class="grc-cta-left">
        <h2>Your GRC compliance<br><span>running in one platform</span></h2>
        <p>Not advisory alone. We also run our own GRC platform that digitises risk management, compliance and security processes. Your team works in a system we built out of real implementations.</p>
        <ul class="grc-features">
          <li>CSA/NIS2, GDPR, ISO 27001, ISO 9001, ISO 14001, ISO 22301, DORA</li>
          <li>Vendor risk management with automated risk scoring</li>
          <li>AI document analysis and automated benchmarking</li>
          <li>Incident management and regulatory reporting</li>
          <li>BIA wizard, audit log and compliance dashboard</li>
          <li>Multi-tenant architecture for consultants and their clients</li>
        </ul>
        <a href="https://app.adventurespirit.hr" target="_blank" rel="noopener" class="btn-primary">Try the GRC Portal &rarr;</a>
      </div>
      <div class="grc-portal-box">
        <div class="portal-logo-row">
          <svg width="28" height="28" viewBox="0 0 100 100" fill="none">
            <circle cx="50" cy="50" r="44" stroke="#EF653F" stroke-width="1.5" opacity=".3"/>
            <path d="M50 12 L41 46 L50 41 L59 46 Z" fill="#EF653F"/>
            <line x1="44" y1="37" x2="56" y2="37" stroke="#c14b28" stroke-width="3"/>
            <circle cx="50" cy="50" r="5" fill="#EF653F"/>
          </svg>
          <div class="portal-title">Adventure Spirit GRC</div>
        </div>
        <div class="portal-sub">Compliance platform for risk management</div>
        <div class="portal-stats">
          <div class="portal-stat"><div class="portal-stat-num">9+</div><div class="portal-stat-label">Compliance modules</div></div>
          <div class="portal-stat"><div class="portal-stat-num">AI</div><div class="portal-stat-label">Document analysis</div></div>
          <div class="portal-stat"><div class="portal-stat-num">24/7</div><div class="portal-stat-label">Portal availability</div></div>
        </div>
        <a href="https://app.adventurespirit.hr" target="_blank" rel="noopener" class="portal-login-btn"><svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align:-2px;margin-right:7px"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>Sign in to the portal</a>
        <a href="#contact" class="portal-trial-link">No account yet? <span>Ask us for a demo &rarr;</span></a>
      </div>
    </div>
  </div>
</section>

<!-- ═══ PROCESS ═══ -->
<section class="process-section" id="process">
  <div class="container">
    <div class="section-header">
      <div class="section-tag">Methodology</div>
      <h2 class="section-h2">How we work</h2>
      <p class="section-desc">A structured approach that delivers - from the first assessment through to certification and continuous monitoring.</p>
    </div>
    <div class="steps-grid">
''' + steps + '''
    </div>

    <div class="deliver-wrap">
      <div class="deliver-head">What you actually get</div>
      <div class="deliver-grid">
''' + deliverables + '''
      </div>
    </div>
  </div>
</section>

<!-- ═══ CLIENTS ═══ -->
<section id="clients" class="references-section">
  <div class="container">
    <div class="section-header">
      <div class="section-tag">Clients</div>
      <h2 class="section-h2">Organisations that trust us</h2>
    </div>
    <p class="ref-intro">We have worked with organisations across financial services, insurance, energy, healthcare, the food industry, IT and sport - implementing ISMS, BCMS, GDPR, DORA, NIS2 and ISO certifications.</p>
    <div class="ref-categories">
''' + clients + '''
    </div>
    <div class="ref-total">
      <span class="ref-total-num">40+</span>
      <div class="ref-total-label">organisations across banking, insurance, energy, IT, the food and pharmaceutical industries, logistics and sport</div>
    </div>
  </div>
</section>

<div class="section-divider"></div>

<!-- ═══ INSIGHTS ═══ -->
<section id="insights" class="kb-section">
  <div class="container">
    <div class="section-header">
      <div class="section-tag">Knowledge base</div>
      <h2 class="section-h2">What the rules ask for and what proves it</h2>
      <p class="section-desc">Articles on the Croatian Cybersecurity Act, ISO standards and risk management. Every claim carries the article of the law or standard behind it, where one exists.</p>
    </div>
    <div class="kb-grid">
''' + posts_en + '''
    </div>
    <div class="kb-all"><a href="/en/blog/" class="btn-outline">Open the knowledge base</a></div>
  </div>
</section>

<div class="section-divider"></div>

<!-- ═══ FAQ ═══ -->
<section id="faq" style="background: var(--dark2)">
  <div class="container">
    <div class="section-header">
      <div class="section-tag">Frequently asked</div>
      <h2 class="section-h2">What clients ask us most</h2>
      <p class="section-desc">Answers carry the article of the law or standard behind them, where one exists.</p>
    </div>
    <div class="faq-list">
''' + faq + '''
    </div>

    <div class="boundary">
      <h3>We prepare you for the audit and the certification. We do not perform them.</h3>
      <p>The formal cybersecurity audit is carried out by an authorised provider, and ISO certification by an accredited certification body. Adventure Spirit Consulting holds neither authorisation and does not seek them. A body that has built a management system should not also assess it, so that separation protects you: what we tell you is ready is ready for someone who has no interest in it being so.</p>
    </div>
  </div>
</section>

<!-- ═══ CONTACT ═══ -->
<section id="contact" class="contact-section">
  <div class="container">
    <div class="contact-grid">
      <div class="contact-left">
        <h2>Get in touch</h2>
        <p>Need a compliance assessment, an ISO implementation, DORA or NIS2 preparation, or a demo of the GRC platform? Write to us - we reply within 24 hours.</p>
        <div class="contact-item">
          <div class="contact-icon"><svg viewBox="0 0 24 24"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.4 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/></svg></div>
          <div><strong>Phone</strong><a href="tel:+385955041496" style="color:var(--orange);text-decoration:none">+385 95 504 1496</a></div>
        </div>
        <div class="contact-item">
          <div class="contact-icon"><svg viewBox="0 0 24 24"><path d="M4 4h16v16H4z"/><path d="M4 7l8 6 8-6"/></svg></div>
          <div><strong>Email</strong>info@adventurespirit.hr</div>
        </div>
        <div class="contact-item">
          <div class="contact-icon"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15 15 0 0 1 0 20 15 15 0 0 1 0-20z"/></svg></div>
          <div><strong>GRC Portal</strong><a href="https://app.adventurespirit.hr" target="_blank" rel="noopener" style="color:var(--orange);text-decoration:none">app.adventurespirit.hr</a></div>
        </div>
      </div>
      <form class="contact-form" onsubmit="handleContact(event)">
        <div class="form-row">
          <input class="form-input" type="text" placeholder="Full name *" required id="c-name">
          <input class="form-input" type="email" placeholder="Email address *" required id="c-email">
        </div>
        <div class="form-row">
          <input class="form-input" type="text" placeholder="Company / organisation" id="c-company">
          <input class="form-input" type="tel" placeholder="Phone" id="c-phone">
        </div>
        <select class="form-select" id="c-subject">
          <option>CSA / NIS2 compliance</option>
          <option>GDPR compliance</option>
          <option>ISO 27001</option>
          <option>ISO 9001 / 14001 / 22301</option>
          <option>DORA</option>
          <option>Vendor risk management</option>
          <option>Security audit / penetration test</option>
          <option>GRC platform demo</option>
          <option>Other</option>
        </select>
        <textarea class="form-textarea" placeholder="A short description of the project or question" id="c-message"></textarea>
        <div id="c-success" style="display:none;color:#6ec47a;font-size:13px;padding:8px 0">&#10003; Thank you. We will be in touch shortly.</div>
        <div id="c-error" style="display:none;color:#f87171;font-size:13px;padding:8px 0"></div>
        <button type="submit" class="form-submit">Send enquiry &rarr;</button>
        <p class="legal-note">The legally binding versions of our terms of use and privacy policy are published in Croatian.</p>
      </form>
    </div>
  </div>
</section>
''' + EN_FOOTER + '''

<script>
function toggleNav() { document.getElementById('nav-links').classList.toggle('open'); }
document.querySelectorAll('#nav-links a').forEach(function (a) {
  a.addEventListener('click', function () { document.getElementById('nav-links').classList.remove('open'); });
});
window.addEventListener('scroll', function () {
  document.getElementById('navbar').style.borderBottomColor =
    window.scrollY > 40 ? 'rgba(239,101,63,.15)' : 'rgba(255,255,255,.06)';
});
document.querySelectorAll('a[href^="#"]').forEach(function (a) {
  a.addEventListener('click', function (e) {
    var t = document.querySelector(a.getAttribute('href'));
    if (t) { e.preventDefault(); window.scrollTo({ top: t.offsetTop - 104, behavior: 'smooth' }); }
  });
});
function toggleFaq(btn) {
  var item = btn.parentElement, wasOpen = item.classList.contains('open');
  item.parentElement.querySelectorAll('.faq-item.open').forEach(function (el) {
    el.classList.remove('open');
    el.querySelector('.faq-q').setAttribute('aria-expanded', 'false');
  });
  if (!wasOpen) { item.classList.add('open'); btn.setAttribute('aria-expanded', 'true'); }
}
(function () {
  var chart = document.querySelector('.mchart');
  if (!chart || !('IntersectionObserver' in window)) return;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var cells = Array.prototype.slice.call(chart.querySelectorAll('.mcell.on'));
  cells.forEach(function (c) { c.classList.remove('on'); });
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (!en.isIntersecting) return;
      cells.forEach(function (c, i) { setTimeout(function () { c.classList.add('on'); }, 30 * i); });
      io.disconnect();
    });
  }, { threshold: .3 });
  io.observe(chart);
})();
async function handleContact(e) {
  e.preventDefault();
  var btn = e.target.querySelector('.form-submit');
  var ok = document.getElementById('c-success'), err = document.getElementById('c-error');
  ok.style.display = 'none'; err.style.display = 'none';
  btn.disabled = true; btn.textContent = 'Sending...';
  var phone = document.getElementById('c-phone').value;
  var body = {
    name: document.getElementById('c-name').value,
    email: document.getElementById('c-email').value,
    phone: phone || '-',
    message: '[EN][' + document.getElementById('c-subject').value + '] ' +
             document.getElementById('c-company').value +
             (phone ? ' - Tel: ' + phone : '') + '\\n\\n' +
             document.getElementById('c-message').value
  };
  try {
    var res = await fetch('https://formspree.io/f/mojpkknr', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify(body)
    });
    if (res.ok) { ok.style.display = 'block'; e.target.reset(); } else { throw new Error(); }
  } catch (x) {
    err.textContent = 'Could not send. Please contact us directly: info@adventurespirit.hr';
    err.style.display = 'block';
  } finally { btn.disabled = false; btn.textContent = 'Send enquiry \\u2192'; }
}
</script>'''

    ld = [{
      "@context": "https://schema.org", "@type": "ProfessionalService",
      "@id": SITE + "/en/#organization",
      "name": "Adventure Spirit Consulting", "legalName": "Adventure Spirit d.o.o.",
      "alternateName": ["Adventure Spirit d.o.o.", "Adventure Spirit"],
      "url": SITE + "/en/", "email": "info@adventurespirit.hr",
      "telephone": "+385 95 504 1496",
      "description": "Advisory in cyber security, GRC and compliance - Croatian Cybersecurity Act (NIS2), GDPR, DORA, ISO 27001, ISO 9001, ISO 14001 and ISO 22301.",
      "address": {"@type": "PostalAddress", "streetAddress": "Antuna Šoljana 22",
                  "postalCode": "10000", "addressLocality": "Zagreb", "addressCountry": "HR"},
      "vatID": "HR72169598754", "taxID": "72169598754",
      "identifier": [{"@type": "PropertyValue", "propertyID": "OIB", "value": "72169598754"},
                     {"@type": "PropertyValue", "propertyID": "MBS", "value": "4845552"}],
      "areaServed": {"@type": "Country", "name": "Croatia"},
      "knowsLanguage": ["hr", "en"],
      "founder": {"@type": "Person", "name": "Daniel Bara", "honorificSuffix": "PhD",
                  "jobTitle": "Founder and Principal Consultant"},
      "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Advisory services",
        "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": n}}
                            for _, n, _, _ in EN_SERVICES]},
    }, {
      "@context": "https://schema.org", "@type": "FAQPage",
      "mainEntity": [{"@type": "Question", "name": strip_html(q),
                      "acceptedAnswer": {"@type": "Answer", "text": strip_html(a)}}
                     for q, a, _ in EN_FAQ],
    }]

    head = ('<style>' + SHARED_CSS + LANG_CSS + '</style>\n'
            '<link rel="alternate" hreflang="hr" href="%s/">\n'
            '<link rel="alternate" hreflang="en" href="%s/en/">\n'
            '<link rel="alternate" hreflang="x-default" href="%s/">' % (SITE, SITE, SITE))

    out = page("Adventure Spirit Consulting - NIS2, GDPR, DORA and ISO compliance in Croatia",
               "Cyber security and GRC advisory in Croatia. Croatian Cybersecurity Act (NIS2), GDPR, DORA, ISO 27001, ISO 22301. We know what the regulator asks for and what proves it.",
               body, SITE + "/en/", extra_head=head, ld=ld)
    out = out.replace('<link rel="stylesheet" href="/blog/assets/blog.css">\n', '')
    out = out.replace('<link rel="alternate" type="application/rss+xml" title="Baza znanja - Adventure Spirit Consulting" href="/blog/feed.xml">',
                      '<link rel="alternate" type="application/rss+xml" title="Insights - Adventure Spirit Consulting" href="/en/blog/feed.xml">')
    out = out.replace('<html lang="hr">', '<html lang="en">')
    os.makedirs(os.path.join(ROOT, "en"), exist_ok=True)
    io.open(os.path.join(ROOT, "en", "index.html"), "w", encoding="utf-8").write(out)

# ══════════════════════════════════════════════════════════════════
# Generiranje - zajednicko za oba jezika
# ══════════════════════════════════════════════════════════════════
HR_MJ = ["siječnja","veljače","ožujka","travnja","svibnja","lipnja",
         "srpnja","kolovoza","rujna","listopada","studenoga","prosinca"]
EN_MJ = ["January","February","March","April","May","June",
         "July","August","September","October","November","December"]
RFC_MJ = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

def fmt_date(iso, lang):
    y, m, d = iso.split("-")
    if lang == "hr":
        return "%d. %s %s." % (int(d), HR_MJ[int(m)-1], y)
    return "%d %s %s" % (int(d), EN_MJ[int(m)-1], y)

def rfc_date(iso):
    y, m, d = iso.split("-")
    return "Tue, %s %s %s 09:00:00 +0200" % (d, RFC_MJ[int(m)-1], y)


def card(a, lang, featured=False):
    t = L[lang]
    return '''<a class="post-card%s" href="%s%s/" data-cat="%s">
      <div class="post-cat">%s</div>
      <div class="post-title">%s</div>
      <div class="post-lead">%s</div>
      <div class="post-meta"><span>%s</span><span class="read">%d %s</span></div>
    </a>''' % (" featured" if featured else "", t["blog"], a["slug"], a["catkey"],
               html.escape(a["cat"]), html.escape(a["title"]), html.escape(a["lead"]),
               fmt_date(a["date"], lang), a["read"], t["read"])


def cta_block(lang):
    t = L[lang]
    return '''<div class="art-cta">
  <h3>%s</h3>
  <p>%s</p>
  <div class="cta-btns">
    <a href="%s#%s" class="btn-primary">%s</a>
    <a href="%s" class="btn-outline">%s</a>
  </div>
</div>''' % (t["cta_h"], t["cta_p"], t["base"] or "/", "kontakt" if lang == "hr" else "contact",
              t["cta_b1"], t["cta_b2_url"], t["cta_b2"])


def build_blog(lang, articles, table_fn):
    t = L[lang]
    articles = sorted(articles, key=lambda a: a["date"], reverse=True)
    FOOT = footer(lang, articles)
    out_dir = os.path.join(ROOT, "en", "blog") if lang == "en" else os.path.join(ROOT, "blog")
    os.makedirs(out_dir, exist_ok=True)

    # ── Clanci ────────────────────────────────────────────────────
    for a in articles:
        body_html = a["body"].replace("__TABLICA__", table_fn())
        srcs = "\n".join('    <li>%s</li>'
          % (('<a href="%s" target="_blank" rel="noopener">%s</a>' % (u, html.escape(s)))
             if u else html.escape(s)) for s, u in a["sources"])
        rel = [x for x in articles if x["slug"] != a["slug"]][:3]
        url = SITE + t["blog"] + a["slug"] + "/"

        body = header(lang) + '''
<main>
  <div class="container narrow">
    <div class="crumbs">
      <a href="%s">%s</a><span>&rsaquo;</span><a href="%s">%s</a><span>&rsaquo;</span>%s
    </div>
    <header class="art-head">
      <div class="eyebrow">%s</div>
      <h1>%s</h1>
      <p class="art-lead">%s</p>
      <div class="art-meta">
        <span><strong>%s</strong></span><span>%s</span><span>%d %s</span>
      </div>
    </header>
    <article>
%s
      <div class="sources">
        <h4>%s</h4>
        <ul>
%s
        </ul>
      </div>
      %s
    </article>
    <div class="related">
      <h3>%s</h3>
      <div class="related-grid">
%s
      </div>
    </div>
  </div>
</main>
''' % (t["base"] or "/", t["home"], t["blog"], t["kb_title"], html.escape(a["cat"]),
       html.escape(a["cat"]), html.escape(a["title"]), html.escape(a["lead"]),
       AUTHOR_L[lang], fmt_date(a["date"], lang), a["read"], t["read"],
       body_html, t["sources"], srcs, cta_block(lang), t["related"],
       "\n".join(card(x, lang) for x in rel)) + FOOT

        ld = [{
          "@context": "https://schema.org", "@type": "BlogPosting",
          "headline": a["title"], "description": a["desc"],
          "datePublished": a["date"], "dateModified": a["date"],
          "inLanguage": "hr-HR" if lang == "hr" else "en-GB",
          "articleSection": a["cat"],
          "author": {"@type": "Person", "name": "Daniel Bara",
                     "honorificSuffix": "dr. sc." if lang == "hr" else "PhD",
                     "url": SITE + (t["base"] or "") + "/#" + ("onama" if lang == "hr" else "about")},
          "publisher": {"@type": "Organization", "name": "Adventure Spirit Consulting",
                        "legalName": "Adventure Spirit d.o.o.", "url": SITE + "/"},
          "mainEntityOfPage": {"@type": "WebPage", "@id": url}, "url": url,
        }, {
          "@context": "https://schema.org", "@type": "BreadcrumbList",
          "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": t["home"], "item": SITE + (t["base"] or "/")},
            {"@type": "ListItem", "position": 2, "name": t["kb_title"], "item": SITE + t["blog"]},
            {"@type": "ListItem", "position": 3, "name": a["title"], "item": url}]}]

        d = os.path.join(out_dir, a["slug"])
        os.makedirs(d, exist_ok=True)
        io.open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(
          page(a["title"] + " | Adventure Spirit Consulting", a["desc"], body, url,
               lang=lang, og_type="article", ld=ld))

    # ── Popisna stranica ──────────────────────────────────────────
    cats = []
    for a in articles:
        if (a["catkey"], a["cat"]) not in cats:
            cats.append((a["catkey"], a["cat"]))
    catbtns = ('<button class="cat-btn active" data-f="all">%s</button>\n      ' % t["all_topics"]) + \
              "\n      ".join('<button class="cat-btn" data-f="%s">%s</button>' % (k, html.escape(v))
                              for k, v in cats)
    articles = sorted(articles, key=lambda a: a["date"], reverse=True)
    feat = [a for a in articles if a.get("featured")]
    rest = [a for a in articles if not a.get("featured")]
    cards = "\n".join([card(a, lang, True) for a in feat] + [card(a, lang) for a in rest])

    listing = header(lang) + '''
<main>
  <section class="kb-hero">
    <div class="container">
      <div class="eyebrow">%s</div>
      <h1>%s</h1>
      <p>%s</p>
      <div class="cat-bar">
      %s
      </div>
    </div>
  </section>
  <div class="container">
    <div class="post-grid" id="posts">
%s
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
''' % (t["kb_title"], t["kb_h1"], t["kb_intro"], catbtns, cards) + FOOT

    ld_list = [{
      "@context": "https://schema.org", "@type": "Blog",
      "@id": SITE + t["blog"] + "#blog", "name": t["feed_title"],
      "description": t["kb_desc"], "url": SITE + t["blog"],
      "inLanguage": "hr-HR" if lang == "hr" else "en-GB",
      "publisher": {"@type": "Organization", "name": "Adventure Spirit Consulting",
                    "legalName": "Adventure Spirit d.o.o.", "url": SITE + "/"},
      "blogPost": [{"@type": "BlogPosting", "headline": a["title"],
                    "url": SITE + t["blog"] + a["slug"] + "/",
                    "datePublished": a["date"], "description": a["desc"]} for a in articles]}]

    io.open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8").write(
      page(t["kb_title"] + " | Adventure Spirit Consulting", t["kb_desc"], listing,
           SITE + t["blog"], lang=lang, extra_head=hreflang(SITE + "/blog/", SITE + "/en/blog/"),
           ld=ld_list))

    # ── RSS ───────────────────────────────────────────────────────
    items = "\n".join('''  <item>
    <title>%s</title>
    <link>%s%s%s/</link>
    <guid isPermaLink="true">%s%s%s/</guid>
    <category>%s</category>
    <pubDate>%s</pubDate>
    <description>%s</description>
  </item>''' % (html.escape(a["title"]), SITE, t["blog"], a["slug"], SITE, t["blog"], a["slug"],
                html.escape(a["cat"]), rfc_date(a["date"]), html.escape(a["desc"]))
      for a in articles)
    io.open(os.path.join(out_dir, "feed.xml"), "w", encoding="utf-8").write(
'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
  <title>%s</title>
  <link>%s%s</link>
  <atom:link href="%s%sfeed.xml" rel="self" type="application/rss+xml"/>
  <description>%s</description>
  <language>%s</language>
%s
</channel>
</rss>
''' % (html.escape(t["feed_title"]), SITE, t["blog"], SITE, t["blog"],
       html.escape(t["kb_desc"]), lang, items))

    # ── 404 ───────────────────────────────────────────────────────
    nf_nav = "\n".join('        <a href="%s">%s</a>' % (u, n) for u, n in t["nf_nav"])
    nf_body = header(lang, active_blog=False) + '''
<main>
  <section class="kb-hero">
    <div class="container">
      <div class="nf-code">404</div>
      <h1>%s</h1>
      <p>%s</p>
      <div class="nf-links">
        <a href="%s" class="btn-primary">%s</a>
        <a href="%s#%s" class="btn-outline">%s</a>
      </div>
      <div class="nf-nav">
%s
        <a href="https://app.adventurespirit.hr" target="_blank" rel="noopener">GRC Portal</a>
      </div>
    </div>
  </section>
  <div class="container">
    <div style="padding:44px 0 12px"><div class="eyebrow">%s</div></div>
    <div class="post-grid" style="padding-top:0">
%s
    </div>
  </div>
</main>
''' % (t["nf_h1"], t["nf_p"], t["base"] or "/", t["nf_home"], t["base"] or "/",
       "kontakt" if lang == "hr" else "contact", t["nf_contact"], nf_nav, t["nf_from_kb"],
       "\n".join(card(a, lang) for a in articles[:3])) + FOOT

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
    nf_dir = os.path.join(ROOT, "en") if lang == "en" else ROOT
    os.makedirs(nf_dir, exist_ok=True)
    io.open(os.path.join(nf_dir, "404.html"), "w", encoding="utf-8").write(
      page(t["nf_title"] + " | Adventure Spirit Consulting", t["nf_desc"], nf_body,
           SITE + (t["base"] or "") + "/404.html", lang=lang,
           extra_head=NF_CSS + '\n<meta name="robots" content="noindex, follow">'))


AUTHOR_L = {"hr": "Daniel Bara, dr. sc.", "en": "Daniel Bara, PhD"}

build_blog("hr", ARTICLES, mjere_tablica)
build_blog("en", ARTICLES_EN, mjere_tablica_en)
en_index()

# ══════════════════════════════════════════════════════════════════
# hreflang i preklopnik jezika na hrvatskoj naslovnici
# ══════════════════════════════════════════════════════════════════
_idx = os.path.join(ROOT, "index.html")
_s = io.open(_idx, encoding="utf-8").read()

if 'hreflang="en"' not in _s:
    _s = _s.replace('  <link rel="canonical" href="https://adventurespirit.hr/">',
      '  <link rel="canonical" href="https://adventurespirit.hr/">\n  ' +
      hreflang(SITE + "/", SITE + "/en/").replace("\n", "\n  "), 1)

if 'lang-switch' not in _s:
    _s = _s.replace('    <li><a href="#kontakt">Kontakt</a></li>',
      '    <li><a href="#kontakt">Kontakt</a></li>\n'
      '    <li class="lang-switch"><span>HR</span><a href="/en/" hreflang="en">EN</a></li>', 1)
    _s = _s.replace('    /* ── Footer pravni podaci ───────────────────────────────── */',
      LANG_CSS + '\n    /* ── Footer pravni podaci ───────────────────────────────── */', 1)

if '>English version<' not in _s:
    _s = _s.replace('        <a href="#kontakt">Kontakt</a>\n      </div>',
      '        <a href="#kontakt">Kontakt</a>\n        <a href="/en/">English version</a>\n      </div>', 1)

io.open(_idx, "w", encoding="utf-8").write(_s)

# ══════════════════════════════════════════════════════════════════
# sitemap.xml + robots.txt
# ══════════════════════════════════════════════════════════════════
urls = [(SITE + "/", "1.0", "weekly"), (SITE + "/en/", "0.9", "weekly"),
        (SITE + "/blog/", "0.9", "weekly"), (SITE + "/en/blog/", "0.8", "weekly")]
urls += [("%s/blog/%s/" % (SITE, a["slug"]), "0.8", "monthly") for a in ARTICLES]
urls += [("%s/en/blog/%s/" % (SITE, a["slug"]), "0.7", "monthly") for a in ARTICLES_EN]
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

print("Generirano: HR %d + EN %d clanaka, 2 popisne stranice, 2 feeda, 2x404, EN naslovnica, sitemap, robots"
      % (len(ARTICLES), len(ARTICLES_EN)))
