"""
Flask API Backend for SIP Investment Recommendation System
WITH INFLATION DATA INTEGRATION FROM EXCEL
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import numpy as np
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# ============================================================================
# LOAD INFLATION DATA FROM EXCEL
# ============================================================================

def load_inflation_data(filepath='inflation_data.xlsx'):
    """
    Load inflation data from Excel file
    Expected columns: 'month', 'combined_inflation'
    """
    try:
        # Read Excel file
        inflation_df = pd.read_excel(filepath)
        
        # Standardize column names (handle different naming conventions)
        inflation_df.columns = inflation_df.columns.str.lower().str.strip()
        
        # Rename columns to expected format
        column_mapping = {
            'combined inflation': 'combined_inflation',
            'combined_inflation': 'combined_inflation',
            'inflation': 'combined_inflation'
        }
        
        for old_col, new_col in column_mapping.items():
            if old_col in inflation_df.columns:
                inflation_df.rename(columns={old_col: new_col}, inplace=True)
        
        # Convert month column to datetime if it's not already
        if 'month' in inflation_df.columns:
            inflation_df['month'] = pd.to_datetime(inflation_df['month'])
        
        # Sort by date
        inflation_df = inflation_df.sort_values('month', ascending=False)
        
        print(f"✓ Loaded {len(inflation_df)} inflation records")
        print(f"  Date range: {inflation_df['month'].min()} to {inflation_df['month'].max()}")
        print(f"  Latest inflation: {inflation_df.iloc[0]['combined_inflation']:.2f}%")
        
        return inflation_df
        
    except FileNotFoundError:
        print(f"⚠ Warning: {filepath} not found. Using default inflation value.")
        return None
    except Exception as e:
        print(f"⚠ Error loading inflation data: {e}")
        return None


def get_current_inflation(inflation_df):
    """
    Get the most recent inflation rate from the dataset
    """
    if inflation_df is None or len(inflation_df) == 0:
        return 5.2  # Default fallback value
    
    # Return the most recent inflation value
    return float(inflation_df.iloc[0]['combined_inflation'])


def get_historical_inflation_trend(inflation_df, months=12):
    """
    Get inflation trend for the last N months
    """
    if inflation_df is None or len(inflation_df) == 0:
        return None
    
    recent_data = inflation_df.head(months)
    
    return {
        'average': float(recent_data['combined_inflation'].mean()),
        'min': float(recent_data['combined_inflation'].min()),
        'max': float(recent_data['combined_inflation'].max()),
        'current': float(recent_data.iloc[0]['combined_inflation']),
        'trend': 'increasing' if recent_data.iloc[0]['combined_inflation'] > recent_data['combined_inflation'].mean() else 'decreasing',
        'months_analyzed': len(recent_data)
    }


def get_inflation_by_date(inflation_df, target_date=None):
    """
    Get inflation for a specific date or the closest available date
    """
    if inflation_df is None or len(inflation_df) == 0:
        return 5.2
    
    if target_date is None:
        return get_current_inflation(inflation_df)
    
    target_date = pd.to_datetime(target_date)
    
    # Find the closest date
    inflation_df['date_diff'] = abs(inflation_df['month'] - target_date)
    closest = inflation_df.loc[inflation_df['date_diff'].idxmin()]
    
    return float(closest['combined_inflation'])


# ============================================================================
# INITIALIZE - LOAD MODELS AND INFLATION DATA
# ============================================================================

print("=" * 80)
print("INITIALIZING SIP RECOMMENDATION API")
print("=" * 80)

# Load ML Models
print("\n[1/2] Loading trained ML models...")
try:
    sip_model = joblib.load('sip_amount_model.pkl')
    allocation_model = joblib.load('allocation_model.pkl')
    scaler = joblib.load('scaler.pkl')
    label_encoders = joblib.load('label_encoders.pkl')
    print("✓ All ML models loaded successfully!")
except FileNotFoundError as e:
    print(f"⚠ Model files not found. Please run the training script first.")
    print(f"Error: {e}")

# Load Inflation Data
print("\n[2/2] Loading inflation data from Excel...")
INFLATION_DATA = load_inflation_data('inflation_data.xlsx')  # Update path as needed

print("\n" + "=" * 80)
print("✅ INITIALIZATION COMPLETE")
print("=" * 80 + "\n")

# ============================================================================
# FUND DATABASE
# ============================================================================

FUND_DATABASE = {
    'equity': [
        {
            'name': 'Parag Parikh Flexi Cap Fund',
            'category': 'Equity',
            'sub_category': 'Flexi Cap',
            'returns_1y': 18.5,
            'returns_3y': 15.2,
            'returns_5y': 17.8,
            'risk': 'High',
            'expense_ratio': 0.82,
            'min_sip': 1000
        },
        {
            'name': 'Axis Bluechip Fund',
            'category': 'Equity',
            'sub_category': 'Large Cap',
            'returns_1y': 16.2,
            'returns_3y': 13.8,
            'returns_5y': 15.4,
            'risk': 'High',
            'expense_ratio': 0.45,
            'min_sip': 500
        },
        {
            'name': 'Kotak Emerging Equity Fund',
            'category': 'Equity',
            'sub_category': 'Mid Cap',
            'returns_1y': 22.4,
            'returns_3y': 19.6,
            'returns_5y': 21.2,
            'risk': 'Very High',
            'expense_ratio': 0.68,
            'min_sip': 1000
        },
        {
            'name': 'HDFC Top 100 Fund',
            'category': 'Equity',
            'sub_category': 'Large Cap',
            'returns_1y': 15.8,
            'returns_3y': 13.2,
            'returns_5y': 14.9,
            'risk': 'High',
            'expense_ratio': 0.52,
            'min_sip': 500
        }
    ],
    'debt': [
        {
            'name': 'ICICI Prudential Corporate Bond Fund',
            'category': 'Debt',
            'sub_category': 'Corporate Bond',
            'returns_1y': 7.2,
            'returns_3y': 7.8,
            'returns_5y': 8.1,
            'risk': 'Low',
            'expense_ratio': 0.35,
            'min_sip': 1000
        },
        {
            'name': 'Axis Banking & PSU Debt Fund',
            'category': 'Debt',
            'sub_category': 'Banking & PSU',
            'returns_1y': 7.5,
            'returns_3y': 8.0,
            'returns_5y': 8.3,
            'risk': 'Low',
            'expense_ratio': 0.28,
            'min_sip': 500
        },
        {
            'name': 'SBI Magnum Gilt Fund',
            'category': 'Debt',
            'sub_category': 'Gilt',
            'returns_1y': 6.8,
            'returns_3y': 7.2,
            'returns_5y': 7.8,
            'risk': 'Low',
            'expense_ratio': 0.42,
            'min_sip': 500
        }
    ],
    'hybrid': [
        {
            'name': 'HDFC Balanced Advantage Fund',
            'category': 'Hybrid',
            'sub_category': 'Dynamic Asset Allocation',
            'returns_1y': 12.8,
            'returns_3y': 11.5,
            'returns_5y': 12.9,
            'risk': 'Medium',
            'expense_ratio': 0.88,
            'min_sip': 1000
        },
        {
            'name': 'ICICI Prudential Equity & Debt Fund',
            'category': 'Hybrid',
            'sub_category': 'Aggressive Hybrid',
            'returns_1y': 14.2,
            'returns_3y': 12.8,
            'returns_5y': 13.5,
            'risk': 'Medium',
            'expense_ratio': 0.95,
            'min_sip': 500
        },
        {
            'name': 'Mirae Asset Hybrid Equity Fund',
            'category': 'Hybrid',
            'sub_category': 'Aggressive Hybrid',
            'returns_1y': 15.1,
            'returns_3y': 13.2,
            'returns_5y': 14.8,
            'risk': 'Medium',
            'expense_ratio': 0.72,
            'min_sip': 1000
        }
    ]
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_market_data():
    """
    Get current market data including real-time inflation from Excel
    """
    # Get current inflation from loaded data
    current_inflation = get_current_inflation(INFLATION_DATA)
    
    return {
        'inflation_rate': current_inflation,  # 🔥 REAL INFLATION FROM EXCEL
        'repo_rate': 6.5,
        'Nifty50_PE_ratio': 22.5,
        'market_volatility_index': 15.3,
        'GDP_growth_rate': 6.7,
        'average_fund_return_3y': 12.5,
        'fund_risk_score': 6.2,
        'FD_interest_rate': 7.0
    }


def select_funds(equity_pct, debt_pct, hybrid_pct, risk_tolerance):
    """Select best funds based on allocation and risk tolerance"""
    recommendations = []
    
    if equity_pct > 0:
        equity_funds = FUND_DATABASE['equity']
        if risk_tolerance == 'high':
            selected = equity_funds[2]
        else:
            selected = equity_funds[0]
        
        recommendations.append({
            **selected,
            'allocation_percentage': round(equity_pct, 1)
        })
    
    if debt_pct > 0:
        debt_funds = FUND_DATABASE['debt']
        selected = debt_funds[0]
        
        recommendations.append({
            **selected,
            'allocation_percentage': round(debt_pct, 1)
        })
    
    if hybrid_pct > 0:
        hybrid_funds = FUND_DATABASE['hybrid']
        if risk_tolerance == 'high':
            selected = hybrid_funds[2]
        else:
            selected = hybrid_funds[0]
        
        recommendations.append({
            **selected,
            'allocation_percentage': round(hybrid_pct, 1)
        })
    
    return recommendations


def calculate_projections(sip_amount, equity_pct, debt_pct, hybrid_pct, duration_years, goal_amount):
    """Calculate investment projections"""
    equity_return = 0.14
    debt_return = 0.075
    hybrid_return = 0.115
    
    weighted_return = (
        (equity_pct / 100) * equity_return +
        (debt_pct / 100) * debt_return +
        (hybrid_pct / 100) * hybrid_return
    )
    
    r = weighted_return / 12
    n = duration_years * 12
    
    if r > 0:
        future_value = sip_amount * ((np.power(1 + r, n) - 1) / r)
    else:
        future_value = sip_amount * n
    
    total_investment = sip_amount * n
    
    return {
        'total_investment': int(total_investment),
        'future_value': int(future_value),
        'expected_returns': round(weighted_return * 100, 2),
        'goal_achievement': min(100, round((future_value / goal_amount) * 100, 1)) if goal_amount > 0 else 100,
        'wealth_gain': int(future_value - total_investment)
    }


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.route('/', methods=['GET'])
def home():
    """Health check endpoint"""
    current_inflation = get_current_inflation(INFLATION_DATA)
    
    return jsonify({
        'status': 'active',
        'message': 'SIP Investment Recommendation API with Real-time Inflation Data',
        'version': '2.0.0',
        'current_inflation': current_inflation,
        'inflation_data_loaded': INFLATION_DATA is not None,
        'endpoints': {
            'predict': '/api/predict (POST)',
            'market_data': '/api/market-data (GET)',
            'inflation_info': '/api/inflation-info (GET)',
            'inflation_trend': '/api/inflation-trend (GET)',
            'funds': '/api/funds (GET)'
        }
    })


@app.route('/api/inflation-info', methods=['GET'])
def get_inflation_info():
    """
    Get current inflation information
    """
    if INFLATION_DATA is None:
        return jsonify({
            'success': False,
            'error': 'Inflation data not loaded'
        }), 404
    
    current_inflation = get_current_inflation(INFLATION_DATA)
    latest_record = INFLATION_DATA.iloc[0]
    
    return jsonify({
        'success': True,
        'data': {
            'current_inflation': current_inflation,
            'as_of_date': latest_record['month'].strftime('%Y-%m-%d'),
            'total_records': len(INFLATION_DATA),
            'data_range': {
                'from': INFLATION_DATA['month'].min().strftime('%Y-%m-%d'),
                'to': INFLATION_DATA['month'].max().strftime('%Y-%m-%d')
            }
        }
    })


@app.route('/api/inflation-trend', methods=['GET'])
def get_inflation_trend_endpoint():
    """
    Get inflation trend analysis
    Query params: months (default: 12)
    """
    if INFLATION_DATA is None:
        return jsonify({
            'success': False,
            'error': 'Inflation data not loaded'
        }), 404
    
    months = request.args.get('months', default=12, type=int)
    months = min(max(1, months), len(INFLATION_DATA))  # Validate range
    
    trend_data = get_historical_inflation_trend(INFLATION_DATA, months)
    
    # Get monthly data for charting
    recent_data = INFLATION_DATA.head(months)
    monthly_values = [
        {
            'month': row['month'].strftime('%Y-%m'),
            'inflation': float(row['combined_inflation'])
        }
        for _, row in recent_data.iterrows()
    ]
    monthly_values.reverse()  # Chronological order
    
    return jsonify({
        'success': True,
        'data': {
            'summary': trend_data,
            'monthly_data': monthly_values
        }
    })


@app.route('/api/market-data', methods=['GET'])
def get_market_info():
    """Get current market indicators with real inflation"""
    market_data = get_market_data()
    
    # Add inflation trend if available
    inflation_trend = None
    if INFLATION_DATA is not None:
        inflation_trend = get_historical_inflation_trend(INFLATION_DATA, 6)
    
    return jsonify({
        'success': True,
        'data': market_data,
        'inflation_trend': inflation_trend,
        'timestamp': pd.Timestamp.now().isoformat()
    })


@app.route('/api/funds', methods=['GET'])
def get_funds():
    """Get all available funds"""
    category = request.args.get('category', 'all')
    
    if category == 'all':
        funds = {
            'equity': FUND_DATABASE['equity'],
            'debt': FUND_DATABASE['debt'],
            'hybrid': FUND_DATABASE['hybrid']
        }
    elif category in FUND_DATABASE:
        funds = FUND_DATABASE[category]
    else:
        return jsonify({
            'success': False,
            'error': 'Invalid category. Use: equity, debt, hybrid, or all'
        }), 400
    
    return jsonify({
        'success': True,
        'data': funds
    })


@app.route('/api/predict', methods=['POST'])
def predict():
    """
    Main prediction endpoint with real-time inflation integration
    """
    try:
        data = request.get_json()
        
        required_fields = [
            'age', 'monthly_income', 'monthly_expenses', 'existing_EMIs',
            'current_savings', 'current_investments_value', 'goal_type',
            'goal_amount', 'goal_duration_years', 'risk_tolerance',
            'investment_experience', 'need_for_liquidity'
        ]
        
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({
                'success': False,
                'error': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400
        
        # Get market data with REAL INFLATION from Excel
        market_data = get_market_data()
        user_input = {**data, **market_data}
        
        # Prepare features
        feature_cols = [
            'age', 'monthly_income', 'monthly_expenses', 'existing_EMIs',
            'current_savings', 'current_investments_value', 'goal_amount',
            'goal_duration_years', 'need_for_liquidity', 'inflation_rate',
            'repo_rate', 'Nifty50_PE_ratio', 'market_volatility_index',
            'GDP_growth_rate', 'average_fund_return_3y', 'fund_risk_score',
            'FD_interest_rate', 'goal_type', 'risk_tolerance', 'investment_experience'
        ]
        
        input_df = pd.DataFrame([{k: user_input[k] for k in feature_cols}])
        
        # Encode categorical variables
        for col, le in label_encoders.items():
            if col in input_df.columns:
                try:
                    input_df[col] = le.transform([input_df[col].values[0]])[0]
                except ValueError:
                    input_df[col] = 0
        
        # Scale and predict
        input_scaled = scaler.transform(input_df)
        sip_amount = sip_model.predict(input_scaled)[0]
        allocations = allocation_model.predict(input_scaled)[0]
        
        # Process predictions
        sip_amount = int(round(sip_amount, -2))
        equity_pct = max(0, min(100, round(allocations[0], 1)))
        debt_pct = max(0, min(100, round(allocations[1], 1)))
        hybrid_pct = max(0, min(100, round(allocations[2], 1)))
        
        # Normalize allocations
        total = equity_pct + debt_pct + hybrid_pct
        if total > 0:
            equity_pct = round((equity_pct / total) * 100, 1)
            debt_pct = round((debt_pct / total) * 100, 1)
            hybrid_pct = 100 - equity_pct - debt_pct
        
        # Get recommendations
        fund_recommendations = select_funds(
            equity_pct, debt_pct, hybrid_pct, data['risk_tolerance']
        )
        
        # Calculate projections
        projections = calculate_projections(
            sip_amount, equity_pct, debt_pct, hybrid_pct,
            data['goal_duration_years'], data['goal_amount']
        )
        
        # Get inflation context
        inflation_context = None
        if INFLATION_DATA is not None:
            inflation_context = get_historical_inflation_trend(INFLATION_DATA, 6)
        
        # Generate response
        response = {
            'success': True,
            'data': {
                'recommended_SIP_amount': sip_amount,
                'asset_allocation': {
                    'equity': equity_pct,
                    'debt': debt_pct,
                    'hybrid': hybrid_pct
                },
                'fund_recommendations': fund_recommendations,
                'projections': projections,
                'market_conditions': market_data,
                'inflation_context': inflation_context,
                'insights': generate_insights(
                    sip_amount, equity_pct, data['monthly_income'],
                    data['risk_tolerance'], projections['goal_achievement'],
                    market_data['inflation_rate']
                )
            },
            'timestamp': pd.Timestamp.now().isoformat()
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


def generate_insights(sip_amount, equity_pct, monthly_income, risk_tolerance, goal_achievement, inflation_rate):
    """Generate personalized insights with inflation consideration"""
    insights = []
    
    # SIP affordability
    sip_to_income_ratio = (sip_amount / monthly_income) * 100
    if sip_to_income_ratio < 10:
        insights.append({
            'type': 'positive',
            'message': f'Your SIP is {sip_to_income_ratio:.1f}% of income, leaving room for emergencies.'
        })
    elif sip_to_income_ratio > 30:
        insights.append({
            'type': 'warning',
            'message': f'Your SIP is {sip_to_income_ratio:.1f}% of income. Consider optimizing expenses.'
        })
    
    # Inflation impact warning
    if inflation_rate > 6.5:
        insights.append({
            'type': 'warning',
            'message': f'Current inflation at {inflation_rate:.1f}% is high. Your investments should beat inflation for real wealth growth.'
        })
    elif inflation_rate > 5.5:
        insights.append({
            'type': 'info',
            'message': f'Inflation at {inflation_rate:.1f}% - ensure returns exceed this to maintain purchasing power.'
        })
    
    # Equity allocation
    if equity_pct > 70 and risk_tolerance == 'low':
        insights.append({
            'type': 'warning',
            'message': 'High equity allocation may not suit your low risk tolerance.'
        })
    
    # Goal achievement
    if goal_achievement >= 100:
        insights.append({
            'type': 'positive',
            'message': f'Excellent! Projected to achieve {goal_achievement}% of your goal.'
        })
    elif goal_achievement >= 80:
        insights.append({
            'type': 'info',
            'message': f'On track for {goal_achievement}% of goal. Small increases can bridge the gap.'
        })
    else:
        insights.append({
            'type': 'warning',
            'message': f'Current SIP achieves {goal_achievement}% of goal. Increase SIP or extend timeline.'
        })
    
    insights.append({
        'type': 'tip',
        'message': 'Review portfolio annually and rebalance to maintain optimal allocation.'
    })
    
    return insights


@app.route('/api/calculate-required-sip', methods=['POST'])
def calculate_required_sip():
    """Calculate required SIP to reach goal"""
    try:
        data = request.get_json()
        
        goal_amount = data.get('goal_amount', 0)
        duration_years = data.get('duration_years', 0)
        expected_return = data.get('expected_return', 12) / 100
        
        if goal_amount <= 0 or duration_years <= 0:
            return jsonify({
                'success': False,
                'error': 'Goal amount and duration must be positive'
            }), 400
        
        r = expected_return / 12
        n = duration_years * 12
        
        required_sip = (goal_amount * r) / (np.power(1 + r, n) - 1)
        
        return jsonify({
            'success': True,
            'data': {
                'required_monthly_sip': int(round(required_sip, -2)),
                'total_investment': int(required_sip * n),
                'expected_returns': expected_return * 100,
                'goal_amount': goal_amount,
                'duration_years': duration_years
            }
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/compare-scenarios', methods=['POST'])
def compare_scenarios():
    """Compare different SIP scenarios"""
    try:
        data = request.get_json()
        
        sip_amounts = data.get('sip_amounts', [5000, 10000, 15000])
        duration_years = data.get('duration_years', 10)
        equity_pct = data.get('equity_pct', 60)
        debt_pct = data.get('debt_pct', 30)
        hybrid_pct = data.get('hybrid_pct', 10)
        
        scenarios = []
        
        for sip in sip_amounts:
            projection = calculate_projections(
                sip, equity_pct, debt_pct, hybrid_pct, duration_years, 0
            )
            
            scenarios.append({
                'sip_amount': sip,
                'total_investment': projection['total_investment'],
                'future_value': projection['future_value'],
                'wealth_gain': projection['wealth_gain'],
                'expected_returns': projection['expected_returns']
            })
        
        return jsonify({
            'success': True,
            'data': {
                'scenarios': scenarios,
                'duration_years': duration_years,
                'allocation': {
                    'equity': equity_pct,
                    'debt': debt_pct,
                    'hybrid': hybrid_pct
                }
            }
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(e):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def internal_error(e):
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500


# ============================================================================
# RUN SERVER
# ============================================================================

if __name__ == '__main__':
    print("\n" + "=" * 80)
    print("🚀 SIP INVESTMENT RECOMMENDATION API v2.0")
    print("   WITH REAL-TIME INFLATION DATA INTEGRATION")
    print("=" * 80)
    print("\nAvailable Endpoints:")
    print("  GET  /                          - Health check")
    print("  GET  /api/market-data           - Market indicators (with real inflation)")
    print("  GET  /api/inflation-info        - Current inflation details")
    print("  GET  /api/inflation-trend       - Inflation trend analysis")
    print("  GET  /api/funds                 - Available mutual funds")
    print("  POST /api/predict               - Get SIP recommendations")
    print("  POST /api/calculate-required-sip - Calculate required SIP")
    print("  POST /api/compare-scenarios     - Compare scenarios")
    print("\n" + "=" * 80)
    
    app.run(debug=True, host='0.0.0.0', port=5001)