#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generator baze znanja za adventurespirit.hr - statican HTML, bez build alata."""
import io, os, re, html, json

ROOT = "/Users/dbara/adventurespirit-website"
BLOG = os.path.join(ROOT, "blog")
SITE = "https://adventurespirit.hr"

# ══════════════════════════════════════════════════════════════════
# Formspree odredista
# Tri odvojena obrasca umjesto jednoga, jer se razlikuju po hitnosti i
# po djelatnosti. Dok se zasebni obrasci ne otvore, sva tri pokazuju na
# postojeci, pa promjena ovdje nista ne lomi.
#   UPITI      - prodajni upiti, traze odgovor u 24 sata
#   OBAVIJESTI - prijave na obavijesti i zahtjevi za izvjestajem
#   IZLETI     - izleti, odvojena djelatnost (u izleti/index.html)
# ══════════════════════════════════════════════════════════════════
FS_UPITI = "xbgjpgvb"
FS_OBAVIJESTI = "xjyvpyqq"

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
   nav=[("/#onama","O nama"),("/usluge/","Usluge"),("/sektori/","Sektori"),
        ("/blog/","Baza znanja"),("/propisi/","Propisi"),("/mjere/","13 mjera"),("/alati/","Alati"),("/#reference","Reference"),
        ("/#faq","FAQ"),("/kontakt/","Kontakt")],
   legal_line="Adventure Spirit d.o.o. &middot; Zagreb",
   brand_line="Tržišni naziv: Adventure Spirit Consulting",
   addr="Antuna Šoljana 22, 10000 Zagreb, Hrvatska", oib="OIB / PDV ID: 72169598754 &middot; MBS: 4845552<br>Trgovački sud u Zagrebu",
   tagline="Kibernetička sigurnost, GRC compliance i upravljanje rizicima - preko 20 godina iskustva u službi vašeg poslovanja.",
   f_kb="Baza znanja", f_all="Svi članci", f_svc="Usluge", f_co="Tvrtka",
   f_links=[("/usluge/zks-nis2-uskladenost/","ZKS / NIS2"),("/usluge/gdpr-uskladenost/","GDPR"),
            ("/usluge/iso-27001/","ISO 27001"),("/usluge/dora/","DORA"),("/usluge/","Sve usluge")],
   f_co_links=[("/#onama","O konzultantu"),("/predavanja/","Predavanja"),("/#faq","Česta pitanja"),
               ("/kontakt/","Kontakt"),("/en/","English version")],
   nl_h="Novi tekst otprilike svaka dva tjedna",
   nl_p="Kad izađe nov članak u bazi znanja ili se promijeni nešto u propisu, javimo se kratkom porukom. Bez ponuda i bez podsjetnika.",
   nl_ph="Vaša e-mail adresa", nl_btn="Prijavi me",
   nl_consent='Pristajem primati obavijesti o novim tekstovima od Adventure Spirit d.o.o. Privolu mogu povući u svakom trenutku, porukom na info@adventurespirit.hr ili poveznicom u svakoj obavijesti. Više u <a href="/privatnost/">politici privatnosti</a>.',
   nl_ok="Hvala, prijava je zabilježena. Javljamo se kad izađe novi tekst.",
   nl_err="Prijava nije uspjela. Pišite nam na info@adventurespirit.hr.",
   nl_need="Upišite ispravnu adresu i potvrdite privolu.",
   nl_send="Šaljem...",
   nl_fine="Adresu koristimo isključivo za slanje ovih obavijesti. Ne prosljeđujemo je nikome i ne koristimo za druge svrhe.",
   rights="Sva prava pridržana", terms="Uvjeti korištenja", privacy="Privatnost",
   terms_url="/uvjeti/", privacy_url="/privatnost/",
   kb_title="Baza znanja", kb_h1="Što propis traži i čime se to dokazuje",
   kb_intro="Tekstovi o Zakonu o kibernetičkoj sigurnosti, ISO normama, zaštiti podataka i upravljanju rizicima. Bez uopćavanja: uz svaku tvrdnju stoji članak propisa ili norme ondje gdje ga ima.",
   kb_desc="Stručni tekstovi o Zakonu o kibernetičkoj sigurnosti, 13 mjera Uredbe, samoprocjeni, prijavi incidenata, ISO normama i upravljanju rizicima.",
   all_topics="Sve teme", read="min čitanja", home="Početna",
   pretraga="Pretražite po pojmu, mjeri ili propisu",
   pret_broj="Prikazano <b>%d</b> od %d članaka",
   pret_nema="Nema članka koji odgovara pojmu <b>%s</b>.",
   pret_savjet="Probajte kraći pojam, ili pogledajte sve teme.",
   pret_ocisti="Očisti",
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
   nav=[("/en/#about","About"),("/en/services/","Services"),("/en/sectors/","Sectors"),
        ("/en/blog/","Insights"),("/en/regulations/","Regulations"),("/en/measures/","13 measures"),("/en/tools/","Tools"),("/en/#clients","Clients"),
        ("/en/#faq","FAQ"),("/en/contact/","Contact")],
   legal_line="Adventure Spirit d.o.o. &middot; Zagreb, Croatia",
   brand_line="Trading as: Adventure Spirit Consulting",
   addr="Antuna Šoljana 22, 10000 Zagreb, Croatia", oib="OIB / VAT ID: 72169598754 &middot; Reg. no. (MBS): 4845552<br>Commercial Court in Zagreb",
   tagline="Cyber security, GRC compliance and risk management - over 20 years of experience in the service of your business.",
   f_kb="Insights", f_all="All articles", f_svc="Services", f_co="Company",
   f_links=[("/en/services/csa-nis2-compliance/","CSA / NIS2"),("/en/services/gdpr-compliance/","GDPR"),
            ("/en/services/iso-27001/","ISO 27001"),("/en/services/dora/","DORA"),("/en/services/","All services")],
   f_co_links=[("/en/#about","About the consultant"),("/en/speaking/","Speaking"),("/en/#faq","FAQ"),
               ("/en/contact/","Contact"),("/","Hrvatska verzija")],
   nl_h="A new article roughly every two weeks",
   nl_p="When a new article appears in the knowledge base, or something changes in the rules, we send a short note. No offers and no reminders.",
   nl_ph="Your email address", nl_btn="Sign me up",
   nl_consent='I agree to receive notifications about new articles from Adventure Spirit d.o.o. I can withdraw this consent at any time, by writing to info@adventurespirit.hr or via the link in every message. See the <a href="/en/privacy/">privacy policy</a>.',
   nl_ok="Thank you, you are signed up. We will write when a new article appears.",
   nl_err="Sign-up failed. Please write to info@adventurespirit.hr.",
   nl_need="Enter a valid address and confirm consent.",
   nl_send="Sending...",
   nl_fine="We use the address solely to send these notifications. We do not pass it on and do not use it for anything else.",
   rights="All rights reserved", terms="Terms (HR)", privacy="Privacy (HR)",
   terms_url="/en/terms/", privacy_url="/en/privacy/",
   kb_title="Knowledge base", kb_h1="What the rules ask for and what proves it",
   kb_intro="Articles on the Croatian Cybersecurity Act, ISO standards, data protection and risk management. No generalities: every claim carries the article of the law or standard behind it, where one exists.",
   kb_desc="Expert articles on the Croatian Cybersecurity Act, the 13 measures of the Regulation, self-assessment scoring, incident reporting, ISO standards and risk management.",
   all_topics="All topics", read="min read", home="Home",
   pretraga="Search by term, measure or regulation",
   pret_broj="Showing <b>%d</b> of %d articles",
   pret_nema="No article matches <b>%s</b>.",
   pret_savjet="Try a shorter term, or browse all topics.",
   pret_ocisti="Clear",
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
    # Po jedna tema, najnoviji clanak iz nje - inace se ista tema ponavlja
    _vid, _kb = set(), []
    for a in sorted(articles, key=lambda x: x["date"], reverse=True):
        if a["cat"] in _vid:
            continue
        _vid.add(a["cat"])
        _kb.append('        <a href="%s%s/">%s</a>' % (t["blog"], a["slug"], html.escape(a["cat"])))
        if len(_kb) == 4:
            break
    kb = "\n".join(_kb) + '\n        <a href="%s">%s</a>' % (t["blog"], t["f_all"])
    svc = "\n".join('        <a href="%s">%s</a>' % (u, n) for u, n in t["f_links"])
    co = "\n".join('        <a href="%s">%s</a>' % (u, n) for u, n in t["f_co_links"])
    nl = '''<div class="nl">
      <h4>%s</h4>
      <p>%s</p>
      <div class="nl-row">
        <label class="vh" for="nl-mail">%s</label>
        <input type="email" id="nl-mail" placeholder="%s" autocomplete="email">
        <button type="button" id="nl-btn">%s</button>
      </div>
      <label class="nl-consent"><input type="checkbox" id="nl-ok"><span>%s</span></label>
      <p class="nl-msg" id="nl-msg" hidden></p>
      <p class="nl-fine">%s</p>
    </div>''' % (t["nl_h"], t["nl_p"], t["nl_ph"], t["nl_ph"], t["nl_btn"], t["nl_consent"], t["nl_fine"])

    nl_js = '''<script>
(function () {
  var T = %s, $ = function (i) { return document.getElementById(i); };
  var b = $("nl-btn"); if (!b) { return; }
  b.addEventListener("click", function () {
    var m = $("nl-mail").value.trim(), msg = $("nl-msg");
    if (!/^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$/.test(m) || !$("nl-ok").checked) {
      msg.textContent = T.need; msg.className = "nl-msg bad"; msg.hidden = false; return;
    }
    var lab = b.textContent; b.disabled = true; b.textContent = T.send; msg.hidden = true;
    fetch("https://formspree.io/f/__FS_OBAVIJESTI__", {
      method: "POST", headers: { "Content-Type": "application/json", Accept: "application/json" },
      body: JSON.stringify({ email: m, _subject: T.subj,
        message: T.subj + "\\n" + location.href + "\\n\\n" + T.log })
    }).then(function (r) {
      if (!r.ok) { throw new Error(); }
      msg.textContent = T.ok; msg.className = "nl-msg ok"; msg.hidden = false;
      $("nl-mail").value = ""; $("nl-ok").checked = false;
      if (window.asTrack) { window.asTrack("newsletter_signup"); }
    }).catch(function () {
      msg.textContent = T.err; msg.className = "nl-msg bad"; msg.hidden = false;
    }).finally(function () { b.disabled = false; b.textContent = lab; });
  });
})();
</script>''' % json.dumps({
      "need": t["nl_need"], "send": t["nl_send"], "ok": t["nl_ok"], "err": t["nl_err"],
      "subj": ("Prijava na obavijesti o novim tekstovima" if lang == "hr"
               else "Sign-up for new article notifications"),
      "log": ("Privola dana kroz obrazac u podnozju stranice." if lang == "hr"
              else "Consent given via the form in the page footer."),
    }, ensure_ascii=False)

    return '''<footer>
  <div class="container">
    ''' + nl + '''
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
</footer>''' + nl_js


def hreflang(hr_url, en_url):
    return ('<link rel="alternate" hreflang="hr" href="%s">\n'
            '<link rel="alternate" hreflang="en" href="%s">\n'
            '<link rel="alternate" hreflang="x-default" href="%s">' % (hr_url, en_url, hr_url))



# ── Mjerni skript (prvostrana analitika, bez kolacica) ────────────
BEACON = """<script>
(function () {
  var Q = "/analitika/collect.php";
  function send(body) {
    try {
      var s = JSON.stringify(body);
      if (navigator.sendBeacon) {
        navigator.sendBeacon(Q, new Blob([s], { type: "application/json" }));
      } else {
        fetch(Q, { method: "POST", headers: { "Content-Type": "application/json" },
                   body: s, keepalive: true }).catch(function () {});
      }
    } catch (e) {}
  }
  window.asTrack = function (name, value) {
    send({ p: location.pathname, e: name, v: value === undefined ? "" : value, w: window.innerWidth });
  };
  if (location.hostname === "localhost" || location.hostname === "127.0.0.1") { return; }
  send({ p: location.pathname, r: document.referrer, l: (navigator.language || "").slice(0, 5),
         w: window.innerWidth });
  document.addEventListener("click", function (ev) {
    var a = ev.target.closest && ev.target.closest("a[href]");
    if (a && a.hostname === "app.adventurespirit.hr") { window.asTrack("portal_click"); }
  }, true);
})();
</script>"""

def page(title, desc, body, canonical, lang="hr", extra_head="", og_type="website", ld=None,
         css_link=True, feed=None):
    ldjs = ""
    if ld:
        ldjs = "\n".join('<script type="application/ld+json">\n%s\n</script>'
                         % json.dumps(o, ensure_ascii=False, indent=2) for o in ld)
    feed = feed or L[lang]["blog"] + "feed.xml"
    css = '<link rel="stylesheet" href="/blog/assets/blog.css">\n' if css_link else ''
    body = (body.replace("__FS_UPITI__", FS_UPITI)
                .replace("__FS_OBAVIJESTI__", FS_OBAVIJESTI))
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
%s
</body>
</html>
''' % (lang, html.escape(title), html.escape(desc), canonical, AUTHOR, og_type,
       "hr_HR" if lang == "hr" else "en_GB", canonical, html.escape(title), html.escape(desc),
       SITE, html.escape(title), html.escape(desc), html.escape(L[lang]["feed_title"]), feed,
       FAVICON, css, extra_head, body, ldjs, BEACON)

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
<p>Zakon zatim nabraja skupine kod kojih <strong>veličina uopće nije mjerilo</strong>. Ključni su, neovisno o veličini: kvalificirani pružatelji usluga povjerenja, registar naziva vršne nacionalne domene i pružatelji usluga DNS-a, informacijski posrednici u razmjeni elektroničkog računa, subjekti utvrđeni kao kritični prema zakonu o kritičnoj infrastrukturi, tijela državne uprave te upravitelji državne informacijske infrastrukture. Važni su, neovisno o veličini: pružatelji usluga povjerenja koji nisu ključni, pružatelji javnih elektroničkih komunikacijskih mreža i usluga koji nisu ključni, jedinice lokalne i područne samouprave te subjekti iz sustava obrazovanja.</p>
<p>Uz to, <strong>članak 11.</strong> dopušta razvrstavanje neovisno o veličini svakom subjektu iz priloga koji je jedini pružatelj usluge ključne za održavanje ključnih društvenih ili gospodarskih djelatnosti, čiji bi ispad znatno utjecao na javnu sigurnost, zaštitu ili zdravlje, mogao uzrokovati sistemske rizike, ili koji je značajan zbog posebne važnosti na nacionalnoj, regionalnoj ili lokalnoj razini. Zbog tog članka mala ustanova može biti ključni subjekt jednako kao i velika, i to je najčešći izvor iznenađenja.</p>
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
   ('Zakon o kibernetičkoj sigurnosti, NN 14/2024', 'https://narodne-novine.nn.hr/clanci/sluzbeni/2024_02_14_254.html'),
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
   ('Direktiva (EU) 2022/2555 (NIS2), čl. 21.', 'https://eur-lex.europa.eu/eli/dir/2022/2555/oj/hrv'),
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
   ('Zakon o kibernetičkoj sigurnosti, NN 14/2024', 'https://narodne-novine.nn.hr/clanci/sluzbeni/2024_02_14_254.html'),
   ('Uredba o kibernetičkoj sigurnosti, NN 135/2024', 'https://narodne-novine.nn.hr/clanci/sluzbeni/2024_11_135_2217.html'),
   ('Uredba (EU) 2016/679 (Opća uredba o zaštiti podataka), čl. 33.', 'https://eur-lex.europa.eu/eli/reg/2016/679/oj/hrv'),
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
   ('HRN EN ISO/IEC 27001:2022 - Sustavi upravljanja informacijskom sigurnošću', '/blog/iso-27001-i-zks/'),
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
 sources=[('HRN EN ISO/IEC 27001:2022, Prilog A', '/blog/iso-27002-2022-atributi-kontrola/'),
          ('HRN EN ISO/IEC 27002:2022 - Kontrole informacijske sigurnosti', '/blog/iso-27002-2022-atributi-kontrola/'),
          ('ISO/IEC 27001:2022/Amd 1:2024 - climate action changes', '/blog/iso-27002-2022-atributi-kontrola/')]))

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
 sources=[('HRN EN ISO 22301:2019 - Sustavi upravljanja kontinuitetom poslovanja', '/blog/bia-koja-daje-upotrebljiv-rto/'),
          ('ISO/TS 22317 - Smjernice za analizu poslovnog utjecaja', '/blog/bia-koja-daje-upotrebljiv-rto/'),
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
 sources=[('Uredba (EU) 2022/2554 (DORA)', 'https://eur-lex.europa.eu/eli/reg/2022/2554/oj/hrv'),
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
          ('HRN EN ISO/IEC 27001:2022, Prilog A', '/blog/iso-27002-2022-atributi-kontrola/')]))

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
          ('HRN EN ISO/IEC 27002:2022 - atributi kontrola', '/blog/iso-27002-2022-atributi-kontrola/')]))

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
          ('HRN EN ISO/IEC 27002:2022 - kontrole tehnoloških mjera', '/blog/iso-27002-2022-atributi-kontrola/'),
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
          ('Provedbena uredba Komisije (EU) 2024/2690', 'https://eur-lex.europa.eu/eli/reg_impl/2024/2690/oj/hrv'),
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
          ('Uredba (EU) 2019/881 - definicije kibernetičke sigurnosti i prijetnje', 'https://eur-lex.europa.eu/eli/reg/2019/881/oj/hrv')]))

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
 sources=[('Uredba (EU) 2024/1689 (Akt o umjetnoj inteligenciji)', 'https://eur-lex.europa.eu/eli/reg/2024/1689/oj/hrv'),
          ('Uredba (EU) 2016/679 (Opća uredba o zaštiti podataka)', 'https://eur-lex.europa.eu/eli/reg/2016/679/oj/hrv')]))

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
 sources=[('Uredba (EU) 2024/1689 (Akt o umjetnoj inteligenciji), čl. 4. i 5.', 'https://eur-lex.europa.eu/eli/reg/2024/1689/oj/hrv'),
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
 sources=[('Uredba (EU) 2024/1689 (Akt o umjetnoj inteligenciji)', 'https://eur-lex.europa.eu/eli/reg/2024/1689/oj/hrv'),
          ('Uredba o kibernetičkoj sigurnosti, NN 135/2024, Prilog II., mjere 2 i 8', 'https://narodne-novine.nn.hr/clanci/sluzbeni/2024_11_135_2217.html'),
          ('HRN EN ISO/IEC 27001:2022, Prilog A - upravljanje imovinom', '/blog/iso-27001-i-zks/')]))

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
 sources=[('Uredba (EU) 2024/1689 (Akt o umjetnoj inteligenciji)', 'https://eur-lex.europa.eu/eli/reg/2024/1689/oj/hrv'),
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
          ('Direktiva (EU) 2022/2555 (NIS2) - sektori energetike, vodoopskrbe i prometa', 'https://eur-lex.europa.eu/eli/dir/2022/2555/oj/hrv'),
          ('Prioritetne preporuke za zaštitu od kibernetičkih napada, NCSC-HR', 'https://www.ncsc.hr/')]))

# ══════════════════════════════════════════════════════════════════
# Novi clanci: kazne, revizija, sigurnosna kultura
# ══════════════════════════════════════════════════════════════════
ARTICLES.append(dict(
 slug="zks-kazne-tko-placa-i-koliko", cat="ZKS / NIS2", catkey="zks",
 date="2026-06-23", read=8, featured=False,
 title="Kazne prema ZKS-u: tko plaća, koliko, i zašto se to tiče uprave osobno",
 lead="Do 10 milijuna eura ili 2 posto svjetskog prometa za ključne subjekte. Ali brojka koja mijenja razgovor s upravom nije ta - nego ona uz nju: članovi upravljačkog tijela odgovaraju osobno, vlastitim novcem.",
 desc="Pregled prekršajnih odredbi Zakona o kibernetičkoj sigurnosti: rasponi kazni za ključne i važne subjekte, osobna odgovornost članova upravljačkih tijela, okolnosti koje utječu na visinu i pravilo o zabrani dvostrukog kažnjavanja s AZOP-om.",
 body='''
<p>U razgovorima o usklađivanju sa Zakonom o kibernetičkoj sigurnosti brojka koja se najčešće spominje je deset milijuna eura. Točna je, ali nepotpuna, i sama po sebi rijetko pomiče stvari s mrtve točke.</p>
<p>Ono što ih pomiče je članak 88. stavak 2. i njegov parnjak za važne subjekte - odredba po kojoj <strong>fizičke osobe odgovorne za upravljanje mjerama odgovaraju osobno</strong>.</p>

<h2>Rasponi kazni</h2>
<div class="tbl-wrap">
  <table>
    <thead><tr><th>Tko</th><th>Raspon</th><th>Alternativno</th></tr></thead>
    <tbody>
      <tr><td><strong>Ključni subjekt</strong></td><td>10.000 - 10.000.000 EUR</td><td>0,5 % do 2 % ukupnog godišnjeg svjetskog prometa</td></tr>
      <tr><td><strong>Važni subjekt</strong></td><td>5.000 - 7.000.000 EUR</td><td>0,2 % do 1,4 % ukupnog godišnjeg svjetskog prometa</td></tr>
      <tr><td><strong>Odgovorna osoba, ključni subjekt</strong></td><td class="num">1.000 - 6.000 EUR</td><td>-</td></tr>
      <tr><td><strong>Odgovorna osoba, važni subjekt</strong></td><td class="num">500 - 3.000 EUR</td><td>-</td></tr>
      <tr><td><strong>Nedostava podataka NCSC-u</strong></td><td>2.000 - 20.000 EUR</td><td>odgovorna osoba 200 - 1.000 EUR</td></tr>
    </tbody>
  </table>
</div>
<p>Kod pravnih osoba primjenjuje se <strong>viši od dva iznosa</strong> - fiksni ili postotak prometa. Za subjekt s prometom od 400 milijuna eura gornja granica nije 10 milijuna nego 8 milijuna po postotku, pa se primjenjuje fiksni iznos. Za subjekt s prometom od milijardu, postotak nadmašuje fiksni iznos.</p>

<h2>Tko je "odgovorna osoba"</h2>
<p>Članak 29. je precizan i širi nego što se očekuje. Za provedbu mjera odgovorni su:</p>
<ul>
  <li><strong>članovi upravljačkih tijela</strong> ključnih i važnih subjekata</li>
  <li><strong>čelnici tijela državne uprave</strong> i drugih državnih tijela</li>
  <li><strong>izvršna tijela</strong> jedinica lokalne i područne samouprave</li>
</ul>
<p>Stavak 4. proširuje krug i na druge fizičke osobe koje na temelju ovlasti za nadzor nad vođenjem poslova, punomoći ili druge ovlasti za zastupanje <strong>sudjeluju u donošenju odluka o mjerama ili u njihovoj provedbi</strong>.</p>
<div class="callout">
  <div class="c-label">Praktična posljedica</div>
  <p>Prokurist, član nadzornog odbora koji odlučuje o ulaganju u sigurnost, ili direktor informatike s punomoći - svi mogu ući u krug osobno odgovornih. Odgovornost se ne prenosi ugovorom na dobavljača ni na konzultanta.</p>
</div>

<h2>Dvije obveze koje uprava ne može delegirati</h2>
<p>Članak 29. stavak 2. traži da odgovorne osobe <strong>odobravaju</strong> mjere i <strong>kontroliraju njihovu provedbu</strong>. Stavak 3. dodaje obvezu koja se redovito previđa:</p>
<ul>
  <li>odgovorne osobe dužne su <strong>same pohađati odgovarajuća osposobljavanja</strong></li>
  <li>i zaposlenicima omogućiti pohađanje osposobljavanja</li>
</ul>
<p>Uprava koja nije prošla edukaciju ne ispunjava zakonsku obvezu, bez obzira na to koliko je dobar sustav ispod nje. To je jedan od rijetkih zahtjeva gdje dokaz mora glasiti na ime člana uprave.</p>

<h2>Što utječe na visinu kazne</h2>
<p>Članak 85. nabraja okolnosti koje nadležno tijelo uzima u obzir:</p>
<ul>
  <li>ozbiljnost povrede i važnost prekršene odredbe</li>
  <li>trajanje povrede</li>
  <li>ranije povrede istog subjekta</li>
  <li>uzrokovana šteta, uključujući financijske gubitke, učinak na druge usluge i broj pogođenih korisnika</li>
  <li>je li subjekt postupao <strong>s namjerom ili nepažnjom</strong></li>
  <li>mjere poduzete radi sprječavanja ili ublažavanja štete</li>
  <li>postupanje sukladno kodeksima ponašanja i uvjetima certificiranja</li>
  <li><strong>razina suradnje odgovornih osoba s nadležnim tijelima</strong></li>
</ul>
<div class="callout">
  <div class="c-label">Što se izrijekom smatra ozbiljnom povredom</div>
  <p>Stavak 2. istog članka nabraja: opetovane povrede, <strong>neprijavljivanje ili nerješavanje značajnih incidenata</strong>, neuklanjanje nedostataka po nalogu nadležnog tijela, te <strong>onemogućavanje ili otežavanje provedbe revizije</strong>.</p>
  <p>Drugim riječima: propuštena prijava incidenta i opstrukcija revizije nisu tehnički previdi nego otegotne okolnosti koje same po sebi podižu kaznu.</p>
</div>

<h2>Neće vas kazniti dvaput za istu stvar</h2>
<p>Odredba koja se rijetko spominje, a vrijedi je znati: ako je za povrede osobnih podataka koje proizlaze iz <strong>istog postupanja</strong> Agencija za zaštitu osobnih podataka već izrekla upravnu novčanu kaznu prema Općoj uredbi, u stručnom se nadzoru za to isto postupanje ne može podnijeti prijava ovlaštenom tužitelju ni izdati prekršajni nalog.</p>
<p>To ne znači da se obveze preklapaju - znači da se za isto djelo ne kažnjava dvaput. Prijava incidenta nadležnom CSIRT-u i prijava AZOP-u ostaju dvije odvojene obveze s vlastitim rokovima.</p>

<h2>Kako o ovome razgovarati s upravom</h2>
<p>Iz iskustva, tri stvari mijenjaju ton sastanka:</p>
<ol>
  <li><strong>Osobna odgovornost.</strong> Raspon od 1.000 do 6.000 eura nije velik novac za tvrtku, ali je vrlo konkretan za pojedinca koji ga plaća iz svog džepa.</li>
  <li><strong>Suradnja se boduje.</strong> Razina suradnje s nadležnim tijelom izrijekom utječe na kaznu. Organizacija koja sama prijavi propust i ima plan popravka nije u istoj poziciji kao ona koja čeka nadzor.</li>
  <li><strong>Edukacija uprave je zakonska obveza</strong>, ne preporuka. To je najlakša stavka za zatvoriti i najčešće otvorena.</li>
</ol>

<div class="note">
  <p>Ovaj tekst je informativni pregled prekršajnih odredbi, ne pravni savjet. Visina kazne u konkretnom slučaju ovisi o okolnostima iz članka 85. i o odluci nadležnog tijela odnosno suda. Za procjenu izloženosti vaše organizacije pogledajte <a href="/alati/provjera-kategorizacije/">provjeru kategorizacije</a> - kategorija određuje koji se raspon primjenjuje.</p>
</div>
''',
 sources=[('Zakon o kibernetičkoj sigurnosti, NN 14/2024, čl. 29., 85. i prekršajne odredbe', 'https://narodne-novine.nn.hr/clanci/sluzbeni/2024_02_14_254.html'),
          ('Uredba (EU) 2016/679 (Opća uredba o zaštiti podataka)', 'https://eur-lex.europa.eu/eli/reg/2016/679/oj/hrv'),
          ('Direktiva (EU) 2022/2555 (NIS2)', 'https://eur-lex.europa.eu/eli/dir/2022/2555/oj/hrv')]))

ARTICLES.append(dict(
 slug="revizija-kiberneticke-sigurnosti", cat="Samoprocjena", catkey="samoprocjena",
 date="2026-07-21", read=7,
 title="Revizija kibernetičke sigurnosti: tko je smije provoditi i kako teče",
 lead="Ključni subjekti ne provode samoprocjenu nego neovisnu reviziju. Provodi je pružatelj s propisanim ovlaštenjem, a kod tijela državne uprave nadležno tijelo. Evo kako postupak izgleda i što se najčešće ne prizna.",
 desc="Kako teče neovisna revizija kibernetičke sigurnosti ključnih subjekata: tko je smije provoditi, koraci postupka, kako revizor ocjenjuje dokumentaciju i provedbu, i koji se dokazi najčešće ne priznaju.",
 body='''
<p>Razlika između ključnog i važnog subjekta svodi se na jednu rečenicu: važni provode samoprocjenu, ključni prolaze <strong>neovisnu reviziju kibernetičke sigurnosti</strong>. To je razlika u trošku, u vremenu i u tome tko drži olovku.</p>

<h2>Tko je smije provoditi</h2>
<p>Reviziju ne može provesti bilo koji konzultant. Provodi je pružatelj usluga s propisanim ovlaštenjem, a kod tijela državne uprave nadležno tijelo za informacijsku sigurnost.</p>
<div class="callout">
  <div class="c-label">Zašto vas ta razdvojenost štiti</div>
  <p>Tko je sustav gradio ne smije ga i ocjenjivati. Ako vam netko nudi i uspostavu sustava i njegovu formalnu reviziju, to nije ušteda nego sukob interesa - i nalaz takve revizije nema težinu prema nadležnom tijelu.</p>
</div>

<h2>Kako postupak teče</h2>
<ol>
  <li><strong>Najava i dogovor opsega.</strong> Utvrđuje se koji su sustavi, procesi i lokacije obuhvaćeni te koja je razina provedbe mjerodavna za vašu kategoriju.</li>
  <li><strong>Plan revizije.</strong> Raspored, sugovornici i popis dokumentacije koja se dostavlja unaprijed.</li>
  <li><strong>Pregled dokumentacije.</strong> Politike, procedure, registri i zapisi - prije razgovora, ne umjesto njih.</li>
  <li><strong>Razgovori.</strong> S upravom, s vlasnicima procesa i s ljudima koji mjere stvarno provode. Ovdje se najbrže vidi razlika između napisanog i primijenjenog.</li>
  <li><strong>Uzorkovanje dokaza.</strong> Revizor bira uzorak i traži dokaz za svaku odabranu kontrolu. Ne provjerava se sve, nego se iz uzorka zaključuje o cjelini.</li>
  <li><strong>Nalazi i rokovi.</strong> Izvještaj s nalazima, njihovom ozbiljnošću i rokovima za uklanjanje.</li>
</ol>

<h2>Kako revizor ocjenjuje</h2>
<p>Ocjenjivanje se oslanja na isti bodovni okvir koji se koristi i u samoprocjeni: ocjena po kontroli, uz prag koji svaka kontrola mora doseći i dodatni prag prosjeka po podmjeri.</p>
<p>Praktično važno: <strong>dokumentiranost i provedba ocjenjuju se odvojeno</strong>. Savršena politika koja se ne primjenjuje ne daje visoku ocjenu, a dobra praksa bez zapisa ne daje ocjenu uopće - jer se ne može dokazati.</p>

<h2>Što se najčešće ne prizna</h2>
<p>Popis nalaza koji se ponavljaju iz revizije u reviziju:</p>
<ul>
  <li><strong>Dokument bez datuma i bez odobrenja.</strong> Politika koju nitko nije usvojio nije politika nego nacrt.</li>
  <li><strong>Zapis koji je nastao nakon najave revizije.</strong> Vidi se po datumima i po tome što nedostaje za razdoblje prije toga.</li>
  <li><strong>Ekran umjesto zapisa.</strong> Snimka zaslona koja pokazuje trenutno stanje ne dokazuje da je kontrola radila kroz cijelo razdoblje.</li>
  <li><strong>Registar rizika bez vlasnika i bez promjena.</strong> Ako se nije mijenjao godinu dana, ne koristi se u odlučivanju.</li>
  <li><strong>Plan kontinuiteta koji nije isproban.</strong> Bez zapisa o vježbi, plan dokumentira namjeru, ne sposobnost.</li>
  <li><strong>Edukacija bez evidencije.</strong> "Svi su prošli obuku" nije dokaz; popis s imenima i datumima jest.</li>
  <li><strong>Mjere kod dobavljača bez ugovorne osnove.</strong> Usmeno uvjeravanje pružatelja usluge ne zamjenjuje klauzulu.</li>
</ul>
<div class="callout">
  <div class="c-label">Zajednički nazivnik</div>
  <p>Gotovo svi ovi nalazi imaju isti uzrok: dokaz se pokušava proizvesti u trenutku revizije. Većina mjera dokazuje se zapisima koji nastaju tijekom ciklusa, pa se ne mogu retroaktivno napraviti. Zato rok od dvanaest mjeseci nije velikodušan.</p>
</div>

<h2>Kako se pripremiti</h2>
<p>Redoslijed koji funkcionira:</p>
<ol>
  <li><strong>Bodujte se sami, po istom okviru.</strong> Interna provjera koja simulira revizijski postupak otkriva iste nalaze, samo bez posljedica.</li>
  <li><strong>Prođite dokumentaciju kronološki.</strong> Postoji li zapis za svaki mjesec razdoblja, ili samo za zadnji?</li>
  <li><strong>Provjerite ono što se ne može popraviti brzo.</strong> Godišnji ciklus izvještavanja uprave, vježba plana kontinuiteta i evidencija edukacija traže kalendarsko vrijeme.</li>
  <li><strong>Pripremite sugovornike.</strong> Ne da nauče odgovore, nego da znaju gdje je što - revizor prepoznaje razliku.</li>
</ol>

<div class="note">
  <p>Mi provodimo interne revizije i provjeru koja simulira revizijski postupak. Formalnu neovisnu reviziju ključnih subjekata provodi ovlašteni pružatelj. Više o tome što radimo na stranici <a href="/usluge/revizije-i-interne-provjere/">Revizije i interne provjere</a>, a bodovni okvir objašnjen je u tekstu <a href="/blog/kako-se-boduje-samoprocjena/">Kako se zapravo boduje samoprocjena</a>.</p>
</div>
''',
 sources=[('Zakon o kibernetičkoj sigurnosti, NN 14/2024', 'https://narodne-novine.nn.hr/clanci/sluzbeni/2024_02_14_254.html'),
          ('Uredba o kibernetičkoj sigurnosti, NN 135/2024', 'https://narodne-novine.nn.hr/clanci/sluzbeni/2024_11_135_2217.html'),
          ('ZSIS - Prilog B, Okvir za evaluaciju mjera', 'https://www.zsis.hr/UserDocsImages/Samoprocjena/Prilog%20B%20-%20Okvir%20za%20evaluaciju.pdf')]))

ARTICLES.append(dict(
 slug="sigurnosna-kultura-i-ljudski-faktor", cat="Ljudski faktor", catkey="ljudi",
 date="2026-08-11", read=6,
 title="Sigurnosna kultura: zašto edukacija ne mijenja ponašanje, i što mijenja",
 lead="Godišnja prezentacija o phishingu proizvodi evidenciju, a ne promjenu. Mjera 5 traži podizanje svijesti, ali ono što se stvarno mjeri je ponašanje - a ono se mijenja drukčijim polugama.",
 desc="Kako pristupiti podizanju svijesti o sigurnosti tako da mijenja ponašanje, a ne samo proizvodi evidenciju: mjerenje, kultura prijave, i veza s mjerom 5 iz Priloga II. Uredbe.",
 body='''
<p>Mjera 5 iz Priloga II. traži osnovne prakse kibernetičke higijene i podizanje svijesti zaposlenika. Većina organizacija to ispuni godišnjom prezentacijom i popisom potpisa.</p>
<p>Formalno prolazi. Ponašanje se ne mijenja, i sljedeći incident dolazi kroz isti kanal kao i prošli.</p>

<h2>Zašto klasična edukacija ne radi</h2>
<h3>Uči prepoznavanje po znakovima koji su nestali</h3>
<p>Generacija materijala koja uči da se phishing prepoznaje po lošem jeziku i čudnoj adresi zastarjela je. Jezične pogreške više nisu signal - poruke su gramatički besprijekorne i prilagođene primatelju. Ono što je ostalo kao signal je <strong>kontekst</strong>: neočekivan zahtjev, pritisak vremena, promjena kanala, traženje iznimke od pravila.</p>
<h3>Mjeri pohađanje, ne ponašanje</h3>
<p>Evidencija odgovara na pitanje tko je bio prisutan. Ne odgovara na pitanje bi li ta osoba postupila drukčije. To su različite stvari i samo se druga vidi u incidentu.</p>
<h3>Kažnjava prijavu</h3>
<p>Ovo je najveći problem i najmanje se spominje. U organizaciji u kojoj se onaj tko klikne na phishing izloži poruzi ili razgovoru s nadređenim, sljedeći put nitko neće prijaviti - nego će šutjeti i nadati se. Vrijeme do otkrivanja incidenta tada se mjeri tjednima umjesto minutama.</p>

<div class="callout">
  <div class="c-label">Jedno pitanje koje otkriva stanje</div>
  <p>Pitajte nekoliko zaposlenika: "Da ste jučer kliknuli na sumnjivu poveznicu, kome biste to rekli i što mislite da bi se dogodilo?" Odgovor na drugi dio pitanja govori više o vašoj otpornosti od bilo koje evidencije edukacija.</p>
</div>

<h2>Što stvarno mijenja ponašanje</h2>
<ol>
  <li><strong>Kratko i često, umjesto dugo i jednom.</strong> Petnaest minuta u kvartalu s jednim konkretnim scenarijem nadmašuje dva sata jednom godišnje.</li>
  <li><strong>Simulacije s povratnom informacijom, ne s posljedicom.</strong> Tko klikne, dobije objašnjenje odmah, na mjestu. Rezultati se prijavljuju zbirno, nikad po osobi.</li>
  <li><strong>Prijava se nagrađuje.</strong> Onaj tko prijavi sumnjivu poruku, čak i ako se pokaže bezopasnom, treba dobiti potvrdu da je postupio ispravno. To je jedina poluga koja skraćuje vrijeme do otkrivanja.</li>
  <li><strong>Uloge dobivaju svoj sadržaj.</strong> Računovodstvo treba znati za prijevaru s promjenom bankovnog računa, informatika za napade na povlaštene račune, uprava za prijevaru s lažnim nalogom uprave.</li>
  <li><strong>Postupak umjesto opreza.</strong> "Budite oprezni s plaćanjima" ne radi. "Svako plaćanje iznad iznosa X ili promjena bankovnog računa potvrđuje se telefonski na broj iz našeg registra, nikad na broj iz e-poruke" radi, jer ne ovisi o procjeni pojedinca u trenutku pritiska.</li>
</ol>

<h2>Što mjeriti</h2>
<div class="tbl-wrap">
  <table>
    <thead><tr><th>Umjesto</th><th>Mjerite</th></tr></thead>
    <tbody>
      <tr><td>Postotak zaposlenika koji su prošli obuku</td><td>Udio prijavljenih simuliranih poruka</td></tr>
      <tr><td>Ocjena na kvizu</td><td>Prosječno vrijeme do prve prijave</td></tr>
      <tr><td>Broj održanih edukacija</td><td>Broj prijava iz odjela koji ranije nisu prijavljivali</td></tr>
      <tr><td>Zadovoljstvo edukacijom</td><td>Udio plaćanja provjerenih drugim kanalom</td></tr>
    </tbody>
  </table>
</div>
<p>Lijeva strana zadovoljava evidenciju. Desna pokazuje mijenja li se otpornost.</p>

<h2>Veza s obvezama</h2>
<p>Podizanje svijesti pripada mjeri 5, a osposobljavanje odgovornih osoba traži i članak 29. stavak 3. Zakona - članovi uprave dužni su sami pohađati odgovarajuća osposobljavanja. Uz to, članak 4. Akta o umjetnoj inteligenciji traži dostatnu razinu osposobljenosti za rad sa sustavima umjetne inteligencije.</p>
<p>Sva tri zahtjeva traže <strong>evidenciju</strong>. Dobra vijest je da program koji stvarno mijenja ponašanje proizvodi bogatiju evidenciju od onoga koji to ne čini - jer ima više dodirnih točaka kroz godinu.</p>

<div class="note">
  <p>Radionice po ulogama - za upravu, informatiku i sve zaposlenike - opisane su na stranici <a href="/predavanja/">Predavanja i radionice</a>. Svaka proizvodi evidenciju koja zadovoljava mjeru 5.</p>
</div>
''',
 sources=[('Uredba o kibernetičkoj sigurnosti, NN 135/2024, Prilog II., mjera 5', 'https://narodne-novine.nn.hr/clanci/sluzbeni/2024_11_135_2217.html'),
          ('Zakon o kibernetičkoj sigurnosti, NN 14/2024, čl. 29. st. 3.', 'https://narodne-novine.nn.hr/clanci/sluzbeni/2024_02_14_254.html'),
          ('Uredba (EU) 2024/1689 (Akt o umjetnoj inteligenciji), čl. 4.', 'https://eur-lex.europa.eu/eli/reg/2024/1689/oj/hrv')]))

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

# EN_FOOTER uklonjen - engleska naslovnica koristi footer("en"), da se
# podnozje ne odrzava na dva mjesta.


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
 ("Cybersecurity Act", "OG 14/2024", "Croatian implementation of NIS2. Entity categorisation, risk management measures, incident reporting, audit and self-assessment.", "https://narodne-novine.nn.hr/clanci/sluzbeni/2024_02_14_254.html"),
 ("Cybersecurity Regulation", "OG 135/2024", "Breaks the statutory duties down into 13 measures with sub-measures and controls, across three levels of implementation.", "https://narodne-novine.nn.hr/clanci/sluzbeni/2024_11_135_2217.html"),
 ("NIS2", "EU 2022/2555", "Directive on measures for a high common level of cybersecurity across the Union.", "https://eur-lex.europa.eu/eli/dir/2022/2555/oj/eng"),
 ("DORA", "EU 2022/2554", "Digital operational resilience for the financial sector - ICT risk, resilience testing, third-party providers.", "https://eur-lex.europa.eu/eli/reg/2022/2554/oj/eng"),
 ("GDPR", "EU 2016/679", "Personal data protection - records of processing, DPIA, DPO, breach notification to the supervisory authority.", "https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng"),
 ("AI Act", "EU 2024/1689", "Risk-based classification of AI systems, obligations for providers and deployers, governance and oversight.", "https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng"),
 ("ISO/IEC 27001", "2022", "Information security management system - 93 Annex A controls and the Statement of Applicability. Read our guide.", "/en/blog/iso-27001-and-the-cybersecurity-act/"),
 ("ISO 22301", "2019", "Business continuity management system - BIA, RTO/RPO, plans and exercising. Read our guide.", "/en/blog/bia-that-produces-a-usable-rto/"),
]

EN_SECTORS = [
 ("Banking and finance", "CSA AND DORA, PARALLEL OBLIGATIONS &middot; CNB AND HANFA"),
 ("Insurance", "DORA FOR ICT RISK &middot; ISO 27001 AND BUSINESS CONTINUITY"),
 ("Energy", "GENERATION, TRANSMISSION, DISTRIBUTION, GAS AND OIL"),
 ("Healthcare and pharma", "ANNEX I &middot; HIGH-CRITICALITY SECTOR &middot; NCSC-HR"),
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
  "The category is determined by sector and by the size of the entity, subject to exceptions. Essential entities are subject to an independent cybersecurity audit, while important entities carry out a self-assessment. You are notified of the categorisation in writing by the competent authority. Size is not the criterion for state administration bodies and operators of the state information infrastructure (essential), for local and regional self-government and the education system (important), nor for trust service providers, DNS service providers and the national domain registry. In addition, Article 11 allows any entity to be categorised regardless of size if it is the sole provider of an essential service or if its disruption would significantly affect public safety, security or health.",
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
 ("Do you perform audits and certification?",
  "We perform internal audits of management systems, compliance reviews and a documentation review that simulates the audit process. We do not perform ISO certification - by definition that is carried out by an accredited certification body, and whoever built a system may not certify it. The independent cybersecurity audit of essential entities under the Act is carried out by a provider holding the prescribed authorisation, and for state administration bodies by the competent authority.",
  None),
]

EN_AUTHORITIES = [
 ('SOA', 'https://www.soa.hr/', 'central cybersecurity authority', None, None),
 ('NCSC-HR', 'https://www.ncsc.hr/', 'incident reporting', None, None),
 ('ZSIS', 'https://www.zsis.hr/', 'state administration bodies', 'UVNS', 'https://www.uvns.hr/'),
 ('AZOP', 'https://azop.hr/', 'personal data breaches', None, None),
 ('HNB', 'https://www.hnb.hr/', 'DORA, financial sector', 'HANFA', 'https://www.hanfa.hr/'),
 ('HAKOM', 'https://www.hakom.hr/', 'digital infrastructure sector', None, None),
]

EN_CLIENTS = [
 ("Banking and finance", ["Zagreb Stock Exchange", "Šted banka", "Partner banka", "Euroleasing", "Fintastic", "Krypto Investment Partners"]),
 ("Insurance", ["Croatia osiguranje", "Adriatic osiguranje", "Sunce osiguranje", "UNIQA osiguranje", "ANO Insurance Solutions"]),
 ("Energy and industry", ["HROTE", "E.ON", "INA", "IHC Engineering Croatia", "TEHMA", "MCZ"]),
 ("IT and digital services", ["APIS-IT", "Rocket DBS", "SmartGroup HR Solutions", "SmartGroup Recruitment", "BCC Services", "Digital Assembly", "AMODO", "Cooperante", "TPA Hrvatska"]),
 ("Food industry", ["Franck d.d.", "Pan-pek", "Mlinar", "Intersnack", "Offertissima"]),
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
<p>The Act then lists groups where <strong>size is not a criterion at all</strong>. Essential regardless of size: qualified trust service providers, the national top-level domain registry and DNS service providers, e-invoice exchange intermediaries, entities designated as critical under the critical infrastructure legislation, state administration bodies and operators of the state information infrastructure. Important regardless of size: trust service providers not classified as essential, providers of public electronic communications networks and services not classified as essential, local and regional self-government units, and entities in the education system.</p>
<p>In addition, <strong>Article 11</strong> allows any entity listed in the annexes to be categorised regardless of size where it is the sole provider of a service essential to maintaining critical societal or economic activities, where its disruption could significantly affect public safety, security or health, could cause systemic risk, or where it is significant because of its particular importance nationally, regionally or locally. That article is why a small institution can be an essential entity just as a large one is, and it is the most common source of surprise.</p>
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
 sources=[('Cybersecurity Act, OG 14/2024 (Croatian)', 'https://narodne-novine.nn.hr/clanci/sluzbeni/2024_02_14_254.html'),
          ('Cybersecurity Regulation, OG 135/2024 (Croatian)', 'https://narodne-novine.nn.hr/clanci/sluzbeni/2024_11_135_2217.html'),
          ('Directive (EU) 2022/2555 (NIS2)', 'https://eur-lex.europa.eu/eli/dir/2022/2555/oj/eng')]))

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
          ('Directive (EU) 2022/2555 (NIS2), Art. 21', 'https://eur-lex.europa.eu/eli/dir/2022/2555/oj/eng')]))

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
 sources=[('Cybersecurity Act, OG 14/2024 (Croatian)', 'https://narodne-novine.nn.hr/clanci/sluzbeni/2024_02_14_254.html'),
          ('Cybersecurity Regulation, OG 135/2024 (Croatian)', 'https://narodne-novine.nn.hr/clanci/sluzbeni/2024_11_135_2217.html'),
          ('Regulation (EU) 2016/679 (GDPR), Art. 33', 'https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng')]))

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
          ('ISO/IEC 27001:2022 - Information security management systems', '/en/blog/iso-27001-and-the-cybersecurity-act/')]))

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
 sources=[('ISO/IEC 27001:2022, Annex A', '/en/blog/iso-27002-2022-control-attributes/'),
          ('ISO/IEC 27002:2022 - Information security controls', '/en/blog/iso-27002-2022-control-attributes/'),
          ('ISO/IEC 27001:2022/Amd 1:2024 - climate action changes', '/en/blog/iso-27002-2022-control-attributes/')]))

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
 sources=[('ISO 22301:2019 - Business continuity management systems', '/en/blog/bia-that-produces-a-usable-rto/'),
          ('ISO/TS 22317 - Guidelines for business impact analysis', '/en/blog/bia-that-produces-a-usable-rto/'),
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
 sources=[('Regulation (EU) 2022/2554 (DORA)', 'https://eur-lex.europa.eu/eli/reg/2022/2554/oj/eng'),
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
          ('ISO/IEC 27001:2022, Annex A', '/en/blog/iso-27002-2022-control-attributes/')]))

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
          ('ISO/IEC 27002:2022 - control attributes', '/en/blog/iso-27002-2022-control-attributes/')]))

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
          ('ISO/IEC 27002:2022 - technological controls', '/en/blog/iso-27002-2022-control-attributes/'),
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
 sources=[('Regulation (EU) 2024/1689 (AI Act)', 'https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng'),
          ('Regulation (EU) 2016/679 (GDPR)', 'https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng')]))

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
 sources=[('Regulation (EU) 2024/1689 (AI Act), Art. 4 and 5', 'https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng'),
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
 sources=[('Regulation (EU) 2024/1689 (AI Act)', 'https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng'),
          ('Cybersecurity Regulation, OG 135/2024, Annex II, measures 2 and 8 (Croatian)', 'https://narodne-novine.nn.hr/clanci/sluzbeni/2024_11_135_2217.html'),
          ('ISO/IEC 27001:2022, Annex A - asset management', '/en/blog/iso-27001-and-the-cybersecurity-act/')]))

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
 sources=[('Regulation (EU) 2024/1689 (AI Act)', 'https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng'),
          ('NIST Cybersecurity Framework 2.0 - Detect and Respond functions', 'https://www.nist.gov/cyberframework'),
          ('Recommendations for systematic log collection, NCSC-HR (Croatian)', 'https://www.ncsc.hr/')]))

# ══════════════════════════════════════════════════════════════════
# Engleski: kazne, revizija, sigurnosna kultura, korelacija
# ══════════════════════════════════════════════════════════════════
ARTICLES_EN.append(dict(
 slug="penalties-under-the-cybersecurity-act", cat="CSA / NIS2", catkey="csa",
 date="2026-06-23", read=8,
 title="Penalties under the Croatian Cybersecurity Act: who pays, how much, and why it is personal",
 lead="Up to EUR 10 million or 2 per cent of global turnover for essential entities. But the figure that changes the conversation with a board is the other one: members of the management body are liable personally, out of their own pocket.",
 desc="The penalty provisions of the Croatian Cybersecurity Act: ranges for essential and important entities, personal liability of management body members, the circumstances affecting the amount, and the rule against double punishment with the data protection authority.",
 body='''
<p>In conversations about compliance with the Croatian Cybersecurity Act the figure most often quoted is ten million euro. It is accurate but incomplete, and on its own it rarely moves anything.</p>
<p>What moves things is the provision alongside it: <strong>the individuals responsible for managing the measures are liable personally</strong>.</p>

<h2>The ranges</h2>
<div class="tbl-wrap">
  <table>
    <thead><tr><th>Who</th><th>Range</th><th>Alternative</th></tr></thead>
    <tbody>
      <tr><td><strong>Essential entity</strong></td><td>EUR 10,000 - 10,000,000</td><td>0.5 % to 2 % of total annual worldwide turnover</td></tr>
      <tr><td><strong>Important entity</strong></td><td>EUR 5,000 - 7,000,000</td><td>0.2 % to 1.4 % of total annual worldwide turnover</td></tr>
      <tr><td><strong>Responsible individual, essential entity</strong></td><td class="num">EUR 1,000 - 6,000</td><td>-</td></tr>
      <tr><td><strong>Responsible individual, important entity</strong></td><td class="num">EUR 500 - 3,000</td><td>-</td></tr>
      <tr><td><strong>Failure to deliver data to NCSC-HR</strong></td><td>EUR 2,000 - 20,000</td><td>responsible individual EUR 200 - 1,000</td></tr>
    </tbody>
  </table>
</div>
<p>For legal persons <strong>the higher of the two figures applies</strong> - the fixed amount or the percentage of turnover. For an entity with EUR 400 million turnover the ceiling is not 10 million but 8 million by percentage, so the fixed amount governs. Above roughly half a billion, the percentage overtakes it.</p>

<h2>Who counts as a "responsible individual"</h2>
<p>Article 29 is precise, and broader than expected. Responsible for implementing the measures are:</p>
<ul>
  <li><strong>members of the management bodies</strong> of essential and important entities</li>
  <li><strong>heads of state administration bodies</strong> and other state bodies</li>
  <li><strong>executive bodies</strong> of local and regional self-government units</li>
</ul>
<p>Paragraph 4 extends the circle to other individuals who, on the basis of authority to supervise the conduct of business, a power of attorney or another authority to represent, <strong>take part in decisions about the measures or in their implementation</strong>.</p>
<div class="callout">
  <div class="c-label">What this means in practice</div>
  <p>A procurator, a supervisory board member deciding on security investment, or an IT director holding a power of attorney can all fall within the circle of personal liability. That liability cannot be transferred by contract to a supplier or a consultant.</p>
</div>

<h2>Two duties a board cannot delegate</h2>
<p>Article 29(2) requires responsible individuals to <strong>approve</strong> the measures and to <strong>verify their implementation</strong>. Paragraph 3 adds a duty that is routinely overlooked:</p>
<ul>
  <li>responsible individuals must <strong>themselves attend appropriate training</strong></li>
  <li>and must enable staff to attend training</li>
</ul>
<p>A board that has not been trained does not meet a statutory duty, however good the system beneath it. It is one of the few requirements where the evidence has to carry a board member's name.</p>

<h2>What affects the amount</h2>
<p>Article 85 lists the circumstances the competent authority takes into account:</p>
<ul>
  <li>the seriousness of the breach and the importance of the provision breached</li>
  <li>its duration</li>
  <li>previous breaches by the same entity</li>
  <li>the damage caused, including financial loss, effects on other services and the number of affected users</li>
  <li>whether the entity acted <strong>with intent or through negligence</strong></li>
  <li>measures taken to prevent or mitigate the damage</li>
  <li>adherence to codes of conduct and certification conditions</li>
  <li><strong>the level of cooperation of the responsible individuals with the authorities</strong></li>
</ul>
<div class="callout">
  <div class="c-label">What counts expressly as a serious breach</div>
  <p>Paragraph 2 of the same article lists: repeated breaches, <strong>failure to report or to resolve significant incidents</strong>, failure to remedy deficiencies when ordered to, and <strong>obstructing or impeding an audit</strong>.</p>
  <p>In other words: a missed incident notification and obstruction of an audit are not technical oversights but aggravating circumstances that raise the penalty in themselves.</p>
</div>

<h2>You will not be punished twice for the same conduct</h2>
<p>A provision rarely mentioned and worth knowing: where the data protection authority has already imposed an administrative fine under the GDPR for a personal data breach arising from <strong>the same conduct</strong>, no misdemeanour charge or order may be issued under the Act for that same conduct.</p>
<p>This does not merge the obligations - it prevents double punishment for one act. Notification to the competent CSIRT and notification to the data protection authority remain two separate duties with their own deadlines.</p>

<h2>How to raise this with a board</h2>
<ol>
  <li><strong>Personal liability.</strong> A range of EUR 1,000 to 6,000 is not much money for a company, but it is very concrete for the individual paying it.</li>
  <li><strong>Cooperation is scored.</strong> The level of cooperation with the authority expressly affects the penalty. An organisation that reports its own failure with a remediation plan is not in the same position as one that waits for an inspection.</li>
  <li><strong>Board training is a statutory duty</strong>, not a recommendation. It is the easiest item to close and the most commonly left open.</li>
</ol>

<div class="note">
  <p>This is an informative overview of the penalty provisions, not legal advice. The amount in any given case depends on the circumstances in Article 85 and on the decision of the authority or court. To assess your own exposure, start with the <a href="/en/tools/entity-categorisation-check/">categorisation check</a> - the category determines which range applies.</p>
</div>
''',
 sources=[('Cybersecurity Act, OG 14/2024, Art. 29, 85 and the penalty provisions (Croatian)', 'https://narodne-novine.nn.hr/clanci/sluzbeni/2024_02_14_254.html'),
          ('Regulation (EU) 2016/679 (GDPR)', 'https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng'),
          ('Directive (EU) 2022/2555 (NIS2)', 'https://eur-lex.europa.eu/eli/dir/2022/2555/oj/eng')]))

ARTICLES_EN.append(dict(
 slug="cybersecurity-audit-how-it-works", cat="Self-assessment", catkey="selfassessment",
 date="2026-07-21", read=7,
 title="The cybersecurity audit: who may perform it and how it runs",
 lead="Essential entities do not self-assess - they undergo an independent audit. It is carried out by a provider holding the prescribed authorisation, and for state administration bodies by the competent authority. Here is how it runs and what usually is not accepted.",
 desc="How the independent cybersecurity audit of essential entities runs: who may perform it, the steps of the process, how the auditor scores documentation and implementation, and which evidence is most often rejected.",
 body='''
<p>The difference between an essential and an important entity comes down to one sentence: important entities self-assess, essential entities undergo an <strong>independent cybersecurity audit</strong>. That is a difference in cost, in time, and in who holds the pen.</p>

<h2>Who may perform it</h2>
<p>The audit cannot be run by any consultant. It is performed by a service provider holding the prescribed authorisation, and for state administration bodies by the competent information security authority.</p>
<div class="callout">
  <div class="c-label">Why that separation protects you</div>
  <p>Whoever built the system may not also assess it. If someone offers you both the implementation and the formal audit, that is not a saving but a conflict of interest - and the findings of such an audit carry no weight with the authority.</p>
</div>

<h2>How the process runs</h2>
<ol>
  <li><strong>Notice and scoping.</strong> Which systems, processes and locations are covered, and which level of implementation applies to your category.</li>
  <li><strong>Audit plan.</strong> Schedule, interviewees, and the documentation to be submitted in advance.</li>
  <li><strong>Documentation review.</strong> Policies, procedures, registers and records - before the interviews, not instead of them.</li>
  <li><strong>Interviews.</strong> With the board, with process owners and with the people who actually perform the measures. This is where the gap between what is written and what is done shows fastest.</li>
  <li><strong>Evidence sampling.</strong> The auditor picks a sample and asks for evidence for each selected control. Not everything is checked; the sample supports a conclusion about the whole.</li>
  <li><strong>Findings and deadlines.</strong> A report setting out findings, their seriousness and the time allowed to remedy them.</li>
</ol>

<h2>How the auditor scores</h2>
<p>Scoring uses the same framework as the self-assessment: a score per control, with a threshold each control must reach and an additional average threshold per sub-measure.</p>
<p>Practically important: <strong>documentation and implementation are scored separately</strong>. A perfect policy that is not applied does not produce a high score, and good practice without records produces no score at all - because it cannot be evidenced.</p>

<h2>What usually is not accepted</h2>
<ul>
  <li><strong>A document with no date and no approval.</strong> A policy nobody adopted is a draft, not a policy.</li>
  <li><strong>A record created after the audit was announced.</strong> It shows in the dates, and in what is missing for the period before.</li>
  <li><strong>A screenshot instead of a record.</strong> An image of the current state does not evidence that the control operated throughout the period.</li>
  <li><strong>A risk register with no owners and no changes.</strong> If it has not changed in a year, it is not used in decision-making.</li>
  <li><strong>A continuity plan that has never been exercised.</strong> Without an exercise record, the plan documents intent, not capability.</li>
  <li><strong>Training without records.</strong> "Everyone attended" is not evidence; a list with names and dates is.</li>
  <li><strong>Supplier measures with no contractual basis.</strong> A provider's verbal assurance does not replace a clause.</li>
</ul>
<div class="callout">
  <div class="c-label">The common denominator</div>
  <p>Nearly all of these have the same cause: the evidence is being manufactured at the moment of the audit. Most measures are evidenced by records that arise during the cycle, so they cannot be produced retrospectively. That is why twelve months is not generous.</p>
</div>

<h2>How to prepare</h2>
<ol>
  <li><strong>Score yourself against the same framework.</strong> An internal review simulating the audit produces the same findings, without the consequences.</li>
  <li><strong>Walk the documentation chronologically.</strong> Is there a record for every month of the period, or only for the last one?</li>
  <li><strong>Check what cannot be fixed quickly.</strong> The annual board reporting cycle, the continuity exercise and training records all need calendar time.</li>
  <li><strong>Prepare the interviewees.</strong> Not to learn answers, but to know where things are - an auditor can tell the difference.</li>
</ol>

<div class="note">
  <p>We carry out internal audits and reviews that simulate the audit process. The formal independent audit of essential entities is performed by an authorised provider. More on what we do at <a href="/en/services/audits-and-internal-reviews/">Audits and internal reviews</a>, and the scoring framework is explained in <a href="/en/blog/how-self-assessment-is-scored/">How the self-assessment is actually scored</a>.</p>
</div>
''',
 sources=[('Cybersecurity Act, OG 14/2024 (Croatian)', 'https://narodne-novine.nn.hr/clanci/sluzbeni/2024_02_14_254.html'),
          ('Cybersecurity Regulation, OG 135/2024 (Croatian)', 'https://narodne-novine.nn.hr/clanci/sluzbeni/2024_11_135_2217.html'),
          ('ZSIS - Annex B, Framework for the evaluation of measures', 'https://www.zsis.hr/UserDocsImages/Samoprocjena/Prilog%20B%20-%20Okvir%20za%20evaluaciju.pdf')]))

ARTICLES_EN.append(dict(
 slug="security-culture-and-the-human-factor", cat="Human factor", catkey="people",
 date="2026-08-11", read=6,
 title="Security culture: why training does not change behaviour, and what does",
 lead="An annual presentation about phishing produces a record, not a change. Measure 5 requires awareness raising, but what actually gets measured is behaviour - and behaviour moves on different levers.",
 desc="How to approach security awareness so it changes behaviour rather than just producing records: what to measure, building a reporting culture, and the link to measure 5 of Annex II.",
 body='''
<p>Measure 5 of Annex II requires basic cyber hygiene practices and staff awareness raising. Most organisations satisfy it with an annual presentation and a list of signatures.</p>
<p>It formally passes. Behaviour does not change, and the next incident arrives through the same channel as the last one.</p>

<h2>Why conventional training fails</h2>
<h3>It teaches signals that have disappeared</h3>
<p>Material that teaches people to spot phishing by poor language and a strange address is out of date. Language errors are no longer a signal - messages are grammatically flawless and tailored to the recipient. What remains as a signal is <strong>context</strong>: an unexpected request, time pressure, a change of channel, a request for an exception to a rule.</p>
<h3>It measures attendance, not behaviour</h3>
<p>Records answer who was present. They do not answer whether that person would act differently. Those are different things, and only the second one shows up in an incident.</p>
<h3>It punishes reporting</h3>
<p>This is the biggest problem and the least discussed. In an organisation where the person who clicks a phishing link faces ridicule or a conversation with their manager, nobody will report next time - they will stay quiet and hope. Time to detection is then measured in weeks rather than minutes.</p>

<div class="callout">
  <div class="c-label">One question that reveals the state of things</div>
  <p>Ask a few staff: "If you had clicked a suspicious link yesterday, who would you tell and what do you think would happen?" The answer to the second half tells you more about your resilience than any training record.</p>
</div>

<h2>What actually changes behaviour</h2>
<ol>
  <li><strong>Short and frequent, instead of long and once.</strong> Fifteen minutes a quarter with one concrete scenario beats two hours once a year.</li>
  <li><strong>Simulations with feedback, not consequences.</strong> Whoever clicks gets an explanation immediately, in place. Results are reported in aggregate, never per person.</li>
  <li><strong>Reporting is rewarded.</strong> Anyone who reports a suspicious message, even one that turns out harmless, should be told they did the right thing. It is the only lever that shortens time to detection.</li>
  <li><strong>Roles get their own content.</strong> Finance needs to know about bank detail change fraud, IT about attacks on privileged accounts, the board about fake executive instruction fraud.</li>
  <li><strong>A procedure instead of vigilance.</strong> "Be careful with payments" does not work. "Any payment above X, or any change of bank details, is confirmed by telephone on the number in our register, never the number in the email" does work, because it does not depend on one person's judgement under pressure.</li>
</ol>

<h2>What to measure</h2>
<div class="tbl-wrap">
  <table>
    <thead><tr><th>Instead of</th><th>Measure</th></tr></thead>
    <tbody>
      <tr><td>Percentage of staff who completed training</td><td>Share of simulated messages reported</td></tr>
      <tr><td>Quiz score</td><td>Average time to first report</td></tr>
      <tr><td>Number of sessions held</td><td>Reports from teams that never reported before</td></tr>
      <tr><td>Training satisfaction score</td><td>Share of payments verified through a second channel</td></tr>
    </tbody>
  </table>
</div>
<p>The left column satisfies the record. The right column shows whether resilience is changing.</p>

<h2>The link to your obligations</h2>
<p>Awareness raising falls under measure 5, and Article 29(3) of the Act requires responsible individuals to attend appropriate training themselves. In addition, Article 4 of the AI Act requires a sufficient level of AI literacy for staff operating AI systems.</p>
<p>All three require <strong>records</strong>. The good news is that a programme which genuinely changes behaviour produces richer records than one that does not, because it has more touchpoints across the year.</p>

<div class="note">
  <p>Role-based workshops - for the board, for IT and for all staff - are described on the <a href="/en/speaking/">Lectures and workshops</a> page. Each produces records that satisfy measure 5.</p>
</div>
''',
 sources=[('Cybersecurity Regulation, OG 135/2024, Annex II, measure 5 (Croatian)', 'https://narodne-novine.nn.hr/clanci/sluzbeni/2024_11_135_2217.html'),
          ('Cybersecurity Act, OG 14/2024, Art. 29(3) (Croatian)', 'https://narodne-novine.nn.hr/clanci/sluzbeni/2024_02_14_254.html'),
          ('Regulation (EU) 2024/1689 (AI Act), Art. 4', 'https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng')]))

ARTICLES_EN.append(dict(
 slug="correlation-of-measures-to-standards", cat="CSA / NIS2", catkey="csa",
 date="2026-02-24", read=7,
 title="The correlation overview: the document that halves your work",
 lead="Article 49 of the Regulation requires a correlation overview mapping every sub-measure onto ISO 27001, ISO 27002, ISO 22301, NIST CSF 2.0, NIST SP 800-53 and CIS v8. Organisations that ignore it write documentation they already have.",
 desc="What the correlation overview required by Article 49 of the Croatian Cybersecurity Regulation is, which standards it maps to, and how to use it so existing ISO or NIST documentation is not written twice.",
 body='''
<p>The most expensive mistake in a compliance project is not a missed control. It is documentation written a second time, because nobody checked what already existed.</p>
<p>The Regulation anticipated this. Article 49 provides for a <strong>correlation overview of the measures</strong>, mapping every sub-measure of Annex II onto recognised standards and good practice.</p>

<h2>What it maps to</h2>
<div class="tbl-wrap">
  <table>
    <thead><tr><th>Source</th><th>What it covers</th></tr></thead>
    <tbody>
      <tr><td><strong>ISO/IEC 27001:2022</strong></td><td>The information security management system framework</td></tr>
      <tr><td><strong>ISO/IEC 27002:2022</strong></td><td>Implementation guidance for the controls, in four themes</td></tr>
      <tr><td><strong>ISO/IEC 22301:2019</strong></td><td>Business continuity</td></tr>
      <tr><td><strong>NIST CSF 2.0</strong></td><td>Six functions, including the new Govern</td></tr>
      <tr><td><strong>NIST SP 800-53</strong></td><td>An extensive set of technical and organisational controls</td></tr>
      <tr><td><strong>CIS v8</strong></td><td>Practical controls, including cloud and mobile</td></tr>
      <tr><td><strong>ZSIS control catalogue</strong></td><td>The 132 controls used in the self-assessment</td></tr>
    </tbody>
  </table>
</div>

<div class="callout">
  <div class="c-label">What this means in practice</div>
  <p>If you hold ISO 27001, the correlation overview tells you, for every sub-measure, which of your existing controls are thematically related. That is not proof of compliance, but it is a list of the places where the evidence probably already exists. Instead of 99 empty fields you start with 99 fields that have a candidate.</p>
</div>

<h2>The trap the overview itself points out</h2>
<p>The guidance notes something easy to miss: <strong>the scope of each control from the international standards exceeds the scope of the sub-measure being mapped</strong>. A control from ISO 27002 appearing next to sub-measure 3.2 also covers things that sub-measure does not require, and may not cover everything it does.</p>
<p>The consequence: mapping is a starting point, not a conclusion. A tick in the correlation table is not evidence. Evidence is a record answering what the sub-measure requires, to the extent it requires it.</p>

<h2>How to use it so it genuinely saves work</h2>
<ol>
  <li><strong>Start from your Statement of Applicability.</strong> For each applicable control, see which sub-measures it appears against in the correlation. That gives you the reverse mapping - from what you have towards what is required.</li>
  <li><strong>Mark three states, not two.</strong> Covered, partly covered, not covered. Partly is the largest group and the most useful, because it is resolved by extending an existing document rather than writing a new one.</li>
  <li><strong>Check the level.</strong> A control satisfying the basic level need not satisfy the medium one. The correlation does not distinguish levels - you must.</li>
  <li><strong>Record the reasoning for every link.</strong> At verification you will have to explain why you considered an existing document to cover a sub-measure. A sentence written at the time of mapping is worth more than a reconstruction six months later.</li>
</ol>

<h2>Who benefits most</h2>
<ul>
  <li><strong>An organisation with ISO 27001 and 22301</strong> - the greatest benefit. Much of measures 2, 3, 7, 8 and 12 already has an evidential basis.</li>
  <li><strong>An organisation working to CIS v8</strong> - technical measures 5, 6, 7 and 9 are largely covered; the organisational ones are not.</li>
  <li><strong>An organisation reporting against NIST CSF</strong> - the correlation is also a bridge to board reporting, since the six functions remain as the presentation frame.</li>
  <li><strong>An organisation with none of these</strong> - still useful as a guide to what to write, because it points to controls describing how a sub-measure is usually implemented.</li>
</ul>

<div class="note">
  <p>The correlation overview is an aid, not law. The authority assesses compliance with the measures of Annex II and the controls of the catalogue, not with the standards the overview points to. An ISO 27001 certificate replaces neither the self-assessment nor the audit.</p>
</div>
''',
 sources=[('Cybersecurity Regulation, OG 135/2024, Art. 49 (Croatian)', 'https://narodne-novine.nn.hr/clanci/sluzbeni/2024_11_135_2217.html'),
          ('Guidelines for the correlation overview of cybersecurity measures, NCSC-HR', 'https://www.ncsc.hr/'),
          ('ZSIS - Annex C, Control catalogue', 'https://www.zsis.hr/UserDocsImages/Samoprocjena/Prilog%20C%20-%20Katalog%20kontrola.pdf')]))

# ══════════════════════════════════════════════════════════════════
# STRANICE SEKTORA
# ══════════════════════════════════════════════════════════════════
# kljuc, slug HR, slug EN, ime HR, ime EN, prilog, csirt, tijelo HR, tijelo EN
SEKTORI = [
 dict(k="bankarstvo", hr="bankarstvo-i-financije", en="banking-and-finance",
   nHR="Bankarstvo i financije", nEN="Banking and finance", prilog=1, csirt="cert",
   tHR='<a href="https://www.hnb.hr/" target="_blank" rel="noopener">Hrvatska narodna banka</a> i <a href="https://www.hanfa.hr/" target="_blank" rel="noopener">HANFA</a>', tEN='<a href="https://www.hnb.hr/" target="_blank" rel="noopener">Croatian National Bank</a> and <a href="https://www.hanfa.hr/" target="_blank" rel="noopener">HANFA</a>',
   qHR="ZKS I DORA, USPOREDNE OBVEZE", qEN="CSA AND DORA, PARALLEL OBLIGATIONS",
   leadHR="Financijski sektor je jedini koji istovremeno nosi dva režima. DORA detaljnije uređuje IKT rizik, ali ne ukida obveze iz Zakona o kibernetičkoj sigurnosti. Posao se radi jednom, izvještava na dvije strane.",
   leadEN="Financial services is the only sector carrying two regimes at once. DORA governs ICT risk in more detail but does not displace the obligations under the Cybersecurity Act. The work is done once and reported in two directions.",
   mjHR=[("03","Upravljanje rizicima","DORA i Uredba traže isti registar rizika. Dvije metodologije znače dva registra koja se raziđu."),
         ("08","Sigurnost lanca opskrbe","DORA registar informacija o ugovorima s pružateljima IKT usluga je najzahtjevniji dio, i pada na kvaliteti podataka, ne na propisu."),
         ("11","Postupanje s incidentima","Prijava nadležnom CSIRT-u i prijava prema DORA-i teku usporedno, uz vlastite obrasce i rokove."),
         ("12","Kontinuitet poslovanja","DORA traži testiranje otpornosti, što je više od klasičnog plana oporavka.")],
   mjEN=[("03","Risk management","DORA and the Regulation require the same risk register. Two methodologies mean two registers that diverge."),
         ("08","Supply chain security","The DORA register of information on ICT provider contracts is the hardest part, and it fails on data quality, not on the rules."),
         ("11","Incident handling","Notification to the competent CSIRT and DORA reporting run in parallel, with their own forms and deadlines."),
         ("12","Business continuity","DORA requires resilience testing, which goes beyond a classical recovery plan.")],
   nalHR=["Registar informacija popunjen ručno iz tri nepovezana izvora - nabave, informatike i financija",
          "Ugovori s pružateljima usluga u oblaku bez obveze prijave podugovaratelja",
          "Registar rizika koji ne pokriva rizike trećih strana",
          "Testiranje oporavka koje se dokumentira, ali se ne mjeri vrijeme"],
   nalEN=["A register of information populated by hand from three unconnected sources - procurement, IT and finance",
          "Cloud provider contracts with no obligation to disclose subcontractors",
          "A risk register that does not cover third-party risk",
          "Recovery testing that is documented but never timed"],
   clHR=["dora-registar-informacija","registar-rizika-koji-prolazi-provjeru","znacajan-incident-pet-obavijesti-pixi"],
   clEN=["dora-register-of-information","risk-register-that-passes-review","incident-reporting-deadlines"]),

 dict(k="osiguranje", hr="osiguranje", en="insurance",
   nHR="Osiguranje", nEN="Insurance", prilog=1, csirt="cert",
   tHR='<a href="https://www.hanfa.hr/" target="_blank" rel="noopener">HANFA</a>', tEN='<a href="https://www.hanfa.hr/" target="_blank" rel="noopener">HANFA</a>',
   qHR="DORA ZA IKT RIZIK &middot; ISO 27001 I KONTINUITET", qEN="DORA FOR ICT RISK &middot; ISO 27001 AND CONTINUITY",
   leadHR="Osiguravatelji podliježu DORA-i kao i ostali financijski subjekti, uz dodatnu složenost: velik broj vanjskih posrednika i agenata koji obrađuju osobne podatke ugovaratelja.",
   leadEN="Insurers fall under DORA like other financial entities, with added complexity: a large network of external intermediaries and agents processing policyholder data.",
   mjHR=[("02","Upravljanje imovinom","Podaci ugovaratelja i podaci o štetama su kritična imovina, često raspršena po naslijeđenim sustavima."),
         ("04","Digitalni identiteti","Vanjski posrednici imaju pristup sustavima, a oduzimanje prava pri prestanku suradnje rijetko je automatizirano."),
         ("08","Lanac opskrbe","Posrednici, procjenitelji šteta i pružatelji usluga u oblaku ulaze u istu procjenu rizika."),
         ("10","Kriptografija","Zdravstveni podaci u policama i prijavama šteta traže zaštitu u prijenosu i mirovanju.")],
   mjEN=[("02","Asset management","Policyholder and claims data are critical assets, often scattered across legacy systems."),
         ("04","Digital identities","External intermediaries have system access, and revoking it when the relationship ends is rarely automated."),
         ("08","Supply chain","Intermediaries, loss adjusters and cloud providers enter the same risk assessment."),
         ("10","Cryptography","Health data in policies and claims requires protection in transit and at rest.")],
   nalHR=["Aktivni računi posrednika s kojima je suradnja prestala prije više godina",
          "Naslijeđeni sustavi za obradu šteta bez podrške proizvođača, bez odluke uprave o riziku",
          "Zdravstveni podaci u testnim okruženjima, bez maskiranja",
          "Procjena rizika koja ne obuhvaća posrednike"],
   nalEN=["Active intermediary accounts from relationships that ended years ago",
          "Legacy claims systems past vendor support, with no board decision on the risk",
          "Health data in test environments, unmasked",
          "A risk assessment that does not cover intermediaries"],
   clHR=["dora-registar-informacija","iso-27001-i-zks","bia-koja-daje-upotrebljiv-rto"],
   clEN=["dora-register-of-information","iso-27001-and-the-cybersecurity-act","bia-that-produces-a-usable-rto"]),

 dict(k="energetika", hr="energetika", en="energy",
   nHR="Energetika", nEN="Energy", prilog=1, csirt="ncsc", tHR="", tEN="",
   qHR="PROIZVODNJA, PRIJENOS, DISTRIBUCIJA, PLIN I NAFTA", qEN="GENERATION, TRANSMISSION, DISTRIBUTION, GAS AND OIL",
   leadHR="Energetika je sektor u kojem se najjasnije vidi razlika između informacijskih i operativnih sustava. Kontrola koja je u uredskoj mreži rutinska u pogonu može zaustaviti proizvodnju.",
   leadEN="Energy is where the difference between information and operational systems shows most clearly. A control that is routine on the office network can halt production in the plant.",
   mjHR=[("06","Sigurnost mreže","Segmentacija je najisplativija kontrola jer ne dira same uređaje - odvaja proizvodnu od uredske mreže."),
         ("05","Kibernetička higijena","Zakrpe se ne mogu primijeniti izvan planiranog zastoja, pa rizik traži nadoknadne kontrole i pisanu odluku."),
         ("07","Kontrola pristupa","Trajni udaljeni pristup dobavljača opreme s dijeljenim računom najčešći je stvarni rizik."),
         ("12","Kontinuitet poslovanja","Oporavak znači i sigurno pokretanje procesa, što je operativni postupak, a ne informatički.")],
   mjEN=[("06","Network security","Segmentation is the highest-return control because it does not touch the devices - it separates production from the office network."),
         ("05","Cyber hygiene","Patches cannot be applied outside a planned outage, so the risk needs compensating controls and a written decision."),
         ("07","Access control","Permanent vendor remote access on a shared account is the most common real risk."),
         ("12","Business continuity","Recovery also means safely restarting the process, which is an operational procedure, not an IT one.")],
   nalHR=["Proizvodna i uredska mreža bez stvarne segmentacije",
          "Udaljeni pristup dobavljača opreme bez odobravanja po zahtjevu i bez zapisa",
          "Sustavi bez podrške proizvođača, bez procjene rizika i odluke uprave",
          "Popis OT uređaja u dokumentaciji stariji od stvarnog stanja"],
   nalEN=["Production and office networks with no real segmentation",
          "Vendor remote access without per-request approval and without records",
          "Systems past vendor support, with no risk assessment or board decision",
          "An OT device list in the documentation older than reality"],
   clHR=["ot-sustavi-i-zks","prioritetne-preporuke-ncsc","bia-koja-daje-upotrebljiv-rto"],
   clEN=["active-directory-attack-paths","bia-that-produces-a-usable-rto","iso-27001-and-the-cybersecurity-act"]),

 dict(k="zdravstvo", hr="zdravstvo-i-farmacija", en="healthcare-and-pharma",
   nHR="Zdravstvo i farmacija", nEN="Healthcare and pharma", prilog=1, csirt="ncsc", tHR="", tEN="",
   qHR="BOLNICE, DOMOVI ZDRAVLJA, LJEKARNE, PROIZVODNJA LIJEKOVA", qEN="HOSPITALS, CLINICS, PHARMACIES, MEDICINAL PRODUCTS",
   leadHR="Zdravstvo je u Prilogu I., pa se primjenjuje kriterij veličine. Ali članak 11. dopušta razvrstavanje neovisno o veličini svakoj ustanovi čiji bi ispad znatno utjecao na javno zdravlje - a to u zdravstvu nije rijedak slučaj.",
   leadEN="Health is in Annex I, so the size criterion applies. But Article 11 allows categorisation regardless of size for any institution whose disruption would significantly affect public health - which in healthcare is not unusual.",
   mjHR=[("02","Upravljanje imovinom","Medicinski uređaji povezani na mrežu dio su imovine, a rijetko su u inventaru informatike."),
         ("10","Kriptografija","Podaci o zdravlju su posebna kategorija prema Općoj uredbi i traže zaštitu u prijenosu i mirovanju."),
         ("11","Postupanje s incidentima","Incident sa zdravstvenim podacima gotovo uvijek pokreće i usporednu prijavu AZOP-u u 72 sata."),
         ("12","Kontinuitet poslovanja","Nedostupnost bolničkog sustava nije poslovna šteta nego rizik za pacijente.")],
   mjEN=[("02","Asset management","Networked medical devices are assets, and are rarely in the IT inventory."),
         ("10","Cryptography","Health data is a special category under the GDPR and requires protection in transit and at rest."),
         ("11","Incident handling","An incident involving health data almost always triggers a parallel 72-hour notification to the data protection authority."),
         ("12","Business continuity","Unavailability of a hospital system is not commercial damage but a risk to patients.")],
   nalHR=["Medicinski uređaji na mreži koji nisu u inventaru imovine",
          "Zajednički računi na odjelima, bez veze s osobom",
          "Sigurnosne kopije dostupne iz iste mreže iz koje se šire ucjenjivački programi",
          "Plan kontinuiteta bez postupka za rad bez informacijskog sustava"],
   nalEN=["Networked medical devices absent from the asset inventory",
          "Shared ward accounts with no link to a person",
          "Backups reachable from the same network ransomware spreads through",
          "A continuity plan with no procedure for working without the information system"],
   clHR=["kategorizacija-prema-zks-u","rokovi-prijave-incidenta","bia-koja-daje-upotrebljiv-rto"],
   clEN=["entity-categorisation-croatian-cybersecurity-act","incident-reporting-deadlines","bia-that-produces-a-usable-rto"]),

 dict(k="hrana", hr="prehrambena-industrija", en="food-industry",
   nHR="Prehrambena industrija", nEN="Food industry", prilog=2, csirt="ncsc", tHR="", tEN="",
   qHR="PROIZVODNJA, PRERADA, DISTRIBUCIJA I VELEPRODAJA HRANE", qEN="PRODUCTION, PROCESSING, DISTRIBUTION AND WHOLESALE",
   leadHR="Prehrambena industrija je u Prilogu II., pa srednji i veliki subjekti postaju važni subjekti. Proizvodne linije, skladišni sustavi i logistika čine je sektorom s izraženom operativnom tehnologijom.",
   leadEN="Food is in Annex II, so medium and large entities become important entities. Production lines, warehouse systems and logistics make it a sector with substantial operational technology.",
   mjHR=[("06","Sigurnost mreže","Proizvodne linije i sustavi upravljanja skladištem u pravilu dijele mrežu s uredskim sustavima."),
         ("05","Kibernetička higijena","Sigurnosne kopije sustava planiranja resursa i njihovo testirano vraćanje odlučuju koliko dugo stoji proizvodnja."),
         ("08","Lanac opskrbe","Dobavljači opreme i pružatelji logističkih usluga imaju pristup sustavima."),
         ("12","Kontinuitet poslovanja","Zastoj u proizvodnji hrane ima rok trajanja - sirovina se kvari dok sustav stoji.")],
   mjEN=[("06","Network security","Production lines and warehouse management systems usually share a network with office systems."),
         ("05","Cyber hygiene","Backups of the ERP system and a tested restore decide how long production stands still."),
         ("08","Supply chain","Equipment suppliers and logistics providers have system access."),
         ("12","Business continuity","A stoppage in food production has a shelf life - raw material spoils while the system is down.")],
   nalHR=["Sustav planiranja resursa i proizvodne linije u istoj mrežnoj zoni",
          "Vraćanje podataka iz sigurnosne kopije nikad testirano do kraja",
          "Udaljeni pristup dobavljača linija bez vremenskog ograničenja",
          "Analiza poslovnog utjecaja u kojoj svi procesi imaju isti RTO"],
   nalEN=["The ERP system and production lines in the same network zone",
          "A restore from backup never tested end to end",
          "Vendor remote access to lines with no time limit",
          "A business impact analysis in which every process carries the same RTO"],
   clHR=["ot-sustavi-i-zks","bia-koja-daje-upotrebljiv-rto","prioritetne-preporuke-ncsc"],
   clEN=["bia-that-produces-a-usable-rto","risk-register-that-passes-review","what-cyber-insurers-actually-ask"]),

 dict(k="ikt", hr="digitalna-infrastruktura-i-ikt", en="digital-infrastructure-and-ict",
   nHR="Digitalna infrastruktura i IKT", nEN="Digital infrastructure and ICT", prilog=1, csirt="ncsc",
   tHR='<a href="https://www.hakom.hr/" target="_blank" rel="noopener">HAKOM</a> za elektroničke komunikacije', tEN='<a href="https://www.hakom.hr/" target="_blank" rel="noopener">HAKOM</a> for electronic communications',
   qHR="PODATKOVNI CENTRI, OBLAK, MREŽE, UPRAVLJANE USLUGE", qEN="DATA CENTRES, CLOUD, NETWORKS, MANAGED SERVICES",
   leadHR="Ovdje kriterij veličine često ne vrijedi. Pružatelji usluga DNS-a i registar vršne nacionalne domene ključni su neovisno o veličini, a pružatelji elektroničkih komunikacija i usluga povjerenja kategoriziraju se neovisno o veličini.",
   leadEN="Here the size criterion often does not apply. DNS service providers and the national top-level domain registry are essential regardless of size, and providers of electronic communications and trust services are categorised regardless of size.",
   mjHR=[("07","Kontrola pristupa","Pružatelj upravljanih usluga ima pristup sustavima svojih klijenata - kompromitacija se množi."),
         ("08","Lanac opskrbe","Vi ste nečiji lanac opskrbe. Mjera 8 vaših klijenata postavlja zahtjeve vama, ugovorom."),
         ("09","Razvoj i održavanje","Odvojena okruženja i upravljanje promjenama presudni su kad jedna promjena pogađa više klijenata."),
         ("11","Postupanje s incidentima","Za dio digitalnih pružatelja vrijede posebna pravila značajnosti iz Provedbene uredbe (EU) 2024/2690.")],
   mjEN=[("07","Access control","A managed service provider has access to its clients' systems - a compromise multiplies."),
         ("08","Supply chain","You are somebody's supply chain. Your clients' measure 8 imposes requirements on you, contractually."),
         ("09","Development and maintenance","Separated environments and change management are decisive when one change affects several clients."),
         ("11","Incident handling","For some digital providers special significance rules apply under Implementing Regulation (EU) 2024/2690.")],
   nalHR=["Zajednički administratorski računi za više klijenata",
          "Alati za udaljeno upravljanje bez višefaktorske autentifikacije",
          "Nema razdvajanja klijentskih okruženja na razini mreže",
          "Ugovori bez definiranog roka prijave incidenta prema klijentu"],
   nalEN=["Shared administrator accounts across several clients",
          "Remote management tools without multi-factor authentication",
          "No network-level separation of client environments",
          "Contracts with no defined incident notification deadline towards the client"],
   clHR=["kategorizacija-prema-zks-u","active-directory-putovi-napada","dnevnicki-zapisi-sto-prikupljati"],
   clEN=["entity-categorisation-croatian-cybersecurity-act","active-directory-attack-paths","iso-27002-2022-control-attributes"]),

 dict(k="javna", hr="javna-uprava", en="public-administration",
   nHR="Javna uprava", nEN="Public administration", prilog=1, csirt="ncsc", tHR="", tEN="",
   qHR="TIJELA DRŽAVNE UPRAVE KLJUČNA NEOVISNO O VELIČINI", qEN="STATE ADMINISTRATION BODIES ESSENTIAL REGARDLESS OF SIZE",
   leadHR="Ovdje veličina ne igra ulogu. Tijela državne uprave razvrstavaju se u ključne subjekte neovisno o veličini, kao i subjekti koji upravljaju državnom informacijskom infrastrukturom. Jedinice lokalne i područne samouprave razvrstavaju se u važne subjekte.",
   leadEN="Size plays no role here. State administration bodies are classified as essential entities regardless of size, as are operators of the state information infrastructure. Local and regional self-government units are classified as important entities.",
   mjHR=[("01","Predanost i odgovornost","Kontakt osoba mora biti iz reda dužnosnika odnosno izvršnog tijela, ne iz informatike."),
         ("02","Upravljanje imovinom","Dostava podataka NCSC-u traži i IP adresne raspone koje subjekt koristi."),
         ("04","Digitalni identiteti","Velik broj korisnika, česte promjene radnih mjesta i dugotrajni pristupi."),
         ("11","Postupanje s incidentima","Pristup platformi PiXi ide preko sustava NIAS i mora biti riješen prije incidenta.")],
   mjEN=[("01","Commitment and accountability","The contact person must be an official or executive body member, not from IT."),
         ("02","Asset management","Data delivery to NCSC-HR also requires the IP address ranges the entity uses."),
         ("04","Digital identities","Large user numbers, frequent role changes and long-lived access rights."),
         ("11","Incident handling","Access to the PiXi platform runs through the national identification system and must be sorted before an incident.")],
   nalHR=["Kontakt osoba imenovana iz informatike umjesto iz upravljačkog tijela",
          "Nepotpun popis IP adresnih raspona koje tijelo koristi",
          "Prava pristupa koja ostaju nakon premještaja na drugo radno mjesto",
          "Nitko nema pristup platformi za prijavu incidenata"],
   nalEN=["A contact person appointed from IT instead of the management body",
          "An incomplete list of the IP ranges the body uses",
          "Access rights that persist after an internal transfer",
          "Nobody has access to the incident reporting platform"],
   clHR=["kategorizacija-prema-zks-u","znacajan-incident-pet-obavijesti-pixi","korelacijski-pregled-mjera"],
   clEN=["entity-categorisation-croatian-cybersecurity-act","incident-reporting-deadlines","how-self-assessment-is-scored"]),

 dict(k="promet", hr="promet-i-logistika", en="transport-and-logistics",
   nHR="Promet i logistika", nEN="Transport and logistics", prilog=1, csirt="ncsc",
   tHR='<a href="https://www.ccaa.hr/" target="_blank" rel="noopener">Hrvatska agencija za civilno zrakoplovstvo</a> za zračni promet', tEN='<a href="https://www.ccaa.hr/" target="_blank" rel="noopener">Croatian Civil Aviation Agency</a> for air transport',
   qHR="ZRAČNI, ŽELJEZNIČKI, VODNI I CESTOVNI", qEN="AIR, RAIL, WATER AND ROAD",
   leadHR="Promet je u Prilogu I. i podijeljen na četiri podsektora. Zračni promet ima vlastito sektorsko nadležno tijelo, dok za ostale nadležnost ostaje kod središnjeg tijela za kibernetičku sigurnost.",
   leadEN="Transport is in Annex I and split into four subsectors. Air transport has its own sectoral competent authority, while for the others competence stays with the central cybersecurity authority.",
   mjHR=[("06","Sigurnost mreže","Sustavi upravljanja prometom i signalizacija odvojeni su od poslovnih sustava - u dokumentaciji češće nego u stvarnosti."),
         ("08","Lanac opskrbe","Logistika ovisi o velikom broju partnera s pristupom sustavima za praćenje pošiljaka."),
         ("11","Postupanje s incidentima","Incident koji zaustavi prijevoz ima prekogranični učinak, što mijenja sadržaj prijave."),
         ("12","Kontinuitet poslovanja","Oporavak mora obuhvatiti i ručni način rada dok sustav ne proradi.")],
   mjEN=[("06","Network security","Traffic management and signalling systems are separated from business systems - more often in documentation than in reality."),
         ("08","Supply chain","Logistics depends on many partners with access to shipment tracking systems."),
         ("11","Incident handling","An incident that halts transport has cross-border effect, which changes the content of the notification."),
         ("12","Business continuity","Recovery must also cover manual operation until the system is back.")],
   nalHR=["Sustavi za praćenje pošiljaka dostupni partnerima bez ograničenja opsega",
          "Nema postupka za ručni rad pri ispadu sustava",
          "Naslijeđeni sustavi signalizacije bez segmentacije",
          "Kriterij značajnosti incidenta ne uzima u obzir prekogranični učinak"],
   nalEN=["Shipment tracking systems available to partners with no scope limitation",
          "No procedure for manual operation during a system outage",
          "Legacy signalling systems without segmentation",
          "A significance criterion that ignores cross-border effect"],
   clHR=["ot-sustavi-i-zks","znacajan-incident-pet-obavijesti-pixi","registar-rizika-koji-prolazi-provjeru"],
   clEN=["incident-reporting-deadlines","risk-register-that-passes-review","bia-that-produces-a-usable-rto"]),
]

SEK_T = {
 "hr": dict(hub="/sektori/", name="Sektori",
   h1="Sektori koje pokrivamo",
   intro="Kategoriju subjekta određuju sektor iz priloga Zakona i veličina, uz niz iznimaka. Za svaki sektor navodimo koje mjere u praksi nose najviše posla, tko je nadležan i što najčešće nalazimo.",
   desc="Sektorski pregled obveza iz Zakona o kibernetičkoj sigurnosti: bankarstvo, osiguranje, energetika, zdravstvo, prehrambena industrija, IKT, javna uprava i promet.",
   crumb_home="Početna",
   cat_h="Kategorizacija", prilog_h="Prilog Zakona", auth_h="Nadležnost",
   csirt_l="Nadležni CSIRT", body_l="Sektorsko tijelo",
   p1="Prilog I. - sektor visoke kritičnosti", p2="Prilog II. - drugi kritični sektor",
   mj_h="Mjere koje u ovom sektoru nose najviše posla",
   nal_h="Što najčešće nalazimo",
   cl_h="Iz baze znanja",
   tools_h="Provjerite sami",
   tool1="Provjera kategorizacije subjekta", tool2="Kalkulator rokova prijave incidenta",
   tool3="Mini samoprocjena po 13 mjera",
   ncsc='<a href="https://www.ncsc.hr/" target="_blank" rel="noopener">Nacionalni centar za kibernetičku sigurnost (NCSC-HR)</a>',
   cert='<a href="https://www.cert.hr/" target="_blank" rel="noopener">Nacionalni CERT</a>',
   all_l="Svi sektori",
   zks_url="https://narodne-novine.nn.hr/clanci/sluzbeni/2024_02_14_254.html",
 ),
 "en": dict(hub="/en/sectors/", name="Sectors",
   h1="Sectors we cover",
   intro="Entity category is determined by the sector listed in the annexes to the Act and by size, subject to a number of exceptions. For each sector we set out which measures carry the most work in practice, who is competent, and what we most often find.",
   desc="Sector overview of obligations under the Croatian Cybersecurity Act: banking, insurance, energy, healthcare, food, ICT, public administration and transport.",
   crumb_home="Home",
   cat_h="Categorisation", prilog_h="Annex to the Act", auth_h="Competence",
   csirt_l="Competent CSIRT", body_l="Sectoral authority",
   p1="Annex I - high-criticality sector", p2="Annex II - other critical sector",
   mj_h="The measures that carry most of the work in this sector",
   nal_h="What we most often find",
   cl_h="From the knowledge base",
   tools_h="Check for yourself",
   tool1="Entity categorisation check", tool2="Incident reporting deadline calculator",
   tool3="Readiness check against the 13 measures",
   ncsc='<a href="https://www.ncsc.hr/" target="_blank" rel="noopener">National Cyber Security Centre (NCSC-HR)</a>',
   cert='<a href="https://www.cert.hr/" target="_blank" rel="noopener">National CERT</a>',
   all_l="All sectors",
   zks_url="https://narodne-novine.nn.hr/clanci/sluzbeni/2024_02_14_254.html",
 ),
}

def build_sectors(lang, articles):
    t = L[lang]
    st = SEK_T[lang]
    FOOT = footer(lang, articles)
    out_dir = os.path.join(ROOT, "en", "sectors") if lang == "en" else os.path.join(ROOT, "sektori")
    os.makedirs(out_dir, exist_ok=True)
    blog = t["blog"]
    tools = TOOLS_T[lang]["hub"]
    arts = {a["slug"]: a for a in articles}

    def slug(s): return s["en"] if lang == "en" else s["hr"]
    def name(s): return s["nEN"] if lang == "en" else s["nHR"]
    def qual(s): return s["qEN"] if lang == "en" else s["qHR"]

    # ── Hub ───────────────────────────────────────────────────────
    def _big(s):
        csirt = "Nacionalni CERT" if s["csirt"] == "cert" else "NCSC-HR"
        if lang == "en" and s["csirt"] == "cert":
            csirt = "National CERT"
        nmj = len(s["mjEN"] if lang == "en" else s["mjHR"])
        return '''      <a class="sx-card" href="%s%s/">
        <div class="sx-top">
          <span class="sx-badge p%d">%s</span>
          <span class="sx-csirt">%s</span>
        </div>
        <div class="sx-name">%s</div>
        <div class="sx-note">%s</div>
        <div class="sx-foot">
          <span>%s</span>
          <span class="sx-go">%s &rarr;</span>
        </div>
      </a>''' % (st["hub"], slug(s), s["prilog"],
                 ("Prilog I." if s["prilog"] == 1 else "Prilog II.") if lang == "hr"
                 else ("Annex I" if s["prilog"] == 1 else "Annex II"),
                 csirt, name(s), qual(s),
                 ("%d prioritetne mjere" % nmj) if lang == "hr" else ("%d priority measures" % nmj),
                 "Otvorite" if lang == "hr" else "Open")

    p1 = [x for x in SEKTORI if x["prilog"] == 1]
    p2 = [x for x in SEKTORI if x["prilog"] == 2]
    cards = ('    <h2 class="sx-h">%s</h2>\n    <p class="sx-sub">%s</p>\n    <div class="sx-grid">\n%s\n    </div>\n'
             % (("Sektori visoke kritičnosti" if lang == "hr" else "High-criticality sectors"),
                ("Prilog I. Zakona. Veliki subjekti su ključni, srednji su važni - uz iznimke u kojima veličina nije mjerilo."
                 if lang == "hr" else
                 "Annex I of the Act. Large entities are essential, medium ones important - subject to exceptions where size is not the criterion."),
                "\n".join(_big(x) for x in p1)))
    if p2:
        cards += ('\n    <h2 class="sx-h">%s</h2>\n    <p class="sx-sub">%s</p>\n    <div class="sx-grid">\n%s\n    </div>\n'
                  % (("Drugi kritični sektori" if lang == "hr" else "Other critical sectors"),
                     ("Prilog II. Zakona. Srednji i veliki subjekti razvrstavaju se u važne subjekte."
                      if lang == "hr" else
                      "Annex II of the Act. Medium and large entities are classified as important entities."),
                     "\n".join(_big(x) for x in p2)))

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
    <div class="sx-wrap">
%s
    </div>
  </div>
</main>
''' % (st["name"], st["h1"], st["intro"], cards) + FOOT

    io.open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8").write(
      page(st["name"] + " | Adventure Spirit Consulting", st["desc"], hub_body,
           SITE + st["hub"], lang=lang,
           extra_head=hreflang(SITE + "/sektori/", SITE + "/en/sectors/")))

    # ── Stranice sektora ──────────────────────────────────────────
    for s in SEKTORI:
        sl, nm = slug(s), name(s)
        url = SITE + st["hub"] + sl + "/"
        lead = s["leadEN"] if lang == "en" else s["leadHR"]
        mj = s["mjEN"] if lang == "en" else s["mjHR"]
        nal = s["nalEN"] if lang == "en" else s["nalHR"]
        cl = s["clEN"] if lang == "en" else s["clHR"]

        mjere = "\n".join('''      <div class="gap-item crit">
        <div class="gap-h"><span class="gap-n">%s</span><span class="gap-t">%s</span></div>
        <div class="gap-d">%s</div>
      </div>''' % (n, t2, d) for n, t2, d in mj)

        nalazi = "\n".join("        <li>%s</li>" % x for x in nal)

        rel = [arts[c] for c in cl if c in arts]
        clanci = "\n".join(card(a, lang) for a in rel)

        auth = '<div><span class="auth-k">%s</span>%s</div>' % (
            st["csirt_l"], st["cert"] if s["csirt"] == "cert" else st["ncsc"])
        body_t = s["tEN"] if lang == "en" else s["tHR"]
        if body_t:
            auth += '<div><span class="auth-k">%s</span>%s</div>' % (st["body_l"], body_t)

        others = [x for x in SEKTORI if x["k"] != s["k"]][:4]
        drugi = "\n".join('<a class="chip-link" href="%s%s/">%s</a>' % (st["hub"], slug(x), name(x))
                          for x in others)

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

    <article>
      <div class="auth-box" style="margin-top:36px">
        <div><span class="auth-k">%s</span>%s</div>
        %s
      </div>

      <h2>%s</h2>
%s

      <h2>%s</h2>
      <ul>
%s
      </ul>

      <h2>%s</h2>
      <p>Tri alata koja rade u pregledniku, bez registracije:</p>
      <div class="nf-nav" style="border:none;padding-top:0;margin-top:0">
        <a href="%s%s/">%s</a>
        <a href="%s%s/">%s</a>
        <a href="%s%s/">%s</a>
      </div>

      %s
    </article>

    <div class="related">
      <h3>%s</h3>
      <div class="related-grid">
%s
      </div>
    </div>

    <div class="related" style="margin-top:0;padding-top:32px">
      <h3>%s</h3>
      <div class="chip-row">
%s
        <a class="chip-link" href="%s">%s</a>
      </div>
    </div>
  </div>
</main>
''' % (t["base"] or "/", st["crumb_home"], st["hub"], st["name"], nm,
       st["name"], nm, lead,
       st["prilog_h"],
       '<a href="%s" target="_blank" rel="noopener">%s</a>' % (st["zks_url"], st["p1"] if s["prilog"] == 1 else st["p2"]),
       auth,
       st["mj_h"], mjere,
       st["nal_h"], nalazi,
       st["tools_h"],
       tools, CAT_T[lang]["slug"], st["tool1"],
       tools, TOOLS_T[lang]["slug"], st["tool2"],
       tools, SA_T[lang]["slug"], st["tool3"],
       cta_block(lang),
       st["cl_h"], clanci,
       st["all_l"], drugi, st["hub"], st["all_l"]) + FOOT

        ld = [{
          "@context": "https://schema.org", "@type": "WebPage",
          "name": nm, "url": url,
          "description": lead[:300],
          "inLanguage": "hr-HR" if lang == "hr" else "en-GB",
          "isPartOf": {"@type": "WebSite", "url": SITE + "/"},
          "publisher": {"@type": "Organization", "name": "Adventure Spirit Consulting",
                        "legalName": "Adventure Spirit d.o.o.", "url": SITE + "/"},
        }, {
          "@context": "https://schema.org", "@type": "BreadcrumbList",
          "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": st["crumb_home"], "item": SITE + (t["base"] or "/")},
            {"@type": "ListItem", "position": 2, "name": st["name"], "item": SITE + st["hub"]},
            {"@type": "ListItem", "position": 3, "name": nm, "item": url}]}]

        d = os.path.join(out_dir, sl)
        os.makedirs(d, exist_ok=True)
        io.open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(
          page(nm + " | Adventure Spirit Consulting",
               (lead[:150] + "...") if len(lead) > 150 else lead, body, url, lang=lang,
               extra_head=hreflang(SITE + "/sektori/" + s["hr"] + "/",
                                   SITE + "/en/sectors/" + s["en"] + "/"), ld=ld))

# ══════════════════════════════════════════════════════════════════
# Sklapanje engleske naslovnice
# ══════════════════════════════════════════════════════════════════
def en_index():
    legal = "\n".join(
      ('        <a class="legal-item" href="%s"%s>%s</a>'
       % (u, '' if u.startswith('/') else ' target="_blank" rel="noopener"', inner)) if u
      else ('        <div class="legal-item">%s</div>' % inner)
      for code, ref, desc, u in EN_LEGAL
      for inner in ['<div class="legal-code">%s</div><div class="legal-ref">%s</div><div class="legal-desc">%s</div>' % (code, ref, desc)])

    EN_SUB = {
     "CSA / NIS2 compliance": [("The 13 measures of Annex II", "/en/blog/thirteen-measures-annex-ii/"),
                               ("Entity categorisation", "/en/blog/entity-categorisation-croatian-cybersecurity-act/"),
                               ("How scoring works", "/en/blog/how-self-assessment-is-scored/")],
     "GDPR compliance": [("Incident reporting deadlines", "/en/blog/incident-reporting-deadlines/"),
                         ("AI inventory and asset register", "/en/blog/ai-inventory-and-asset-register/")],
     "ISO/IEC 27001 - Information security": [("ISO 27001 and the Act", "/en/blog/iso-27001-and-the-cybersecurity-act/"),
                                              ("ISO 27002:2022 attributes", "/en/blog/iso-27002-2022-control-attributes/")],
     "ISO 9001 - Quality management": [("Risk register that passes", "/en/blog/risk-register-that-passes-review/")],
     "ISO 14001 - Environmental management": [("Risk register that passes", "/en/blog/risk-register-that-passes-review/")],
     "ISO 22301 - Business continuity": [("A BIA that produces a usable RTO", "/en/blog/bia-that-produces-a-usable-rto/"),
                                         ("ISO 27001 and the Act", "/en/blog/iso-27001-and-the-cybersecurity-act/")],
     "DORA - Digital operational resilience": [("The DORA register of information", "/en/blog/dora-register-of-information/"),
                                               ("Banking and finance", "/en/sectors/banking-and-finance/")],
     "Vendor risk management": [("The DORA register of information", "/en/blog/dora-register-of-information/"),
                                ("Risk register that passes", "/en/blog/risk-register-that-passes-review/")],
     "Security audits and testing": [("Active Directory: five findings", "/en/blog/active-directory-attack-paths/"),
                                     ("What cyber insurers ask", "/en/blog/what-cyber-insurers-actually-ask/")],
    }
    def _sub(nm):
        ls = EN_SUB.get(nm, [])
        if not ls:
            return ""
        return '\n        <div class="card-sub">' + "".join(
          '<a href="%s">%s</a>' % (u, t2) for t2, u in ls) + '</div>'
    services = "\n".join('''      <div class="service-card">
        <div class="card-icon">%s</div>
        <div class="card-title">%s</div>
        <div class="card-desc">%s</div>%s
        <div class="card-footer"><span class="card-badge">%s</span><a class="card-more" href="#contact">Ask about this &rarr;</a></div>
      </div>''' % (svg(ic), name, desc, _sub(name), badge) for ic, name, badge, desc in EN_SERVICES)

    _smap = {x["nEN"]: x["en"] for x in SEKTORI}
    def _sc(a, b):
        sl = _smap.get(a)
        if not sl:
            return '        <div class="sector-card"><div class="sector-name">%s</div><div class="sector-note">%s</div></div>' % (a, b)
        return ('        <a class="sector-card" href="/en/sectors/%s/"><div class="sector-name">%s</div>'
                '<div class="sector-note">%s</div><span class="sector-more">View sector &rarr;</span></a>' % (sl, a, b))
    sectors = "\n".join(_sc(a, b) for a, b in EN_SECTORS)
    def _chip(a, url, desc, b, burl):
        left = '<a href="%s" target="_blank" rel="noopener">%s</a>' % (url, a)
        if b:
            left += ' / <a href="%s" target="_blank" rel="noopener">%s</a>' % (burl, b)
        return '      <span class="authority"><strong>%s</strong> &middot; %s</span>' % (left, desc)
    authorities = "\n".join(_chip(*x) for x in EN_AUTHORITIES)
    steps = "\n".join('      <div class="step"><div class="step-num">%s</div><div class="step-title">%s</div><div class="step-desc">%s</div><span class="step-dur">%s</span></div>'
                      % s for s in EN_PROCESS)
    CHK = '<svg viewBox="0 0 24 24"><path d="M20 6 9 17l-5-5"/></svg>'
    deliverables = "\n".join('        <div class="deliver-item">%s<span>%s</span></div>' % (CHK, d)
                             for d in EN_DELIVERABLES)
    REF_URLS = {'Zagreb Stock Exchange': 'https://www.zse.hr/', 'Partner banka': 'https://www.paba.hr/', 'Euroleasing': 'https://www.euroleasing.hr/', 'Fintastic': 'https://www.fintastic.hr/', 'Croatia osiguranje': 'https://www.crosig.hr/', 'Adriatic osiguranje': 'https://www.adriatic.hr/', 'UNIQA osiguranje': 'https://www.uniqa.hr/', 'HROTE': 'https://www.hrote.hr/', 'E.ON': 'https://www.eon.hr/', 'INA': 'https://www.ina.hr/', 'TEHMA': 'https://www.tehma.hr/', 'APIS-IT': 'https://www.apis-it.hr/', 'Rocket DBS': 'https://www.rocketdbs.com/', 'SmartGroup HR Solutions': 'https://www.smartgroup.hr/', 'SmartGroup Recruitment': 'https://www.smartgroup.hr/', 'AMODO': 'https://amodo.eu/', 'Cooperante': 'https://www.cooperante.hr/', 'TPA Hrvatska': 'https://www.tpa-group.hr/', 'Franck d.d.': 'https://www.franck.eu/', 'Pan-pek': 'https://www.panpek.hr/', 'Mlinar': 'https://www.mlinar.hr/', 'Offertissima': 'https://www.offertissima.hr/', 'Medika d.d.': 'https://www.medika.hr/', 'Biovega': 'https://www.biovega.hr/', 'EOS Matrix': 'https://hr.eos-solutions.com/', 'Kompas': 'https://kompas-travel.com/', 'Hrvatski Telekom': 'https://www.hrvatskitelekom.hr/', 'Hajduk Split': 'https://hajduk.hr/', 'Krypto Investment Partners': 'https://kip.investments/', 'ANO Insurance Solutions': 'https://www.ano.hr/hr/naslovna/', 'Sunce osiguranje': 'https://www.agramlife.hr/', 'IHC Engineering Croatia': 'https://www.royalihc.com/about-us/global-presence/croatia', 'Digital Assembly': 'https://digital-assembly.hr/', 'Delmerion Natural Beauty': 'https://delmerion.hr/', 'Log Adria': 'https://www.rhenus.group/', 'Travel Experience Museum': 'https://travelexperiencemuseum.com/', 'Intersnack': 'https://www.intersnack.hr/', 'BCC Services': 'https://www.bccservices.com/'}
    REF_TIPS = {'Sunce osiguranje': 'Merged into Agram Life osiguranje', 'IHC Engineering Croatia': 'Part of the Royal IHC group', 'Log Adria': 'Acquired by the Rhenus group', 'Šted banka': 'In liquidation', 'MCZ': 'Ceased operations', 'Intersnack': 'Formerly Adria Snack Company'}
    def _ref(c):
        u = REF_URLS.get(c)
        tip = REF_TIPS.get(c)
        t = ' title="%s"' % tip if tip else ''
        if not u:
            cls = "ref-chip ref-past" if tip else "ref-chip"
            return '<span class="%s"%s>%s</span>' % (cls, t, c)
        return '<a class="ref-chip" href="%s" target="_blank" rel="noopener"%s>%s</a>' % (u, t, c)
    clients = "\n".join('''      <div class="ref-category">
        <div class="ref-cat-label">%s</div>
        <div class="ref-logos">%s</div>
      </div>''' % (cat, "".join(_ref(c) for c in items))
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
          <li><span>&#9656;</span>CIPP/E - Certified Information Privacy Professional/Europe</li>
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
        Principal consultant Daniel Bara, PhD, brings more than 20 years of work in information security, a doctorate in business intelligence, an MBA, the PMP and CIPP/E certifications and experience as an external evaluator on more than 300 EU-funded projects. He has lectured at RIT Croatia since 2017, with guest lectures at ZSEM, VERN and Libertas.</p>
        <div class="onama-expertise">
          <h3>Areas of expertise</h3>
          <div class="expertise-tags">
            <span class="expertise-tag">ISO 27001:2022</span><span class="expertise-tag">ISO 9001:2015</span>
            <span class="expertise-tag">ISO 14001:2015</span><span class="expertise-tag">ISO 22301:2019</span>
            <span class="expertise-tag">GDPR / DPO</span><span class="expertise-tag">CIPP/E</span><span class="expertise-tag">NIS2 / CSA</span>
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
      <p class="section-desc">Entity category is determined by the sector listed in the annexes to the Act and by size, subject to a number of exceptions where size is not the criterion at all.</p>
    </div>
    <div class="sector-grid">
''' + sectors + '''
    </div>
    <div class="kb-all" style="margin-top:26px"><a href="/en/sectors/" class="btn-outline">All sectors in detail &rarr;</a></div>
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
      <h3>What we perform ourselves, and what we do not</h3>
      <p><strong>We do perform</strong> internal audits of management systems, compliance reviews against the Croatian Cybersecurity Act and data protection law, and a documentation review that simulates the audit process before an external auditor arrives. We also act as external DPO and external CISO.</p>
      <p><strong>We do not perform</strong> ISO certification - by definition that is carried out by an accredited certification body, and nobody who built a system may also certify it. That separation is not a formality but protection for you: what we tell you is ready is ready for someone who has no interest in it being so.</p>
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
          <label class="vh" for="c-name">Full name</label>
          <input class="form-input" type="text" placeholder="Full name *" required id="c-name">
          <label class="vh" for="c-email">Email address</label>
          <input class="form-input" type="email" placeholder="Email address *" required id="c-email">
        </div>
        <div class="form-row">
          <label class="vh" for="c-company">Company / organisation</label>
          <input class="form-input" type="text" placeholder="Company / organisation" id="c-company">
          <label class="vh" for="c-phone">Phone</label>
          <input class="form-input" type="tel" placeholder="Phone" id="c-phone">
        </div>
        <label class="vh" for="c-subject">Subject</label>
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
        <label class="vh" for="c-message">A short description of the project or question</label>
        <textarea class="form-textarea" placeholder="A short description of the project or question" id="c-message"></textarea>
        <div id="c-success" style="display:none;color:#6ec47a;font-size:13px;padding:8px 0">&#10003; Thank you. We will be in touch shortly.</div>
        <div id="c-error" style="display:none;color:#f87171;font-size:13px;padding:8px 0"></div>
        <button type="submit" class="form-submit">Send enquiry &rarr;</button>
        <p class="legal-note">The legally binding versions of our terms of use and privacy policy are published in Croatian.</p>
      </form>
    </div>
  </div>
</section>
''' + footer("en", ARTICLES_EN) + '''

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
    var href = a.getAttribute('href');
    if (!href || href === '#') { return; }
    var t = null;
    try { t = document.querySelector(href); } catch (err) { return; }
    if (!t) { return; }
    e.preventDefault();
    if (document.body.style.overflow === 'hidden' && !document.querySelector('.modal-overlay.open')) {
      document.body.style.overflow = '';
    }
    var y = Math.max(0, t.getBoundingClientRect().top + window.pageYOffset - 104);
    try { window.scrollTo({ top: y, behavior: 'smooth' }); }
    catch (err) { window.scrollTo(0, y); }
    setTimeout(function () {
      if (Math.abs(window.pageYOffset - y) > 4) { window.scrollTo(0, y); }
    }, 600);
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
    var res = await fetch('https://formspree.io/f/__FS_UPITI__', {
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
                  "jobTitle": "Founder and Principal Consultant",
                  "hasCredential": ["PhD", "MBA", "PMP", "CIPP/E"]},
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
    hay = " ".join([a["title"], a["lead"], a["desc"], a["cat"]]).lower()
    return '''<a class="post-card%s" href="%s%s/" data-cat="%s" data-q="%s">
      <div class="post-cat">%s</div>
      <div class="post-title">%s</div>
      <div class="post-lead">%s</div>
      <div class="post-meta"><span>%s</span><span class="read">%d %s</span></div>
    </a>''' % (" featured" if featured else "", t["blog"], a["slug"], a["catkey"],
               html.escape(hay), html.escape(a["cat"]), html.escape(a["title"]),
               html.escape(a["lead"]), fmt_date(a["date"], lang), a["read"], t["read"])


def cta_block(lang):
    t = L[lang]
    return '''<div class="art-cta">
  <h3>%s</h3>
  <p>%s</p>
  <div class="cta-btns">
    <a href="%s" class="btn-primary">%s</a>
    <a href="%s" class="btn-outline">%s</a>
  </div>
</div>''' % (t["cta_h"], t["cta_p"], "/kontakt/" if lang == "hr" else "/en/contact/",
              t["cta_b1"], t["cta_b2_url"], t["cta_b2"])


# ══════════════════════════════════════════════════════════════════
# Jezicni parovi clanaka (HR slug -> EN slug)
# Bez ovoga clanci nemaju hreflang pa ih Google tretira kao dvije
# nepovezane stranice umjesto kao isti tekst na dva jezika.
# Clanci kojih nema na popisu postoje samo na hrvatskom.
# ══════════════════════════════════════════════════════════════════
PAROVI = {
 "kategorizacija-prema-zks-u":            "entity-categorisation-croatian-cybersecurity-act",
 "trinaest-mjera-priloga-ii":             "thirteen-measures-annex-ii",
 "kako-se-boduje-samoprocjena":           "how-self-assessment-is-scored",
 "rokovi-prijave-incidenta":              "incident-reporting-deadlines",
 "iso-27001-i-zks":                       "iso-27001-and-the-cybersecurity-act",
 "registar-rizika-koji-prolazi-provjeru": "risk-register-that-passes-review",
 "iso-27002-2022-atributi-kontrola":      "iso-27002-2022-control-attributes",
 "bia-koja-daje-upotrebljiv-rto":         "bia-that-produces-a-usable-rto",
 "dora-registar-informacija":             "dora-register-of-information",
 "sto-osiguravatelji-pitaju-kibernetickom-osiguranju": "what-cyber-insurers-actually-ask",
 "nist-csf-2-funkcija-govern":            "nist-csf-2-govern-function",
 "active-directory-putovi-napada":        "active-directory-attack-paths",
 "korelacijski-pregled-mjera":            "correlation-of-measures-to-standards",
 "akt-o-umjetnoj-inteligenciji-razine-rizika": "ai-act-risk-levels",
 "zabranjene-prakse-i-ai-pismenost":      "prohibited-practices-and-ai-literacy",
 "registar-ai-sustava-i-registar-imovine": "ai-inventory-and-asset-register",
 "ai-u-obrani-gdje-pomaze-gdje-odmaze":   "ai-in-defence-where-it-helps",
 "zks-kazne-tko-placa-i-koliko":          "penalties-under-the-cybersecurity-act",
 "revizija-kiberneticke-sigurnosti":      "cybersecurity-audit-how-it-works",
 "sigurnosna-kultura-i-ljudski-faktor":   "security-culture-and-the-human-factor",
}
PAROVI_EN = {v: k for k, v in PAROVI.items()}


def hreflang_clanak(lang, slug):
    """Vraca hreflang oznake za clanak, ili prazno ako prijevoda nema."""
    if lang == "hr":
        en = PAROVI.get(slug)
        if not en:
            return ""
        return hreflang(SITE + "/blog/%s/" % slug, SITE + "/en/blog/%s/" % en)
    hr = PAROVI_EN.get(slug)
    if not hr:
        return ""
    return hreflang(SITE + "/blog/%s/" % hr, SITE + "/en/blog/%s/" % slug)


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
          % (('<a href="%s"%s>%s</a>' % (u, '' if u.startswith('/') else ' target="_blank" rel="noopener"',
                                         html.escape(src)))
             if u else html.escape(src)) for src, u in a["sources"])
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
               lang=lang, og_type="article", ld=ld,
               extra_head=hreflang_clanak(lang, a["slug"])))

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
      <div class="kb-search">
        <svg class="ic" viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.35-4.35"/></svg>
        <label class="vh" for="kb-q">%s</label>
        <input type="search" id="kb-q" placeholder="%s" autocomplete="off" spellcheck="false">
        <button type="button" class="kb-clear" id="kb-x" hidden aria-label="%s">&times;</button>
      </div>
      <div class="cat-bar">
      %s
      </div>
      <p class="kb-count" id="kb-count"></p>
    </div>
  </section>
  <div class="container">
    <div class="post-grid" id="posts">
%s
    </div>
  </div>
</main>
<script>
(function () {
  var T = __PRETXT__;
  var q = document.getElementById('kb-q'), x = document.getElementById('kb-x'),
      cnt = document.getElementById('kb-count'), grid = document.getElementById('posts');
  var kartice = [].slice.call(document.querySelectorAll('.post-card'));
  var tema = 'all';

  // dijakritika se zanemaruje, pa "uskladenost" nade "usklađenost"
  function norm(s) {
    return (s || '').toLowerCase()
      .replace(/[čć]/g, 'c').replace(/\\u0111/g, 'd').replace(/š/g, 's').replace(/ž/g, 'z')
      .normalize ? (s || '').toLowerCase()
        .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
        .replace(/\\u0111/g, 'd').replace(/\u0111/g, 'd')
      : (s || '').toLowerCase();
  }

  var prazno = document.createElement('div');
  prazno.className = 'kb-none';
  prazno.hidden = true;
  grid.parentNode.insertBefore(prazno, grid.nextSibling);

  function filtriraj() {
    var pojam = norm(q.value.trim());
    var rijeci = pojam ? pojam.split(/\\s+/).filter(Boolean) : [];
    var vidljivih = 0;
    kartice.forEach(function (c) {
      var okTema = (tema === 'all' || c.dataset.cat === tema);
      var okPojam = !rijeci.length || rijeci.every(function (r) {
        return norm(c.dataset.q).indexOf(r) !== -1;
      });
      var vidi = okTema && okPojam;
      c.classList.toggle('hidden', !vidi);
      if (vidi) vidljivih++;
    });
    x.hidden = !q.value;
    if (rijeci.length || tema !== 'all') {
      cnt.innerHTML = T.broj.replace('%%d', vidljivih).replace('%%d', kartice.length);
    } else {
      cnt.innerHTML = '';
    }
    if (vidljivih === 0) {
      prazno.hidden = false;
      prazno.innerHTML = '<p>' + T.nema.replace('%%s', q.value.replace(/[<>&]/g, '')) +
                         '<br>' + T.savjet + '</p>';
    } else {
      prazno.hidden = true;
    }
  }

  document.querySelectorAll('.cat-btn').forEach(function (b) {
    b.addEventListener('click', function () {
      document.querySelectorAll('.cat-btn').forEach(function (y) { y.classList.remove('active'); });
      b.classList.add('active');
      tema = b.dataset.f;
      filtriraj();
    });
  });
  q.addEventListener('input', filtriraj);
  x.addEventListener('click', function () { q.value = ''; q.focus(); filtriraj(); });
  q.addEventListener('keydown', function (e) { if (e.key === 'Escape') { q.value = ''; filtriraj(); } });

  // pojam iz adrese, npr. /blog/?q=kazne
  var iz = new URLSearchParams(location.search).get('q');
  if (iz) { q.value = iz; filtriraj(); }
})();
</script>
''' % (t["kb_title"], t["kb_h1"], t["kb_intro"], t["pretraga"], t["pretraga"], t["pret_ocisti"], catbtns, cards)
    listing = listing.replace("__PRETXT__", json.dumps(
        {"broj": t["pret_broj"], "nema": t["pret_nema"], "savjet": t["pret_savjet"]},
        ensure_ascii=False))
    listing = listing + FOOT

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
        <a href="%s" class="btn-outline">%s</a>
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
''' % (t["nf_h1"], t["nf_p"], t["base"] or "/", t["nf_home"],
       "/kontakt/" if lang == "hr" else "/en/contact/", t["nf_contact"], nf_nav, t["nf_from_kb"],
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
   hub_h1="Alati koji daju odgovor, a ne objašnjenje",
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
    cards += '''
      <a class="tool-card" href="%s%s/">
        <div class="tool-icon">%s</div>
        <div class="tool-name">%s</div>
        <div class="tool-desc">%s</div>
        <span class="tool-tag">%s</span>
      </a>''' % (w["hub"], CAT_T[lang]["slug"], TOOL_ICONS["split"], CAT_T[lang]["name"],
                 CAT_T[lang]["desc"], "ZKS / NIS2" if lang == "hr" else "CSA / NIS2")
    cards += '''
      <a class="tool-card" href="%s%s/">
        <div class="tool-icon">%s</div>
        <div class="tool-name">%s</div>
        <div class="tool-desc">%s</div>
        <span class="tool-tag">%s</span>
      </a>''' % (w["hub"], SA_T[lang]["slug"], TOOL_ICONS["chart"], SA_T[lang]["name"],
                 SA_T[lang]["desc"], "ZKS / NIS2" if lang == "hr" else "CSA / NIS2")
    for icon, nm, ds in []:
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
    if (window.asTrack) window.asTrack("tool_deadlines");
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


# ══════════════════════════════════════════════════════════════════
# ALAT 2 - Provjera kategorizacije subjekta
# ══════════════════════════════════════════════════════════════════
# Sektori iz Priloga I. i II. ZKS-a, s nadleznim CSIRT-om iz Priloga III.
# csirt: "ncsc" ili "cert"; special: posebno pravilo iz cl. 9., 10., 12. ili 13.
SECTORS = [
 # (kljuc, prilog, HR naziv, EN naziv, csirt, sektorsko tijelo HR, sektorsko tijelo EN)
 ("energetika", 1, "Energetika", "Energy", "ncsc", "", ""),
 ("promet-zracni", 1, "Promet - zračni", "Transport - air", "ncsc", "Hrvatska agencija za civilno zrakoplovstvo", "Croatian Civil Aviation Agency"),
 ("promet-ostalo", 1, "Promet - željeznički, vodni, cestovni", "Transport - rail, water, road", "ncsc", "", ""),
 ("bankarstvo", 1, "Bankarstvo", "Banking", "cert", "Hrvatska narodna banka", "Croatian National Bank"),
 ("financijsko-trziste", 1, "Infrastruktura financijskog tržišta", "Financial market infrastructure", "cert", "HANFA", "HANFA"),
 ("zdravstvo", 1, "Zdravstvo", "Health", "ncsc", "", ""),
 ("voda", 1, "Voda za ljudsku potrošnju", "Drinking water", "ncsc", "", ""),
 ("otpadne-vode", 1, "Otpadne vode", "Waste water", "ncsc", "", ""),
 ("di-povjerenje", 1, "Digitalna infrastruktura - pružatelj usluga povjerenja", "Digital infrastructure - trust service provider", "ncsc", "", ""),
 ("di-komunikacije", 1, "Digitalna infrastruktura - javne elektroničke komunikacije", "Digital infrastructure - public electronic communications", "ncsc", "HAKOM", "HAKOM"),
 ("di-dns", 1, "Digitalna infrastruktura - DNS, registar .hr, razmjena prometa", "Digital infrastructure - DNS, .hr registry, internet exchange", "cert", "", ""),
 ("di-oblak", 1, "Digitalna infrastruktura - oblak, podatkovni centri, CDN", "Digital infrastructure - cloud, data centres, CDN", "ncsc", "", ""),
 ("ikt-b2b", 1, "Upravljanje uslugama IKT-a (B2B)", "ICT service management (B2B)", "ncsc", "", ""),
 ("javni-sektor", 1, "Javni sektor", "Public administration", "ncsc", "", ""),
 ("svemir", 1, "Svemir", "Space", "ncsc", "", ""),
 ("posta", 2, "Poštanske i kurirske usluge", "Postal and courier services", "ncsc", "", ""),
 ("otpad", 2, "Gospodarenje otpadom", "Waste management", "ncsc", "", ""),
 ("kemikalije", 2, "Izrada, proizvodnja i distribucija kemikalija", "Manufacture and distribution of chemicals", "ncsc", "", ""),
 ("hrana", 2, "Proizvodnja, prerada i distribucija hrane", "Production, processing and distribution of food", "ncsc", "", ""),
 ("proizvodnja", 2, "Proizvodnja (medicinski proizvodi, elektronika, strojevi, vozila)", "Manufacturing (medical devices, electronics, machinery, vehicles)", "ncsc", "", ""),
 ("digitalne-usluge", 2, "Pružatelji digitalnih usluga (tržišta, tražilice, društvene mreže)", "Digital service providers (marketplaces, search engines, social networks)", "ncsc", "", ""),
 ("istrazivanje", 2, "Istraživanje", "Research", "cert", "", ""),
 ("obrazovanje", 2, "Sustav obrazovanja", "Education system", "cert", "", ""),
 ("izvan", 0, "Nijedan od navedenih", "None of the above", "", "", ""),
]

CAT_T = {
 "hr": dict(
   slug="provjera-kategorizacije",
   name="Provjera kategorizacije subjekta",
   desc="Sektor, veličina i posebne okolnosti daju vjerojatnu kategoriju subjekta prema ZKS-u i popis obveza koje iz nje slijede.",
   title="Provjera kategorizacije subjekta prema ZKS-u",
   lead="Kategoriju vam određuje nadležno tijelo i o njoj vas pisano obavještava. Do tada je korisno znati što je vjerojatno. Alat primjenjuje kriterije iz članaka 9. do 15. Zakona i pokaže koje pravilo je odlučilo.",
   desc_meta="Besplatna provjera jeste li ključni ili važni subjekt prema Zakonu o kibernetičkoj sigurnosti: sektor iz Priloga I. i II., kriterij veličine i posebna pravila iz čl. 11. do 13.",
   f_sector="Sektor iz Priloga I. ili II. Zakona",
   f_sector_sub="Odaberite sektor u kojem obavljate djelatnost. Ako obavljate više djelatnosti, mjerodavna je ona koja je obuhvaćena prilozima.",
   f_size="Veličina subjekta",
   f_size_sub="Prema članku 15. Zakona uzima se godišnji prosjek broja zaposlenika i ukupan godišnji poslovni prihod, odnosno ukupna aktiva.",
   sizes=[("mikro","Mikro ili mali - manje od 50 zaposlenih i do 10 mil. EUR prihoda ili aktive"),
          ("srednji","Srednji - 50 do 249 zaposlenih, ili do 50 mil. EUR prihoda odnosno 43 mil. EUR aktive"),
          ("veliki","Veliki - 250 ili više zaposlenih, ili preko 50 mil. EUR prihoda odnosno 43 mil. EUR aktive")],
   f_special="Posebne okolnosti",
   f_special_sub="Označite sve što se na vas odnosi. Svaka od ovih stavki nadjačava kriterij veličine.",
   specials=[
     ("drzavna","Tijelo državne uprave ili drugo državno tijelo s javnim ovlastima","Članak 12. stavak 1."),
     ("dii","Upravljamo, razvijamo ili održavamo državnu informacijsku infrastrukturu","Članak 12. stavak 2."),
     ("jlprs","Jedinica lokalne ili područne (regionalne) samouprave","Članak 12. stavak 3."),
     ("kvalpovjerenje","Kvalificirani smo pružatelj usluga povjerenja","Članak 9. podstavak 2."),
     ("eracun","Informacijski smo posrednik u razmjeni elektroničkog računa","Članak 9. podstavak 4."),
     ("kriticni","Utvrđeni smo kao kritični subjekt prema zakonu o kritičnoj infrastrukturi","Članak 9. podstavak 5."),
     ("cl11","Jedini smo pružatelj ključne usluge, ili bi naš ispad znatno utjecao na javnu sigurnost, zaštitu ili zdravlje","Članak 11."),
   ],
   btn="Provjeri kategoriju", reset="Poništi", copy="Kopiraj sažetak", print="Ispiši",
   copied="Sažetak kopiran",
   err="Odaberite sektor i veličinu subjekta.",
   res_h="Vjerojatna kategorija",
   r_kljucni="Ključni subjekt", r_vazni="Važni subjekt", r_izvan="Vjerojatno izvan opsega Zakona",
   why="Zašto",
   next_h="Što iz toga slijedi",
   csirt_h="Nadležni CSIRT za prijavu incidenata",
   sector_body="Sektorsko nadležno tijelo",
   ncsc="Nacionalni centar za kibernetičku sigurnost (NCSC-HR)",
   cert="Nacionalni CERT",
   disclaimer="Ovo je informativna procjena, ne pravni savjet i ne službena kategorizacija. Kategorizaciju provodi nadležno tijelo i o njoj vas pisano obavještava. Mjerodavna je isključivo ta obavijest. Alat ne obuhvaća sve iznimke, posebno procjenu važnosti iz članka 12. stavaka 1. i 3. te članka 13.",
   privacy="Alat radi isključivo u vašem pregledniku. Unesenih podataka nema na našem poslužitelju.",
   more="Više o kategorizaciji", more_url="/blog/kategorizacija-prema-zks-u/",
   sum_h="PROVJERA KATEGORIZACIJE PREMA ZKS-u",
   l_sector="Sektor:", l_size="Veličina:", l_cat="Vjerojatna kategorija:", l_why="Osnova:",
   next_kljucni=["Rok za usklađivanje: godinu dana od dostave obavijesti o kategorizaciji (čl. 26. st. 5.)",
                 "Provjera usklađenosti: neovisna revizija kibernetičke sigurnosti",
                 "Provedba 13 mjera iz Priloga II. Uredbe, na propisanoj razini",
                 "Imenovanje kontakt osobe iz upravljačkog tijela i najmanje dvije osobe za operacionalizaciju dostave podataka",
                 "Dostava podataka NCSC-u: naziv, OIB, veličina, adresa, kontakti, IP adresni rasponi, sektor i vrsta subjekta",
                 "Prijava značajnih incidenata u rokovima 24 h, 72 h i 30 dana"],
   next_vazni=["Rok za usklađivanje: godinu dana od dostave obavijesti o kategorizaciji (čl. 26. st. 5.)",
               "Provjera usklađenosti: samoprocjena prema bodovnom okviru ZSIS-a",
               "Provedba 13 mjera iz Priloga II. Uredbe, na propisanoj razini",
               "Imenovanje kontakt osobe iz upravljačkog tijela i najmanje dvije osobe za operacionalizaciju dostave podataka",
               "Dostava podataka NCSC-u: naziv, OIB, veličina, adresa, kontakti, IP adresni rasponi, sektor i vrsta subjekta",
               "Prijava značajnih incidenata u rokovima 24 h, 72 h i 30 dana"],
   next_izvan=["Prema odabranim kriterijima ne ispunjavate opće uvjete za kategorizaciju.",
               "To ne isključuje članak 11.: nadležno tijelo može vas razvrstati neovisno o veličini ako ste jedini pružatelj ključne usluge ili bi vaš ispad imao znatan učinak.",
               "Ako ste dobavljač kategoriziranim subjektima, njihova mjera 8 (sigurnost lanca opskrbe) ionako će vam postaviti sigurnosne zahtjeve ugovorom.",
               "Mjere iz Priloga II. korisne su i bez obveze - one su ono što osiguravatelji i veliki kupci ionako traže."],
   why_prilog1_veliki="Sektor je u Prilogu I., a subjekt prelazi gornje granice za srednje - članak 9. podstavak 1.",
   why_prilog1_srednji="Sektor je u Prilogu I., a subjekt je srednji - članak 10. podstavak 2.",
   why_prilog2="Sektor je u Prilogu II., a subjekt je srednji ili veći - članak 10. podstavak 1.",
   why_mali="Sektor je u prilozima, ali je subjekt mikro ili mali, pa opći kriteriji veličine nisu ispunjeni.",
   why_izvan="Odabrani sektor nije u Prilogu I. ni u Prilogu II. Zakona.",
   why_dvostruko="Subjekt ispunjava uvjete i za ključne i za važne subjekte; prema članku 16. primjenjuju se odredbe za ključne subjekte.",
   why_komunikacije="Pružatelji javnih elektroničkih komunikacijskih mreža i usluga kategoriziraju se neovisno o veličini - članak 9. podstavak 3. odnosno članak 10. podstavak 4.",
   why_povjerenje="Pružatelji usluga povjerenja kategoriziraju se neovisno o veličini - članak 10. podstavak 3.",
   why_dns="Registar naziva vršne nacionalne domene i pružatelji usluga DNS-a su ključni neovisno o veličini - članak 9. podstavak 2.",
   why_obrazovanje="Subjekti iz sustava obrazovanja razvrstavaju se u važne neovisno o veličini, ovisno o procjeni važnosti - članak 13.",
 ),
 "en": dict(
   slug="entity-categorisation-check",
   name="Entity categorisation check",
   desc="Sector, size and special circumstances produce a likely entity category under the Croatian Cybersecurity Act and the obligations that follow.",
   title="Entity categorisation check under the Croatian Cybersecurity Act",
   lead="Your category is determined by the competent authority, which notifies you in writing. Until then it helps to know what is likely. This tool applies the criteria in Articles 9 to 15 of the Act and shows which rule decided.",
   desc_meta="Free check of whether you are an essential or important entity under the Croatian Cybersecurity Act: sector from Annexes I and II, the size criterion and the special rules in Articles 11 to 13.",
   f_sector="Sector from Annex I or II of the Act",
   f_sector_sub="Select the sector you operate in. If you carry out several activities, the one covered by the annexes governs.",
   f_size="Size of the entity",
   f_size_sub="Under Article 15 the annual average headcount and the total annual turnover or total assets are taken into account.",
   sizes=[("mikro","Micro or small - fewer than 50 staff and up to EUR 10m turnover or assets"),
          ("srednji","Medium - 50 to 249 staff, or up to EUR 50m turnover / EUR 43m assets"),
          ("veliki","Large - 250 or more staff, or above EUR 50m turnover / EUR 43m assets")],
   f_special="Special circumstances",
   f_special_sub="Tick everything that applies. Each of these overrides the size criterion.",
   specials=[
     ("drzavna","State administration body or another state body with public authority","Article 12(1)"),
     ("dii","We operate, develop or maintain the state information infrastructure","Article 12(2)"),
     ("jlprs","Local or regional self-government unit","Article 12(3)"),
     ("kvalpovjerenje","We are a qualified trust service provider","Article 9, indent 2"),
     ("eracun","We are an e-invoice exchange intermediary","Article 9, indent 4"),
     ("kriticni","We are designated a critical entity under the critical infrastructure legislation","Article 9, indent 5"),
     ("cl11","We are the sole provider of an essential service, or our disruption would significantly affect public safety, security or health","Article 11"),
   ],
   btn="Check category", reset="Reset", copy="Copy summary", print="Print",
   copied="Summary copied",
   err="Select a sector and an entity size.",
   res_h="Likely category",
   r_kljucni="Essential entity", r_vazni="Important entity", r_izvan="Likely outside the scope of the Act",
   why="Why",
   next_h="What follows from this",
   csirt_h="Competent CSIRT for incident reporting",
   sector_body="Sectoral competent authority",
   ncsc="National Cyber Security Centre (NCSC-HR)",
   cert="National CERT",
   disclaimer="This is an informative assessment, not legal advice and not an official categorisation. Categorisation is carried out by the competent authority, which notifies you in writing. Only that notice governs. The tool does not cover every exception, in particular the importance assessments under Article 12(1) and (3) and Article 13.",
   privacy="The tool runs entirely in your browser. Nothing you enter reaches our server.",
   more="More on categorisation", more_url="/en/blog/entity-categorisation-croatian-cybersecurity-act/",
   sum_h="ENTITY CATEGORISATION CHECK",
   l_sector="Sector:", l_size="Size:", l_cat="Likely category:", l_why="Basis:",
   next_kljucni=["Compliance deadline: one year from delivery of the categorisation notice (Art. 26(5))",
                 "Verification: independent cybersecurity audit",
                 "Implementation of the 13 measures of Annex II at the prescribed level",
                 "Appointment of a contact person from the management body and at least two people to operationalise data delivery",
                 "Data delivery to NCSC-HR: name, company ID, size, address, contacts, IP address ranges, sector and entity type",
                 "Reporting of significant incidents within 24 h, 72 h and 30 days"],
   next_vazni=["Compliance deadline: one year from delivery of the categorisation notice (Art. 26(5))",
               "Verification: self-assessment against the ZSIS scoring framework",
               "Implementation of the 13 measures of Annex II at the prescribed level",
               "Appointment of a contact person from the management body and at least two people to operationalise data delivery",
               "Data delivery to NCSC-HR: name, company ID, size, address, contacts, IP address ranges, sector and entity type",
               "Reporting of significant incidents within 24 h, 72 h and 30 days"],
   next_izvan=["On the criteria selected you do not meet the general conditions for categorisation.",
               "That does not rule out Article 11: the competent authority may categorise you regardless of size if you are the sole provider of an essential service or your disruption would have significant effect.",
               "If you supply categorised entities, their measure 8 (supply chain security) will impose security requirements on you contractually anyway.",
               "The Annex II measures are useful without an obligation - they are what insurers and large customers ask for regardless."],
   why_prilog1_veliki="The sector is in Annex I and the entity exceeds the ceilings for medium-sized entities - Article 9, indent 1.",
   why_prilog1_srednji="The sector is in Annex I and the entity is medium-sized - Article 10, indent 2.",
   why_prilog2="The sector is in Annex II and the entity is medium-sized or larger - Article 10, indent 1.",
   why_mali="The sector is in the annexes, but the entity is micro or small, so the general size criteria are not met.",
   why_izvan="The selected sector is in neither Annex I nor Annex II of the Act.",
   why_dvostruko="The entity meets the conditions for both essential and important; under Article 16 the provisions for essential entities apply.",
   why_komunikacije="Providers of public electronic communications networks and services are categorised regardless of size - Article 9, indent 3 and Article 10, indent 4.",
   why_povjerenje="Trust service providers are categorised regardless of size - Article 10, indent 3.",
   why_dns="The national top-level domain registry and DNS service providers are essential regardless of size - Article 9, indent 2.",
   why_obrazovanje="Entities in the education system are classified as important regardless of size, subject to an importance assessment - Article 13.",
 ),
}


def build_tool2(lang, articles):
    t = L[lang]
    w = TOOLS_T[lang]
    c = CAT_T[lang]
    FOOT = footer(lang, articles)
    out_dir = os.path.join(ROOT, "en", "tools") if lang == "en" else os.path.join(ROOT, "alati")
    os.makedirs(os.path.join(out_dir, c["slug"]), exist_ok=True)
    url = SITE + w["hub"] + c["slug"] + "/"

    opts = "\n".join('        <option value="%s">%s</option>' % (k, (hr if lang == "hr" else en))
                     for k, pril, hr, en, cs, sh, se in SECTORS)
    sizes = "\n".join(
      '      <label class="check"><input type="radio" name="size" value="%s"><span>%s</span></label>' % (k, v)
      for k, v in c["sizes"])
    specials = "\n".join(
      '      <label class="check"><input type="checkbox" id="s-%s"><span>%s<em>%s</em></span></label>' % (k, lbl, art)
      for k, lbl, art in c["specials"])

    SECT_JS = json.dumps({k: {"p": pril, "csirt": cs, "body": (sh if lang == "hr" else se),
                              "name": (hr if lang == "hr" else en)}
                          for k, pril, hr, en, cs, sh, se in SECTORS}, ensure_ascii=False)
    TXT_JS = json.dumps({
      "err": c["err"], "kljucni": c["r_kljucni"], "vazni": c["r_vazni"], "izvan": c["r_izvan"],
      "why": c["why"], "nextH": c["next_h"], "csirtH": c["csirt_h"], "sectorBody": c["sector_body"],
      "ncsc": c["ncsc"], "cert": c["cert"],
      "nextK": c["next_kljucni"], "nextV": c["next_vazni"], "nextI": c["next_izvan"],
      "w1v": c["why_prilog1_veliki"], "w1s": c["why_prilog1_srednji"], "w2": c["why_prilog2"],
      "wm": c["why_mali"], "wi": c["why_izvan"], "wd": c["why_dvostruko"],
      "wkom": c["why_komunikacije"], "wpov": c["why_povjerenje"], "wdns": c["why_dns"],
      "wobr": c["why_obrazovanje"],
      "sumH": c["sum_h"], "lSector": c["l_sector"], "lSize": c["l_size"],
      "lCat": c["l_cat"], "lWhy": c["l_why"], "disclaimer": c["disclaimer"],
      "specials": {k: art for k, lbl, art in c["specials"]},
      "sizeNames": {k: v.split(" - ")[0] for k, v in c["sizes"]},
    }, ensure_ascii=False)

    JS = '''<script>
(function () {
  var S = %s, T = %s;
  var $ = function (id) { return document.getElementById(id); };

  function chk(id) { var e = $("s-" + id); return e && e.checked; }

  function decide(sector, size) {
    var s = S[sector], reasons = [], cat = null;
    // Pravila neovisna o velicini
    if (chk("drzavna"))       { cat = "K"; reasons.push(T.specials["drzavna"]); }
    if (chk("dii"))           { cat = "K"; reasons.push(T.specials["dii"]); }
    if (chk("kvalpovjerenje")){ cat = "K"; reasons.push(T.specials["kvalpovjerenje"]); }
    if (chk("eracun"))        { cat = "K"; reasons.push(T.specials["eracun"]); }
    if (chk("kriticni"))      { cat = "K"; reasons.push(T.specials["kriticni"]); }
    if (sector === "di-dns")  { cat = "K"; reasons.push(T.wdns); }
    if (!cat && chk("jlprs")) { cat = "V"; reasons.push(T.specials["jlprs"]); }
    if (!cat && sector === "obrazovanje") { cat = "V"; reasons.push(T.wobr); }
    if (!cat && sector === "di-povjerenje") { cat = "V"; reasons.push(T.wpov); }
    if (!cat && sector === "di-komunikacije") {
      cat = (size === "mikro") ? "V" : "K"; reasons.push(T.wkom);
    }
    if (!cat && chk("cl11")) {
      cat = (s && s.p === 1) ? "K" : "V"; reasons.push(T.specials["cl11"]);
    }
    // Opci kriteriji
    if (!cat) {
      if (!s || s.p === 0) { reasons.push(T.wi); return { cat: "-", reasons: reasons }; }
      if (size === "mikro") { reasons.push(T.wm); return { cat: "-", reasons: reasons }; }
      if (s.p === 1) {
        if (size === "veliki") { cat = "K"; reasons.push(T.w1v); }
        else { cat = "V"; reasons.push(T.w1s); }
      } else { cat = "V"; reasons.push(T.w2); }
    } else if (s && s.p !== 0 && size !== "mikro" && cat === "K") {
      var g = (s.p === 1 && size === "veliki") ? T.w1v : (s.p === 1 ? T.w1s : T.w2);
      if (reasons.indexOf(g) === -1) reasons.push(g + " " + T.wd);
    }
    return { cat: cat, reasons: reasons };
  }

  function calc() {
    var sector = $("c-sector").value;
    var sizeEl = document.querySelector('input[name="size"]:checked');
    var err = $("c-err");
    if (!sector || !sizeEl) { err.textContent = T.err; err.hidden = false; $("c-result").hidden = true; return; }
    err.hidden = true;
    var size = sizeEl.value, s = S[sector];
    var r = decide(sector, size);

    var label = r.cat === "K" ? T.kljucni : (r.cat === "V" ? T.vazni : T.izvan);
    var steps = r.cat === "K" ? T.nextK : (r.cat === "V" ? T.nextV : T.nextI);

    var html = '<div class="verdict ' + (r.cat === "K" ? "k" : r.cat === "V" ? "v" : "o") + '">' +
               '<div class="verdict-label">' + label + '</div>' +
               '<ul class="verdict-why">' + r.reasons.map(function (x) { return "<li>" + x + "</li>"; }).join("") +
               '</ul></div>';

    html += '<h3 class="res-sub">' + T.nextH + '</h3><ul class="next-list">' +
            steps.map(function (x) { return "<li>" + x + "</li>"; }).join("") + '</ul>';

    if (r.cat !== "-" && s && s.csirt) {
      html += '<div class="auth-box"><div><span class="auth-k">' + T.csirtH + '</span>' +
              (s.csirt === "cert" ? T.cert : T.ncsc) + '</div>';
      if (s.body) html += '<div><span class="auth-k">' + T.sectorBody + '</span>' + s.body + '</div>';
      html += '</div>';
    }

    $("c-out").innerHTML = html;
    $("c-result").hidden = false;

    var lines = [T.sumH, "", T.lSector + " " + (s ? s.name : "-"),
                 T.lSize + " " + T.sizeNames[size], T.lCat + " " + label, "",
                 T.lWhy];
    r.reasons.forEach(function (x) { lines.push("  - " + x); });
    lines.push("", T.nextH);
    steps.forEach(function (x) { lines.push("  - " + x); });
    if (r.cat !== "-" && s && s.csirt) lines.push("", T.csirtH + " " + (s.csirt === "cert" ? T.cert : T.ncsc));
    lines.push("", T.disclaimer);
    $("c-summary").textContent = lines.join("\\n");
    $("c-result").scrollIntoView({ behavior: "smooth", block: "start" });
    if (window.asTrack) window.asTrack("tool_categorisation");
  }

  $("c-calc").addEventListener("click", calc);
  $("c-reset").addEventListener("click", function () {
    $("c-sector").value = "";
    document.querySelectorAll('input[name="size"]').forEach(function (x) { x.checked = false; });
    document.querySelectorAll('.tool-panel input[type="checkbox"]').forEach(function (x) { x.checked = false; });
    $("c-result").hidden = true; $("c-err").hidden = true;
  });
  $("c-print").addEventListener("click", function () { window.print(); });
  $("c-copy").addEventListener("click", function () {
    var txt = $("c-summary").textContent;
    var done = function () { $("c-copied").hidden = false; setTimeout(function () { $("c-copied").hidden = true; }, 2500); };
    if (navigator.clipboard) { navigator.clipboard.writeText(txt).then(done, done); }
    else { var ta = document.createElement("textarea"); ta.value = txt; document.body.appendChild(ta);
           ta.select(); try { document.execCommand("copy"); } catch (e) {} ta.remove(); done(); }
  });
})();
</script>''' % (SECT_JS, TXT_JS)

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
        <label for="c-sector">%s</label>
        <select class="form-select-tool" id="c-sector">
          <option value="">&mdash;</option>
%s
        </select>
        <div class="sub">%s</div>
      </div>
      <div class="field">
        <label>%s</label>
        <div class="sub" style="margin:0 0 10px">%s</div>
%s
      </div>
      <div class="field">
        <label>%s</label>
        <div class="sub" style="margin:0 0 10px">%s</div>
%s
      </div>
      <p id="c-err" class="dl-left over" hidden style="margin-top:12px"></p>
      <div class="tool-actions">
        <button type="button" class="btn-primary" id="c-calc">%s</button>
        <button type="button" class="btn-ghost" id="c-reset">%s</button>
      </div>
      <p class="sub" style="margin-top:18px">%s</p>
    </div>

    <div class="tool-result" id="c-result" hidden>
      <div class="result-head"><h2>%s</h2></div>
      <div id="c-out"></div>
      <div class="summary-box" id="c-summary"></div>
      <div class="tool-actions">
        <button type="button" class="btn-ghost" id="c-copy">%s</button>
        <button type="button" class="btn-ghost" id="c-print">%s</button>
        <span class="copied" id="c-copied" hidden>%s</span>
      </div>
    </div>

    <article style="padding-top:40px">
      <div class="note"><p>%s</p></div>
      <p><a href="%s">%s &rarr;</a></p>
    </article>
    %s
  </div>
</main>
''' % (t["base"] or "/", t["home"], w["hub"], w["hub_name"], c["name"],
       w["hub_name"], c["title"], c["lead"],
       c["f_sector"], opts, c["f_sector_sub"],
       c["f_size"], c["f_size_sub"], sizes,
       c["f_special"], c["f_special_sub"], specials,
       c["btn"], c["reset"], c["privacy"],
       c["res_h"], c["copy"], c["print"], c["copied"],
       c["disclaimer"], c["more_url"], c["more"], cta_block(lang)) + FOOT + JS

    ld = [{
      "@context": "https://schema.org", "@type": "WebApplication",
      "name": c["title"], "description": c["desc_meta"], "url": url,
      "applicationCategory": "BusinessApplication", "operatingSystem": "Any",
      "browserRequirements": "JavaScript",
      "inLanguage": "hr-HR" if lang == "hr" else "en-GB", "isAccessibleForFree": True,
      "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"},
      "publisher": {"@type": "Organization", "name": "Adventure Spirit Consulting",
                    "legalName": "Adventure Spirit d.o.o.", "url": SITE + "/"},
    }, {
      "@context": "https://schema.org", "@type": "BreadcrumbList",
      "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": t["home"], "item": SITE + (t["base"] or "/")},
        {"@type": "ListItem", "position": 2, "name": w["hub_name"], "item": SITE + w["hub"]},
        {"@type": "ListItem", "position": 3, "name": c["name"], "item": url}]}]

    io.open(os.path.join(out_dir, c["slug"], "index.html"), "w", encoding="utf-8").write(
      page(c["title"] + " | Adventure Spirit Consulting", c["desc_meta"], body, url,
           lang=lang, extra_head=hreflang(SITE + "/alati/" + CAT_T["hr"]["slug"] + "/",
                                          SITE + "/en/tools/" + CAT_T["en"]["slug"] + "/"), ld=ld))



# ══════════════════════════════════════════════════════════════════
# ALAT 3 - Mini samoprocjena po 13 mjera
# ══════════════════════════════════════════════════════════════════
# Pitanje po mjeri + preporuka koja se prikaze kad je mjera ispod praga.
SA_Q_HR = [
 ("Je li uprava formalno usvojila politiku kibernetičke sigurnosti, imenovala odgovorne osobe i prima li redovito izvještaje o stanju?",
  "Uprava odobrava, imenuje, osigurava resurse i preispituje. Bez toga ostale mjere nemaju vlasnika.",
  "Donesite odluku uprave o politici i imenovanju odgovorne osobe, i uvedite izvještaj upravi barem jednom godišnje. Ovo je mjera s najduljim vremenom dozrijevanja jer se dokazuje zapisima koji nastaju kroz ciklus."),
 ("Postoji li ažuran inventar programske i sklopovske imovine, s izdvojenom kritičnom imovinom i klasifikacijom podataka?",
  "Inventar je preduvjet za procjenu rizika, nadzor i gotovo svaku drugu mjeru.",
  "Napravite jedan inventar i držite ga jedinim izvorom. Označite kritičnu imovinu i vlasnika po stavci. Ako imate odvojene popise po odjelima, prvo ih uskladite."),
 ("Postoji li dokumentiran proces procjene rizika, s registrom rizika, vlasnicima i planom obrade?",
  "Uredba traži pristup koji obuhvaća sve vrste opasnosti, ne samo informacijske prijetnje.",
  "Povežite svaki rizik s imovinom iz inventara i osobom kao vlasnikom. Proširite opseg procjene na fizičke opasnosti - požar, poplava, nestanak struje, ispad komunikacija."),
 ("Kako upravljate pravima pristupa kroz cijeli životni ciklus zaposlenika i vanjskog osoblja?",
  "Od zapošljavanja i ugovornih obveza do oduzimanja prava pri odlasku, uz odvojene administratorske račune.",
  "Uvedite postupak oduzimanja prava pri odlasku s dokazom o izvršenju i redovitu reviziju povlaštenih računa. Odvojite administratorske od redovnih računa."),
 ("Kako stojite s osnovnom higijenom - zakrpe, sigurnosne kopije, zaštita krajnjih točaka i edukacija zaposlenika?",
  "Mjera s najviše podmjera nakon upravljanja identitetima; ujedno ona koja najviše smanjuje stvarni rizik.",
  "Odredite tko je zadužen za zakrpe po svakom dijelu infrastrukture i uspostavite mjesečni ciklus. Testirajte vraćanje podataka iz sigurnosne kopije i zapišite koliko je trajalo."),
 ("Je li mreža segmentirana, je li perimetar zaštićen i prati li se mrežni promet?",
  "Segmentacija je najisplativija kontrola jer smanjuje doseg napada bez dodiranja pojedinih sustava.",
  "Odvojite poslužiteljsku od korisničke mreže i uklonite izravan pristup internetu s poslužitelja. Provjerite koji su servisi javno izloženi - vanjskom tražilicom, ne popisom iz informatike."),
 ("Primjenjuje li se načelo najmanje privilegije i višefaktorska autentifikacija na izloženim sučeljima?",
  "Posebno na udaljenom pristupu, elektroničkoj pošti i administratorskim računima.",
  "Uključite višefaktorsku autentifikaciju na udaljenom pristupu i za administratorske račune. Prebrojite članove najpovlaštenije grupe i uklonite one koji ta prava ne koriste."),
 ("Postavljate li sigurnosne zahtjeve dobavljačima i procjenjujete li rizik trećih strana?",
  "Ugovorne klauzule, upitnici, procjena i praćenje kroz vrijeme.",
  "Napravite popis dobavljača koji imaju pristup vašim sustavima ili podacima i procijenite ih po istoj metodologiji kao vlastite rizike. Provjerite obvezuju li ugovori na prijavu incidenta."),
 ("Postoje li sigurnosni zahtjevi u razvoju i održavanju sustava, uz upravljanje promjenama?",
  "Odvojena okruženja, testiranje prije puštanja u rad, pravila sigurnog kodiranja i za nabavljeni softver.",
  "Odvojite testno od produkcijskog okruženja i uvedite zapis o odobrenju promjene. Ako razvoj radi vanjski partner, ovi zahtjevi idu u ugovor."),
 ("Imate li pravila primjene kriptografije, zaštitu podataka u prijenosu i mirovanju te upravljanje ključevima?",
  "Uredba uz to traži i razmatranje kvantno otporne kriptografije razmjerno procijenjenom riziku.",
  "Popišite gdje se kriptografija koristi i tko upravlja ključevima. Provjerite jesu li sigurnosne kopije i prijenosna računala šifrirani."),
 ("Postoji li plan odgovora na incident, kriterij značajnosti i uspostavljen proces prijave nadležnom CSIRT-u?",
  "Rokovi su 24 sata, 72 sata i 30 dana, a teku od saznanja. Proces mora postojati prije incidenta.",
  "Odredite tko donosi odluku o značajnosti i tko šalje prijavu, uz zamjenu. Provjerite ima li netko pristup platformi PiXi. Napravite vježbu na stolu i izmjerite vrijeme do pripremljenog ranog upozorenja."),
 ("Postoji li analiza poslovnog utjecaja, planovi kontinuiteta i oporavka, i jesu li testirani?",
  "Plan koji nije isproban dokumentira namjeru, ne sposobnost.",
  "Ako svi procesi imaju isti RTO, analiza nije razlikovala - mjerite utjecaj kroz vrijeme, ne u jednoj točki. Provedite vježbu i zapišite rezultat; taj zapis je dokaz koji mjera traži."),
 ("Je li fizički pristup prostorima s opremom kontroliran, uz zaštitu od požara, vode i ispada napajanja?",
  "Zasebna mjera s vlastitim podmjerama, ne dio šireg skupa kontrola.",
  "Provjerite tko sve ima pristup prostoru s opremom i postoji li evidencija ulazaka. Zaštita napajanja i kabliranja spada ovdje, a redovito se previdi."),
]

SA_Q_EN = [
 ("Has the board formally adopted a cybersecurity policy, appointed responsible people and does it receive regular reports?",
  "The board approves, appoints, provides resources and reviews. Without that the other measures have no owner.",
  "Pass a board decision on the policy and the appointment, and introduce a report to the board at least annually. This measure has the longest lead time because it is evidenced by records produced over a cycle."),
 ("Is there a current inventory of software and hardware assets, with critical assets identified and data classified?",
  "The inventory is a precondition for risk assessment, monitoring and almost every other measure.",
  "Build one inventory and keep it as the single source. Mark critical assets and an owner per item. If departments keep separate lists, reconcile them first."),
 ("Is there a documented risk assessment process, with a risk register, owners and a treatment plan?",
  "The Regulation requires an all-hazards approach, not just information threats.",
  "Link every risk to an asset in the inventory and to a person as owner. Widen the scope to physical hazards - fire, flood, power loss, communications failure."),
 ("How do you manage access rights across the full lifecycle of employees and external staff?",
  "From hiring and contractual duties through to revoking rights on departure, with separate administrator accounts.",
  "Introduce a leaver process with evidence of execution, and a regular review of privileged accounts. Separate administrator accounts from ordinary ones."),
 ("How do you stand on basic hygiene - patching, backups, endpoint protection and staff training?",
  "The measure with the most sub-measures after identity management, and the one that reduces real risk most.",
  "Name who is responsible for patching each part of the infrastructure and establish a monthly cycle. Test a restore from backup and record how long it took."),
 ("Is the network segmented, is the perimeter protected and is traffic monitored?",
  "Segmentation is the highest-return control because it limits reach without touching individual systems.",
  "Separate server from user networks and remove direct internet access from servers. Check which services are publicly exposed - with an external search engine, not with IT's list."),
 ("Is least privilege applied, and multi-factor authentication on exposed interfaces?",
  "Particularly on remote access, email and administrator accounts.",
  "Enable multi-factor authentication on remote access and for administrator accounts. Count the members of the most privileged group and remove those not using those rights."),
 ("Do you set security requirements for suppliers and assess third-party risk?",
  "Contractual clauses, questionnaires, assessment and monitoring over time.",
  "List suppliers with access to your systems or data and assess them with the same methodology as your own risks. Check whether contracts oblige them to report incidents."),
 ("Are there security requirements in system development and maintenance, with change management?",
  "Separated environments, testing before go-live, secure coding rules that also apply to acquired software.",
  "Separate test from production and introduce a record of change approval. If an external partner develops for you, these requirements belong in the contract."),
 ("Do you have rules on cryptography, protection of data in transit and at rest, and key management?",
  "The Regulation also asks you to consider quantum-resistant cryptography proportionate to assessed risk.",
  "List where cryptography is used and who manages the keys. Check whether backups and laptops are encrypted."),
 ("Is there an incident response plan, a significance criterion and an established process for notifying the competent CSIRT?",
  "The deadlines are 24 hours, 72 hours and 30 days, running from awareness. The process must exist before the incident.",
  "Decide who makes the significance call and who sends the notification, with a deputy. Check that someone has access to the PiXi platform. Run a tabletop and measure the time to a prepared early warning."),
 ("Is there a business impact analysis, continuity and recovery plans, and have they been exercised?",
  "A plan that has never been exercised documents intent, not capability.",
  "If every process carries the same RTO, the analysis did not discriminate - measure impact over time, not at a single point. Run an exercise and record the result; that record is the evidence the measure asks for."),
 ("Is physical access to areas holding equipment controlled, with fire, water and power protection?",
  "A standalone measure with its own sub-measures, not part of a wider control set.",
  "Check who has access to the equipment area and whether entries are logged. Power and cabling protection belongs here and is regularly overlooked."),
]

SA_T = {
 "hr": dict(
   slug="samoprocjena-13-mjera", name="Mini samoprocjena po 13 mjera",
   desc="Trinaest pitanja, jedno po mjeri iz Priloga II. Uredbe. Rezultat je graf spremnosti s pragom od 60 % i popis mjera koje su ispod njega.",
   title="Mini samoprocjena spremnosti po 13 mjera ZKS-a",
   lead="Trinaest pitanja, jedno po mjeri iz Priloga II. Uredbe. Nije zamjena za formalnu samoprocjenu prema bodovnom okviru ZSIS-a, ali pokazuje gdje ste i što je prvo na redu.",
   desc_meta="Besplatna mini samoprocjena spremnosti po 13 mjera upravljanja kibernetičkim sigurnosnim rizicima iz Priloga II. Uredbe NN 135/2024, s grafom i pragom spremnosti.",
   scale_h="Za svaku mjeru odaberite tvrdnju koja najbolje opisuje stvarno stanje, ne željeno.",
   scale=["Ne postoji ili se ne provodi",
          "Provodi se djelomično, nije dokumentirano",
          "Dokumentirano, ali se primjenjuje neujednačeno",
          "Dokumentirano, primjenjuje se, postoje zapisi",
          "Uz to se redovito preispituje i poboljšava"],
   btn="Prikaži rezultat", reset="Poništi", copy="Kopiraj sažetak", print="Ispiši",
   copied="Sažetak kopiran",
   err="Odgovorite na sva pitanja - nedostaje ih još %d.",
   progress="Odgovoreno %d od 13",
   res_h="Vaša snimka stanja",
   score_lbl="Spremnost",
   verdict=[(0, 40, "Sustav je u ranoj fazi. Prioritet su mjere 1, 2 i 3 - bez vlasnika, inventara i registra rizika ostale mjere nemaju na čemu stajati."),
            (40, 60, "Temelji postoje, ali dokazna baza je nejednaka. Većina posla je dopuna postojećeg, ne pisanje novog."),
            (60, 80, "Iznad praga spremnosti. Preostalo je produbljivanje i zapisi koji dokazuju da sustav živi kroz ciklus."),
            (80, 101, "Visoka spremnost. Fokus prelazi na dokazivanje kontinuiteta primjene i na pripremu za provjeru.")],
   chart_h="Spremnost po mjerama", thresh="PRAG 60 %",
   legend="Jedna kocka je jedna razina zrelosti. Sivi stupci su mjere ispod praga spremnosti. Prag je naš interni pokazatelj, a ne zakonski prag - bodovne pragove propisuje okvir ZSIS-a po podmjeri i razini.",
   gaps_h="Mjere ispod praga", gaps_none="Nijedna mjera nije ispod praga spremnosti.",
   score_of="%d od 5",
   disclaimer="Ovo je informativna procjena zrelosti, ne formalna samoprocjena. Formalna samoprocjena provodi se po bodovnom okviru ZSIS-a, gdje se svaka od 13 mjera razrađuje kroz 99 podmjera i katalog od 132 kontrole, s pragom po kontroli i dodatnim pragom prosjeka po podmjeri. Ovaj alat daje jednu ocjenu po mjeri i služi za grubu orijentaciju.",
   privacy="Alat radi isključivo u vašem pregledniku. Odgovora nema na našem poslužitelju.",
   more="Kako se boduje formalna samoprocjena", more_url="/blog/kako-se-boduje-samoprocjena/",
   sum_h="MINI SAMOPROCJENA - 13 MJERA ZKS-a", sum_score="Ukupna spremnost:", sum_gaps="Ispod praga:",
   cta_h="Ovo je izvadak iz naše GRC platforme",
   cta_p="U platformi se ista procjena vodi po svih 99 podmjera i 132 kontrole, s dokazima, vlasnicima, rokovima i revizijskim tragom - pa napredak pratite kontinuirano, a ne jednom godišnje.",
   cta_b1="Pogledajte GRC Portal", cta_b2="Dogovorite razgovor",
   rep_h="Detaljan izvještaj na e-mail",
   rep_p="Pošaljemo vam vaš rezultat s preporukama po mjerama, i kratku napomenu što bismo prvo napravili da smo na vašem mjestu. Izvještaj možete i odmah ispisati ili spremiti kao PDF gumbom iznad.",
   rep_email="Vaša e-mail adresa", rep_org="Organizacija (nije obavezno)",
   rep_consent='Pristajem da mi Adventure Spirit d.o.o. pošalje ovaj izvještaj na navedenu adresu i da me kontaktira u vezi s njim. Privolu mogu povući u svakom trenutku porukom na info@adventurespirit.hr. Više u <a href="/privatnost/">politici privatnosti</a>.',
   rep_btn="Pošalji mi izvještaj",
   rep_legal="Šaljemo samo rezultat ove procjene i odgovor na njega. Ne uvrštavamo vas na listu za slanje obavijesti i ne prosljeđujemo vašu adresu trećim stranama.",
   rep_ok="Hvala. Izvještaj šaljemo na navedenu adresu, obično isti radni dan.",
   rep_err="Slanje nije uspjelo. Kontaktirajte nas izravno na info@adventurespirit.hr.",
   rep_need="Upišite ispravnu e-mail adresu i potvrdite privolu.",
   rep_sending="Šaljem...",
   print_title="Snimka stanja po 13 mjera ZKS-a",
 ),
 "en": dict(
   slug="readiness-check-13-measures", name="Readiness check against the 13 measures",
   desc="Thirteen questions, one per measure of Annex II. The result is a readiness chart with a 60 % threshold and a list of the measures below it.",
   title="Readiness check against the 13 measures",
   lead="Thirteen questions, one per measure of Annex II of the Croatian Cybersecurity Regulation. Not a substitute for the formal self-assessment against the ZSIS scoring framework, but it shows where you stand and what comes first.",
   desc_meta="Free readiness check against the 13 cyber risk management measures of Annex II of the Croatian Cybersecurity Regulation, with a chart and a readiness threshold.",
   scale_h="For each measure choose the statement that best describes the actual state, not the intended one.",
   scale=["Does not exist or is not performed",
          "Partly performed, not documented",
          "Documented, but applied inconsistently",
          "Documented, applied, records exist",
          "And regularly reviewed and improved"],
   btn="Show result", reset="Reset", copy="Copy summary", print="Print",
   copied="Summary copied",
   err="Answer all questions - %d still missing.",
   progress="%d of 13 answered",
   res_h="Your readiness snapshot",
   score_lbl="Readiness",
   verdict=[(0, 40, "The system is at an early stage. Measures 1, 2 and 3 come first - without an owner, an inventory and a risk register the other measures have nothing to stand on."),
            (40, 60, "The foundations are there but the evidence base is uneven. Most of the work is extending what exists rather than writing something new."),
            (60, 80, "Above the readiness threshold. What remains is depth, and the records proving the system runs through a full cycle."),
            (80, 101, "High readiness. The focus moves to evidencing continuity of application and preparing for verification.")],
   chart_h="Readiness by measure", thresh="THRESHOLD 60 %",
   legend="One block is one maturity level. Grey columns are measures below the readiness threshold. The threshold is our internal indicator, not a statutory one - the statutory thresholds are set by the ZSIS framework per sub-measure and level.",
   gaps_h="Measures below the threshold", gaps_none="No measure is below the readiness threshold.",
   score_of="%d of 5",
   disclaimer="This is an informative maturity assessment, not a formal self-assessment. The formal self-assessment follows the ZSIS scoring framework, where each of the 13 measures is broken into 99 sub-measures and a catalogue of 132 controls, with a threshold per control and an additional average threshold per sub-measure. This tool gives one score per measure and serves for rough orientation.",
   privacy="The tool runs entirely in your browser. Your answers do not reach our server.",
   more="How the formal self-assessment is scored", more_url="/en/blog/how-self-assessment-is-scored/",
   sum_h="READINESS CHECK - 13 MEASURES", sum_score="Overall readiness:", sum_gaps="Below threshold:",
   cta_h="This is an extract from our GRC platform",
   cta_p="In the platform the same assessment runs across all 99 sub-measures and 132 controls, with evidence, owners, deadlines and an audit trail - so you track progress continuously rather than once a year.",
   cta_b1="See the GRC Portal", cta_b2="Book a conversation",
   rep_h="Detailed report by email",
   rep_p="We send you your result with per-measure recommendations, and a short note on what we would tackle first in your position. You can also print or save the report as PDF right now with the button above.",
   rep_email="Your email address", rep_org="Organisation (optional)",
   rep_consent='I agree that Adventure Spirit d.o.o. may send this report to the address given and contact me about it. I can withdraw this consent at any time by writing to info@adventurespirit.hr. See the <a href="/en/privacy/">privacy policy</a>.',
   rep_btn="Send me the report",
   rep_legal="We send only the result of this assessment and a response to it. You are not added to a mailing list and your address is not shared with third parties.",
   rep_ok="Thank you. We will send the report to the address given, usually the same working day.",
   rep_err="Sending failed. Please contact us directly at info@adventurespirit.hr.",
   rep_need="Enter a valid email address and confirm consent.",
   rep_sending="Sending...",
   print_title="Readiness snapshot against the 13 measures",
 ),
}


def build_tool3(lang, articles):
    t = L[lang]
    w = TOOLS_T[lang]
    a = SA_T[lang]
    QS = SA_Q_HR if lang == "hr" else SA_Q_EN
    MJ = MJERE if lang == "hr" else MJERE_EN
    FOOT = footer(lang, articles)
    out_dir = os.path.join(ROOT, "en", "tools") if lang == "en" else os.path.join(ROOT, "alati")
    os.makedirs(os.path.join(out_dir, a["slug"]), exist_ok=True)
    url = SITE + w["hub"] + a["slug"] + "/"

    qs = []
    for i, (q, sub, rec) in enumerate(QS):
        opts = "\n".join(
          '          <label class="q-opt"><input type="radio" name="m%d" value="%d"><span>%s</span></label>'
          % (i + 1, v + 1, a["scale"][v]) for v in range(5))
        qs.append('''      <div class="q-block">
        <div class="q-head"><span class="q-num">%02d</span><span class="q-title">%s</span></div>
        <p class="q-sub">%s &middot; %s</p>
        <div class="q-opts">
%s
        </div>
      </div>''' % (i + 1, q, MJ[i][1], sub, opts))

    JS = '''<script>
(function () {
  var T = %s;
  var $ = function (id) { return document.getElementById(id); };

  function answers() {
    var out = [];
    for (var i = 1; i <= 13; i++) {
      var el = document.querySelector('input[name="m' + i + '"]:checked');
      out.push(el ? parseInt(el.value, 10) : 0);
    }
    return out;
  }
  function progress() {
    var n = answers().filter(function (x) { return x > 0; }).length;
    $("sa-bar").style.width = Math.round(n / 13 * 100) + "%%";
    $("sa-prog").textContent = T.progress.replace("%%d", n);
  }
  document.querySelectorAll('.q-opt input').forEach(function (el) {
    el.addEventListener("change", progress);
  });

  function calc() {
    var v = answers(), missing = v.filter(function (x) { return x === 0; }).length;
    var err = $("sa-err");
    if (missing) { err.textContent = T.err.replace("%%d", missing); err.hidden = false; $("sa-result").hidden = true; return; }
    err.hidden = true;

    var total = v.reduce(function (s, x) { return s + x; }, 0);
    var pct = Math.round(total / 65 * 100);

    var cols = "";
    for (var i = 0; i < 13; i++) {
      var cells = "";
      for (var k = 0; k < 5; k++) cells += '<div class="sa-cell' + (k < v[i] ? " on" : "") + '"></div>';
      cols += '<div class="sa-col ' + (v[i] >= 3 ? "ok" : "low") + '">' +
              '<div class="sa-lab">' + (i + 1 < 10 ? "0" : "") + (i + 1) + '</div>' + cells + '</div>';
    }
    $("sa-chart").innerHTML = cols;
    $("sa-pct").innerHTML = pct + '<small>%%</small>';

    var msg = T.verdict[T.verdict.length - 1][2];
    for (var j = 0; j < T.verdict.length; j++) {
      if (pct >= T.verdict[j][0] && pct < T.verdict[j][1]) { msg = T.verdict[j][2]; break; }
    }
    $("sa-msg").textContent = msg;

    var gaps = "";
    for (var i2 = 0; i2 < 13; i2++) {
      if (v[i2] >= 3) continue;
      gaps += '<div class="gap-item' + (v[i2] === 1 ? " crit" : "") + '">' +
        '<div class="gap-h"><span class="gap-n">' + (i2 + 1 < 10 ? "0" : "") + (i2 + 1) + '</span>' +
        '<span class="gap-t">' + T.names[i2] + '</span>' +
        '<span class="gap-s">' + T.scoreOf.replace("%%d", v[i2]) + '</span></div>' +
        '<div class="gap-d">' + T.recs[i2] + '</div></div>';
    }
    $("sa-gaps").innerHTML = gaps || '<p class="dl-left ok" style="font-size:14px">' + T.gapsNone + '</p>';
    $("sa-result").hidden = false;

    var lines = [T.sumH, "", T.sumScore + " " + pct + " %%", "", ];
    for (var i3 = 0; i3 < 13; i3++) {
      lines.push("  " + (i3 + 1 < 10 ? "0" : "") + (i3 + 1) + "  " +
        "#####".slice(0, v[i3]) + ".....".slice(0, 5 - v[i3]) + "  " + T.names[i3]);
    }
    var below = [];
    for (var i4 = 0; i4 < 13; i4++) if (v[i4] < 3) below.push(i4 + 1);
    lines.push("", T.sumGaps + " " + (below.length ? below.join(", ") : "-"));
    lines.push("", T.disclaimer);
    $("sa-summary").textContent = lines.join("\\n");
    lastResult = lines.join("\\n");
    $("sa-result").scrollIntoView({ behavior: "smooth", block: "start" });
    if (window.asTrack) window.asTrack("selfassessment_completed", pct);
  }

  // Zahtjev za izvjestajem na e-mail
  var lastResult = null;
  $("rp-send").addEventListener("click", function () {
    var mail = $("rp-mail").value.trim(), org = $("rp-org").value.trim();
    var msg = $("rp-msg");
    var okMail = /^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$/.test(mail);
    if (!okMail || !$("rp-ok").checked || !lastResult) {
      msg.textContent = T.repNeed; msg.className = "report-msg bad"; msg.hidden = false; return;
    }
    var btn = $("rp-send"), label = btn.textContent;
    btn.disabled = true; btn.textContent = T.repSending; msg.hidden = true;
    fetch("https://formspree.io/f/__FS_OBAVIJESTI__", {
      method: "POST",
      headers: { "Content-Type": "application/json", Accept: "application/json" },
      body: JSON.stringify({
        name: org || "-", email: mail, _subject: T.repSubject,
        message: T.repSubject + "\\n" + (org ? T.repOrg2 + " " + org + "\\n" : "") +
                 "\\n" + lastResult + "\\n\\n" + T.repConsentLog
      })
    }).then(function (r) {
      if (!r.ok) throw new Error();
      msg.textContent = T.repOk; msg.className = "report-msg ok"; msg.hidden = false;
      $("rp-mail").value = ""; $("rp-org").value = ""; $("rp-ok").checked = false;
      if (window.asTrack) window.asTrack("report_requested");
    }).catch(function () {
      msg.textContent = T.repErr; msg.className = "report-msg bad"; msg.hidden = false;
    }).finally(function () { btn.disabled = false; btn.textContent = label; });
  });

  $("sa-calc").addEventListener("click", calc);
  $("sa-reset").addEventListener("click", function () {
    document.querySelectorAll('.q-opt input').forEach(function (x) { x.checked = false; });
    $("sa-result").hidden = true; $("sa-err").hidden = true; progress();
  });
  $("sa-print").addEventListener("click", function () { window.print(); });
  $("sa-copy").addEventListener("click", function () {
    var txt = $("sa-summary").textContent;
    var done = function () { $("sa-copied").hidden = false; setTimeout(function () { $("sa-copied").hidden = true; }, 2500); };
    if (navigator.clipboard) { navigator.clipboard.writeText(txt).then(done, done); }
    else { var ta = document.createElement("textarea"); ta.value = txt; document.body.appendChild(ta);
           ta.select(); try { document.execCommand("copy"); } catch (e) {} ta.remove(); done(); }
  });
  progress();
})();
</script>''' % json.dumps({
      "progress": a["progress"], "err": a["err"], "verdict": a["verdict"],
      "names": [m[1] for m in MJ], "recs": [q[2] for q in QS],
      "gapsNone": a["gaps_none"], "scoreOf": a["score_of"],
      "sumH": a["sum_h"], "sumScore": a["sum_score"], "sumGaps": a["sum_gaps"],
      "disclaimer": a["disclaimer"],
      "repNeed": a["rep_need"], "repSending": a["rep_sending"],
      "repOk": a["rep_ok"], "repErr": a["rep_err"],
      "repSubject": ("Zahtjev za izvjestajem - mini samoprocjena 13 mjera" if lang == "hr"
                     else "Report request - readiness check, 13 measures"),
      "repOrg2": ("Organizacija:" if lang == "hr" else "Organisation:"),
      "repConsentLog": ("Privola za slanje izvjestaja i kontakt dana kroz obrazac na "
                        "/alati/samoprocjena-13-mjera/" if lang == "hr"
                        else "Consent given via the form at /en/tools/readiness-check-13-measures/"),
    }, ensure_ascii=False)

    body = header(lang, active_blog=False) + '''
<main>
  <div class="container narrow">
    <div class="crumbs">
      <a href="%s">%s</a><span>&rsaquo;</span><a href="%s">%s</a><span>&rsaquo;</span>%s
    </div>
    <div class="print-head">
      <div class="ph-name">Adventure Spirit Consulting &middot; %s</div>
      <div class="ph-meta">Adventure Spirit d.o.o. &middot; adventurespirit.hr &middot; info@adventurespirit.hr &middot; +385 95 504 1496</div>
    </div>
    <header class="art-head">
      <div class="eyebrow">%s</div>
      <h1>%s</h1>
      <p class="art-lead">%s</p>
    </header>

    <div class="tool-panel">
      <div class="progress-bar"><i id="sa-bar"></i></div>
      <p class="progress-txt" id="sa-prog"></p>
      <p class="hint">%s</p>
%s
      <p id="sa-err" class="dl-left over" hidden style="margin-top:16px"></p>
      <div class="tool-actions">
        <button type="button" class="btn-primary" id="sa-calc">%s</button>
        <button type="button" class="btn-ghost" id="sa-reset">%s</button>
      </div>
      <p class="sub" style="margin-top:18px">%s</p>
    </div>

    <div class="tool-result" id="sa-result" hidden>
      <div class="result-head"><h2>%s</h2></div>
      <div class="score-top">
        <div><div class="score-num" id="sa-pct"></div><div class="score-lbl">%s</div></div>
        <p class="score-txt" id="sa-msg"></p>
      </div>
      <h3 class="res-sub">%s</h3>
      <div class="sa-chart-wrap">
        <div class="sa-chart" id="sa-chart"></div>
        <div class="sa-thresh"><span>%s</span></div>
      </div>
      <p class="sub" style="margin:-14px 0 30px">%s</p>
      <h3 class="res-sub">%s</h3>
      <div id="sa-gaps" style="margin-bottom:28px"></div>
      <div class="summary-box" id="sa-summary"></div>
      <div class="tool-actions">
        <button type="button" class="btn-ghost" id="sa-copy">%s</button>
        <button type="button" class="btn-ghost" id="sa-print">%s</button>
        <span class="copied" id="sa-copied" hidden>%s</span>
      </div>

      <div class="report-box">
        <h3>%s</h3>
        <p>%s</p>
        <div class="report-row">
          <label class="vh" for="rp-mail">%s</label>
          <input type="email" id="rp-mail" placeholder="%s" autocomplete="email">
          <label class="vh" for="rp-org">%s</label>
          <input type="text" id="rp-org" placeholder="%s" autocomplete="organization">
        </div>
        <label class="consent"><input type="checkbox" id="rp-ok"><span>%s</span></label>
        <div class="tool-actions" style="border:none;padding-top:14px;margin-top:6px">
          <button type="button" class="btn-primary" id="rp-send">%s</button>
        </div>
        <p class="report-msg" id="rp-msg" hidden></p>
        <p class="report-legal">%s</p>
      </div>

      <div class="art-cta" style="margin-top:36px">
        <h3>%s</h3>
        <p>%s</p>
        <div class="cta-btns">
          <a href="https://app.adventurespirit.hr" target="_blank" rel="noopener" class="btn-primary">%s</a>
          <a href="%s" class="btn-outline">%s</a>
        </div>
      </div>
    </div>

    <article style="padding-top:40px">
      <div class="note"><p>%s</p></div>
      <p><a href="%s">%s &rarr;</a></p>
    </article>
  </div>
</main>
''' % (t["base"] or "/", t["home"], w["hub"], w["hub_name"], a["name"],
       a["print_title"], w["hub_name"], a["title"], a["lead"],
       a["scale_h"], "\n".join(qs), a["btn"], a["reset"], a["privacy"],
       a["res_h"], a["score_lbl"], a["chart_h"], a["thresh"], a["legend"],
       a["gaps_h"], a["copy"], a["print"], a["copied"],
       a["rep_h"], a["rep_p"], a["rep_email"], a["rep_email"], a["rep_org"], a["rep_org"], a["rep_consent"],
       a["rep_btn"], a["rep_legal"],
       a["cta_h"], a["cta_p"], a["cta_b1"],
       "/kontakt/" if lang == "hr" else "/en/contact/", a["cta_b2"],
       a["disclaimer"], a["more_url"], a["more"]) + FOOT + JS

    ld = [{
      "@context": "https://schema.org", "@type": "WebApplication",
      "name": a["title"], "description": a["desc_meta"], "url": url,
      "applicationCategory": "BusinessApplication", "operatingSystem": "Any",
      "browserRequirements": "JavaScript",
      "inLanguage": "hr-HR" if lang == "hr" else "en-GB", "isAccessibleForFree": True,
      "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"},
      "publisher": {"@type": "Organization", "name": "Adventure Spirit Consulting",
                    "legalName": "Adventure Spirit d.o.o.", "url": SITE + "/"},
    }, {
      "@context": "https://schema.org", "@type": "BreadcrumbList",
      "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": t["home"], "item": SITE + (t["base"] or "/")},
        {"@type": "ListItem", "position": 2, "name": w["hub_name"], "item": SITE + w["hub"]},
        {"@type": "ListItem", "position": 3, "name": a["name"], "item": url}]}]

    io.open(os.path.join(out_dir, a["slug"], "index.html"), "w", encoding="utf-8").write(
      page(a["title"] + " | Adventure Spirit Consulting", a["desc_meta"], body, url,
           lang=lang, extra_head=hreflang(SITE + "/alati/" + SA_T["hr"]["slug"] + "/",
                                          SITE + "/en/tools/" + SA_T["en"]["slug"] + "/"), ld=ld))



# ══════════════════════════════════════════════════════════════════
# STRANICE USLUGA
# ══════════════════════════════════════════════════════════════════
# Sadrzaj koraka i isporucevina za hrvatsku verziju izvlaci se iz
# modala u index.html pri pokretanju, da se ne odrzava na dva mjesta.
USLUGE_META = [
 dict(key="zks", hr="zks-nis2-uskladenost", en="csa-nis2-compliance", icon="shield",
      nEN="CSA / NIS2 compliance", subEN="Croatian Cybersecurity Act &middot; EU NIS2 Directive",
      badgeHR="Zakonska obveza", badgeEN="Statutory duty",
      leadEN="We deliver full implementation of cyber security for essential and important entities under the Croatian Cybersecurity Act. We cover everything from establishing your category and competent authority to setting up incident notification to the competent CSIRT.",
      stepsEN=[("01","Gap assessment","Scoring against each of the 13 measures of Annex II of the Regulation (OG 135/2024), by sub-measure and control, with a list of the evidence that is missing."),
               ("02","Categorisation and competence","Establishing your status (essential or important entity), the competent authority, the level of implementation and the deadlines that follow."),
               ("03","Implementation of the 13 measures","Risk management, supply chain security, MFA, encryption, incident handling, business continuity, training, cryptography, physical security and access management."),
               ("04","Self-assessment and audit preparation","Self-assessment for important entities, or an internal review simulating the audit process for essential entities, with management review."),
               ("05","Incident management","Establishing the notification process to the competent CSIRT: early warning within 24 hours, incident notification within 72 hours, final report within 30 days."),
               ("06","Continuous monitoring","Integration into the GRC platform to track measure status, incidents and deadlines in real time.")],
      delsEN=["Gap assessment report","Cyber security policy","Remediation plan","Measure register","Incident notification process","GRC platform setup"],
      mjere=[1,2,3,4,5,6,7,8,9,10,11,12,13],
      clHR=["trinaest-mjera-priloga-ii","kategorizacija-prema-zks-u","korelacijski-pregled-mjera"],
      clEN=["thirteen-measures-annex-ii","entity-categorisation-croatian-cybersecurity-act","how-self-assessment-is-scored"],
      sekt=["energetika","zdravstvo-i-farmacija","prehrambena-industrija","javna-uprava"]),

 dict(key="gdpr", hr="gdpr-uskladenost", en="gdpr-compliance", icon="lock",
      nEN="GDPR compliance", subEN="Regulation (EU) 2016/679",
      badgeHR="EU Regulativa", badgeEN="EU regulation",
      leadEN="We establish every personal data protection process - from the record of processing activities and impact assessments to DPO support and breach notification to the supervisory authority.",
      stepsEN=[("01","Records of processing","Mapping every processing activity, its purpose, lawful basis, categories of data and retention period."),
               ("02","Lawful bases and consent","Reviewing bases, consent mechanisms and evidence that consent was validly obtained."),
               ("03","Impact assessments","DPIA where processing is likely to result in high risk, with a documented outcome."),
               ("04","Processor contracts","Data processing agreements, transfers outside the EU and safeguards."),
               ("05","Data subject rights","A process for access, rectification, erasure and portability requests, within the statutory deadlines."),
               ("06","Breach handling","Risk assessment and notification to the supervisory authority within 72 hours, with notification to data subjects where required.")],
      delsEN=["Record of processing activities","DPIA","Processor contracts","Register of data subject requests","Breach procedure","Staff training"],
      mjere=[2,3,4,10,11],
      clHR=["rokovi-prijave-incidenta","registar-ai-sustava-i-registar-imovine"],
      clEN=["incident-reporting-deadlines","ai-inventory-and-asset-register"],
      sekt=["zdravstvo-i-farmacija","osiguranje","javna-uprava","bankarstvo-i-financije"]),

 dict(key="iso27001", hr="iso-27001", en="iso-27001", icon="award",
      nEN="ISO/IEC 27001 - Information security", subEN="ISO/IEC 27001:2022",
      badgeHR="Međunarodni standard", badgeEN="International standard",
      leadEN="Gap analysis, ISMS implementation, risk assessment, Statement of Applicability and full preparation for the certification audit against ISO/IEC 27001:2022.",
      stepsEN=[("01","Gap analysis","Current state against the requirements of the standard and the 93 Annex A controls."),
               ("02","Scope and context","Defining the ISMS scope, interested parties and their requirements."),
               ("03","Risk assessment","Methodology, risk register, treatment plan and risk acceptance criteria."),
               ("04","Statement of Applicability","Justification for each control included or excluded."),
               ("05","Documentation and implementation","Policies, procedures and records, with staff training."),
               ("06","Internal audit and certification","Internal audit programme, management review and support through the certification audit.")],
      delsEN=["ISMS documentation","Risk register","Statement of Applicability","Internal audit report","Management review","Certification readiness"],
      mjere=[1,2,3,4,7,8,12],
      clHR=["iso-27001-i-zks","iso-27002-2022-atributi-kontrola","korelacijski-pregled-mjera"],
      clEN=["iso-27001-and-the-cybersecurity-act","iso-27002-2022-control-attributes"],
      sekt=["bankarstvo-i-financije","digitalna-infrastruktura-i-ikt","osiguranje"]),

 dict(key="iso9001", hr="iso-9001", en="iso-9001", icon="gear",
      nEN="ISO 9001 - Quality management", subEN="ISO 9001:2015",
      badgeHR="Upravljanje kvalitetom", badgeEN="Quality management",
      leadEN="QMS implementation, process documentation, quality objectives and KPIs, and preparation for the certification audit.",
      stepsEN=[("01","Gap analysis","Current state against the requirements of the standard."),
               ("02","Process map","Identifying processes, their inputs, outputs, owners and interactions."),
               ("03","Quality objectives","Measurable objectives and indicators at process level."),
               ("04","Documentation","Quality policy, procedures and records."),
               ("05","Internal audit","Audit programme, findings and corrective actions."),
               ("06","Certification","Management review and support through the certification audit.")],
      delsEN=["Quality policy","Process map","Objectives and KPIs","Procedures","Internal audit report","Certification readiness"],
      mjere=[1,3],
      clHR=["korelacijski-pregled-mjera","registar-rizika-koji-prolazi-provjeru"],
      clEN=["risk-register-that-passes-review"],
      sekt=["prehrambena-industrija","promet-i-logistika"]),

 dict(key="iso14001", hr="iso-14001", en="iso-14001", icon="leaf",
      nEN="ISO 14001 - Environmental management", subEN="ISO 14001:2015",
      badgeHR="Okolišni standard", badgeEN="Environmental standard",
      leadEN="EMS implementation - identification of environmental aspects and impacts, a legal compliance register, carbon footprint reduction and certification readiness.",
      stepsEN=[("01","Gap analysis","Current state against the requirements of the standard."),
               ("02","Aspects and impacts","Identifying environmental aspects and assessing their significance."),
               ("03","Legal register","Applicable environmental legislation and evidence of compliance."),
               ("04","Objectives and programmes","Measurable environmental objectives with owners and deadlines."),
               ("05","Operational control","Procedures, emergency preparedness and response."),
               ("06","Certification","Internal audit, management review and support through certification.")],
      delsEN=["Environmental policy","Aspects and impacts register","Legal register","Objectives and programmes","Internal audit report","Certification readiness"],
      mjere=[1,3,13],
      clHR=["registar-rizika-koji-prolazi-provjeru"],
      clEN=["risk-register-that-passes-review"],
      sekt=["energetika","prehrambena-industrija"]),

 dict(key="iso22301", hr="iso-22301", en="iso-22301", icon="cycle",
      nEN="ISO 22301 - Business continuity", subEN="ISO 22301:2019",
      badgeHR="Business Continuity", badgeEN="Business continuity",
      leadEN="Business impact analysis, RTO and RPO definition, business continuity and disaster recovery plans, exercising and preparation for certification against ISO 22301:2019.",
      stepsEN=[("01","Business impact analysis","Impact over time by category, dependencies and minimum service level."),
               ("02","RTO and RPO","Recovery time and recovery point objectives, with justification per process."),
               ("03","Strategy","Recovery options and the resources each one requires."),
               ("04","Plans","Business continuity and disaster recovery plans, with activation criteria."),
               ("05","Exercising","Tabletop or full exercise, with measured recovery time."),
               ("06","Certification","Internal audit, management review and support through certification.")],
      delsEN=["BIA report","RTO and RPO per process","Continuity plan","Recovery plan","Exercise record","Certification readiness"],
      mjere=[3,12],
      clHR=["bia-koja-daje-upotrebljiv-rto","iso-27001-i-zks"],
      clEN=["bia-that-produces-a-usable-rto","iso-27001-and-the-cybersecurity-act"],
      sekt=["energetika","zdravstvo-i-farmacija","prehrambena-industrija","promet-i-logistika"]),

 dict(key="dora", hr="dora", en="dora", icon="bank",
      nEN="DORA - Digital operational resilience", subEN="Regulation (EU) 2022/2554",
      badgeHR="Financijski sektor", badgeEN="Financial sector",
      leadEN="Compliance with the EU DORA regulation for the financial sector - ICT risk management framework, third-party risk, resilience testing and regulatory reporting.",
      stepsEN=[("01","Gap assessment","Current state against the DORA requirements, by pillar."),
               ("02","ICT risk management framework","Governance, roles, risk methodology and reporting to the management body."),
               ("03","Register of information","Contractual arrangements with ICT providers, function criticality, subcontracting and processing locations."),
               ("04","Incident management","Classification, reporting and the register of ICT-related incidents."),
               ("05","Resilience testing","A testing programme proportionate to the entity's size and risk profile."),
               ("06","Exit strategies","Substitutability assessment and exit plans for critical providers.")],
      delsEN=["Gap assessment","ICT risk framework","Register of information","Incident procedure","Testing programme","Exit strategies"],
      mjere=[2,3,8,11,12],
      clHR=["dora-registar-informacija","registar-rizika-koji-prolazi-provjeru"],
      clEN=["dora-register-of-information","risk-register-that-passes-review"],
      sekt=["bankarstvo-i-financije","osiguranje"]),

 dict(key="vendor", hr="upravljanje-rizicima-treci-strana", en="vendor-risk-management", icon="chain",
      nEN="Vendor risk management", subEN="Supply chain security",
      badgeHR="Lanac opskrbe", badgeEN="Supply chain",
      leadEN="Third-party risk assessment, due diligence questionnaires, automated risk scoring, continuous monitoring and contractual security clauses across the supply chain.",
      stepsEN=[("01","Supplier inventory","One list reconciled across procurement, IT and finance, with the access each supplier holds."),
               ("02","Classification","Criticality derived from the function the supplier supports, not from the supplier's size."),
               ("03","Due diligence","Questionnaires proportionate to criticality, with evidence rather than assurances."),
               ("04","Contractual clauses","Security requirements, incident notification duties and audit rights."),
               ("05","Monitoring","Reassessment on a cycle and on change, recorded in the GRC platform.")],
      delsEN=["Supplier register","Criticality classification","Questionnaires and findings","Contract clauses","Monitoring plan"],
      mjere=[2,3,8],
      clHR=["dora-registar-informacija","registar-rizika-koji-prolazi-provjeru"],
      clEN=["dora-register-of-information","risk-register-that-passes-review"],
      sekt=["bankarstvo-i-financije","digitalna-infrastruktura-i-ikt","prehrambena-industrija"]),

 dict(key="audit", hr="sigurnosni-auditi-i-testiranje", en="security-audits-and-testing", icon="scan",
      nEN="Security audits and testing", subEN="Offensive security",
      badgeHR="Ofenzivna sigurnost", badgeEN="Offensive security",
      leadEN="Penetration testing, vulnerability assessment, configuration review, social engineering simulations and reports written for both technical and board-level audiences.",
      stepsEN=[("01","Scope and authorisation","Written authorisation, agreed scope, timing and rules of engagement."),
               ("02","External exposure","What is reachable from the internet, established independently of the IT inventory."),
               ("03","Penetration testing","Exploitation attempts within the agreed scope, with all activity logged."),
               ("04","Domain assessment","Relationships between objects - delegation, privileged membership, legacy protocols, backup access."),
               ("05","Social engineering","Phishing simulation where agreed, with results reported in aggregate, never per person."),
               ("06","Reporting","One report for the technical team with reproduction steps, one summary for the board.")],
      delsEN=["Technical report","Board summary","Ranked findings","Remediation plan","Retest"],
      mjere=[4,5,6,7],
      clHR=["active-directory-putovi-napada","prioritetne-preporuke-ncsc"],
      clEN=["active-directory-attack-paths","what-cyber-insurers-actually-ask"],
      sekt=["digitalna-infrastruktura-i-ikt","bankarstvo-i-financije","energetika"]),

 dict(key="revizije", hr="revizije-i-interne-provjere", en="audits-and-internal-reviews", icon="audit",
      nEN="Audits and internal reviews", subEN="Internal audit &middot; compliance review &middot; pre-audit review",
      badgeHR="Neovisna provjera", badgeEN="Independent review",
      leadEN="We carry out internal audits of management systems and compliance reviews, and we walk your documentation the way an external auditor or certification body will - before they arrive.",
      stepsEN=[("01","Internal audit of the management system","To ISO 19011, for ISMS, QMS, EMS and BCMS - audit programme, execution, findings and follow-up of corrective actions."),
               ("02","Compliance review against the Act","Scoring across the 13 measures and 99 sub-measures, against the control catalogue, with a list of missing evidence."),
               ("03","Data protection review","Records of processing, lawful bases, processor contracts, transfers outside the EU and data subject requests."),
               ("04","Pre-audit review","A simulation of the audit process, with a report of findings and priorities."),
               ("05","Corrective action tracking","Owner, deadline and closure evidence for every finding, in the GRC platform.")],
      delsEN=["Audit programme","Findings report","Corrective action plan","Evidence base","Management review"],
      mjere=[1,3,11],
      clHR=["kako-se-boduje-samoprocjena","registar-rizika-koji-prolazi-provjeru"],
      clEN=["how-self-assessment-is-scored","risk-register-that-passes-review"],
      sekt=["bankarstvo-i-financije","zdravstvo-i-farmacija","javna-uprava"]),

 dict(key="dpo", hr="eksterni-dpo", en="external-dpo", icon="dpo",
      nEN="External data protection officer", subEN="GDPR, Articles 37 to 39",
      badgeHR="GDPR čl. 37-39", badgeEN="GDPR Art. 37-39",
      leadEN="We take on the data protection officer function. An external DPO is expressly provided for by the GDPR and for most organisations is cheaper and more independent than an internal appointment. The role is held by a CIPP/E certified practitioner.",
      stepsEN=[("01","Monitoring compliance","Tracking application of the GDPR and internal rules, with regular reporting to the highest management level."),
               ("02","Advice","Opinions on impact assessments, new processing, processor contracts and transfers outside the EU."),
               ("03","Contact point","Towards the supervisory authority and data subjects, including access, rectification and erasure requests."),
               ("04","Personal data breaches","Risk assessment and notification to the supervisory authority within 72 hours, with notification to data subjects where required."),
               ("05","Training","Training for staff involved in processing, with records that can be produced.")],
      delsEN=["Appointed DPO and contact","Records of processing","Impact assessments","Register of data subject requests","Annual report to management"],
      mjere=[1,2,4,11],
      clHR=["rokovi-prijave-incidenta","registar-ai-sustava-i-registar-imovine"],
      clEN=["incident-reporting-deadlines","ai-inventory-and-asset-register"],
      sekt=["zdravstvo-i-farmacija","osiguranje","javna-uprava","bankarstvo-i-financije"]),

 dict(key="ciso", hr="eksterni-ciso", en="external-ciso", icon="ciso",
      nEN="External CISO", subEN="Leadership and oversight of the security programme",
      badgeHR="Vodstvo i nadzor", badgeEN="Leadership and oversight",
      leadEN="Measure 1 of Annex II requires a named responsible person who sets direction, reports to the board and secures resources. For most organisations a permanent hire at that level is not justified, and the obligation remains.",
      stepsEN=[("01","Strategy and policy","Setting direction, drafting the cyber security policy and having it adopted by the board."),
               ("02","Risk management","Maintaining the risk register, defining risk appetite and investment priorities."),
               ("03","Reporting to the board","Regular status, trend and open issues, in language the board understands."),
               ("04","Running the compliance programme","Tracking deadlines, owners and evidence for each measure, through to verification."),
               ("05","Incident response","Leadership during an incident and the decision on significance and notification to the competent CSIRT.")],
      delsEN=["Named responsible person","Policy and strategy","Risk register","Board reporting","Compliance roadmap"],
      mjere=[1,3,11],
      clHR=["trinaest-mjera-priloga-ii","nist-csf-2-funkcija-govern"],
      clEN=["thirteen-measures-annex-ii","nist-csf-2-govern-function"],
      sekt=["bankarstvo-i-financije","energetika","digitalna-infrastruktura-i-ikt"]),
]

USL_T = {
 "hr": dict(hub="/usluge/", name="Usluge",
   h1="Savjetodavne usluge",
   intro="Dvanaest usluga, jedna dokazna baza. Ondje gdje se zahtjevi preklapaju, dokumentacija se piše jednom.",
   desc="Savjetovanje u kibernetičkoj sigurnosti i usklađenosti: ZKS/NIS2, GDPR, DORA, ISO 27001, ISO 9001, ISO 14001, ISO 22301, revizije, eksterni DPO i CISO.",
   home="Početna",
   koraci="Kako radimo", isporuke="Što dobivate",
   mjere_h="Mjere iz Priloga II. koje ova usluga pokriva",
   sekt_h="Sektori u kojima je najtraženija", cl_h="Iz baze znanja",
   alati_h="Provjerite sami prije razgovora", svi="Sve usluge",
   otvori="Pogledajte uslugu", cijela="Pogledajte cijelu uslugu",
 ),
 "en": dict(hub="/en/services/", name="Services",
   h1="Advisory services",
   intro="Twelve services, one evidence base. Where the requirements overlap, the documentation is written once.",
   desc="Cyber security and compliance advisory: CSA/NIS2, GDPR, DORA, ISO 27001, ISO 9001, ISO 14001, ISO 22301, audits, external DPO and CISO.",
   home="Home",
   koraci="How we work", isporuke="What you get",
   mjere_h="Measures of Annex II this service covers",
   sekt_h="Sectors where it is most in demand", cl_h="From the knowledge base",
   alati_h="Check for yourself before we talk", svi="All services",
   otvori="View service", cijela="View the full service",
 ),
}

# ── Hrvatski sadrzaj usluga se cita iz modala u index.html ────────
def _ucitaj_modale():
    src = io.open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
    d = {}
    pat = re.compile(r'<div class="modal-overlay" id="modal-([a-z0-9]+)".*?'
                     r'<div class="modal-title">(.*?)</div>\s*'
                     r'<div class="modal-sub">(.*?)</div>\s*'
                     r'<div class="modal-lead">(.*?)</div>(.*?)\n</div>\n', re.S)
    for m in pat.finditer(src):
        key, title, sub, lead, rest = m.groups()
        steps = re.findall(r'<span class="modal-step-num">(\d+)</span><div><strong>(.*?)</strong>(.*?)</div>', rest, re.S)
        dels = re.findall(r'<span class="modal-del-tag">(.*?)</span>', rest)
        d[key] = dict(title=title.strip(), sub=sub.strip(),
                      lead=re.sub(r'\s+', ' ', lead).strip(),
                      steps=[(a, b.strip(), re.sub(r'\s+', ' ', c).strip()) for a, b, c in steps],
                      dels=[x.strip() for x in dels])
    return d

MODALI = _ucitaj_modale()

SVC_ICONS = dict(SVG)
SVC_ICONS["audit"] = '<path d="M9 11l2 2 4-4"/><path d="M21 12c0 5-3.6 7.4-8.1 8.9a2 2 0 0 1-1.3 0C7.1 19.4 3.5 17 3.5 12V6.3a1 1 0 0 1 .7-1l7.5-2.6a2 2 0 0 1 1.3 0l7.5 2.6a1 1 0 0 1 .7 1z"/>'
SVC_ICONS["dpo"] = '<path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/><path d="M17.5 3.5a3 3 0 0 1 0 5"/>'
SVC_ICONS["ciso"] = '<path d="M12 2l7 3v6c0 5-3 8.5-7 11-4-2.5-7-6-7-11V5z"/><path d="M12 8v4M12 15h.01"/>'


def build_services(lang, articles):
    t = L[lang]
    ut = USL_T[lang]
    st = SEK_T[lang]
    tools = TOOLS_T[lang]["hub"]
    FOOT = footer(lang, articles)
    out_dir = os.path.join(ROOT, "en", "services") if lang == "en" else os.path.join(ROOT, "usluge")
    os.makedirs(out_dir, exist_ok=True)
    arts = {a["slug"]: a for a in articles}
    sekt_ime = {x["hr"]: (x["nEN"] if lang == "en" else x["nHR"]) for x in SEKTORI}
    sekt_slug = {x["hr"]: (x["en"] if lang == "en" else x["hr"]) for x in SEKTORI}
    mj_ime = {m[0]: m[1] for m in (MJERE_EN if lang == "en" else MJERE)}

    def podaci(u):
        if lang == "hr":
            m = MODALI[u["key"]]
            return m["title"], m["sub"], m["lead"], m["steps"], m["dels"], u["badgeHR"]
        return u["nEN"], u["subEN"], u["leadEN"], u["stepsEN"], u["delsEN"], u["badgeEN"]

    def slug(u): return u["en"] if lang == "en" else u["hr"]

    # ── Hub ───────────────────────────────────────────────────────
    cards = []
    for u in USLUGE_META:
        nm, sub, lead, steps, dels, badge = podaci(u)
        kratko = lead if len(lead) < 165 else lead[:162].rsplit(" ", 1)[0] + "..."
        cards.append('''      <a class="sx-card" href="%s%s/">
        <div class="sx-top"><span class="sx-badge p1">%s</span></div>
        <div class="sx-name">%s</div>
        <div class="sx-note" style="text-transform:none;letter-spacing:0;font-size:13.5px">%s</div>
        <div class="sx-foot"><span>%d %s</span><span class="sx-go">%s &rarr;</span></div>
      </a>''' % (ut["hub"], slug(u), badge, nm, kratko, len(steps),
                 "koraka" if lang == "hr" else "steps", ut["otvori"]))

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
    <div class="sx-wrap"><div class="sx-grid">
%s
    </div></div>
  </div>
</main>
''' % (ut["name"], ut["h1"], ut["intro"], "\n".join(cards)) + FOOT

    io.open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8").write(
      page(ut["name"] + " | Adventure Spirit Consulting", ut["desc"], hub_body,
           SITE + ut["hub"], lang=lang,
           extra_head=hreflang(SITE + "/usluge/", SITE + "/en/services/")))

    # ── Stranice usluga ───────────────────────────────────────────
    for u in USLUGE_META:
        nm, sub, lead, steps, dels, badge = podaci(u)
        sl = slug(u)
        url = SITE + ut["hub"] + sl + "/"

        koraci = "\n".join('''      <div class="gap-item crit">
        <div class="gap-h"><span class="gap-n">%s</span><span class="gap-t">%s</span></div>
        <div class="gap-d">%s</div>
      </div>''' % (n, ttl, opis) for n, ttl, opis in steps)

        CHK = '<svg viewBox="0 0 24 24"><path d="M20 6 9 17l-5-5"/></svg>'
        isporuke = "\n".join('        <div class="deliver-item">%s<span>%s</span></div>' % (CHK, d)
                             for d in dels)

        mjere_chips = "\n".join(
          '        <span class="mj-chip"><b>%02d</b> %s</span>' % (n, mj_ime.get(n, ""))
          for n in u["mjere"])

        sekt_chips = "\n".join(
          '        <a class="chip-link" href="%s%s/">%s</a>' % (st["hub"], sekt_slug[k], sekt_ime[k])
          for k in u["sekt"] if k in sekt_ime)

        cl = u["clEN"] if lang == "en" else u["clHR"]
        rel = [arts[c] for c in cl if c in arts]
        clanci = "\n".join(card(a, lang) for a in rel)

        ostale = [x for x in USLUGE_META if x["key"] != u["key"]][:5]
        druge = "\n".join('<a class="chip-link" href="%s%s/">%s</a>'
                          % (ut["hub"], slug(x), podaci(x)[0]) for x in ostale)

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
      <div class="art-meta"><span><strong>%s</strong></span></div>
    </header>

    <article>
      <h2>%s</h2>
%s

      <h2>%s</h2>
      <div class="deliver-grid" style="margin-top:0">
%s
      </div>

      <h2>%s</h2>
      <div class="mj-row">
%s
      </div>

      <h2>%s</h2>
      <div class="chip-row">
%s
      </div>

      <h2>%s</h2>
      <div class="nf-nav" style="border:none;padding-top:0;margin-top:0">
        <a href="%s%s/">%s</a>
        <a href="%s%s/">%s</a>
        <a href="%s%s/">%s</a>
      </div>

      %s
    </article>

    <div class="related">
      <h3>%s</h3>
      <div class="related-grid">
%s
      </div>
    </div>

    <div class="related" style="margin-top:0;padding-top:32px">
      <h3>%s</h3>
      <div class="chip-row">
%s
        <a class="chip-link" href="%s">%s</a>
      </div>
    </div>
  </div>
</main>
''' % (t["base"] or "/", ut["home"], ut["hub"], ut["name"], nm,
       ut["name"], nm, lead, sub,
       ut["koraci"], koraci,
       ut["isporuke"], isporuke,
       ut["mjere_h"], mjere_chips,
       ut["sekt_h"], sekt_chips,
       ut["alati_h"],
       tools, CAT_T[lang]["slug"], CAT_T[lang]["name"],
       tools, SA_T[lang]["slug"], SA_T[lang]["name"],
       tools, TOOLS_T[lang]["slug"], TOOLS_T[lang]["t_name"],
       cta_block(lang),
       ut["cl_h"], clanci,
       ut["svi"], druge, ut["hub"], ut["svi"]) + FOOT

        ld = [{
          "@context": "https://schema.org", "@type": "Service",
          "name": nm, "description": lead[:300], "url": url,
          "serviceType": sub,
          "areaServed": {"@type": "Country", "name": "Hrvatska" if lang == "hr" else "Croatia"},
          "provider": {"@type": "Organization", "name": "Adventure Spirit Consulting",
                       "legalName": "Adventure Spirit d.o.o.", "url": SITE + "/"},
        }, {
          "@context": "https://schema.org", "@type": "BreadcrumbList",
          "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": ut["home"], "item": SITE + (t["base"] or "/")},
            {"@type": "ListItem", "position": 2, "name": ut["name"], "item": SITE + ut["hub"]},
            {"@type": "ListItem", "position": 3, "name": nm, "item": url}]}]

        d = os.path.join(out_dir, sl)
        os.makedirs(d, exist_ok=True)
        io.open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(
          page(nm + " | Adventure Spirit Consulting",
               (lead[:155] + "...") if len(lead) > 155 else lead, body, url, lang=lang,
               extra_head=hreflang(SITE + "/usluge/" + u["hr"] + "/",
                                   SITE + "/en/services/" + u["en"] + "/"), ld=ld))


# ══════════════════════════════════════════════════════════════════
# REFERENTNA STRANICA - 13 MJERA
# ══════════════════════════════════════════════════════════════════
# Sluzbeni ciljevi iz Priloga B ZSIS-a, skraceni na jednu recenicu gdje
# je izvornik predugacak. Broj podmjera prebrojan iz istog dokumenta.
MJ_REF = [
 (1, 11, "Osigurati da osobe odgovorne za upravljanje mjerama prepoznaju kibernetičku sigurnost kao ključni aspekt poslovanja i aktivno sudjeluju u njezinu upravljanju, kroz integraciju u strateške planove i odluke.",
     "Ensure that those responsible for managing the measures treat cyber security as a core aspect of the business and take an active part in managing it, through integration into strategic plans and decisions.",
     ["Odluka uprave o politici kibernetičke sigurnosti", "Imenovanje odgovornih osoba", "Osigurani financijski, tehnički i ljudski resursi", "Redovito izvještavanje uprave"],
     ["Board decision on the cyber security policy", "Appointment of responsible people", "Financial, technical and human resources secured", "Regular reporting to the board"],
     ["ciso", "revizije"]),
 (2, 9, "Uspostaviti strukturirani pristup identifikaciji i klasifikaciji programske i sklopovske imovine te potpunu kontrolu nad njom kroz cijeli životni ciklus, od korištenja i pohrane do brisanja ili uništavanja.",
     "Establish a structured approach to identifying and classifying software and hardware assets, and full control over them across the entire lifecycle, from use and storage through to deletion or destruction.",
     ["Inventar programske i sklopovske imovine", "Izdvojen inventar kritične imovine", "Klasifikacija podataka", "Pravila za uklanjanje i ponovnu upotrebu opreme"],
     ["Inventory of software and hardware assets", "Separate inventory of critical assets", "Data classification", "Rules for disposal and reuse of equipment"],
     ["zks", "iso27001", "vendor"]),
 (3, 8, "Uspostaviti organizacijski okvir za upravljanje rizikom kako bi subjekt utvrdio i odgovorio na sve rizike koji prijete sigurnosti njegovih mrežnih i informacijskih sustava.",
     "Establish an organisational framework for risk management so the entity identifies and responds to every risk threatening the security of its network and information systems.",
     ["Dokumentiran proces procjene rizika", "Procjena po načelu svih opasnosti", "Registar rizika s vlasnicima", "Plan obrade rizika"],
     ["Documented risk assessment process", "All-hazards assessment approach", "Risk register with owners", "Risk treatment plan"],
     ["zks", "iso27001", "ciso"]),
 (4, 12, "Uspostaviti strukturirani pristup upravljanju zapošljavanjem odgovarajućeg ljudskog potencijala te pravima pristupa zaposlenika i vanjskog osoblja mrežnim i informacijskim sustavima.",
     "Establish a structured approach to hiring suitable people and to managing the access rights of employees and external staff to network and information systems.",
     ["Provjere pri zapošljavanju", "Ugovorne obveze o povjerljivosti", "Upravljanje pravima kroz životni ciklus", "Odvojeni administratorski računi"],
     ["Pre-employment checks", "Contractual confidentiality duties", "Lifecycle management of access rights", "Separate administrator accounts"],
     ["zks", "audit", "dpo"]),
 (5, 11, "Za sve zaposlenike te mrežne i informacijske sustave osigurati provedbu osnovnih praksi kibernetičke higijene i redovito podizanje svijesti o kibernetičkim prijetnjama.",
     "Ensure basic cyber hygiene practices are applied across all staff and all network and information systems, with regular awareness raising about cyber threats.",
     ["Redovito zakrpavanje", "Sigurnosne kopije i testirano vraćanje", "Zaštita krajnjih točaka", "Edukacija zaposlenika uz evidenciju"],
     ["Regular patching", "Backups with tested restore", "Endpoint protection", "Staff training with records"],
     ["zks", "audit"]),
 (6, 5, "Osigurati cjelovitost, povjerljivost i dostupnost mrežnih resursa subjekta.",
     "Ensure the integrity, confidentiality and availability of the entity's network resources.",
     ["Segmentacija mreže", "Zaštita perimetra", "Nadzor mrežnog prometa", "Sigurna konfiguracija mrežne opreme"],
     ["Network segmentation", "Perimeter protection", "Network traffic monitoring", "Secure network device configuration"],
     ["zks", "audit"]),
 (7, 6, "Uspostaviti sveobuhvatan sustav politika i procedura za kontrolu fizičkog i logičkog pristupa mrežnim i informacijskim sustavima.",
     "Establish a comprehensive set of policies and procedures for controlling physical and logical access to network and information systems.",
     ["Načelo najmanje privilegije", "Višefaktorska autentifikacija", "Upravljanje povlaštenim pristupom", "Evidencija pristupa"],
     ["Least privilege", "Multi-factor authentication", "Privileged access management", "Access records"],
     ["zks", "audit", "iso27001"]),
 (8, 6, "Uspostaviti jasnu i sveobuhvatnu politiku za izravne dobavljače i pružatelje usluga, uz procjenu rizika koji iz tih odnosa proizlaze.",
     "Establish a clear and comprehensive policy for direct suppliers and service providers, with assessment of the risks arising from those relationships.",
     ["Minimalni sigurnosni zahtjevi za dobavljače", "Ugovorne sigurnosne klauzule", "Procjena rizika trećih strana", "Praćenje kroz vrijeme"],
     ["Minimum security requirements for suppliers", "Contractual security clauses", "Third-party risk assessment", "Monitoring over time"],
     ["vendor", "dora", "zks"]),
 (9, 6, "Osigurati da subjekt uspostavi, dokumentira i kontinuirano provodi sigurnosne zahtjeve u nabavi, razvoju i održavanju mrežnih i informacijskih sustava.",
     "Ensure the entity establishes, documents and continuously applies security requirements in the acquisition, development and maintenance of network and information systems.",
     ["Sigurnosni zahtjevi u razvoju", "Odvojena razvojna, testna i produkcijska okruženja", "Upravljanje promjenama", "Testiranje prije puštanja u rad"],
     ["Security requirements in development", "Separated development, test and production environments", "Change management", "Testing before go-live"],
     ["zks", "iso27001"]),
 (10, 6, "Uspostaviti sveobuhvatan okvir primjene kriptografije, sukladno vlastitim poslovnim potrebama i procijenjenom riziku.",
     "Establish a comprehensive framework for the use of cryptography, in line with business needs and assessed risk.",
     ["Pravila primjene kriptografije", "Zaštita podataka u prijenosu", "Zaštita podataka u mirovanju", "Upravljanje kriptografskim ključevima"],
     ["Rules on the use of cryptography", "Protection of data in transit", "Protection of data at rest", "Cryptographic key management"],
     ["zks", "gdpr", "iso27001"]),
 (11, 6, "Uspostaviti sveobuhvatan okvir za utvrđivanje uloga, odgovornosti i postupaka pri otkrivanju incidenata, odgovoru na njih i njihovoj prijavi.",
     "Establish a comprehensive framework defining roles, responsibilities and procedures for detecting, responding to and reporting incidents.",
     ["Kriterij značajnosti incidenta", "Plan odgovora na incident", "Prijava nadležnom CSIRT-u u rokovima", "Analiza nakon incidenta"],
     ["Incident significance criteria", "Incident response plan", "Notification to the competent CSIRT within deadlines", "Post-incident analysis"],
     ["zks", "ciso", "dpo"]),
 (12, 8, "Osigurati postojanje unaprijed pripremljenih planova za minimiziranje posljedica poremećaja i za oporavak poslovanja nakon incidenta ili krize.",
     "Ensure that plans exist in advance to minimise the consequences of disruption and to recover the business after an incident or crisis.",
     ["Analiza poslovnog utjecaja", "Planovi kontinuiteta i oporavka", "Upravljanje kibernetičkom krizom", "Redovito testiranje planova"],
     ["Business impact analysis", "Continuity and recovery plans", "Cyber crisis management", "Regular exercising of plans"],
     ["iso22301", "zks", "dora"]),
 (13, 5, "Uspostaviti mjere za sprječavanje i nadziranje neovlaštenog fizičkog pristupa prostorima u kojima se nalaze mrežni i informacijski sustavi te za njihovu zaštitu od okolišnih prijetnji.",
     "Establish measures to prevent and monitor unauthorised physical access to areas holding network and information systems, and to protect them from environmental threats.",
     ["Kontrola ulaska u prostore s opremom", "Zaštita od požara i vode", "Sigurnost napajanja i kabliranja", "Nadzor prostora"],
     ["Entry control to equipment areas", "Fire and water protection", "Power and cabling security", "Premises monitoring"],
     ["zks", "iso27001", "iso22301"]),
]

MJ_T = {
 "hr": dict(url="/mjere/", name="13 mjera",
   h1="Trinaest mjera upravljanja kibernetičkim sigurnosnim rizicima",
   intro="Uredba o kibernetičkoj sigurnosti (NN 135/2024) razrađuje obveze iz Zakona u trinaest mjera, raspisanih kroz 99 podmjera. Uz njih ZSIS je objavio katalog od 132 kontrole s bodovnim pragovima za tri razine provedbe. Ovo je pregled svih trinaest, s ciljem svake mjere i onim što u praksi traži.",
   desc="Pregled svih 13 mjera upravljanja kibernetičkim sigurnosnim rizicima iz Priloga II. Uredbe NN 135/2024, s ciljem svake mjere, brojem podmjera i onim što traži u praksi.",
   home="Početna", cilj="Cilj mjere", trazi="Što traži u praksi",
   pod="podmjera", usl="Usluge koje pokrivaju ovu mjeru",
   napomena="Nazivi mjera i ciljevi preuzeti su iz Priloga II. Uredbe odnosno iz Priloga B ZSIS-ovog okvira za evaluaciju. Broj podmjera prebrojan je iz istog dokumenta i zbraja se na 99. Katalog kontrola sadrži 132 jedinstvene oznake. Prije formalne samoprocjene provjerite koja je verzija okvira na snazi.",
   alat="Napravite mini samoprocjenu po svih 13 mjera",
   clanci="Detaljnije u bazi znanja",
   cl=["trinaest-mjera-priloga-ii","kako-se-boduje-samoprocjena","korelacijski-pregled-mjera"],
 ),
 "en": dict(url="/en/measures/", name="The 13 measures",
   h1="The thirteen cyber risk management measures",
   intro="The Croatian Cybersecurity Regulation (OG 135/2024) breaks the statutory duties into thirteen measures, set out across 99 sub-measures. Alongside them ZSIS published a catalogue of 132 controls with scoring thresholds for three levels of implementation. This is an overview of all thirteen, with the objective of each and what it asks for in practice.",
   desc="Overview of all 13 cyber risk management measures from Annex II of the Croatian Cybersecurity Regulation, with each measure's objective, sub-measure count and what it requires in practice.",
   home="Home", cilj="Objective", trazi="What it requires in practice",
   pod="sub-measures", usl="Services covering this measure",
   napomena="Measure names and objectives are taken from Annex II of the Regulation and from Annex B of the ZSIS evaluation framework. The sub-measure count was taken from the same document and totals 99. The control catalogue contains 132 unique identifiers. Check which version of the framework is current before a formal self-assessment.",
   alat="Run the readiness check against all 13 measures",
   clanci="More in the knowledge base",
   cl=["thirteen-measures-annex-ii","how-self-assessment-is-scored","iso-27001-and-the-cybersecurity-act"],
 ),
}


def build_measures(lang, articles):
    t = L[lang]
    mt = MJ_T[lang]
    ut = USL_T[lang]
    FOOT = footer(lang, articles)
    arts = {a["slug"]: a for a in articles}
    usl_ime = {}
    for u in USLUGE_META:
        if lang == "hr":
            usl_ime[u["key"]] = (MODALI[u["key"]]["title"], u["hr"])
        else:
            usl_ime[u["key"]] = (u["nEN"], u["en"])

    blokovi = []
    for br, pod, cHR, cEN, tHR, tEN, usl in MJ_REF:
        cilj = cEN if lang == "en" else cHR
        traz = tEN if lang == "en" else tHR
        stavke = "\n".join("          <li>%s</li>" % x for x in traz)
        uslchips = "\n".join('          <a class="chip-link" href="%s%s/">%s</a>'
                             % (ut["hub"], usl_ime[k][1], usl_ime[k][0]) for k in usl if k in usl_ime)
        blokovi.append('''      <div class="mjera" id="mjera-%d">
        <div class="mjera-h">
          <span class="mjera-n">%02d</span>
          <h2>%s</h2>
          <span class="mjera-pod">%d %s</span>
        </div>
        <p class="mjera-cilj"><b>%s</b> %s</p>
        <div class="mjera-body">
          <div>
            <div class="mjera-lbl">%s</div>
            <ul class="mjera-list">
%s
            </ul>
          </div>
          <div>
            <div class="mjera-lbl">%s</div>
            <div class="chip-row">
%s
            </div>
          </div>
        </div>
      </div>''' % (br, br, (MJERE_EN if lang == "en" else MJERE)[br-1][1], pod, mt["pod"],
                   mt["cilj"], cilj, mt["trazi"], stavke, mt["usl"], uslchips))

    nav = " ".join('<a href="#mjera-%d">%02d</a>' % (b[0], b[0]) for b in MJ_REF)
    rel = [arts[c] for c in mt["cl"] if c in arts]
    clanci = "\n".join(card(a, lang) for a in rel)
    url = SITE + mt["url"]

    body = header(lang, active_blog=False) + '''
<main>
  <section class="kb-hero">
    <div class="container">
      <div class="crumbs" style="padding:0 0 14px"><a href="%s">%s</a><span>&rsaquo;</span>%s</div>
      <div class="eyebrow">%s</div>
      <h1>%s</h1>
      <p>%s</p>
      <div class="mjera-nav">%s</div>
    </div>
  </section>
  <div class="container narrow">
    <div class="mjere-wrap">
%s
    </div>
    <div class="note" style="margin-bottom:30px"><p>%s</p></div>
    <div class="nf-nav" style="border:none;margin-top:0;padding-top:0">
      <a href="%s%s/">%s</a>
    </div>
    <div class="related">
      <h3>%s</h3>
      <div class="related-grid">
%s
      </div>
    </div>
    %s
  </div>
</main>
''' % (t["base"] or "/", mt["home"], mt["name"], mt["name"], mt["h1"], mt["intro"], nav,
       "\n".join(blokovi), mt["napomena"],
       TOOLS_T[lang]["hub"], SA_T[lang]["slug"], mt["alat"],
       mt["clanci"], clanci, cta_block(lang)) + FOOT

    ld = [{
      "@context": "https://schema.org", "@type": "ItemList",
      "name": mt["h1"], "description": mt["desc"], "url": url,
      "numberOfItems": 13,
      "itemListElement": [{"@type": "ListItem", "position": b[0],
                           "name": (MJERE_EN if lang == "en" else MJERE)[b[0]-1][1],
                           "url": url + "#mjera-%d" % b[0]} for b in MJ_REF],
    }, {
      "@context": "https://schema.org", "@type": "BreadcrumbList",
      "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": mt["home"], "item": SITE + (t["base"] or "/")},
        {"@type": "ListItem", "position": 2, "name": mt["name"], "item": url}]}]

    d = os.path.join(ROOT, "en", "measures") if lang == "en" else os.path.join(ROOT, "mjere")
    os.makedirs(d, exist_ok=True)
    io.open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(
      page(mt["h1"] + " | Adventure Spirit Consulting", mt["desc"], body, url, lang=lang,
           extra_head=hreflang(SITE + "/mjere/", SITE + "/en/measures/"), ld=ld))


# ══════════════════════════════════════════════════════════════════
# PREDAVANJA I NASTUPI
# ══════════════════════════════════════════════════════════════════
PRED_T = {
 "hr": dict(url="/predavanja/", name="Predavanja",
   h1="Predavanja, radionice i nastupi",
   intro="Predajem od 2017. i to je razlog zašto ova stranica postoji: objasniti propis nekome tko ga prvi put vidi teže je nego provesti ga. Radionice držim za upravu, informatiku i zaposlenike, a teme dolaze iz stvarnih projekata, ne iz prezentacija.",
   desc="Predavanja, radionice i konferencijski nastupi iz kibernetičke sigurnosti, ZKS-a, GDPR-a i upravljanja rizicima. Daniel Bara, predavač na RIT Croatia od 2017.",
   home="Početna",
   nast_h="Nastavno iskustvo", nast_p="Predajem na dodiplomskoj i diplomskoj razini, s naglaskom na spoju informacijskih sustava, upravljanja rizicima i vođenja projekata.",
   nastava=[("RIT Croatia", "od 2017.", "Information Systems and Technology, Strateški menadžment, Upravljanje projektima", True),
            ("Zagreb School of Economics and Management", "gostujuća predavanja", "Informacijska sigurnost i upravljanje rizicima", False),
            ("VERN", "gostujuća predavanja", "Kibernetička sigurnost i zaštita podataka", False),
            ("Libertas", "gostujuća predavanja", "Upravljanje informacijskim sustavima", False)],
   cred_h="Uz nastavu",
   cred=[("Doktorat iz Business Intelligencea", "Ekonomski fakultet u Osijeku"),
         ("MBA", "Zagreb School of Economics and Management"),
         ("PMP - Project Management Professional", "Project Management Institute"),
         ("CIPP/E - Certified Information Privacy Professional/Europe", "International Association of Privacy Professionals"),
         ("Aktivan član", "PMI Croatia"),
         ("Vanjski evaluator", "HAMAG-BICRO, više od 300 EU projekata")],
   tema_h="Teme za radionice i nastupe",
   tema_p="Svaka tema postoji i kao tekst u bazi znanja, pa možete unaprijed vidjeti pristup i razinu detalja. Trajanje i dubina prilagođavaju se publici - upravi, informatici ili svim zaposlenicima.",
   pub_h="Za koga",
   pub=[("Uprava i nadzorni odbor", "Što propis traži od vas osobno, koje odluke morate donijeti i što potpisujete. Bez tehničkog rječnika. Obično 60 do 90 minuta."),
        ("Informatika i sigurnost", "Mjere, podmjere, kontrole i dokazi. Kako se bodovi računaju i gdje se najčešće pada. Pola dana ili dan."),
        ("Svi zaposlenici", "Podizanje svijesti koje ne uči ljude da phishing prepoznaju po lošem hrvatskom. Kratko, konkretno, uz evidenciju koja zadovoljava mjeru 5."),
        ("Konferencije i stručni skupovi", "Nastupi na temu ZKS-a, DORA-e, umjetne inteligencije i upravljanja rizicima.")],
   cta_h="Trebate predavanje ili radionicu?",
   cta_p="Javite temu, publiku i okvirni termin. Odgovaramo u roku 24 sata i predlažemo program prilagođen razini polaznika.",
   cta_b="Dogovorite termin",
   napomena="Edukacija zaposlenika i podizanje svijesti dio su mjere 5 iz Priloga II. Uredbe, a osposobljenost za rad sa sustavima umjetne inteligencije traži članak 4. Akta o umjetnoj inteligenciji. U oba slučaja traži se evidencija - tko je, kada i što prošao.",
 ),
 "en": dict(url="/en/speaking/", name="Speaking",
   h1="Lectures, workshops and conference talks",
   intro="I have been teaching since 2017, and that is why this page exists: explaining a regulation to someone seeing it for the first time is harder than implementing it. Workshops are run for boards, for IT and for all staff, and the material comes from real projects rather than from slide decks.",
   desc="Lectures, workshops and conference talks on cyber security, the Croatian Cybersecurity Act, GDPR and risk management. Daniel Bara, lecturer at RIT Croatia since 2017.",
   home="Home",
   nast_h="Teaching experience", nast_p="I teach at undergraduate and graduate level, focused on where information systems, risk management and project delivery meet.",
   nastava=[("RIT Croatia", "since 2017", "Information Systems and Technology, Strategic Management, Project Management", True),
            ("Zagreb School of Economics and Management", "guest lectures", "Information security and risk management", False),
            ("VERN University", "guest lectures", "Cyber security and data protection", False),
            ("Libertas International University", "guest lectures", "Information systems management", False)],
   cred_h="Alongside teaching",
   cred=[("PhD in business intelligence", "Faculty of Economics, Osijek"),
         ("MBA", "Zagreb School of Economics and Management"),
         ("PMP - Project Management Professional", "Project Management Institute"),
         ("CIPP/E - Certified Information Privacy Professional/Europe", "International Association of Privacy Professionals"),
         ("Active member", "PMI Croatia"),
         ("External evaluator", "HAMAG-BICRO, more than 300 EU-funded projects")],
   tema_h="Topics for workshops and talks",
   tema_p="Every topic also exists as an article in the knowledge base, so you can see the approach and the level of detail in advance. Length and depth are adapted to the audience - board, IT, or all staff.",
   pub_h="Audiences",
   pub=[("Board and supervisory board", "What the rules require of you personally, which decisions you must take and what you are signing. No technical vocabulary. Usually 60 to 90 minutes."),
        ("IT and security", "Measures, sub-measures, controls and evidence. How the scoring works and where organisations most often fail. Half a day or a full day."),
        ("All staff", "Awareness training that does not teach people to spot phishing by its bad grammar. Short, concrete, with records that satisfy measure 5."),
        ("Conferences and professional events", "Talks on the Cybersecurity Act, DORA, artificial intelligence and risk management.")],
   cta_h="Need a lecture or a workshop?",
   cta_p="Tell us the topic, the audience and a rough date. We reply within 24 hours with a programme matched to the participants' level.",
   cta_b="Arrange a date",
   napomena="Staff training and awareness form part of measure 5 of Annex II of the Regulation, and AI literacy is required by Article 4 of the AI Act. Both require records - who completed what, and when.",
 ),
}


def build_speaking(lang, articles):
    t = L[lang]
    pt = PRED_T[lang]
    FOOT = footer(lang, articles)

    nastava = "\n".join('''      <div class="pred-item%s">
        <div class="pred-top"><span class="pred-org">%s</span><span class="pred-when">%s</span></div>
        <div class="pred-what">%s</div>
      </div>''' % (" main" if glavni else "", org, kada, sto)
      for org, kada, sto, glavni in pt["nastava"])

    cred = "\n".join('        <li><strong>%s</strong><span>%s</span></li>' % (a, b) for a, b in pt["cred"])

    # teme dolaze iz baze znanja, po jedna kartica po clanku
    izbor = articles[:9]
    teme = "\n".join(card(a, lang) for a in izbor)

    pub = "\n".join('''      <div class="gap-item crit">
        <div class="gap-h"><span class="gap-t">%s</span></div>
        <div class="gap-d" style="margin-left:0">%s</div>
      </div>''' % (kome, opis) for kome, opis in pt["pub"])

    url = SITE + pt["url"]
    body = header(lang, active_blog=False) + '''
<main>
  <section class="kb-hero">
    <div class="container">
      <div class="crumbs" style="padding:0 0 14px"><a href="%s">%s</a><span>&rsaquo;</span>%s</div>
      <div class="eyebrow">%s</div>
      <h1>%s</h1>
      <p>%s</p>
    </div>
  </section>
  <div class="container narrow">
    <article>
      <h2>%s</h2>
      <p>%s</p>
      <div class="pred-list">
%s
      </div>

      <h2>%s</h2>
      <ul class="cred-list">
%s
      </ul>

      <h2>%s</h2>
%s

      <h2>%s</h2>
      <p>%s</p>
    </article>

    <div class="related" style="margin-top:14px">
      <div class="related-grid">
%s
      </div>
    </div>

    <div class="note" style="margin-bottom:30px"><p>%s</p></div>

    <div class="art-cta">
      <h3>%s</h3>
      <p>%s</p>
      <div class="cta-btns">
        <a href="%s" class="btn-primary">%s</a>
        <a href="%s" class="btn-outline">%s</a>
      </div>
    </div>
  </div>
</main>
''' % (t["base"] or "/", pt["home"], pt["name"], pt["name"], pt["h1"], pt["intro"],
       pt["nast_h"], pt["nast_p"], nastava,
       pt["cred_h"], cred,
       pt["pub_h"], pub,
       pt["tema_h"], pt["tema_p"], teme, pt["napomena"],
       pt["cta_h"], pt["cta_p"],
       "/kontakt/" if lang == "hr" else "/en/contact/", pt["cta_b"],
       L[lang]["blog"], L[lang]["kb_title"]) + FOOT

    ld = [{
      "@context": "https://schema.org", "@type": "WebPage",
      "name": pt["h1"], "description": pt["desc"], "url": url,
      "inLanguage": "hr-HR" if lang == "hr" else "en-GB",
      "about": {"@type": "Person", "name": "Daniel Bara",
                "honorificSuffix": "dr. sc." if lang == "hr" else "PhD",
                "jobTitle": "Osnivač i glavni konzultant" if lang == "hr" else "Founder and Principal Consultant",
                "worksFor": {"@type": "Organization", "name": "Adventure Spirit Consulting"},
                "alumniOf": ["Ekonomski fakultet u Osijeku", "Zagreb School of Economics and Management"]},
    }, {
      "@context": "https://schema.org", "@type": "BreadcrumbList",
      "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": pt["home"], "item": SITE + (t["base"] or "/")},
        {"@type": "ListItem", "position": 2, "name": pt["name"], "item": url}]}]

    d = os.path.join(ROOT, "en", "speaking") if lang == "en" else os.path.join(ROOT, "predavanja")
    os.makedirs(d, exist_ok=True)
    io.open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(
      page(pt["h1"] + " | Adventure Spirit Consulting", pt["desc"], body, url, lang=lang,
           extra_head=hreflang(SITE + "/predavanja/", SITE + "/en/speaking/"), ld=ld))


# ══════════════════════════════════════════════════════════════════
# REFERENTNA STRANICA - PROPISI
# ══════════════════════════════════════════════════════════════════
PROPISI = [
 dict(k="zks", oznHR="NN 14/2024", oznEN="OG 14/2024",
   nHR="Zakon o kibernetičkoj sigurnosti", nEN="Cybersecurity Act",
   sHR="Štiti sustave", sEN="Protects systems",
   url="https://narodne-novine.nn.hr/clanci/sluzbeni/2024_02_14_254.html",
   traziHR=["Kategorizacija subjekta na ključne i važne", "13 mjera iz Priloga II. Uredbe, na propisanoj razini",
            "Prijava značajnog incidenta u 24, 72 sata i 30 dana", "Neovisna revizija ili samoprocjena",
            "Dostava podataka NCSC-u, uključujući IP raspone"],
   traziEN=["Categorisation into essential and important entities", "The 13 measures of Annex II at the prescribed level",
            "Significant incident notification within 24 h, 72 h and 30 days", "Independent audit or self-assessment",
            "Data delivery to NCSC-HR, including IP ranges"],
   kaznaHR="Do 10 mil. EUR ili 2 % svjetskog prometa (ključni)<br>Do 7 mil. EUR ili 1,4 % (važni)<br><b>Odgovorne osobe osobno: 500 do 6.000 EUR</b>",
   kaznaEN="Up to EUR 10m or 2 % of global turnover (essential)<br>Up to EUR 7m or 1.4 % (important)<br><b>Responsible individuals personally: EUR 500 to 6,000</b>",
   nadzorHR="SOA i sektorska tijela &middot; prijava incidenata NCSC-HR i Nacionalni CERT",
   nadzorEN="SOA and sectoral authorities &middot; incidents to NCSC-HR and the National CERT",
   clHR="kazne", clEN=None),

 dict(k="gdpr", oznHR="EU 2016/679", oznEN="EU 2016/679",
   nHR="Opća uredba o zaštiti podataka", nEN="General Data Protection Regulation",
   sHR="Štiti osobne podatke", sEN="Protects personal data",
   url="https://eur-lex.europa.eu/eli/reg/2016/679/oj/hrv",
   urlEN="https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng",
   traziHR=["Evidencija obrada i pravna osnova za svaku", "Procjena učinka gdje je rizik visok",
            "Ugovori s izvršiteljima i prijenosi izvan EU", "Zahtjevi ispitanika u propisanim rokovima",
            "Prijava povrede AZOP-u u 72 sata"],
   traziEN=["Records of processing and a lawful basis for each", "Impact assessment where risk is high",
            "Processor contracts and transfers outside the EU", "Data subject requests within statutory deadlines",
            "Breach notification to the authority within 72 hours"],
   kaznaHR="Do 20 mil. EUR ili 4 % svjetskog prometa,<br>ovisno o tome koji je iznos veći",
   kaznaEN="Up to EUR 20m or 4 % of global turnover,<br>whichever is higher",
   nadzorHR="Agencija za zaštitu osobnih podataka (AZOP)",
   nadzorEN="Croatian Personal Data Protection Agency (AZOP)",
   clHR=None, clEN=None),

 dict(k="ai", oznHR="EU 2024/1689", oznEN="EU 2024/1689",
   nHR="Akt o umjetnoj inteligenciji", nEN="AI Act",
   sHR="Uređuje automatizirano odlučivanje", sEN="Governs automated decision-making",
   url="https://eur-lex.europa.eu/eli/reg/2024/1689/oj/hrv",
   urlEN="https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng",
   traziHR=["Popis AI sustava po slučaju uporabe", "Klasifikacija u četiri razine rizika",
            "Zabranjene prakse se ne smiju primjenjivati", "Osposobljenost osoblja koje sustave koristi",
            "Obveze transparentnosti prema korisnicima"],
   traziEN=["Inventory of AI systems by use case", "Classification into four risk levels",
            "Prohibited practices must not be used", "AI literacy for staff operating the systems",
            "Transparency duties towards users"],
   kaznaHR="Do 35 mil. EUR ili 7 % svjetskog prometa<br>za zabranjene prakse; niži rasponi za ostale povrede",
   kaznaEN="Up to EUR 35m or 7 % of global turnover<br>for prohibited practices; lower ranges for other breaches",
   nadzorHR="Tijela određena nacionalnom provedbom",
   nadzorEN="Authorities designated by national implementation",
   clHR=None, clEN=None),

 dict(k="dora", oznHR="EU 2022/2554", oznEN="EU 2022/2554",
   nHR="DORA - digitalna operativna otpornost", nEN="DORA - digital operational resilience",
   sHR="Poseban režim za financijski sektor", sEN="A specific regime for financial services",
   url="https://eur-lex.europa.eu/eli/reg/2022/2554/oj/hrv",
   urlEN="https://eur-lex.europa.eu/eli/reg/2022/2554/oj/eng",
   traziHR=["Okvir upravljanja IKT rizikom", "Registar informacija o ugovorima s IKT pružateljima",
            "Prijava velikih IKT incidenata", "Program testiranja otpornosti",
            "Izlazne strategije za kritične pružatelje"],
   traziEN=["ICT risk management framework", "Register of information on ICT provider contracts",
            "Reporting of major ICT-related incidents", "Resilience testing programme",
            "Exit strategies for critical providers"],
   kaznaHR="Prema Zakonu o provedbi DORA-e (NN 136/2024)<br>i sektorskim propisima",
   kaznaEN="Under the Croatian DORA implementation act (OG 136/2024)<br>and sectoral legislation",
   nadzorHR="Hrvatska narodna banka i HANFA",
   nadzorEN="Croatian National Bank and HANFA",
   clHR=None, clEN=None),
]

PROP_T = {
 "hr": dict(url="/propisi/", name="Propisi",
   h1="Četiri propisa koja zajedno određuju kako štitite sustave i podatke",
   intro="U praksi se stalno preklapaju na istim mjestima: isti popis imovine, isti registar rizika, isti zapisi o incidentima. Ovdje su jedan pored drugoga - što svaki traži, tko ga nadzire i koliko košta neusklađenost.",
   desc="Pregled ZKS-a, Opće uredbe, Akta o umjetnoj inteligenciji i DORA-e: što svaki propis traži, tko nadzire provedbu i koje su kazne za neusklađenost.",
   home="Početna",
   trazi="Što traži", kazna="Kazne", nadzor="Nadzor", tekst="Puni tekst propisa",
   prekl_h="Gdje se preklapaju",
   prekl_p="Tri točke u kojima se sva četiri propisa oslanjaju na isti materijal. Organizacija koja ih vodi kao jedan izvor izvještava; ona koja ih vodi odvojeno prepisuje.",
   prekl=[("Popis imovine", "Registar informacijske imovine, registar AI sustava i DORA registar informacija tri su pogleda na istu imovinu. Jedan izvor, tri izvještaja."),
          ("Procjena rizika", "Sva četiri propisa traže dokumentiranu procjenu rizika s vlasnikom i planom obrade. Dvije metodologije znače dva registra koja se raziđu."),
          ("Prijava incidenta", "Rokovi i primatelji se razlikuju, ali zapis o incidentu je isti. Ako je zahvaćena i povreda osobnih podataka, dvije prijave teku usporedno.")],
   nap="Iznosi kazni navedeni su kao gornje granice iz propisa. Stvarna visina ovisi o okolnostima koje propis nabraja - ozbiljnosti i trajanju povrede, namjeri ili nepažnji, poduzetim mjerama i razini suradnje s nadležnim tijelom. Ovo je informativni pregled, ne pravni savjet.",
   dvostruko_h="Nećete biti kažnjeni dvaput za isto",
   dvostruko="Ako je za povrede osobnih podataka koje proizlaze iz istog postupanja AZOP već izrekao upravnu novčanu kaznu prema Općoj uredbi, u stručnom se nadzoru za to isto postupanje ne može podnijeti prijava ovlaštenom tužitelju ni izdati prekršajni nalog prema ZKS-u. Obveze ostaju odvojene, ali se za isto djelo ne kažnjava dvaput.",
   cl_h="Detaljnije u bazi znanja",
   cl=["zks-kazne-tko-placa-i-koliko","trinaest-mjera-priloga-ii","akt-o-umjetnoj-inteligenciji-razine-rizika"],
 ),
 "en": dict(url="/en/regulations/", name="Regulations",
   h1="Four instruments that together set how you protect systems and data",
   intro="In practice they keep overlapping at the same points: the same asset inventory, the same risk register, the same incident records. Here they are side by side - what each requires, who supervises it, and what non-compliance costs.",
   desc="Overview of the Croatian Cybersecurity Act, the GDPR, the AI Act and DORA: what each requires, who supervises enforcement, and the penalties for non-compliance.",
   home="Home",
   trazi="What it requires", kazna="Penalties", nadzor="Supervision", tekst="Full text",
   prekl_h="Where they overlap",
   prekl_p="Three points where all four rely on the same material. An organisation that keeps them as one source reports; one that keeps them apart transcribes.",
   prekl=[("Asset inventory", "The information asset register, the AI system inventory and the DORA register of information are three views of the same assets. One source, three reports."),
          ("Risk assessment", "All four require a documented risk assessment with an owner and a treatment plan. Two methodologies mean two registers that diverge."),
          ("Incident reporting", "Deadlines and recipients differ, but the incident record is the same. Where a personal data breach is involved, two notifications run in parallel.")],
   nap="The penalty figures are the upper limits set by each instrument. The actual amount depends on the circumstances each instrument lists - the seriousness and duration of the breach, intent or negligence, measures taken, and the level of cooperation with the authority. This is an informative overview, not legal advice.",
   dvostruko_h="You will not be penalised twice for the same conduct",
   dvostruko="Where the data protection authority has already imposed an administrative fine under the GDPR for a personal data breach arising from the same conduct, no misdemeanour charge or order may be issued under the Cybersecurity Act for that same conduct. The obligations remain separate, but the same act is not punished twice.",
   cl_h="More in the knowledge base",
   cl=["thirteen-measures-annex-ii","ai-act-risk-levels","incident-reporting-deadlines"],
 ),
}


def build_regulations(lang, articles):
    t = L[lang]
    pt = PROP_T[lang]
    FOOT = footer(lang, articles)
    arts = {a["slug"]: a for a in articles}
    url = SITE + pt["url"]

    kartice = []
    for p in PROPISI:
        nm = p["nEN"] if lang == "en" else p["nHR"]
        ozn = p["oznEN"] if lang == "en" else p["oznHR"]
        sub = p["sEN"] if lang == "en" else p["sHR"]
        traz = p["traziEN"] if lang == "en" else p["traziHR"]
        kazna = p["kaznaEN"] if lang == "en" else p["kaznaHR"]
        nadzor = p["nadzorEN"] if lang == "en" else p["nadzorHR"]
        link = p.get("urlEN") if (lang == "en" and p.get("urlEN")) else p["url"]
        stavke = "\n".join("            <li>%s</li>" % x for x in traz)
        kartice.append('''      <div class="prop">
        <div class="prop-h">
          <div>
            <span class="prop-ozn">%s</span>
            <h2>%s</h2>
            <div class="prop-sub">%s</div>
          </div>
        </div>
        <div class="prop-body">
          <div>
            <div class="mjera-lbl">%s</div>
            <ul class="mjera-list">
%s
            </ul>
          </div>
          <div>
            <div class="mjera-lbl">%s</div>
            <p class="prop-kazna">%s</p>
            <div class="mjera-lbl" style="margin-top:18px">%s</div>
            <p class="prop-nadzor">%s</p>
            <a class="chip-link" style="margin-top:14px;display:inline-block" href="%s" target="_blank" rel="noopener">%s &rarr;</a>
          </div>
        </div>
      </div>''' % (ozn, nm, sub, pt["trazi"], stavke, pt["kazna"], kazna,
                   pt["nadzor"], nadzor, link, pt["tekst"]))

    prekl = "\n".join('''      <div class="gap-item crit">
        <div class="gap-h"><span class="gap-t">%s</span></div>
        <div class="gap-d" style="margin-left:0">%s</div>
      </div>''' % (a, b) for a, b in pt["prekl"])

    rel = [arts[c] for c in pt["cl"] if c in arts]
    clanci = "\n".join(card(a, lang) for a in rel)

    body = header(lang, active_blog=False) + '''
<main>
  <section class="kb-hero">
    <div class="container">
      <div class="crumbs" style="padding:0 0 14px"><a href="%s">%s</a><span>&rsaquo;</span>%s</div>
      <div class="eyebrow">%s</div>
      <h1>%s</h1>
      <p>%s</p>
    </div>
  </section>
  <div class="container narrow">
    <div class="prop-wrap">
%s
    </div>

    <article style="padding-top:10px">
      <h2>%s</h2>
      <p>%s</p>
%s

      <div class="callout">
        <div class="c-label">%s</div>
        <p>%s</p>
      </div>

      <div class="note"><p>%s</p></div>
    </article>

    <div class="related">
      <h3>%s</h3>
      <div class="related-grid">
%s
      </div>
    </div>
    %s
  </div>
</main>
''' % (t["base"] or "/", pt["home"], pt["name"], pt["name"], pt["h1"], pt["intro"],
       "\n".join(kartice), pt["prekl_h"], pt["prekl_p"], prekl,
       pt["dvostruko_h"], pt["dvostruko"], pt["nap"],
       pt["cl_h"], clanci, cta_block(lang)) + FOOT

    ld = [{
      "@context": "https://schema.org", "@type": "WebPage",
      "name": pt["h1"], "description": pt["desc"], "url": url,
      "inLanguage": "hr-HR" if lang == "hr" else "en-GB",
      "publisher": {"@type": "Organization", "name": "Adventure Spirit Consulting",
                    "legalName": "Adventure Spirit d.o.o.", "url": SITE + "/"},
    }, {
      "@context": "https://schema.org", "@type": "BreadcrumbList",
      "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": pt["home"], "item": SITE + (t["base"] or "/")},
        {"@type": "ListItem", "position": 2, "name": pt["name"], "item": url}]}]

    d = os.path.join(ROOT, "en", "regulations") if lang == "en" else os.path.join(ROOT, "propisi")
    os.makedirs(d, exist_ok=True)
    io.open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(
      page(pt["h1"] + " | Adventure Spirit Consulting", pt["desc"], body, url, lang=lang,
           extra_head=hreflang(SITE + "/propisi/", SITE + "/en/regulations/"), ld=ld))


# ══════════════════════════════════════════════════════════════════
# KONTAKT STRANICA
# ══════════════════════════════════════════════════════════════════
KON_T = {
 "hr": dict(url="/kontakt/", name="Kontakt",
   h1="Stupite u kontakt",
   intro="Trebate procjenu usklađenosti, implementaciju ISO norme, pripremu za ZKS ili DORA-u, ili demo GRC platforme? Javite se. Odgovaramo u roku 24 sata radnim danom.",
   desc="Kontaktirajte Adventure Spirit Consulting - savjetovanje u kibernetičkoj sigurnosti, ZKS/NIS2, GDPR, DORA i ISO normama. Odgovaramo u roku 24 sata.",
   home="Početna",
   tel_l="Telefon", mail_l="E-pošta", portal_l="GRC Portal", sjed_l="Sjedište",
   forma_h="Pošaljite upit",
   f_ime="Ime i prezime *", f_mail="E-mail adresa *", f_tvrtka="Tvrtka ili organizacija",
   f_tel="Telefon", f_poruka="Kratki opis projekta ili upita",
   f_tema="Tema upita",
   teme=["ZKS / NIS2 usklađenost","GDPR i zaštita podataka","ISO 27001",
         "ISO 9001, 14001 ili 22301","DORA","Upravljanje rizicima trećih strana",
         "Sigurnosni audit ili penetracijski test","Revizija i interna provjera",
         "Eksterni DPO","Eksterni CISO","Predavanje ili radionica",
         "Demo GRC platforme","Nešto drugo"],
   f_salji="Pošaljite upit", f_saljem="Šaljem...",
   m_tema="Tema", m_tvrtka="Tvrtka", m_tel="Telefon", m_str="Stranica", m_por="Poruka",
   f_ok="Hvala. Javit ćemo se u roku 24 sata radnim danom.",
   f_err="Slanje nije uspjelo. Pišite nam izravno na info@adventurespirit.hr.",
   f_need="Upišite ime i ispravnu e-mail adresu.",
   privola="Slanjem upita pristajete da vaše podatke koristimo isključivo za odgovor na ovaj upit. Ne uvrštavamo vas na listu za obavijesti niti prosljeđujemo podatke trećim stranama. Više u <a href=\"/privatnost/\">politici privatnosti</a>.",
   prije_h="Prije razgovora možete provjeriti sami",
   prije_p="Tri alata rade u pregledniku, bez registracije. Ako ih prođete prije poziva, razgovor kreće od konkretnog stanja umjesto od nule.",
   sto_h="Kako izgleda prvi razgovor",
   sto=[("Pola sata, bez obveze", "Ništa vas ne obvezuje i ne šaljemo ponudu ako nema smisla."),
        ("Pitamo, ne prezentiramo", "Zanima nas što već imate, koja ste obavijest dobili i koji vam rok teče."),
        ("Na kraju znate što dalje", "Kažemo što bismo napravili prvo i koliko to otprilike traje, bez obzira radite li to s nama.")],
   pravni_h="Podaci o društvu",
 ),
 "en": dict(url="/en/contact/", name="Contact",
   h1="Get in touch",
   intro="Need a compliance assessment, an ISO implementation, preparation for the Croatian Cybersecurity Act or DORA, or a demo of the GRC platform? Write to us. We reply within 24 hours on working days.",
   desc="Contact Adventure Spirit Consulting - advisory in cyber security, CSA/NIS2, GDPR, DORA and ISO standards. We reply within 24 hours.",
   home="Home",
   tel_l="Phone", mail_l="Email", portal_l="GRC Portal", sjed_l="Registered office",
   forma_h="Send an enquiry",
   f_ime="Full name *", f_mail="Email address *", f_tvrtka="Company or organisation",
   f_tel="Phone", f_poruka="A short description of the project or question",
   f_tema="Subject",
   teme=["CSA / NIS2 compliance","GDPR and data protection","ISO 27001",
         "ISO 9001, 14001 or 22301","DORA","Vendor risk management",
         "Security audit or penetration test","Audit and internal review",
         "External DPO","External CISO","Lecture or workshop",
         "GRC platform demo","Something else"],
   f_salji="Send enquiry", f_saljem="Sending...",
   m_tema="Subject", m_tvrtka="Company", m_tel="Phone", m_str="Page", m_por="Message",
   f_ok="Thank you. We will reply within 24 hours on working days.",
   f_err="Sending failed. Please write to us directly at info@adventurespirit.hr.",
   f_need="Enter your name and a valid email address.",
   privola="By sending this enquiry you agree that we use your details solely to reply to it. You are not added to a notification list and your details are not passed to third parties. See the <a href=\"/en/privacy/\">privacy policy</a>.",
   prije_h="You can check for yourself before we talk",
   prije_p="Three tools run in your browser, with no sign-up. Running them before the call means the conversation starts from a concrete position rather than from nothing.",
   sto_h="What the first conversation looks like",
   sto=[("Half an hour, no obligation", "Nothing binds you, and we do not send a proposal if it makes no sense."),
        ("We ask rather than present", "We want to know what you already have, which notice you received and what deadline is running."),
        ("You leave knowing what comes next", "We say what we would do first and roughly how long it takes, whether or not you do it with us.")],
   pravni_h="Company details",
 ),
}


def build_contact(lang, articles):
    t = L[lang]
    k = KON_T[lang]
    tools = TOOLS_T[lang]["hub"]
    FOOT = footer(lang, articles)
    url = SITE + k["url"]

    IC = {
     "tel": '<svg viewBox="0 0 24 24"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.4 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/></svg>',
     "mail": '<svg viewBox="0 0 24 24"><path d="M4 4h16v16H4z"/><path d="M4 7l8 6 8-6"/></svg>',
     "web": '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15 15 0 0 1 0 20 15 15 0 0 1 0-20z"/></svg>',
     "pin": '<svg viewBox="0 0 24 24"><path d="M21 10c0 6-9 12-9 12s-9-6-9-12a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>',
    }
    kontakti = '''      <a class="kon-item" href="tel:+385955041496">
        <span class="kon-ic">%s</span>
        <span><b>%s</b>+385 95 504 1496</span>
      </a>
      <a class="kon-item" href="mailto:info@adventurespirit.hr">
        <span class="kon-ic">%s</span>
        <span><b>%s</b>info@adventurespirit.hr</span>
      </a>
      <a class="kon-item" href="https://app.adventurespirit.hr" target="_blank" rel="noopener">
        <span class="kon-ic">%s</span>
        <span><b>%s</b>app.adventurespirit.hr</span>
      </a>
      <div class="kon-item static">
        <span class="kon-ic">%s</span>
        <span><b>%s</b>Antuna Šoljana 22, 10000 Zagreb</span>
      </div>''' % (IC["tel"], k["tel_l"], IC["mail"], k["mail_l"],
                   IC["web"], k["portal_l"], IC["pin"], k["sjed_l"])

    opcije = "\n".join('          <option>%s</option>' % o for o in k["teme"])
    kako = "\n".join('''      <div class="gap-item crit">
        <div class="gap-h"><span class="gap-t">%s</span></div>
        <div class="gap-d" style="margin-left:0">%s</div>
      </div>''' % (a, b) for a, b in k["sto"])

    JS = '''<script>
(function () {
  var T = %s, g = function (i) { return document.getElementById(i); };
  var b = g("k-send"); if (!b) { return; }
  b.addEventListener("click", function () {
    var ime = g("k-ime").value.trim(), mail = g("k-mail").value.trim(), msg = g("k-msg");
    if (!ime || !/^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$/.test(mail)) {
      msg.textContent = T.need; msg.className = "nl-msg bad"; msg.hidden = false; return;
    }
    var lab = b.textContent; b.disabled = true; b.textContent = T.send; msg.hidden = true;
    var tel = g("k-tel").value.trim(), tvrtka = g("k-tvrtka").value.trim(), tema = g("k-tema").value;
    var redci = [T.m_tema + ": " + tema];
    if (tvrtka) { redci.push(T.m_tvrtka + ": " + tvrtka); }
    if (tel) { redci.push(T.m_tel + ": " + tel); }
    redci.push(T.m_str + ": " + location.href);
    fetch("https://formspree.io/f/__FS_UPITI__", {
      method: "POST", headers: { "Content-Type": "application/json", Accept: "application/json" },
      body: JSON.stringify({
        name: ime, email: mail, phone: tel || "-", company: tvrtka || "-",
        _subject: "[" + tema + "] " + ime + (tvrtka ? " (" + tvrtka + ")" : ""),
        message: redci.join("\\n") + "\\n\\n" + T.m_por + ":\\n" + g("k-poruka").value
      })
    }).then(function (r) {
      if (!r.ok) { throw new Error(); }
      msg.textContent = T.ok; msg.className = "nl-msg ok"; msg.hidden = false;
      ["k-ime", "k-mail", "k-tvrtka", "k-tel", "k-poruka"].forEach(function (i) { g(i).value = ""; });
      if (window.asTrack) { window.asTrack("contact_sent"); }
    }).catch(function () {
      msg.textContent = T.err; msg.className = "nl-msg bad"; msg.hidden = false;
    }).finally(function () { b.disabled = false; b.textContent = lab; });
  });
})();
</script>''' % json.dumps({"need": k["f_need"], "send": k["f_saljem"],
                          "ok": k["f_ok"], "err": k["f_err"],
                          "m_tema": k["m_tema"], "m_tvrtka": k["m_tvrtka"],
                          "m_tel": k["m_tel"], "m_str": k["m_str"],
                          "m_por": k["m_por"]}, ensure_ascii=False)

    body = header(lang, active_blog=False) + '''
<main>
  <section class="kb-hero">
    <div class="container">
      <div class="crumbs" style="padding:0 0 14px"><a href="%s">%s</a><span>&rsaquo;</span>%s</div>
      <div class="eyebrow">%s</div>
      <h1>%s</h1>
      <p>%s</p>
    </div>
  </section>

  <div class="container narrow">
    <div class="kon-grid">
%s
    </div>

    <div class="tool-panel" style="margin-top:0">
      <h2 style="font-size:19px;font-weight:800;color:var(--white);margin-bottom:20px">%s</h2>
      <div class="report-row">
        <label class="vh" for="k-ime">%s</label>
        <input type="text" id="k-ime" placeholder="%s" autocomplete="name">
        <label class="vh" for="k-mail">%s</label>
        <input type="email" id="k-mail" placeholder="%s" autocomplete="email">
      </div>
      <div class="report-row" style="margin-top:12px">
        <label class="vh" for="k-tvrtka">%s</label>
        <input type="text" id="k-tvrtka" placeholder="%s" autocomplete="organization">
        <label class="vh" for="k-tel">%s</label>
        <input type="text" id="k-tel" placeholder="%s" autocomplete="tel">
      </div>
      <div class="field" style="margin:16px 0 0">
        <label for="k-tema">%s</label>
        <select class="form-select-tool" id="k-tema">
%s
        </select>
      </div>
      <div class="field" style="margin:16px 0 0">
        <label class="vh" for="k-poruka">%s</label>
        <textarea class="kon-textarea" id="k-poruka" placeholder="%s"></textarea>
      </div>
      <div class="tool-actions" style="border:none;padding-top:6px">
        <button type="button" class="btn-primary" id="k-send">%s</button>
      </div>
      <p class="nl-msg" id="k-msg" hidden></p>
      <p class="report-legal">%s</p>
    </div>

    <article style="padding-top:44px">
      <h2>%s</h2>
%s

      <h2>%s</h2>
      <p>%s</p>
      <div class="nf-nav" style="border:none;padding-top:0;margin-top:0">
        <a href="%s%s/">%s</a>
        <a href="%s%s/">%s</a>
        <a href="%s%s/">%s</a>
      </div>

      <h2>%s</h2>
      <div class="auth-box">
        <div><span class="auth-k">Adventure Spirit d.o.o.</span>%s</div>
        <div><span class="auth-k">OIB / PDV ID</span>72169598754</div>
        <div><span class="auth-k">MBS</span>4845552</div>
      </div>
    </article>
  </div>
</main>
''' % (t["base"] or "/", k["home"], k["name"], k["name"], k["h1"], k["intro"],
       kontakti, k["forma_h"],
       k["f_ime"], k["f_ime"], k["f_mail"], k["f_mail"],
       k["f_tvrtka"], k["f_tvrtka"], k["f_tel"], k["f_tel"],
       k["f_tema"], opcije, k["f_poruka"], k["f_poruka"], k["f_salji"], k["privola"],
       k["sto_h"], kako,
       k["prije_h"], k["prije_p"],
       tools, CAT_T[lang]["slug"], CAT_T[lang]["name"],
       tools, SA_T[lang]["slug"], SA_T[lang]["name"],
       tools, TOOLS_T[lang]["slug"], TOOLS_T[lang]["t_name"],
       k["pravni_h"],
       ("Antuna Šoljana 22, 10000 Zagreb, Trgovački sud u Zagrebu" if lang == "hr"
        else "Antuna Šoljana 22, 10000 Zagreb, Commercial Court in Zagreb")) + FOOT + JS

    ld = [{
      "@context": "https://schema.org", "@type": "ContactPage",
      "name": k["h1"], "description": k["desc"], "url": url,
      "inLanguage": "hr-HR" if lang == "hr" else "en-GB",
      "mainEntity": {
        "@type": "Organization", "name": "Adventure Spirit Consulting",
        "legalName": "Adventure Spirit d.o.o.", "url": SITE + "/",
        "email": "info@adventurespirit.hr", "telephone": "+385 95 504 1496",
        "vatID": "HR72169598754",
        "address": {"@type": "PostalAddress", "streetAddress": "Antuna Šoljana 22",
                    "postalCode": "10000", "addressLocality": "Zagreb", "addressCountry": "HR"},
        "contactPoint": {"@type": "ContactPoint", "contactType": "sales",
                         "telephone": "+385 95 504 1496", "email": "info@adventurespirit.hr",
                         "availableLanguage": ["hr", "en"]},
      }}, {
      "@context": "https://schema.org", "@type": "BreadcrumbList",
      "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": k["home"], "item": SITE + (t["base"] or "/")},
        {"@type": "ListItem", "position": 2, "name": k["name"], "item": url}]}]

    d = os.path.join(ROOT, "en", "contact") if lang == "en" else os.path.join(ROOT, "kontakt")
    os.makedirs(d, exist_ok=True)
    io.open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(
      page(k["h1"] + " | Adventure Spirit Consulting", k["desc"], body, url, lang=lang,
           extra_head=hreflang(SITE + "/kontakt/", SITE + "/en/contact/"), ld=ld))


build_tools("hr", ARTICLES)
build_tools("en", ARTICLES_EN)
build_tool2("hr", ARTICLES)
build_tool2("en", ARTICLES_EN)
build_tool3("hr", ARTICLES)
build_tool3("en", ARTICLES_EN)
build_sectors("hr", ARTICLES)
build_sectors("en", ARTICLES_EN)
build_services("hr", ARTICLES)
build_services("en", ARTICLES_EN)
build_measures("hr", ARTICLES)
build_measures("en", ARTICLES_EN)
build_speaking("hr", ARTICLES)
build_speaking("en", ARTICLES_EN)
build_regulations("hr", ARTICLES)
build_regulations("en", ARTICLES_EN)
build_contact("hr", ARTICLES)
build_contact("en", ARTICLES_EN)


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

if 'asTrack' not in _s:
    _s = _s.replace("</body>", BEACON + "\n</body>", 1)

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
        (SITE + "/en/tools/" + TOOLS_T["en"]["slug"] + "/", "0.8", "monthly"),
        (SITE + "/alati/" + CAT_T["hr"]["slug"] + "/", "0.9", "monthly"),
        (SITE + "/en/tools/" + CAT_T["en"]["slug"] + "/", "0.8", "monthly"),
        (SITE + "/alati/" + SA_T["hr"]["slug"] + "/", "0.9", "monthly"),
        (SITE + "/en/tools/" + SA_T["en"]["slug"] + "/", "0.8", "monthly"),
        (SITE + "/sektori/", "0.9", "monthly"), (SITE + "/en/sectors/", "0.8", "monthly")]
urls += [(SITE + "/mjere/", "0.95", "monthly"), (SITE + "/en/measures/", "0.85", "monthly")]
urls += [(SITE + "/predavanja/", "0.8", "monthly"), (SITE + "/en/speaking/", "0.7", "monthly")]
urls += [(SITE + "/propisi/", "0.95", "monthly"), (SITE + "/en/regulations/", "0.85", "monthly")]
urls += [(SITE + "/usluge/", "0.95", "monthly"), (SITE + "/en/services/", "0.85", "monthly")]
urls += [(SITE + "/kontakt/", "0.9", "monthly"), (SITE + "/en/contact/", "0.8", "monthly")]
urls += [("%s/usluge/%s/" % (SITE, x["hr"]), "0.9", "monthly") for x in USLUGE_META]
urls += [("%s/en/services/%s/" % (SITE, x["en"]), "0.8", "monthly") for x in USLUGE_META]
urls += [("%s/sektori/%s/" % (SITE, x["hr"]), "0.8", "monthly") for x in SEKTORI]
urls += [("%s/en/sectors/%s/" % (SITE, x["en"]), "0.7", "monthly") for x in SEKTORI]
urls += [("%s/blog/%s/" % (SITE, a["slug"]), "0.8", "monthly") for a in ARTICLES]
urls += [("%s/en/blog/%s/" % (SITE, a["slug"]), "0.7", "monthly") for a in ARTICLES_EN]
urls += [(SITE + "/en/terms/", "0.3", "yearly"), (SITE + "/en/privacy/", "0.3", "yearly")]
urls += [(SITE + "/uvjeti/", "0.3", "yearly"), (SITE + "/privatnost/", "0.3", "yearly"),
         (SITE + "/mmew/", "0.5", "monthly"), (SITE + "/izleti/", "0.4", "monthly")]
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
