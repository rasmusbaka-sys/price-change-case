import pandas as pd
import os

def load_csv(path):
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    full_path = os.path.join(base_path, path)
    print("Loader fil fra:", full_path)

    # Prøv automatisk separator-detektion
    df = pd.read_csv(full_path, sep=None, engine="python", encoding="utf-8-sig")

    # Fjern BOM og whitespace
    df.columns = df.columns.str.strip().str.replace("\ufeff", "")

    return df
