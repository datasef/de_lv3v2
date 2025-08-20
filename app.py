import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

st.set_page_config(page_title="Quick Sales Dashboard", layout="wide")
st.title("Sales Dashboard ")
st.caption("Sinh dữ liệu giả lập ngay trong app để deploy trên Streamlit Cloud.")

@st.cache_data
def make_data(n=1500, seed=1):
    np.random.seed(seed)
    start = datetime(2024,1,1)
    dates = [start + timedelta(days=int(np.random.uniform(0, 540))) for _ in range(n)]
    regions = np.random.choice(['North','South','East','West'], size=n)
    categories = np.random.choice(['Electronics','Apparel','Home','Grocery','Beauty'], size=n)
    quantity = np.random.poisson(lam=2.4, size=n) + 1
    unit_price = np.random.uniform(10, 500, size=n).round(2)
    discount = np.clip(np.random.normal(0.12, 0.07, size=n), 0, 0.4)
    revenue = (quantity * unit_price * (1-discount)).round(2)
    status = np.random.choice(['Completed','Returned','Cancelled'], size=n, p=[0.88,0.07,0.05])
    df = pd.DataFrame({
        'date': pd.to_datetime(dates),
        'month': [d.strftime('%Y-%m') for d in dates],
        'region': regions,
        'category': categories,
        'quantity': quantity,
        'unit_price': unit_price,
        'discount_rate': discount,
        'revenue': revenue,
        'status': status
    })
    return df

df = make_data()

with st.sidebar:
    st.header("Filters")
    dmin, dmax = df['date'].min(), df['date'].max()
    date_rng = st.date_input("Date range", value=(dmin, dmax), min_value=dmin, max_value=dmax)
    regions = st.multiselect("Region", sorted(df['region'].unique()), placeholder="All")
    cats = st.multiselect("Category", sorted(df['category'].unique()), placeholder="All")
    status = st.multiselect("Status", sorted(df['status'].unique()), placeholder="All")

mask = (df['date'].between(pd.to_datetime(date_rng[0]), pd.to_datetime(date_rng[1])))
if regions: mask &= df['region'].isin(regions)
if cats: mask &= df['category'].isin(cats)
if status: mask &= df['status'].isin(status)
dff = df[mask].copy()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Orders", f"{len(dff):,}")
col2.metric("Revenue", f"{dff['revenue'].sum():,.0f}")
aov = (dff['revenue'].sum()/len(dff)) if len(dff) else 0
col3.metric("AOV", f"{aov:,.0f}")
ret_rate = (len(dff[dff['status']=='Returned'])/len(dff)*100) if len(dff) else 0
col4.metric("Return rate", f"{ret_rate:.2f}%")

st.divider()

rev_month = dff.groupby('month', as_index=False)['revenue'].sum().sort_values('month')
st.subheader("Revenue by Month")
st.line_chart(rev_month, x='month', y='revenue', height=280)

rev_region = dff.groupby('region', as_index=False)['revenue'].sum().sort_values('revenue', ascending=False)
st.subheader("Revenue by Region")
st.bar_chart(rev_region, x='region', y='revenue', height=280)

top_cat = dff.groupby('category', as_index=False)['revenue'].sum().sort_values('revenue', ascending=False).head(5)
st.subheader("Top Categories by Revenue")
st.bar_chart(top_cat, x='category', y='revenue', height=280)

st.caption("One-file app")
