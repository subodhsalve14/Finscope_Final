"""
SIP Investment Recommendation System - Complete ML Pipeline
Includes: Synthetic Data Generation, Model Training, and Prediction API
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# PART 1: SYNTHETIC DATA GENERATION
# ============================================================================

def generate_synthetic_sip_data(n_samples=5000):
    """
    Generate synthetic financial data for SIP recommendation training
    """
    np.random.seed(42)
    
    data = {
        'user_id': [f'USER_{str(i).zfill(5)}' for i in range(n_samples)],
        'age': np.random.randint(22, 60, n_samples),
        'monthly_income': np.random.choice(
            [30000, 40000, 50000, 60000, 75000, 100000, 150000, 200000, 300000, 500000],
            n_samples,
            p=[0.15, 0.15, 0.15, 0.12, 0.10, 0.10, 0.08, 0.07, 0.05, 0.03]
        ),
        'goal_type': np.random.choice(
            ['retirement', 'child_education', 'house', 'vacation', 'wealth_creation'],
            n_samples,
            p=[0.3, 0.25, 0.25, 0.05, 0.15]
        ),
        'risk_tolerance': np.random.choice(
            ['low', 'medium', 'high'],
            n_samples,
            p=[0.25, 0.50, 0.25]
        ),
        'investment_experience': np.random.choice(
            ['beginner', 'intermediate', 'expert'],
            n_samples,
            p=[0.40, 0.40, 0.20]
        ),
        'need_for_liquidity': np.random.choice([0, 1], n_samples, p=[0.7, 0.3])
    }
    
    df = pd.DataFrame(data)
    
    # Derive monthly_expenses (40-70% of income)
    df['monthly_expenses'] = (df['monthly_income'] * 
                               np.random.uniform(0.40, 0.70, n_samples)).astype(int)
    
    # Derive existing_EMIs (0-30% of income)
    df['existing_EMIs'] = (df['monthly_income'] * 
                           np.random.uniform(0, 0.30, n_samples)).astype(int)
    
    # Current savings (0.5x to 24x monthly income)
    df['current_savings'] = (df['monthly_income'] * 
                             np.random.uniform(0.5, 24, n_samples)).astype(int)
    
    # Current investments (0 to 36x monthly income)
    df['current_investments_value'] = (df['monthly_income'] * 
                                       np.random.uniform(0, 36, n_samples)).astype(int)
    
    # Goal amount based on goal type
    goal_multipliers = {
        'retirement': (100, 300),
        'child_education': (30, 100),
        'house': (30, 150),
        'vacation': (2, 10),
        'wealth_creation': (50, 200)
    }
    
    df['goal_amount'] = df.apply(
        lambda row: int(row['monthly_income'] * 
                       np.random.uniform(*goal_multipliers[row['goal_type']])),
        axis=1
    )
    
    # Goal duration based on age and goal type
    def get_duration(row):
        if row['goal_type'] == 'retirement':
            return max(5, 60 - row['age'])
        elif row['goal_type'] == 'child_education':
            return np.random.randint(5, 20)
        elif row['goal_type'] == 'house':
            return np.random.randint(3, 15)
        elif row['goal_type'] == 'vacation':
            return np.random.randint(1, 5)
        else:  # wealth_creation
            return np.random.randint(5, 25)
    
    df['goal_duration_years'] = df.apply(get_duration, axis=1)
    
    # Market indicators (with slight variations)
    df['inflation_rate'] = np.random.normal(5.2, 0.5, n_samples).clip(4.0, 7.0)
    df['repo_rate'] = np.random.normal(6.5, 0.3, n_samples).clip(5.5, 7.5)
    df['Nifty50_PE_ratio'] = np.random.normal(22.5, 2.0, n_samples).clip(18, 28)
    df['market_volatility_index'] = np.random.normal(15.0, 3.0, n_samples).clip(10, 25)
    df['GDP_growth_rate'] = np.random.normal(6.7, 0.8, n_samples).clip(5.0, 8.5)
    df['average_fund_return_3y'] = np.random.normal(12.5, 2.0, n_samples).clip(8, 18)
    df['fund_risk_score'] = np.random.normal(6.2, 1.5, n_samples).clip(3, 9)
    df['FD_interest_rate'] = np.random.normal(7.0, 0.4, n_samples).clip(6.0, 8.0)
    
    # ========================================================================
    # TARGET VARIABLES - SIP Amount Calculation
    # ========================================================================
    
    def calculate_sip_and_allocation(row):
        # Disposable income
        disposable = row['monthly_income'] - row['monthly_expenses'] - row['existing_EMIs']
        disposable = max(0, disposable)
        
        # Calculate required SIP using future value formula
        # FV = SIP * [(1+r)^n - 1] / r
        r = 0.12 / 12  # Assuming 12% annual return
        n = row['goal_duration_years'] * 12
        
        if n > 0:
            required_sip = (row['goal_amount'] * r) / (np.power(1 + r, n) - 1)
        else:
            required_sip = row['goal_amount']
        
        # Recommend 60-80% of disposable or required, whichever is feasible
        sip_percentage = np.random.uniform(0.60, 0.80)
        recommended_sip = min(disposable * sip_percentage, required_sip * 1.2)
        recommended_sip = max(500, round(recommended_sip / 500) * 500)  # Round to nearest 500
        
        # Allocation logic based on risk tolerance, age, and duration
        if row['risk_tolerance'] == 'high':
            if row['goal_duration_years'] > 10:
                equity = np.random.randint(70, 85)
                debt = np.random.randint(10, 20)
            else:
                equity = np.random.randint(60, 75)
                debt = np.random.randint(15, 25)
        elif row['risk_tolerance'] == 'medium':
            if row['goal_duration_years'] > 10:
                equity = np.random.randint(55, 70)
                debt = np.random.randint(20, 30)
            else:
                equity = np.random.randint(45, 60)
                debt = np.random.randint(25, 35)
        else:  # low risk
            if row['goal_duration_years'] > 10:
                equity = np.random.randint(35, 50)
                debt = np.random.randint(35, 45)
            else:
                equity = np.random.randint(25, 40)
                debt = np.random.randint(45, 55)
        
        # Age adjustment (older = more conservative)
        if row['age'] > 45:
            shift = min(15, (row['age'] - 45) * 2)
            equity -= shift
            debt += shift
        
        # Ensure allocations sum to 100
        hybrid = 100 - equity - debt
        hybrid = max(5, min(30, hybrid))  # Keep hybrid between 5-30%
        
        # Normalize
        total = equity + debt + hybrid
        equity = int((equity / total) * 100)
        debt = int((debt / total) * 100)
        hybrid = 100 - equity - debt
        
        return pd.Series({
            'recommended_SIP_amount': int(recommended_sip),
            'equity_allocation': equity,
            'debt_allocation': debt,
            'hybrid_allocation': hybrid
        })
    
    targets = df.apply(calculate_sip_and_allocation, axis=1)
    df = pd.concat([df, targets], axis=1)
    
    return df


# ============================================================================
# PART 2: DATA PREPROCESSING
# ============================================================================

def preprocess_data(df):
    """
    Preprocess data for ML model training
    """
    # Separate features and targets
    feature_cols = [
        'age', 'monthly_income', 'monthly_expenses', 'existing_EMIs',
        'current_savings', 'current_investments_value', 'goal_amount',
        'goal_duration_years', 'need_for_liquidity', 'inflation_rate',
        'repo_rate', 'Nifty50_PE_ratio', 'market_volatility_index',
        'GDP_growth_rate', 'average_fund_return_3y', 'fund_risk_score',
        'FD_interest_rate', 'goal_type', 'risk_tolerance', 'investment_experience'
    ]
    
    target_cols = [
        'recommended_SIP_amount', 'equity_allocation', 
        'debt_allocation', 'hybrid_allocation'
    ]
    
    X = df[feature_cols].copy()
    y = df[target_cols].copy()
    
    # Encode categorical variables
    label_encoders = {}
    categorical_cols = ['goal_type', 'risk_tolerance', 'investment_experience']
    
    for col in categorical_cols:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col])
        label_encoders[col] = le
    
    return X, y, label_encoders


# ============================================================================
# PART 3: MODEL TRAINING
# ============================================================================

def train_models(X, y):
    """
    Train ML models for SIP recommendation
    """
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    print("=" * 80)
    print("TRAINING MODEL 1: SIP AMOUNT PREDICTION")
    print("=" * 80)
    
    # Model 1: SIP Amount Prediction
    sip_model = RandomForestRegressor(
        n_estimators=200,
        max_depth=15,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )
    
    sip_model.fit(X_train_scaled, y_train['recommended_SIP_amount'])
    sip_pred = sip_model.predict(X_test_scaled)
    
    # Evaluate Model 1
    sip_mae = mean_absolute_error(y_test['recommended_SIP_amount'], sip_pred)
    sip_rmse = np.sqrt(mean_squared_error(y_test['recommended_SIP_amount'], sip_pred))
    sip_r2 = r2_score(y_test['recommended_SIP_amount'], sip_pred)
    
    print(f"✓ Mean Absolute Error (MAE): ₹{sip_mae:,.2f}")
    print(f"✓ Root Mean Squared Error (RMSE): ₹{sip_rmse:,.2f}")
    print(f"✓ R² Score: {sip_r2:.4f}")
    
    print("\n" + "=" * 80)
    print("TRAINING MODEL 2: ASSET ALLOCATION PREDICTION")
    print("=" * 80)
    
    # Model 2: Asset Allocation (Multi-output)
    allocation_targets = ['equity_allocation', 'debt_allocation', 'hybrid_allocation']
    
    allocation_model = MultiOutputRegressor(
        RandomForestRegressor(
            n_estimators=200,
            max_depth=12,
            min_samples_split=5,
            random_state=42,
            n_jobs=-1
        )
    )
    
    allocation_model.fit(X_train_scaled, y_train[allocation_targets])
    allocation_pred = allocation_model.predict(X_test_scaled)
    
    # Evaluate Model 2
    for i, target in enumerate(allocation_targets):
        mae = mean_absolute_error(y_test[target], allocation_pred[:, i])
        rmse = np.sqrt(mean_squared_error(y_test[target], allocation_pred[:, i]))
        r2 = r2_score(y_test[target], allocation_pred[:, i])
        
        print(f"\n{target.upper()}:")
        print(f"  MAE: {mae:.2f}%")
        print(f"  RMSE: {rmse:.2f}%")
        print(f"  R²: {r2:.4f}")
    
    # Feature Importance
    print("\n" + "=" * 80)
    print("TOP 10 IMPORTANT FEATURES (SIP Amount Model)")
    print("=" * 80)
    
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': sip_model.feature_importances_
    }).sort_values('importance', ascending=False).head(10)
    
    for idx, row in feature_importance.iterrows():
        print(f"{row['feature']:30s}: {row['importance']:.4f}")
    
    return sip_model, allocation_model, scaler


# ============================================================================
# PART 4: PREDICTION FUNCTION
# ============================================================================

# def predict_sip_recommendation(user_data, sip_model, allocation_model, scaler, label_encoders):
#     """
#     Make predictions for a new user
#     """
#     # Prepare input
#     input_df = pd.DataFrame([user_data])
    
#     # Encode categorical variables
#     for col, le in label_encoders.items():
#         if col in input_df.columns:
#             input_df[col] = le.transform([input_df[col].values[0]])[0]
    
#     # Scale features
#     input_scaled = scaler.transform(input_df)
    
#     # Predict
#     sip_amount = sip_model.predict(input_scaled)[0]
#     allocations = allocation_model.predict(input_scaled)[0]
    
#     # Fund recommendations based on allocation
#     fund_recommendations = []
    
#     if allocations[0] > 0:  # Equity
#         fund_recommendations.append({
#             'name': 'Parag Parikh Flexi Cap Fund' if allocations[0] > 50 else 'HDFC Top 100 Fund',
#             'type': 'Equity',
#             'allocation': round(allocations[0], 1),
#             'returns_3y': 15.2,
#             'risk': 'High'
#         })
    
#     if allocations[1] > 0:  # Debt
#         fund_recommendations.append({
#             'name': 'ICICI Prudential Corporate Bond Fund',
#             'type': 'Debt',
#             'allocation': round(allocations[1], 1),
#             'returns_3y': 7.8,
#             'risk': 'Low'
#         })
    
#     if allocations[2] > 0:  # Hybrid
#         fund_recommendations.append({
#             'name': 'HDFC Balanced Advantage Fund',
#             'type': 'Hybrid',
#             'allocation': round(allocations[2], 1),
#             'returns_3y': 11.5,
#             'risk': 'Medium'
#         })
    
#     return {
#         'recommended_SIP_amount': int(round(sip_amount, -2)),  # Round to nearest 100
#         'equity_allocation': round(allocations[0], 1),
#         'debt_allocation': round(allocations[1], 1),
#         'hybrid_allocation': round(allocations[2], 1),
#         'fund_recommendations': fund_recommendations
#     }

def predict_sip_recommendation(user_data, sip_model, allocation_model, scaler, label_encoders):
    """
    Make predictions for a new user
    """
    # Prepare input
    input_df = pd.DataFrame([user_data])
    
    # Encode categorical variables
    for col, le in label_encoders.items():
        if col in input_df.columns:
            input_df[col] = le.transform([input_df[col].values[0]])[0]
    
    # Ensure same column order as training
    feature_cols = [
        'age', 'monthly_income', 'monthly_expenses', 'existing_EMIs',
        'current_savings', 'current_investments_value', 'goal_amount',
        'goal_duration_years', 'need_for_liquidity', 'inflation_rate',
        'repo_rate', 'Nifty50_PE_ratio', 'market_volatility_index',
        'GDP_growth_rate', 'average_fund_return_3y', 'fund_risk_score',
        'FD_interest_rate', 'goal_type', 'risk_tolerance', 'investment_experience'
    ]
    
    input_df = input_df[feature_cols]  # 🔥 Force correct column order
    
    # Scale features
    input_scaled = scaler.transform(input_df)
    
    # Predict
    sip_amount = sip_model.predict(input_scaled)[0]
    allocations = allocation_model.predict(input_scaled)[0]
    
    # Fund recommendations logic (same as before)...
    fund_recommendations = []
    if allocations[0] > 0:
        fund_recommendations.append({
            'name': 'Parag Parikh Flexi Cap Fund' if allocations[0] > 50 else 'HDFC Top 100 Fund',
            'type': 'Equity',
            'allocation': round(allocations[0], 1),
            'returns_3y': 15.2,
            'risk': 'High'
        })
    if allocations[1] > 0:
        fund_recommendations.append({
            'name': 'ICICI Prudential Corporate Bond Fund',
            'type': 'Debt',
            'allocation': round(allocations[1], 1),
            'returns_3y': 7.8,
            'risk': 'Low'
        })
    if allocations[2] > 0:
        fund_recommendations.append({
            'name': 'HDFC Balanced Advantage Fund',
            'type': 'Hybrid',
            'allocation': round(allocations[2], 1),
            'returns_3y': 11.5,
            'risk': 'Medium'
        })
    
    return {
        'recommended_SIP_amount': int(round(sip_amount, -2)),
        'equity_allocation': round(allocations[0], 1),
        'debt_allocation': round(allocations[1], 1),
        'hybrid_allocation': round(allocations[2], 1),
        'fund_recommendations': fund_recommendations
    }



# ============================================================================
# PART 5: MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("SIP INVESTMENT RECOMMENDATION SYSTEM - ML PIPELINE")
    print("=" * 80)
    
    # Step 1: Generate synthetic data
    print("\n[1/5] Generating synthetic training data...")
    df = generate_synthetic_sip_data(n_samples=5000)
    print(f"✓ Generated {len(df)} samples")
    print(f"✓ Dataset shape: {df.shape}")
    
    # Save dataset
    df.to_csv('sip_training_data.csv', index=False)
    print("✓ Saved to 'sip_training_data.csv'")
    
    # Display sample
    print("\n📊 Sample Data (first 3 rows):")
    print(df.head(3).to_string())
    
    # Step 2: Preprocess data
    print("\n[2/5] Preprocessing data...")
    X, y, label_encoders = preprocess_data(df)
    print(f"✓ Features shape: {X.shape}")
    print(f"✓ Targets shape: {y.shape}")
    
    # Step 3: Train models
    print("\n[3/5] Training ML models...")
    sip_model, allocation_model, scaler = train_models(X, y)
    
    # Step 4: Save models
    print("\n[4/5] Saving trained models...")
    joblib.dump(sip_model, 'sip_amount_model.pkl')
    joblib.dump(allocation_model, 'allocation_model.pkl')
    joblib.dump(scaler, 'scaler.pkl')
    joblib.dump(label_encoders, 'label_encoders.pkl')
    print("✓ Models saved successfully")
    
    # Step 5: Test prediction
    print("\n[5/5] Testing prediction on sample user...")
    
    test_user = {
        'age': 30,
        'monthly_income': 80000,
        'monthly_expenses': 45000,
        'existing_EMIs': 5000,
        'current_savings': 100000,
        'current_investments_value': 50000,
        'goal_type': 'retirement',
        'goal_amount': 5000000,
        'goal_duration_years': 25,
        'risk_tolerance': 'medium',
        'investment_experience': 'intermediate',
        'need_for_liquidity': 0,
        'inflation_rate': 5.2,
        'repo_rate': 6.5,
        'Nifty50_PE_ratio': 22.5,
        'market_volatility_index': 15.3,
        'GDP_growth_rate': 6.7,
        'average_fund_return_3y': 12.5,
        'fund_risk_score': 6.2,
        'FD_interest_rate': 7.0
    }
    
    result = predict_sip_recommendation(
        test_user, sip_model, allocation_model, scaler, label_encoders
    )
    
    print("\n" + "=" * 80)
    print("PREDICTION RESULT")
    print("=" * 80)
    print(f"Recommended Monthly SIP: ₹{result['recommended_SIP_amount']:,}")
    print(f"\nAsset Allocation:")
    print(f"  • Equity:  {result['equity_allocation']}%")
    print(f"  • Debt:    {result['debt_allocation']}%")
    print(f"  • Hybrid:  {result['hybrid_allocation']}%")
    print(f"\nRecommended Funds:")
    for fund in result['fund_recommendations']:
        print(f"  • {fund['name']} ({fund['type']}) - {fund['allocation']}%")
    
    print("\n" + "=" * 80)
    print("✅ PIPELINE COMPLETE - All models trained and saved successfully!")
    print("=" * 80)
    print("\nFiles created:")
    print("  1. sip_training_data.csv - Training dataset")
    print("  2. sip_amount_model.pkl - SIP amount prediction model")
    print("  3. allocation_model.pkl - Asset allocation model")
    print("  4. scaler.pkl - Feature scaler")
    print("  5. label_encoders.pkl - Categorical encoders")
    print("\nYou can now use these models in your Flask/FastAPI backend!")