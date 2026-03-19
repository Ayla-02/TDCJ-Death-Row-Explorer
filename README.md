# Texas Death Row Execution Records Explorer

A menu-driven CLI tool for exploring Texas Department of Criminal Justice (TDCJ) execution records from 1982–2024, built as a university assignment for *Fundamentals of Computing* at Abertay University.

**Data source:** [TDCJ Executed Offenders](https://www.tdcj.texas.gov/death_row/dr_executed_offenders.html)

---

## Features

- Look up individual records by execution number
- View summary statistics — total executions, year range, median and mode age, and a breakdown by decade
- Search records by first or last name

---

## Requirements

- Python 3.8+
- `pandas`
- `pyreadstat`

Install dependencies:

```bash
pip install pandas pyreadstat
```

---

## Usage

```bash
python tx_dataset.py
```

You'll be prompted to enter the path to the `.sav` file, then navigate via a numbered menu.

---

## Dataset

The SPSS file (`tx_ds.sav`) contains the following fields:

| Field | Description |
|---|---|
| `last_name` | Offender last name |
| `first_name` | Offender first name |
| `TDCJ` | TDCJ identification number |
| `age` | Age at time of execution |
| `year` | Year of execution |

---

## Notes

This was developed as an introductory assignment and is intended for educational use only. The dataset covers executions carried out between 1982 and 2024.
