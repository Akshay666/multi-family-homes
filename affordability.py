# Import neccessary modules
import numpy as np

def print_intro():
    print('This algorithm will help you to answer 2 questions regarding your affordability: ', 
         '\n 1. What is the maximum mortgage amount I can afford based on my current conditions?',
         '\n 2. Is this property completely affordable for me when I account for typical home expenses?',
         '\n', '\n', 'We will first start by asking you a few questions regarding your current conditions.',
         "\n Let's get started!")
          
# User Info 
def get_user_info():
    # Prompt to get key inputs from user.
    reported_city = input("\nWhich county are you looking at? ")
    reported_desired_pmt = input('How much do you currently pay for housing? ')
    reported_down_pmt = input('How much savings do you have and wish to put towards your down paymnent? ')
    reported_term = input('In how many years do you want to own your home? (either 30 Years or 15 Years) ')
    reported_first_home_flag = input('Is this your first home purchase? Please enter - Yes or No. ')
    reported_credit_score = input('Please enter your credit score? ')
    user_data = [reported_city, reported_desired_pmt, reported_down_pmt, reported_term, reported_first_home_flag, reported_credit_score]
    return user_data

# Normalize user input data 
def process_user_inputs(user_data):
    
    chars = ['$', ' ', ',', 'years']
    for i in range(len(user_data)):
    
        # Parse out formatting issues.
        var = user_data[i].lower()
        for c in chars:
            if c in var:
                var = var.replace(c.lower(),'')
                
        # Process data types.
        if i == 0:
            var = var
        elif i == 4:
            if var == 'yes' or var == 'y':
                var = 'Yes'
            else:
                var = 'No'
        elif i == 3 or 5:
            var = int(float(var))
        else:
            var = float(var)
        user_data[i] = var
        
    return user_data

def get_property_info():
    property_amount = input("\nWhat is the property amount for this home? ")
    property_rent = input("How much do you think you can get in rent for this home? ")
    return property_amount, property_rent
    
# Retrieve standardized data
def get_variables(clean_data):
    city = clean_data[0]
    desired_pmt = clean_data[1]
    down_pmt = clean_data[2]
    term = clean_data[3] * 12 # in Months
    first_time_flag = clean_data[4]
    credit_score = clean_data[5]
    return city, desired_pmt, down_pmt, term, first_time_flag, credit_score
    
# Derive assumptions (interest rate and target_property_amount)
def derived_assumptions(city, desired_pmt, down_pmt, term, first_time_flag, credit_score):
    # Interest Rate Assumption: Highest Fannie Mae MultiFamily
    rate = 0.06
    
    # Down Payment Assumption: King County, first time home buyers who are credit worthy borrowers get to put down 3.5% 
    # Subject to Max Cap for King County 
    if first_time_flag == 'Yes':
        if city == 'king':
            import pdb; pdb.set_trace
            if credit_score > 600:
                down_payment_percentage = 0.035
                fha_max_king = 930300
    else:
        down_payment_percentage = 'inf'
        print('Model cannot support at this time.')
    max_mortgage_amt_dp = min((down_pmt/down_payment_percentage), fha_max_king) 
    
    # Max Mortgage based on affordability
    max_mortgage_amt_afford = -1 * np.pv(rate/12,term,desired_pmt)
    
    # Mortgage Max 
    max_mortgage = min(max_mortgage_amt_dp, max_mortgage_amt_afford)
    
    # Max Amount 
    max_property_amount = max_mortgage + down_pmt
    return max_property_amount, rate

def cashflow_savings(pmt, property_rent):
    extra_cash = round(property_rent, 2)
    return extra_cash

def prepay_savings(bal, rate, term, pmt, property_rent):
    required_pmt = pmt
    prepay = property_rent 
    principal_paid = 0
    months = 0
    while bal > 0:
        actual_pmt = required_pmt + prepay
        interest_paid = bal * (rate/12)
        principal_paid = actual_pmt - interest_paid
        bal -= principal_paid
        months += 1
    payoff_years = round(months/12, 0)  # in years
    payoff_months = months - (payoff_years*12)
    return payoff_years, payoff_months

def print_scenarios(property_amount, max_property_amount, mtg_bal, extra_cash, payoff_years, payoff_months, term):
    print('\nBase Case: Maximum property amount you can afford not including property taxes and home insurance is : $', round(max_property_amount,2))
    print('\nPay Off Quickly: If you decide to prepay this house using your rental income, you will pay off your house in ', payoff_years, ' years and ', payoff_months,
          ' months instead of ', term/12, ' years.')
    print('\nExtra Cash: If you want to gain extra cash instead, you will get extra $', extra_cash, ' every month.')



def affordability():
    
    # Property Inputs
    # property_rent --> (Monthly/Zillow Estimate)
    # property_taxes --> (Yearly)
    
    print_intro()
          
    # User Inputs (County, Monthly Payment, Down Payment, Term, First Time Home Buyer, Credit Score)
    reported_user_data = get_user_info()
    # reported_user_data = ['king', '$3000.00 ', '50,000.00 ', '30 Years ', 'Yes', '710']
    clean_data = process_user_inputs(reported_user_data)
    city, desired_pmt, down_pmt, term, first_time_flag, credit_score = get_variables(clean_data)
    
    # Base Case # Not including property taxes and home insurance
    max_property_amount, rate = derived_assumptions(city, desired_pmt, down_pmt, term, first_time_flag, credit_score)
    
    property_comparison = input("\nDo you have a property that you would like to see our scenario analysis for?")
    if property_comparison == 'Yes' or property_comparison == 'yes':
        
        property_amount, property_rent = get_property_info()
        property_amount = float(property_amount)
        property_rent = float(property_rent)
        
        # Offset rental income + incorporate monthly:
        # property taxes (King County 1.02%)  
        # home insurance ($811/year - avg Washington) for monthly payment 
        # maintenance cost (1% of purchase price as per 1 percent rule)
        
        property_taxes = 0.0102 * property_amount 
        home_insurance = 811
        maintenance_cost = 0.01 * property_amount
        additional_property_expenses = (maintenance_cost + property_taxes + home_insurance)/12
        property_rent -= additional_property_expenses 


        # Property Acceptability
        prop_acceptable = 'No'
        if property_amount < max_property_amount:
            prop_acceptable  = 'Yes'

        # Run Only on Acceptable Properties
        if prop_acceptable == 'Yes':

            # Financing Outputs
            mtg_bal = property_amount - down_pmt
            pmt = -1 * np.pmt(rate/12, term, mtg_bal, 0)

            # Savings
            extra_cash = cashflow_savings(pmt, property_rent)
            payoff_years, payoff_months = prepay_savings(mtg_bal, rate, term, pmt, property_rent)
            print_scenarios( property_amount, max_property_amount, mtg_bal, extra_cash, payoff_years, payoff_months, term)
        else:
            print('Even though you could potentially afford up to ', max_property_amount, 
                  '/n This is not an acceptable property for you because the rental income does not offset property taxes and insurance enough.')
            mtg_bal = 0
            extra_cash = 0
            payoff = 0

    else:
        print('You can potentially afford up to $', round(max_property_amount, 2), '.')

affordability()