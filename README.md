Multi-brand prisændringshåndtering (data/indkøb-fokus)

Formål
Denne løsning automatiserer håndteringen af prisændringer på tværs af flere brands.

Systemet:
1) Parser leverandørprislister (CSV)
2) Sammenligner mod eksisterende produktdata
3) Beregner prisændringer og margin-impact
4) Genererer reasoning pr. SKU
5) Foreslår auto-approve af små ændringer
6) Eksporterer både CSV- og Markdown-rapport
7) Udskriver farvekodet oversigt i terminalen
Løsningen er designet til at kunne køre som et batch-script uden UI.

Sådan køres løsningen:
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

Output
1) Farvekodet tabel i terminalen
2) output/price_report.csv
3) output/price_report.md

Arkitektur
Parser (parser.py)
1) Loader CSV-filer
2) Logger filstier
3) Sikrer ensartede datatyper
Logik (logic.py)
1) Sammenligner eksisterende og nye priser
2) Beregner:
      1. prisændring
      2. procentændring
      3. margin før/efter
      4. margin-impact (pp)
3) Genererer reasoning-tekst
4) Tilføjer farvekodet prisflag
   
Main pipeline (main.py)
1) Definerer marginregler pr. brand
2) Tvinger brand-kolonne ind i alle merges
3) Tilføjer margin-risiko
4) Tilføjer auto-approve
5) Samler alle brands i én DataFrame
6) Eksporterer CSV + Markdown

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
1) hvert brand er blot en CSV-fil
2) marginregler ligger i en dictionary
3) pipeline er brand-agnostisk
4) DataFrames concat’es dynamisk

For at tilføje et nyt brand:
1. Tilføj CSV i /data
2. Tilføj brand i brand_files
3. Tilføj marginregel i MARGIN_RULES
Ingen ændringer i logikken er nødvendige.

Hvad jeg ikke ville automatisere:
1. Store prisfald (>10%)
2. Produkter med negativ margin
3. Currency mismatch
4. Nye SKU’er der ikke findes i eksisterende data
   
Edgecases & robusthed
Løsningen håndterer:
1) Manglende kolonner
2) Merge-konflikter
3) Brand-kolonner der overskrives
4) Ugyldige talformater
5) Manglende værdier
Derudover er der indbygget:
1) tvungen brand-kolonne
2) fjernelse af brand_old / brand_new
3) debug-print af kolonner

Produktionsovervejelser
Hvis løsningen skulle i produktion:
1) Validering af inputfiler
2) Logging
3) Fejlhåndtering
4) Scheduling - eksempelvis “kør når leverandør uploader en fil” eller “hver gang der
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
1) cost_price
2) recommended_retail_price
3) marginregler
4) brandfiler
Og verificere:
1) margin_risk
2) auto_approve
3) reasoning
4) farvekoder
5) rapporter
