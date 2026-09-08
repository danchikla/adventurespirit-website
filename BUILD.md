# Kako se gradi stranica

Dio stranice je **generiran skriptom** `_build.py`. Pokreće se iz korijena repozitorija:

```
python3 _build.py
```

## Što je generirano, a što se uređuje ručno

| Datoteka / mapa | Kako se mijenja |
|---|---|
| `index.html` | **Ručno.** Hrvatska naslovnica, sav CSS i JS inline. |
| `blog/assets/blog.css` | **Ručno.** Stil bloga, 404 stranice i popisnih stranica. |
| `uvjeti/`, `privatnost/`, `mmew/`, `izleti/` | **Ručno.** |
| `en/index.html` | Generirano. Engleska naslovnica. |
| `blog/`, `en/blog/` | Generirano. Članci, popisne stranice, RSS. |
| `404.html`, `en/404.html` | Generirano. |
| `sitemap.xml`, `robots.txt` | Generirano. |

Skripta pri svakom pokretanju **preuzima `<style>` blok iz `index.html`** i ugrađuje ga
u englesku naslovnicu, pa promjena stila na hrvatskoj naslovnici automatski vrijedi i za englesku.
Skripta također u `index.html` dopisuje `hreflang` oznake i HR/EN preklopnik ako ih nema.

## Dodavanje novog članka

Članci žive u dvije liste u `_build.py`: `ARTICLES` (hrvatski) i `ARTICLES_EN` (engleski).
Ne moraju biti u paru - jezik može imati članak koji drugi nema.

```python
ARTICLES.append(dict(
 slug="url-clanka",              # postaje /blog/url-clanka/ odnosno /en/blog/...
 cat="ZKS / NIS2",               # naziv teme na kartici
 catkey="zks",                   # ključ za filtar; isti catkey = ista tema
 date="2026-10-15",              # YYYY-MM-DD
 read=7,                         # procijenjeno vrijeme čitanja
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

Nakon toga pokrenite `python3 _build.py`, provjerite lokalno
(`python3 -m http.server 8099`, pa `http://localhost:8099/blog/`) i commitajte.

## Elementi koje možete koristiti u `body`

- `<h2>`, `<h3>`, `<p>`, `<ul>`, `<ol>` - standardno
- `<div class="callout"><div class="c-label">Oznaka</div><p>Tekst</p></div>` - narančasti okvir
- `<div class="note"><p>Tekst</p></div>` - diskretna napomena
- `<div class="tbl-wrap"><table>...</table></div>` - tablica (obavezno u wrapperu zbog mobitela)
- `<td class="num">` - brojčana ćelija u narančastoj boji
- `__TABLICA__` - umeće generiranu tablicu svih 13 mjera ZKS-a

## Mijenjanje navigacije, podnožja i prijevoda sučelja

Sve tekstualne konstante sučelja su u rječniku `L` na vrhu `_build.py`, odvojeno po jeziku
(`L["hr"]`, `L["en"]`). Ondje se mijenjaju stavke izbornika, naslovi stupaca u podnožju,
tekst 404 stranice i poziv na akciju ispod članaka.

**Navigacija na `index.html` uređuje se ručno** i nije povezana s rječnikom `L` -
ako mijenjate izbornik, promijenite ga na oba mjesta.

## Sadržaj engleske naslovnice

Tekstovi engleske naslovnice su u konstantama `EN_LEGAL`, `EN_SECTORS`, `EN_SERVICES`,
`EN_DELIVERABLES`, `EN_PROCESS`, `EN_FAQ`, `EN_AUTHORITIES` i `EN_CLIENTS`, a raspored
u funkciji `en_index()`.

## Deploy

Push na `main` pokreće GitHub Actions koji FTPS-om šalje repozitorij na cPanel.
`_build.py` i `BUILD.md` su isključeni iz deploya i dodatno blokirani u `.htaccess`.
**Pokrenite `python3 _build.py` prije commita** ako ste mijenjali nešto što skripta generira.

## Formspree obrasci

Obrasci na stranici dijele se na tri Formspree odredišta, jer se razlikuju
po hitnosti i po djelatnosti:

| Oznaka | Što prima | Gdje se postavlja |
|---|---|---|
| `FS_UPITI` | prodajni upiti, traže odgovor u 24 sata | `_build.py` (konstanta) + `index.html` |
| `FS_OBAVIJESTI` | prijave na obavijesti, zahtjevi za izvještajem | `_build.py` (konstanta) + `index.html` |
| izleti | upiti za izlete, odvojena djelatnost | `izleti/index.html` |

U generatoru se ne piše ID izravno nego oznaka `__FS_UPITI__` odnosno
`__FS_OBAVIJESTI__`, koju `page()` zamijeni vrijednošću konstante pri
pisanju svake stranice. Za promjenu odredišta dovoljno je izmijeniti
konstantu na vrhu `_build.py`.

U `index.html` i `izleti/index.html` ID stoji izravno u kodu jer se te
datoteke ne generiraju. Svako mjesto ima komentar koje je odredište.

Dok se zasebni obrasci ne otvore, sva tri pokazuju na isti postojeći ID,
pa promjena ničega ne lomi.
