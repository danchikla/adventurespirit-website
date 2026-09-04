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

Google nudi nekoliko metoda. Najlakša za nas je **HTML tag**:

1. Odaberite metodu **HTML tag**
2. Google prikaže nešto poput
   `<meta name="google-site-verification" content="Abc123..." />`
3. **Pošaljite tu oznaku** - dodaje se u `index.html`, na pripremljeno mjesto
   iznad kanonske poveznice
4. Nakon deploya kliknite **Verify**

Alternativa bez čekanja: metoda **HTML file**. Google ponudi datoteku
`googleXXXX.html`; preuzmite je i stavite u korijen preko cPanel File
Managera, pa kliknite Verify. Datoteku poslije treba dodati i u repozitorij,
inače je sljedeći deploy obriše.

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
