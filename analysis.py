import pandas as pd
import numpy as np


def load_raw_data(path):
    return pd.read_csv(path)


def clean_data(df):
   
    report = {}
    report["raw_rows"] = len(df)
    report["raw_missing_cells"] = int(df.isnull().sum().sum())
    report["raw_duplicate_rows"] = int(df.duplicated().sum())

    has_missing = df.isnull().any(axis=1)
    is_dup = df.duplicated()
    non_standard_date = ~df['Date'].astype(str).str.match(r'^\d{4}-\d{2}-\d{2}$', na=False)
    affected_rows = (has_missing | is_dup | non_standard_date).sum()
    report["pct_records_with_issues"] = round(100 * affected_rows / len(df), 1)

    df = df.copy()

    df = df.drop_duplicates()
    def parse_sales(val):
        if pd.isna(val):
            return np.nan
        if isinstance(val, str):
            val = val.replace("₹", "").replace(",", "").strip()
        try:
            return float(val)
        except (ValueError, TypeError):
            return np.nan

    type_mismatches = df["Sales"].apply(lambda v: isinstance(v, str)).sum()
    df["Sales"] = df["Sales"].apply(parse_sales)

    df["Date"] = pd.to_datetime(df["Date"], format="mixed", errors="coerce")

    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")

    before_dropna = len(df)
    df = df.dropna(subset=["Date", "Sales", "Quantity"])
    dropped_for_missing = before_dropna - len(df)

    df["Customer"] = df["Customer"].fillna("Unknown Customer")
    df["Product"] = df["Product"].fillna("Unknown Product")

    report["type_mismatches_fixed"] = int(type_mismatches)
    report["rows_dropped_missing_critical"] = int(dropped_for_missing)
    report["clean_rows"] = len(df)

    return df, report


def total_revenue(df):
    return df['Sales'].sum()


def sales_by_category(df):
    return df.groupby('Category')['Sales'].sum().sort_values(ascending=False)


def top_products(df):
    return df.groupby('Product')['Sales'].sum().sort_values(ascending=False).head(5)


def monthly_sales(df):
    df = df.copy()
    df['Month'] = df['Date'].dt.to_period('M')
    return df.groupby('Month')['Sales'].sum()


def top_customers(df):
    return df.groupby('Customer')['Sales'].sum().sort_values(ascending=False)


def average_order_value(df):
    return df['Sales'].mean()
