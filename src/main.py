from parser import load_csv
from logic import compare_prices
import pandas as pd
import os

# Margin-regler pr. brand
MARGIN_RULES = {
    "BrandA": 0.40,  # 40%
    "BrandB": 0.30,  # 30%
    "BrandC": 0.25   # 25%
}

def generate_markdown_report(df, output_path="output/price_report.md"):
    lines = []

    # Header
    lines.append("# Prisændringsrapport")
    lines.append("")
    lines.append("Genereret: **i dag**")
    lines.append("")

    # Opsummering pr. brand
    lines.append("## Oversigt pr. brand")
    for brand in df["brand"].unique():
        subset = df[df["brand"] == brand]
        total = len(subset)
        changes = len(subset[subset["price_flag"] != "Uændret"])
        critical = len(subset[subset["margin_risk"] == "UNDER MINIMUM"])

        lines.append(f"### {brand}")
        lines.append(f"- Produkter i alt: **{total}**")
        lines.append(f"- Prisændringer: **{changes}**")
        lines.append(f"- Kritiske marginfald: **{critical}**")
        lines.append("")

    # Detaljeret tabel
    lines.append("## Detaljeret ændringsliste")
    lines.append("")
    lines.append("| SKU | Brand | Prisændring | % | Margin ændring (pp) | Risiko | Auto | Reasoning |")
    lines.append("|-----|--------|-------------|------|----------------------|---------|--------|-----------|")

    for _, row in df.iterrows():
        lines.append(
            f"| {row['sku']} "
            f"| {row['brand']} "
            f"| {row['price_change']} "
            f"| {row['percent_change']}% "
            f"| {row['margin_change_pp']} "
            f"| {row['margin_risk']} "
            f"| {row['auto_approve']} "
            f"| {row['reasoning']} |"
        )

    # Skriv filen
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Markdown-rapport gemt som: {output_path}")


def main():
    # Load existing products
    existing = load_csv("data/existing_products.csv")

    # Load all brand files
    brand_files = {
        "BrandA": "data/BrandA.csv",
        "BrandB": "data/BrandB.csv",
        "BrandC": "data/BrandC.csv"
    }

    results = []

    for brand_name, path in brand_files.items():
        new_prices = load_csv(path)

        # Tving brand-kolonnen ind i new_prices
        new_prices["brand"] = brand_name

        # Sammenlign
        merged = compare_prices(existing, new_prices)

        # Tving brand-kolonnen ind i merged (uanset merge-resultat)
        merged["brand"] = brand_name

        # Fjern evt. brand_old / brand_new fra merge
        for col in ["brand_old", "brand_new"]:
            if col in merged.columns:
                merged = merged.drop(columns=[col])

        # Margin-risiko baseret på brandets marginregel
        required_margin = MARGIN_RULES[brand_name]
        merged["margin_risk"] = merged["margin_new"].apply(
            lambda m: "OK" if m >= required_margin else "UNDER MINIMUM"
        )

        # Auto-approve logik
        merged["auto_approve"] = merged.apply(
            lambda row: (
                "AUTO-APPROVE"
                if (
                    row["price_flag"] == "Uændret"
                    or abs(row["percent_change"]) < 2
                    or row["margin_risk"] == "OK"
                )
                else "REVIEW"
            ),
            axis=1
        )

        results.append(merged)

    # Saml alle brands i én DataFrame
    final_df = pd.concat(results, ignore_index=True)

    # Debug: print kolonner
    print("Kolonner i final_df:", list(final_df.columns))

    # Udskriv farvekodet tabel i terminalen
    print(final_df[[
        "sku",
        "brand",
        "recommended_retail_price_old",
        "recommended_retail_price_new",
        "price_change",
        "percent_change",
        "margin_change_pp",
        "margin_risk",
        "auto_approve",
        "price_flag_colored"
    ]])

    # Gem ren CSV-rapport (uden farvekoder)
    output_path = "output/price_report.csv"
    final_df.to_csv(output_path, index=False, encoding="utf-8")
    print(f"CSV-rapport gemt som: {output_path}")

    # Gem Markdown-rapport
    generate_markdown_report(final_df)


if __name__ == "__main__":
    main()
