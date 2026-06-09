README.md
Multi-brand prisændringshåndtering (data/indkøb-fokus)
Formål
Denne løsning automatiserer håndteringen af prisændringer på tværs af flere brands.
Systemet:
● Parser leverandørprislister (CSV)
● Sammenligner mod eksisterende produktdata
● Beregner prisændringer og margin-impact
● Genererer reasoning pr. SKU
● Foreslår auto-approve af små ændringer
● Eksporterer både CSV- og Markdown-rapport
● Udskriver farvekodet oversigt i terminalen
Løsningen er designet til at kunne køre som et batch-script uden UI.

Sådan køres løsningen
1) Installer afhængigheder
pip install pandas
2) Projektstruktur
/data
existing_products.csv
BrandA.csv
BrandB.csv
BrandC.csv
/src
main.py
logic.py
parser.py
/output
price_report.csv
price_report.md
3) Kør scriptet
python src/main.py

Output:
● Farvekodet tabel i terminalen
● output/price_report.csv
● output/price_report.md

Arkitektur
Parser (parser.py)
● Loader CSV-filer
● Logger filstier
● Sikrer ensartede datatyper
Logik (logic.py)
● Sammenligner eksisterende og nye priser
● Beregner:
o prisændring
o procentændring
o margin før/efter
o margin-impact (pp)
● Genererer reasoning-tekst
● Tilføjer farvekodet prisflag
Main pipeline (main.py)
● Definerer marginregler pr. brand
● Tvinger brand-kolonne ind i alle merges
● Tilføjer margin-risiko
● Tilføjer auto-approve
● Samler alle brands i én DataFrame
● Eksporterer CSV + Markdown
Auto-approve logik
Et produkt auto-approves hvis:
1. Pris er uændret eller
2. Prisændring er < 2% eller
3. Margin stadig er ≥ brandets minimum
Ellers markeres det som REVIEW.
Reasoning-eksempler
Systemet genererer en menneskelig forklaring pr. SKU:
“Pris steg med 10.1%. Margin ændrede sig fra 42.0% til 35.0% (-7.0 pp). Margin
under minimum for brand.”
Dette gør rapporten brugbar for indkøb og stakeholders.
Skalering til flere brands
Løsningen skalerer naturligt fordi:
● hvert brand er blot en CSV-fil
● marginregler ligger i en dictionary
● pipeline er brand-agnostisk
● DataFrames concat’es dynamisk
For at tilføje et nyt brand:
1. Tilføj CSV i /data
2. Tilføj brand i brand_files
3. Tilføj marginregel i MARGIN_RULES
Ingen ændringer i logikken er nødvendige.
Hvad jeg ikke ville automatisere
1. Store prisfald (>10%)
2. Produkter med negativ margin
3. Currency mismatch
4. Nye SKU’er der ikke findes i eksisterende data
Edgecases & robusthed
Løsningen håndterer:
● Manglende kolonner
● Merge-konflikter
● Brand-kolonner der overskrives
● Ugyldige talformater
● Manglende værdier
Derudover er der indbygget:
● tvungen brand-kolonne
● fjernelse af brand_old / brand_new
● debug-print af kolonner
Produktionsovervejelser
Hvis løsningen skulle i produktion:
● Validering af inputfiler
● Logging
● Fejlhåndtering
● Scheduling - eksempelvis “kør når leverandør uploader en fil” eller “hver gang der
kommer en ny prisfil”

Output
CSV
output/price_report.csv
Markdown
output/price_report.md
Terminal
Farvekodet tabel for hurtig visning

Test
Du kan teste funktionalitet ved at ændre:
● cost_price
● recommended_retail_price
● marginregler
● brandfiler
Og verificere:
● margin_risk
● auto_approve
● reasoning
● farvekoder
● rapporter
