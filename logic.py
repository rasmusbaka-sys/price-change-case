def compare_prices(existing_df, new_df):
    # Merge existing + new data
    merged = existing_df.merge(new_df, on="sku", suffixes=("_old", "_new"))

    # Absolut prisændring
    merged["price_change"] = (
        merged["recommended_retail_price_new"] - merged["recommended_retail_price_old"]
    )

    # Procentændring
    merged["percent_change"] = (
        merged["price_change"] / merged["recommended_retail_price_old"] * 100
    ).round(2)

    # Prisflag
    def price_flag(row):
        if row["price_change"] > 0:
            return "Stigning"
        elif row["price_change"] < 0:
            return "Fald"
        else:
            return "Uændret"

    merged["price_flag"] = merged.apply(price_flag, axis=1)

    # Margin før
    merged["margin_old"] = (
        (merged["recommended_retail_price_old"] - merged["cost_price_old"])
        / merged["recommended_retail_price_old"]
    ).round(3)

    # Margin efter
    merged["margin_new"] = (
        (merged["recommended_retail_price_new"] - merged["cost_price_new"])
        / merged["recommended_retail_price_new"]
    ).round(3)

    # Margin impact (procentpoint)
    merged["margin_change_pp"] = (
        (merged["margin_new"] - merged["margin_old"]) * 100
    ).round(2)

    # Reasoning-tekst
    def reasoning(row):
        # Prisændring
        if row["price_change"] > 0:
            change_text = f"Pris steg med {row['percent_change']}%."
        elif row["price_change"] < 0:
            change_text = f"Pris faldt med {abs(row['percent_change'])}%."
        else:
            change_text = "Pris uændret."

        # Marginændring
        margin_text = (
            f"Margin ændrede sig fra {row['margin_old']*100:.1f}% "
            f"til {row['margin_new']*100:.1f}% "
            f"({row['margin_change_pp']} pp)."
        )

        # Risiko (tilføjes i main.py)
        risk = row.get("margin_risk", "N/A")
        if risk == "UNDER MINIMUM":
            risk_text = "⚠️ Margin under minimum for brand."
        else:
            risk_text = "Margin OK."

        return f"{change_text} {margin_text} {risk_text}"

    merged["reasoning"] = merged.apply(reasoning, axis=1)

    # Farvekoder til terminalen
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    RESET = "\033[0m"

    def colorize(row):
        if row["price_flag"] == "Stigning":
            return f"{RED}{row['price_flag']}{RESET}"
        elif row["price_flag"] == "Fald":
            return f"{GREEN}{row['price_flag']}{RESET}"
        else:
            return f"{YELLOW}{row['price_flag']}{RESET}"

    merged["price_flag_colored"] = merged.apply(colorize, axis=1)

    return merged
