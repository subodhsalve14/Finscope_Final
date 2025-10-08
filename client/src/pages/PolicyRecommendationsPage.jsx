import React from 'react';
import Navbar from '../components/Navbar';

const PolicyRecommendationsPage = () => {
    const FLASK_BASE_URL = 'http://127.0.0.1:5000';
    
    return (
        <div className="bg-slate-50 min-h-screen">
            <Navbar />
            <div className="w-full" style={{ height: 'calc(100vh - 64px)' }}>
                <iframe
                    src={`${FLASK_BASE_URL}/policy-recommendations`}
                    title="Policy Recommendations"
                    className="w-full h-full border-0"
                    style={{ display: 'block' }}
                />
            </div>
        </div>
    );
};

export default PolicyRecommendationsPage;
