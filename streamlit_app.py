import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# --- PAGE SETUP ---
st.set_page_config(page_title="Wealth Engine", layout="wide", initial_sidebar_state="expanded")
st.title("West-Wiseman Wealth Architecture")

# --- THE CONTROL ROOM (SIDEBAR) ---
st.sidebar.header("The Control Room")
st.sidebar.markdown("Adjust variables to see real-time impact on the masterplan.")

fortnightly_shovel = st.sidebar.slider("The Shovel (Fortnightly IBKR)", min_value=400, max_value=1500, value=800, step=50)
margin_interest = st.sidebar.slider("Margin Interest Rate (%)", min_value=4.0, max_value=10.0, value=6.8, step=0.1) / 100
googl_growth = st.sidebar.slider("GOOGL Assumed Annual Growth (%)", min_value=2.0, max_value=20.0, value=10.0, step=0.5) / 100

# --- THE CURRENT METRICS ---
st.header("Phase 1: The Leveraged Launch")
col1, col2, col3, col4 = st.columns(4)

current_margin = 30000
current_portfolio = 60000
safe_drop = ((current_portfolio - (current_margin / 0.75)) / current_portfolio) * 100

col1.metric(label="Current Margin Debt", value=f"${current_margin:,.0f}")
col2.metric(label="Total GOOGL Equity", value=f"${current_portfolio:,.0f}")
col3.metric(label="Auto-Sell Trigger", value=f"${current_margin / 0.75:,.0f}")
col4.metric(label="Safe Drop Buffer", value=f"{safe_drop:.1f}%")

# --- THE MATHEMATICS ENGINE ---
start_date = datetime(2026, 4, 23)
loan = current_margin
portfolio = current_portfolio
fortnights_in_year = 26

dates, loans, portfolios = [], [], []

current_date = start_date
while loan > 0:
    interest = loan * (margin_interest / fortnights_in_year)
    principal_payment = fortnightly_shovel - interest
    
    if loan < principal_payment:
        principal_payment = loan
        
    loan -= principal_payment
    portfolio *= (1 + googl_growth / fortnights_in_year)
    
    dates.append(current_date)
    loans.append(loan if loan > 0 else 0)
    portfolios.append(portfolio)
    
    current_date += timedelta(days=14)

df = pd.DataFrame({'Date': dates, 'Margin Loan': loans, 'Portfolio Value': portfolios})

# --- THE DESTRUCTION GRAPH ---
st.subheader("The Margin Destruction Timeline")
st.markdown("Watch the $800 shovel drag the debt to $0 before the October 2027 deadline.")

fig = px.line(df, x='Date', y=['Margin Loan', 'Portfolio Value'], 
              color_discrete_map={'Margin Loan': '#ef4444', 'Portfolio Value': '#10b981'})
fig.update_layout(yaxis_title="AUD ($)", xaxis_title="Timeline", hovermode="x unified")
st.plotly_chart(fig, use_container_width=True)

# --- PHASE 2: SETTLEMENT HUB ---
st.header("Phase 2: The Almeria Three Settlement (Late 2027)")
colA, colB = st.columns(2)

# Placeholder variables you can update manually as accounts grow
hisa_current = 20000 
fhsss_current = 50000 

colA.metric(label="HISA Arsenal (Target: $87,000)", value=f"${hisa_current:,.0f}", delta=f"${87000 - hisa_current:,.0f} remaining", delta_color="inverse")
st.progress(hisa_current / 87000 if hisa_current < 87000 else 1.0)

colB.metric(label="FHSSS Reservoir (Target: $90,000)", value=f"${fhsss_current:,.0f}", delta=f"${90000 - fhsss_current:,.0f} remaining", delta_color="inverse")
st.progress(fhsss_current / 90000 if fhsss_current < 90000 else 1.0)

st.markdown("---")
st.markdown("**System Status:** Dual-Engine Architecture is fully operational. Awaiting Phase 2 FHSSS extraction trigger.")
