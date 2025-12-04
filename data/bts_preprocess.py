import pandas as pd
import zipfile
from pathlib import Path


RAW_ZIP_FOLDER = Path("Raw/bts_on_time")
EXTRACTED_FOLDER = Path("extracted")
COLUMNS_FILE = Path("bts_columns_of_interest.txt")
PARQUET_OUTPUT = Path("bts_all.parquet")


def load_columns_of_interest(path: Path) -> list[str]:
    cols = []
    if path.exists():
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                cols.append(line)
    else:
        print(f"Warning: columns file not found at {path}. Loading all columns.")
        return []

    if "FL_DATE" not in cols:  # ensure date field present
        cols.append("FL_DATE")

    return cols


def extract_zip_files():
    EXTRACTED_FOLDER.mkdir(exist_ok=True, parents=True)

    for z in RAW_ZIP_FOLDER.glob("*.zip"):
        print(f"Processing zip: {z.name}")
        with zipfile.ZipFile(z, "r") as zf:
            for f in zf.namelist():
                if f.endswith(".csv"):
                    print(f"  Extracting {f}")
                    zf.extract(f, EXTRACTED_FOLDER)


def cleanup_extracted_csvs():
    """Delete extracted CSV files to save disk space."""
    csv_files = list(EXTRACTED_FOLDER.glob("*.csv"))
    if not csv_files:
        print("\nNo CSV files to clean up.")
        return

    print("\nCleaning up extracted CSV files...")
    for f in csv_files:
        print(f"  Deleting {f.name}")
        f.unlink()

    print("Cleanup complete.")


def preprocess_to_parquet():
    extract_zip_files()
    cols_of_interest = load_columns_of_interest(COLUMNS_FILE)

    if cols_of_interest:
        print(f"Using columns file:")
        for c in cols_of_interest: print(f"  - {c}")

        cols_set = set(cols_of_interest)
        def usecols(col): return col in cols_set
    else:
        print("No columns-of-interest file found. Loading ALL columns.")
        usecols = None

    # Load CSVs
    csv_files = list(EXTRACTED_FOLDER.glob("*.csv"))
    print(f"\nFound {len(csv_files)} CSV files. Loading...")

    dfs = []
    for f in csv_files:
        print(f"  Loading {f.name}")
        df = pd.read_csv(f, low_memory=False, usecols=usecols)
        dfs.append(df)

    df_all = pd.concat(dfs, ignore_index=True)

    # Convert FL_DATE to datetime
    if "FL_DATE" in df_all.columns:
        print("\nConverting FL_DATE to datetime...")
        df_all["FL_DATE"] = pd.to_datetime(
            df_all["FL_DATE"].astype(str),
            format="%Y%m%d",
            errors="coerce"
        )

    # Save as Parquet
    print(f"\nWriting Parquet to: {PARQUET_OUTPUT}")
    df_all.to_parquet(PARQUET_OUTPUT, compression="zstd")

    # Cleanup
    cleanup_extracted_csvs()
    print("\nDone.")


if __name__ == "__main__":
    preprocess_to_parquet()
