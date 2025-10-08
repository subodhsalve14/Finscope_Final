import React from 'react';
import Navbar from '../components/Navbar';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';

const modules = [
  {
    title: 'Economic Trend Analyzer',
    icon: '📊',
    description: 'Shows users historical + forecasted economic indicators like inflation, GDP, interest rates that directly affect their savings, investments, and insurance premiums.',
    tech: 'Time-series forecasting models → ARIMA, Facebook Prophet.',
    benefit: 'Helps users see how inflation erodes money value and how GDP/interest rates affect their policies/investments.',
  },
  {
    title: 'Insurance Policy Analyzer & Gap Finder',
    icon: '🛡️',
    description: 'Reads user’s uploaded insurance policy PDF, extracts key details (premium, coverage, riders), and checks if coverage matches their life stage & income.',
    tech: 'NLP (LLM / LangChain + pdfplumber) → extract policy details.',
    benefit: 'Removes dependency on agents who often mis-sell, gives unbiased, data-driven analysis.',
  },
  {
    title: 'Premium Affordability Calculator',
    icon: '🧮',
    description: 'Helps middle-class users check whether their insurance premiums fit into their budget. Prevents over-buying policies that strain monthly income.',
    tech: 'Rule-based affordability rule: Premium ≤ 10–15% of monthly income.',
    benefit: 'Makes financial planning practical & family-friendly.',
  },
  {
    title: 'Investment Portfolio Advisor',
    icon: '💹',
    description: 'Recommends personalized portfolios (SIP, mutual funds, FD, gold) based on user’s goals, risk profile, and inflation forecast.',
    tech: 'Risk profiling → clustering / decision tree.',
    benefit: 'Ensures users don’t just invest blindly but know future real growth of money.',
  },
];

const AboutPage = () => {
  return (
    <div className="bg-slate-50 min-h-screen">
      <Navbar />
      <div className="container mx-auto p-8">
        <header className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-800">
            🌐 Forecasting & Personalized Financial Wellness Platform
          </h1>
          <p className="text-lg text-gray-600 mt-4 max-w-3xl mx-auto">
            A fintech web platform that helps individuals and families make smarter financial decisions by combining economic forecasting, insurance gap detection, investment advising, and affordability analysis.
          </p>
        </header>

        <section>
          <h2 className="text-3xl font-bold text-center text-gray-800 mb-8">📌 Modules Breakdown</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {modules.map((mod, index) => (
              <Card key={index} className="shadow-lg hover:shadow-xl transition-shadow duration-300">
                <CardHeader>
                  <CardTitle className="flex items-center text-2xl">
                    <span className="text-3xl mr-3">{mod.icon}</span>
                    {mod.title}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-gray-700 mb-4">{mod.description}</p>
                  <p className="text-sm text-gray-600 mb-2"><strong className="font-semibold">ML/Tech Used:</strong> {mod.tech}</p>
                  <p className="text-sm text-green-700 bg-green-100 p-2 rounded">👉 {mod.benefit}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </section>

        <section className="mt-16">
          <h2 className="text-3xl font-bold text-center text-gray-800 mb-8">🔄 Project Flow</h2>
          <div className="bg-white p-6 rounded-lg shadow-md">
            <ul className="list-decimal list-inside space-y-3 text-gray-700">
              <li>User Login/Register (via website).</li>
              <li>Upload Policy PDF + Enter Personal & Financial Details (income, expenses, dependents, goals).</li>
              <li>Backend Processing: NLP extracts policy, forecasts trends, checks affordability, and advises on portfolios.</li>
              <li>Dashboard Output: Graphs, policy insights, affordability status, and investment suggestions are displayed.</li>
              <li>Downloadable Report with charts + insights.</li>
            </ul>
          </div>
        </section>

        <div className="grid md:grid-cols-2 gap-8 mt-16">
            <section>
              <h2 className="text-3xl font-bold text-center text-gray-800 mb-8">🎯 Target Users</h2>
              <div className="bg-white p-6 rounded-lg shadow-md h-full">
                <ul className="list-disc list-inside space-y-2 text-gray-700">
                  <li>Middle-class individuals/families concerned about premiums & affordability.</li>
                  <li>Young professionals wanting investment + insurance advice.</li>
                  <li>Financially aware users who want independent, data-driven advice.</li>
                </ul>
              </div>
            </section>

            <section>
              <h2 className="text-3xl font-bold text-center text-gray-800 mb-8">🚀 Why It’s a Major Project</h2>
              <div className="bg-white p-6 rounded-lg shadow-md h-full">
                <ul className="list-disc list-inside space-y-2 text-gray-700">
                  <li>An end-to-end fintech ecosystem, not just a single module.</li>
                  <li>Uses diverse techniques like ML models, NLP, and forecasting.</li>
                  <li>Solves a genuine problem: financial literacy and independent decision-making.</li>
                  <li>User-centric, with clear visuals (graphs, dashboards).</li>
                </ul>
              </div>
            </section>
        </div>

      </div>
    </div>
  );
};

export default AboutPage;
