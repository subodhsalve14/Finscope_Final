# 📊 Economic Trend Analyzer

A comprehensive economic forecasting dashboard for personal finance decisions using real Indian economic data.

## 🚀 Features

- **📈 Inflation Forecast**: Historical analysis and 12-month predictions
- **📊 GDP Growth Forecast**: Quarterly GDP trends and job market insights  
- **💰 Interest Rates Forecast**: Multiple rate types with EMI impact calculator

## 🏃‍♂️ Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the main dashboard
streamlit run main_dashboard.py
```

## 📁 Project Structure

```
financial_wellness/
├── main_dashboard.py              # Main navigation hub
├── pages/                         # Individual dashboard pages
│   ├── 1_📈_Inflation_Forecast.py
│   ├── 2_📊_GDP_Forecast.py
│   └── 3_💰_Interest_Rates_Forecast.py
├── data/                          # Economic datasets
│   ├── df_all.xlsx               # Inflation data
│   ├── india_quarterly_gdp_2015-2024_fiscal_qoy.csv  # Raw GDP data
│   ├── INDIRLTLT01STM.csv        # Raw interest rates data
│   ├── gdp_data.xlsx             # Processed GDP data
│   └── interest_rates_data.xlsx  # Processed interest rates data
├── process_real_data.py          # Data processing script
└── requirements.txt              # Python dependencies
```

## 📊 Data Sources

- **GDP Data**: India quarterly GDP growth (2015-2025)
- **Interest Rates**: Long-term interest rates (2011-2025)  
- **Inflation Data**: Combined inflation indicators

## 🔄 Updating Data

To update with new economic data:

```bash
# Replace raw data files in data/ folder
# Then run the processing script
python process_real_data.py
```

## 🎯 Key Features

- **Prophet ML Models**: Advanced time-series forecasting
- **Personal Impact Analysis**: Salary predictions, EMI calculators
- **Interactive Charts**: Plotly visualizations with confidence intervals
- **Real-time Insights**: Current economic snapshot and trends

---

*All forecasts are for educational purposes. Please consult financial advisors for investment decisions.*