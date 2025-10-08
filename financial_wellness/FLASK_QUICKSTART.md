# 🚀 Quick Start Guide - Flask Financial Advisor

## Running the Application

### Method 1: Using Batch File (Easiest)
Simply double-click the `run_flask.bat` file in the project folder.

### Method 2: Using PowerShell Script
Right-click `run_flask.ps1` and select "Run with PowerShell"

### Method 3: Manual Command
Open PowerShell or Command Prompt in the project folder and run:
```bash
python flask_app.py
```

## Accessing the Application
Once the server is running, open your web browser and navigate to:
```
http://localhost:5000
```

## What You'll See

### 1. Input Form (Left Sidebar)
Fill in the following information:
- **Personal Details**: Age, marital status, dependents
- **Financial Information**: Annual income, monthly expenses
- **Current Insurance**: Coverage amount, annual premium
- **Riders**: Accident cover, critical illness cover
- **Debts**: Home loan, other debts
- **Assumptions**: Expected inflation rate

### 2. Analysis Results (Main Area)
After clicking "Analyze", you'll see:

#### Coverage Analysis
- Current coverage vs recommended coverage
- Coverage gap (if any)
- Income multiplier assessment

#### Premium Analysis
- Current premium as % of income
- Maximum affordable premium
- Additional premium capacity

#### Rider Analysis
- Critical illness coverage assessment
- Recommended critical illness cover (3x income)
- Coverage gaps

#### Financial Health Score
- Coverage Score (0-10)
- Premium Score (0-10)
- Debt Management Score (0-10)
- Savings Score (0-10)
- Overall Score (0-10)

#### Personalized Recommendations
- Specific action items based on your financial situation
- Priority-ranked suggestions

#### Future Planning
- Inflation impact over 10 years
- Action timeline (30 days, 3 months, 6 months)

### 3. Detailed Report
Click "Generate Detailed Summary Report" to get:
- Comprehensive financial analysis
- Detailed recommendations
- Inflation protection strategies
- Immediate action plan
- Download as Markdown file

## Features Overview

### 📊 Interactive Analysis
- Real-time calculations
- Dynamic form inputs with sliders
- Instant results display

### 💰 Comprehensive Metrics
- Coverage adequacy assessment
- Premium affordability analysis
- Rider gap analysis
- Financial health scoring

### 🎯 Personalized Recommendations
- Based on your specific financial situation
- Prioritized action items
- Timeline-based planning

### 📄 Report Generation
- Detailed markdown reports
- Downloadable for future reference
- Professional formatting

## Understanding the Scores

### Coverage Score (0-10)
- **8-10**: Excellent coverage
- **6-8**: Good coverage
- **Below 6**: Needs improvement

### Premium Score (0-10)
- **8-10**: Highly affordable (< 5% of income)
- **6-8**: Affordable (5-10% of income)
- **Below 6**: High premium burden (> 10% of income)

### Debt Score (0-10)
- **8-10**: Low debt-to-income ratio
- **6-8**: Manageable debt
- **Below 6**: High debt burden

### Savings Score (0-10)
- **8-10**: Excellent savings rate (> 30%)
- **6-8**: Good savings rate (20-30%)
- **Below 6**: Low savings rate (< 20%)

## Key Financial Rules Used

1. **Recommended Life Insurance**: 10-15x annual income
2. **Maximum Premium**: 10% of annual income
3. **Critical Illness Cover**: 3x annual income
4. **Emergency Fund**: 6 months of expenses
5. **Savings Rate**: Minimum 20% of income

## Tips for Best Results

1. **Be Accurate**: Enter exact figures for best analysis
2. **Include All Debts**: Don't forget credit cards, personal loans, etc.
3. **Review Riders**: Make sure you know your current rider coverage
4. **Realistic Inflation**: Use 6-7% for India-specific scenarios
5. **Annual Review**: Re-run analysis every year or when life events occur

## Common Questions

**Q: Why is my coverage gap so high?**
A: The 10x income rule ensures your family can maintain their lifestyle for 10+ years even without your income.

**Q: What if I can't afford the recommended coverage?**
A: Start with term insurance (cheapest), and gradually increase coverage. The tool shows your additional premium capacity.

**Q: How is Critical Illness cover different from Life Insurance?**
A: CI pays you while you're alive if diagnosed with covered conditions. Life insurance pays beneficiaries after death.

**Q: Should I include my spouse's income?**
A: No, calculate separately for each income earner, then sum the coverage needed.

**Q: What about inflation on premium?**
A: Term insurance premiums are typically fixed. The inflation impact is on your living expenses and coverage needs.

## Troubleshooting

**Application won't start:**
- Check if Python is installed: `python --version`
- Install dependencies: `pip install -r requirements.txt`
- Check if port 5000 is free

**Results not showing:**
- Check browser console for errors (F12)
- Ensure all required fields are filled
- Try refreshing the page

**Report won't download:**
- Generate the report first
- Check browser download permissions
- Try a different browser

## Next Steps After Analysis

1. **If Underinsured:**
   - Compare term insurance plans online
   - Look for pure term plans (no investment component)
   - Check riders availability

2. **If Over-Paying Premium:**
   - Review your current policy
   - Consider switching to pure term insurance
   - Check for unnecessary riders

3. **If High Debt:**
   - Create debt repayment plan
   - Consider debt consolidation
   - Build emergency fund first

4. **If Low Savings:**
   - Track expenses for 3 months
   - Identify areas to cut back
   - Automate savings (monthly SIP)

## Support & Feedback

For technical issues or feature requests, please refer to the main project documentation.

---

**Disclaimer**: This tool provides general financial guidance based on standard principles. For personalized financial advice, please consult a certified financial planner.
