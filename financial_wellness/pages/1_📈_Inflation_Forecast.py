# This is a copy of app.py for the multipage app structure
import streamlit as st
import pandas as pd
from prophet import Prophet
import plotly.graph_objects as go

# -------------------------------
# 1️⃣ App title
# -------------------------------
st.set_page_config(page_title="Inflation Forecast Dashboard", layout="wide")
st.title("📊 Inflation Forecast Dashboard")

# -------------------------------
# 2️⃣ Load Data
# -------------------------------
df_all = pd.read_excel("data/df_all.xlsx", parse_dates=['Month'])

# -------------------------------
# 3️⃣ Prepare data for Prophet
# -------------------------------
df_prophet = df_all[['Month', 'Combined Inflation (%)']].copy()
df_prophet['y'] = pd.to_numeric(df_prophet['Combined Inflation (%)'], errors='coerce')
df_prophet['y'] = df_prophet['y'].ffill()
df_prophet = df_prophet.rename(columns={'Month': 'ds'})

# -------------------------------
# 4️⃣ Initialize Prophet
# -------------------------------
model = Prophet(
    yearly_seasonality=True,
    weekly_seasonality=False,
    daily_seasonality=False,
    changepoint_prior_scale=1.0,
    seasonality_mode='multiplicative'
)
model.add_seasonality(name='monthly', period=12, fourier_order=8)
model.fit(df_prophet)

# -------------------------------
# 5️⃣ Forecast next 12 months
# -------------------------------
future = model.make_future_dataframe(periods=12, freq='MS')
forecast = model.predict(future)
df_prophet['Fitted'] = forecast.loc[:len(df_prophet)-1, 'yhat']

# -------------------------------
# 6️⃣ Interactive Plotly Chart
# -------------------------------
fig = go.Figure()

# Actual
fig.add_trace(go.Scatter(
    x=df_prophet['ds'], y=df_prophet['y'],
    mode='lines+markers', name='Actual',
    line=dict(color='#1f77b4', width=2),
    marker=dict(size=6)
))

# Fitted
fig.add_trace(go.Scatter(
    x=df_prophet['ds'], y=df_prophet['Fitted'],
    mode='lines', name='Fitted (Prophet)',
    line=dict(color='#2ca02c', dash='dash', width=2)
))

# Forecast
fig.add_trace(go.Scatter(
    x=forecast['ds'], y=forecast['yhat'],
    mode='lines+markers', name='Forecast (Prophet)',
    line=dict(color='#d62728', width=3),
    marker=dict(size=5)
))

# Confidence interval
fig.add_trace(go.Scatter(
    x=list(forecast['ds']) + list(forecast['ds'][::-1]),
    y=list(forecast['yhat_lower']) + list(forecast['yhat_upper'][::-1]),
    fill='toself', fillcolor='rgba(214,39,40,0.15)',
    line=dict(color='rgba(255,255,255,0)'),
    hoverinfo="skip", showlegend=True, name='Forecast CI'
))

# Layout styling
fig.update_layout(
    title=dict(text='📈 Combined Inflation: Actual, Fitted & Forecast', x=0.5, xanchor='center'),
    xaxis_title='Month',
    yaxis_title='Combined Inflation (%)',
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
# 7️⃣ Forecasted values next 12 months
# -------------------------------
st.subheader("📅 Forecasted Combined Inflation for Next 12 Months")
forecast_12m = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(12)
forecast_12m = forecast_12m.rename(columns={
    'ds': 'Month',
    'yhat': 'Predicted',
    'yhat_lower': 'Lower CI',
    'yhat_upper': 'Upper CI'
})

st.dataframe(
    forecast_12m.style.format({
        'Predicted': "{:.2f}%",
        'Lower CI': "{:.2f}%",
        'Upper CI': "{:.2f}%"
    })
)