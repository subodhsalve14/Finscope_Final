from flask import Flask, render_template, request, jsonify
import pandas as pd
from datetime import datetime
from prophet import Prophet
import plotly.graph_objects as go
import plotly
import json
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # ✅ fixes browser “Failed to fetch” due to CORS


app = Flask(__name__)

# Main route - Home page with cards
@app.route('/')
def index():
    return render_template('index.html')

# Financial Advisor route
@app.route('/financial-advisor')
def financial_advisor():
    return render_template('financial_advisor.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Process financial advisor analysis"""
    try:
        # Get form data
        data = request.get_json()
        
        age = int(data.get('age', 32))
        marital_status = data.get('marital_status', 'Single')
        dependents = int(data.get('dependents', 2))
        annual_income = float(data.get('annual_income', 800000))
        monthly_expenses = float(data.get('monthly_expenses', 40000))
        current_coverage = float(data.get('current_coverage', 5000000))
        annual_premium = float(data.get('annual_premium', 25000))
        accident_cover = float(data.get('accident_cover', 1000000))
        critical_illness = float(data.get('critical_illness', 500000))
        home_loan = float(data.get('home_loan', 2000000))
        other_debts = float(data.get('other_debts', 0))
        inflation_rate = float(data.get('inflation_rate', 6.5))
        
        # Perform calculations
        analysis = calculate_analysis(
            age, marital_status, dependents, annual_income, monthly_expenses,
            current_coverage, annual_premium, accident_cover, critical_illness,
            home_loan, other_debts, inflation_rate
        )
        
        return jsonify({
            'success': True,
            'analysis': analysis
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/generate-report', methods=['POST'])
def generate_report():
    """Generate detailed financial report"""
    try:
        data = request.get_json()
        
        annual_income = float(data.get('annual_income', 800000))
        monthly_expenses = float(data.get('monthly_expenses', 40000))
        current_coverage = float(data.get('current_coverage', 5000000))
        annual_premium = float(data.get('annual_premium', 25000))
        home_loan = float(data.get('home_loan', 2000000))
        age = int(data.get('age', 32))
        dependents = int(data.get('dependents', 2))
        critical_illness = float(data.get('critical_illness', 500000))
        accident_cover = float(data.get('accident_cover', 1000000))
        inflation_rate = float(data.get('inflation_rate', 6.5))
        
        report = generate_detailed_analysis(
            annual_income, monthly_expenses, current_coverage, annual_premium,
            home_loan, age, dependents, critical_illness, accident_cover, inflation_rate
        )
        
        return jsonify({
            'success': True,
            'report': report
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

def calculate_analysis(age, marital_status, dependents, annual_income, monthly_expenses,
                       current_coverage, annual_premium, accident_cover, critical_illness,
                       home_loan, other_debts, inflation_rate):
    """Calculate financial analysis metrics"""
    
    # Basic calculations
    annual_expenses = monthly_expenses * 12
    net_savings = annual_income - annual_expenses
    recommended_min = annual_income * 10
    recommended_max = annual_income * 15
    premium_percentage = (annual_premium / annual_income) * 100 if annual_income > 0 else 0
    total_debts = home_loan + other_debts
    
    # Coverage assessment
    coverage_gap = max(0, recommended_min - current_coverage)
    is_underinsured = coverage_gap > 0
    
    # Premium affordability
    max_affordable_premium = annual_income * 0.1  # 10% of income
    additional_premium_capacity = max_affordable_premium - annual_premium
    
    # Future expenses with inflation
    future_expenses_10y = annual_expenses * ((1 + inflation_rate/100) ** 10)
    
    # Recommended critical illness cover
    recommended_ci = annual_income * 3
    
    # Calculate scores
    coverage_score = min(10, (current_coverage / recommended_min) * 10)
    premium_score = 10 if premium_percentage < 5 else 8 if premium_percentage < 10 else 5
    debt_score = 10 if total_debts < annual_income else 7 if total_debts < annual_income * 2 else 4
    savings_score = 10 if net_savings > annual_income * 0.3 else 7 if net_savings > annual_income * 0.2 else 4
    overall_score = (coverage_score + premium_score + debt_score + savings_score) / 4
    
    # Savings and debt metrics
    savings_rate = (net_savings / annual_income * 100) if annual_income > 0 else 0
    debt_to_income = (total_debts / annual_income) if annual_income > 0 else 0
    
    # Affordability status
    affordability_status = "Highly Affordable" if premium_percentage < 5 else "Affordable" if premium_percentage < 10 else "High"
    
    # Critical illness gap
    ci_gap = max(0, recommended_ci - critical_illness)
    
    # Recommendations
    recommendations = []
    
    if is_underinsured:
        recommendations.append(f"🎯 **Increase Life Insurance Coverage** to ₹{recommended_min:,.0f} (minimum) to adequately protect your family.")
    
    if critical_illness < recommended_ci:
        recommendations.append(f"🏥 **Enhance Critical Illness Cover** to ₹{recommended_ci:,.0f} (3x your annual income).")
    
    if net_savings < annual_income * 0.2:
        recommendations.append("💰 **Improve Savings Rate** - Aim to save at least 20% of your income for long-term financial security.")
    
    if total_debts > annual_income * 2:
        recommendations.append("📉 **Debt Management** - Your debt-to-income ratio is high. Consider debt consolidation or prepayment strategies.")
    
    recommendations.append("📊 **Build Emergency Fund** - Maintain 6 months of expenses as emergency fund.")
    recommendations.append("🔄 **Review Annually** - Review and adjust your insurance coverage every year to account for inflation and life changes.")
    
    return {
        'annual_expenses': annual_expenses,
        'net_savings': net_savings,
        'recommended_min': recommended_min,
        'recommended_max': recommended_max,
        'premium_percentage': premium_percentage,
        'total_debts': total_debts,
        'coverage_gap': coverage_gap,
        'is_underinsured': is_underinsured,
        'additional_premium_capacity': additional_premium_capacity,
        'future_expenses_10y': future_expenses_10y,
        'recommended_ci': recommended_ci,
        'coverage_score': coverage_score,
        'premium_score': premium_score,
        'debt_score': debt_score,
        'savings_score': savings_score,
        'overall_score': overall_score,
        'savings_rate': savings_rate,
        'debt_to_income': debt_to_income,
        'affordability_status': affordability_status,
        'ci_gap': ci_gap,
        'recommendations': recommendations,
        'max_affordable_premium': max_affordable_premium
    }

def generate_detailed_analysis(annual_income, monthly_expenses, current_coverage, annual_premium, 
                              home_loan, age, dependents, critical_illness, accident_cover, inflation_rate):
    """Generate detailed analysis using financial rules"""
    
    # Calculations
    annual_expenses = monthly_expenses * 12
    recommended_min = annual_income * 10
    recommended_max = annual_income * 15
    premium_percentage = (annual_premium / annual_income) * 100
    
    # Coverage gap
    coverage_gap = max(0, recommended_min - current_coverage)
    
    # Future expenses with inflation
    inflation_decimal = inflation_rate / 100
    future_expenses_10y = annual_expenses * ((1 + inflation_decimal) ** 10)
    
    # Generate detailed report
    report = f"""
## 🏦 FINANCIAL ADVISORY ANALYSIS REPORT

### 1. COVERAGE ADEQUACY ASSESSMENT
---
**Current Coverage:** ₹{current_coverage:,} ({current_coverage/annual_income:.1f}x income)  
**Recommended Range:** ₹{recommended_min:,} - ₹{recommended_max:,} (10-15x income)  
**Assessment:** {"**⚠️ UNDERINSURED**" if coverage_gap > 0 else "**✅ ADEQUATE**"}  
**Coverage Gap:** ₹{coverage_gap:,}  
**Risk Factors:** Home loan ₹{home_loan:,} + {dependents} dependents  

{"🎯 **RECOMMENDATION:** Increase coverage by ₹" + f"{coverage_gap:,}" if coverage_gap > 0 else "✅ **STATUS:** Current coverage is adequate"}

### 2. PREMIUM AFFORDABILITY ANALYSIS
---
**Current Premium:** ₹{annual_premium:,} ({premium_percentage:.1f}% of income)  
**Affordability:** {"**Highly Affordable** 🟢" if premium_percentage < 5 else "**Affordable** 🟡" if premium_percentage < 10 else "**High** 🔴"}  
**Maximum Recommended:** ₹{annual_income * 0.1:,} (10% of income)  
**Additional Capacity:** ₹{(annual_income * 0.1) - annual_premium:,}  

💡 **RECOMMENDATION:** You can afford additional ₹{(annual_income * 0.1) - annual_premium:,} in premiums for more coverage

### 3. RIDER ANALYSIS
---
**Critical Illness Cover:** ₹{critical_illness:,} (Current)  
**Recommended CI Cover:** ₹{annual_income * 3:,} (3x income)  
**Accidental Death:** ₹{accident_cover:,} {"✅ (Adequate)" if accident_cover >= current_coverage * 2 else "⚠️ (Consider increasing)"}  

🏥 **RECOMMENDATION:** {"Increase Critical Illness cover to ₹" + f"{annual_income * 3:,}" if critical_illness < annual_income * 3 else "Critical illness coverage is adequate"}

### 4. INFLATION PROTECTION STRATEGY
---
**Current Annual Expenses:** ₹{annual_expenses:,}  
**Expenses in 10 years ({inflation_rate}% inflation):** ₹{future_expenses_10y:,}  
**Inflation Impact:** {((future_expenses_10y/annual_expenses - 1) * 100):.1f}% increase over 10 years  

📈 **STRATEGIES:**
- Increase coverage by 8-10% every 3 years
- Start SIP of ₹15,000/month in equity mutual funds
- Maximize PPF contribution (₹1.5L annually)
- Consider ULIP with top-up facility

### 5. IMMEDIATE ACTION PLAN
---
**🎯 Priority 1 (Next 30 days):**
- Increase term insurance to ₹{recommended_min:,}
- Build emergency fund: ₹{monthly_expenses * 6:,} (6 months expenses)

**📋 Priority 2 (Next 90 days):**
- Enhance Critical Illness cover to ₹{annual_income * 3:,}
- Start monthly SIP of ₹10,000 in diversified equity funds

**📅 Priority 3 (Next 6 months):**
- Review and optimize home loan prepayment strategy
- Set up automatic premium payments with annual increases

### 6. FINANCIAL HEALTH SCORE
---
"""
    
    # Calculate scores
    insurance_score = min(10, (current_coverage / recommended_min) * 10)
    premium_score = 9 if premium_percentage < 5 else 7 if premium_percentage < 10 else 4
    debt_score = 7 if home_loan < annual_income * 2 else 5 if home_loan < annual_income * 3 else 3
    overall_score = (insurance_score + premium_score + debt_score) / 3
    
    report += f"""
**Insurance Coverage:** {insurance_score:.1f}/10 {"(Underinsured)" if insurance_score < 8 else "(Good)" if insurance_score < 10 else "(Excellent)"}  
**Premium Affordability:** {premium_score:.1f}/10 {"(Highly affordable)" if premium_score >= 8 else "(Affordable)" if premium_score >= 6 else "(High)"}  
**Debt Management:** {debt_score:.1f}/10 {"(Manageable)" if debt_score >= 6 else "(Needs attention)"}  
**Overall Score:** {overall_score:.1f}/10 {"🟢 **Good foundation, needs enhancement**" if overall_score >= 6 else "🟡 **Needs improvement**"}

---
*This analysis is based on standard financial planning principles. Please consult a certified financial planner for personalized advice.*
"""
    
    return report

# Inflation Forecast route
@app.route('/inflation-forecast')
def inflation_forecast():
    return render_template('inflation_forecast.html')

@app.route('/api/inflation-data')
def get_inflation_data():
    """Get inflation forecast data"""
    try:
        df_all = pd.read_excel("data/df_all.xlsx", parse_dates=['Month'])
        
        # Prepare data for Prophet
        df_prophet = df_all[['Month', 'Combined Inflation (%)']].copy()
        df_prophet['y'] = pd.to_numeric(df_prophet['Combined Inflation (%)'], errors='coerce')
        df_prophet['y'] = df_prophet['y'].ffill()
        df_prophet = df_prophet.rename(columns={'Month': 'ds'})
        
        # Train model
        model = Prophet(
            yearly_seasonality=True,
            weekly_seasonality=False,
            daily_seasonality=False,
            changepoint_prior_scale=1.0,
            seasonality_mode='multiplicative'
        )
        model.add_seasonality(name='monthly', period=12, fourier_order=8)
        model.fit(df_prophet)
        
        # Forecast
        future = model.make_future_dataframe(periods=12, freq='MS')
        forecast = model.predict(future)
        
        # Create plot
        fig = go.Figure()
        
        # Historical data
        fig.add_trace(go.Scatter(
            x=df_prophet['ds'],
            y=df_prophet['y'],
            mode='lines',
            name='Historical Inflation',
            line=dict(color='blue', width=2)
        ))
        
        # Forecast
        forecast_future = forecast[len(df_prophet):]
        fig.add_trace(go.Scatter(
            x=forecast_future['ds'],
            y=forecast_future['yhat'],
            mode='lines',
            name='Forecast',
            line=dict(color='red', width=2, dash='dash')
        ))
        
        # Confidence interval
        fig.add_trace(go.Scatter(
            x=forecast_future['ds'],
            y=forecast_future['yhat_upper'],
            mode='lines',
            name='Upper Bound',
            line=dict(width=0),
            showlegend=False
        ))
        
        fig.add_trace(go.Scatter(
            x=forecast_future['ds'],
            y=forecast_future['yhat_lower'],
            mode='lines',
            name='Lower Bound',
            fill='tonexty',
            fillcolor='rgba(255,0,0,0.2)',
            line=dict(width=0),
            showlegend=False
        ))
        
        fig.update_layout(
            title='Inflation Forecast - Next 12 Months',
            xaxis_title='Date',
            yaxis_title='Inflation Rate (%)',
            hovermode='x unified',
            template='plotly_white'
        )
        
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        
        # Get summary stats
        latest_actual = df_prophet['y'].iloc[-1]
        avg_forecast = forecast_future['yhat'].mean()
        trend = "increasing" if avg_forecast > latest_actual else "decreasing"
        
        return jsonify({
            'success': True,
            'graph': graphJSON,
            'latest_actual': float(latest_actual),
            'avg_forecast': float(avg_forecast),
            'trend': trend,
            'forecast_data': forecast_future[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_dict('records')
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# GDP Forecast route
@app.route('/gdp-forecast')
def gdp_forecast():
    return render_template('gdp_forecast.html')

@app.route('/api/gdp-data')
def get_gdp_data():
    """Get GDP forecast data"""
    try:
        df_gdp = pd.read_excel("data/gdp_data.xlsx", parse_dates=['Date'])
        
        # Prepare data
        df_prophet = df_gdp[['Date', 'GDP_Growth_Rate']].copy()
        df_prophet['y'] = pd.to_numeric(df_prophet['GDP_Growth_Rate'], errors='coerce')
        df_prophet['y'] = df_prophet['y'].ffill()
        df_prophet = df_prophet.rename(columns={'Date': 'ds'})
        df_prophet = df_prophet.dropna()
        
        # Train model
        model = Prophet(
            yearly_seasonality=True,
            weekly_seasonality=False,
            daily_seasonality=False,
            changepoint_prior_scale=0.8,
            seasonality_mode='additive'
        )
        model.fit(df_prophet)
        
        # Forecast
        future = model.make_future_dataframe(periods=12, freq='MS')
        forecast = model.predict(future)
        
        # Create plot
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df_prophet['ds'],
            y=df_prophet['y'],
            mode='lines+markers',
            name='Historical GDP Growth',
            line=dict(color='green', width=2)
        ))
        
        forecast_future = forecast[len(df_prophet):]
        fig.add_trace(go.Scatter(
            x=forecast_future['ds'],
            y=forecast_future['yhat'],
            mode='lines',
            name='Forecast',
            line=dict(color='orange', width=2, dash='dash')
        ))
        
        fig.update_layout(
            title='GDP Growth Forecast',
            xaxis_title='Date',
            yaxis_title='GDP Growth Rate (%)',
            hovermode='x unified',
            template='plotly_white'
        )
        
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        
        latest_actual = df_prophet['y'].iloc[-1]
        avg_forecast = forecast_future['yhat'].mean()
        
        return jsonify({
            'success': True,
            'graph': graphJSON,
            'latest_actual': float(latest_actual),
            'avg_forecast': float(avg_forecast),
            'forecast_data': forecast_future[['ds', 'yhat']].to_dict('records')
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# Interest Rates Forecast route
@app.route('/interest-rates-forecast')
def interest_rates_forecast():
    return render_template('interest_rates_forecast.html')

@app.route('/api/interest-rates-data')
def get_interest_rates_data():
    """Get interest rates forecast data"""
    try:
        rate_type = request.args.get('rate_type', 'Repo_Rate')
        
        df_rates = pd.read_excel("data/interest_rates_data.xlsx", parse_dates=['Date'])
        
        # Prepare data
        df_prophet = df_rates[['Date', rate_type]].copy()
        df_prophet['y'] = pd.to_numeric(df_prophet[rate_type], errors='coerce')
        df_prophet['y'] = df_prophet['y'].ffill()
        df_prophet = df_prophet.rename(columns={'Date': 'ds'})
        df_prophet = df_prophet.dropna()
        
        # Train model
        model = Prophet(
            yearly_seasonality=True,
            weekly_seasonality=False,
            daily_seasonality=False,
            changepoint_prior_scale=0.5,
            seasonality_mode='additive'
        )
        model.fit(df_prophet)
        
        # Forecast
        future = model.make_future_dataframe(periods=12, freq='MS')
        forecast = model.predict(future)
        
        # Create plot
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df_prophet['ds'],
            y=df_prophet['y'],
            mode='lines',
            name=f'Historical {rate_type}',
            line=dict(color='purple', width=2)
        ))
        
        forecast_future = forecast[len(df_prophet):]
        fig.add_trace(go.Scatter(
            x=forecast_future['ds'],
            y=forecast_future['yhat'],
            mode='lines',
            name='Forecast',
            line=dict(color='red', width=2, dash='dash')
        ))
        
        fig.update_layout(
            title=f'{rate_type} Forecast',
            xaxis_title='Date',
            yaxis_title='Rate (%)',
            hovermode='x unified',
            template='plotly_white'
        )
        
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        
        latest_actual = df_prophet['y'].iloc[-1]
        avg_forecast = forecast_future['yhat'].mean()
        
        return jsonify({
            'success': True,
            'graph': graphJSON,
            'latest_actual': float(latest_actual),
            'avg_forecast': float(avg_forecast),
            'forecast_data': forecast_future[['ds', 'yhat']].to_dict('records')
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# Policy Recommendations route
@app.route('/policy-recommendations')
def policy_recommendations():
    return render_template('policy_recommendations.html')

@app.route('/api/policy-recommend', methods=['POST'])
def get_policy_recommendation():
    """Get policy recommendations based on user profile"""
    try:
        from risk_assesment import calculate_risk_score
        from search_serp import get_policy_recommendations_from_serpapi
        from utils import build_prompt_with_search
        from gemini_llm import query_gemini

        data = request.get_json()

        # Extract data safely
        age = int(data.get('age', 30))
        gender = data.get('gender', 'Male')
        occupation = data.get('occupation', 'Employee')
        income = float(data.get('income', 500000))
        smoker = data.get('smoker', 'No')
        driving_record = data.get('driving_record', 'Clean')
        policy_type = data.get('policy_type', 'Health Insurance')
        disease = data.get('disease', 'None')

        # 1️⃣ Calculate risk score
        risk_score = calculate_risk_score(age, income, driving_record, smoker)

        # 2️⃣ Build user profile dictionary
        user_profile = {
            "Age": age,
            "Gender": gender,
            "Occupation": occupation,
            "Income Level": income,
            "Insurance Type": policy_type,
            "Smoker": smoker,
            "Driving Record": driving_record,
            "Risk Score": risk_score,
            "Pre-existing Condition": disease,
        }

        # 3️⃣ Get real policy recommendations (SERP API)
        search_results = get_policy_recommendations_from_serpapi(user_profile)
        if not search_results:
            search_results = [{"title": "No results found", "link": "", "snippet": ""}]

        # 4️⃣ Build Gemini prompt using search results
        prompt = build_prompt_with_search(user_profile, search_results)

        # 5️⃣ Query Gemini for insights
        recommendation = query_gemini(prompt)

        risk_category = calculate_risk_score(age, income, driving_record, smoker)
        # 6️⃣ Return JSON response
        return jsonify({
    'success': True,
    'risk_category': risk_category,  # e.g., "🔴 High Risk"
    'recommendation': recommendation
}), 200
    except Exception as e:
        print("Error in /api/policy-recommend:", str(e))

        # Fallback response
        return jsonify({
            'success': False,
            'error': str(e),
            'recommendation': f"""
## Policy Recommendations (Fallback)

### Risk Summary
- Age: {data.get('age', 30)}
- Income: ₹{data.get('income', 500000)}
- Smoker: {data.get('smoker', 'No')}
- Driving Record: {data.get('driving_record', 'Clean')}
- Risk Score: Medium (Fallback)

### Suggested Coverage
- Coverage: ₹{int(float(data.get('income', 500000))) * 10:,}
- Term: 20–30 years
- Premium: ₹{int(float(data.get('income', 500000))) * 0.05:,}/year

> *Note: This is an auto-generated fallback suggestion. Please try again for personalized insights.*
"""
        }), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
