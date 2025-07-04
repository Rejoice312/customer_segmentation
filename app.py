import streamlit as st
import pandas as pd
import plotly.express as px

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv('your_dataset.csv', parse_dates=['TransactionDate', 'PreviousTransactionDate'])
    return df

# Load dataset
df = load_data()

# Page Config
st.set_page_config(page_title="PalmPay Payment Insights", layout="wide")

st.title("\U0001F4B0 PalmPay Payment Transactions Dashboard")

# KPI Section
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_transactions = df['TransactionID'].nunique()
    st.metric("Total Transactions", f"{total_transactions:,}")

with col2:
    total_amount = df['TransactionAmount'].sum()
    st.metric("Total Transaction Value (₦)", f"{total_amount:,.2f}")

with col3:
    avg_transaction = df['TransactionAmount'].mean()
    st.metric("Average Transaction (₦)", f"{avg_transaction:,.2f}")

with col4:
    active_customers = df['AccountID'].nunique()
    st.metric("Active Customers", f"{active_customers:,}")

# Time Series Analysis
st.subheader("\U0001F4C5 Daily Transaction Volume")
df['TransactionDate'] = pd.to_datetime(df['TransactionDate'])
daily_volume = df.groupby(df['TransactionDate'].dt.date)['TransactionID'].count().reset_index()
fig1 = px.line(daily_volume, x='TransactionDate', y='TransactionID', title='Daily Transactions', markers=True)
st.plotly_chart(fig1, use_container_width=True)

# Channel Performance
st.subheader("\U0001F310 Channel Usage Breakdown")
channel_data = df['Channel'].value_counts().reset_index()
channel_data.columns = ['Channel', 'Count']
fig2 = px.pie(channel_data, values='Count', names='Channel', title='Transactions by Channel', color_discrete_sequence=px.colors.qualitative.Set3)
st.plotly_chart(fig2, use_container_width=True)

# Customer Age vs. Transaction Amount
st.subheader("\U0001F465 Customer Age vs. Average Transaction Amount")
age_amount = df.groupby('CustomerAge')['TransactionAmount'].mean().reset_index()
fig3 = px.bar(age_amount, x='CustomerAge', y='TransactionAmount', color='TransactionAmount', color_continuous_scale='Tealgrn', title='Avg Transaction Amount by Age')
st.plotly_chart(fig3, use_container_width=True)

# Occupation Analysis
st.subheader("\U0001F4BC Transactions by Customer Occupation")
occupation_data = df.groupby('CustomerOccupation')['TransactionAmount'].sum().reset_index().sort_values(by='TransactionAmount', ascending=False)
fig4 = px.bar(occupation_data, x='CustomerOccupation', y='TransactionAmount', color='TransactionAmount', color_continuous_scale='Blues', title='Total Transaction Value by Occupation')
st.plotly_chart(fig4, use_container_width=True)

# Fraud Risk Flags
st.subheader("\U0001F6E1\ufe0f Potential Risk Indicators")
df['HighValueFlag'] = (df['TransactionAmount'] > df['TransactionAmount'].quantile(0.95)).astype(int)
df['MultipleLoginsFlag'] = (df['LoginAttempts'] > 3).astype(int)
df['LateNightFlag'] = df['TransactionDate'].dt.hour.apply(lambda x: 1 if x < 6 or x > 22 else 0)
df['FraudScore'] = df[['HighValueFlag', 'MultipleLoginsFlag', 'LateNightFlag']].sum(axis=1)

risk_summary = df['FraudScore'].value_counts().reset_index()
risk_summary.columns = ['FraudScore', 'Count']
fig5 = px.bar(risk_summary, x='FraudScore', y='Count', color='Count', color_continuous_scale='Reds', title='Fraud Risk Score Distribution')
st.plotly_chart(fig5, use_container_width=True)

st.success("\U0001F389 Dashboard Generated Successfully!")
