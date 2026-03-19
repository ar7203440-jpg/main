# dashboard.py - My Smart Bot Dashboard
import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# Page config
st.set_page_config(page_title="My Smart Bot", layout="wide")
st.title("🤖 My Smart Bot - Live Dashboard")

# Load data from database
@st.cache_data
def load_data():
    conn = sqlite3.connect('business.db')
    
    # Earnings data
    earnings_df = pd.read_sql_query("SELECT * FROM earnings ORDER BY date DESC", conn)
    # Posts data
    posts_df = pd.read_sql_query("SELECT * FROM posts ORDER BY timestamp DESC", conn)
    
    conn.close()
    return earnings_df, posts_df

earnings_df, posts_df = load_data()

# KPI Cards
col1, col2, col3 = st.columns(3)
total_earnings = earnings_df['amount'].sum() if not earnings_df.empty else 0
total_posts = len(posts_df)
col1.metric("💰 Total Earnings", f"Rs. {total_earnings:,.0f}")
col2.metric("📝 Total Posts", total_posts)
if not earnings_df.empty:
    top_source = earnings_df.groupby('source')['amount'].sum().idxmax()
    col3.metric("🏆 Top Source", top_source)

st.divider()

# Charts
col_ch1, col_ch2 = st.columns(2)

with col_ch1:
    st.subheader("Earnings by Source")
    if not earnings_df.empty:
        source_sum = earnings_df.groupby('source')['amount'].sum().reset_index()
        fig = px.pie(source_sum, values='amount', names='source')
        st.plotly_chart(fig, use_container_width=True)

with col_ch2:
    st.subheader("Recent Posts")
    if not posts_df.empty:
        st.dataframe(posts_df[['timestamp', 'platform', 'content']].head(5))

st.subheader("📋 All Posts")
if not posts_df.empty:
    st.dataframe(posts_df)
else:
    st.info("No posts yet.")