# compliance_data.py
from typing import Dict, Any

# --- EU Compliance Rules 2026+ (Based on DPP and REACH/ESPR) ---
# This data structure can be easily updated over time.

COMPLIANCE_RULES: Dict[str, Any] = {
    "REACH_BANNED_SUBSTANCES": {
        "PFAS": {
            "keywords": ["pfa", "fluorochemical"],
            "limit": 0.0001, # Simplified - actual limits vary by substance
            "error_msg": "Contains reference to PFAS (per- and polyfluoroalkyl substances). Highly restricted/banned under REACH. **CRITICAL FAILURE**.",
        },
        "Azo_dyes": {
            "keywords": ["azo", "aminobenzene"],
            "limit": 0.003,
            "error_msg": "Contains reference to certain Azo dyes. Restricted/banned under REACH Annex XVII.",
        }
    },
    
    "DPP_CIRCULARITY_REQUIREMENTS": {
        "repairability": {
            "target": True,
            "warning_msg": "DPP (starting 2027) heavily penalizes items not designed for repair. 'is_repairable' set to False. Future non-compliance risk.",
            "error_msg_on_destruction_ban": "From July 2026, the EU bans the destruction of unsold textiles. Low repairability increases this risk.",
        },
        "traceability": {
            "data_required": ["SKU", "Origin", "Composition"],
            "error_msg": "Missing key data (SKU, Origin, Composition) required for fundamental DPP traceability.",
        }
    },
    
    "LABELING_STANDARDS": {
        "material_mix_limit": {
            "max_fibers": 3,
            "warning_msg": "Highly mixed fibers (more than 3 different types) complicate recycling and may be restricted under future DPP/ESPR rules. Simplify material composition.",
        }
    }
}
