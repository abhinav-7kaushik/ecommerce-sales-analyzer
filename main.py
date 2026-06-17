import streamlit as st
import pandas as pd
from analysis import *
import matplotlib.pyplot as plt

st.set_page_config(page_title="Ecommerce Sales Analyzer", page_icon="🛒", layout="wide")

st.title("🛒 Ecommerce Sales Analyzer")
st.markdown("---")

df = load_data("data/sales_data.csv")

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
    st.dataframe(top_products(df).reset_index(), use_container_width=True)

with col7:
    st.subheader("Top Customers")
    st.dataframe(top_customers(df).reset_index(), use_container_width=True)

st.markdown("---")
st.subheader("Raw Data")
st.dataframe(df, use_container_width=True)