"""
PM SVANidhi Eligibility Checker
Determines which government schemes a vendor qualifies for based on their profile.
"""


def check_eligibility(
    has_cov: bool = False,
    has_lor: bool = False,
    is_food_vendor: bool = False,
    city: str = None,
) -> dict:
    """
    Check eligibility for PM SVANidhi and other schemes.
    Returns eligibility status, loan amount, applicable schemes, and next steps.
    """
    schemes = []
    next_steps = []
    documents = [
        "Aadhaar Card",
        "Savings Bank Account passbook",
        "Mobile number linked to Aadhaar",
        "Passport-size photograph",
    ]

    # PM SVANidhi eligibility
    if has_cov or has_lor:
        schemes.append({
            "name": "PM SVANidhi",
            "eligible": True,
            "amount": "Rs.10,000 (1st loan), Rs.20,000 (2nd), Rs.50,000 (3rd)",
            "benefit": "7% interest subsidy + Rs.1,200/year digital cashback",
            "portal": "pmsvanidhi.mohua.gov.in",
            "helpline": "1800-11-1979",
        })
        next_steps.extend([
            "Visit pmsvanidhi.mohua.gov.in or nearest bank/CSC",
            "Submit Aadhaar + Certificate of Vending (CoV) or Letter of Recommendation (LoR)",
            "Link your bank account for direct subsidy transfer",
            "Start using UPI payments to earn cashback rewards",
        ])
        if has_cov:
            loan_amount = "Rs.10,000 (immediately eligible, 1st tier)"
        else:
            loan_amount = "Rs.10,000 (with LoR, 1st tier)"
    else:
        schemes.append({
            "name": "PM SVANidhi",
            "eligible": False,
            "amount": "Requires CoV or LoR",
            "benefit": "Get your Certificate of Vending first from your local ULB/TVC",
            "portal": "pmsvanidhi.mohua.gov.in",
            "helpline": "1800-11-1979",
        })
        loan_amount = "Not yet eligible — need CoV/LoR"
        next_steps.extend([
            "Visit your nearest Town Vending Committee (TVC) or Municipal Ward Office",
            "Apply for Certificate of Vending (CoV) — it's free",
            "Once CoV is obtained, apply for PM SVANidhi loan",
        ])

    # MSME Udyam — always eligible
    schemes.append({
        "name": "MSME Udyam Registration",
        "eligible": True,
        "amount": "Free forever",
        "benefit": "Priority sector loans, 50% patent subsidy, government tender access",
        "portal": "udyamregistration.gov.in",
        "helpline": "1800-111-956",
    })
    next_steps.append("Register free at udyamregistration.gov.in using Aadhaar")

    # Mudra Yojana — eligible for all
    schemes.append({
        "name": "Mudra Yojana (Shishu)",
        "eligible": True,
        "amount": "Up to Rs.50,000 (Shishu) / Rs.5 lakh (Kishore)",
        "benefit": "Zero collateral, simple documentation",
        "portal": "mudra.org.in",
        "helpline": "1800-180-1111",
    })
    next_steps.append("Apply at any PSU bank for Mudra Shishu loan")

    # FSSAI for food vendors
    if is_food_vendor:
        documents.append("FSSAI Basic Registration (Rs.100/year)")
        schemes.append({
            "name": "FSSAI Basic Registration",
            "eligible": True,
            "amount": "Rs.100/year",
            "benefit": "Legal right to sell food, required for Zomato/Swiggy listing",
            "portal": "foscos.fssai.gov.in",
            "helpline": "1800-112-100",
        })
        next_steps.append("Register at foscos.fssai.gov.in (only Rs.100/year)")

    # e-Shram
    schemes.append({
        "name": "e-Shram Card",
        "eligible": True,
        "amount": "Free + Rs.2 lakh accident insurance",
        "benefit": "Universal Account Number, social security access",
        "portal": "eshram.gov.in",
        "helpline": "14434",
    })

    return {
        "eligible": has_cov or has_lor,
        "loan_amount": loan_amount,
        "schemes": schemes,
        "next_steps": list(dict.fromkeys(next_steps)),  # deduplicate
        "documents_needed": documents,
    }
