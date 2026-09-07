# Google Search Console - postavljanje

Sve na strani stranice je spremno. Ovo su koraci koje morate napraviti vi,
jer traže prijavu vašim Google računom.

## 1. Dodajte vlasništvo

Otvorite **search.google.com/search-console** i prijavite se.

Kliknite **Add property** i odaberite **URL prefix** (desna kutija), pa upišite:

```
https://adventurespirit.hr/
```

> Lijeva opcija, *Domain*, traži DNS zapis kod registrara domene. Ako imate
> pristup DNS-u, ona je bolja jer pokriva i `www` i podomene poput
> `izleti.adventurespirit.hr`. Ako nemate, uzmite *URL prefix*.

## 2. Potvrdite vlasništvo

### Napravljeno: metoda s HTML datotekom

Datoteka `googlecc366259b4bb184a.html` je u repozitoriju i nakon deploya
dostupna je na:

```
https://adventurespirit.hr/googlecc366259b4bb184a.html
```

U Search Consoleu kliknite **Verify**. To potvrđuje vlasništvo za *URL prefix*
vlasništvo `https://adventurespirit.hr/`.

**Datoteku nemojte brisati.** Google povremeno ponovno provjerava vlasništvo i
ako datoteka nestane, vlasništvo se gubi.

### Preporučeno uz to: Domain vlasništvo preko DNS-a

Budući da imate pristup DNS-u kod registrara, dodajte i **Domain** vlasništvo.
Ono je šire i pokriva sve odjednom:

| Pokriva | URL prefix | Domain |
|---|---|---|
| `https://adventurespirit.hr` | da | da |
| `https://www.adventurespirit.hr` | ne | da |
| `http://` verzije | ne | da |
| `izleti.adventurespirit.hr` | ne | da |
| `app.adventurespirit.hr` | ne | da |

Vama to konkretno znači da u jednom izvještaju vidite i GRC stranicu i
planinarski dio i portal.

**Koraci:**

1. U Search Consoleu **Add property**, ovaj put lijeva kutija **Domain**
2. Upišite `adventurespirit.hr` (bez `https://` i bez `www`)
3. Google prikaže TXT zapis, oblika:
   ```
   google-site-verification=nekiNasumicniNiz
   ```
4. Kod registrara domene dodajte TXT zapis:

   | Polje | Vrijednost |
   |---|---|
   | Tip | `TXT` |
   | Naziv / Host | `@` (ili prazno, ovisno o sučelju - označava samu domenu) |
   | Vrijednost | cijeli niz koji je Google dao, s `google-site-verification=` na početku |
   | TTL | ostavite zadano, obično 3600 |

5. Pričekajte da se zapis proširi. Obično 15 minuta do sat vremena, iznimno do 24 sata.
6. Kliknite **Verify**

**Važno:** TXT zapis ne brišite ni nakon potvrde, iz istog razloga kao i datoteku.

Ako imate više TXT zapisa na `@` (npr. SPF za e-poštu), to nije problem -
domena može imati više TXT zapisa istovremeno. Nemojte zamijeniti postojeći,
nego dodajte novi.

**Provjera da je zapis vidljiv**, prije nego kliknete Verify, u Terminalu:

```
dig +short TXT adventurespirit.hr
```

Trebate vidjeti svoj `google-site-verification=...` među rezultatima.

## 3. Pošaljite sitemap

U izborniku lijevo **Sitemaps**, u polje upišite:

```
sitemap.xml
```

i kliknite **Submit**. Sitemap ima 111 adresa i sadrži obje jezične verzije.

## 4. Zatražite indeksiranje najvažnijih stranica

Indeksiranje cijelog sitemapa traje tjednima. Za stranice koje najviše
nose, koristite **URL Inspection** (polje na vrhu) pa **Request indexing**.
Redoslijed prema vrijednosti:

1. `https://adventurespirit.hr/`
2. `https://adventurespirit.hr/mjere/`
3. `https://adventurespirit.hr/propisi/`
4. `https://adventurespirit.hr/usluge/`
5. `https://adventurespirit.hr/alati/samoprocjena-13-mjera/`
6. `https://adventurespirit.hr/blog/zks-kazne-tko-placa-i-koliko/`
7. `https://adventurespirit.hr/blog/trinaest-mjera-priloga-ii/`

Dnevna kvota je ograničena, pa ostalo prepustite sitemapu.

## 5. Što gledati poslije

Prvi korisni podaci stižu nakon 3 do 7 dana.

| Gdje | Što gledati |
|---|---|
| **Pages** | Koliko je indeksirano, i razlozi za neindeksirane |
| **Performance** | Po kojim upitima se pojavljujete i koji donose klikove |
| **Sitemaps** | Je li sitemap procitan bez grešaka |

Ako se pod *Pages* pojavi puno stranica s razlogom
*Duplicate without user-selected canonical*, javite - to bi značilo problem
s kanonskim poveznicama koji treba popraviti.

## Provjereno prije slanja

- Sitemap: 111 adresa, bez duplikata, sve datoteke postoje
- Kanonska poveznica na svakoj stranici osim dijagnostičke, koja je `noindex`
- `hreflang` obostran na svih 62 dvojezične stranice - Google ga inace ignorira
- `noindex` samo ondje gdje treba: 404 stranice, dijagnostika i stara
  adresa MMEW-a koja preusmjerava na `/mmew/`
- `robots.txt` upućuje na sitemap

## Bing

Isti sitemap vrijedi i za **bing.com/webmasters**. Bing dopušta uvoz
vlasništva izravno iz Search Consolea, pa je to poslije stvar dvije minute.
