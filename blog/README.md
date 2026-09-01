# Baza znanja - kako dodati članak

Stranice u `/blog/` **generiraju se skriptom** `blog/_build.py`.
Ne uređujte `blog/index.html` ni `blog/<slug>/index.html` ručno - promjene će
biti prebrisane pri sljedećem pokretanju.

## Dodavanje novog članka

1. Otvorite `blog/_build.py` i u listu `ARTICLES` dodajte novi unos:

```python
ARTICLES.append(dict(
 slug="url-clanka",              # postaje /blog/url-clanka/
 cat="ZKS / NIS2",               # naziv teme, prikazuje se na kartici
 catkey="zks",                   # ključ za filtar (isti catkey = ista tema)
 date="2026-10-15",              # YYYY-MM-DD
 read=7,                         # procijenjeno vrijeme čitanja u minutama
 featured=False,                 # True = veliki istaknuti blok na vrhu popisa
 title="Naslov članka",
 lead="Uvodni odlomak, prikazuje se na kartici i ispod naslova.",
 desc="Meta opis za tražilice, do ~160 znakova.",
 body='''
<h2>Podnaslov</h2>
<p>Tekst.</p>
''',
 sources=[
   ('Naziv izvora', 'https://url-izvora'),
   ('Izvor bez poveznice', None),
 ]))
```

2. Pokrenite iz korijena repozitorija:

```
python3 blog/_build.py
```

3. Provjerite lokalno (`python3 -m http.server 8099`, pa
   `http://localhost:8099/blog/`) i commitajte.

Skripta pri svakom pokretanju regenerira: sve stranice članaka, popisnu
stranicu, `blog/feed.xml`, `sitemap.xml` i `robots.txt`.

## Elementi koje možete koristiti u `body`

- `<h2>`, `<h3>`, `<p>`, `<ul>`, `<ol>` - standardno
- `<div class="callout"><div class="c-label">Oznaka</div><p>Tekst</p></div>` - narančasti okvir
- `<div class="note"><p>Tekst</p></div>` - diskretna napomena
- `<div class="tbl-wrap"><table>...</table></div>` - tablica (obavezno u wrapperu zbog mobitela)
- `<td class="num">` - brojčana ćelija u narančastoj boji
- `__TABLICA__` - umeće generiranu tablicu svih 13 mjera

## Stil

Zajednički CSS je `blog/assets/blog.css` i uređuje se ručno.
Navigacija i podnožje definirani su u `_build.py` (funkcija `header()` i
konstanta `FOOTER`) - ako mijenjate izbornik na naslovnici, promijenite ga i ondje.
