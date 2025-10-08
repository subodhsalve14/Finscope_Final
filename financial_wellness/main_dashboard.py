# Main Economic Trend Analyzer Dashboard
import streamlit as st

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="Economic Trend Analyzer",
    page_icon="📊",
    layout="wide"
)

# Add navigation info
st.sidebar.success("Select a page above to view different economic forecasts!")

# -------------------------------
# Main Dashboard
# -------------------------------
st.title("📊 Economic Trend Analyzer")
st.markdown("### Comprehensive Economic Forecasting for Personal Finance Decisions")

# -------------------------------
# Navigation Cards
# -------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="padding: 20px; border-radius: 10px; border: 2px solid #1f77b4; background-color: #f0f8ff;">
        <h3 style="color: #1f77b4;">📈 Inflation Forecast</h3>
        <p>Track inflation trends and understand how they impact your purchasing power, savings, and investments.</p>
        <ul>
            <li>Historical inflation analysis</li>
            <li>12-month forecasts</li>
            <li>Personal expense impact</li>
            <li>Insurance coverage recommendations</li>
        </ul>
        <p><strong>👆 Use the sidebar to navigate to "📈 Inflation Forecast" page</strong></p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="padding: 20px; border-radius: 10px; border: 2px solid #2ca02c; background-color: #f0fff0;">
        <h3 style="color: #2ca02c;">📊 GDP Growth Forecast</h3>
        <p>Monitor GDP trends to make informed career and investment decisions.</p>
        <ul>
            <li>Quarterly GDP forecasts</li>
            <li>Job market predictions</li>
            <li>Salary growth expectations</li>
            <li>Investment timing insights</li>
        </ul>
        <p><strong>👆 Use the sidebar to navigate to "📊 GDP Forecast" page</strong></p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="padding: 20px; border-radius: 10px; border: 2px solid #d62728; background-color: #fff5f5;">
        <h3 style="color: #d62728;">💰 Interest Rates Forecast</h3>
        <p>Track interest rate trends for optimal loan and investment decisions.</p>
        <ul>
            <li>Multiple rate forecasts</li>
            <li>EMI impact calculator</li>
            <li>Savings optimization</li>
            <li>Refinancing recommendations</li>
        </ul>
        <p><strong>👆 Use the sidebar to navigate to "💰 Interest Rates Forecast" page</strong></p>
    </div>
    """, unsafe_allow_html=True)

# -------------------------------
# Key Features Overview
# -------------------------------
st.markdown("---")
st.subheader("🎯 Key Features")

feature_col1, feature_col2 = st.columns(2)

with feature_col1:
    st.markdown("""
    #### 🔮 Advanced Forecasting
    - **Prophet ML Models**: Facebook's time-series forecasting
    - **ARIMA Integration**: Statistical forecasting methods
    - **Seasonal Patterns**: Account for economic cycles
    - **Confidence Intervals**: Understand forecast uncertainty
    """)

with feature_col2:
    st.markdown("""
    #### 🎯 Actionable Insights
    - **Timing Recommendations**: When to buy, sell, invest
    - **Risk Alerts**: Early warning systems
    - **Portfolio Optimization**: Asset allocation guidance
    - **Life Planning**: Major financial decisions
    """)

# -------------------------------
# Data Sources
# -------------------------------
st.markdown("---")
st.subheader("📋 Data Sources")

st.markdown("""
Our forecasts are based on official data from:
- **Reserve Bank of India (RBI)**: Interest rates, monetary policy
- **Ministry of Statistics (MOSPI)**: GDP, inflation, economic indicators  
- **World Bank**: International economic data
- **Financial Benchmarks India (FBIL)**: Bond yields, market rates

*All forecasts are for educational purposes. Please consult financial advisors for investment decisions.*
""")

# -------------------------------
# Quick Stats (if data available)
# -------------------------------
try:
    import pandas as pd
    
    # Try to load and display quick stats
    st.markdown("---")
    st.subheader("📊 Current Economic Snapshot")
    
    # This will show current values if data files exist
    col1, col2, col3 = st.columns(3)
    
    try:
        df_inflation = pd.read_excel("data/df_all.xlsx")
        latest_inflation = df_inflation['Combined Inflation (%)'].iloc[-1]
        col1.metric("Current Inflation", f"{latest_inflation:.1f}%")
    except:
        col1.metric("Current Inflation", "Data Loading...")
    
    try:
        df_gdp = pd.read_excel("data/gdp_data.xlsx")
        latest_gdp = df_gdp['GDP_Growth_Rate'].iloc[-1]
        col2.metric("Latest GDP Growth", f"{latest_gdp:.1f}%")
    except:
        col2.metric("Latest GDP Growth", "Data Loading...")
        
    try:
        df_rates = pd.read_excel("data/interest_rates_data.xlsx")
        latest_repo = df_rates['Repo_Rate'].iloc[-1]
        col3.metric("Current Repo Rate", f"{latest_repo:.2f}%")
    except:
        col3.metric("Current Repo Rate", "Data Loading...")
        
except ImportError:
    pass