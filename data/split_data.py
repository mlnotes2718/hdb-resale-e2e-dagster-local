#!/usr/bin/env python3
import argparse
from pathlib import Path

import pandas as pd


def split_csv() -> None:
    input_path = Path("ResaleflatpricesbasedonregistrationdatefromJan2017onwards.csv").expanduser().resolve()
    output_dir = Path("./split").expanduser()
    output_dir.mkdir(parents=True, exist_ok=True)

    first_path = output_dir / "ResaleflatpricesbasedonregistrationdatefromJan2017onwards_part1_200k.csv"
    second_path = output_dir / "ResaleflatpricesbasedonregistrationdatefromJan2017onwards_part2_10k.csv"
    third_path = output_dir / "ResaleflatpricesbasedonregistrationdatefromJan2017onwards_part3_10k.csv"
    fourth_path = output_dir / "ResaleflatpricesbasedonregistrationdatefromJan2017onwards_part4_remaining.csv"

    df = pd.read_csv(input_path)
    if df.empty:
        raise ValueError("Input CSV is empty")

    if "id" in df.columns:
        df = df.set_index("id")
    else:
        df.index = pd.RangeIndex(start=1, stop=len(df) + 1, step=1)
        df.index.name = "id"

    first_df = df.iloc[:200_000]
    second_df = df.iloc[200_000:210_000]
    third_df = df.iloc[210_000:220_000]
    fourth_df = df.iloc[220_000:]

    first_df.to_csv(first_path, index=True, index_label="id")
    second_df.to_csv(second_path, index=True, index_label="id")
    third_df.to_csv(third_path, index=True, index_label="id")
    fourth_df.to_csv(fourth_path, index=True, index_label="id")

    total_rows = len(df)
    print("Split complete:")
    print(f"  1) {first_path} ({len(first_df)} rows)")
    print(f"  2) {second_path} ({len(second_df)} rows)")
    print(f"  3) {third_path} ({len(third_df)} rows)")
    print(f"  4) {fourth_path} ({len(fourth_df)} rows)")
    print(f"Total rows processed (excluding header): {total_rows}")


if __name__ == "__main__":
    split_csv()
