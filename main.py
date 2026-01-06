# main.py
from fastapi import FastAPI, HTTPException
from models import ProductData, ComplianceResult
from compliance_data import COMPLIANCE_RULES
from typing import List, Dict

app = FastAPI(
    title="ComplianceCheck EU Textile API",
    description="Automated validation of E-commerce textile products against core EU DPP and REACH regulations (Passive Income Microservice).",
    version="1.0.0"
)

def run_compliance_checks(product: ProductData) -> Dict[str, List[str]]:
    """
    Applies the rules from compliance_data.py to the submitted product data.
    """
    errors: List[str] = []
    warnings: List[str] = []
    
    # 1. REACH: Banned Chemical Substances Check (Hard Errors)
    composition_lower = product.material_composition.lower()
    for substance_name, rules in COMPLIANCE_RULES["REACH_BANNED_SUBSTANCES"].items():
        for keyword in rules["keywords"]:
            if keyword in composition_lower:
                errors.append(f"{substance_name}: {rules['error_msg']}")
    
    # 2. REACH: Biocidal Treatment Check
    if product.has_biocidal_treatment:
        errors.append("Biocidal treatments require separate EU Biocidal Product Regulation (BPR) documentation and strict labeling. Treat as **CRITICAL FAILURE** until BPR is met.")

    # 3. DPP: Traceability Check (Mandatory Data)
    if not product.product_sku or not product.country_of_origin:
        errors.append(COMPLIANCE_RULES["DPP_CIRCULARITY_REQUIREMENTS"]["traceability"]["error_msg"])

    # 4. DPP: Repairability/Circularity Check (Warnings/Future Compliance)
    if not product.is_repairable:
        warnings.append(COMPLIANCE_RULES["DPP_CIRCULARITY_REQUIREMENTS"]["repairability"]["warning_msg"])
        
    # 5. DPP: Material Complexity/Recyclability Check
    # Simple check for MVP: count distinct fiber types
    fiber_types = [s.split('%')[1].strip() for s in composition_lower.split(',') if '%' in s]
    if len(fiber_types) > COMPLIANCE_RULES["LABELING_STANDARDS"]["material_mix_limit"]["max_fibers"]:
        warnings.append(COMPLIANCE_RULES["LABELING_STANDARDS"]["material_mix_limit"]["warning_msg"])
        
    return {"errors": errors, "warnings": warnings}


@app.post("/v1/check_product", response_model=ComplianceResult, tags=["Compliance"])
async def check_product(product: ProductData):
    """
    Submit product data (Composition, Origin, etc.) to check compliance against 
    current and future EU Digital Product Passport (DPP) and REACH rules.
    """
    
    # Run all defined checks
    results = run_compliance_checks(product)
    
    is_compliant = len(results["errors"]) == 0
    
    # Define a default next step based on the outcome
    next_steps_advice = None
    if not is_compliant:
        next_steps_advice = "The product cannot be legally placed on the EU market until all CRITICAL ERRORS are resolved."
    elif len(results["warnings"]) > 0:
         next_steps_advice = "Compliance is met, but WARNINGS indicate high-risk areas for future (2027+) DPP enforcement. Start preparing your supply chain data now."
    else:
        next_steps_advice = "Product data appears compliant with current core regulations. Good to go."


    return ComplianceResult(
        product_sku=product.product_sku,
        is_compliant=is_compliant,
        errors=results["errors"],
        warnings=results["warnings"],
        next_steps=next_steps_advice
    )


@app.get("/")
def read_root():
    """Simple health check endpoint."""
    return {"status": "ok", "service": "ComplianceCheck API v1.0"}

# This image illustrates the high-level concept your API supports:
# centralizing and standardizing product data for regulators and consumers.
