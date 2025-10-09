import React from 'react'
import { Button } from './components/ui/button'
import { BrowserRouter, Route, Routes } from 'react-router-dom'
import HomePage from './pages/HomePage'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import Dashboard from './pages/Dashboard'
import { Toaster } from './components/ui/toaster'
import AboutPage from './pages/AboutPage'
import EconomicTrendAnalyzerPage from './pages/EconomicTrendAnalyzerPage'
import InsurancePolicyAnalyzerPage from './pages/InsurancePolicyAnalyzerPage'
import PremiumAffordabilityCalculatorPage from './pages/PremiumAffordabilityCalculatorPage'
import InvestmentPortfolioAdvisorPage from './pages/InvestmentPortfolioAdvisorPage'
import InflationForecastPage from './pages/InflationForecastPage'
import GdpForecastPage from './pages/GdpForecastPage'
import InterestRatesForecastPage from './pages/InterestRatesForecastPage'
import PolicyRecommendationsPage from './pages/PolicyRecommendationsPage'
import FinancialAdvisorPage from './pages/FinancialAdvisorPage'
import SIPRecommender from './pages/investmentrecom'

const App = () => {
    return (
        <div>
             <Toaster />
            <BrowserRouter>
                <Routes>
                    <Route index element={<HomePage />} />
                    <Route path='/login' element={<LoginPage />} />
                    <Route path='/register' element={<RegisterPage />} />
                    <Route path='/dashboard' element={<Dashboard />} />
                    <Route path='/about' element={<AboutPage />} />
                    <Route path='/economic-trend-analyzer' element={<EconomicTrendAnalyzerPage />} />
                    <Route path='/insurance-policy-analyzer' element={<InsurancePolicyAnalyzerPage />} />
                    <Route path='/premium-affordability-calculator' element={<PremiumAffordabilityCalculatorPage />} />
                    <Route path='/investment-portfolio-advisor' element={<InvestmentPortfolioAdvisorPage />} />
                    <Route path='/inflation-forecast' element={<InflationForecastPage />} />
                    <Route path='/gdp-forecast' element={<GdpForecastPage />} />
                    <Route path='/interest-rates-forecast' element={<InterestRatesForecastPage />} />
                    <Route path='/policy-recommendations' element={<PolicyRecommendationsPage />} />
                    <Route path='/financial-advisor' element={<FinancialAdvisorPage />} />
                    <Route path='/investmentrecom' element={<SIPRecommender/>} />
                </Routes>
            </BrowserRouter>
        </div>
    )
}

export default App