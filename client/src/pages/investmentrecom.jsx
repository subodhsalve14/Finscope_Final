import React, { useState } from "react";
import {
  Calculator,
  TrendingUp,
  PieChart,
  AlertCircle,
  Scale,
  Target,
  TrendingDown,
  Activity,
  DollarSign,
  Info,
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
    investment_experience: "intermediate",
    need_for_liquidity: 0,
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const API_BASE = "http://127.0.0.1:5001";

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
      setError("Could not connect to Flask backend.");
    } finally {
      setLoading(false);
    }
  };

  const getInsightIcon = (type) => {
    switch (type) {
      case "positive":
        return <TrendingUp className="text-green-600" />;
      case "warning":
        return <AlertCircle className="text-orange-600" />;
      case "info":
        return <Info className="text-blue-600" />;
      case "tip":
        return <Target className="text-purple-600" />;
      default:
        return <Info className="text-gray-600" />;
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

  return (
    <div className="p-6 max-w-6xl mx-auto bg-gradient-to-br from-blue-50 to-indigo-50 min-h-screen">
      <div className="bg-white shadow-2xl rounded-2xl p-8">
        <h1 className="text-3xl font-bold mb-6 flex items-center gap-3 text-gray-800">
          <Calculator className="text-blue-600" size={36} /> 
          SIP Investment Recommender
        </h1>

        {/* Input Form */}
        <form className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
          {Object.entries(formData).map(([key, value]) => (
            <div key={key}>
              <label className="block text-sm font-medium mb-1 capitalize text-gray-700">
                {key.replaceAll("_", " ")}
              </label>
              <input
                type={typeof value === "number" ? "number" : "text"}
                name={key}
                value={value}
                onChange={handleChange}
                className="border border-gray-300 rounded-lg p-2 w-full focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              />
            </div>
          ))}
        </form>

        {/* Buttons */}
        <div className="flex flex-wrap gap-3 mb-6">
          <button
            onClick={() => callAPI("/api/predict", setResult)}
            className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-semibold transition-colors duration-200 flex items-center gap-2"
            disabled={loading}
          >
            {loading ? (
              <>
                <Activity className="animate-spin" size={20} />
                Calculating...
              </>
            ) : (
              <>
                <Calculator size={20} />
                Get Recommendation
              </>
            )}
          </button>
        </div>

        {/* Error */}
        {error && (
          <div className="bg-red-100 border border-red-300 text-red-700 p-4 rounded-lg mb-4 flex items-center gap-2">
            <AlertCircle /> {error}
          </div>
        )}

        {/* Results Section */}
        {result && (
          <div className="space-y-6">
            {/* Market Conditions & Inflation */}
            {result.market_conditions && (
              <div className="p-6 bg-gradient-to-r from-indigo-50 to-blue-50 rounded-xl border border-indigo-200">
                <h2 className="text-xl font-bold flex items-center gap-2 mb-4 text-gray-800">
                  <Activity className="text-indigo-600" /> Market Conditions
                </h2>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div className="bg-white p-3 rounded-lg shadow-sm">
                    <p className="text-sm text-gray-600">Inflation Rate</p>
                    <p className="text-2xl font-bold text-red-600">
                      {result.market_conditions.inflation_rate.toFixed(2)}%
                    </p>
                  </div>
                  <div className="bg-white p-3 rounded-lg shadow-sm">
                    <p className="text-sm text-gray-600">Repo Rate</p>
                    <p className="text-2xl font-bold text-blue-600">
                      {result.market_conditions.repo_rate.toFixed(2)}%
                    </p>
                  </div>
                  <div className="bg-white p-3 rounded-lg shadow-sm">
                    <p className="text-sm text-gray-600">Nifty50 P/E</p>
                    <p className="text-2xl font-bold text-purple-600">
                      {result.market_conditions.Nifty50_PE_ratio.toFixed(1)}
                    </p>
                  </div>
                  <div className="bg-white p-3 rounded-lg shadow-sm">
                    <p className="text-sm text-gray-600">GDP Growth</p>
                    <p className="text-2xl font-bold text-green-600">
                      {result.market_conditions.GDP_growth_rate.toFixed(2)}%
                    </p>
                  </div>
                </div>

                {/* Inflation Context */}
                {result.inflation_context && (
                  <div className="mt-4 p-4 bg-white rounded-lg shadow-sm">
                    <h3 className="font-semibold text-gray-800 mb-2">
                      Inflation Trend Analysis (Last 6 Months)
                    </h3>
                    <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
                      <div>
                        <p className="text-xs text-gray-600">Current</p>
                        <p className="text-lg font-bold text-red-600">
                          {result.inflation_context.current.toFixed(2)}%
                        </p>
                      </div>
                      <div>
                        <p className="text-xs text-gray-600">Average</p>
                        <p className="text-lg font-bold text-orange-600">
                          {result.inflation_context.average.toFixed(2)}%
                        </p>
                      </div>
                      <div>
                        <p className="text-xs text-gray-600">Minimum</p>
                        <p className="text-lg font-bold text-green-600">
                          {result.inflation_context.min.toFixed(2)}%
                        </p>
                      </div>
                      <div>
                        <p className="text-xs text-gray-600">Maximum</p>
                        <p className="text-lg font-bold text-red-600">
                          {result.inflation_context.max.toFixed(2)}%
                        </p>
                      </div>
                      <div>
                        <p className="text-xs text-gray-600">Trend</p>
                        <p className="text-lg font-bold text-blue-600 capitalize flex items-center gap-1">
                          {result.inflation_context.trend === "increasing" ? (
                            <TrendingUp size={16} />
                          ) : (
                            <TrendingDown size={16} />
                          )}
                          {result.inflation_context.trend}
                        </p>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* SIP Recommendation */}
            <div className="p-6 bg-gradient-to-r from-green-50 to-emerald-50 rounded-xl border border-green-200">
              <h2 className="text-xl font-bold flex items-center gap-2 mb-3 text-gray-800">
                <TrendingUp className="text-green-600" /> Recommended Monthly SIP
              </h2>
              <p className="text-4xl font-bold text-green-600 mb-4">
                ₹{result.recommended_SIP_amount.toLocaleString()}
              </p>

              {/* Asset Allocation */}
              <div className="mt-4">
                <h3 className="font-semibold text-gray-800 mb-2 flex items-center gap-2">
                  <PieChart size={18} /> Asset Allocation
                </h3>
                <div className="grid grid-cols-3 gap-3">
                  {Object.entries(result.asset_allocation).map(([key, val]) => (
                    <div key={key} className="bg-white p-3 rounded-lg shadow-sm">
                      <p className="text-sm text-gray-600 capitalize">{key}</p>
                      <p className="text-2xl font-bold text-gray-800">{val}%</p>
                    </div>
                  ))}
                </div>
              </div>

              {/* Projections */}
              {result.projections && (
                <div className="mt-4 p-4 bg-white rounded-lg shadow-sm">
                  <h3 className="font-semibold text-gray-800 mb-3">
                    Investment Projections
                  </h3>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                    <div>
                      <p className="text-xs text-gray-600">Total Investment</p>
                      <p className="text-lg font-bold text-blue-600">
                        ₹{result.projections.total_investment.toLocaleString()}
                      </p>
                    </div>
                    <div>
                      <p className="text-xs text-gray-600">Future Value</p>
                      <p className="text-lg font-bold text-green-600">
                        ₹{result.projections.future_value.toLocaleString()}
                      </p>
                    </div>
                    <div>
                      <p className="text-xs text-gray-600">Wealth Gain</p>
                      <p className="text-lg font-bold text-purple-600">
                        ₹{result.projections.wealth_gain.toLocaleString()}
                      </p>
                    </div>
                    <div>
                      <p className="text-xs text-gray-600">Goal Achievement</p>
                      <p className="text-lg font-bold text-orange-600">
                        {result.projections.goal_achievement}%
                      </p>
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Fund Recommendations */}
            <div className="p-6 bg-gray-50 rounded-xl border border-gray-200">
              <h2 className="text-xl font-bold flex items-center gap-2 mb-4 text-gray-800">
                <DollarSign className="text-blue-600" /> Recommended Funds
              </h2>
              <div className="space-y-3">
                {result.fund_recommendations.map((fund, i) => (
                  <div
                    key={i}
                    className="border border-gray-200 p-4 rounded-lg bg-white shadow-sm hover:shadow-md transition-shadow"
                  >
                    <div className="flex justify-between items-start">
                      <div className="flex-1">
                        <p className="font-bold text-lg text-gray-800">{fund.name}</p>
                        <p className="text-sm text-gray-600 mt-1">
                          {fund.category} • {fund.sub_category}
                        </p>
                        <div className="flex gap-4 mt-2 text-sm">
                          <span className="text-gray-700">
                            Risk: <strong className="text-red-600">{fund.risk}</strong>
                          </span>
                          <span className="text-gray-700">
                            3Y Returns: <strong className="text-green-600">{fund.returns_3y}%</strong>
                          </span>
                          <span className="text-gray-700">
                            Expense Ratio: <strong>{fund.expense_ratio}%</strong>
                          </span>
                        </div>
                      </div>
                      <div className="ml-4 text-right">
                        <p className="text-sm text-gray-600">Allocation</p>
                        <p className="text-3xl font-bold text-blue-600">
                          {fund.allocation_percentage}%
                        </p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Insights */}
            {result.insights && result.insights.length > 0 && (
              <div className="p-6 bg-yellow-50 rounded-xl border border-yellow-200">
                <h2 className="text-xl font-bold flex items-center gap-2 mb-4 text-gray-800">
                  <AlertCircle className="text-yellow-600" /> Personalized Insights
                </h2>
                <div className="space-y-3">
                  {result.insights.map((insight, i) => (
                    <div
                      key={i}
                      className={`p-4 rounded-lg border flex items-start gap-3 ${getInsightColor(
                        insight.type
                      )}`}
                    >
                      {getInsightIcon(insight.type)}
                      <p className="flex-1">{insight.message}</p>
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