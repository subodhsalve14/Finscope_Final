from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from huggingface_hub import login
import torch
import os

# Suppress warnings
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

# Authenticate
login("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")

# Use a better model for financial analysis (GPT-Neo is better than DialoGPT for this)
model_name = "EleutherAI/gpt-neo-1.3B"  # Better for analysis tasks

print("Loading model... This may take a few minutes...")

# Load model with proper parameters
tokenizer = AutoTokenizer.from_pretrained(model_name, token=True)
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(
    model_name, 
    token=True,
    torch_dtype=torch.float32,  # Use float32 for CPU
    low_cpu_mem_usage=True      # Optimize memory usage
)

print("Model loaded successfully!")

# Enhanced generator setup
generator = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    device=-1  # CPU
)

def create_focused_prompt(section="coverage"):
    """Create focused prompts for each section to avoid repetition"""
    
    base_data = """
Client Profile: 32-year-old married male, 2 dependents
Income: ₹8,00,000 annually (₹66,667 monthly)
Expenses: ₹40,000 monthly (₹4,80,000 annually)  
Current Policy: ₹50,00,000 term life insurance, ₹25,000 annual premium
Riders: ₹10,00,000 accident benefit, ₹5,00,000 critical illness
Home Loan: ₹20,00,000 outstanding
Expected Inflation: 6.5%
"""

    if section == "coverage":
        return f"""As a financial advisor, analyze this client's life insurance coverage adequacy:

{base_data}

Coverage Analysis:
• Standard recommendation: 10-15x annual income = ₹80,00,000 to ₹1,20,00,000
• Current coverage: ₹50,00,000 (6.25x income)
• Assessment: UNDERINSURED by ₹30,00,000 to ₹70,00,000
• Risk factors: Home loan ₹20,00,000 + 2 dependents

Recommendation: Increase coverage to ₹80,00,000 minimum."""

    elif section == "premium":
        return f"""Analyze premium affordability and optimization:

{base_data}

Premium Analysis:
• Current premium: ₹25,000 (3.1% of income) - AFFORDABLE
• Recommended limit: <10% of income (₹80,000 max)
• Additional premium capacity: ₹55,000 available

Optimization: Can afford 3x more coverage within budget."""

    elif section == "inflation":
        return f"""Provide inflation protection strategy:

{base_data}

Inflation Impact (6.5% annually):
• Today's ₹40,000 monthly expenses = ₹88,000 in 10 years
• Current coverage adequacy will erode over time
• Need systematic coverage increases

Strategy: Increase coverage by 10% every 3 years."""

def generate_comprehensive_analysis():
    """Generate analysis section by section"""
    
    print("=" * 80)
    print("COMPREHENSIVE FINANCIAL ADVISORY REPORT")
    print("=" * 80)
    
    sections = {
        "1. COVERAGE ADEQUACY ASSESSMENT": "coverage",
        "2. PREMIUM AFFORDABILITY ANALYSIS": "premium", 
        "3. INFLATION PROTECTION STRATEGY": "inflation"
    }
    
    full_report = ""
    
    for title, section_type in sections.items():
        print(f"\nGenerating {title}...")
        
        prompt = create_focused_prompt(section_type)
        
        try:
            response = generator(
                prompt,
                max_new_tokens=200,         # Shorter responses to avoid repetition
                do_sample=True,
                temperature=0.2,            # Very focused
                top_k=30,
                top_p=0.8,
                repetition_penalty=1.5,     # Strong anti-repetition
                pad_token_id=tokenizer.eos_token_id,
                truncation=True,
                return_full_text=False,      # Only new text
                clean_up_tokenization_spaces=True
            )
            
            generated_text = response[0]['generated_text'].strip()
            
            # Clean up the response
            lines = generated_text.split('\n')
            clean_lines = []
            seen_lines = set()
            
            for line in lines:
                line = line.strip()
                if line and line not in seen_lines and len(line) > 10:
                    clean_lines.append(line)
                    seen_lines.add(line)
                if len(clean_lines) >= 5:  # Limit to 5 meaningful lines
                    break
            
            section_content = '\n'.join(clean_lines)
            
        except Exception as e:
            section_content = f"Error generating {section_type}: {str(e)}"
        
        full_report += f"\n{title}\n{'-' * len(title)}\n{section_content}\n"
        print(f"✓ {title} completed")
    
    return full_report

# Alternative: Rule-based analysis (more reliable)
def generate_rule_based_analysis():
    """Generate analysis using financial rules rather than AI"""
    
    # Client data
    annual_income = 800000
    monthly_expenses = 40000
    current_coverage = 5000000
    annual_premium = 25000
    home_loan = 2000000
    age = 32
    dependents = 2
    
    # Calculations
    annual_expenses = monthly_expenses * 12
    recommended_min = annual_income * 10
    recommended_max = annual_income * 15
    premium_percentage = (annual_premium / annual_income) * 100
    
    # Coverage gap
    coverage_gap = max(0, recommended_min - current_coverage)
    
    # Future expenses with inflation
    inflation_rate = 0.065
    future_expenses_10y = annual_expenses * ((1 + inflation_rate) ** 10)
    
    report = f"""
╔══════════════════════════════════════════════════════════════════════╗
║                    FINANCIAL ADVISORY ANALYSIS REPORT               ║
╚══════════════════════════════════════════════════════════════════════╝

1. COVERAGE ADEQUACY ASSESSMENT
─────────────────────────────────────────
• Current Coverage: ₹{current_coverage:,} ({current_coverage/annual_income:.1f}x income)
• Recommended Range: ₹{recommended_min:,} - ₹{recommended_max:,} (10-15x income)
• Assessment: {"UNDERINSURED" if coverage_gap > 0 else "ADEQUATE"}
• Coverage Gap: ₹{coverage_gap:,}
• Risk Factors: Home loan ₹{home_loan:,} + {dependents} dependents

RECOMMENDATION: {"Increase coverage by ₹" + f"{coverage_gap:,}" if coverage_gap > 0 else "Current coverage is adequate"}

2. PREMIUM AFFORDABILITY ANALYSIS  
─────────────────────────────────────────
• Current Premium: ₹{annual_premium:,} ({premium_percentage:.1f}% of income)
• Affordability: {"HIGHLY AFFORDABLE" if premium_percentage < 5 else "AFFORDABLE" if premium_percentage < 10 else "HIGH"}
• Maximum Recommended: ₹{annual_income * 0.1:,} (10% of income)
• Additional Capacity: ₹{(annual_income * 0.1) - annual_premium:,}

RECOMMENDATION: You can afford additional ₹{(annual_income * 0.1) - annual_premium:,} in premiums for more coverage

3. RIDER ANALYSIS
─────────────────────────────────────────
• Critical Illness Cover: ₹5,00,000 (Current)
• Recommended CI Cover: ₹{annual_income * 3:,} (3x income)
• Accidental Death: ₹10,00,000 (Adequate - 2x base cover)

RECOMMENDATION: Increase Critical Illness cover to ₹{annual_income * 3:,}

4. INFLATION PROTECTION STRATEGY
─────────────────────────────────────────
• Current Annual Expenses: ₹{annual_expenses:,}
• Expenses in 10 years (6.5% inflation): ₹{future_expenses_10y:,}
• Inflation Impact: {((future_expenses_10y/annual_expenses - 1) * 100):.1f}% increase

STRATEGIES:
a) Increase coverage by 8-10% every 3 years
b) Start SIP of ₹15,000/month in equity mutual funds  
c) Maximize PPF contribution (₹1.5L annually)
d) Consider ULIP with top-up facility

5. IMMEDIATE ACTION PLAN
─────────────────────────────────────────
Priority 1 (Next 30 days):
• Increase term insurance to ₹{recommended_min:,}
• Build emergency fund: ₹{monthly_expenses * 6:,} (6 months expenses)

Priority 2 (Next 90 days):  
• Enhance Critical Illness cover to ₹{annual_income * 3:,}
• Start monthly SIP of ₹10,000 in diversified equity funds

Priority 3 (Next 6 months):
• Review and optimize home loan prepayment strategy
• Set up automatic premium payments with annual increases

6. FINANCIAL HEALTH SCORE
─────────────────────────────────────────
• Insurance Coverage: 6/10 (Underinsured)
• Premium Affordability: 9/10 (Highly affordable) 
• Debt Management: 7/10 (Manageable home loan)
• Overall Score: 7/10 (Good foundation, needs enhancement)

═══════════════════════════════════════════════════════════════════════
This analysis is based on standard financial planning principles.
Please consult a certified financial planner for personalized advice.
═══════════════════════════════════════════════════════════════════════
"""
    
    return report

# Main execution
if __name__ == "__main__":
    print("Choose analysis method:")
    print("1. AI-generated analysis (may be inconsistent)")
    print("2. Rule-based analysis (reliable and fast)")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        try:
            report = generate_comprehensive_analysis()
            print(report)
        except Exception as e:
            print(f"AI analysis failed: {e}")
            print("Falling back to rule-based analysis...\n")
            print(generate_rule_based_analysis())
    else:
        print(generate_rule_based_analysis())