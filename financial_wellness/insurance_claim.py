import re
import streamlit as st
import PyPDF2
from PIL import Image
import pytesseract
import cohere
import os
from dotenv import load_dotenv
from fpdf import FPDF
from datetime import datetime
import pandas as pd
from prophet import Prophet
from io import BytesIO

load_dotenv()

# Load Cohere API
co = cohere.Client(os.getenv("COHERE_API_KEY"))

# ------------------ Streamlit Page Setup ------------------
st.set_page_config(page_title="Insurance Claim Assistant (Multi-Agent)", layout="centered")
st.title("Smart Insurance Assistant")

if "user_inputs" not in st.session_state:
    st.session_state.user_inputs = {}

# ------------------ Upload Section ------------------
st.header("Upload Your Claim Document")
uploaded_files = st.file_uploader(
    "Upload one or more claim documents",
    type=["pdf", "png", "jpg", "jpeg"],
    accept_multiple_files=True
)

# Initialize session_state for extracted text and results
if "extracted_text" not in st.session_state:
    st.session_state.extracted_text = ""
if "doc_summary" not in st.session_state:
    st.session_state.doc_summary = ""
if "coverages" not in st.session_state:
    st.session_state.coverages = {}

# ------------------ Extract Text from Uploaded Files ------------------

import pytesseract

# 👇 Set this to your Tesseract installation path
# Example for Windows: r"C:\Program Files\Tesseract-OCR\tesseract.exe"
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# ------------------ Extract Text from Uploaded Files ------------------
if uploaded_files and not st.session_state.extracted_text:
    for file in uploaded_files:
        # Get file extension in lowercase
        file_ext = file.name.split('.')[-1].lower()
        
        try:
            if file_ext == "pdf":
                # PDF extraction
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    st.session_state.extracted_text += page.extract_text() or ""
            
            elif file_ext in ["png", "jpg", "jpeg"]:
                # Image OCR
                image = Image.open(file).convert('RGB')  # ensures compatibility
                text = pytesseract.image_to_string(image)
                st.session_state.extracted_text += text
            
            else:
                st.warning(f"Unsupported file type: {file_ext}")

        except Exception as e:
            st.error(f"Failed to process {file.name}: {e}")


# Display extracted text
if st.session_state.extracted_text:
    st.success("✅ Text extracted from all uploaded documents.")
    st.text_area("🧾 Combined Extracted Text", st.session_state.extracted_text, height=200)

# ------------------ Cohere NLP Analysis ------------------
if st.session_state.extracted_text and not st.session_state.doc_summary:
    with st.spinner("🔍 Analyzing document details..."):
        prompt = f"""
        
Extract all key numeric details from the insurance document below. 
- Include any numbers related to policy coverage, individual coverage, premiums, taxes, start/end dates, or sums insured.
- Convert all amounts to **exact numbers in rupees** with commas.
- Output as bullet points with descriptive names based on context, even if the text uses different words.
- Skip fields that are not present. Example format:

- Policy Number: 30209660201200
- Plan Name: Family First Silver
- Sum Insured: ₹5,000,000
- Individual Cover: ₹2,500,000
- Premium: ₹45,897
- Taxes: ₹5,108
- Start Date: 03/04/2021
- End Date: 04/04/2022


Combined Document Text:
{st.session_state.extracted_text}
        """
        try:
            response = co.generate(model="command", prompt=prompt, max_tokens=500)
            st.session_state.doc_summary = response.generations[0].text.strip()
        except Exception as e:
            st.error(f"❌ Analysis failed: {e}")

# Display document summary
if st.session_state.doc_summary:
    st.info("📄 Document Summary:")
    st.write(st.session_state.doc_summary)

    # ------------------ Parse Cohere bullet-point summary ------------------
    coverages = {}
    for line in st.session_state.doc_summary.split('\n'):
        if ':' in line:
            key, val = line.split(':', 1)
            key, val = key.strip(), val.strip()
            # Remove ₹, commas for numeric conversion
            if '₹' in val:
                try:
                    val_numeric = float(val.replace('₹', '').replace(',', '').strip())
                except:
                    val_numeric = val
            else:
                val_numeric = val
            coverages[key] = val_numeric

    st.session_state.coverages = coverages

# Display extracted coverages
coverages = st.session_state.coverages
if coverages:
    st.write("🧾 Parsed Coverage Dictionary:")
    st.write(coverages)

# ------------------ Prophet Inflation Forecast ------------------
@st.cache_data
def load_forecast():
    df_all = pd.read_excel("data/df_all.xlsx", parse_dates=['Month'])
    df_prophet = df_all[['Month', 'Combined Inflation (%)']].copy()
    df_prophet['y'] = pd.to_numeric(df_prophet['Combined Inflation (%)'], errors='coerce').ffill()
    df_prophet = df_prophet.rename(columns={'Month': 'ds'})

    model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=False,
        daily_seasonality=False,
        seasonality_mode='multiplicative'
    )
    model.add_seasonality(name='monthly', period=12, fourier_order=8)
    model.fit(df_prophet)

    future = model.make_future_dataframe(periods=60, freq='MS')
    forecast = model.predict(future)
    return forecast

forecast = load_forecast()

def get_avg_inflation(current_year, future_year):
    mask = (forecast['ds'].dt.year > current_year) & (forecast['ds'].dt.year <= future_year)
    relevant = forecast.loc[mask, 'yhat']
    return relevant.mean() if len(relevant) > 0 else 0

def calculate_future_coverage(current_amount, current_year, future_year):
    avg_inflation = get_avg_inflation(current_year, future_year)
    future_value = current_amount * ((1 + avg_inflation / 100) ** (future_year - current_year))
    return round(future_value, 2)

# ------------------ Future Coverage Section ------------------
years_ahead = st.slider("Years Ahead for Coverage Forecast", min_value=1, max_value=10, value=5)
current_year = datetime.now().year

if coverages:
    future_suggestions = {}
    for cov_type, amount in coverages.items():
        # Only calculate numeric fields
        if isinstance(amount, (int, float)):
            future_val = calculate_future_coverage(amount, current_year, current_year + years_ahead)
            future_suggestions[cov_type] = {
                "Current Coverage": f"₹{amount:,.2f}",
                f"Coverage in {years_ahead} years": f"₹{future_val:,.2f}",
                "Message": f"Your ₹{amount:,.0f} {cov_type} today may be worth only ₹{future_val:,.2f} in {years_ahead} years."
            }

    st.subheader("📊 Future Coverage Suggestions")
    st.table(pd.DataFrame(future_suggestions).T)
else:
    st.info("No coverage amounts found in the document.")
