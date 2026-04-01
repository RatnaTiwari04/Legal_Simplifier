import os
import re
import pandas as pd

DATASET_FOLDER = "dataset"

def clean_text(text):
    text = str(text).strip()
    text = re.sub(r"\s+", " ", text)
    return text

def load_single_csv(file_path):
    try:
        df = pd.read_csv(file_path, on_bad_lines="skip", encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, on_bad_lines="skip", encoding="latin1")

    df.columns = [str(col).strip().lower() for col in df.columns]

    if "input" not in df.columns or "output" not in df.columns:
        raise ValueError(
            f"{os.path.basename(file_path)} does not contain required columns: input, output"
        )

    df = df[["input", "output"]].copy()

    df["input"] = df["input"].apply(clean_text)
    df["output"] = df["output"].apply(clean_text)

    df = df[
        (df["input"] != "") &
        (df["output"] != "") &
        (df["input"].str.lower() != "nan") &
        (df["output"].str.lower() != "nan")
    ]

    df["source_file"] = os.path.basename(file_path)
    return df

def load_and_merge_datasets():
    if not os.path.exists(DATASET_FOLDER):
        raise FileNotFoundError(f"Dataset folder not found: {DATASET_FOLDER}")

    csv_files = sorted(
        [f for f in os.listdir(DATASET_FOLDER) if f.lower().endswith(".csv")]
    )

    if not csv_files:
        raise ValueError(f"No CSV files found inside '{DATASET_FOLDER}' folder.")

    all_dataframes = []

    print("\nLoading dataset files...\n")
    for file_name in csv_files:
        file_path = os.path.join(DATASET_FOLDER, file_name)
        try:
            df = load_single_csv(file_path)
            print(f"Loaded: {file_name} -> {df.shape[0]} valid rows")
            all_dataframes.append(df)
        except Exception as e:
            print(f"Skipped: {file_name} -> {e}")

    if not all_dataframes:
        raise ValueError("No valid CSV files with input/output columns could be loaded.")

    merged_df = pd.concat(all_dataframes, ignore_index=True)

    before_dedup = merged_df.shape[0]

    merged_df.drop_duplicates(subset=["input", "output"], inplace=True)

    same_rows = (merged_df["input"].str.lower() == merged_df["output"].str.lower()).sum()
    merged_df = merged_df[
        merged_df["input"].str.lower() != merged_df["output"].str.lower()
    ]

    merged_df = merged_df[
        (merged_df["input"].str.len() > 10) &
        (merged_df["output"].str.len() > 5)
    ]

    merged_df.reset_index(drop=True, inplace=True)

    after_clean = merged_df.shape[0]

    print("\nMerge summary:")
    print(f"Total rows before deduplication: {before_dedup}")
    print(f"Rows removed where input == output: {same_rows}")
    print(f"Final dataset shape after cleaning: {after_clean}")

    source_summary = merged_df["source_file"].value_counts()
    print("\nRows retained from each file:")
    for source, count in source_summary.items():
        print(f"{source}: {count}")

    return merged_df[["input", "output"]]

if __name__ == "__main__":
    df = load_and_merge_datasets()
    print("\nSample rows:")
    print(df.head(10).to_string(index=False))