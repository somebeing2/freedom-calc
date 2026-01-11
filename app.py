import streamlit as st
import pandas as pd
import math

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="FreedomCalc.ai | FIRE Simulator",
    page_icon="📈",
    layout="wide"
)

# Custom CSS for a "Fintech" look
st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #00C853;
    }
    .stButton>button {
        width: 100%;
        background-color: #000000;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: USER INPUTS ---
with st.sidebar:
    st.header("⚙️ Your Financial Profile")
    
    current_age = st.number_input("Current Age", 18, 60, 24)
    retire_age = st.number_input("Target Retirement Age", 30, 80, 50)
    
    st.markdown("---")
    
    current_savings = st.number_input("Current Savings (₹)", 0, 10000000, 50000)
    monthly_investment = st.number_input("Monthly SIP Amount (₹)", 500, 500000, 10000)
    
    st.markdown("---")
    
    expected_return = st.slider("Expected Annual Return (%)", 4.0, 20.0, 12.0, help="Nifty 50 historic average is ~12%")
    inflation_rate = st.slider("Expected Inflation (%)", 1.0, 10.0, 6.0)

# --- MAIN LOGIC (THE FINANCE ENGINE) ---
years_to_invest = retire_age - current_age
months = years_to_invest * 12

# We calculate year-by-year for the chart
data = []
corpus = current_savings
total_invested = current_savings

for year in range(1, years_to_invest + 1):
    # Add yearly contribution (approx)
    yearly_contribution = monthly_investment * 12
    total_invested += yearly_contribution
    
    # Add Interest
    interest = corpus * (expected_return / 100)
    corpus += interest + yearly_contribution
    
    # Adjust for inflation (Purchasing Power)
    real_value = corpus / ((1 + inflation_rate/100) ** year)
    
    data.append({
        "Year": current_age + year,
        "Portfolio Value (Nominal)": round(corpus),
        "Invested Amount": round(total_invested),
        "Real Purchasing Power": round(real_value)
    })

df = pd.read_json(pd.DataFrame(data).to_json()) # Simple conversion for Streamlit

# --- DASHBOARD UI ---
st.title("💸 FreedomCalc.ai")
st.caption("Financial Independence & Retire Early (FIRE) Simulator")

# Top Level Metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="⏳ Years to Freedom", value=f"{years_to_invest} Years")

with col2:
    st.metric(label="💰 Projected Corpus", value=f"₹ {corpus:,.0f}", delta="Target Hit")

with col3:
    # 4% Withdrawal Rule
    monthly_income = (corpus * 0.04) / 12
    st.metric(label="🏖️ Passive Monthly Income", value=f"₹ {monthly_income:,.0f}", help="Based on the 4% Safe Withdrawal Rule")

st.markdown("---")

# The Growth Chart
st.subheader("📈 Your Wealth Trajectory")
st.line_chart(df, x="Year", y=["Portfolio Value (Nominal)", "Invested Amount"], color=["#00C853", "#FF5252"])

# Detailed Analysis
st.subheader("🧐 The Reality Check")
col_a, col_b = st.columns([1, 2])

with col_a:
    st.info(f"""
    **Analysis:**
    To retire at **{retire_age}**, you need to stay consistent.
    
    While you will invest **₹ {total_invested:,.0f}**, 
    compound interest will generate **₹ {(corpus - total_invested):,.0f}** for you.
    """)

with col_b:
    st.dataframe(df, use_container_width=True)

# Footer
st.markdown("---")
st.caption("Built with Python & Streamlit | Project by Kevin Joseph")