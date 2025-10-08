import React, { useEffect, useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import Navbar from '../components/Navbar';

const styles = `
.hero-section { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 60px 30px; text-align: center; color: white; }
.hero-section h1 { font-size: 3rem; margin-bottom: 15px; font-weight: bold; }
.hero-section p { font-size: 1.3rem; margin-bottom: 30px; opacity: 0.9; }
.tools-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 30px; padding: 50px 30px; max-width: 1400px; margin: 0 auto; }
.tool-card { background: white; border-radius: 15px; padding: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); transition: all 0.3s ease; cursor: pointer; text-decoration: none; color: inherit; display: block; border: 3px solid transparent; }
.tool-card:hover { transform: translateY(-10px); box-shadow: 0 15px 40px rgba(0,0,0,0.2); border-color: #667eea; }
.tool-icon { font-size: 4rem; margin-bottom: 20px; display: block; }
.tool-card h2 { color: #2e7d32; font-size: 1.8rem; margin-bottom: 15px; }
.tool-card p { color: #666; font-size: 1.1rem; line-height: 1.6; margin-bottom: 20px; }
.tool-features { list-style: none; padding: 0; margin: 20px 0; }
.tool-features li { padding: 8px 0; color: #555; border-bottom: 1px solid #f0f0f0; }
.tool-features li:before { content: "✓ "; color: #4caf50; font-weight: bold; margin-right: 10px; }
.cta-button { display: inline-block; background: linear-gradient(135deg, #1f77b4 0%, #2e7d32 100%); color: white; padding: 12px 30px; border-radius: 25px; font-weight: bold; text-decoration: none; transition: all 0.3s; }
.cta-button:hover { transform: scale(1.05); box-shadow: 0 5px 15px rgba(31, 119, 180, 0.4); }
.tool-card.inflation { border-top: 5px solid #ff6b6b; }
.tool-card.gdp { border-top: 5px solid #4ecdc4; }
.tool-card.interest { border-top: 5px solid #f7b731; }
.tool-card.policy { border-top: 5px solid #5f27cd; }
.tool-card.advisor { border-top: 5px solid #00d2d3; }
.footer { background: #2c3e50; color: white; text-align: center; padding: 30px; margin-top: 50px; }
.stats-section { background: #f8f9fa; padding: 40px 30px; text-align: center; }
.stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 30px; max-width: 1200px; margin: 30px auto 0; }
.stat-item { background: white; padding: 25px; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
.stat-number { font-size: 2.5rem; font-weight: bold; color: #1f77b4; margin-bottom: 10px; }
.stat-label { color: #666; font-size: 1.1rem; }
`;

const Card = ({ to, icon, title, desc, features, modifier, ctaText }) => (
    <Link to={to} className={`tool-card ${modifier || ''}`}>
        <span className="tool-icon" aria-hidden>
            {icon}
        </span>
        <h2>{title}</h2>
        <p>{desc}</p>
        <ul className="tool-features">
            {features.map((f, i) => (
                <li key={i}>{f}</li>
            ))}
        </ul>
        <span className="cta-button">{ctaText || 'View Forecast →'}</span>
    </Link>
);

const Dashboard = () => {
    const baseUrl = import.meta.env.VITE_API_BASE_URL;
    const navigate = useNavigate();
    const [user, setUser] = useState(null);

    useEffect(() => {
        const getUser = async () => {
            try {
                const response = await fetch(`${baseUrl}/api/auth/get-user`, {
                    credentials: 'include'
                });
                const data = await response.json();
                if (!data.status) {
                    navigate('/login');
                    return;
                }
                setUser(data.user);
            } catch (err) {
                console.error('Failed to fetch user', err);
                navigate('/login');
            }
        };
        getUser();
    }, [baseUrl, navigate]);

    if (!user) {
        return (
            <div className="flex justify-center items-center h-screen">
                <div className="text-xl">Loading....</div>
            </div>
        );
    }

    return (
        <div className="bg-slate-50 min-h-screen">
            <style>{styles}</style>
            <Navbar />
            <div className="container mx-auto p-8">
                {/* Welcome Banner */}
                <div className="bg-white rounded-lg shadow-md p-6 mb-8">
                    <h1 className="text-3xl font-bold text-gray-800">Welcome, {user.name}!</h1>
                    <p className="text-gray-600 mt-2">We're glad to have you here. Explore the features below to manage your finances.</p>
                </div>

                {/* Converted Hero, Stats, Tools */}
                <div>
                    <div className="hero-section">
                        <h1>🏦 Financial Wellness Dashboard</h1>
                        <p>Your Complete Financial Analysis & Planning Platform</p>
                        <p style={{ fontSize: '1rem', opacity: 0.8 }}>Make informed decisions with AI-powered forecasts and personalized recommendations</p>
                    </div>

                    <div className="stats-section">
                        <h2 style={{ color: '#2e7d32', marginBottom: 10 }}>Comprehensive Financial Insights</h2>
                        <div className="stats-grid">
                            <div className="stat-item">
                                <div className="stat-number">5</div>
                                <div className="stat-label">Analysis Tools</div>
                            </div>
                            <div className="stat-item">
                                <div className="stat-number">12</div>
                                <div className="stat-label">Month Forecasts</div>
                            </div>
                            <div className="stat-item">
                                <div className="stat-number">AI</div>
                                <div className="stat-label">Powered Insights</div>
                            </div>
                            <div className="stat-item">
                                <div className="stat-number">24/7</div>
                                <div className="stat-label">Access</div>
                            </div>
                        </div>
                    </div>

                    <div className="tools-grid">


                        <Card
                            to="/financial-advisor"
                            icon={<span>💡</span>}
                            title="Financial Advisor"
                            desc="Comprehensive financial planning and analysis tool"
                            features={["Coverage adequacy check", "Premium affordability analysis", "Financial health scoring", "Detailed action plans"]}
                            modifier="advisor"
                            ctaText="Start Analysis →"
                        />

                        <Card
                            to="/inflation-forecast"
                            icon={<span>📈</span>}
                            title="Inflation Forecast"
                            desc="Track and predict inflation trends with advanced AI models"
                            features={["12-month inflation predictions", "Historical trend analysis", "Interactive visualizations", "Confidence intervals"]}
                            modifier="inflation"
                            ctaText="View Forecast →"
                        />

                        <Card
                            to="/gdp-forecast"
                            icon={<span>📊</span>}
                            title="GDP Growth Forecast"
                            desc="Analyze economic growth patterns and future projections"
                            features={["Quarterly GDP predictions", "Growth rate analysis", "Economic trend insights", "Data-driven forecasts"]}
                            modifier="gdp"
                        />

                        <Card
                            to="/interest-rates-forecast"
                            icon={<span>💰</span>}
                            title="Interest Rates Forecast"
                            desc="Predict lending and deposit rate movements"
                            features={["Multiple rate predictions", "Repo, bond & loan rates", "Rate change analysis", "Financial planning support"]}
                            modifier="interest"
                        />

                        <Card
                            to="/policy-recommendations"
                            icon={<span>🔍</span>}
                            title="Policy Recommendations"
                            desc="Get personalized insurance policy suggestions"
                            features={["Risk assessment analysis", "Personalized recommendations", "Coverage optimization", "AI-powered insights"]}
                            modifier="policy"
                            ctaText="Get Recommendations →"
                        />

                    </div>

                    <div className="footer">
                        <h3>🌟 Make Smarter Financial Decisions Today</h3>
                        <p style={{ marginTop: 15, opacity: 0.8 }}>
                            All forecasts and recommendations are based on advanced AI models and historical data analysis.
                            <br />
                            For personalized financial advice, please consult with a certified financial planner.
                        </p>
                        <p style={{ marginTop: 20, fontSize: '0.9rem' }}>
                            © 2025 Financial Wellness Dashboard. All rights reserved.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;