# GDP Forecast Dashboard
import streamlit as st
import pandas as pd
from prophet import Prophet
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

# -------------------------------
# 1️⃣ App Configuration
# -------------------------------
st.set_page_config(page_title="GDP Growth Forecast Dashboard", layout="wide")
st.title("📈 GDP Growth Forecast Dashboard")

# -------------------------------
# 2️⃣ Load GDP Data
# -------------------------------
@st.cache_data
def load_gdp_data():
    try:
        # Load GDP data (we'll need to create this file)
        df_gdp = pd.read_excel("data/gdp_data.xlsx", parse_dates=['Date'])
        return df_gdp
    except FileNotFoundError:
        st.error("GDP data file not found. Please add 'gdp_data.xlsx' to the data folder.")
        return None

df_gdp = load_gdp_data()

if df_gdp is not None:
    # -------------------------------
    # 3️⃣ Prepare Data for Prophet
    # -------------------------------
    df_prophet = df_gdp[['Date', 'GDP_Growth_Rate']].copy()
    df_prophet['y'] = pd.to_numeric(df_prophet['GDP_Growth_Rate'], errors='coerce')
    df_prophet['y'] = df_prophet['y'].ffill()
    df_prophet = df_prophet.rename(columns={'Date': 'ds'})
    df_prophet = df_prophet.dropna()

    # -------------------------------
    # 4️⃣ Train Prophet Model
    # -------------------------------
    @st.cache_data
    def train_gdp_model(df):
        model = Prophet(
            yearly_seasonality=True,
            weekly_seasonality=False,
            daily_seasonality=False,
            changepoint_prior_scale=0.8,  # GDP is less volatile than inflation
            seasonality_mode='additive'
        )
        # Add quarterly seasonality for GDP
        model.add_seasonality(name='quarterly', period=91.25, fourier_order=4)
        model.fit(df)
        return model

    model = train_gdp_model(df_prophet)

    # -------------------------------
    # 5️⃣ Generate Forecast
    # -------------------------------
    future = model.make_future_dataframe(periods=12, freq='QS')  # Quarterly forecasts
    forecast = model.predict(future)
    df_prophet['Fitted'] = forecast.loc[:len(df_prophet)-1, 'yhat']

    # -------------------------------
    # 6️⃣ Key Insights Section
    # -------------------------------
    st.subheader("🔑 Key GDP Insights")

    # Latest GDP growth
    latest_gdp = df_prophet['y'].iloc[-1]
    # Next quarter forecast
    next_quarter_forecast = forecast.iloc[len(df_prophet)]['yhat']
    # Average forecast over next 4 quarters
    avg_forecast_4q = forecast.tail(4)['yhat'].mean()

    # Display metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("📊 Latest GDP Growth", f"{latest_gdp:.1f}%")
    col2.metric("📅 Next Quarter Forecast", f"{next_quarter_forecast:.1f}%")
    col3.metric("📈 Avg 4Q Forecast", f"{avg_forecast_4q:.1f}%")

    # -------------------------------
    # 7️⃣ User Impact Analysis
    # -------------------------------
    st.subheader("💰 What This Means for You")
    
    # User inputs
    col1, col2 = st.columns(2)
    with col1:
        current_salary = st.number_input("Your Current Annual Salary (₹):", value=800000, step=50000)
    with col2:
        investment_amount = st.number_input("Your Equity Investment (₹):", value=500000, step=50000)

    # GDP impact calculations
    if avg_forecast_4q > 7.0:
        salary_growth = "12-15%"
        market_outlook = "Strong Bull Market Expected"
        recommendation = "Good time for aggressive equity allocation"
    elif avg_forecast_4q > 6.0:
        salary_growth = "8-12%"
        market_outlook = "Moderate Growth Expected"
        recommendation = "Balanced portfolio recommended"
    else:
        salary_growth = "5-8%"
        market_outlook = "Cautious Market Conditions"
        recommendation = "Focus on defensive investments"

    # Expected salary next year
    expected_salary = current_salary * (1 + (avg_forecast_4q * 0.015))  # GDP correlation factor

    st.markdown(f"""
    **📊 GDP Impact Analysis:**
    - 💼 **Expected Salary Growth:** {salary_growth} (GDP correlation factor)
    - 💰 **Your Salary Next Year:** ₹{expected_salary:,.0f}
    - 📈 **Market Outlook:** {market_outlook}
    - 🎯 **Investment Recommendation:** {recommendation}
    
    **📚 Historical Context:**
    - GDP above 7%: Historically best for job market and equity returns
    - GDP 6-7%: Moderate growth, balanced approach works
    - GDP below 6%: Focus on stability and defensive assets
    """)

    # -------------------------------
    # 8️⃣ Interactive Chart
    # -------------------------------
    st.subheader("📈 GDP Growth: Historical & Forecast")
    
    fig = go.Figure()

    # Historical GDP
    fig.add_trace(go.Scatter(
        x=df_prophet['ds'], y=df_prophet['y'],
        mode='lines+markers', name='Historical GDP Growth',
        line=dict(color='#1f77b4', width=2),
        marker=dict(size=6)
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
        mode='lines+markers', name='GDP Forecast',
        line=dict(color='#d62728', width=3),
        marker=dict(size=5)
    ))

    # Confidence interval
    fig.add_trace(go.Scatter(
        x=list(forecast_data['ds']) + list(forecast_data['ds'][::-1]),
        y=list(forecast_data['yhat_lower']) + list(forecast_data['yhat_upper'][::-1]),
        fill='toself', fillcolor='rgba(214,39,40,0.15)',
        line=dict(color='rgba(255,255,255,0)'),
        hoverinfo="skip", showlegend=True, name='Forecast Confidence'
    ))

    # Add reference lines
    fig.add_hline(y=7.0, line_dash="dot", line_color="green", 
                  annotation_text="Strong Growth (7%+)")
    fig.add_hline(y=6.0, line_dash="dot", line_color="orange", 
                  annotation_text="Moderate Growth (6%)")

    fig.update_layout(
        title=dict(text='🇮🇳 India GDP Growth Rate: Historical & Forecast', x=0.5, xanchor='center'),
        xaxis_title='Quarter',
        yaxis_title='GDP Growth Rate (%)',
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
    # 9️⃣ Forecast Table
    # -------------------------------
    st.subheader("📅 GDP Growth Forecast (Next 4 Quarters)")
    forecast_4q = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(4)
    forecast_4q = forecast_4q.rename(columns={
        'ds': 'Quarter',
        'yhat': 'Predicted Growth (%)',
        'yhat_lower': 'Lower Bound (%)',
        'yhat_upper': 'Upper Bound (%)'
    })

    st.dataframe(
        forecast_4q.style.format({
            'Predicted Growth (%)': "{:.1f}%",
            'Lower Bound (%)': "{:.1f}%",
            'Upper Bound (%)': "{:.1f}%"
        })
    )

else:
    st.info("Please add GDP data to continue. See instructions below.")
    
    st.markdown("""
    ### 📋 Required Data Format for GDP Analysis
    
    Create a file `data/gdp_data.xlsx` with columns:
    - **Date**: Quarter dates (e.g., 2020-01-01, 2020-04-01, etc.)
    - **GDP_Growth_Rate**: Quarterly GDP growth rate in percentage
    
    **Data Sources:**
    - RBI Database on Indian Economy (DBIE)
    - Ministry of Statistics and Programme Implementation (MOSPI)
    - National Statistical Office (NSO)
    """)