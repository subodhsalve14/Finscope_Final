# Interest Rates Forecast Dashboard
import streamlit as st
import pandas as pd
from prophet import Prophet
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

# -------------------------------
# 1️⃣ App Configuration
# -------------------------------
st.set_page_config(page_title="Interest Rates Forecast Dashboard", layout="wide")
st.title("💰 Interest Rates Forecast Dashboard")

# -------------------------------
# 2️⃣ Load Interest Rates Data
# -------------------------------
@st.cache_data
def load_rates_data():
    try:
        # Load interest rates data (we'll need to create this file)
        df_rates = pd.read_excel("data/interest_rates_data.xlsx", parse_dates=['Date'])
        return df_rates
    except FileNotFoundError:
        st.error("Interest rates data file not found. Please add 'interest_rates_data.xlsx' to the data folder.")
        return None

df_rates = load_rates_data()

if df_rates is not None:
    # -------------------------------
    # 3️⃣ Rate Selection
    # -------------------------------
    st.sidebar.header("📊 Select Interest Rate")
    available_rates = [col for col in df_rates.columns if col != 'Date']
    selected_rate = st.sidebar.selectbox("Choose Rate to Forecast:", available_rates)
    
    # Rate descriptions
    rate_descriptions = {
        'Repo_Rate': 'RBI Repo Rate - The key policy rate',
        'Bond_10Y': '10-Year Government Bond Yield - Long-term benchmark',
        'Home_Loan_Rate': 'Average Home Loan Rate - What you pay for housing',
        'Deposit_Rate': 'Average Bank Deposit Rate - What you earn on savings',
        'Personal_Loan_Rate': 'Average Personal Loan Rate',
        'Car_Loan_Rate': 'Average Car Loan Rate'
    }
    
    st.info(f"**{selected_rate}**: {rate_descriptions.get(selected_rate, 'Interest rate indicator')}")

    # -------------------------------
    # 4️⃣ Prepare Data for Prophet
    # -------------------------------
    df_prophet = df_rates[['Date', selected_rate]].copy()
    df_prophet['y'] = pd.to_numeric(df_prophet[selected_rate], errors='coerce')
    df_prophet['y'] = df_prophet['y'].ffill()
    df_prophet = df_prophet.rename(columns={'Date': 'ds'})
    df_prophet = df_prophet.dropna()

    # -------------------------------
    # 5️⃣ Train Prophet Model
    # -------------------------------
    @st.cache_data
    def train_rates_model(df, rate_name):
        model = Prophet(
            yearly_seasonality=True,
            weekly_seasonality=False,
            daily_seasonality=False,
            changepoint_prior_scale=1.2,  # Interest rates can be volatile
            seasonality_mode='additive'
        )
        # Add monthly seasonality for interest rates
        model.add_seasonality(name='monthly', period=30.44, fourier_order=6)
        model.fit(df)
        return model

    model = train_rates_model(df_prophet, selected_rate)

    # -------------------------------
    # 6️⃣ Generate Forecast
    # -------------------------------
    future = model.make_future_dataframe(periods=12, freq='MS')  # Monthly forecasts
    forecast = model.predict(future)
    df_prophet['Fitted'] = forecast.loc[:len(df_prophet)-1, 'yhat']

    # -------------------------------
    # 7️⃣ Key Insights Section
    # -------------------------------
    st.subheader("🔑 Key Rate Insights")

    # Latest rate
    latest_rate = df_prophet['y'].iloc[-1]
    # Next month forecast
    next_month_forecast = forecast.iloc[len(df_prophet)]['yhat']
    # Average forecast over next 12 months
    avg_forecast_12m = forecast.tail(12)['yhat'].mean()
    # Rate direction
    rate_direction = "📈 Rising" if next_month_forecast > latest_rate else "📉 Falling"

    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📊 Current Rate", f"{latest_rate:.2f}%")
    col2.metric("📅 Next Month", f"{next_month_forecast:.2f}%")
    col3.metric("📈 12M Average", f"{avg_forecast_12m:.2f}%")
    col4.metric("🎯 Trend", rate_direction)

    # -------------------------------
    # 8️⃣ User Impact Analysis
    # -------------------------------
    st.subheader("💰 Personal Finance Impact")
    
    # User inputs based on selected rate
    if selected_rate in ['Repo_Rate', 'Home_Loan_Rate']:
        st.markdown("#### 🏠 Home Loan Impact")
        col1, col2 = st.columns(2)
        with col1:
            loan_amount = st.number_input("Outstanding Loan Amount (₹):", value=5000000, step=100000)
        with col2:
            remaining_tenure = st.number_input("Remaining Tenure (Years):", value=15, step=1)
        
        # EMI calculation
        def calculate_emi(principal, rate, tenure_years):
            monthly_rate = rate / (12 * 100)
            tenure_months = tenure_years * 12
            if monthly_rate > 0:
                emi = principal * monthly_rate * (1 + monthly_rate)**tenure_months / ((1 + monthly_rate)**tenure_months - 1)
            else:
                emi = principal / tenure_months
            return emi
        
        current_emi = calculate_emi(loan_amount, latest_rate, remaining_tenure)
        forecast_emi = calculate_emi(loan_amount, avg_forecast_12m, remaining_tenure)
        emi_difference = forecast_emi - current_emi
        
        st.markdown(f"""
        **🏠 Home Loan Analysis:**
        - 💳 **Current EMI:** ₹{current_emi:,.0f}
        - 🔮 **Forecasted EMI:** ₹{forecast_emi:,.0f}
        - 📊 **Monthly Difference:** ₹{emi_difference:,.0f}
        - 💰 **Annual Impact:** ₹{emi_difference * 12:,.0f}
        """)
        
        if emi_difference < -1000:
            st.success("🎉 Great news! Your EMI is expected to decrease significantly.")
        elif emi_difference > 1000:
            st.warning("⚠️ Your EMI may increase. Consider prepayment or refinancing.")
        else:
            st.info("📊 EMI expected to remain relatively stable.")

    elif selected_rate in ['Deposit_Rate']:
        st.markdown("#### 💰 Savings & Investment Impact")
        savings_amount = st.number_input("Your Savings/FD Amount (₹):", value=1000000, step=50000)
        
        current_returns = savings_amount * latest_rate / 100
        forecast_returns = savings_amount * avg_forecast_12m / 100
        returns_difference = forecast_returns - current_returns
        
        st.markdown(f"""
        **💰 Savings Analysis:**
        - 📊 **Current Annual Returns:** ₹{current_returns:,.0f}
        - 🔮 **Forecasted Returns:** ₹{forecast_returns:,.0f}
        - 📈 **Annual Difference:** ₹{returns_difference:,.0f}
        """)

    # -------------------------------
    # 9️⃣ Interactive Chart
    # -------------------------------
    st.subheader(f"📈 {selected_rate}: Historical & Forecast")
    
    fig = go.Figure()

    # Historical rates
    fig.add_trace(go.Scatter(
        x=df_prophet['ds'], y=df_prophet['y'],
        mode='lines+markers', name=f'Historical {selected_rate}',
        line=dict(color='#1f77b4', width=2),
        marker=dict(size=4)
    ))

    # Fitted values
    fig.add_trace(go.Scatter(
        x=df_prophet['ds'], y=df_prophet['Fitted'],
        mode='lines', name='Model Fit',
        line=dict(color='#2ca02c', dash='dash', width=2)
    ))

    # Forecast
    forecast_data = forecast[len(df_prophet):]
    fig.add_trace(go.Scatter(
        x=forecast_data['ds'], y=forecast_data['yhat'],
        mode='lines+markers', name='Rate Forecast',
        line=dict(color='#d62728', width=3),
        marker=dict(size=4)
    ))

    # Confidence interval
    fig.add_trace(go.Scatter(
        x=list(forecast_data['ds']) + list(forecast_data['ds'][::-1]),
        y=list(forecast_data['yhat_lower']) + list(forecast_data['yhat_upper'][::-1]),
        fill='toself', fillcolor='rgba(214,39,40,0.15)',
        line=dict(color='rgba(255,255,255,0)'),
        hoverinfo="skip", showlegend=True, name='Forecast Confidence'
    ))

    fig.update_layout(
        title=dict(text=f'🇮🇳 {selected_rate}: Historical & Forecast', x=0.5, xanchor='center'),
        xaxis_title='Date',
        yaxis_title='Interest Rate (%)',
        hovermode='x unified',
        template="plotly_white",
        height=600,
        margin=dict(l=40, r=40, t=60, b=40),
        legend=dict(
            orientation="h", yanchor="bottom", y=-0.2,
            xanchor="center", x=0.5, font=dict(size=12)
        )
    )

    st.plotly_chart(fig, use_container_width=True)

    # -------------------------------
    # 🔟 Forecast Table
    # -------------------------------
    st.subheader("📅 Interest Rate Forecast (Next 12 Months)")
    forecast_12m = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(12)
    forecast_12m = forecast_12m.rename(columns={
        'ds': 'Month',
        'yhat': 'Predicted Rate (%)',
        'yhat_lower': 'Lower Bound (%)',
        'yhat_upper': 'Upper Bound (%)'
    })

    st.dataframe(
        forecast_12m.style.format({
            'Predicted Rate (%)': "{:.2f}%",
            'Lower Bound (%)': "{:.2f}%",
            'Upper Bound (%)': "{:.2f}%"
        })
    )

    # -------------------------------
    # 1️⃣1️⃣ Rate Comparison
    # -------------------------------
    if len(available_rates) > 1:
        st.subheader("📊 Rate Comparison")
        
        # Show current rates for all available rates
        current_rates_data = []
        for rate in available_rates:
            latest_val = df_rates[rate].iloc[-1]
            current_rates_data.append({
                'Rate Type': rate,
                'Current Rate (%)': f"{latest_val:.2f}%"
            })
        
        rates_df = pd.DataFrame(current_rates_data)
        st.dataframe(rates_df)

else:
    st.info("Please add interest rates data to continue. See instructions below.")
    
    st.markdown("""
    ### 📋 Required Data Format for Interest Rates Analysis
    
    Create a file `data/interest_rates_data.xlsx` with columns:
    - **Date**: Monthly dates (e.g., 2020-01-01, 2020-02-01, etc.)
    - **Repo_Rate**: RBI Repo Rate (%)
    - **Bond_10Y**: 10-Year Government Bond Yield (%)
    - **Home_Loan_Rate**: Average Home Loan Rate (%)
    - **Deposit_Rate**: Average Bank Deposit Rate (%)
    - **Personal_Loan_Rate**: Average Personal Loan Rate (%) [Optional]
    - **Car_Loan_Rate**: Average Car Loan Rate (%) [Optional]
    
    **Data Sources:**
    - Reserve Bank of India (RBI) Database
    - Financial Benchmarks India Ltd (FBIL)
    - Major bank websites for retail rates
    """)