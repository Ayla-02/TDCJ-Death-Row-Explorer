"""
Texas Department of Criminal Justice: Death Row Execution Records (1982–2024)
Data source: https://www.tdcj.texas.gov/death_row/dr_executed_offenders.html

Menu-driven CLI tool for exploring TDCJ execution records loaded from an SPSS (.sav) file - Developed as an introductory assignment for the Computer Science and Software Engineering course at the University of Abertay, Dundee "Fundamentals of Computing" 2024.
The dataset includes fields for last name, first name, TDCJ number, age at execution, and year of execution. Users can view individual records by execution number, see summary statistics (total executions, year range, median and mode age), and search for records by name. 
The tool handles file loading errors and validates user input for a smooth experience.
"""

import sys
import pandas as pd
import pyreadstat


COLUMNS = ["last_name", "first_name", "TDCJ", "age", "year"]

TITLE = "Texas Department of Criminal Justice: Death Row Execution Records (1982–2024)"
SOURCE_URL = "https://www.tdcj.texas.gov/death_row/dr_executed_offenders.html"


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_dataset(file_path: str) -> pd.DataFrame:
    """Load and return the relevant columns from an SPSS .sav file."""
    try:
        df, _ = pyreadstat.read_sav(file_path)
    except FileNotFoundError:
        print(f"Error: File not found — '{file_path}'. Check the path and try again.")
        sys.exit(1)
    except Exception as exc:
        print(f"Error loading file: {exc}")
        sys.exit(1)

    missing = [c for c in COLUMNS if c not in df.columns]
    if missing:
        print(f"Error: Expected columns not found in dataset: {missing}")
        sys.exit(1)

    return df[COLUMNS].reset_index(drop=True)


# ---------------------------------------------------------------------------
# Statistics computation
# ---------------------------------------------------------------------------

def compute_stats(df: pd.DataFrame) -> dict:
    mode_vals = df["age"].mode()
    return {
        "mode": int(mode_vals.iloc[0]) if not mode_vals.empty else None,
        "median": float(df["age"].median()),
        "total": len(df),
        "year_range": f"{int(df['year'].min())}–{int(df['year'].max())}",
        "executions_by_decade": _executions_by_decade(df),
    }


def _executions_by_decade(df: pd.DataFrame) -> dict:
    df = df.copy()
    df["decade"] = (df["year"] // 10 * 10).astype(int)
    return df.groupby("decade").size().to_dict()


# ---------------------------------------------------------------------------
# Display helpers
# ---------------------------------------------------------------------------

def display_row(df: pd.DataFrame, row_num: int) -> None:
    if not (0 <= row_num < len(df)):
        print(f"Invalid execution number. Enter a value between 0 and {len(df) - 1}.")
        return

    row = df.iloc[row_num]
    print(f"\n{'─' * 35}")
    print(f"  Execution no. : {row_num}")
    print(f"  Name          : {row['first_name']} {row['last_name']}")
    print(f"  TDCJ no.      : {int(row['TDCJ'])}")
    print(f"  Age           : {int(row['age'])}")
    print(f"  Year          : {int(row['year'])}")
    print(f"{'─' * 35}")


def display_stats(stats: dict) -> None:
    print(f"\n{'─' * 35}")
    print(f"  Total executions : {stats['total']}")
    print(f"  Year range       : {stats['year_range']}")
    print(f"  Median age       : {stats['median']:.0f}")
    print(f"  Mode age         : {stats['mode'] if stats['mode'] is not None else 'N/A'}")
    print(f"\n  Executions by decade:")
    for decade, count in sorted(stats["executions_by_decade"].items()):
        print(f"    {decade}s : {count}")
    print(f"{'─' * 35}")


def display_menu() -> None:
    print("\n=== TDCJ Death Row Explorer ===")
    print("  1. View record by execution number")
    print("  2. Show statistics")
    print("  3. Search by name")
    print("  4. Exit")


# ---------------------------------------------------------------------------
# Search
# ---------------------------------------------------------------------------

def search_by_name(df: pd.DataFrame, query: str) -> None:
    query = query.strip().lower()
    if not query:
        print("Please enter a name to search.")
        return

    mask = (
        df["first_name"].str.lower().str.contains(query, na=False) |
        df["last_name"].str.lower().str.contains(query, na=False)
    )
    results = df[mask]

    if results.empty:
        print(f"No records found matching '{query}'.")
        return

    print(f"\n{len(results)} result(s) for '{query}':\n")
    for idx, row in results.iterrows():
        print(f"  [{idx}] {row['first_name']} {row['last_name']} — age {int(row['age'])}, {int(row['year'])}")


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------

def main() -> None:
    print(f"\n{TITLE}")
    print(f"Source: {SOURCE_URL}\n")

    file_path = input("Enter the path to the SPSS (.sav) file: ").strip().strip('"').strip("'")
    df = load_dataset(file_path)
    stats = compute_stats(df)

    print(f"\nDataset loaded — {stats['total']} records ({stats['year_range']}).")

    while True:
        display_menu()
        choice = input("\nChoice: ").strip()

        if choice == "1":
            raw = input("Execution number: ").strip()
            try:
                display_row(df, int(raw))
            except ValueError:
                print("Invalid input. Please enter a whole number.")

        elif choice == "2":
            display_stats(stats)

        elif choice == "3":
            query = input("Search name: ").strip()
            search_by_name(df, query)

        elif choice == "4":
            confirm = input("Exit? (y/n): ").strip().lower()
            if confirm == "y":
                print("Goodbye.")
                break

        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
