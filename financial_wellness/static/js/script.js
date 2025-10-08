// Update slider values dynamically
function updateValue(id) {
    const element = document.getElementById(id);
    const valueElement = document.getElementById(`${id}-value`);
    
    if (id === 'inflation_rate') {
        valueElement.textContent = `${element.value}%`;
    } else {
        valueElement.textContent = element.value;
    }
}

// Format currency in Indian Rupees
function formatCurrency(amount) {
    return '₹' + amount.toLocaleString('en-IN', { maximumFractionDigits: 0 });
}

// Format number with decimals
function formatNumber(num, decimals = 1) {
    return num.toFixed(decimals);
}

// Get form data
function getFormData() {
    const form = document.getElementById('financialForm');
    const formData = new FormData(form);
    const data = {};
    
    for (let [key, value] of formData.entries()) {
        data[key] = value;
    }
    
    return data;
}

// Handle form submission
document.getElementById('financialForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Show loading
    document.getElementById('loading').style.display = 'block';
    document.getElementById('results').style.display = 'none';
    document.getElementById('detailed-report').style.display = 'none';
    
    // Get form data
    const formData = getFormData();
    
    try {
        // Send data to backend
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        const result = await response.json();
        
        if (result.success) {
            displayResults(result.analysis, formData);
        } else {
            alert('Error: ' + result.error);
        }
    } catch (error) {
        alert('An error occurred: ' + error.message);
    } finally {
        // Hide loading
        document.getElementById('loading').style.display = 'none';
    }
});

// Display results
function displayResults(analysis, formData) {
    // Show results section
    document.getElementById('results').style.display = 'block';
    
    // Coverage Analysis
    document.getElementById('current-coverage-display').textContent = formatCurrency(parseFloat(formData.current_coverage));
    document.getElementById('coverage-multiplier').textContent = `${formatNumber(parseFloat(formData.current_coverage) / parseFloat(formData.annual_income))}x income`;
    document.getElementById('recommended-min').textContent = formatCurrency(analysis.recommended_min);
    document.getElementById('coverage-gap').textContent = formatCurrency(analysis.coverage_gap);
    
    const coverageStatus = analysis.is_underinsured ? '⚠️ Underinsured' : '✅ Adequate';
    document.getElementById('coverage-status').textContent = coverageStatus;
    
    // Coverage Alert
    const coverageAlert = document.getElementById('coverage-alert');
    if (analysis.is_underinsured) {
        coverageAlert.innerHTML = `
            <div class="warning">
                <strong>⚠️ Coverage Gap Alert:</strong><br>
                You are underinsured by ${formatCurrency(analysis.coverage_gap)}. Consider increasing your coverage to protect your family's financial future.
            </div>
        `;
    } else {
        coverageAlert.innerHTML = `
            <div class="recommendation">
                <strong>✅ Coverage Status:</strong><br>
                Your current coverage is adequate based on the 10x income rule.
            </div>
        `;
    }
    
    // Premium Analysis
    document.getElementById('current-premium-display').textContent = formatCurrency(parseFloat(formData.annual_premium));
    document.getElementById('premium-percentage').textContent = `${formatNumber(analysis.premium_percentage)}% of income`;
    document.getElementById('max-affordable').textContent = formatCurrency(analysis.max_affordable_premium);
    document.getElementById('additional-capacity').textContent = formatCurrency(analysis.additional_premium_capacity);
    
    const premiumInfo = document.getElementById('premium-info');
    premiumInfo.innerHTML = `
        <strong>Premium Affordability:</strong> ${analysis.affordability_status}<br>
        You can afford an additional ${formatCurrency(analysis.additional_premium_capacity)} in annual premiums for enhanced coverage.
    `;
    
    // Rider Analysis
    document.getElementById('ci-current').textContent = formatCurrency(parseFloat(formData.critical_illness));
    document.getElementById('ci-recommended').textContent = formatCurrency(analysis.recommended_ci);
    document.getElementById('accident-current').textContent = formatCurrency(parseFloat(formData.accident_cover));
    document.getElementById('ci-gap').textContent = formatCurrency(analysis.ci_gap);
    
    // Financial Health Scores
    document.getElementById('coverage-score').textContent = `${formatNumber(analysis.coverage_score)}/10`;
    document.getElementById('premium-score').textContent = `${formatNumber(analysis.premium_score)}/10`;
    document.getElementById('debt-score').textContent = `${formatNumber(analysis.debt_score)}/10`;
    document.getElementById('savings-score').textContent = `${formatNumber(analysis.savings_score)}/10`;
    
    const overallScoreText = analysis.overall_score >= 8 ? 'Excellent' : analysis.overall_score >= 6 ? 'Good' : 'Needs Improvement';
    document.getElementById('overall-score').innerHTML = `${formatNumber(analysis.overall_score)}/10 <small>(${overallScoreText})</small>`;
    
    // Key Metrics
    document.getElementById('monthly-savings').textContent = formatCurrency(analysis.net_savings / 12);
    document.getElementById('savings-rate').textContent = `${formatNumber(analysis.savings_rate)}%`;
    document.getElementById('debt-to-income').textContent = `${formatNumber(analysis.debt_to_income)}x`;
    
    // Recommendations
    const recommendationsList = document.getElementById('recommendations-list');
    recommendationsList.innerHTML = '';
    
    analysis.recommendations.forEach((rec, index) => {
        const recDiv = document.createElement('div');
        recDiv.className = 'recommendation';
        recDiv.innerHTML = `<strong>${index + 1}.</strong> ${rec}`;
        recommendationsList.appendChild(recDiv);
    });
    
    // Future Planning
    document.getElementById('current-expenses').textContent = formatCurrency(analysis.annual_expenses);
    document.getElementById('future-expenses').textContent = formatCurrency(analysis.future_expenses_10y);
    
    const increasePercent = ((analysis.future_expenses_10y / analysis.annual_expenses - 1) * 100).toFixed(1);
    document.getElementById('expense-increase').textContent = `+${increasePercent}%`;
    
    // Scroll to results
    document.getElementById('results').scrollIntoView({ behavior: 'smooth' });
}

// Generate detailed report
document.addEventListener('DOMContentLoaded', () => {
    const generateReportBtn = document.getElementById('generateReport');
    
    if (generateReportBtn) {
        generateReportBtn.addEventListener('click', async () => {
            const formData = getFormData();
            
            generateReportBtn.textContent = '⏳ Generating...';
            generateReportBtn.disabled = true;
            
            try {
                const response = await fetch('/generate-report', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(formData)
                });
                
                const result = await response.json();
                
                if (result.success) {
                    // Display report
                    document.getElementById('detailed-report').style.display = 'block';
                    document.getElementById('report-content').textContent = result.report;
                    
                    // Store report for download
                    window.currentReport = result.report;
                    
                    // Scroll to report
                    document.getElementById('detailed-report').scrollIntoView({ behavior: 'smooth' });
                } else {
                    alert('Error: ' + result.error);
                }
            } catch (error) {
                alert('An error occurred: ' + error.message);
            } finally {
                generateReportBtn.textContent = '📄 Generate Detailed Summary Report';
                generateReportBtn.disabled = false;
            }
        });
    }
    
    // Download report
    const downloadReportBtn = document.getElementById('downloadReport');
    
    if (downloadReportBtn) {
        downloadReportBtn.addEventListener('click', () => {
            if (!window.currentReport) {
                alert('Please generate a report first');
                return;
            }
            
            const formData = getFormData();
            const filename = `financial_analysis_report_${formData.age}yr.md`;
            
            const blob = new Blob([window.currentReport], { type: 'text/markdown' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        });
    }
});

// Initialize slider values on page load
window.addEventListener('DOMContentLoaded', () => {
    updateValue('age');
    updateValue('inflation_rate');
});
