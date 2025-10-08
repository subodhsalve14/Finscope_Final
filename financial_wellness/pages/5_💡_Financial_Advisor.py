import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Financial Advisory Tool",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.3rem;
        font-weight: bold;
        color: #2e7d32;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
        border-bottom: 2px solid #2e7d32;
        padding-bottom: 5px;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .recommendation {
        background-color: #e8f5e8;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #4caf50;
        margin: 0.5rem 0;
    }
    .warning {
        background-color: #fff3e0;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ff9800;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Main title
st.markdown('<div class="main-header">💰 Financial Advisory Tool</div>', unsafe_allow_html=True)

# Sidebar for inputs
with st.sidebar:
    st.header("📝 Client Information")
    
    # Personal Details
    st.subheader("Personal Details")
    age = st.slider("Age", 22, 65, 32)
    marital_status = st.selectbox("Marital Status", ["Single", "Married"])
    dependents = st.number_input("Number of Dependents", 0, 10, 2)
    
    # Financial Details
    st.subheader("Financial Information")
    annual_income = st.number_input("Annual Income (₹)", 100000, 10000000, 800000, step=50000)
    monthly_expenses = st.number_input("Monthly Expenses (₹)", 10000, 500000, 40000, step=5000)
    
    # Current Insurance
    st.subheader("Current Insurance")
    current_coverage = st.number_input("Current Life Insurance Coverage (₹)", 0, 50000000, 5000000, step=500000)
    annual_premium = st.number_input("Annual Premium (₹)", 0, 500000, 25000, step=5000)
    
    # Riders
    st.subheader("Riders")
    accident_cover = st.number_input("Accident Death Benefit (₹)", 0, 20000000, 1000000, step=100000)
    critical_illness = st.number_input("Critical Illness Cover (₹)", 0, 10000000, 500000, step=100000)
    
    # Debts
    st.subheader("Outstanding Debts")
    home_loan = st.number_input("Home Loan Outstanding (₹)", 0, 50000000, 2000000, step=100000)
    other_debts = st.number_input("Other Debts (₹)", 0, 10000000, 0, step=50000)
    
    # Assumptions
    st.subheader("Assumptions")
    inflation_rate = st.slider("Expected Inflation Rate (%)", 3.0, 10.0, 6.5, 0.5)

# Function to calculate analysis
def calculate_analysis():
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
        'recommended_ci': recommended_ci
    }

# Calculate analysis
analysis = calculate_analysis()

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    # Coverage Analysis
    st.markdown('<div class="section-header">🛡️ Coverage Analysis</div>', unsafe_allow_html=True)
    
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.metric("Current Coverage", f"₹{current_coverage:,.0f}", f"{current_coverage/annual_income:.1f}x income")
    with col_b:
        st.metric("Recommended Min", f"₹{analysis['recommended_min']:,.0f}", "10x income")
    with col_c:
        st.metric("Coverage Gap", f"₹{analysis['coverage_gap']:,.0f}", 
                 "⚠️ Underinsured" if analysis['is_underinsured'] else "✅ Adequate")
    
    if analysis['is_underinsured']:
        st.markdown(f'''
        <div class="warning">
        <strong>⚠️ Coverage Gap Alert:</strong><br>
        You are underinsured by ₹{analysis['coverage_gap']:,.0f}. Consider increasing your coverage to protect your family's financial future.
        </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown(f'''
        <div class="recommendation">
        <strong>✅ Coverage Status:</strong><br>
        Your current coverage is adequate based on the 10x income rule.
        </div>
        ''', unsafe_allow_html=True)

    # Premium Analysis
    st.markdown('<div class="section-header">💳 Premium Analysis</div>', unsafe_allow_html=True)
    
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.metric("Current Premium", f"₹{annual_premium:,.0f}", f"{analysis['premium_percentage']:.1f}% of income")
    with col_b:
        st.metric("Max Affordable", f"₹{annual_income * 0.1:,.0f}", "10% of income")
    with col_c:
        st.metric("Additional Capacity", f"₹{analysis['additional_premium_capacity']:,.0f}")
    
    affordability_status = "Highly Affordable" if analysis['premium_percentage'] < 5 else "Affordable" if analysis['premium_percentage'] < 10 else "High"
    
    st.markdown(f'''
    <div class="metric-card">
    <strong>Premium Affordability:</strong> {affordability_status}<br>
    You can afford an additional ₹{analysis['additional_premium_capacity']:,.0f} in annual premiums for enhanced coverage.
    </div>
    ''', unsafe_allow_html=True)

    # Rider Analysis
    st.markdown('<div class="section-header">🔒 Rider Analysis</div>', unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("Critical Illness (Current)", f"₹{critical_illness:,.0f}")
        st.metric("Accident Cover (Current)", f"₹{accident_cover:,.0f}")
    with col_b:
        st.metric("Critical Illness (Recommended)", f"₹{analysis['recommended_ci']:,.0f}", "3x income")
        ci_gap = max(0, analysis['recommended_ci'] - critical_illness)
        st.metric("CI Coverage Gap", f"₹{ci_gap:,.0f}")

with col2:
    # Financial Health Score
    st.markdown('<div class="section-header">📊 Financial Health</div>', unsafe_allow_html=True)
    
    # Calculate scores
    coverage_score = min(10, (current_coverage / analysis['recommended_min']) * 10)
    premium_score = 10 if analysis['premium_percentage'] < 5 else 8 if analysis['premium_percentage'] < 10 else 5
    debt_score = 10 if analysis['total_debts'] < annual_income else 7 if analysis['total_debts'] < annual_income * 2 else 4
    savings_score = 10 if analysis['net_savings'] > annual_income * 0.3 else 7 if analysis['net_savings'] > annual_income * 0.2 else 4
    
    overall_score = (coverage_score + premium_score + debt_score + savings_score) / 4
    
    st.metric("Coverage Score", f"{coverage_score:.1f}/10")
    st.metric("Premium Score", f"{premium_score:.1f}/10")
    st.metric("Debt Management", f"{debt_score:.1f}/10")
    st.metric("Savings Rate", f"{savings_score:.1f}/10")
    st.metric("Overall Score", f"{overall_score:.1f}/10", 
             "Excellent" if overall_score >= 8 else "Good" if overall_score >= 6 else "Needs Improvement")
    
    # Quick Stats
    st.markdown('<div class="section-header">📈 Key Metrics</div>', unsafe_allow_html=True)
    
    savings_rate = (analysis['net_savings'] / annual_income * 100) if annual_income > 0 else 0
    debt_to_income = (analysis['total_debts'] / annual_income) if annual_income > 0 else 0
    
    st.metric("Monthly Savings", f"₹{analysis['net_savings']/12:,.0f}")
    st.metric("Savings Rate", f"{savings_rate:.1f}%")
    st.metric("Debt-to-Income", f"{debt_to_income:.1f}x")

# Recommendations Section
st.markdown('<div class="section-header">💡 Personalized Recommendations</div>', unsafe_allow_html=True)

recommendations = []

if analysis['is_underinsured']:
    recommendations.append(f"🎯 **Increase Life Insurance Coverage** to ₹{analysis['recommended_min']:,.0f} (minimum) to adequately protect your family.")

if critical_illness < analysis['recommended_ci']:
    recommendations.append(f"🏥 **Enhance Critical Illness Cover** to ₹{analysis['recommended_ci']:,.0f} (3x your annual income).")

if analysis['net_savings'] < annual_income * 0.2:
    recommendations.append("💰 **Improve Savings Rate** - Aim to save at least 20% of your income for long-term financial security.")

if analysis['total_debts'] > annual_income * 2:
    recommendations.append("📉 **Debt Management** - Your debt-to-income ratio is high. Consider debt consolidation or prepayment strategies.")

recommendations.append("📊 **Build Emergency Fund** - Maintain 6 months of expenses as emergency fund.")
recommendations.append("🔄 **Review Annually** - Review and adjust your insurance coverage every year to account for inflation and life changes.")

for i, rec in enumerate(recommendations, 1):
    st.markdown(f'''
    <div class="recommendation">
    <strong>{i}.</strong> {rec}
    </div>
    ''', unsafe_allow_html=True)

# Inflation Impact
st.markdown('<div class="section-header">📈 Future Planning</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.subheader("Inflation Impact (10 years)")
    st.metric("Current Annual Expenses", f"₹{analysis['annual_expenses']:,.0f}")
    st.metric("Future Annual Expenses", f"₹{analysis['future_expenses_10y']:,.0f}", 
             f"+{((analysis['future_expenses_10y']/analysis['annual_expenses'] - 1) * 100):.1f}%")

with col2:
    st.subheader("Action Timeline")
    st.markdown("""
    **Next 30 Days:**
    - Review and increase life insurance coverage
    - Start building emergency fund
    
    **Next 3 Months:**
    - Enhance critical illness cover
    - Optimize debt repayment strategy
    
    **Next 6 Months:**
    - Set up systematic investments
    - Annual insurance review process
    """)

# Footer
st.markdown("---")
st.markdown("*This analysis is based on standard financial planning principles. Please consult a certified financial planner for personalized advice.*")

# Function to generate rule-based analysis (from test.py)
def generate_detailed_analysis(annual_income, monthly_expenses, current_coverage, annual_premium, 
                              home_loan, age, dependents, critical_illness, accident_cover, inflation_rate):
    """Generate detailed analysis using financial rules from test.py"""
    
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

# Generate Summary Report button
if st.button("📄 Generate Detailed Summary Report", type="primary"):
    with st.spinner("Generating comprehensive financial analysis..."):
        # Generate detailed analysis using the test.py logic
        detailed_report = generate_detailed_analysis(
            annual_income=annual_income,
            monthly_expenses=monthly_expenses,
            current_coverage=current_coverage,
            annual_premium=annual_premium,
            home_loan=home_loan,
            age=age,
            dependents=dependents,
            critical_illness=critical_illness,
            accident_cover=accident_cover,
            inflation_rate=inflation_rate
        )
        
        # Display the detailed report
        st.markdown("---")
        st.markdown(detailed_report)
        
        # Add download option
        st.download_button(
            label="📥 Download Report as Text",
            data=detailed_report,
            file_name=f"financial_analysis_report_{age}yr.md",
            mime="text/markdown"
        )