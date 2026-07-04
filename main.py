import streamlit as st
import pandas as pd
from analysis import *
import matplotlib.pyplot as plt

st.set_page_config(page_title="Ecommerce Sales Analyzer", page_icon="🛒", layout="wide")

st.title("Ecommerce Sales Analyzer")
st.markdown("---")

raw_df = load_raw_data("data/sales_data_raw.csv")
df, report = clean_data(raw_df)

with st.expander("🧹 Data Cleaning Report", expanded=False):
    r1, r2, r3, r4 = st.columns(4)
    r1.metric("Raw Records", f"{report['raw_rows']:,}")
    r2.metric("Duplicates Removed", f"{report['raw_duplicate_rows']:,}")
    r3.metric("Type Mismatches Fixed", f"{report['type_mismatches_fixed']:,}")
    r4.metric("Records w/ Quality Issues", f"{report['pct_records_with_issues']}%")
    st.caption(
        f"Cleaned {report['raw_rows']:,} raw records down to {report['clean_rows']:,} "
        f"analysis-ready rows: removed exact duplicates, standardized inconsistent date "
        f"formats, converted currency-formatted Sales values to numeric, and imputed "
        f"missing categorical fields."
    )

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Revenue", f"₹{total_revenue(df):,.2f}")
with col2:
    st.metric("Total Orders", f"{len(df):,}")
with col3:
    st.metric("Avg Order Value", f"₹{average_order_value(df):,.2f}")

st.markdown("---")

col4, col5 = st.columns(2)

with col4:
    st.subheader("Sales by Category")
    category = sales_by_category(df)
    fig1, ax1 = plt.subplots()
    category.plot(kind='bar', ax=ax1, color='steelblue')
    ax1.set_xlabel("Category")
    ax1.set_ylabel("Sales")
    plt.tight_layout()
    st.pyplot(fig1)

with col5:
    st.subheader("Monthly Sales Trend")
    monthly = monthly_sales(df)
    fig2, ax2 = plt.subplots()
    monthly.plot(kind='line', marker='o', ax=ax2, color='coral')
    ax2.set_xlabel("Month")
    ax2.set_ylabel("Sales")
    plt.tight_layout()
    st.pyplot(fig2)

st.markdown("---")

col6, col7 = st.columns(2)

with col6:
    st.subheader("Top 5 Products")
    st.dataframe(top_products(df).reset_index(), width='stretch')

with col7:
    st.subheader("Top Customers")
    st.dataframe(top_customers(df).head(10).reset_index(), width='stretch')

st.markdown("---")
st.subheader("Cleaned Data (sample)")
st.dataframe(df.head(100), width='stretch')
