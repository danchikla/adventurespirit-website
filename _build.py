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
        ("/blog/","Baza znanja"),("/alati/","Alati"),("/#reference","Reference"),
        ("/#faq","FAQ"),("/#kontakt","Kontakt")],
   legal_line="Adventure Spirit d.o.o. &middot; Zagreb",
   brand_line="Tržišni naziv: Adventure Spirit Consulting",
   addr="Antuna Šoljana 22, 10000 Zagreb, Hrvatska", oib="OIB / PDV ID: 72169598754 &middot; MBS: 4845552<br>Trgovački sud u Zagrebu",
   tagline="Kibernetička sigurnost, GRC compliance i upravljanje rizicima - preko 20 godina iskustva u službi vašeg poslovanja.",
   f_kb="Baza znanja", f_all="Svi članci", f_svc="Usluge", f_co="Tvrtka",
   f_links=[("/#sigurnost","ZKS / NIS2"),("/#sigurnost","GDPR"),("/#sigurnost","ISO 27001"),
            ("/#sigurnost","DORA"),("/#sektori","Sektori")],
   f_co_links=[("/#onama","O konzultantu"),("/alati/","Alati"),("/#faq","Česta pitanja"),
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
           ("/blog/","Baza znanja"),("/alati/","Alati"),("/#faq","Česta pitanja")],
   cta_h="Ne znate gdje stojite?",
   cta_p="Pola sata razgovora i ništa vas ne obvezuje. Kad završimo, znate što trebate napraviti i kojim redom.",
   cta_b1="Dogovorite razgovor", cta_b2="Pogledajte usluge", cta_b2_url="/#sigurnost",
   feed_title="Baza znanja - Adventure Spirit Consulting",
 ),
 "en": dict(
   lang="en", base="/en", blog="/en/blog/", other="/", other_label="HR", self_label="EN",
   nav=[("/en/#about","About"),("/en/#services","Services"),("/en/#sectors","Sectors"),
        ("/en/blog/","Insights"),("/en/tools/","Tools"),("/en/#clients","Clients"),
        ("/en/#faq","FAQ"),("/en/#contact","Contact")],
   legal_line="Adventure Spirit d.o.o. &middot; Zagreb, Croatia",
   brand_line="Trading as: Adventure Spirit Consulting",
   addr="Antuna Šoljana 22, 10000 Zagreb, Croatia", oib="OIB / VAT ID: 72169598754 &middot; Reg. no. (MBS): 4845552<br>Commercial Court in Zagreb",
   tagline="Cyber security, GRC compliance and risk management - over 20 years of experience in the service of your business.",
   f_kb="Insights", f_all="All articles", f_svc="Services", f_co="Company",
   f_links=[("/en/#services","CSA / NIS2"),("/en/#services","GDPR"),("/en/#services","ISO 27001"),
            ("/en/#services","DORA"),("/en/#sectors","Sectors")],
   f_co_links=[("/en/#about","About the consultant"),("/en/tools/","Tools"),("/en/#faq","FAQ"),
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
           ("/en/blog/","Knowledge base"),("/en/tools/","Tools"),("/en/#faq","FAQ")],
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
      <tr><td class="num">30 dana</td><td>Završno izvješće</td><td>Detaljan opis, vrsta prijetnje i uzrok, primijenjene i planirane mjere, prekogranični učinak. Rok teče od dostave obavijesti o incidentu, ne od saznanja.</td></tr>
    </tbody>
  </table>
</div>
<p>Rokovi se računaju <strong>od saznanja o incidentu</strong>, ne od njegovog nastanka i ne od trenutka kad je istraga završena. To je razlika koja odlučuje jeste li u roku.</p>
<p>Uz ova tri postoje i <strong>privremeno izvješće</strong>, koje nadležni CSIRT može zatražiti u roku od 48 sati do 7 dana, te <strong>izvješće o napretku</strong>, koje se dostavlja svakih 30 dana ako incident još traje. Detaljan pregled svih pet vrsta obavijesti i prijave preko platforme PiXi <a href="/blog/znacajan-incident-pet-obavijesti-pixi/">u zasebnom tekstu</a>.</p>

<div class="callout">
  <div class="c-label">Izračunajte svoje rokove</div>
  <p>Unesite trenutak saznanja u <a href="/alati/rokovi-prijave-incidenta/">kalkulator rokova</a> pa dobijete svih pet datuma odjednom, uključujući usporednu prijavu AZOP-u. Radi u pregledniku, ne traži registraciju.</p>
</div>

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
# Dodatni hrvatski clanci
# ══════════════════════════════════════════════════════════════════
ARTICLES.append(dict(
 slug="iso-27002-2022-atributi-kontrola", cat="ISO norme", catkey="iso",
 date="2026-05-05", read=6,
 title="ISO 27002:2022: 93 kontrole i pet atributa koje većina preskoči",
 lead="Revizija iz 2022. srezala je 114 kontrola na 93 i posložila ih u četiri teme umjesto četrnaest. Veća promjena od preslagivanja su atributi - i oni su razlog zašto se stara Izjava o primjenjivosti ne može samo prenumerirati.",
 desc="Što se promijenilo u ISO/IEC 27002:2022 - četiri teme umjesto četrnaest poglavlja, 93 kontrole i pet atributa. Kako prijeći sa stare Izjave o primjenjivosti bez gubitka dokazne baze.",
 body='''
<p>Prelazak na ISO/IEC 27002:2022 najčešće se izvede kao vježba prenumeriranja: uzme se stara Izjava o primjenjivosti, kontrole se preslikaju u novu numeraciju i posao je gotov. Formalno prolazi. Suštinski se propušta jedini dio revizije koji stvarno mijenja način rada.</p>

<h2>Što se promijenilo u brojkama</h2>
<div class="tbl-wrap">
  <table>
    <thead><tr><th></th><th>ISO 27002:2013</th><th>ISO 27002:2022</th></tr></thead>
    <tbody>
      <tr><td><strong>Kontrola</strong></td><td>114</td><td>93</td></tr>
      <tr><td><strong>Struktura</strong></td><td>14 poglavlja</td><td>4 teme</td></tr>
      <tr><td><strong>Nove kontrole</strong></td><td>-</td><td>11</td></tr>
      <tr><td><strong>Spojene</strong></td><td>-</td><td>57 u 24</td></tr>
      <tr><td><strong>Atributi</strong></td><td>ne postoje</td><td>5 po kontroli</td></tr>
    </tbody>
  </table>
</div>
<p>Četiri teme su organizacijska, ljudska, fizička i tehnološka. Smanjenje broja kontrola nije smanjenje opsega - većina je nastala spajanjem kontrola koje su se u praksi ionako provodile zajedno.</p>

<h2>Jedanaest novih kontrola</h2>
<p>Ovo je popis koji vrijedi pogledati prije nego što se zaključi da je sve pokriveno:</p>
<ul>
  <li><strong>Obavještajni podaci o prijetnjama</strong> - prikupljanje i korištenje informacija o prijetnjama relevantnima za vas.</li>
  <li><strong>Informacijska sigurnost pri korištenju usluga u oblaku</strong> - od nabave do izlaza iz usluge.</li>
  <li><strong>Spremnost IKT-a za kontinuitet poslovanja</strong> - poveznica prema ISO 22301.</li>
  <li><strong>Praćenje fizičke sigurnosti</strong> - nadzor prostora, ne samo kontrola ulaska.</li>
  <li><strong>Upravljanje konfiguracijom</strong> - sigurne osnovne konfiguracije i praćenje odstupanja.</li>
  <li><strong>Brisanje informacija</strong> - i kod vas i kod obrađivača.</li>
  <li><strong>Maskiranje podataka</strong> - posebno u testnim okruženjima.</li>
  <li><strong>Sprječavanje curenja podataka</strong> - DLP kao kontrola, ne kao proizvod.</li>
  <li><strong>Aktivnosti praćenja</strong> - nadzor mreža, sustava i aplikacija radi otkrivanja anomalija.</li>
  <li><strong>Filtriranje weba</strong> - kontrola pristupa vanjskim stranicama.</li>
  <li><strong>Sigurno kodiranje</strong> - pravila koja vrijede i za nabavljeni softver.</li>
</ul>
<p>Kod većine organizacija barem četiri od ovih jedanaest postoje tehnički, ali nemaju dokument koji ih opisuje ni zapis koji ih dokazuje. To je razlika između kontrole koja radi i kontrole koja prolazi audit.</p>

<h2>Atributi su prava novost</h2>
<p>Svaka kontrola u novoj normi nosi pet atributa: vrstu kontrole (preventivna, detektivna, korektivna), svojstva informacijske sigurnosti (povjerljivost, cjelovitost, dostupnost), koncepte kibernetičke sigurnosti (identificiraj, zaštiti, otkrij, odgovori, oporavi), operativne sposobnosti i sigurnosne domene.</p>
<div class="callout">
  <div class="c-label">Zašto je to korisno</div>
  <p>Atributi vam omogućuju da isti skup kontrola presložite prema pitanju koje postavljate. Uprava pita "koliko smo sposobni otkriti napad?" - filtrirate po konceptu <em>otkrij</em>. Regulator traži dokaze o dostupnosti - filtrirate po tom svojstvu. Bez atributa svako takvo pitanje znači ručno prolaženje kroz cijeli popis.</p>
</div>
<p>Atributi su ujedno najbrži put do mapiranja prema drugim okvirima. Koncepti kibernetičke sigurnosti izravno odgovaraju funkcijama NIST-ovog okvira, pa organizacija koja radi i prema ZKS-u i prema NIST-u ne mora održavati dvije nepovezane tablice.</p>

<h2>Kako prijeći bez gubitka dokazne baze</h2>
<ol>
  <li><strong>Mapirajte staro u novo, ne obrnuto.</strong> Krenite od svojih 114 kontrola i svakoj pronađite mjesto u novih 93. Ono što nema para najčešće je spojeno, ne ukinuto.</li>
  <li><strong>Zadržite tragove.</strong> U Izjavi o primjenjivosti zadržite stupac sa starom oznakom barem jedan ciklus. Auditori i interni ljudi još godinu dana razmišljaju u staroj numeraciji.</li>
  <li><strong>Obradite jedanaest novih posebno.</strong> To je jedini dio gdje stvarno nastaje novi posao.</li>
  <li><strong>Popunite atribute.</strong> Ne zato što ih norma traži kao obvezu - nego zato što je to jedini trenutak kad ćete ih ionako prolaziti kontrolu po kontrolu.</li>
  <li><strong>Provjerite poveznice prema drugim obvezama.</strong> Nove kontrole o oblaku, praćenju i kontinuitetu izravno hrane mjere iz Uredbe o kibernetičkoj sigurnosti.</li>
</ol>

<div class="note">
  <p>ISO/IEC 27001:2022 je norma prema kojoj se certificirate, a 27002 je zbirka smjernica za provedbu kontrola iz Priloga A. Certifikat se ne dobiva prema 27002, ali se dokazi pišu uz njezinu pomoć.</p>
</div>
''',
 sources=[('HRN EN ISO/IEC 27001:2022, Prilog A', None),
          ('HRN EN ISO/IEC 27002:2022 - Kontrole informacijske sigurnosti', None),
          ('ISO/IEC 27001:2022/Amd 1:2024 - climate action changes', None)]))

ARTICLES.append(dict(
 slug="bia-koja-daje-upotrebljiv-rto", cat="Kontinuitet poslovanja", catkey="bcm",
 date="2026-05-26", read=7,
 title="BIA koja daje upotrebljiv RTO, a ne broj koji svi ignoriraju",
 lead="Analiza poslovnog utjecaja najčešće završi kao tablica u kojoj svaki proces ima RTO od četiri sata. Ako je sve kritično, ništa nije - a plan oporavka koji iz toga nastane ne izdrži prvi pravi ispad.",
 desc="Kako provesti analizu poslovnog utjecaja prema ISO 22301 tako da RTO i RPO budu upotrebljivi: tko daje podatke, kako se izbjegava da sve bude kritično, i kako se BIA povezuje s mjerom 12 Uredbe o kibernetičkoj sigurnosti.",
 body='''
<p>Analiza poslovnog utjecaja je temelj cijelog sustava upravljanja kontinuitetom. Ako je pogrešna, pogrešno je sve što stoji na njoj: planovi oporavka, ulaganja u redundanciju, ugovori s dobavljačima i prioriteti tijekom stvarne krize.</p>
<p>A pogrešna je češće nego što se misli, i to gotovo uvijek na isti način.</p>

<h2>Simptom: svi procesi su kritični</h2>
<p>Kad se voditelje odjela pita koliko dugo njihov proces smije stajati, odgovor je predvidljiv. Nitko ne kaže "moj proces može čekati tri dana". Rezultat je tablica u kojoj dvadeset od dvadeset dva procesa ima RTO od četiri sata, a organizacija koja to pokuša ostvariti mora udvostručiti infrastrukturu.</p>
<div class="callout">
  <div class="c-label">Zašto se to događa</div>
  <p>Pitanje "koliko dugo proces smije stajati" je pitanje o osjećaju važnosti. Pitanje "koliki je gubitak nakon 4, 24 i 72 sata, izražen u novcu, ugovornoj kazni, regulatornom riziku i broju pogođenih korisnika" je pitanje o posljedici. Prvo daje jednake odgovore, drugo ih razlikuje.</p>
</div>

<h2>Kako postaviti BIA da razlikuje</h2>
<p>Tri promjene u pristupu daju upotrebljiv rezultat:</p>
<h3>1. Mjerite utjecaj kroz vrijeme, ne u jednoj točki</h3>
<p>Za svaki proces procijenite posljedicu u nekoliko vremenskih odsječaka - primjerice nakon 4 sata, 24 sata, 3 dana i 7 dana. Krivulja koja iz toga nastane pokazuje gdje je stvarni prag boli. Većina procesa ima ravnu krivulju do određene točke pa nagli skok; RTO se postavlja prije tog skoka, ne na proizvoljne četiri sata.</p>
<h3>2. Koristite više kategorija utjecaja</h3>
<p>Financijski gubitak, ugovorne obveze, regulatorne posljedice, sigurnost ljudi i ugled. Proces može biti financijski nevažan, a regulatorno kritičan - prijava incidenta je upravo takav slučaj.</p>
<h3>3. Neka ukupni RTO bude ograničen resurs</h3>
<p>Ako unaprijed znate da možete financirati oporavak pet procesa u prva četiri sata, onda voditelji ne rangiraju svaki svoj proces zasebno nego zajedno raspoređuju ograničeni kapacitet. Razgovor se odmah promijeni.</p>

<h2>RPO se određuje drugdje</h2>
<p>Česta zamjena teza: RTO i RPO postavlja ista osoba u istom retku tablice. RTO je poslovna odluka o tome koliko dugo proces smije stajati. RPO je odluka o tome koliko podataka smijete izgubiti, i ona ovisi o tome koliko se često podaci mijenjaju i može li se gubitak nadoknaditi ručno.</p>
<p>Proces koji jednom dnevno obrađuje šaržu podataka može imati RTO od dva sata i RPO od 24 sata bez ikakve nedosljednosti. Proces koji prima transakcije u realnom vremenu ne može.</p>

<h2>Što BIA mora proizvesti da bi bila upotrebljiva</h2>
<ul>
  <li><strong>Popis procesa s vlasnicima</strong> - osobama, ne odjelima.</li>
  <li><strong>Ovisnosti.</strong> Aplikacije, ljudi, prostori, dobavljači i drugi procesi. Proces s RTO-om od 4 sata koji ovisi o dobavljaču s ugovornim SLA-om od 48 sati nema RTO od 4 sata.</li>
  <li><strong>Krivulju utjecaja</strong> po kategorijama i vremenskim odsječcima.</li>
  <li><strong>RTO i RPO s obrazloženjem.</strong> Broj bez obrazloženja se ne može ni obraniti ni osporiti.</li>
  <li><strong>Minimalnu razinu usluge.</strong> Rijetko se oporavlja na sto posto - definirajte što je dovoljno za nastavak rada.</li>
  <li><strong>Razliku između postojeće i tražene sposobnosti.</strong> To je ulaz u proračun, i najvrjedniji izlaz cijele vježbe.</li>
</ul>

<h2>Poveznica prema Uredbi o kibernetičkoj sigurnosti</h2>
<p>Mjera 12 iz Priloga II. Uredbe traži kontinuitet poslovanja i upravljanje kibernetičkim krizama, s osam podmjera. BIA napravljena prema ISO 22301 pokriva njezin analitički dio gotovo u cijelosti, ali dvije stvari treba dodati:</p>
<ol>
  <li><strong>Kibernetički scenariji.</strong> Klasična BIA računa s ispadom sustava. Ransomware nije ispad - sustavi rade, ali podaci su nedostupni i sigurnosne kopije su možda zahvaćene. RPO se u tom scenariju ponaša drukčije.</li>
  <li><strong>Veza prema upravljanju incidentima.</strong> Plan kontinuiteta i plan odgovora na incident moraju dijeliti kriterij aktivacije, inače će se u krizi aktivirati jedan bez drugoga.</li>
</ol>

<div class="note">
  <p>Plan koji nije isproban dokumentira namjeru, ne sposobnost. Vježba na stolu u trajanju od dva sata, sa scenarijem i stvarnim mjerenjem vremena, otkriva više nego još jedan krug uređivanja dokumenta - i ujedno proizvodi zapis koji mjera 12 traži.</p>
</div>
''',
 sources=[('HRN EN ISO 22301:2019 - Sustavi upravljanja kontinuitetom poslovanja', None),
          ('ISO/TS 22317 - Smjernice za analizu poslovnog utjecaja', None),
          ('Uredba o kibernetičkoj sigurnosti, NN 135/2024, Prilog II., mjera 12', 'https://narodne-novine.nn.hr/clanci/sluzbeni/2024_11_135_2217.html')]))

ARTICLES.append(dict(
 slug="dora-registar-informacija", cat="DORA", catkey="dora",
 date="2026-06-16", read=7,
 title="DORA registar informacija: zašto pada na podacima, a ne na propisu",
 lead="Registar informacija o ugovorima s pružateljima IKT usluga izgleda kao administrativna vježba dok se ne pokuša popuniti. Tada se otkrije da tri odjela imaju tri različita popisa dobavljača, i da nijedan nije potpun.",
 desc="Što DORA traži u registru informacija o ugovorima s pružateljima IKT usluga, zašto se popunjavanje najčešće zaglavi na kvaliteti podataka i kako povezati registar s postojećim registrom imovine i rizika.",
 body='''
<p>Uredba (EU) 2022/2554 traži od financijskih subjekata da vode i održavaju <strong>registar informacija</strong> o svim ugovornim aranžmanima s pružateljima IKT usluga, te da ga na zahtjev dostave nadležnom tijelu. Zvuči kao popis dobavljača. Nije.</p>

<h2>Što registar zapravo traži</h2>
<p>Registar se vodi na nekoliko razina i povezuje podatke koji u većini organizacija žive u odvojenim sustavima:</p>
<ul>
  <li><strong>Subjekt</strong> - tko je ugovorna strana i gdje se nalazi u grupi.</li>
  <li><strong>Pružatelj</strong> - identifikacija, država sjedišta, matično društvo.</li>
  <li><strong>Ugovorni aranžman</strong> - vrsta, trajanje, otkazni rokovi, mjerodavno pravo.</li>
  <li><strong>Funkcija</strong> koju usluga podupire, i je li ta funkcija kritična ili važna.</li>
  <li><strong>Podugovaranje</strong> - lanac ispod izravnog pružatelja, do razine koja je bitna.</li>
  <li><strong>Lokacija obrade i pohrane podataka.</strong></li>
  <li><strong>Procjena zamjenjivosti</strong> i postojanje izlazne strategije.</li>
</ul>
<p>Ključna riječ je <em>povezuje</em>. Registar ne traži samo popis, nego odnos između ugovora, funkcije koju taj ugovor podupire i kritičnosti te funkcije.</p>

<h2>Gdje se popunjavanje zaglavi</h2>
<div class="callout">
  <div class="c-label">Tri izvora podataka, tri istine</div>
  <p>Nabava ima popis ugovora. Informatika ima popis sustava. Financije imaju popis dobavljača kojima se plaća. U praksi se ta tri popisa ne poklapaju: postoje sustavi bez ugovora, ugovori bez sustava i plaćanja bez oboje. Prvo popunjavanje registra u pravilu je prvi put da netko te tri liste stavi jednu pored druge.</p>
</div>
<p>Drugi čest zastoj je <strong>podugovaranje</strong>. Izravni pružatelj usluga u oblaku je poznat. Tko je njegov pružatelj infrastrukture i gdje se podaci fizički nalaze, zna se rjeđe, a ugovori često ne obvezuju pružatelja da to prijavi.</p>
<p>Treći je <strong>određivanje kritičnosti funkcije</strong>. Ako organizacija nema BIA-u, kritičnost se procjenjuje ad hoc, po pružatelju umjesto po funkciji. To je pogrešan smjer: kritična je funkcija, a pružatelj to svojstvo nasljeđuje.</p>

<h2>Kako to ne raditi dvaput</h2>
<p>Registar informacija se najviše preklapa s tri stvari koje već imate ili biste trebali imati:</p>
<div class="tbl-wrap">
  <table>
    <thead><tr><th>Registar informacija traži</th><th>Već postoji u</th></tr></thead>
    <tbody>
      <tr><td>Popis IKT usluga i sustava</td><td>Registru imovine (ISO 27001, mjera 2 Uredbe)</td></tr>
      <tr><td>Kritičnost funkcije</td><td>Analizi poslovnog utjecaja (ISO 22301)</td></tr>
      <tr><td>Procjena rizika pružatelja</td><td>Upravljanju rizicima trećih strana (mjera 8 Uredbe)</td></tr>
      <tr><td>Izlazna strategija</td><td>Planu kontinuiteta poslovanja</td></tr>
    </tbody>
  </table>
</div>
<p>Organizacija koja ta četiri izvora vodi kao jedan povezani skup popunjava registar izvještajem. Organizacija koja ih vodi odvojeno popunjava ga ručno, svake godine iznova.</p>

<h2>Što napraviti prije popunjavanja</h2>
<ol>
  <li><strong>Uskladite tri popisa.</strong> Nabava, informatika i financije, jedan zajednički identifikator po pružatelju.</li>
  <li><strong>Krenite od funkcija, ne od dobavljača.</strong> Odredite koje su funkcije kritične ili važne, pa im pridružite usluge.</li>
  <li><strong>Provjerite ugovore na podugovaranje.</strong> Ondje gdje obveza prijave podugovaratelja ne postoji, to je nalaz sam po sebi.</li>
  <li><strong>Označite gdje podataka nema.</strong> Prazno polje s obrazloženjem je bolje od pogađanja - i lakše se popravlja u idućem ciklusu.</li>
</ol>

<div class="note">
  <p>DORA je za financijski sektor poseban propis, ali ne isključuje ostale obveze. Dokazna baza se preklapa s Uredbom o kibernetičkoj sigurnosti gotovo u cijelosti: isti registar imovine, isti registar rizika, isti zapisi o incidentima. Posao se radi jednom, izvještava na više strana.</p>
</div>
''',
 sources=[('Uredba (EU) 2022/2554 (DORA)', 'https://eur-lex.europa.eu/legal-content/HR/TXT/?uri=CELEX:32022R2554'),
          ('Provedbeni tehnički standardi za registar informacija (ESA)', 'https://www.eba.europa.eu/'),
          ('Uredba o kibernetičkoj sigurnosti, NN 135/2024, Prilog II., mjera 8', 'https://narodne-novine.nn.hr/clanci/sluzbeni/2024_11_135_2217.html')]))

ARTICLES.append(dict(
 slug="sto-osiguravatelji-pitaju-kibernetickom-osiguranju", cat="Cyber osiguranje", catkey="insurance",
 date="2026-07-07", read=6,
 title="Što osiguravatelji stvarno pitaju prije nego što ponude policu",
 lead="Upitnik za kibernetičko osiguranje nije formalnost nego procjena rizika koju netko drugi radi o vama. Pitanja su svake godine sve konkretnija, a netočan odgovor može biti razlog za odbijanje štete.",
 desc="Koja pitanja se pojavljuju u upitnicima za kibernetičko osiguranje, zašto se premija i pokriće vežu uz konkretne kontrole i kako se dokazna baza za ZKS i ISO 27001 koristi u pregovorima o polici.",
 body='''
<p>Kibernetičko osiguranje se u posljednjih nekoliko godina promijenilo iz proizvoda koji se prodavao uz kratki upitnik u proizvod koji se odobrava nakon tehničke procjene. Razlog je jednostavan: šteta od ransomwarea pokazala je da osiguravatelji ne mogu cijeniti rizik bez uvida u konkretne kontrole.</p>

<h2>Pitanja koja se ponavljaju</h2>
<p>Formulacije se razlikuju, ali sadržaj konvergira. Ovo su područja koja se pojavljuju gotovo u svakom upitniku:</p>
<h3>Autentifikacija i pristup</h3>
<ul>
  <li>Je li višefaktorska autentifikacija uključena za udaljeni pristup, za e-poštu i za administratorske račune? Sva tri se pitaju odvojeno.</li>
  <li>Koliko ima računa s povlaštenim pravima i kako se odobravaju?</li>
  <li>Postoje li odvojeni računi za administrativne zadatke?</li>
</ul>
<h3>Sigurnosne kopije</h3>
<ul>
  <li>Postoji li kopija koja je nedostupna iz produkcijske mreže?</li>
  <li>Kad je zadnji put napravljen test vraćanja podataka i koliko je trajao?</li>
  <li>Jesu li kopije šifrirane i je li pristup njima pod višefaktorskom autentifikacijom?</li>
</ul>
<h3>Detekcija i odgovor</h3>
<ul>
  <li>Postoji li zaštita krajnjih točaka s mogućnošću detekcije i odgovora?</li>
  <li>Prate li se zapisi, i tko ih gleda izvan radnog vremena?</li>
  <li>Postoji li plan odgovora na incident i je li isproban?</li>
</ul>
<h3>Upravljanje ranjivostima i lanac opskrbe</h3>
<ul>
  <li>Koliko brzo se zakrpavaju kritične ranjivosti na sustavima izloženima internetu?</li>
  <li>Koji su ključni dobavljači i imaju li pristup vašim sustavima?</li>
  <li>Postoje li sustavi kojima je istekla podrška proizvođača?</li>
</ul>

<div class="callout">
  <div class="c-label">Zašto je preciznost odgovora važna</div>
  <p>Upitnik je sastavni dio ugovora. Odgovor "da, imamo višefaktorsku autentifikaciju" kad je ona uključena za devedeset posto korisnika, a napad prođe kroz preostalih deset, otvara raspravu o tome je li rizik bio točno prikazan. Precizniji odgovor s ogradom uvijek je bolja pozicija od šireg odgovora bez nje.</p>
</div>

<h2>Što snižava premiju, a što je uvjet za ponudu</h2>
<p>Korisno je razlikovati dvije skupine. Neke kontrole djeluju na cijenu, druge su preduvjet za to da ponuda uopće postoji. U posljednjih nekoliko godina u drugu skupinu preselili su se višefaktorska autentifikacija za udaljeni pristup, izdvojena sigurnosna kopija i zaštita krajnjih točaka s detekcijom.</p>
<p>Organizacija koja to nema u pravilu ne dobiva skuplju policu nego nikakvu, ili policu s isključenjem baš za scenarij koji joj je najvjerojatniji.</p>

<h2>Kako iskoristiti ono što već imate</h2>
<p>Organizacija koja se uskladila sa ZKS-om ili ima ISO 27001 već posjeduje gotovo sve dokaze koje upitnik traži - samo u drugom formatu. Konkretno:</p>
<div class="tbl-wrap">
  <table>
    <thead><tr><th>Upitnik traži</th><th>Već imate u</th></tr></thead>
    <tbody>
      <tr><td>Popis kritične imovine i sustava bez podrške</td><td>Registru imovine (mjera 2)</td></tr>
      <tr><td>Praksu zakrpavanja i zaštite krajnjih točaka</td><td>Mjeri 5, kibernetička higijena</td></tr>
      <tr><td>Kontrolu pristupa i višefaktorsku autentifikaciju</td><td>Mjeri 7</td></tr>
      <tr><td>Plan odgovora na incident i zapise o vježbi</td><td>Mjeri 11</td></tr>
      <tr><td>Testove vraćanja podataka</td><td>Mjeri 12 i BIA-i</td></tr>
      <tr><td>Procjenu rizika dobavljača</td><td>Mjeri 8</td></tr>
    </tbody>
  </table>
</div>
<p>Praktična posljedica: pregovori o polici idu bolje ako se uz upitnik priloži izvještaj o stanju usklađenosti s bodovima po mjerama. Osiguravatelju je to jači dokaz od potvrdnih odgovora, a vama daje pregovaračku poziciju za premiju i za širinu pokrića.</p>

<div class="note">
  <p>Osiguranje ne zamjenjuje kontrole i ne pokriva regulatorne posljedice na način na koji pokriva izravnu štetu. Novčane kazne po propisima o kibernetičkoj sigurnosti i zaštiti podataka u većini su polica isključene ili ograničene - provjerite to prije nego što se na policu osloni plan upravljanja rizikom.</p>
</div>
''',
 sources=[('NIST Cybersecurity Framework 2.0', 'https://www.nist.gov/cyberframework'),
          ('Uredba o kibernetičkoj sigurnosti, NN 135/2024, Prilog II.', 'https://narodne-novine.nn.hr/clanci/sluzbeni/2024_11_135_2217.html'),
          ('HRN EN ISO/IEC 27001:2022, Prilog A', None)]))

ARTICLES.append(dict(
 slug="nist-csf-2-funkcija-govern", cat="Okviri", catkey="frameworks",
 date="2026-07-28", read=6,
 title="NIST CSF 2.0 i funkcija Govern: okvir koji je konačno priznao upravu",
 lead="Verzija 2.0 dodala je šestu funkciju iznad svih ostalih. Nije riječ o kozmetici - Govern je odgovor na nalaz koji se ponavljao godinama: tehničke kontrole ne popravljaju organizaciju koja nema vlasnika rizika.",
 desc="Što donosi funkcija Govern u NIST Cybersecurity Framework 2.0, kako se šest funkcija odnosi prema 13 mjera Uredbe o kibernetičkoj sigurnosti i zašto se okvir isplati koristiti kao zajednički jezik prema upravi.",
 body='''
<p>NIST-ov okvir kibernetičke sigurnosti dugo je imao pet funkcija: identificiraj, zaštiti, otkrij, odgovori i oporavi. Verzija 2.0 dodala je šestu - <strong>Govern</strong> - i nije je stavila uz ostale nego iznad njih.</p>

<h2>Što Govern pokriva</h2>
<p>Funkcija obuhvaća ono što se prije podrazumijevalo pa se zato rijetko provodilo:</p>
<ul>
  <li><strong>Organizacijski kontekst</strong> - misija, dionici, pravne i regulatorne obveze.</li>
  <li><strong>Strategija upravljanja rizikom</strong> - sklonost riziku i prag prihvatljivosti, izraženi tako da se po njima može odlučivati.</li>
  <li><strong>Uloge i odgovornosti</strong> - tko odlučuje, tko provodi, tko izvještava.</li>
  <li><strong>Politika</strong> - donesena, priopćena i održavana.</li>
  <li><strong>Nadzor</strong> - preispitivanje rezultata i prilagodba strategije.</li>
  <li><strong>Upravljanje rizikom lanca opskrbe</strong> - podignuto na razinu upravljanja, ne nabave.</li>
</ul>
<div class="callout">
  <div class="c-label">Zašto je to promjena, a ne dodatak</div>
  <p>U verziji 1.1 sklonost riziku bila je implicitna. To je značilo da su odluke o prihvaćanju rizika donosili ljudi koji za njih nisu odgovarali - najčešće informatika, jer je ona jedina imala podatke. Govern to eksplicitno vraća upravi.</p>
</div>

<h2>Kako se odnosi prema hrvatskim obvezama</h2>
<p>Okvir nije propis i nitko ga u Hrvatskoj ne traži. Koristan je iz drugog razloga: on je zajednički jezik. Uprava koja ne razumije podmjeru 1.3 razumije pitanje "koliko smo sposobni otkriti napad".</p>
<p>Preslikavanje je izravnije nego što se čini:</p>
<div class="tbl-wrap">
  <table>
    <thead><tr><th>Funkcija CSF 2.0</th><th>Odgovara mjerama Uredbe</th></tr></thead>
    <tbody>
      <tr><td><strong>Govern</strong></td><td>1 (predanost i odgovornost), 3 (upravljanje rizicima), 8 (lanac opskrbe)</td></tr>
      <tr><td><strong>Identify</strong></td><td>2 (imovina), 3 (rizici)</td></tr>
      <tr><td><strong>Protect</strong></td><td>4, 5, 6, 7, 9, 10, 13</td></tr>
      <tr><td><strong>Detect</strong></td><td>6 (nadzor mreže), 11 (detekcija incidenata)</td></tr>
      <tr><td><strong>Respond</strong></td><td>11 (postupanje s incidentima)</td></tr>
      <tr><td><strong>Recover</strong></td><td>12 (kontinuitet i krize)</td></tr>
    </tbody>
  </table>
</div>
<p>Isto preslikavanje postoji i prema ISO/IEC 27002:2022, jer njezini atributi kontrola koriste upravo koncepte identificiraj, zaštiti, otkrij, odgovori i oporavi. Tri okvira, jedna dokazna baza.</p>

<h2>Gdje je okvir stvarno koristan</h2>
<p>Ne kao zamjena za usklađenost, nego kao alat za tri stvari:</p>
<ol>
  <li><strong>Izvještavanje upravi.</strong> Šest funkcija je pregled koji stane na jedan slajd. Devedeset devet podmjera nije.</li>
  <li><strong>Postavljanje ciljnog profila.</strong> Okvir razlikuje trenutni i ciljni profil, što je bolji način za razgovor o proračunu od popisa nedostataka.</li>
  <li><strong>Usporedba kroz vrijeme.</strong> Jednom postavljeni profil daje trend, a trend je jedino što upravu zanima više od trenutnog stanja.</li>
</ol>

<h2>Zamka koju treba izbjeći</h2>
<p>Okvir opisuje ishode, ne kontrole. "Identificirani su i zabilježeni rizici lanca opskrbe" je ishod - kako ćete to postići, okvir ne propisuje. To je njegova snaga kad se koristi za upravljanje i njegova slabost kad se pokuša koristiti kao popis zadataka.</p>
<p>Organizacije koje pokušaju provesti CSF umjesto Uredbe završe s dobrim pregledom i bez dokazne baze. Redoslijed koji radi je obrnut: provedite mjere, pa rezultat prikažite kroz šest funkcija.</p>

<div class="note">
  <p>NIST je uz verziju 2.0 objavio i primjere provedbe koji svakom ishodu pridružuju konkretne aktivnosti. To je najkorisniji dio dokumentacije za nekoga tko okvir koristi prvi put, i najčešće preskočen.</p>
</div>
''',
 sources=[('NIST Cybersecurity Framework 2.0', 'https://www.nist.gov/cyberframework'),
          ('NIST CSF 2.0 Implementation Examples', 'https://www.nist.gov/cyberframework'),
          ('HRN EN ISO/IEC 27002:2022 - atributi kontrola', None)]))

ARTICLES.append(dict(
 slug="active-directory-putovi-napada", cat="Ofenzivna sigurnost", catkey="offensive",
 date="2026-08-18", read=7,
 title="Active Directory: pet nalaza koje pronađemo u gotovo svakom testu",
 lead="Domenska infrastruktura rijetko pada zbog nezakrpane ranjivosti. Pada zbog konfiguracije koja je nekad imala smisla, ostala je iza sebe i nitko je više ne gleda. Ovih pet nalaza vide se u većini okruženja.",
 desc="Najčešći nalazi u sigurnosnim procjenama Active Directoryja: naslijeđeni protokoli, prekomjerne delegacije, lozinke u atributima, nepotrebna članstva u povlaštenim grupama i pristup sigurnosnim kopijama.",
 body='''
<p>Kad se radi sigurnosna procjena domenske infrastrukture, očekivanje naručitelja obično je da će nalaz biti nezakrpani poslužitelj. U praksi je najčešći put od običnog korisničkog računa do potpune kontrole nad domenom sastavljen od konfiguracija koje nisu ranjivosti nego odluke - donesene davno, iz dobrog razloga koji više ne vrijedi.</p>
<p>Ovih pet ponavlja se najčešće.</p>

<h2>1. Naslijeđeni protokoli koji nitko ne koristi, ali su uključeni</h2>
<p>Protokoli za razlučivanje imena u lokalnoj mreži koji su ostali uključeni jer su nekad trebali jednoj aplikaciji. Rezultat je da napadač u mreži može navesti klijente da mu pošalju podatke za autentifikaciju, bez ijednog eksploita.</p>
<p><strong>Provjera:</strong> jesu li stariji protokoli za razlučivanje imena i stariji dijalekti dijeljenja datoteka isključeni, i traži li se potpisivanje prometa? <strong>Prepreka:</strong> gotovo uvijek jedna stara aplikacija koju nitko ne želi dirati.</p>

<h2>2. Delegacija koja je šira nego što itko misli</h2>
<p>Delegacija omogućuje računu da djeluje u ime korisnika. Postavljena bez ograničenja, ona znači da kompromitiranje jednog poslužitelja daje pristup svemu čemu pristupaju korisnici koji su se na njega spajali.</p>
<p><strong>Provjera:</strong> koji računi imaju neograničenu delegaciju i je li ijedan od njih izložen prema korisnicima? <strong>Popravak:</strong> prijelaz na ograničenu delegaciju i označavanje osjetljivih računa kao onih koji se ne mogu delegirati.</p>

<div class="callout">
  <div class="c-label">Zajednički nazivnik</div>
  <p>Nijedan od ovih nalaza ne pojavljuje se u izvještaju skenera ranjivosti kao kritičan. Svi se vide tek kad se gleda odnos između objekata, a ne stanje pojedinog poslužitelja. Zato procjena domene nije isto što i skeniranje mreže.</p>
</div>

<h2>3. Lozinke u atributima i skriptama</h2>
<p>Opisni atributi objekata su čitljivi svakom autenticiranom korisniku. U njima se redovito nađu lozinke servisnih računa, upisane radi praktičnosti. Isto vrijedi za skripte u dijeljenim mapama koje se izvršavaju pri prijavi.</p>
<p><strong>Provjera:</strong> pretraga atributa i dijeljenih mapa za nizovima koji izgledaju kao lozinke. Nalaz je rijetko prazan.</p>

<h2>4. Povlaštena članstva koja su preživjela promjenu radnog mjesta</h2>
<p>Administrator koji je prije tri godine rješavao jedan problem, dodan je u povlaštenu grupu i nikad uklonjen. Ili servisni račun aplikacije koja je ugašena, ali je račun ostao aktivan s pravima domenskog administratora.</p>
<p><strong>Provjera:</strong> koliko računa je u najpovlaštenijim grupama, kad se svaki zadnji put prijavio i tko je vlasnik? <strong>Uobičajen nalaz:</strong> broj članova je dvoznamenkast, a broj onih koji ta prava stvarno trebaju jednoznamenkast.</p>

<h2>5. Sigurnosne kopije domene dostupne iz domene</h2>
<p>Kopija baze podataka domene sadrži sve. Ako je pohranjena na dijeljenoj mapi kojoj pristupaju obični administratori poslužitelja, put do potpune kontrole prolazi kroz nju - bez ijednog napada na sam kontroler domene.</p>
<p><strong>Provjera:</strong> tko ima pristup sigurnosnim kopijama, jesu li šifrirane i je li kopija dostupna iz produkcijske domene? Ovo je ujedno i najizravnija poveznica prema mjeri 12 - kopija do koje ransomware dolazi nije sigurnosna kopija.</p>

<h2>Kako to povezati s obvezama</h2>
<p>Svih pet nalaza pripada mjerama iz Priloga II. Uredbe o kibernetičkoj sigurnosti, i to onima koje se najčešće ocjenjuju kao provedene:</p>
<ul>
  <li>Naslijeđeni protokoli i konfiguracija - mjera 6, sigurnost mreže</li>
  <li>Delegacija i povlaštena članstva - mjera 7, kontrola pristupa</li>
  <li>Lozinke u atributima - mjera 4, digitalni identiteti</li>
  <li>Pristup sigurnosnim kopijama - mjere 5 i 12</li>
</ul>
<p>To je razlog zašto tehnička procjena i procjena usklađenosti ne bi trebale biti odvojeni projekti. Dokument koji tvrdi da je kontrola pristupa uspostavljena, uz nalaz da domenskih administratora ima sedamnaest, ne prolazi ozbiljnu provjeru.</p>

<div class="note">
  <p>Sigurnosna procjena domene provodi se uz pisano odobrenje i u dogovorenom opsegu. Sve navedene provjere su izvedive na produkcijskoj domeni bez prekida rada, ali se radi o postupcima koji ostavljaju tragove u nadzoru - dogovorite ih s timom koji prati zapise, inače prvi nalaz bude vaš vlastiti test.</p>
</div>
''',
 sources=[('Uredba o kibernetičkoj sigurnosti, NN 135/2024, Prilog II., mjere 4, 6, 7 i 12', 'https://narodne-novine.nn.hr/clanci/sluzbeni/2024_11_135_2217.html'),
          ('HRN EN ISO/IEC 27002:2022 - kontrole tehnoloških mjera', None),
          ('NIST Cybersecurity Framework 2.0 - funkcije Protect i Detect', 'https://www.nist.gov/cyberframework')]))

# ══════════════════════════════════════════════════════════════════
# Serija: sluzbene smjernice NCSC-HR / CERT / ZSIS
# ══════════════════════════════════════════════════════════════════
ARTICLES.append(dict(
 slug="korelacijski-pregled-mjera", cat="ZKS / NIS2", catkey="zks",
 date="2026-02-24", read=7,
 title="Korelacijski pregled mjera: dokument koji vam štedi pola posla",
 lead="Članak 49. Uredbe obvezuje na izradu korelacijskog pregleda koji svaku podmjeru mapira na ISO 27001, ISO 27002, ISO 22301, NIST CSF 2.0, NIST SP 800-53 i CIS v8. Organizacije koje ga ne koriste pišu dokumentaciju koju već imaju.",
 desc="Što je korelacijski pregled mjera iz članka 49. Uredbe o kibernetičkoj sigurnosti, na koje se norme mapira i kako ga iskoristiti da se postojeća ISO ili NIST dokumentacija ne piše ponovno.",
 body='''
<p>Najskuplja greška u projektu usklađivanja sa Zakonom o kibernetičkoj sigurnosti nije propuštena kontrola. To je dokumentacija napisana drugi put, jer nitko nije provjerio što već postoji.</p>
<p>Uredba je taj problem predvidjela. Članak 49. propisuje <strong>korelacijski pregled mjera</strong> koji svaku podmjeru iz Priloga II. mapira na priznate norme i najbolje prakse.</p>

<h2>Na što se mapira</h2>
<p>Korelacijski pregled povezuje podskupove mjera s kontrolama iz šest izvora:</p>
<div class="tbl-wrap">
  <table>
    <thead><tr><th>Izvor</th><th>Što pokriva</th></tr></thead>
    <tbody>
      <tr><td><strong>ISO/IEC 27001:2022</strong></td><td>Okvir sustava upravljanja informacijskom sigurnošću</td></tr>
      <tr><td><strong>ISO/IEC 27002:2022</strong></td><td>Smjernice za primjenu kontrola, četiri tematske cjeline</td></tr>
      <tr><td><strong>ISO/IEC 22301:2019</strong></td><td>Kontinuitet poslovanja</td></tr>
      <tr><td><strong>NIST CSF 2.0</strong></td><td>Šest funkcija, uključujući novu Govern</td></tr>
      <tr><td><strong>NIST SP 800-53</strong></td><td>Opsežan skup tehničkih i organizacijskih kontrola</td></tr>
      <tr><td><strong>CIS v8</strong></td><td>Praktične kontrole, uključujući oblak i mobilne uređaje</td></tr>
      <tr><td><strong>Katalog kontrola ZSIS-a</strong></td><td>132 kontrole koje se koriste u samoprocjeni</td></tr>
    </tbody>
  </table>
</div>

<div class="callout">
  <div class="c-label">Što to znači u praksi</div>
  <p>Ako imate ISO 27001, korelacijski pregled vam za svaku podmjeru kaže koje su vaše postojeće kontrole tematski srodne. To nije dokaz usklađenosti, ali je popis mjesta gdje dokaz vjerojatno već postoji. Umjesto 99 praznih polja krećete s 99 polja koja imaju kandidata.</p>
</div>

<h2>Zamka koju sam pregled izrijekom navodi</h2>
<p>Smjernice napominju nešto što se lako previdi: <strong>opseg svake kontrole iz međunarodnih normi nadilazi opseg podmjere za koju se mapiranje provodi</strong>. Kontrola iz ISO 27002 koja se pojavljuje uz podmjeru 3.2 pokriva i stvari koje ta podmjera ne traži, a možda ne pokriva sve što podmjera traži.</p>
<p>Praktična posljedica: mapiranje je polazište, ne zaključak. Kvačica u tablici korelacije nije dokaz. Dokaz je zapis koji odgovara na ono što podmjera traži, u opsegu u kojem to traži.</p>

<h2>Kako ga koristiti da stvarno skrati posao</h2>
<ol>
  <li><strong>Krenite od svoje Izjave o primjenjivosti.</strong> Za svaku primjenjivu kontrolu pogledajte uz koje se podmjere pojavljuje u korelaciji. Time dobivate obrnuto mapiranje - iz onoga što imate prema onome što se traži.</li>
  <li><strong>Označite tri stanja, ne dva.</strong> Pokriveno, djelomično pokriveno, nepokriveno. Djelomično je najveća skupina i najkorisnija, jer se rješava dopunom postojećeg dokumenta, ne pisanjem novog.</li>
  <li><strong>Provjerite razinu.</strong> Kontrola koja zadovoljava osnovnu razinu ne mora zadovoljiti srednju. Korelacija ne razlikuje razine - to morate vi.</li>
  <li><strong>Zapišite obrazloženje uz svaku vezu.</strong> Kod provjere ćete morati objasniti zašto ste smatrali da postojeći dokument pokriva podmjeru. Rečenica napisana u trenutku mapiranja vrijedi više od rekonstrukcije šest mjeseci kasnije.</li>
</ol>

<h2>Za koga je najkorisniji</h2>
<p>Vrijednost pregleda raste s količinom onoga što već imate:</p>
<ul>
  <li><strong>Organizacija s ISO 27001 i 22301</strong> - najveća korist. Znatan dio mjera 2, 3, 7, 8 i 12 već ima dokaznu podlogu.</li>
  <li><strong>Organizacija koja radi prema CIS v8</strong> - tehničke mjere 5, 6, 7 i 9 dobrim dijelom su pokrivene, organizacijske nisu.</li>
  <li><strong>Organizacija koja izvještava prema NIST CSF-u</strong> - korelacija je ujedno i most prema izvještavanju upravi, jer se šest funkcija zadržava kao okvir prikaza.</li>
  <li><strong>Organizacija bez ičega od navedenog</strong> - pregled je i dalje koristan kao vodič što uopće napisati, jer upućuje na kontrole koje opisuju kako se podmjera obično provodi.</li>
</ul>

<div class="note">
  <p>Korelacijski pregled je pomagalo, ne propis. Nadležno tijelo ocjenjuje usklađenost s mjerama iz Priloga II. i kontrolama iz Kataloga, a ne s normama na koje pregled upućuje. Certifikat prema ISO 27001 ne zamjenjuje ni samoprocjenu ni reviziju.</p>
</div>
''',
 sources=[('Uredba o kibernetičkoj sigurnosti, NN 135/2024, čl. 49.', 'https://narodne-novine.nn.hr/clanci/sluzbeni/2024_11_135_2217.html'),
          ('Smjernice za korelacijski pregled mjera kibernetičke sigurnosti, NCSC-HR', 'https://www.ncsc.hr/'),
          ('ZSIS - Katalog kontrola (Prilog C)', 'https://www.zsis.hr/UserDocsImages/Samoprocjena/Prilog%20C%20-%20Katalog%20kontrola.pdf')]))

ARTICLES.append(dict(
 slug="prioritetne-preporuke-ncsc", cat="ZKS / NIS2", catkey="zks",
 date="2026-03-17", read=6,
 title="Prioritetne preporuke NCSC-HR: što napraviti prije nego što krenete s papirima",
 lead="Nacionalni centar za kibernetičku sigurnost objavio je kratak popis mjera koje smanjuju najveći dio rizika. Nijedna nije skupa, sve su izvedive u nekoliko tjedana, i većina organizacija ih nema provedene.",
 desc="Pregled prioritetnih preporuka NCSC-HR za zaštitu od kibernetičkih napada: izloženi servisi, lozinke i dvofaktorska autentifikacija, sigurnosne zakrpe i smanjenje broja povlaštenih računa.",
 body='''
<p>Kad organizacija dobije obavijest o kategorizaciji, prvi impuls je krenuti pisati politike. To je razumljivo jer se politike traže, ali je pogrešan redoslijed: napadač ne čita vašu politiku sigurnosti.</p>
<p>NCSC-HR objavio je popis prioritetnih preporuka koji je vrijedan upravo zato što je kratak. Ovo je sažetak s napomenama iz prakse.</p>

<h2>1. Znajte što vam je izloženo prema internetu</h2>
<p>Prvi korak je popis javno dostupnih servisa: web stranice, e-pošta, VPN ulazne točke, nadzorne konzole, servisi za udaljenu administraciju, servisi za razmjenu datoteka. Preporuka izrijekom navodi da se pregled može dobiti i vanjskim tražilicama poput Shodana ili Censysa.</p>
<div class="callout">
  <div class="c-label">Zašto to gotovo uvijek iznenadi</div>
  <p>Popis dobiven vanjskom tražilicom redovito je duži od popisa koji ima informatika. Razlika su testna okruženja, stara sučelja i uređaji koje je netko izložio radi praktičnosti pa zaboravio. To nisu ranjivosti - to su vrata za koja nitko ne zna da postoje.</p>
</div>

<h2>2. Ograničite dostupnost onoga što ne mora biti izloženo</h2>
<p>Preporuka navodi dva konkretna primjera. Servis za udaljenu administraciju vjerojatno ne treba biti dostupan preko interneta nego tek nakon VPN-a ili drugog oblika pred-autentifikacije. Ako VPN mora biti dostupan, može se ograničiti na pojedine adrese ili na domaće adresne raspone.</p>
<p>Dodaje se i blokiranje pristupa s anonimizacijskih mreža te ograničavanje izravnog pristupa internetu s poslužitelja - nadogradnje se distribuiraju interno, razlučivanje imena ide preko središnjih poslužitelja.</p>

<h2>3. Smanjite broj povlaštenih računa</h2>
<p>Uklonite račune bivših djelatnika, generičke račune koji nisu vezani uz osobu i servisne račune kojima administratorske ovlasti zapravo ne trebaju.</p>
<p>Ovo je mjera koja ne košta ništa i koju gotovo nitko nije proveo do kraja. Uobičajen nalaz u procjenama je dvoznamenkast broj članova u najpovlaštenijoj grupi, uz jednoznamenkast broj onih koji ta prava stvarno koriste.</p>

<h2>4. Lozinke i dvofaktorska autentifikacija</h2>
<p>Preporuka je ovdje neuobičajeno konkretna, pa vrijedi citirati brojke:</p>
<ul>
  <li><strong>12 znakova</strong> minimalno za redovne korisnike</li>
  <li><strong>16 znakova</strong> za privilegirane korisnike</li>
  <li><strong>24 znaka</strong> za servisne račune</li>
  <li>Kombinacija velikih i malih slova, znamenki i posebnih znakova</li>
  <li>Zaključavanje računa nakon prekomjernih neuspjelih pokušaja, uz automatsko otključavanje nakon razumnog razdoblja</li>
</ul>
<p>Uz to dolazi dvofaktorska autentifikacija na sučeljima za prijavu - e-pošta, VPN, sustavi za upravljanje sadržajem - s posebnim naglaskom na dvije skupine: sučelja izložena internetu i sučelja koja vode u internu mrežu.</p>
<div class="callout">
  <div class="c-label">Detalj koji se najčešće preskoči</div>
  <p>Preporuka traži provjeru <em>kada je lozinka zadnji put promijenjena</em>. Ako su pravila u međuvremenu postrožena, a lozinke se od tada nisu mijenjale, nova pravila nisu primijenjena ni na jedan postojeći račun. Politika je ažurirana, stanje nije.</p>
</div>

<h2>5. Sigurnosne zakrpe s imenom uz svaki dio infrastrukture</h2>
<p>Preporuka traži da se odredi <strong>tko je zadužen</strong> za zakrpe na poslužiteljima, mrežnoj opremi i sigurnosnim uređajima, te da se uspostavi proces redovne primjene najmanje jednom mjesečno, uz dodatnu primjenu po saznanju o novim kritičnim ranjivostima.</p>
<p>Riječ "tko" nosi cijelu težinu. Mrežna oprema i sigurnosni uređaji su u praksi najzapušteniji jer se nalaze između odgovornosti sistemaca i mrežaša.</p>

<h2>Kako se to uklapa u obveze</h2>
<p>Sve navedeno pripada mjerama iz Priloga II. Uredbe - pretežno mjeri 5 (kibernetička higijena), mjeri 7 (kontrola pristupa) i mjeri 6 (sigurnost mreže). Prednost je što su to mjere kod kojih dokaz nastaje iz same provedbe: zapis o zakrpama, popis povlaštenih računa i konfiguracija dvofaktorske autentifikacije istovremeno su i mjera i dokaz.</p>
<p>Zato je ovo dobar prvi korak i za usklađenost i za stvarnu sigurnost, što se ne poklapa uvijek.</p>
''',
 sources=[('Prioritetne preporuke za zaštitu od kibernetičkih napada, NCSC-HR', 'https://www.ncsc.hr/'),
          ('Uredba o kibernetičkoj sigurnosti, NN 135/2024, Prilog II., mjere 5, 6 i 7', 'https://narodne-novine.nn.hr/clanci/sluzbeni/2024_11_135_2217.html')]))

ARTICLES.append(dict(
 slug="dnevnicki-zapisi-sto-prikupljati", cat="Nadzor i zapisi", catkey="logging",
 date="2026-04-07", read=7,
 title="Dnevnički zapisi: jedanaest izvora bez kojih istraga incidenta ne postoji",
 lead="Kad dođe do napada, već je kasno za postavljanje prikupljanja zapisa. NCSC-HR objavio je preporuke koje nabrajaju izvore po prioritetu - i one otkrivaju koliko toga većina organizacija uopće ne bilježi.",
 desc="Koje izvore dnevničkih zapisa preporučuje NCSC-HR, zašto se prikupljanje mora postaviti prije incidenta i kako se to povezuje s mjerama nadzora iz Uredbe o kibernetičkoj sigurnosti.",
 body='''
<p>Preporuke NCSC-HR-a za sustavno prikupljanje dnevničkih zapisa otvaraju rečenicom koja sažima cijeli problem: nedostatak zapisa jedan je od najvećih izazova za otkrivanje, istragu i odgovor. U trenutku destruktivnog napada već je kasno - istragom se najčešće neće uspjeti utvrditi što se sve dogodilo.</p>
<p>Praktična posljedica je neugodna. Organizacija koja nema zapise ne može odgovoriti na najvažnije pitanje nakon incidenta: <strong>je li napadač bio i drugdje, i koliko dugo</strong>. Bez toga se ne može ni potvrditi da je incident zatvoren.</p>

<h2>Preduvjeti koji nisu tehnički</h2>
<p>Dokument započinje s onim što mora postojati prije nego što se uključi ijedan zapis:</p>
<ul>
  <li>Inventar uređaja i programskih rješenja</li>
  <li>Dokumentacija informacijskog sustava i njegovih segmenata</li>
  <li>Definirani vlasnici sustava</li>
  <li>Praćenje servisnih i korisničkih računa</li>
</ul>
<div class="callout">
  <div class="c-label">Zašto to nije birokracija</div>
  <p>Zapis bez konteksta je niz redaka. Da bi se iz njega izvukla informacija, mora se znati što je taj sustav, tko ga koristi i što je za njega normalno. Zato je registar imovine preduvjet za nadzor, a ne paralelna obveza.</p>
</div>

<h2>Izvori zapisa po prioritetu</h2>
<p>Preporuke nabrajaju jedanaest skupina izvora. Poredak nije slučajan - prvi su oni koji najčešće daju prvi trag:</p>
<div class="tbl-wrap">
  <table>
    <thead><tr><th>Izvor</th><th>Što otkriva</th></tr></thead>
    <tbody>
      <tr><td><strong>DNS</strong></td><td>Komunikaciju prema zloćudnoj infrastrukturi, često prvi vidljivi trag</td></tr>
      <tr><td><strong>Web poslužitelji</strong></td><td>Pokušaje iskorištavanja ranjivosti i pristup s neuobičajenih adresa</td></tr>
      <tr><td><strong>Elektronička pošta</strong></td><td>Phishing, pravila preusmjeravanja koja postavi napadač</td></tr>
      <tr><td><strong>VPN i udaljeni pristup</strong></td><td>Prijave s neuobičajenih lokacija i u neuobičajeno vrijeme</td></tr>
      <tr><td><strong>Središnja sigurnosna rješenja</strong></td><td>Detekcije koje su možda već zabilježene, a nitko ih nije pogledao</td></tr>
      <tr><td><strong>Web proxy</strong></td><td>Odlazni promet prema poslužiteljima za upravljanje napadom</td></tr>
      <tr><td><strong>Klijenti i poslužitelji</strong></td><td>Prijave, pokretanje procesa, promjene ovlasti</td></tr>
      <tr><td><strong>Vatrozid</strong></td><td>Mrežne veze, prihvaćene i odbijene</td></tr>
      <tr><td><strong>Mrežni uređaji</strong></td><td>Promjene konfiguracije, pristup upravljačkom sučelju</td></tr>
      <tr><td><strong>DHCP</strong></td><td>Vezu između adrese i uređaja u određenom trenutku</td></tr>
      <tr><td><strong>Ostali izvori</strong></td><td>Aplikacije, baze podataka, sustavi za sigurnosne kopije</td></tr>
    </tbody>
  </table>
</div>
<p>DHCP je najčešće zaboravljen, a bez njega se adresa iz zapisa ne može povezati s uređajem. Istraga tada zna da se nešto dogodilo, ali ne i gdje.</p>

<h2>Tri stvari koje odlučuju je li prikupljanje upotrebljivo</h2>
<h3>Vrijeme mora biti usklađeno</h3>
<p>Zapisi iz različitih sustava spajaju se po vremenu. Ako su satovi razmaknuti, redoslijed događaja se ne može rekonstruirati. Sinkronizacija vremena je jednodnevni posao koji odlučuje o upotrebljivosti svega ostalog.</p>
<h3>Zapisi moraju biti izvan dosega napadača</h3>
<p>Zapisi koji ostaju samo na kompromitiranom sustavu izbrisat će se zajedno sa svime ostalim. Središnje prikupljanje nije stvar udobnosti nego integriteta dokaza.</p>
<h3>Razdoblje čuvanja mora biti dulje od vremena otkrivanja</h3>
<p>Napadi se u pravilu otkriju tjednima ili mjesecima nakon početka. Zapisi koji se čuvaju sedam dana odgovaraju na pitanje što se dogodilo jučer, a ne na pitanje kada je napadač ušao.</p>

<h2>Poveznica prema obvezama</h2>
<p>Prikupljanje i analiza zapisa pripada mjeri 6 (sigurnost mreže) i mjeri 11 (postupanje s incidentima) iz Priloga II. Uredbe, a preduvjeti se naslanjaju na mjeru 2 (upravljanje imovinom). U ZSIS-ovom katalogu kontrola skupina oznaka NAD pokriva praćenje i nadzor i jedna je od većih - šesnaest kontrola.</p>
<p>To nije slučajno. Nadzor je mjera kod koje se najlakše napiše da postoji, a najteže dokaže da radi.</p>

<div class="note">
  <p>Preporuke NCSC-HR-a temeljene su na dokumentu danskog centra za kibernetičku sigurnost, dopunjenom domaćim iskustvima. Sadrže i scenarije primjene - pretraga po indikatoru, phishing i složeni incident - koji su korisni kao predložak za vježbu.</p>
</div>
''',
 sources=[('Preporuke za uspostavu sustavnog prikupljanja dnevničkih zapisa, NCSC-HR', 'https://www.ncsc.hr/'),
          ('Uredba o kibernetičkoj sigurnosti, NN 135/2024, Prilog II., mjere 2, 6 i 11', 'https://narodne-novine.nn.hr/clanci/sluzbeni/2024_11_135_2217.html'),
          ('ZSIS - Katalog kontrola, skupina NAD', 'https://www.zsis.hr/UserDocsImages/Samoprocjena/Prilog%20C%20-%20Katalog%20kontrola.pdf')]))

ARTICLES.append(dict(
 slug="znacajan-incident-pet-obavijesti-pixi", cat="Incidenti", catkey="incidenti",
 date="2026-04-28", read=8,
 title="Značajan incident: pet vrsta obavijesti, platforma PiXi i pravilo koje se previđa",
 lead="Rokovi 24 i 72 sata su poznati. Manje je poznato da vrsta obavijesti ima pet, da završno izvješće teče od početne obavijesti a ne od saznanja, i da se dva manja incidenta s istim uzrokom mogu zbrojiti u jedan značajan.",
 desc="Detaljan pregled obveze obavještavanja o značajnim incidentima: pet vrsta obavijesti i njihovi rokovi, prijava preko platforme PiXi, rezervni kanali i pravilo o incidentima s istim temeljnim uzrokom.",
 body='''
<p>Opće smjernice za provedbu obveze obavještavanja o značajnim incidentima donijeli su nadležni CSIRT-ovi na temelju članka 72. Uredbe. Dokument je precizniji od većine tekstova koji o rokovima kruže, i sadrži nekoliko odredbi koje mijenjaju planiranje.</p>

<h2>Pet vrsta obavijesti, ne tri</h2>
<p>Uredba u člancima 65. do 71. propisuje pet vrsta obavijesti:</p>
<div class="tbl-wrap">
  <table>
    <thead><tr><th>Obavijest</th><th>Rok</th><th>Napomena</th></tr></thead>
    <tbody>
      <tr><td><strong>Rano upozorenje</strong></td><td>24 sata</td><td>Bez odgode, od saznanja za značajan incident</td></tr>
      <tr><td><strong>Početna obavijest</strong></td><td>72 sata</td><td>Bez odgode, od saznanja</td></tr>
      <tr><td><strong>Privremeno izvješće</strong></td><td>48 sati do 7 dana</td><td>Samo na zahtjev nadležnog CSIRT-a</td></tr>
      <tr><td><strong>Završno izvješće</strong></td><td>30 dana</td><td>Od dostave <em>početne obavijesti</em></td></tr>
      <tr><td><strong>Izvješće o napretku</strong></td><td>svakih 30 dana</td><td>Ako incident još traje</td></tr>
    </tbody>
  </table>
</div>
<div class="callout">
  <div class="c-label">Detalj koji mijenja računicu</div>
  <p>Završno izvješće ne teče od saznanja nego <strong>od dostave početne obavijesti</strong>. Organizacija koja početnu obavijest pošalje 70. sat ima 30 dana od tog trenutka, ne 30 dana od trenutka kad je incident otkrila. Razlika je do tri dana i može odlučiti o tome jeste li u roku.</p>
</div>
<p>Ako incident još traje kad rok istekne, umjesto završnog izvješća šalje se izvješće o napretku, i tako svakih idućih 30 dana dok incident ne završi.</p>

<h2>Iznimka za pružatelje usluga povjerenja</h2>
<p>Prema članku 68. Uredbe, pružatelji usluga povjerenja ne dostavljaju rano upozorenje. Umjesto toga, početnu obavijest dostavljaju u roku od 24 sata. Ostali rokovi ostaju isti.</p>

<div class="callout">
  <div class="c-label">Izračunajte svoje rokove</div>
  <p>Svih pet datuma za konkretan incident dobijete u <a href="/alati/rokovi-prijave-incidenta/">kalkulatoru rokova</a>, uz obračun iznimke za pružatelje usluga povjerenja i usporedne prijave AZOP-u.</p>
</div>

<h2>Prijava se predaje preko platforme PiXi</h2>
<p>Obavještavanje se provodi ispunjavanjem web obrazaca na Nacionalnoj platformi za prikupljanje, analizu i razmjenu podataka o kibernetičkim prijetnjama i incidentima, dostupnoj na <strong>pixi.carnet.hr</strong>. Pristup imaju isključivo ovlaštene osobe, putem Nacionalnog identifikacijskog i autentifikacijskog sustava.</p>
<div class="callout">
  <div class="c-label">Što napraviti prije incidenta</div>
  <p>Pristup platformi ovisi o nacionalnom sustavu prijave. Ako se u trenutku incidenta ispostavi da nitko nema pristup ili da ovlaštena osoba više nije zaposlena, sat teče dok se to rješava. Provjerite tko ima pristup i imenujte zamjenu prije nego što zatreba.</p>
</div>
<p>Ako platforma nije dostupna zbog tehničkih poteškoća, održavanja ili nedostupnosti sustava prijave, obavijest se šalje ispunjavanjem obrazaca i slanjem na adresu nadležnog CSIRT-a. Nakon što platforma ponovno postane dostupna, podaci se moraju unijeti i u nju.</p>

<h2>Pravilo o ponovljenim incidentima</h2>
<p>Članak 62. Uredbe propisuje da se dva ili više incidenta <strong>s istim temeljnim uzrokom u razdoblju od šest mjeseci</strong>, koji zajedno ispunjavaju najmanje jedan kriterij za značajan incident, za potrebe obavještavanja smatraju jednim značajnim incidentom.</p>
<p>Šalje se jedna obavijest koja obuhvaća sve te incidente, uz izričitu napomenu u opisu da je riječ o obavijesti po članku 62.</p>
<p>To znači da niz manjih incidenata koje ste pojedinačno ocijenili beznačajnima može zajedno prijeći prag. Praktična posljedica: <strong>evidencija svih incidenata, i onih ispod praga, nije formalnost nego preduvjet za ispunjenje ove obveze.</strong> Bez nje ne možete znati da imate ponovljeni uzrok.</p>

<h2>Više sektora, više CSIRT-ova</h2>
<p>Nadležnost CSIRT-a određuje se prema sektoru, sukladno Prilogu III. Zakona. Subjekt kategoriziran u jednom sektoru uvijek obavještava CSIRT nadležan za taj sektor.</p>
<p>Subjekt kategoriziran u više sektora, kod incidenta koji obuhvaća poslovanje u više njih, može poslati jednu obavijest za sve obuhvaćene sektore ako je za njih nadležan isti CSIRT. Ako nije, obavijesti idu odvojeno.</p>

<h2>Posebna pravila za digitalne pružatelje</h2>
<p>Za subjekte iz članka 22. Zakona koji se vode i u posebnom registru - pružatelje usluga DNS-a, registre vršnih domena, pružatelje usluga u oblaku i podatkovnih centara, mreža za isporuku sadržaja, upravljanih i upravljanih sigurnosnih usluga, internetskih tržišta, tražilica, platformi društvenih mreža te usluga povjerenja - primjenjuju se posebna pravila za utvrđivanje značajnosti prema Provedbenoj uredbi Komisije (EU) 2024/2690.</p>

<div class="note">
  <p>Ako je incidentom zahvaćena i povreda osobnih podataka, usporedno teče prijava Agenciji za zaštitu osobnih podataka u roku od 72 sata prema članku 33. Opće uredbe. Ta dva postupka ne zamjenjuju jedan drugoga i ne teku jedan za drugim.</p>
</div>
''',
 sources=[('Opće smjernice za provedbu obveze obavještavanja o značajnim incidentima, NCSC-HR i Nacionalni CERT', 'https://www.ncsc.hr/'),
          ('Uredba o kibernetičkoj sigurnosti, NN 135/2024, čl. 59.-72.', 'https://narodne-novine.nn.hr/clanci/sluzbeni/2024_11_135_2217.html'),
          ('Provedbena uredba Komisije (EU) 2024/2690', 'https://eur-lex.europa.eu/legal-content/HR/TXT/?uri=CELEX:32024R2690'),
          ('Platforma PiXi', 'https://pixi.carnet.hr/')]))

ARTICLES.append(dict(
 slug="nacionalna-taksonomija-incidenata", cat="Incidenti", catkey="incidenti",
 date="2026-05-19", read=6,
 title="Nacionalna taksonomija incidenata: pet atributa koji zamjenjuju opisnu prijavu",
 lead="Sigurnosno-obavještajna agencija objavila je taksonomiju koja incident opisuje s pet atributa umjesto slobodnim tekstom. Model se zove VOUND i korisniji je nego što izgleda - ne samo za prijavu nego i za predviđanje sljedećeg poteza napadača.",
 desc="Kako radi Nacionalna taksonomija kibernetičkih incidenata: vektor napada, operativni učinak, učinak na informacije, objekt napada i dosegnuta faza. Zašto strukturirani opis incidenta ubrzava prijavu i istragu.",
 body='''
<p>Opis incidenta slobodnim tekstom ima dva problema. Prvi je da se dva analitičara ne slože oko toga što se dogodilo. Drugi je da se opisi ne mogu uspoređivati - ni između organizacija, ni kroz vrijeme unutar iste organizacije.</p>
<p>Nacionalna taksonomija kibernetičkih incidenata rješava oba tako što incident opisuje s pet atributa. Dokument je vlasništvo Sigurnosno-obavještajne agencije, izrađen je za javnu objavu i smije se koristiti uz navođenje izvora.</p>

<h2>Pet atributa</h2>
<div class="tbl-wrap">
  <table>
    <thead><tr><th>Atribut</th><th>Odgovara na pitanje</th></tr></thead>
    <tbody>
      <tr><td><strong>V</strong> - Vektor napada</td><td>Kojim je putem napad izveden?</td></tr>
      <tr><td><strong>O</strong> - Operativni učinak</td><td>Što je napad učinio sustavu i uslugama?</td></tr>
      <tr><td><strong>U</strong> - Učinak na informacije</td><td>Što se dogodilo s podacima?</td></tr>
      <tr><td><strong>N</strong> - Objekt napada</td><td>Što je bilo meta?</td></tr>
      <tr><td><strong>D</strong> - Dosegnuta faza napada</td><td>Dokle je napadač stigao?</td></tr>
    </tbody>
  </table>
</div>
<p>Skraćeno: <strong>VOUND</strong>. Svaki atribut ima definirane vrijednosti, pa se incident opisuje kombinacijom umjesto rečenicom.</p>

<div class="callout">
  <div class="c-label">Zašto je razdvajanje učinka na dva atributa važno</div>
  <p>Taksonomija odvaja operativni učinak od učinka na informacije. Ransomware koji je zaustavio proizvodnju i ransomware koji je zaustavio proizvodnju i iznio podatke imaju isti operativni učinak, a bitno različit učinak na informacije - i različite obveze prijave. Opis slobodnim tekstom tu razliku često zamagli.</p>
</div>

<h2>Dosegnuta faza je atribut koji najviše govori</h2>
<p>Faza opisuje dokle je napadač stigao u nizu koraka. To je jedini atribut koji ima prognostičku vrijednost: ako znate u kojoj je fazi napad zaustavljen, znate i što je logičan sljedeći korak koji nije izveden - i gdje treba tražiti tragove.</p>
<p>Dokument tu mogućnost izrijekom razrađuje, kroz praćenje tijeka napada i predviđanje sljedećih koraka pomoću pet atributa. To ga čini upotrebljivim i tijekom incidenta, ne samo pri prijavi.</p>

<h2>Gdje se taksonomija isplati u praksi</h2>
<ol>
  <li><strong>Pri prijavi značajnog incidenta.</strong> Obrasci traže opis koji strukturirani zapis popunjava brže i dosljednije od slobodnog teksta, u trenutku kad je vremena najmanje.</li>
  <li><strong>Pri utvrđivanju ponovljenog uzroka.</strong> Članak 62. Uredbe zbraja incidente s istim temeljnim uzrokom u razdoblju od šest mjeseci. Dva incidenta s istim vektorom i istim objektom napada vide se odmah; dva slobodna opisa ne.</li>
  <li><strong>Pri izvještavanju uprave.</strong> Struktura daje brojke: koliko incidenata po vektoru, koliko je dosegnulo koju fazu. To je trend, a ne anegdota.</li>
  <li><strong>Pri razmjeni informacija.</strong> Taksonomija je zajednički jezik prema CSIRT-u i prema drugim organizacijama u sektoru.</li>
</ol>

<h2>Kako je uvesti bez alata</h2>
<p>Nije potrebna platforma. Dovoljno je da evidencija incidenata ima pet dodatnih stupaca i da ih se popunjava pri zatvaranju svakog incidenta, uključujući one ispod praga značajnosti.</p>
<p>Upravo ti manji incidenti daju najveću korist: oni su ulaz u pravilo o ponovljenom uzroku, i oni pokazuju obrasce prije nego što obrazac proizvede štetu.</p>

<div class="note">
  <p>Dokument sadrži i priloge s primjerima klasifikacije poznatih incidenata prema atributima - kampanje zloćudnog koda, ransomware u dvije varijante, izmjenu sadržaja web stranice, skeniranje i uskraćivanje usluge. Ti su primjeri najbrži način da tim uskladi tumačenje prije nego što taksonomiju počne primjenjivati.</p>
</div>
''',
 sources=[('Nacionalna taksonomija kibernetičkih incidenata, Sigurnosno-obavještajna agencija', 'https://www.ncsc.hr/'),
          ('Uredba o kibernetičkoj sigurnosti, NN 135/2024, čl. 62.', 'https://narodne-novine.nn.hr/clanci/sluzbeni/2024_11_135_2217.html'),
          ('Uredba (EU) 2019/881 - definicije kibernetičke sigurnosti i prijetnje', 'https://eur-lex.europa.eu/legal-content/HR/TXT/?uri=CELEX:32019R0881')]))

# ══════════════════════════════════════════════════════════════════
# Serija: umjetna inteligencija i OT
# ══════════════════════════════════════════════════════════════════
ARTICLES.append(dict(
 slug="akt-o-umjetnoj-inteligenciji-razine-rizika", cat="Umjetna inteligencija", catkey="ai",
 date="2026-06-02", read=7,
 title="Akt o umjetnoj inteligenciji: četiri razine rizika i pitanje koje dolazi prvo",
 lead="Uredba (EU) 2024/1689 ne uređuje tehnologiju nego njezinu primjenu. Isti model može biti neregulatorno pomagalo i visokorizičan sustav, ovisno o tome za što ga koristite - a to znači da klasifikacija počinje popisom, ne pravnom analizom.",
 desc="Kako Akt o umjetnoj inteligenciji dijeli sustave u četiri razine rizika, po čemu se određuje visokorizični sustav i zašto klasifikacija mora početi od popisa AI sustava u organizaciji.",
 body='''
<p>Uredba (EU) 2024/1689, poznata kao Akt o umjetnoj inteligenciji, prvi je sveobuhvatan propis te vrste. Njezin je pristup jednostavniji nego što se čini iz opsega teksta: <strong>obveze ne ovise o tome kakav je model, nego o tome za što se koristi i koga može oštetiti.</strong></p>

<h2>Četiri razine</h2>
<div class="tbl-wrap">
  <table>
    <thead><tr><th>Razina</th><th>Što obuhvaća</th><th>Posljedica</th></tr></thead>
    <tbody>
      <tr><td><strong>Neprihvatljiv rizik</strong></td><td>Zabranjene prakse</td><td>Zabrana primjene</td></tr>
      <tr><td><strong>Visok rizik</strong></td><td>Sustavi u osjetljivim područjima primjene i sigurnosne komponente proizvoda</td><td>Najveći skup obveza</td></tr>
      <tr><td><strong>Ograničen rizik</strong></td><td>Sustavi koji komuniciraju s ljudima ili proizvode sadržaj</td><td>Obveza transparentnosti</td></tr>
      <tr><td><strong>Minimalan rizik</strong></td><td>Sve ostalo</td><td>Bez posebnih obveza</td></tr>
    </tbody>
  </table>
</div>
<p>Većina onoga što organizacije koriste svakodnevno završi u zadnje dvije kategorije. To ne znači da posla nema - znači da je posao drukčiji.</p>

<div class="callout">
  <div class="c-label">Ista tehnologija, različita razina</div>
  <p>Model koji predlaže tekst je minimalan rizik kad piše sažetak sastanka, a visokorizičan kad se koristi u odabiru kandidata za zapošljavanje. Klasifikacija se ne radi po alatu nego po slučaju uporabe. Organizacija koja ima jedan alat i deset načina korištenja ima deset stavki za procjenu, ne jednu.</p>
</div>

<h2>Zašto se počinje popisom</h2>
<p>Prvo pitanje nije "je li ovo visokorizično". Prvo pitanje je <strong>koje sve sustave uopće koristimo</strong>. Odgovor je gotovo uvijek nepotpun, iz tri razloga:</p>
<ul>
  <li><strong>Ugrađene funkcije.</strong> Postojeći poslovni softver dobiva AI funkcije nadogradnjom, bez odluke o nabavi.</li>
  <li><strong>Alati koje su uveli sami zaposlenici.</strong> Besplatna verzija alata koji netko koristi za pripremu dokumenata ne prolazi kroz nabavu ni kroz informatiku.</li>
  <li><strong>Usluge dobavljača.</strong> Vanjski pružatelj koji obrađuje vaše podatke uz pomoć umjetne inteligencije uvodi je i u vaš lanac, bez vaše odluke.</li>
</ul>
<p>Popis se zato ne dobiva upitom informatici nego istim postupkom kojim se radi inventar imovine: obilaskom procesa i razgovorom s vlasnicima.</p>

<h2>Uloga određuje obveze</h2>
<p>Uredba razlikuje uloge, a najvažnija je razlika između onoga tko sustav razvija i stavlja na tržište i onoga tko ga koristi. Većina organizacija je u drugoj skupini, s bitno manjim skupom obveza - ali ne s nikakvim.</p>
<p>Uloga se, međutim, može promijeniti neopreznim potezom. Organizacija koja preuzme tuđi sustav, stavi na njega svoje ime ili ga bitno izmijeni može preuzeti i teže obveze. To je razlog zašto odluka o prilagodbi modela nije samo tehnička.</p>

<h2>Što napraviti sada</h2>
<ol>
  <li><strong>Napravite popis.</strong> Sustav, vlasnik, slučaj uporabe, podaci koji ulaze, odluka na koju utječe.</li>
  <li><strong>Označite slučajeve uporabe koji dodiruju ljude.</strong> Zapošljavanje, ocjenjivanje, pristup uslugama, nadzor zaposlenika - to su područja gdje razina raste.</li>
  <li><strong>Provjerite ulazne podatke.</strong> Ako ulaze osobni podaci, usporedno se primjenjuje Opća uredba, s vlastitim zahtjevima za osnovu obrade i procjenu učinka.</li>
  <li><strong>Uspostavite pravila prije nego što ih zatreba.</strong> Interna pravila korištenja, s jasnim popisom onoga što se ne smije unositi u vanjske alate, spriječit će više problema nego bilo koja kasnija analiza.</li>
</ol>

<div class="note">
  <p>Akt o umjetnoj inteligenciji primjenjuje se postupno, s odredbama koje stupaju na snagu u različitim rokovima. Zabranjene prakse i obveza osposobljenosti primjenjuju se prvi, obveze za visokorizične sustave kasnije. Provjerite koji se rok odnosi na vašu situaciju prije nego što se planira dinamika projekta.</p>
</div>
''',
 sources=[('Uredba (EU) 2024/1689 (Akt o umjetnoj inteligenciji)', 'https://eur-lex.europa.eu/legal-content/HR/TXT/?uri=CELEX:32024R1689'),
          ('Uredba (EU) 2016/679 (Opća uredba o zaštiti podataka)', 'https://eur-lex.europa.eu/legal-content/HR/TXT/?uri=CELEX:32016R0679')]))

ARTICLES.append(dict(
 slug="zabranjene-prakse-i-ai-pismenost", cat="Umjetna inteligencija", catkey="ai",
 date="2026-06-30", read=6,
 title="Zabranjene prakse i obveza osposobljenosti: dvije odredbe koje su već na snazi",
 lead="Dok se rasprava vodi o visokorizičnim sustavima, dvije odredbe Akta o umjetnoj inteligenciji primjenjuju se prve. Jedna zabranjuje određene prakse bez iznimke, druga traži da ljudi koji sustave koriste znaju što rade.",
 desc="Koje prakse Akt o umjetnoj inteligenciji zabranjuje bez iznimke, što znači obveza AI pismenosti iz članka 4. i kako je ispuniti bez posebnog programa edukacije.",
 body='''
<p>Akt o umjetnoj inteligenciji primjenjuje se postupno. Dvije skupine odredbi dolaze prve i obje se odnose na svakoga tko sustave koristi, ne samo na one koji ih razvijaju.</p>

<h2>Zabranjene prakse</h2>
<p>Članak 5. nabraja prakse koje se ne smiju primjenjivati, bez procjene rizika i bez mogućnosti da se opravdaju. Među njima su:</p>
<ul>
  <li><strong>Manipulativne tehnike</strong> koje bitno narušavaju sposobnost osobe da donese informiranu odluku i time joj nanose znatnu štetu.</li>
  <li><strong>Iskorištavanje ranjivosti</strong> zbog dobi, invaliditeta ili socijalne odnosno ekonomske situacije.</li>
  <li><strong>Društveno bodovanje</strong> koje dovodi do nepovoljnog postupanja u kontekstu nepovezanom s onim u kojem su podaci prikupljeni.</li>
  <li><strong>Procjena rizika počinjenja kaznenog djela</strong> temeljena isključivo na profiliranju ili osobinama ličnosti.</li>
  <li><strong>Neciljano prikupljanje slika lica</strong> s interneta ili nadzornih snimaka radi izgradnje baza za prepoznavanje.</li>
  <li><strong>Prepoznavanje emocija na radnom mjestu i u obrazovanju</strong>, uz uske iznimke za medicinske i sigurnosne razloge.</li>
  <li><strong>Biometrijska kategorizacija</strong> radi zaključivanja o osjetljivim svojstvima osobe.</li>
</ul>
<div class="callout">
  <div class="c-label">Gdje se to dodiruje s običnim poslovanjem</div>
  <p>Većina zabrana zvuči daleko od prosječne tvrtke dok se ne pogleda dvije stavke. Prepoznavanje emocija na radnom mjestu pojavljuje se u alatima za analizu poziva u kontakt centrima i u sustavima za praćenje angažmana zaposlenika. Biometrijska kategorizacija pojavljuje se u analitici video nadzora. Nijedno se ne nabavlja pod tim imenom.</p>
</div>

<h2>Obveza osposobljenosti</h2>
<p>Članak 4. traži da se osigura dostatna razina osposobljenosti u području umjetne inteligencije kod osoblja i drugih osoba koje u ime organizacije rade sa sustavima umjetne inteligencije. Razina se određuje prema tehničkom znanju tih osoba, njihovom iskustvu i obrazovanju te kontekstu u kojem se sustavi koriste.</p>
<p>Odredba je kratka i namjerno otvorena. Ne propisuje sate, program ni ispit. Traži da ljudi razumiju što alat radi, gdje griješi i što se s njim ne smije.</p>

<h3>Kako je ispuniti bez zasebnog programa</h3>
<p>U organizacijama koje već imaju program podizanja svijesti o sigurnosti, ovo je dopuna, ne novi projekt:</p>
<ol>
  <li><strong>Interna pravila korištenja</strong> - što se smije unositi u vanjske alate, a što ne. Ovo je najkraći put do najveće koristi.</li>
  <li><strong>Kratka edukacija po ulozi.</strong> Onaj tko alat koristi za pripremu teksta i onaj tko ga koristi u odlučivanju o ljudima ne trebaju isti sadržaj.</li>
  <li><strong>Konkretni primjeri pogrešaka.</strong> Izmišljeni podaci prikazani uvjerljivo, pristranost u podacima za treniranje, lažno samopouzdanje modela.</li>
  <li><strong>Evidencija.</strong> Tko je kada prošao edukaciju. Bez zapisa obveza je neprovjerljiva, isto kao i kod mjera iz Uredbe o kibernetičkoj sigurnosti.</li>
</ol>

<h2>Preklapanje s ostalim obvezama</h2>
<p>Zapis o edukaciji koji nastane ovdje istovremeno hrani mjeru 5 iz Priloga II. Uredbe o kibernetičkoj sigurnosti, koja traži podizanje svijesti zaposlenika. Interna pravila korištenja dodiruju i zaštitu podataka, jer je unos osobnih podataka u vanjski alat obrada s vlastitom pravnom osnovom.</p>
<p>To je opći obrazac koji se ponavlja: propisi su različiti, dokazna baza je zajednička.</p>

<div class="note">
  <p>Ovaj tekst je informativan pregled, ne pravni savjet. Točan doseg zabranjenih praksi i način primjene obveze osposobljenosti ovise o konkretnim okolnostima i o smjernicama koje se objavljuju na razini Unije.</p>
</div>
''',
 sources=[('Uredba (EU) 2024/1689 (Akt o umjetnoj inteligenciji), čl. 4. i 5.', 'https://eur-lex.europa.eu/legal-content/HR/TXT/?uri=CELEX:32024R1689'),
          ('Uredba o kibernetičkoj sigurnosti, NN 135/2024, Prilog II., mjera 5', 'https://narodne-novine.nn.hr/clanci/sluzbeni/2024_11_135_2217.html')]))

ARTICLES.append(dict(
 slug="registar-ai-sustava-i-registar-imovine", cat="Umjetna inteligencija", catkey="ai",
 date="2026-07-14", read=6,
 title="Registar AI sustava i registar imovine: zašto se vode kao jedan",
 lead="Organizacije koje popis sustava umjetne inteligencije uvedu kao zaseban dokument otkriju za godinu dana da imaju dva registra koja se razilaze. Preklapanje je veće nego razlika, a razlika staje u četiri stupca.",
 desc="Kako proširiti postojeći registar informacijske imovine tako da pokrije i zahtjeve Akta o umjetnoj inteligenciji, umjesto vođenja odvojenog registra AI sustava.",
 body='''
<p>Kad stigne obveza vezana uz umjetnu inteligenciju, uobičajen prvi potez je otvoriti novu tablicu. Logika je razumljiva: novi propis, novi dokument. Posljedica je predvidljiva.</p>
<p>Za godinu dana postoje dva popisa. Jedan zna za sve poslužitelje ali ne zna koji od njih vrte model. Drugi zna za modele ali ne zna tko je vlasnik sustava na kojem rade. Nijedan nije potpun i nitko ne zna koji je noviji.</p>

<h2>Što oba registra traže isto</h2>
<p>Usporedite li zahtjeve, preklapanje je veliko:</p>
<div class="tbl-wrap">
  <table>
    <thead><tr><th>Podatak</th><th>Registar imovine</th><th>Popis AI sustava</th></tr></thead>
    <tbody>
      <tr><td>Naziv i opis sustava</td><td>da</td><td>da</td></tr>
      <tr><td>Vlasnik</td><td>da</td><td>da</td></tr>
      <tr><td>Poslovni proces koji podupire</td><td>da</td><td>da</td></tr>
      <tr><td>Kritičnost</td><td>da</td><td>da</td></tr>
      <tr><td>Vrste podataka koje obrađuje</td><td>da</td><td>da</td></tr>
      <tr><td>Dobavljač i ugovor</td><td>da</td><td>da</td></tr>
      <tr><td>Lokacija obrade</td><td>da</td><td>da</td></tr>
      <tr><td>Procjena rizika</td><td>da</td><td>da</td></tr>
    </tbody>
  </table>
</div>
<p>Osam stavki koje se ionako vode. Mjera 2 iz Priloga II. Uredbe o kibernetičkoj sigurnosti traži inventar imovine s klasifikacijom i izdvajanjem kritične imovine - to je isti posao.</p>

<h2>Četiri stupca koji se dodaju</h2>
<p>Razlika staje u nekoliko polja koja se dopisuju postojećem registru:</p>
<ol>
  <li><strong>Je li sustav zasnovan na umjetnoj inteligenciji</strong> - da, ne, ili sadrži ugrađenu komponentu. Treća vrijednost je važna jer pokriva postojeći softver koji je AI funkciju dobio nadogradnjom.</li>
  <li><strong>Slučaj uporabe</strong> - konkretno, ne "asistent". Isti alat s tri načina korištenja daje tri retka.</li>
  <li><strong>Uloga organizacije</strong> - koristimo li sustav, razvijamo li ga, ili smo ga izmijenili i stavili na njega svoje ime. To određuje opseg obveza.</li>
  <li><strong>Razina rizika i obrazloženje</strong> - zaključak procjene, s rečenicom zašto. Rečenica je važnija od oznake.</li>
</ol>

<div class="callout">
  <div class="c-label">Zašto slučaj uporabe, a ne alat</div>
  <p>Obveze prema Aktu o umjetnoj inteligenciji ovise o primjeni, ne o tehnologiji. Registar koji ima jedan redak po alatu ne može nositi klasifikaciju, jer isti alat može istovremeno biti minimalnog i visokog rizika. Redak po slučaju uporabe rješava to bez ijedne dodatne tablice.</p>
</div>

<h2>Što se time dobiva osim urednosti</h2>
<ul>
  <li><strong>Procjena rizika se radi jednom.</strong> Rizik gubitka dostupnosti sustava i rizik pogrešne odluke koju sustav proizvede procjenjuju se u istom registru rizika, s istom metodologijom i istim vlasnikom.</li>
  <li><strong>Lanac opskrbe je pokriven.</strong> Dobavljač AI usluge je treća strana kao i svaka druga, pa ulazi u procjenu prema mjeri 8 bez posebnog postupka.</li>
  <li><strong>Zaštita podataka se veže na isto mjesto.</strong> Ako u sustav ulaze osobni podaci, veza prema evidenciji obrada postoji preko istog retka.</li>
  <li><strong>Nadzor ima jedan izvor.</strong> Prikupljanje zapisa i praćenje ponašanja sustava oslanja se na inventar - ako sustav nije u inventaru, nije ni u nadzoru.</li>
</ul>

<h2>Prvi korak, konkretno</h2>
<p>Otvorite postojeći registar imovine, dodajte četiri stupca i prođite popis. Za većinu redaka odgovor na prvo pitanje bit će "ne" i posao je gotov u minuti. Redaka s odgovorom "da" ili "sadrži komponentu" bit će manje nego što se očekuje, a upravo oni traže pažnju.</p>
<p>Ono što će vam nedostajati nisu sustavi iz informatike nego alati koje su uveli sami zaposlenici i AI funkcije koje su stigle nadogradnjom postojećeg softvera. To se ne nalazi u tablici nego u razgovoru s vlasnicima procesa.</p>

<div class="note">
  <p>Isto načelo vrijedi i za DORA registar informacija i za evidenciju obrada prema Općoj uredbi. Svaki od njih traži pogled na istu imovinu iz drugog kuta. Organizacije koje ih vode kao poglede na jedan izvor izvještavaju; one koje ih vode odvojeno prepisuju.</p>
</div>
''',
 sources=[('Uredba (EU) 2024/1689 (Akt o umjetnoj inteligenciji)', 'https://eur-lex.europa.eu/legal-content/HR/TXT/?uri=CELEX:32024R1689'),
          ('Uredba o kibernetičkoj sigurnosti, NN 135/2024, Prilog II., mjere 2 i 8', 'https://narodne-novine.nn.hr/clanci/sluzbeni/2024_11_135_2217.html'),
          ('HRN EN ISO/IEC 27001:2022, Prilog A - upravljanje imovinom', None)]))

ARTICLES.append(dict(
 slug="ai-u-obrani-gdje-pomaze-gdje-odmaze", cat="Umjetna inteligencija", catkey="ai",
 date="2026-08-04", read=7,
 title="Umjetna inteligencija u obrani: gdje stvarno pomaže, a gdje samo pomiče problem",
 lead="Obećanje je da će model uočiti napad koji je čovjeku promakao. Stvarnost je da model dobro radi na zadacima gdje postoji puno primjera i jasan ishod, a loše ondje gdje ih nema - a upravo su ondje najskuplji propusti.",
 desc="Realna procjena primjene umjetne inteligencije u kibernetičkoj obrani: gdje daje mjerljivu korist, gdje stvara lažno povjerenje i koje kontrole treba postaviti prije uvođenja.",
 body='''
<p>Rasprava o umjetnoj inteligenciji u sigurnosti brzo sklizne u dvije krajnosti: da mijenja sve ili da ne mijenja ništa. Korisnije je pitati gdje statistički model ima prednost pred pravilom, a gdje nema.</p>

<h2>Gdje daje mjerljivu korist</h2>
<h3>Smanjenje šuma</h3>
<p>Grupiranje sličnih upozorenja, uklanjanje duplikata i rangiranje po vjerojatnosti stvarnog nalaza. To je zadatak s puno primjera i jasnim ishodom, i ondje modeli rade dobro. Korist nije u tome da model otkriva napade nego u tome da analitičar ne troši dan na tisuću upozorenja od kojih je devet stotina isti događaj.</p>
<h3>Otkrivanje odstupanja od uobičajenog</h3>
<p>Prijava u tri ujutro s adrese iz zemlje u kojoj organizacija ne posluje, ili račun koji odjednom pristupa deset puta većem broju datoteka nego inače. Model uči što je normalno i prijavljuje što nije. Radi dobro kad je "normalno" stabilno, a slabo u okruženjima koja se stalno mijenjaju.</p>
<h3>Ubrzanje razumijevanja</h3>
<p>Sažimanje zapisa, objašnjavanje nepoznate naredbe, prijedlog upita nad podacima. Ovdje model ne odlučuje nego skraćuje vrijeme do razumijevanja, uz čovjeka koji provjerava.</p>
<h3>Priprema dokumentacije</h3>
<p>Nacrt izvještaja o incidentu, prijedlog strukture politike, usporedba postojećeg dokumenta sa zahtjevima norme. Uz obveznu provjeru, ovo je danas najisplativija primjena u compliance radu.</p>

<div class="callout">
  <div class="c-label">Zajedničko svim korisnim primjenama</div>
  <p>Model skraćuje put do odgovora, ali odgovor potvrđuje čovjek. Čim se ta potvrda ukloni radi brzine, korist se pretvara u rizik - i to rizik koji se ne vidi dok se ne dogodi.</p>
</div>

<h2>Gdje pomiče problem umjesto da ga riješi</h2>
<h3>Kad je uzrok organizacijski</h3>
<p>Sustav koji rangira upozorenja ne pomaže organizaciji koja upozorenja ionako nitko ne gleda izvan radnog vremena. Detekcija bez odgovora nije obrana, a alat ne stvara dežurstvo.</p>
<h3>Kad nema podataka</h3>
<p>Model uči iz zapisa. Organizacija koja ne prikuplja zapise sa svih ključnih izvora neće dobiti korisne rezultate - dobit će uvjerljive rezultate na nepotpunim podacima, što je gore.</p>
<h3>Kad se izlaz uzme kao činjenica</h3>
<p>Jezični modeli proizvode uvjerljiv tekst i onda kad nemaju osnovu. Naziv ranjivosti koji ne postoji, članak propisa koji je izmišljen, konfiguracijski parametar koji nikad nije postojao - sve to izlazi u istom tonu kao i točan odgovor.</p>
<h3>Kad se osjetljivi podaci pošalju van</h3>
<p>Analiza incidenta u vanjskom alatu znači da su zapisi, imena sustava i ponekad podaci klijenata izašli iz organizacije. To je obrada s vlastitim pravnim posljedicama, i događa se najčešće upravo pod pritiskom incidenta.</p>

<h2>Napadačka strana</h2>
<p>Ista tehnologija snizila je prag za napadače na tri konkretna načina: phishing bez jezičnih pogrešaka i prilagođen primatelju, brža priprema varijanti zloćudnog koda, i uvjerljivo lažiranje glasa u prijevarama koje ciljaju na plaćanje.</p>
<p>Nijedan od njih nije nova vrsta napada. Svi su postojeći napadi izvedeni jeftinije i uvjerljivije. Zato obrana nije novi alat nego pooštravanje kontrola koje već postoje - potvrda plaćanja drugim kanalom, dvofaktorska autentifikacija, i edukacija koja više ne smije učiti ljude da phishing prepoznaju po lošem hrvatskom.</p>

<h2>Što postaviti prije uvođenja</h2>
<ol>
  <li><strong>Upišite sustav u registar imovine</strong>, s vlasnikom i slučajem uporabe.</li>
  <li><strong>Odredite što u njega ne smije ući.</strong> Osobni podaci, podaci klijenata, konfiguracije, zapisi s imenima sustava.</li>
  <li><strong>Zadržite čovjeka u odluci</strong> svugdje gdje izlaz utječe na ljude ili na dostupnost usluge.</li>
  <li><strong>Bilježite što je model predložio i što je čovjek odlučio.</strong> Bez tog zapisa nema ni provjere ni učenja iz pogrešaka.</li>
  <li><strong>Mjerite.</strong> Ako se nakon uvođenja ne skrati vrijeme do otkrivanja ili do odgovora, alat nije donio ono zbog čega je nabavljen.</li>
</ol>

<div class="note">
  <p>Akt o umjetnoj inteligenciji na sigurnosne alate primjenjuje istu logiku kao i na ostale: obveze ovise o primjeni. Alat koji rangira upozorenja u pravilu je niske razine rizika, ali alat koji automatski blokira korisnika donosi odluku o osobi - i to mijenja procjenu.</p>
</div>
''',
 sources=[('Uredba (EU) 2024/1689 (Akt o umjetnoj inteligenciji)', 'https://eur-lex.europa.eu/legal-content/HR/TXT/?uri=CELEX:32024R1689'),
          ('NIST Cybersecurity Framework 2.0 - funkcije Detect i Respond', 'https://www.nist.gov/cyberframework'),
          ('Preporuke za uspostavu sustavnog prikupljanja dnevničkih zapisa, NCSC-HR', 'https://www.ncsc.hr/')]))

ARTICLES.append(dict(
 slug="ot-sustavi-i-zks", cat="OT i industrija", catkey="ot",
 date="2026-08-25", read=7,
 title="OT sustavi i ZKS: zašto industrijska mreža ne prolazi IT kontrole",
 lead="Mjere iz Priloga II. pisane su tako da vrijede i za informacijske i za operativne sustave. Problem nastaje pri provedbi: kontrola koja je u uredskoj mreži rutinska, u proizvodnoj može zaustaviti liniju.",
 desc="Kako primijeniti mjere upravljanja kibernetičkim sigurnosnim rizicima na operativne tehnologije: zakrpe, segmentacija, nadzor i kontinuitet u okruženjima gdje se sustavi ne smiju restartati.",
 body='''
<p>Uredba o kibernetičkoj sigurnosti izrijekom razmatra primjenjivost mjera i u informacijskim i u operativnim sustavima. To je ispravno postavljeno, ali ostavlja otvoreno pitanje kako se ista kontrola provodi ondje gdje se sustav ne smije isključiti.</p>
<p>Kod energetike, vodoopskrbe, prometa i prehrambene industrije to nije rubni slučaj nego glavnina posla.</p>

<h2>Četiri razlike koje mijenjaju provedbu</h2>
<div class="tbl-wrap">
  <table>
    <thead><tr><th></th><th>IT okruženje</th><th>OT okruženje</th></tr></thead>
    <tbody>
      <tr><td><strong>Prioritet</strong></td><td>Povjerljivost, pa cjelovitost, pa dostupnost</td><td>Dostupnost i sigurnost ljudi, pa cjelovitost</td></tr>
      <tr><td><strong>Životni vijek</strong></td><td>3 do 5 godina</td><td>15 do 25 godina</td></tr>
      <tr><td><strong>Prozor za održavanje</strong></td><td>Noću, tjedno</td><td>Jednom ili dvaput godišnje</td></tr>
      <tr><td><strong>Posljedica ispada</strong></td><td>Poslovna šteta</td><td>Fizička šteta, opasnost za ljude</td></tr>
    </tbody>
  </table>
</div>
<p>Iz toga slijedi sve ostalo. Zakrpa koja se u uredskoj mreži primijeni istog tjedna, u pogonu čeka planirani zastoj. Skeniranje ranjivosti koje je u IT-u bezopasno, u OT-u može srušiti uređaj koji ne očekuje takav promet.</p>

<h2>Kako se mjere provode drukčije</h2>
<h3>Mjera 5 - zakrpe i higijena</h3>
<p>Ako se zakrpa ne može primijeniti, obveza ne nestaje - mijenja se odgovor. Rizik se tretira nadoknadnim kontrolama: izolacija segmenta, ograničenje prometa prema uređaju, pojačan nadzor. Ključno je da to bude <strong>zapisano kao odluka s obrazloženjem</strong>, a ne prešućeno kao propust.</p>
<div class="callout">
  <div class="c-label">Što provjera zapravo gleda</div>
  <p>Nalaz "sustav nije zakrpan" nije sam po sebi neusklađenost ako postoji procjena rizika, odluka o nadoknadnim kontrolama i dokaz da te kontrole rade. Neusklađenost je kad zakrpe nema, a nema ni odluke - jer tada nitko nije procijenio rizik.</p>
</div>
<h3>Mjera 6 - sigurnost mreže</h3>
<p>Segmentacija je najisplativija kontrola u OT-u jer ne dira uređaje. Odvajanje proizvodne mreže od uredske, jednosmjerni prijenos podataka prema poslovnim sustavima i uklanjanje izravnog pristupa internetu s uređaja rješavaju veći dio izloženosti bez ijednog restarta.</p>
<h3>Mjera 7 - kontrola pristupa</h3>
<p>Najveći stvarni rizik u praksi je udaljeni pristup dobavljača opreme. Trajni pristup s dijeljenim računom i bez nadzora nalazi se često, i objašnjava se ugovorom o održavanju. Zamjena je pristup koji se odobrava po zahtjevu, traje ograničeno i bilježi se.</p>
<h3>Mjera 11 i 12 - incidenti i kontinuitet</h3>
<p>Kriterij značajnosti u OT-u mora uključiti fizičke posljedice, ne samo dostupnost usluge. Plan oporavka mora računati s time da vraćanje sustava u rad znači i sigurno pokretanje procesa, što je operativni postupak, a ne informatički.</p>

<h2>Nadzor bez zadiranja</h2>
<p>Prikupljanje dnevničkih zapisa u OT-u često nije izvedivo na uređajima, ali jest na mreži. Pasivno praćenje prometa daje inventar uređaja, uobičajene obrasce komunikacije i odstupanja - bez ijednog paketa poslanog prema uređaju.</p>
<p>To je ujedno i najbrži put do inventara imovine koji mjera 2 traži, jer je popis OT uređaja u dokumentaciji redovito stariji od stvarnog stanja.</p>

<h2>Gdje projekt najčešće zapne</h2>
<ul>
  <li><strong>Vlasništvo.</strong> OT je u pogonu, sigurnost je u informatici, a odgovornost nije napisana. Mjera 1 traži imenovane osobe upravo zbog toga.</li>
  <li><strong>Ugovori s dobavljačima opreme.</strong> Sklopljeni prije nego što je itko razmišljao o kibernetičkoj sigurnosti, bez obveza prijave ranjivosti i bez pravila za udaljeni pristup. To je nalaz po mjeri 8.</li>
  <li><strong>Sustavi bez podrške proizvođača.</strong> Nisu iznimka nego pravilo, i traže odluku uprave o prihvaćanju rizika ili planu zamjene, s rokom.</li>
</ul>

<div class="note">
  <p>Prije bilo kakvog aktivnog testiranja u OT okruženju dogovorite opseg i vrijeme s voditeljem pogona. Skeniranje koje je u uredskoj mreži rutinsko u proizvodnji može uzrokovati zastoj - a zastoj uzrokovan sigurnosnom provjerom najbrži je način da se cijeli program izgubi podršku pogona.</p>
</div>
''',
 sources=[('Uredba o kibernetičkoj sigurnosti, NN 135/2024, Prilog II.', 'https://narodne-novine.nn.hr/clanci/sluzbeni/2024_11_135_2217.html'),
          ('Direktiva (EU) 2022/2555 (NIS2) - sektori energetike, vodoopskrbe i prometa', 'https://eur-lex.europa.eu/legal-content/HR/TXT/?uri=CELEX:32022L2555'),
          ('Prioritetne preporuke za zaštitu od kibernetičkih napada, NCSC-HR', 'https://www.ncsc.hr/')]))

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
  <div class="c-label">Calculate your deadlines</div>
  <p>Enter the moment of awareness in the <a href="/en/tools/incident-reporting-deadlines/">deadline calculator</a> and get all five dates at once, including the parallel GDPR notification. It runs in your browser and needs no sign-up.</p>
</div>

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
# Dodatni engleski clanci
# ══════════════════════════════════════════════════════════════════
ARTICLES_EN.append(dict(
 slug="iso-27002-2022-control-attributes", cat="ISO standards", catkey="iso",
 date="2026-05-05", read=6,
 title="ISO 27002:2022: 93 controls and the five attributes most people skip",
 lead="The 2022 revision cut 114 controls to 93 and reorganised them into four themes instead of fourteen clauses. The bigger change is the attributes - and they are why an old Statement of Applicability cannot simply be renumbered.",
 desc="What changed in ISO/IEC 27002:2022 - four themes instead of fourteen clauses, 93 controls and five attributes. How to migrate an existing Statement of Applicability without losing the evidence base.",
 body='''
<p>Migration to ISO/IEC 27002:2022 is usually executed as a renumbering exercise: take the old Statement of Applicability, map the controls into the new numbering, done. It formally passes. It also misses the only part of the revision that genuinely changes how you work.</p>

<h2>What changed in numbers</h2>
<div class="tbl-wrap">
  <table>
    <thead><tr><th></th><th>ISO 27002:2013</th><th>ISO 27002:2022</th></tr></thead>
    <tbody>
      <tr><td><strong>Controls</strong></td><td>114</td><td>93</td></tr>
      <tr><td><strong>Structure</strong></td><td>14 clauses</td><td>4 themes</td></tr>
      <tr><td><strong>New controls</strong></td><td>-</td><td>11</td></tr>
      <tr><td><strong>Merged</strong></td><td>-</td><td>57 into 24</td></tr>
      <tr><td><strong>Attributes</strong></td><td>none</td><td>5 per control</td></tr>
    </tbody>
  </table>
</div>
<p>The four themes are organisational, people, physical and technological. The reduction in control count is not a reduction in scope - most of it comes from merging controls that were implemented together in practice anyway.</p>

<h2>The eleven new controls</h2>
<p>This is the list worth reviewing before concluding that everything is covered:</p>
<ul>
  <li><strong>Threat intelligence</strong> - collecting and using information on threats relevant to you.</li>
  <li><strong>Information security for use of cloud services</strong> - from procurement through to exit.</li>
  <li><strong>ICT readiness for business continuity</strong> - the bridge to ISO 22301.</li>
  <li><strong>Physical security monitoring</strong> - surveillance of premises, not just entry control.</li>
  <li><strong>Configuration management</strong> - secure baselines and drift detection.</li>
  <li><strong>Information deletion</strong> - at your end and at your processors'.</li>
  <li><strong>Data masking</strong> - particularly in test environments.</li>
  <li><strong>Data leakage prevention</strong> - as a control, not as a product.</li>
  <li><strong>Monitoring activities</strong> - networks, systems and applications, for anomaly detection.</li>
  <li><strong>Web filtering</strong> - control of access to external sites.</li>
  <li><strong>Secure coding</strong> - rules that also apply to acquired software.</li>
</ul>
<p>In most organisations at least four of these eleven exist technically but have no document describing them and no record evidencing them. That is the difference between a control that works and a control that passes an audit.</p>

<h2>The attributes are the real novelty</h2>
<p>Every control in the new standard carries five attributes: control type (preventive, detective, corrective), information security properties (confidentiality, integrity, availability), cybersecurity concepts (identify, protect, detect, respond, recover), operational capabilities and security domains.</p>
<div class="callout">
  <div class="c-label">Why that is useful</div>
  <p>Attributes let you re-sort the same set of controls according to the question being asked. The board asks "how capable are we of detecting an attack?" - filter on the <em>detect</em> concept. A regulator wants evidence on availability - filter on that property. Without attributes, every such question means walking the whole list by hand.</p>
</div>
<p>Attributes are also the fastest route to mapping against other frameworks. The cybersecurity concepts correspond directly to the NIST framework functions, so an organisation working to both the Croatian rules and NIST does not need two unconnected spreadsheets.</p>

<h2>How to migrate without losing your evidence</h2>
<ol>
  <li><strong>Map old into new, not the other way round.</strong> Start from your 114 controls and find each a home among the 93. What has no counterpart has usually been merged, not withdrawn.</li>
  <li><strong>Keep the trail.</strong> Retain a column with the old identifier in the Statement of Applicability for at least one cycle. Auditors and internal staff will think in the old numbering for another year.</li>
  <li><strong>Treat the eleven new controls separately.</strong> That is the only place where genuinely new work arises.</li>
  <li><strong>Populate the attributes.</strong> Not because the standard mandates it, but because this is the one moment when you will be going through the controls one by one anyway.</li>
  <li><strong>Check the links to other obligations.</strong> The new controls on cloud, monitoring and continuity feed directly into the measures of the Croatian Cybersecurity Regulation.</li>
</ol>

<div class="note">
  <p>ISO/IEC 27001:2022 is the standard you certify against; 27002 is the implementation guidance for the Annex A controls. You do not get certified against 27002, but you write your evidence with its help.</p>
</div>
''',
 sources=[('ISO/IEC 27001:2022, Annex A', None),
          ('ISO/IEC 27002:2022 - Information security controls', None),
          ('ISO/IEC 27001:2022/Amd 1:2024 - climate action changes', None)]))

ARTICLES_EN.append(dict(
 slug="bia-that-produces-a-usable-rto", cat="Business continuity", catkey="bcm",
 date="2026-05-26", read=7,
 title="A BIA that produces a usable RTO, not a number everyone ignores",
 lead="Business impact analysis usually ends as a table in which every process has a four-hour RTO. If everything is critical, nothing is - and the recovery plan built on it will not survive the first real outage.",
 desc="How to run a business impact analysis under ISO 22301 so that RTO and RPO are usable: who supplies the data, how to avoid everything being critical, and how the BIA connects to measure 12 of the Croatian Cybersecurity Regulation.",
 body='''
<p>Business impact analysis is the foundation of the whole continuity management system. If it is wrong, everything standing on it is wrong: recovery plans, investment in redundancy, supplier contracts and priorities during an actual crisis.</p>
<p>And it is wrong more often than people think, almost always in the same way.</p>

<h2>The symptom: every process is critical</h2>
<p>When department heads are asked how long their process may be down, the answer is predictable. Nobody says "my process can wait three days". The result is a table in which twenty of twenty-two processes carry a four-hour RTO, and an organisation trying to deliver that has to double its infrastructure.</p>
<div class="callout">
  <div class="c-label">Why this happens</div>
  <p>"How long may this process be down" is a question about perceived importance. "What is the loss after 4, 24 and 72 hours, expressed in money, contractual penalty, regulatory exposure and number of affected customers" is a question about consequence. The first produces identical answers; the second differentiates them.</p>
</div>

<h2>How to set the BIA up so it discriminates</h2>
<p>Three changes in approach produce a usable result:</p>
<h3>1. Measure impact over time, not at a single point</h3>
<p>For each process, estimate the consequence at several time slices - say after 4 hours, 24 hours, 3 days and 7 days. The resulting curve shows where the real pain threshold sits. Most processes have a flat curve up to a point and then a sharp step; the RTO belongs before that step, not at an arbitrary four hours.</p>
<h3>2. Use several impact categories</h3>
<p>Financial loss, contractual obligations, regulatory consequences, safety of people and reputation. A process can be financially insignificant and regulatorily critical - incident notification is exactly that case.</p>
<h3>3. Make total recovery capacity a constrained resource</h3>
<p>If it is known in advance that you can fund recovery of five processes within the first four hours, department heads stop ranking their own process in isolation and start allocating a limited capacity together. The conversation changes immediately.</p>

<h2>RPO is decided elsewhere</h2>
<p>A common conflation: RTO and RPO get set by the same person in the same row of the table. RTO is a business decision about how long a process may be down. RPO is a decision about how much data you may lose, and it depends on how often the data changes and whether the loss can be reconstructed manually.</p>
<p>A process that handles one daily batch can have a two-hour RTO and a 24-hour RPO with no inconsistency at all. A process taking real-time transactions cannot.</p>

<h2>What a BIA must produce to be usable</h2>
<ul>
  <li><strong>A process list with owners</strong> - people, not departments.</li>
  <li><strong>Dependencies.</strong> Applications, people, premises, suppliers and other processes. A process with a four-hour RTO that depends on a supplier contracted at a 48-hour SLA does not have a four-hour RTO.</li>
  <li><strong>An impact curve</strong> by category and time slice.</li>
  <li><strong>RTO and RPO with justification.</strong> A number without reasoning can be neither defended nor challenged.</li>
  <li><strong>A minimum service level.</strong> You rarely recover to a hundred per cent - define what is enough to keep working.</li>
  <li><strong>The gap between current and required capability.</strong> That is the input to the budget, and the most valuable output of the whole exercise.</li>
</ul>

<h2>The link to the Croatian Cybersecurity Regulation</h2>
<p>Measure 12 of Annex II requires business continuity and cyber crisis management across eight sub-measures. A BIA run to ISO 22301 covers almost all of its analytical part, but two things need adding:</p>
<ol>
  <li><strong>Cyber scenarios.</strong> A classical BIA assumes a systems outage. Ransomware is not an outage - the systems run, but the data is unavailable and the backups may be affected. RPO behaves differently in that scenario.</li>
  <li><strong>The link to incident management.</strong> The continuity plan and the incident response plan must share an activation criterion, or one will be triggered without the other in a crisis.</li>
</ol>

<div class="note">
  <p>A plan that has never been exercised documents intent, not capability. A two-hour tabletop with a scenario and real time measurement reveals more than another round of editing the document - and produces exactly the record measure 12 asks for.</p>
</div>
''',
 sources=[('ISO 22301:2019 - Business continuity management systems', None),
          ('ISO/TS 22317 - Guidelines for business impact analysis', None),
          ('Cybersecurity Regulation, OG 135/2024, Annex II, measure 12 (Croatian)', 'https://narodne-novine.nn.hr/clanci/sluzbeni/2024_11_135_2217.html')]))

ARTICLES_EN.append(dict(
 slug="dora-register-of-information", cat="DORA", catkey="dora",
 date="2026-06-16", read=7,
 title="The DORA register of information: it fails on data, not on the rules",
 lead="The register of contractual arrangements with ICT service providers looks like an administrative exercise until you try to populate it. That is when you discover three departments hold three different supplier lists, and none of them is complete.",
 desc="What DORA requires in the register of information on contractual arrangements with ICT service providers, why populating it stalls on data quality, and how to connect it to your existing asset and risk registers.",
 body='''
<p>Regulation (EU) 2022/2554 requires financial entities to maintain a <strong>register of information</strong> covering all contractual arrangements with ICT service providers, and to make it available to the competent authority on request. It sounds like a supplier list. It is not.</p>

<h2>What the register actually asks for</h2>
<p>The register is maintained at several levels and connects data that in most organisations lives in separate systems:</p>
<ul>
  <li><strong>The entity</strong> - who is the contracting party and where it sits in the group.</li>
  <li><strong>The provider</strong> - identification, country of establishment, parent undertaking.</li>
  <li><strong>The contractual arrangement</strong> - type, duration, termination notice, governing law.</li>
  <li><strong>The function</strong> the service supports, and whether that function is critical or important.</li>
  <li><strong>Subcontracting</strong> - the chain below the direct provider, to the depth that matters.</li>
  <li><strong>Location of data processing and storage.</strong></li>
  <li><strong>Substitutability assessment</strong> and the existence of an exit strategy.</li>
</ul>
<p>The operative word is <em>connects</em>. The register does not ask for a list but for the relationship between a contract, the function that contract supports, and the criticality of that function.</p>

<h2>Where population stalls</h2>
<div class="callout">
  <div class="c-label">Three data sources, three truths</div>
  <p>Procurement holds a list of contracts. IT holds a list of systems. Finance holds a list of suppliers being paid. In practice those three do not reconcile: there are systems without contracts, contracts without systems, and payments without either. Populating the register for the first time is usually the first time anyone puts the three lists side by side.</p>
</div>
<p>The second common blocker is <strong>subcontracting</strong>. The direct cloud provider is known. Who provides its infrastructure and where the data physically sits is known far less often, and contracts frequently do not oblige the provider to disclose it.</p>
<p>The third is <strong>determining function criticality</strong>. Without a BIA, criticality gets assessed ad hoc, per provider rather than per function. That is the wrong direction: the function is critical, and the provider inherits the property.</p>

<h2>How not to do it twice</h2>
<p>The register overlaps most with three things you already have, or should:</p>
<div class="tbl-wrap">
  <table>
    <thead><tr><th>The register asks for</th><th>Already exists in</th></tr></thead>
    <tbody>
      <tr><td>A list of ICT services and systems</td><td>The asset register (ISO 27001, measure 2)</td></tr>
      <tr><td>Function criticality</td><td>The business impact analysis (ISO 22301)</td></tr>
      <tr><td>Provider risk assessment</td><td>Third-party risk management (measure 8)</td></tr>
      <tr><td>Exit strategy</td><td>The business continuity plan</td></tr>
    </tbody>
  </table>
</div>
<p>An organisation that keeps those four as one connected set populates the register by running a report. An organisation that keeps them apart populates it by hand, every year, from scratch.</p>

<h2>What to do before populating</h2>
<ol>
  <li><strong>Reconcile the three lists.</strong> Procurement, IT and finance, on one shared identifier per provider.</li>
  <li><strong>Start from functions, not from suppliers.</strong> Determine which functions are critical or important, then attach services to them.</li>
  <li><strong>Check contracts for subcontracting disclosure.</strong> Where no such obligation exists, that is a finding in itself.</li>
  <li><strong>Mark where data is missing.</strong> An empty field with a justification beats a guess, and is easier to fix in the next cycle.</li>
</ol>

<div class="note">
  <p>DORA is the more specific regime for the financial sector, but it does not displace other obligations. The evidence base overlaps almost entirely with the Croatian Cybersecurity Regulation: the same asset register, the same risk register, the same incident records. Do the work once, report it in several directions.</p>
</div>
''',
 sources=[('Regulation (EU) 2022/2554 (DORA)', 'https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32022R2554'),
          ('Implementing technical standards on the register of information (ESAs)', 'https://www.eba.europa.eu/'),
          ('Cybersecurity Regulation, OG 135/2024, Annex II, measure 8 (Croatian)', 'https://narodne-novine.nn.hr/clanci/sluzbeni/2024_11_135_2217.html')]))

ARTICLES_EN.append(dict(
 slug="what-cyber-insurers-actually-ask", cat="Cyber insurance", catkey="insurance",
 date="2026-07-07", read=6,
 title="What cyber insurers actually ask before they quote",
 lead="A cyber insurance questionnaire is not a formality but a risk assessment somebody else is doing about you. The questions get more specific every year, and an inaccurate answer can become grounds for declining a claim.",
 desc="Which questions recur in cyber insurance questionnaires, why premium and cover are tied to specific controls, and how to use your existing compliance evidence in the negotiation.",
 body='''
<p>Over the past few years cyber insurance has moved from a product sold on a short questionnaire to a product underwritten after a technical assessment. The reason is simple: ransomware losses showed insurers they cannot price the risk without visibility into specific controls.</p>

<h2>The questions that recur</h2>
<p>Wording differs, but the substance converges. These are the areas that appear in almost every questionnaire:</p>
<h3>Authentication and access</h3>
<ul>
  <li>Is multi-factor authentication enabled for remote access, for email, and for administrator accounts? All three are asked separately.</li>
  <li>How many privileged accounts are there and how are they approved?</li>
  <li>Are there separate accounts for administrative tasks?</li>
</ul>
<h3>Backups</h3>
<ul>
  <li>Is there a copy that is unreachable from the production network?</li>
  <li>When was a restore last tested, and how long did it take?</li>
  <li>Are backups encrypted, and is access to them behind multi-factor authentication?</li>
</ul>
<h3>Detection and response</h3>
<ul>
  <li>Is there endpoint protection with detection and response capability?</li>
  <li>Are logs monitored, and by whom outside working hours?</li>
  <li>Is there an incident response plan, and has it been exercised?</li>
</ul>
<h3>Vulnerability management and supply chain</h3>
<ul>
  <li>How quickly are critical vulnerabilities patched on internet-facing systems?</li>
  <li>Who are the key suppliers and do they have access to your systems?</li>
  <li>Are there systems past vendor end-of-support?</li>
</ul>

<div class="callout">
  <div class="c-label">Why precision matters</div>
  <p>The questionnaire forms part of the contract. Answering "yes, we have multi-factor authentication" when it covers ninety per cent of users, and the attack comes through the other ten, opens an argument about whether the risk was accurately presented. A narrower answer with a caveat is always a better position than a broad one without.</p>
</div>

<h2>What lowers the premium, and what is a precondition</h2>
<p>It helps to separate two groups. Some controls affect price; others are a precondition for a quote existing at all. In recent years multi-factor authentication for remote access, an isolated backup copy and endpoint detection have all moved into the second group.</p>
<p>An organisation lacking those generally does not get a more expensive policy but no policy - or one with an exclusion covering precisely the scenario most likely to affect it.</p>

<h2>Using what you already have</h2>
<p>An organisation that has complied with the Croatian Cybersecurity Act or holds ISO 27001 already possesses nearly all the evidence the questionnaire asks for, only in a different format:</p>
<div class="tbl-wrap">
  <table>
    <thead><tr><th>The questionnaire asks for</th><th>You already have it in</th></tr></thead>
    <tbody>
      <tr><td>Critical asset list and unsupported systems</td><td>The asset register (measure 2)</td></tr>
      <tr><td>Patching and endpoint protection practice</td><td>Measure 5, cyber hygiene</td></tr>
      <tr><td>Access control and MFA</td><td>Measure 7</td></tr>
      <tr><td>Incident response plan and exercise records</td><td>Measure 11</td></tr>
      <tr><td>Restore tests</td><td>Measure 12 and the BIA</td></tr>
      <tr><td>Supplier risk assessment</td><td>Measure 8</td></tr>
    </tbody>
  </table>
</div>
<p>The practical consequence: negotiations go better when the questionnaire is accompanied by a compliance status report with scores per measure. To an underwriter that is stronger evidence than a column of yes answers, and it gives you a negotiating position on both premium and breadth of cover.</p>

<div class="note">
  <p>Insurance does not replace controls, and it does not cover regulatory consequences the way it covers direct loss. Administrative fines under cybersecurity and data protection law are excluded or capped in most policies - check that before a risk management plan comes to rely on the policy.</p>
</div>
''',
 sources=[('NIST Cybersecurity Framework 2.0', 'https://www.nist.gov/cyberframework'),
          ('Cybersecurity Regulation, OG 135/2024, Annex II (Croatian)', 'https://narodne-novine.nn.hr/clanci/sluzbeni/2024_11_135_2217.html'),
          ('ISO/IEC 27001:2022, Annex A', None)]))

ARTICLES_EN.append(dict(
 slug="nist-csf-2-govern-function", cat="Frameworks", catkey="frameworks",
 date="2026-07-28", read=6,
 title="NIST CSF 2.0 and the Govern function: a framework that finally named the board",
 lead="Version 2.0 added a sixth function above all the others. It is not cosmetic - Govern answers a finding that kept recurring for years: technical controls do not fix an organisation with no owner for its risk.",
 desc="What the Govern function brings to NIST Cybersecurity Framework 2.0, how the six functions map to the 13 measures of the Croatian Cybersecurity Regulation, and why the framework is worth using as a common language with the board.",
 body='''
<p>The NIST Cybersecurity Framework had five functions for a long time: identify, protect, detect, respond and recover. Version 2.0 added a sixth - <strong>Govern</strong> - and did not place it alongside the others but above them.</p>

<h2>What Govern covers</h2>
<p>The function covers what used to be assumed and was therefore rarely done:</p>
<ul>
  <li><strong>Organizational context</strong> - mission, stakeholders, legal and regulatory obligations.</li>
  <li><strong>Risk management strategy</strong> - risk appetite and tolerance, expressed so decisions can actually be made against them.</li>
  <li><strong>Roles and responsibilities</strong> - who decides, who implements, who reports.</li>
  <li><strong>Policy</strong> - established, communicated and maintained.</li>
  <li><strong>Oversight</strong> - reviewing outcomes and adjusting the strategy.</li>
  <li><strong>Supply chain risk management</strong> - raised to governance level rather than procurement.</li>
</ul>
<div class="callout">
  <div class="c-label">Why this is a change, not an addition</div>
  <p>In version 1.1 risk appetite was implicit. That meant decisions to accept risk were being taken by people not accountable for them - usually IT, because IT was the only function with the data. Govern puts that back with the board, explicitly.</p>
</div>

<h2>How it relates to Croatian obligations</h2>
<p>The framework is not law and nobody in Croatia requires it. It is useful for a different reason: it is a common language. A board that does not understand sub-measure 1.3 does understand the question "how capable are we of detecting an attack?"</p>
<p>The mapping is more direct than it appears:</p>
<div class="tbl-wrap">
  <table>
    <thead><tr><th>CSF 2.0 function</th><th>Corresponds to measures</th></tr></thead>
    <tbody>
      <tr><td><strong>Govern</strong></td><td>1 (commitment and accountability), 3 (risk management), 8 (supply chain)</td></tr>
      <tr><td><strong>Identify</strong></td><td>2 (assets), 3 (risk)</td></tr>
      <tr><td><strong>Protect</strong></td><td>4, 5, 6, 7, 9, 10, 13</td></tr>
      <tr><td><strong>Detect</strong></td><td>6 (network monitoring), 11 (incident detection)</td></tr>
      <tr><td><strong>Respond</strong></td><td>11 (incident handling)</td></tr>
      <tr><td><strong>Recover</strong></td><td>12 (continuity and crisis)</td></tr>
    </tbody>
  </table>
</div>
<p>The same mapping exists towards ISO/IEC 27002:2022, because its control attributes use exactly the identify, protect, detect, respond and recover concepts. Three frameworks, one evidence base.</p>

<h2>Where the framework genuinely helps</h2>
<p>Not as a substitute for compliance, but as a tool for three things:</p>
<ol>
  <li><strong>Board reporting.</strong> Six functions fit on one slide. Ninety-nine sub-measures do not.</li>
  <li><strong>Setting a target profile.</strong> The framework distinguishes current and target profiles, which is a better way to discuss budget than a list of deficiencies.</li>
  <li><strong>Comparison over time.</strong> A profile, once set, produces a trend - and a trend is the only thing a board cares about more than the current state.</li>
</ol>

<h2>The trap to avoid</h2>
<p>The framework describes outcomes, not controls. "Supply chain risks are identified and recorded" is an outcome - how you achieve it is not prescribed. That is its strength when used for governance, and its weakness when someone tries to use it as a task list.</p>
<p>Organisations that attempt to implement CSF instead of the Regulation end up with a good overview and no evidence base. The order that works is the reverse: implement the measures, then present the result through the six functions.</p>

<div class="note">
  <p>NIST published implementation examples alongside version 2.0, attaching concrete activities to each outcome. That is the most useful part of the documentation for a first-time user, and the most commonly skipped.</p>
</div>
''',
 sources=[('NIST Cybersecurity Framework 2.0', 'https://www.nist.gov/cyberframework'),
          ('NIST CSF 2.0 Implementation Examples', 'https://www.nist.gov/cyberframework'),
          ('ISO/IEC 27002:2022 - control attributes', None)]))

ARTICLES_EN.append(dict(
 slug="active-directory-attack-paths", cat="Offensive security", catkey="offensive",
 date="2026-08-18", read=7,
 title="Active Directory: five findings we see in almost every assessment",
 lead="Domain infrastructure rarely falls to an unpatched vulnerability. It falls to configuration that once made sense, was left behind, and that nobody looks at any more. These five findings show up in most environments.",
 desc="The most common findings in Active Directory security assessments: legacy protocols, excessive delegation, passwords in attributes, stale privileged group membership, and access to domain backups.",
 body='''
<p>When a domain infrastructure assessment is commissioned, the client usually expects the finding to be an unpatched server. In practice, the most common path from an ordinary user account to full control of the domain is assembled from configurations that are not vulnerabilities but decisions - taken long ago, for a good reason that no longer holds.</p>
<p>These five recur most often.</p>

<h2>1. Legacy protocols nobody uses but that are still enabled</h2>
<p>Local name resolution protocols left enabled because one application once needed them. The result is that an attacker on the network can induce clients to send authentication material, without a single exploit.</p>
<p><strong>Check:</strong> are legacy name resolution protocols and older file sharing dialects disabled, and is traffic signing required? <strong>Obstacle:</strong> almost always one old application nobody wants to touch.</p>

<h2>2. Delegation that is broader than anyone realises</h2>
<p>Delegation lets an account act on behalf of a user. Configured without constraints, it means compromising one server grants access to everything the users who connected to it can reach.</p>
<p><strong>Check:</strong> which accounts have unconstrained delegation, and is any of them user-facing? <strong>Fix:</strong> move to constrained delegation and flag sensitive accounts as not delegatable.</p>

<div class="callout">
  <div class="c-label">The common denominator</div>
  <p>None of these findings appears as critical in a vulnerability scanner report. All of them only become visible when you look at relationships between objects rather than the state of an individual server. That is why a domain assessment is not the same thing as a network scan.</p>
</div>

<h2>3. Passwords in attributes and scripts</h2>
<p>Descriptive attributes on objects are readable by any authenticated user. Service account passwords regularly turn up in them, entered for convenience. The same applies to scripts in shared folders that execute at logon.</p>
<p><strong>Check:</strong> search attributes and shared folders for strings that look like passwords. The result is rarely empty.</p>

<h2>4. Privileged membership that survived a job change</h2>
<p>An administrator who solved one problem three years ago, was added to a privileged group and never removed. Or a service account for a decommissioned application that remains active with domain administrator rights.</p>
<p><strong>Check:</strong> how many accounts are in the most privileged groups, when did each last log on, and who owns it? <strong>Typical finding:</strong> the member count is in double digits and the number who genuinely need those rights is in single digits.</p>

<h2>5. Domain backups reachable from the domain</h2>
<p>A copy of the domain database contains everything. If it sits on a share accessible to ordinary server administrators, the path to full control runs through it - without a single attack on a domain controller itself.</p>
<p><strong>Check:</strong> who has access to backups, are they encrypted, and is a copy reachable from the production domain? This is also the most direct link to measure 12 - a backup that ransomware can reach is not a backup.</p>

<h2>Connecting this to your obligations</h2>
<p>All five findings belong to measures in Annex II of the Croatian Cybersecurity Regulation, and specifically to those most often self-assessed as implemented:</p>
<ul>
  <li>Legacy protocols and configuration - measure 6, network security</li>
  <li>Delegation and privileged membership - measure 7, access control</li>
  <li>Passwords in attributes - measure 4, digital identities</li>
  <li>Access to backups - measures 5 and 12</li>
</ul>
<p>That is why a technical assessment and a compliance assessment should not be separate projects. A document asserting that access control is established, alongside a finding of seventeen domain administrators, does not survive serious scrutiny.</p>

<div class="note">
  <p>A domain security assessment is carried out under written authorisation and within an agreed scope. All the checks above can be run against a production domain without interrupting service, but they do leave traces in monitoring - agree them with the team watching the logs, or your first finding will be your own test.</p>
</div>
''',
 sources=[('Cybersecurity Regulation, OG 135/2024, Annex II, measures 4, 6, 7 and 12 (Croatian)', 'https://narodne-novine.nn.hr/clanci/sluzbeni/2024_11_135_2217.html'),
          ('ISO/IEC 27002:2022 - technological controls', None),
          ('NIST Cybersecurity Framework 2.0 - Protect and Detect functions', 'https://www.nist.gov/cyberframework')]))

# ══════════════════════════════════════════════════════════════════
# Engleski: serija o umjetnoj inteligenciji
# ══════════════════════════════════════════════════════════════════
ARTICLES_EN.append(dict(
 slug="ai-act-risk-levels", cat="Artificial intelligence", catkey="ai",
 date="2026-06-02", read=7,
 title="The AI Act: four risk levels and the question that comes first",
 lead="Regulation (EU) 2024/1689 does not govern the technology but its application. The same model can be an unregulated convenience and a high-risk system, depending on what you use it for - which means classification starts with an inventory, not a legal analysis.",
 desc="How the EU AI Act divides systems into four risk levels, what makes a system high-risk, and why classification has to start from an inventory of the AI systems in your organisation.",
 body='''
<p>Regulation (EU) 2024/1689, the AI Act, is the first comprehensive law of its kind. Its approach is simpler than the length of the text suggests: <strong>obligations do not depend on what kind of model it is, but on what it is used for and who it can harm.</strong></p>

<h2>Four levels</h2>
<div class="tbl-wrap">
  <table>
    <thead><tr><th>Level</th><th>What it covers</th><th>Consequence</th></tr></thead>
    <tbody>
      <tr><td><strong>Unacceptable risk</strong></td><td>Prohibited practices</td><td>Cannot be used</td></tr>
      <tr><td><strong>High risk</strong></td><td>Systems in sensitive areas of use and safety components of products</td><td>The largest set of obligations</td></tr>
      <tr><td><strong>Limited risk</strong></td><td>Systems that interact with people or generate content</td><td>Transparency duties</td></tr>
      <tr><td><strong>Minimal risk</strong></td><td>Everything else</td><td>No specific obligations</td></tr>
    </tbody>
  </table>
</div>
<p>Most of what organisations use day to day lands in the bottom two categories. That does not mean there is no work - it means the work is different.</p>

<div class="callout">
  <div class="c-label">Same technology, different level</div>
  <p>A model that drafts text is minimal risk when it summarises a meeting and high risk when it is used to shortlist job applicants. Classification is done per use case, not per tool. An organisation with one tool and ten ways of using it has ten items to assess, not one.</p>
</div>

<h2>Why you start with an inventory</h2>
<p>The first question is not "is this high risk". The first question is <strong>which systems are we actually using</strong>. The answer is almost always incomplete, for three reasons:</p>
<ul>
  <li><strong>Embedded features.</strong> Existing business software acquires AI functionality through an update, without a procurement decision.</li>
  <li><strong>Tools introduced by staff.</strong> The free tier of a tool someone uses to prepare documents passes through neither procurement nor IT.</li>
  <li><strong>Supplier services.</strong> An external provider processing your data with the help of AI introduces it into your chain without a decision on your part.</li>
</ul>
<p>The inventory is therefore not obtained by asking IT but by the same method used to build an asset register: walking the processes and talking to their owners.</p>

<h2>Your role determines your obligations</h2>
<p>The Act distinguishes roles, and the most important distinction is between whoever develops and places a system on the market and whoever uses it. Most organisations sit in the second group, with a substantially lighter set of obligations - but not with none.</p>
<p>That role can change through an incautious step, however. An organisation that takes someone else's system, puts its own name on it or substantially modifies it may take on the heavier obligations as well. Which is why a decision to fine-tune a model is not purely technical.</p>

<h2>What to do now</h2>
<ol>
  <li><strong>Build the inventory.</strong> System, owner, use case, data going in, decision it influences.</li>
  <li><strong>Flag use cases that touch people.</strong> Recruitment, evaluation, access to services, employee monitoring - those are the areas where the level rises.</li>
  <li><strong>Check the input data.</strong> If personal data goes in, the GDPR applies in parallel, with its own requirements for a lawful basis and impact assessment.</li>
  <li><strong>Set the rules before you need them.</strong> An internal usage policy, with a clear list of what must not be entered into external tools, will prevent more problems than any subsequent analysis.</li>
</ol>

<div class="note">
  <p>The AI Act applies in stages, with provisions taking effect at different dates. Prohibited practices and the AI literacy obligation apply first, obligations for high-risk systems later. Check which date applies to your situation before planning a project timeline.</p>
</div>
''',
 sources=[('Regulation (EU) 2024/1689 (AI Act)', 'https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689'),
          ('Regulation (EU) 2016/679 (GDPR)', 'https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679')]))

ARTICLES_EN.append(dict(
 slug="prohibited-practices-and-ai-literacy", cat="Artificial intelligence", catkey="ai",
 date="2026-06-30", read=6,
 title="Prohibited practices and AI literacy: two provisions already in force",
 lead="While the debate runs on high-risk systems, two provisions of the AI Act apply first. One bans certain practices outright, the other requires that the people using these systems know what they are doing.",
 desc="Which practices the AI Act prohibits outright, what the AI literacy obligation in Article 4 means, and how to satisfy it without building a separate training programme.",
 body='''
<p>The AI Act applies in stages. Two groups of provisions arrive first, and both apply to anyone using these systems, not only to those building them.</p>

<h2>Prohibited practices</h2>
<p>Article 5 lists practices that must not be used, with no risk assessment available and no way to justify them. Among them:</p>
<ul>
  <li><strong>Manipulative techniques</strong> that materially impair a person's ability to make an informed decision and thereby cause significant harm.</li>
  <li><strong>Exploiting vulnerabilities</strong> arising from age, disability or a social or economic situation.</li>
  <li><strong>Social scoring</strong> leading to detrimental treatment in a context unrelated to the one in which the data was collected.</li>
  <li><strong>Predicting criminal offences</strong> based solely on profiling or personality traits.</li>
  <li><strong>Untargeted scraping of facial images</strong> from the internet or CCTV to build recognition databases.</li>
  <li><strong>Emotion recognition in the workplace and in education</strong>, subject to narrow medical and safety exceptions.</li>
  <li><strong>Biometric categorisation</strong> to infer sensitive attributes about a person.</li>
</ul>
<div class="callout">
  <div class="c-label">Where this touches ordinary business</div>
  <p>Most of the prohibitions sound remote from an average company until you look at two entries. Emotion recognition in the workplace appears in call analytics tools for contact centres and in employee engagement monitoring. Biometric categorisation appears in video surveillance analytics. Neither is procured under that name.</p>
</div>

<h2>The AI literacy obligation</h2>
<p>Article 4 requires organisations to ensure a sufficient level of AI literacy among staff and others operating AI systems on their behalf. The level is set against those people's technical knowledge, experience and education, and against the context in which the systems are used.</p>
<p>The provision is short and deliberately open. It prescribes no hours, no curriculum and no exam. It requires that people understand what the tool does, where it fails, and what must not be done with it.</p>

<h3>How to satisfy it without a separate programme</h3>
<p>In organisations that already run security awareness training, this is an addition rather than a new project:</p>
<ol>
  <li><strong>An internal usage policy</strong> - what may and may not be entered into external tools. This is the shortest path to the largest benefit.</li>
  <li><strong>Short role-based training.</strong> Someone using a tool to draft text and someone using it in decisions about people do not need the same content.</li>
  <li><strong>Concrete failure examples.</strong> Fabricated facts presented convincingly, bias in training data, a model's misplaced confidence.</li>
  <li><strong>Records.</strong> Who completed what and when. Without records the obligation cannot be verified, exactly as with cybersecurity measures.</li>
</ol>

<h2>Overlap with other obligations</h2>
<p>The training record produced here simultaneously feeds measure 5 of the Croatian Cybersecurity Regulation, which requires staff awareness. The internal usage policy touches data protection as well, since entering personal data into an external tool is processing with its own lawful basis.</p>
<p>This is the general pattern: the instruments differ, the evidence base is shared.</p>

<div class="note">
  <p>This text is an informative overview, not legal advice. The precise scope of prohibited practices and the way the literacy obligation applies depend on the specific circumstances and on guidance issued at Union level.</p>
</div>
''',
 sources=[('Regulation (EU) 2024/1689 (AI Act), Art. 4 and 5', 'https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689'),
          ('Cybersecurity Regulation, OG 135/2024, Annex II, measure 5 (Croatian)', 'https://narodne-novine.nn.hr/clanci/sluzbeni/2024_11_135_2217.html')]))

ARTICLES_EN.append(dict(
 slug="ai-inventory-and-asset-register", cat="Artificial intelligence", catkey="ai",
 date="2026-07-14", read=6,
 title="The AI system inventory and the asset register: why they are one list",
 lead="Organisations that introduce an AI system inventory as a separate document discover a year later that they have two registers drifting apart. The overlap is larger than the difference, and the difference fits into four columns.",
 desc="How to extend an existing information asset register so it covers the AI Act's inventory requirements, instead of maintaining a separate register of AI systems.",
 body='''
<p>When an AI-related obligation arrives, the usual first move is to open a new spreadsheet. The logic is understandable: new instrument, new document. The consequence is predictable.</p>
<p>A year later there are two lists. One knows about every server but not which of them runs a model. The other knows about the models but not who owns the system they run on. Neither is complete and nobody knows which is more recent.</p>

<h2>What both registers ask for identically</h2>
<div class="tbl-wrap">
  <table>
    <thead><tr><th>Data point</th><th>Asset register</th><th>AI inventory</th></tr></thead>
    <tbody>
      <tr><td>System name and description</td><td>yes</td><td>yes</td></tr>
      <tr><td>Owner</td><td>yes</td><td>yes</td></tr>
      <tr><td>Business process supported</td><td>yes</td><td>yes</td></tr>
      <tr><td>Criticality</td><td>yes</td><td>yes</td></tr>
      <tr><td>Types of data processed</td><td>yes</td><td>yes</td></tr>
      <tr><td>Supplier and contract</td><td>yes</td><td>yes</td></tr>
      <tr><td>Processing location</td><td>yes</td><td>yes</td></tr>
      <tr><td>Risk assessment</td><td>yes</td><td>yes</td></tr>
    </tbody>
  </table>
</div>
<p>Eight entries you are maintaining anyway. Measure 2 of Annex II of the Croatian Cybersecurity Regulation requires an asset inventory with classification and identification of critical assets - that is the same job.</p>

<h2>The four columns you add</h2>
<ol>
  <li><strong>Is the system AI-based</strong> - yes, no, or contains an embedded component. The third value matters, because it captures existing software that acquired AI functionality through an update.</li>
  <li><strong>Use case</strong> - specifically, not "assistant". The same tool used three ways produces three rows.</li>
  <li><strong>Your role</strong> - are you using the system, developing it, or have you modified it and put your name on it. This determines the scope of your obligations.</li>
  <li><strong>Risk level and reasoning</strong> - the conclusion of the assessment, with a sentence saying why. The sentence matters more than the label.</li>
</ol>

<div class="callout">
  <div class="c-label">Why use case, not tool</div>
  <p>Obligations under the AI Act depend on application, not technology. A register with one row per tool cannot carry a classification, because the same tool can be minimal and high risk at the same time. One row per use case solves this without a single additional table.</p>
</div>

<h2>What you gain beyond tidiness</h2>
<ul>
  <li><strong>Risk assessment happens once.</strong> The risk of losing system availability and the risk of a wrong decision the system produces are assessed in the same register, with the same methodology and the same owner.</li>
  <li><strong>The supply chain is covered.</strong> An AI service provider is a third party like any other, entering the assessment under measure 8 with no separate procedure.</li>
  <li><strong>Data protection attaches at the same place.</strong> Where personal data goes in, the link to the record of processing activities runs through the same row.</li>
  <li><strong>Monitoring has one source.</strong> Log collection and behaviour monitoring rely on the inventory - a system that is not in the inventory is not under monitoring either.</li>
</ul>

<h2>The first step, concretely</h2>
<p>Open your existing asset register, add four columns and walk the list. For most rows the answer to the first question is "no" and the work is done in a minute. The rows answering "yes" or "contains a component" will be fewer than expected, and they are precisely the ones needing attention.</p>
<p>What you will be missing is not systems from IT but tools introduced by staff and AI features that arrived through an update of existing software. Those are not found in a spreadsheet but in a conversation with process owners.</p>

<div class="note">
  <p>The same principle applies to the DORA register of information and to the GDPR record of processing activities. Each asks for a view of the same assets from a different angle. Organisations that maintain them as views on one source report; those that maintain them separately transcribe.</p>
</div>
''',
 sources=[('Regulation (EU) 2024/1689 (AI Act)', 'https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689'),
          ('Cybersecurity Regulation, OG 135/2024, Annex II, measures 2 and 8 (Croatian)', 'https://narodne-novine.nn.hr/clanci/sluzbeni/2024_11_135_2217.html'),
          ('ISO/IEC 27001:2022, Annex A - asset management', None)]))

ARTICLES_EN.append(dict(
 slug="ai-in-defence-where-it-helps", cat="Artificial intelligence", catkey="ai",
 date="2026-08-04", read=7,
 title="AI in defence: where it genuinely helps and where it just moves the problem",
 lead="The promise is that a model will catch the attack a human missed. The reality is that models do well on tasks with many examples and a clear outcome, and badly where neither exists - which is exactly where the expensive failures live.",
 desc="A realistic assessment of applying AI in cyber defence: where it delivers measurable benefit, where it creates false confidence, and which controls to put in place before adopting it.",
 body='''
<p>The debate about AI in security quickly slides into two extremes: that it changes everything, or that it changes nothing. It is more useful to ask where a statistical model has an advantage over a rule, and where it does not.</p>

<h2>Where it delivers measurable benefit</h2>
<h3>Reducing noise</h3>
<p>Grouping similar alerts, removing duplicates and ranking by likelihood of a genuine finding. That is a task with many examples and a clear outcome, and models do it well. The benefit is not that the model detects attacks but that the analyst does not spend a day on a thousand alerts of which nine hundred are the same event.</p>
<h3>Detecting deviation from normal</h3>
<p>A login at three in the morning from a country where the organisation does not operate, or an account suddenly accessing ten times more files than usual. The model learns what is normal and flags what is not. It works well where "normal" is stable and poorly in environments that change constantly.</p>
<h3>Accelerating comprehension</h3>
<p>Summarising logs, explaining an unfamiliar command, proposing a query over the data. Here the model does not decide but shortens the time to understanding, with a human verifying.</p>
<h3>Preparing documentation</h3>
<p>A draft incident report, a proposed policy structure, a comparison of an existing document against a standard's requirements. With mandatory review, this is currently the highest-return application in compliance work.</p>

<div class="callout">
  <div class="c-label">What all the useful applications share</div>
  <p>The model shortens the path to an answer, but a human confirms the answer. The moment that confirmation is removed for speed, the benefit turns into a risk - and one that stays invisible until it materialises.</p>
</div>

<h2>Where it moves the problem instead of solving it</h2>
<h3>When the cause is organisational</h3>
<p>A system that ranks alerts does not help an organisation where nobody looks at alerts outside working hours anyway. Detection without response is not defence, and a tool does not create an on-call rota.</p>
<h3>When there is no data</h3>
<p>Models learn from records. An organisation not collecting logs from all key sources will not get useful results - it will get convincing results on incomplete data, which is worse.</p>
<h3>When output is taken as fact</h3>
<p>Language models produce convincing text even with no basis for it. A vulnerability name that does not exist, an invented article of a regulation, a configuration parameter that never existed - all of it arrives in the same tone as the correct answer.</p>
<h3>When sensitive data leaves</h3>
<p>Analysing an incident in an external tool means logs, system names and sometimes client data have left the organisation. That is processing with its own legal consequences, and it happens most often under the pressure of an incident.</p>

<h2>The attacker's side</h2>
<p>The same technology lowered the bar for attackers in three concrete ways: phishing without language errors and tailored to the recipient, faster preparation of malware variants, and convincing voice impersonation in payment fraud.</p>
<p>None of these is a new class of attack. All are existing attacks executed more cheaply and more convincingly. Which is why the defence is not a new tool but tightening controls that already exist - out-of-band payment confirmation, multi-factor authentication, and awareness training that can no longer teach people to spot phishing by its bad grammar.</p>

<h2>What to put in place before adopting</h2>
<ol>
  <li><strong>Enter the system in the asset register</strong>, with an owner and a use case.</li>
  <li><strong>Define what must not go in.</strong> Personal data, client data, configurations, logs containing system names.</li>
  <li><strong>Keep a human in the decision</strong> everywhere the output affects people or service availability.</li>
  <li><strong>Record what the model proposed and what the human decided.</strong> Without that record there is neither review nor learning from mistakes.</li>
  <li><strong>Measure.</strong> If time to detection or time to response does not improve after adoption, the tool did not deliver what it was bought for.</li>
</ol>

<div class="note">
  <p>The AI Act applies the same logic to security tools as to everything else: obligations follow the application. A tool that ranks alerts is generally low risk, but a tool that automatically blocks a user is making a decision about a person - and that changes the assessment.</p>
</div>
''',
 sources=[('Regulation (EU) 2024/1689 (AI Act)', 'https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689'),
          ('NIST Cybersecurity Framework 2.0 - Detect and Respond functions', 'https://www.nist.gov/cyberframework'),
          ('Recommendations for systematic log collection, NCSC-HR (Croatian)', 'https://www.ncsc.hr/')]))

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
# ALATI
# ══════════════════════════════════════════════════════════════════
TOOLS_T = {
 "hr": dict(
   hub="/alati/", hub_name="Alati", slug="rokovi-prijave-incidenta",
   hub_h1="Alati koji rade posao, a ne samo objašnjavaju ga",
   hub_intro="Besplatni alati za obveznike Zakona o kibernetičkoj sigurnosti. Rade u pregledniku, ne traže registraciju i ne šalju vaše podatke nikamo.",
   hub_desc="Besplatni alati za usklađenost sa ZKS-om: kalkulator rokova prijave značajnog incidenta i drugi alati u pripremi.",
   soon="Uskoro",
   t_name="Kalkulator rokova prijave incidenta",
   t_desc="Unesite trenutak saznanja za značajan incident i dobijete svih pet rokova s točnim datumima, uključujući usporednu prijavu AZOP-u.",
   t_title="Kalkulator rokova prijave značajnog incidenta",
   t_lead="Rokovi prema Zakonu o kibernetičkoj sigurnosti ne zbrajaju se i ne teku jedan za drugim. Unesite trenutak saznanja i alat izračuna svih pet obavijesti s točnim datumom i vremenom.",
   t_desc_meta="Besplatan kalkulator rokova prijave značajnog incidenta prema ZKS-u: rano upozorenje 24 h, početna obavijest 72 h, privremeno izvješće, završno izvješće 30 dana i usporedna prijava AZOP-u.",
   soon2_name="Provjera kategorizacije subjekta",
   soon2_desc="Sektor, veličina i djelatnost daju vjerojatnu kategoriju subjekta i popis obveza koje iz nje slijede.",
   soon3_name="Mini samoprocjena po 13 mjera",
   soon3_desc="Kratka procjena spremnosti po svakoj od 13 mjera iz Priloga II. Uredbe, s grafom i pragom spremnosti.",
   f_when="Trenutak saznanja za značajan incident",
   f_when_sub="Rokovi teku od saznanja, ne od nastanka incidenta i ne od završetka istrage.",
   f_sent="Trenutak dostave početne obavijesti",
   f_sent_sub="Ako je već poslana, upišite je. Rok za završno izvješće teče od nje. Ako je ostavite praznu, računa se od isteka roka od 72 sata.",
   f_tsp="Subjekt je pružatelj usluga povjerenja",
   f_tsp_sub="Prema čl. 68. Uredbe, ne dostavlja rano upozorenje, nego početnu obavijest u roku od 24 sata.",
   f_gdpr="Incident uključuje i povredu osobnih podataka",
   f_gdpr_sub="Dodaje usporedni rok prijave Agenciji za zaštitu osobnih podataka prema čl. 33. Opće uredbe.",
   btn_calc="Izračunaj rokove", btn_reset="Poništi", btn_copy="Kopiraj sažetak", btn_print="Ispiši",
   copied="Sažetak kopiran",
   res_h="Vaši rokovi", res_sub="Računato od trenutka saznanja",
   err_date="Unesite trenutak saznanja za incident.",
   d1="Rano upozorenje", d1_d="Nadležnom CSIRT-u, bez odgode. Ne treba objašnjavati incident, nego javiti da se dogodio.",
   d2="Početna obavijest", d2_d="Ažurirana procjena, pokazatelji ugroženosti, ozbiljnost i utjecaj.",
   d3="Privremeno izvješće", d3_d="Samo na zahtjev nadležnog CSIRT-a, u roku koji on odredi.",
   d3_when="48 sati do 7 dana od zahtjeva",
   d4="Završno izvješće", d4_d="Detaljan opis, vrsta prijetnje i temeljni uzrok, primijenjene i planirane mjere.",
   d5="Izvješće o napretku", d5_d="Ako incident još traje kad istekne rok za završno izvješće, umjesto njega ide izvješće o napretku, pa svakih idućih 30 dana.",
   d6="Prijava AZOP-u", d6_d="Usporedno s rokovima iz ZKS-a, prema čl. 33. Opće uredbe o zaštiti podataka.",
   d1_tsp_note="Ne primjenjuje se - pružatelji usluga povjerenja ne dostavljaju rano upozorenje.",
   left_over="rok je istekao", left_h="preostalo %d h %d min", left_d="preostalo %d dana %d h",
   left_from="od dostave početne obavijesti",
   note="Prijava se predaje na platformi PiXi (pixi.carnet.hr), pristup preko sustava NIAS. Ako platforma nije dostupna, obavijest se šalje obrascem na adresu nadležnog CSIRT-a, a podaci se naknadno unose u platformu. Nadležnost CSIRT-a određuje se prema sektoru, sukladno Prilogu III. Zakona.",
   disclaimer="Alat je informativno pomagalo i ne zamjenjuje pravni savjet ni službene smjernice. Rokovi se računaju prema čl. 65. do 71. Uredbe o kibernetičkoj sigurnosti. Provjerite kriterije značajnosti iz čl. 59. do 62. Uredbe prije prijave.",
   more="Više o obvezi prijave",
   more_url="/blog/znacajan-incident-pet-obavijesti-pixi/",
   privacy_note="Alat radi isključivo u vašem pregledniku. Unesenih podataka nema na našem poslužitelju.",
   summary_h="ROKOVI PRIJAVE ZNAČAJNOG INCIDENTA",
   summary_from="Saznanje:",
 ),
 "en": dict(
   hub="/en/tools/", hub_name="Tools", slug="incident-reporting-deadlines",
   hub_h1="Tools that do the work, not just explain it",
   hub_intro="Free tools for entities in scope of the Croatian Cybersecurity Act. They run in your browser, require no sign-up, and send your data nowhere.",
   hub_desc="Free compliance tools: a deadline calculator for reporting significant cyber incidents under the Croatian Cybersecurity Act, and more in preparation.",
   soon="Coming soon",
   t_name="Incident reporting deadline calculator",
   t_desc="Enter the moment you became aware of a significant incident and get all five deadlines with exact dates, including the parallel GDPR notification.",
   t_title="Incident reporting deadline calculator",
   t_lead="Deadlines under the Croatian Cybersecurity Act do not add up and do not run one after another. Enter the moment of awareness and the tool computes all five notifications with exact date and time.",
   t_desc_meta="Free calculator for significant incident reporting deadlines under the Croatian Cybersecurity Act: early warning 24 h, incident notification 72 h, intermediate report, final report 30 days and the parallel GDPR notification.",
   soon2_name="Entity categorisation check",
   soon2_desc="Sector, size and activity produce a likely entity category and the obligations that follow from it.",
   soon3_name="Readiness check against the 13 measures",
   soon3_desc="A short readiness assessment against each of the 13 measures of Annex II, with a chart and a readiness threshold.",
   f_when="Moment of becoming aware of a significant incident",
   f_when_sub="Deadlines run from awareness, not from when the incident occurred and not from when the investigation ends.",
   f_sent="Moment the incident notification was delivered",
   f_sent_sub="If already sent, enter it. The final report deadline runs from it. Leave blank and it is computed from the 72-hour deadline.",
   f_tsp="The entity is a trust service provider",
   f_tsp_sub="Under Art. 68 of the Regulation, no early warning is submitted; the incident notification is due within 24 hours instead.",
   f_gdpr="The incident also involves a personal data breach",
   f_gdpr_sub="Adds the parallel notification to the data protection authority under Art. 33 GDPR.",
   btn_calc="Calculate deadlines", btn_reset="Reset", btn_copy="Copy summary", btn_print="Print",
   copied="Summary copied",
   res_h="Your deadlines", res_sub="Calculated from the moment of awareness",
   err_date="Enter the moment you became aware of the incident.",
   d1="Early warning", d1_d="To the competent CSIRT, without delay. It does not explain the incident, it reports that one occurred.",
   d2="Incident notification", d2_d="Updated assessment, indicators of compromise, severity and impact.",
   d3="Intermediate report", d3_d="Only on request of the competent CSIRT, within the period it sets.",
   d3_when="48 hours to 7 days from the request",
   d4="Final report", d4_d="Detailed description, threat type and root cause, measures applied and planned.",
   d5="Progress report", d5_d="If the incident is still ongoing when the final report falls due, a progress report is submitted instead, and every 30 days thereafter.",
   d6="Data protection notification", d6_d="Runs in parallel with the deadlines under the Act, under Art. 33 GDPR.",
   d1_tsp_note="Not applicable - trust service providers do not submit an early warning.",
   left_over="deadline passed", left_h="%d h %d min left", left_d="%d days %d h left",
   left_from="from delivery of the incident notification",
   note="Notifications are submitted through the PiXi platform (pixi.carnet.hr), accessed via the national identification system. If the platform is unavailable, the notification is sent by form to the competent CSIRT and entered into the platform afterwards. CSIRT competence follows the sector, under Annex III of the Act.",
   disclaimer="This tool is an informative aid and does not replace legal advice or official guidance. Deadlines follow Art. 65 to 71 of the Cybersecurity Regulation. Check the significance criteria in Art. 59 to 62 before reporting.",
   more="More on the reporting obligation",
   more_url="/en/blog/incident-reporting-deadlines/",
   privacy_note="The tool runs entirely in your browser. Nothing you enter reaches our server.",
   summary_h="SIGNIFICANT INCIDENT REPORTING DEADLINES",
   summary_from="Awareness:",
 ),
}

TOOL_ICONS = {
 "clock": '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/></svg>',
 "split": '<svg viewBox="0 0 24 24"><path d="M3 5h5l4 7 4-7h5M3 19h5l4-7"/><circle cx="20" cy="19" r="2"/></svg>',
 "chart": '<svg viewBox="0 0 24 24"><path d="M3 20h18M7 20V10M12 20V4M17 20v-7"/></svg>',
}


def build_tools(lang, articles):
    t = L[lang]
    w = TOOLS_T[lang]
    FOOT = footer(lang, articles)
    out_dir = os.path.join(ROOT, "en", "tools") if lang == "en" else os.path.join(ROOT, "alati")
    os.makedirs(os.path.join(out_dir, w["slug"]), exist_ok=True)

    hr_hub, en_hub = SITE + "/alati/", SITE + "/en/tools/"

    # ── Hub ───────────────────────────────────────────────────────
    cards = '''      <a class="tool-card" href="%s%s/">
        <div class="tool-icon">%s</div>
        <div class="tool-name">%s</div>
        <div class="tool-desc">%s</div>
        <span class="tool-tag">%s</span>
      </a>''' % (w["hub"], w["slug"], TOOL_ICONS["clock"], w["t_name"], w["t_desc"],
                 "ZKS / NIS2" if lang == "hr" else "CSA / NIS2")
    for icon, nm, ds in [("split", w["soon2_name"], w["soon2_desc"]), ("chart", w["soon3_name"], w["soon3_desc"])]:
        cards += '''
      <div class="tool-card soon">
        <div class="tool-icon">%s</div>
        <div class="tool-name">%s</div>
        <div class="tool-desc">%s</div>
        <span class="tool-tag grey">%s</span>
      </div>''' % (TOOL_ICONS[icon], nm, ds, w["soon"])

    hub_body = header(lang, active_blog=False) + '''
<main>
  <section class="kb-hero">
    <div class="container">
      <div class="eyebrow">%s</div>
      <h1>%s</h1>
      <p>%s</p>
    </div>
  </section>
  <div class="container">
    <div class="tool-grid">
%s
    </div>
  </div>
</main>
''' % (w["hub_name"], w["hub_h1"], w["hub_intro"], cards) + FOOT

    io.open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8").write(
      page(w["hub_name"] + " | Adventure Spirit Consulting", w["hub_desc"], hub_body,
           SITE + w["hub"], lang=lang, extra_head=hreflang(hr_hub, en_hub)))

    # ── Kalkulator ────────────────────────────────────────────────
    url = SITE + w["hub"] + w["slug"] + "/"
    JS = '''<script>
(function () {
  var T = %s;
  var $ = function (id) { return document.getElementById(id); };

  function pad(n) { return n < 10 ? "0" + n : "" + n; }
  function fmt(d) {
    var t = pad(d.getHours()) + ":" + pad(d.getMinutes());
    if (T.lang === "en") {
      return d.getDate() + " " + T.months[d.getMonth()] + " " + d.getFullYear() + ", " + t;
    }
    return pad(d.getDate()) + "." + pad(d.getMonth() + 1) + "." + d.getFullYear() + ". " + t;
  }
  function add(d, ms) { return new Date(d.getTime() + ms); }
  // Rokovi u danima racunaju se kalendarski, da prijelaz na ljetno ili
  // zimsko racunanje vremena ne pomakne sat u roku.
  function addDays(d, n) { var x = new Date(d.getTime()); x.setDate(x.getDate() + n); return x; }
  var H = 3600000, D = 86400000;

  function remaining(target) {
    var diff = target.getTime() - Date.now();
    if (diff <= 0) return { cls: "over", txt: T.over };
    if (diff < D) {
      var h = Math.floor(diff / H), m = Math.floor((diff %% H) / 60000);
      return { cls: diff < 6 * H ? "soon" : "ok", txt: T.leftH.replace("%%1", h).replace("%%2", m) };
    }
    var dd = Math.floor(diff / D), hh = Math.floor((diff %% D) / H);
    return { cls: "ok", txt: T.leftD.replace("%%1", dd).replace("%%2", hh) };
  }

  function row(n, title, desc, when, extra, muted) {
    var r = remaining(when instanceof Date ? when : new Date(8640000000000000));
    var whenTxt = when instanceof Date ? fmt(when) : when;
    var leftTxt = when instanceof Date ? r.txt : (extra || "");
    var leftCls = when instanceof Date ? r.cls : "info";
    if (muted) { leftTxt = extra || ""; leftCls = "info"; }
    return '<div class="dl' + (muted ? " muted" : "") + '">' +
      '<div class="dl-num">' + n + '</div>' +
      '<div><div class="dl-title">' + title + '</div><div class="dl-desc">' + desc +
        (!muted && when instanceof Date && extra ? '<br><span style="color:#6b7488">' + extra + '</span>' : '') +
      '</div></div>' +
      '<div class="dl-when"><div class="dl-date">' + whenTxt + '</div>' +
      '<div class="dl-left ' + leftCls + '">' + leftTxt + '</div></div></div>';
  }

  function calc() {
    var raw = $("t-when").value;
    var err = $("t-err");
    if (!raw) { err.textContent = T.errDate; err.hidden = false; $("t-result").hidden = true; return; }
    err.hidden = true;

    var t0 = new Date(raw);
    var tsp = $("t-tsp").checked, gdpr = $("t-gdpr").checked;
    var sentRaw = $("t-sent").value;
    var initial = tsp ? add(t0, 24 * H) : add(t0, 72 * H);
    var sent = sentRaw ? new Date(sentRaw) : initial;
    var finalDue = addDays(sent, 30);

    var html = "", n = 1;
    if (tsp) {
      html += row("-", T.d1, T.d1d, "\\u2014", T.tspNote, true);
    } else {
      html += row(pad(n++), T.d1, T.d1d, add(t0, 24 * H), "24 h");
    }
    html += row(pad(n++), T.d2, T.d2d, initial, tsp ? "24 h" : "72 h");
    html += row(pad(n++), T.d3, T.d3d, T.d3when, "", true);
    html += row(pad(n++), T.d4, T.d4d, finalDue, "30 " + T.days + " " + (sentRaw ? T.leftFrom : T.leftFromCalc));
    html += row(pad(n++), T.d5, T.d5d, addDays(finalDue, 30), T.d5extra, true);
    if (gdpr) html += row("+", T.d6, T.d6d, add(t0, 72 * H), "72 h");

    $("dl-list").innerHTML = html;
    $("t-from").textContent = fmt(t0);
    $("t-result").hidden = false;

    var lines = [T.summaryH, T.summaryFrom + " " + fmt(t0), ""];
    if (!tsp) lines.push("1. " + T.d1 + ": " + fmt(add(t0, 24 * H)));
    lines.push((tsp ? "1. " : "2. ") + T.d2 + ": " + fmt(initial));
    lines.push((tsp ? "2. " : "3. ") + T.d3 + ": " + T.d3when);
    lines.push((tsp ? "3. " : "4. ") + T.d4 + ": " + fmt(finalDue));
    lines.push((tsp ? "4. " : "5. ") + T.d5 + ": " + fmt(addDays(finalDue, 30)));
    if (gdpr) lines.push("+  " + T.d6 + ": " + fmt(add(t0, 72 * H)));
    lines.push("", T.disclaimer);
    $("t-summary").textContent = lines.join("\\n");
    $("t-result").scrollIntoView({ behavior: "smooth", block: "start" });
  }

  $("t-calc").addEventListener("click", calc);
  $("t-reset").addEventListener("click", function () {
    $("t-when").value = ""; $("t-sent").value = "";
    $("t-tsp").checked = false; $("t-gdpr").checked = false;
    $("t-result").hidden = true; $("t-err").hidden = true;
  });
  $("t-print").addEventListener("click", function () { window.print(); });
  $("t-copy").addEventListener("click", function () {
    var txt = $("t-summary").textContent;
    var done = function () { $("t-copied").hidden = false; setTimeout(function () { $("t-copied").hidden = true; }, 2500); };
    if (navigator.clipboard) { navigator.clipboard.writeText(txt).then(done, done); }
    else { var ta = document.createElement("textarea"); ta.value = txt; document.body.appendChild(ta);
           ta.select(); try { document.execCommand("copy"); } catch (e) {} ta.remove(); done(); }
  });
  ["t-when", "t-sent"].forEach(function (id) {
    $(id).addEventListener("keydown", function (e) { if (e.key === "Enter") calc(); });
  });
})();
</script>''' % json.dumps({
      "errDate": w["err_date"], "over": w["left_over"],
      "leftH": w["left_h"].replace("%d", "%1", 1).replace("%d", "%2", 1),
      "leftD": w["left_d"].replace("%d", "%1", 1).replace("%d", "%2", 1),
      "d1": w["d1"], "d1d": w["d1_d"], "d2": w["d2"], "d2d": w["d2_d"],
      "d3": w["d3"], "d3d": w["d3_d"], "d3when": w["d3_when"],
      "d4": w["d4"], "d4d": w["d4_d"], "d5": w["d5"], "d5d": w["d5_d"],
      "d6": w["d6"], "d6d": w["d6_d"], "tspNote": w["d1_tsp_note"],
      "days": "dana" if lang == "hr" else "days",
      "leftFrom": w["left_from"],
      "leftFromCalc": ("od isteka roka od 72 sata" if lang == "hr" else "from the 72-hour deadline"),
      "d5extra": ("i svakih idućih 30 dana" if lang == "hr" else "and every 30 days thereafter"),
      "summaryH": w["summary_h"], "summaryFrom": w["summary_from"],
      "disclaimer": w["disclaimer"], "lang": lang,
      "months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    }, ensure_ascii=False)

    body = header(lang, active_blog=False) + '''
<main>
  <div class="container narrow">
    <div class="crumbs">
      <a href="%s">%s</a><span>&rsaquo;</span><a href="%s">%s</a><span>&rsaquo;</span>%s
    </div>
    <header class="art-head">
      <div class="eyebrow">%s</div>
      <h1>%s</h1>
      <p class="art-lead">%s</p>
    </header>

    <div class="tool-panel">
      <div class="field">
        <label for="t-when">%s</label>
        <input type="datetime-local" id="t-when">
        <div class="sub">%s</div>
      </div>
      <div class="field">
        <label for="t-sent">%s</label>
        <input type="datetime-local" id="t-sent">
        <div class="sub">%s</div>
      </div>
      <label class="check"><input type="checkbox" id="t-tsp"><span>%s<em>%s</em></span></label>
      <label class="check"><input type="checkbox" id="t-gdpr"><span>%s<em>%s</em></span></label>
      <p id="t-err" class="dl-left over" hidden style="margin-top:12px"></p>
      <div class="tool-actions">
        <button type="button" class="btn-primary" id="t-calc">%s</button>
        <button type="button" class="btn-ghost" id="t-reset">%s</button>
      </div>
      <p class="sub" style="margin-top:18px">%s</p>
    </div>

    <div class="tool-result" id="t-result" hidden>
      <div class="result-head">
        <h2>%s</h2>
        <span>%s <strong id="t-from"></strong></span>
      </div>
      <div class="dl-list" id="dl-list"></div>
      <div class="note tool-note"><p>%s</p></div>
      <div class="summary-box" id="t-summary"></div>
      <div class="tool-actions">
        <button type="button" class="btn-ghost" id="t-copy">%s</button>
        <button type="button" class="btn-ghost" id="t-print">%s</button>
        <span class="copied" id="t-copied" hidden>%s</span>
      </div>
    </div>

    <article style="padding-top:40px">
      <div class="note"><p>%s</p></div>
      <p><a href="%s">%s &rarr;</a></p>
    </article>
    %s
  </div>
</main>
''' % (t["base"] or "/", t["home"], w["hub"], w["hub_name"], w["t_name"],
       w["hub_name"], w["t_title"], w["t_lead"],
       w["f_when"], w["f_when_sub"], w["f_sent"], w["f_sent_sub"],
       w["f_tsp"], w["f_tsp_sub"], w["f_gdpr"], w["f_gdpr_sub"],
       w["btn_calc"], w["btn_reset"], w["privacy_note"],
       w["res_h"], w["res_sub"], w["note"],
       w["btn_copy"], w["btn_print"], w["copied"],
       w["disclaimer"], w["more_url"], w["more"], cta_block(lang)) + FOOT + JS

    ld = [{
      "@context": "https://schema.org", "@type": "WebApplication",
      "name": w["t_title"], "description": w["t_desc_meta"], "url": url,
      "applicationCategory": "BusinessApplication",
      "operatingSystem": "Any", "browserRequirements": "JavaScript",
      "inLanguage": "hr-HR" if lang == "hr" else "en-GB",
      "isAccessibleForFree": True,
      "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"},
      "publisher": {"@type": "Organization", "name": "Adventure Spirit Consulting",
                    "legalName": "Adventure Spirit d.o.o.", "url": SITE + "/"},
    }, {
      "@context": "https://schema.org", "@type": "BreadcrumbList",
      "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": t["home"], "item": SITE + (t["base"] or "/")},
        {"@type": "ListItem", "position": 2, "name": w["hub_name"], "item": SITE + w["hub"]},
        {"@type": "ListItem", "position": 3, "name": w["t_name"], "item": url}]}]

    io.open(os.path.join(out_dir, w["slug"], "index.html"), "w", encoding="utf-8").write(
      page(w["t_title"] + " | Adventure Spirit Consulting", w["t_desc_meta"], body, url,
           lang=lang, extra_head=hreflang(hr_hub + TOOLS_T["hr"]["slug"] + "/",
                                          en_hub + TOOLS_T["en"]["slug"] + "/"), ld=ld))


build_tools("hr", ARTICLES)
build_tools("en", ARTICLES_EN)

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

# Osvjezi tri istaknuta clanka u sekciji "Baza znanja" na naslovnici
_top = sorted(ARTICLES, key=lambda a: a["date"], reverse=True)[:3]
_cards = "\n".join('''      <a class="kb-card" href="/blog/%s/">
        <div class="kb-cat">%s</div>
        <div class="kb-title">%s</div>
        <div class="kb-lead">%s</div>
        <div class="kb-meta">%d min čitanja</div>
      </a>''' % (a["slug"], html.escape(a["cat"]), html.escape(a["title"]),
                 html.escape(a["lead"]), a["read"]) for a in _top)
_s = re.sub(r'(<div class="kb-grid">\n).*?(\n    </div>\n    <div class="kb-all">)',
            lambda m: m.group(1) + _cards + m.group(2), _s, count=1, flags=re.S)

if '>English version<' not in _s:
    _s = _s.replace('        <a href="#kontakt">Kontakt</a>\n      </div>',
      '        <a href="#kontakt">Kontakt</a>\n        <a href="/en/">English version</a>\n      </div>', 1)

io.open(_idx, "w", encoding="utf-8").write(_s)

# ══════════════════════════════════════════════════════════════════
# sitemap.xml + robots.txt
# ══════════════════════════════════════════════════════════════════
urls = [(SITE + "/", "1.0", "weekly"), (SITE + "/en/", "0.9", "weekly"),
        (SITE + "/blog/", "0.9", "weekly"), (SITE + "/en/blog/", "0.8", "weekly"),
        (SITE + "/alati/", "0.9", "monthly"), (SITE + "/en/tools/", "0.8", "monthly"),
        (SITE + "/alati/" + TOOLS_T["hr"]["slug"] + "/", "0.9", "monthly"),
        (SITE + "/en/tools/" + TOOLS_T["en"]["slug"] + "/", "0.8", "monthly")]
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

print("Generirano: alati + HR %d + EN %d clanaka, 2 popisne stranice, 2 feeda, 2x404, EN naslovnica, sitemap, robots"
      % (len(ARTICLES), len(ARTICLES_EN)))
