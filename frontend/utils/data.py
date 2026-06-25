"""Hardcoded sample data generators (replace with S3 calls later)."""
import io
import pandas as pd


def get_income_data(entity_id: str) -> pd.DataFrame:
    return pd.DataFrame({
        "Period":        ["Q1 2024", "Q2 2024", "Q3 2024", "Q4 2024"],
        "Revenue ($)":   [320_000,   415_000,   390_000,   480_000],
        "Expenses ($)":  [210_000,   260_000,   245_000,   295_000],
        "Net Income ($)":[110_000,   155_000,   145_000,   185_000],
        "Entity":        [entity_id] * 4,
    })


def get_property_data(entity_id: str) -> pd.DataFrame:
    return pd.DataFrame({
        "Property Address": [
            "10 Anson Rd #20-01, Singapore 079903",
            "1 Harbourfront Ave #14-05, Singapore 098632",
        ],
        "Type":             ["Commercial",  "Industrial"],
        "Annual Value ($)": [85_000,         62_000],
        "Ownership Start":  ["2019-03-01",   "2021-07-15"],
        "Ownership End":    ["Present",       "Present"],
        "Entity":           [entity_id,       entity_id],
    })


def get_tenancy_data(entity_id: str) -> pd.DataFrame:
    return pd.DataFrame({
        "Tenant Name":      ["ABC Pte Ltd", "XYZ Corp",    "Global Trade Sg"],
        "Lease Start":      ["2022-01-01",  "2023-04-01",  "2024-01-01"],
        "Lease End":        ["2024-12-31",  "2025-03-31",  "2025-12-31"],
        "Monthly Rent ($)": [4_500,          3_200,          5_800],
        "Property Address": [
            "10 Anson Rd #20-01",
            "10 Anson Rd #20-01",
            "1 Harbourfront Ave #14-05",
        ],
        "Entity":           [entity_id] * 3,
    })


def compute_gst(entity_id: str, year: int) -> pd.DataFrame:
    quarterly = {"Q1": 320_000, "Q2": 415_000, "Q3": 390_000, "Q4": 480_000}
    gst_rate  = 0.09
    rows = []
    for q, rev in quarterly.items():
        taxable = rev * 0.80
        gst     = round(taxable * gst_rate, 2)
        rows.append({
            "Quarter":              f"{q} {year}",
            "Total Revenue ($)":    rev,
            "Taxable Revenue ($)":  taxable,
            f"GST @ {gst_rate*100:.0f}% ($)": gst,
            "Exempt Revenue ($)":   rev - taxable,
        })
    df = pd.DataFrame(rows)
    gst_col   = f"GST @ {gst_rate*100:.0f}% ($)"
    total_row = pd.DataFrame([{
        "Quarter":             f"TOTAL {year}",
        "Total Revenue ($)":   df["Total Revenue ($)"].sum(),
        "Taxable Revenue ($)": df["Taxable Revenue ($)"].sum(),
        gst_col:               df[gst_col].sum(),
        "Exempt Revenue ($)":  df["Exempt Revenue ($)"].sum(),
    }])
    return pd.concat([df, total_row], ignore_index=True)


def to_excel_bytes(entity_id: str) -> bytes:
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        get_income_data(entity_id).to_excel(writer,   sheet_name="Income",   index=False)
        get_property_data(entity_id).to_excel(writer, sheet_name="Property", index=False)
        get_tenancy_data(entity_id).to_excel(writer,  sheet_name="Tenancy",  index=False)
    return buf.getvalue()


def to_csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode()
