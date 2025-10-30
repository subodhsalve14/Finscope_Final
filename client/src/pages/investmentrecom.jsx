import React, { useState } from "react";
import {
  Calculator,
  TrendingUp,
  PieChart,
  AlertCircle,
  Target,
  TrendingDown,
  Activity,
  DollarSign,
  Info,
  Wallet,
  CreditCard,
  Percent,
  Calendar,
} from "lucide-react";

const SIPRecommender = () => {
  const [formData, setFormData] = useState({
    age: 30,
    monthly_income: 80000,
    monthly_expenses: 45000,
    existing_EMIs: 5000,
    current_savings: 100000,
    current_investments_value: 50000,
    goal_type: "retirement",
    goal_amount: 5000000,
    goal_duration_years: 25,
    risk_tolerance: "medium",
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const API_BASE = "http://127.0.0.1:5001";

  const goalTypeOptions = [
    { value: "retirement", label: "Retirement" },
    { value: "education", label: "Education" },
    { value: "house", label: "House Purchase" },
    { value: "vehicle", label: "Vehicle Purchase" },
    { value: "wealth", label: "Wealth Creation" },
    { value: "emergency", label: "Emergency Fund" },
  ];

  const riskToleranceOptions = [
    { value: "low", label: "Low" },
    { value: "medium", label: "Medium" },
    { value: "high", label: "High" },
  ];

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: isNaN(value) ? value : Number(value),
    }));
  };

  const callAPI = async (endpoint, setState) => {
    setLoading(true);
    setError(null);
    setState(null);

    try {
      const res = await fetch(`${API_BASE}${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      const data = await res.json();
      if (data.success) {
        setState(data.data);
      } else {
        setError(data.error || "Request failed.");
      }
    } catch (err) {
      setError("Could not connect to Flask backend. Make sure the API is running on port 5001.");
    } finally {
      setLoading(false);
    }
  };

  const getInsightIcon = (type) => {
    switch (type) {
      case "positive":
        return <TrendingUp className="text-green-600" size={20} />;
      case "warning":
        return <AlertCircle className="text-orange-600" size={20} />;
      case "info":
        return <Info className="text-blue-600" size={20} />;
      case "tip":
        return <Target className="text-purple-600" size={20} />;
      default:
        return <Info className="text-gray-600" size={20} />;
    }
  };

  const getInsightColor = (type) => {
    switch (type) {
      case "positive":
        return "bg-green-50 border-green-200 text-green-800";
      case "warning":
        return "bg-orange-50 border-orange-200 text-orange-800";
      case "info":
        return "bg-blue-50 border-blue-200 text-blue-800";
      case "tip":
        return "bg-purple-50 border-purple-200 text-purple-800";
      default:
        return "bg-gray-50 border-gray-200 text-gray-800";
    }
  };

  const formatCurrency = (value) => {
    return new Intl.NumberFormat("en-IN").format(value);
  };

  return (
    <div className="p-6 max-w-7xl mx-auto bg-gradient-to-br from-blue-50 to-indigo-50 min-h-screen">
      <div className="bg-white shadow-2xl rounded-2xl p-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2 flex items-center gap-3 text-gray-800">
            <Calculator className="text-blue-600" size={40} /> 
            SIP Investment Recommender
          </h1>
          <p className="text-gray-600">Get personalized SIP recommendations based on your financial profile</p>
        </div>

        <div className="mb-8">
          <h2 className="text-2xl font-semibold mb-6 text-gray-800">Your Financial Details</h2>
          
          <div className="mb-6">
            <h3 className="text-lg font-semibold mb-4 text-gray-700 flex items-center gap-2">
              <Info size={20} className="text-blue-600" />
              Personal Information
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium mb-2 text-gray-700">
                  Age (years)
                </label>
                <input
                  type="text"
                  name="age"
                  value={formData.age}
                  onChange={handleChange}
                  className="border border-gray-300 rounded-lg p-3 w-full focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-2 text-gray-700">
                  Goal Type
                </label>
                <select
                  name="goal_type"
                  value={formData.goal_type}
                  onChange={handleChange}
                  className="border border-gray-300 rounded-lg p-3 w-full focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white"
                  required
                >
                  {goalTypeOptions.map(option => (
                    <option key={option.value} value={option.value}>
                      {option.label}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium mb-2 text-gray-700">
                  Risk Tolerance
                </label>
                <select
                  name="risk_tolerance"
                  value={formData.risk_tolerance}
                  onChange={handleChange}
                  className="border border-gray-300 rounded-lg p-3 w-full focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white"
                  required
                >
                  {riskToleranceOptions.map(option => (
                    <option key={option.value} value={option.value}>
                      {option.label}
                    </option>
                  ))}
                </select>
              </div>
            </div>
          </div>

          <div className="mb-6">
            <h3 className="text-lg font-semibold mb-4 text-gray-700 flex items-center gap-2">
              <Wallet size={20} className="text-green-600" />
              Income & Expenses
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium mb-2 text-gray-700">
                  Monthly Income (₹)
                </label>
                <input
                  type="text"
                  name="monthly_income"
                  value={formData.monthly_income}
                  onChange={handleChange}
                  className="border border-gray-300 rounded-lg p-3 w-full focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-2 text-gray-700">
                  Monthly Expenses (₹)
                </label>
                <input
                  type="text"
                  name="monthly_expenses"
                  value={formData.monthly_expenses}
                  onChange={handleChange}
                  className="border border-gray-300 rounded-lg p-3 w-full focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-2 text-gray-700">
                  Existing EMIs (₹)
                </label>
                <input
                  type="text"
                  name="existing_EMIs"
                  value={formData.existing_EMIs}
                  onChange={handleChange}
                  className="border border-gray-300 rounded-lg p-3 w-full focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  required
                />
              </div>
            </div>
          </div>

          <div className="mb-6">
            <h3 className="text-lg font-semibold mb-4 text-gray-700 flex items-center gap-2">
              <PieChart size={20} className="text-purple-600" />
              Current Wealth
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-2 text-gray-700">
                  Current Savings (₹)
                </label>
                <input
                  type="text"
                  name="current_savings"
                  value={formData.current_savings}
                  onChange={handleChange}
                  className="border border-gray-300 rounded-lg p-3 w-full focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-2 text-gray-700">
                  Current Investments Value (₹)
                </label>
                <input
                  type="text"
                  name="current_investments_value"
                  value={formData.current_investments_value}
                  onChange={handleChange}
                  className="border border-gray-300 rounded-lg p-3 w-full focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  required
                />
              </div>
            </div>
          </div>

          <div>
            <h3 className="text-lg font-semibold mb-4 text-gray-700 flex items-center gap-2">
              <Target size={20} className="text-orange-600" />
              Goal Details
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-2 text-gray-700">
                  Goal Amount (₹)
                </label>
                <input
                  type="text"
                  name="goal_amount"
                  value={formData.goal_amount}
                  onChange={handleChange}
                  className="border border-gray-300 rounded-lg p-3 w-full focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-2 text-gray-700">
                  Goal Duration (years)
                </label>
                <input
                  type="text"
                  name="goal_duration_years"
                  value={formData.goal_duration_years}
                  onChange={handleChange}
                  className="border border-gray-300 rounded-lg p-3 w-full focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  required
                />
              </div>
            </div>
          </div>
        </div>

        <div className="mb-8">
          <button
            onClick={() => callAPI("/api/predict", setResult)}
            className="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white px-8 py-4 rounded-lg font-semibold transition-all duration-200 flex items-center gap-3 text-lg shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed"
            disabled={loading}
          >
            {loading ? (
              <>
                <Activity className="animate-spin" size={24} />
                Calculating Your Personalized Recommendation...
              </>
            ) : (
              <>
                <Calculator size={24} />
                Get My SIP Recommendation
              </>
            )}
          </button>
        </div>

        {error && (
          <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 rounded-lg mb-6 flex items-center gap-3">
            <AlertCircle size={24} /> 
            <div>
              <p className="font-semibold">Error</p>
              <p>{error}</p>
            </div>
          </div>
        )}

        {result && (
          <div className="space-y-6">
            {result.market_conditions && (
              <div className="p-6 bg-gradient-to-r from-indigo-50 to-blue-50 rounded-xl border border-indigo-200 shadow-md">
                <h2 className="text-2xl font-bold flex items-center gap-2 mb-4 text-gray-800">
                  <Activity className="text-indigo-600" /> Market Conditions
                </h2>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div className="bg-white p-4 rounded-lg shadow-sm">
                    <p className="text-sm text-gray-600 mb-1">Inflation Rate</p>
                    <p className="text-3xl font-bold text-red-600">
                      {result.market_conditions.inflation_rate.toFixed(2)}%
                    </p>
                  </div>
                  <div className="bg-white p-4 rounded-lg shadow-sm">
                    <p className="text-sm text-gray-600 mb-1">Repo Rate</p>
                    <p className="text-3xl font-bold text-blue-600">
                      {result.market_conditions.repo_rate.toFixed(2)}%
                    </p>
                  </div>
                  <div className="bg-white p-4 rounded-lg shadow-sm">
                    <p className="text-sm text-gray-600 mb-1">Nifty50 P/E</p>
                    <p className="text-3xl font-bold text-purple-600">
                      {result.market_conditions.Nifty50_PE_ratio.toFixed(1)}
                    </p>
                  </div>
                  <div className="bg-white p-4 rounded-lg shadow-sm">
                    <p className="text-sm text-gray-600 mb-1">GDP Growth</p>
                    <p className="text-3xl font-bold text-green-600">
                      {result.market_conditions.GDP_growth_rate.toFixed(2)}%
                    </p>
                  </div>
                </div>

                {result.inflation_context && (
                  <div className="mt-4 p-4 bg-white rounded-lg shadow-sm">
                    <h3 className="font-semibold text-gray-800 mb-3 flex items-center gap-2">
                      <Percent size={18} />
                      Inflation Trend Analysis (Last 6 Months)
                    </h3>
                    <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
                      <div>
                        <p className="text-xs text-gray-600">Current</p>
                        <p className="text-xl font-bold text-red-600">
                          {result.inflation_context.current.toFixed(2)}%
                        </p>
                      </div>
                      <div>
                        <p className="text-xs text-gray-600">Average</p>
                        <p className="text-xl font-bold text-orange-600">
                          {result.inflation_context.average.toFixed(2)}%
                        </p>
                      </div>
                      <div>
                        <p className="text-xs text-gray-600">Minimum</p>
                        <p className="text-xl font-bold text-green-600">
                          {result.inflation_context.min.toFixed(2)}%
                        </p>
                      </div>
                      <div>
                        <p className="text-xs text-gray-600">Maximum</p>
                        <p className="text-xl font-bold text-red-600">
                          {result.inflation_context.max.toFixed(2)}%
                        </p>
                      </div>
                      <div>
                        <p className="text-xs text-gray-600">Trend</p>
                        <p className="text-xl font-bold text-blue-600 capitalize flex items-center gap-1">
                          {result.inflation_context.trend === "increasing" ? (
                            <TrendingUp size={18} />
                          ) : (
                            <TrendingDown size={18} />
                          )}
                          {result.inflation_context.trend}
                        </p>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            )}

            <div className="p-6 bg-gradient-to-r from-green-50 to-emerald-50 rounded-xl border border-green-200 shadow-md">
              <h2 className="text-2xl font-bold flex items-center gap-2 mb-3 text-gray-800">
                <TrendingUp className="text-green-600" /> Recommended Monthly SIP
              </h2>
              <p className="text-5xl font-bold text-green-600 mb-6">
                ₹{formatCurrency(result.recommended_SIP_amount)}
              </p>

              <div className="mt-4">
                <h3 className="font-semibold text-gray-800 mb-3 flex items-center gap-2 text-lg">
                  <PieChart size={20} /> Asset Allocation Strategy
                </h3>
                <div className="grid grid-cols-3 gap-4">
                  {Object.entries(result.asset_allocation).map(([key, val]) => (
                    <div key={key} className="bg-white p-4 rounded-lg shadow-sm border border-green-100">
                      <p className="text-sm text-gray-600 capitalize mb-1">{key}</p>
                      <p className="text-3xl font-bold text-gray-800">{val}%</p>
                    </div>
                  ))}
                </div>
              </div>

              {result.projections && (
                <div className="mt-6 p-5 bg-white rounded-lg shadow-sm border border-green-100">
                  <h3 className="font-semibold text-gray-800 mb-4 text-lg">
                    Investment Projections
                  </h3>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div>
                      <p className="text-xs text-gray-600 mb-1">Total Investment</p>
                      <p className="text-xl font-bold text-blue-600">
                        ₹{formatCurrency(result.projections.total_investment)}
                      </p>
                    </div>
                    <div>
                      <p className="text-xs text-gray-600 mb-1">Future Value</p>
                      <p className="text-xl font-bold text-green-600">
                        ₹{formatCurrency(result.projections.future_value)}
                      </p>
                    </div>
                    <div>
                      <p className="text-xs text-gray-600 mb-1">Wealth Gain</p>
                      <p className="text-xl font-bold text-purple-600">
                        ₹{formatCurrency(result.projections.wealth_gain)}
                      </p>
                    </div>
                    <div>
                      <p className="text-xs text-gray-600 mb-1">Goal Achievement</p>
                      <p className="text-xl font-bold text-orange-600">
                        {result.projections.goal_achievement}%
                      </p>
                    </div>
                  </div>
                </div>
              )}
            </div>

            <div className="p-6 bg-gray-50 rounded-xl border border-gray-200 shadow-md">
              <h2 className="text-2xl font-bold flex items-center gap-2 mb-4 text-gray-800">
                <DollarSign className="text-blue-600" /> Recommended Funds
              </h2>
              <div className="space-y-3">
                {result.fund_recommendations.map((fund, i) => (
                  <div
                    key={i}
                    className="border border-gray-300 p-5 rounded-lg bg-white shadow-sm hover:shadow-lg transition-shadow"
                  >
                    <div className="flex justify-between items-start">
                      <div className="flex-1">
                        <p className="font-bold text-xl text-gray-800">{fund.name}</p>
                        <p className="text-sm text-gray-600 mt-1">
                          {fund.category} • {fund.sub_category}
                        </p>
                        <div className="flex flex-wrap gap-4 mt-3 text-sm">
                          <span className="text-gray-700 bg-red-50 px-3 py-1 rounded-full">
                            Risk: <strong className="text-red-600">{fund.risk}</strong>
                          </span>
                          <span className="text-gray-700 bg-green-50 px-3 py-1 rounded-full">
                            3Y Returns: <strong className="text-green-600">{fund.returns_3y}%</strong>
                          </span>
                          <span className="text-gray-700 bg-blue-50 px-3 py-1 rounded-full">
                            Expense: <strong className="text-blue-600">{fund.expense_ratio}%</strong>
                          </span>
                        </div>
                      </div>
                      <div className="ml-6 text-right bg-blue-50 p-4 rounded-lg">
                        <p className="text-sm text-gray-600 mb-1">Allocation</p>
                        <p className="text-4xl font-bold text-blue-600">
                          {fund.allocation_percentage}%
                        </p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {result.insights && result.insights.length > 0 && (
              <div className="p-6 bg-yellow-50 rounded-xl border border-yellow-200 shadow-md">
                <h2 className="text-2xl font-bold flex items-center gap-2 mb-4 text-gray-800">
                  <AlertCircle className="text-yellow-600" /> Personalized Insights
                </h2>
                <div className="space-y-3">
                  {result.insights.map((insight, i) => (
                    <div
                      key={i}
                      className={`p-4 rounded-lg border-l-4 flex items-start gap-3 ${getInsightColor(
                        insight.type
                      )}`}
                    >
                      {getInsightIcon(insight.type)}
                      <p className="flex-1 text-sm leading-relaxed">{insight.message}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default SIPRecommender;