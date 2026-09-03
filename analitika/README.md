# Analitika

Prvostrana analitika bez kolačića. Radi na cPanelu, treba samo PHP 7.0 ili noviji.

## Postavljanje nakon deploya

1. **Postavite lozinku.** Otvorite `https://adventurespirit.hr/analitika/` - pri prvom
   otvaranju stranica traži da postavite lozinku (najmanje 12 znakova). Nakon toga
   nitko bez nje ne može do ploče.

   Sprema se samo kriptografski sažetak, u `analitika/config.php`. Ta datoteka nije
   u gitu, ne šalje se deployem i blokirana je u `.htaccess`.

   **Napravite to odmah nakon prvog deploya** - dok lozinka nije postavljena, ploču
   može otvoriti svatko tko zna adresu i sam postaviti lozinku.

   Promjena lozinke: obrišite `analitika/config.php` preko cPanel File Managera i
   ponovno otvorite stranicu.

2. **Provjerite prava na mapu `analitika/`.** PHP mora imati pravo pisanja da bi mogao
   stvoriti `config.php` i mapu `podaci/`. Ako se pri postavljanju lozinke pojavi
   poruka o zapisivanju, postavite prava na 755.

3. **Otvorite `/analitika/`** i provjerite pojavljuju li se pregledi.

Zaštita preko cPanel Directory Privacy nije potrebna, ali je ne škodi dodati kao drugi sloj.

## Što se prikuplja

| Polje | Sadržaj |
|---|---|
| vrijeme | Datum i vrijeme u UTC-u |
| posjetitelj | Otisak iz dnevne tajne, IP adrese i preglednika, skraćen na 16 znakova |
| putanja | Putanja stranice, bez upitnih parametara |
| jezik | Verzija stranice i jezik preglednika |
| izvor | Domena s koje je posjetitelj došao, bez pune adrese |
| uredaj | desktop, tablet ili mobile, izvedeno iz širine prozora |
| dogadaj | Naziv događaja, prazno za obični pregled stranice |
| vrijednost | Brojčana vrijednost uz događaj, npr. postotak spremnosti |

**IP adresa se ne pohranjuje.** Koristi se samo pri izračunu otiska, a tajna se rotira
svaki dan u ponoć po UTC-u, pa se isti posjetitelj sutradan više ne može povezati s
današnjim posjetom. Zbog toga za ovu obradu nije potrebna privola za kolačiće.

Poštuju se zaglavlja `DNT: 1` i `Sec-GPC: 1` - u tom slučaju se ne zapisuje ništa.

## Događaji koji se prate

- `tool_deadlines` - izračun rokova prijave incidenta
- `tool_categorisation` - provjera kategorizacije
- `selfassessment_completed` - dovršena samoprocjena, uz postotak spremnosti
- `report_requested` - zatražen izvještaj na e-mail
- `portal_click` - odlazak na app.adventurespirit.hr

## Čuvanje podataka

Podaci se čuvaju u `podaci/YYYY-MM.csv`. Nema automatskog brisanja - stare datoteke
obrišite ručno prema roku iz vaše politike zadržavanja.
