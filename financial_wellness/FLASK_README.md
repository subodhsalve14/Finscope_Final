# Flask Financial Advisor - Setup Instructions

## Overview
This is a Flask-based Financial Advisory Tool that provides comprehensive financial planning analysis, including insurance coverage assessment, premium affordability, and personalized recommendations.

## Features
- 📊 Coverage adequacy analysis
- 💳 Premium affordability assessment
- 🔒 Rider analysis (Critical Illness, Accident Cover)
- 📈 Financial health scoring
- 💡 Personalized recommendations
- 📄 Detailed financial report generation
- 🎯 Future planning with inflation impact

## Installation

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Flask Application**
   ```bash
   python flask_app.py
   ```

3. **Access the Application**
   Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

## Project Structure

```
financial_wellness/
│
├── flask_app.py              # Main Flask application
├── templates/
│   └── financial_advisor.html # HTML template
├── static/
│   ├── css/
│   │   └── style.css         # Styling
│   └── js/
│       └── script.js         # JavaScript for interactivity
├── requirements.txt          # Python dependencies
└── FLASK_README.md          # This file
```

## Usage

1. **Fill in Client Information**
   - Personal details (age, marital status, dependents)
   - Financial information (income, expenses)
   - Current insurance details
   - Riders and debts
   - Inflation assumptions

2. **Click "Analyze"**
   - The system will calculate comprehensive financial metrics
   - View coverage analysis, premium affordability, and scores

3. **Generate Detailed Report**
   - Click "Generate Detailed Summary Report" for a comprehensive analysis
   - Download the report as a Markdown file

## API Endpoints

### POST /analyze
Analyzes financial data and returns comprehensive metrics.

**Request Body:**
```json
{
  "age": 32,
  "marital_status": "Married",
  "dependents": 2,
  "annual_income": 800000,
  "monthly_expenses": 40000,
  "current_coverage": 5000000,
  "annual_premium": 25000,
  "accident_cover": 1000000,
  "critical_illness": 500000,
  "home_loan": 2000000,
  "other_debts": 0,
  "inflation_rate": 6.5
}
```

**Response:**
```json
{
  "success": true,
  "analysis": {
    "coverage_gap": 0,
    "is_underinsured": false,
    "overall_score": 7.5,
    "recommendations": ["..."],
    ...
  }
}
```

### POST /generate-report
Generates a detailed financial advisory report.

**Request Body:** Same as /analyze

**Response:**
```json
{
  "success": true,
  "report": "## FINANCIAL ADVISORY ANALYSIS REPORT\n..."
}
```

## Technologies Used
- **Backend:** Flask (Python)
- **Frontend:** HTML5, CSS3, JavaScript
- **Styling:** Custom CSS with gradients and animations
- **Data Processing:** Pandas, NumPy

## Key Calculations

1. **Recommended Coverage:** 10-15x annual income
2. **Premium Affordability:** Maximum 10% of annual income
3. **Critical Illness Cover:** 3x annual income
4. **Financial Health Score:** Composite of coverage, premium, debt, and savings scores

## Notes
- All currency values are in Indian Rupees (₹)
- Analysis based on standard financial planning principles
- Consult a certified financial planner for personalized advice

## Switching from Streamlit to Flask

The original application was built with Streamlit. This Flask version provides:
- ✅ More control over UI/UX
- ✅ RESTful API endpoints
- ✅ Better integration possibilities
- ✅ Production-ready deployment options
- ✅ Custom styling and branding

## Deployment Options

### Local Development
```bash
python flask_app.py
```

### Production (with Gunicorn)
```bash
pip install gunicorn
gunicorn -w 4 flask_app:app
```

### Production (with environment variables)
```bash
export FLASK_ENV=production
export FLASK_DEBUG=False
python flask_app.py
```

## Browser Compatibility
- Chrome (recommended)
- Firefox
- Edge
- Safari

## Support
For issues or questions, please refer to the main project documentation.
