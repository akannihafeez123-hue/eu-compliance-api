# models.py
from pydantic import BaseModel, Field
from typing import List, Optional

class ProductData(BaseModel):
    """
    Input schema for the user's product data submission.
    """
    product_sku: str = Field(..., description="Unique SKU or Identifier for the product.")
    material_composition: str = Field(..., description="e.g., '60% Cotton, 40% Recycled Polyester'.")
    weight_g: int = Field(..., gt=0, description="Product weight in grams.")
    country_of_origin: str = Field(..., min_length=2, max_length=2, description="2-letter ISO code (e.g., 'CN', 'IN').")
    
    # REACH/Hazard checks
    has_biocidal_treatment: bool = Field(False, description="Is the product treated with biocidal substances (e.g., for anti-odor)?")
    
    # Durability/Circularity checks (DPP focus)
    is_repairable: bool = Field(False, description="Is the item designed for easy repair (e.g., replaceable zippers)?")


class ComplianceResult(BaseModel):
    """
    Output schema for the API's compliance check result.
    """
    product_sku: str
    is_compliant: bool = Field(..., description="True if no hard 'errors' are found.")
    errors: List[str] = Field(..., description="List of critical compliance failures (FAIL).")
    warnings: List[str] = Field(..., description="List of future or non-critical issues (PREPARE/WARN).")
    next_steps: Optional[str] = Field(None, description="General advice for non-compliant checks.")
