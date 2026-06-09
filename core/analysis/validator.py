"""Formulation validation logic - Complete validation rules."""

from typing import List, Tuple, Dict
from core.models.formulation import FormulationRecord
from core.models.validation import ValidationRule
from core.database.ingredient_db import IngredientDB


class FormulationValidator:
    """Validates formulations against ingredient limits, ratio rules, protocol compliance, and ISO standards."""
    
    @staticmethod
    def validate_ingredient_limits(formulation: FormulationRecord) -> List[ValidationRule]:
        """Check if each ingredient is within its min/max loading limits."""
        rules = []
        
        for item in formulation.items:
            ing = IngredientDB.get(item.ingredient_name)
            if ing and item.weight_grams > 0:
                # Check max limit
                if item.weight_grams > ing.max_loading_wt:
                    rules.append(ValidationRule(
                        category="ingredient",
                        severity="error",
                        message=f"{ing.name}: {item.weight_grams:.1f}g exceeds maximum loading of {ing.max_loading_wt:.1f}g",
                        recommendation=f"Reduce {ing.name} to ≤{ing.max_loading_wt:.1f}g",
                        standard="Good Manufacturing Practice"
                    ))
                
                # Check min limit
                if item.weight_grams < ing.min_loading_wt:
                    rules.append(ValidationRule(
                        category="ingredient",
                        severity="warning",
                        message=f"{ing.name}: {item.weight_grams:.1f}g is below minimum recommended loading of {ing.min_loading_wt:.1f}g",
                        recommendation=f"Increase {ing.name} to ≥{ing.min_loading_wt:.1f}g for optimal performance",
                        standard="Good Manufacturing Practice"
                    ))
                
                # Special check for nanocomposites - agglomeration warning
                if ing.category == "nanocomposite" and item.weight_grams > ing.max_loading_wt * 0.8:
                    rules.append(ValidationRule(
                        category="ingredient",
                        severity="warning",
                        message=f"{ing.name}: Loading is high ({item.weight_grams:.1f}g). Risk of agglomeration.",
                        recommendation=f"Keep nanocomposite loading ≤{ing.max_loading_wt:.1f}g to prevent particle agglomeration",
                        standard="Nanocomposite Literature Review"
                    ))
        
        return rules
    
    @staticmethod
    def validate_category_ratios(formulation: FormulationRecord) -> List[ValidationRule]:
        """Validate the ratios between different ingredient categories."""
        rules = []
        
        # Calculate category totals
        totals = {"resin": 0.0, "solvent": 0.0, "pigment": 0.0, "additive": 0.0, "nanocomposite": 0.0, "filler": 0.0}
        for item in formulation.items:
            ing = IngredientDB.get(item.ingredient_name)
            if ing and ing.category in totals:
                totals[ing.category] += item.weight_grams
        
        total_solids = totals["resin"] + totals["pigment"] + totals["nanocomposite"] + totals["filler"]
        total = formulation.total_weight()
        
        # Rule 1: Resin should be at least 30% of solids
        if total_solids > 0:
            resin_ratio = totals["resin"] / total_solids * 100
            if resin_ratio < 30:
                rules.append(ValidationRule(
                    category="ratio",
                    severity="error",
                    message=f"Resin content is only {resin_ratio:.0f}% of total solids (minimum 30%)",
                    recommendation=f"Increase resin to at least {0.3 * total_solids - totals['resin']:.1f}g or reduce pigments/fillers",
                    standard="ISO 12944-5:2019 Clause 5.2"
                ))
            elif resin_ratio > 70:
                rules.append(ValidationRule(
                    category="ratio",
                    severity="warning",
                    message=f"Resin content is {resin_ratio:.0f}% of solids (>70%). High cost and potentially soft coating.",
                    recommendation="Consider adding more pigments or fillers for mechanical reinforcement",
                    standard="Good Formulation Practice"
                ))
        
        # Rule 2: Solvent should be 15-40% of total formulation
        if total > 0:
            solvent_ratio = totals["solvent"] / total * 100
            if solvent_ratio < 15:
                rules.append(ValidationRule(
                    category="ratio",
                    severity="error",
                    message=f"Solvent content is only {solvent_ratio:.0f}% (minimum 15%)",
                    recommendation=f"Add {0.2 * total - totals['solvent']:.1f}g more solvent for proper viscosity",
                    standard="Coating Application Guidelines"
                ))
            elif solvent_ratio > 45:
                rules.append(ValidationRule(
                    category="ratio",
                    severity="warning",
                    message=f"Solvent content is {solvent_ratio:.0f}% (>45%). High VOC and potential sagging issues.",
                    recommendation="Reduce solvent to ≤40% for better film build and lower VOC",
                    standard="EU Directive 2004/42/EC"
                ))
        
        # Rule 3: Additives should not exceed 5% of total formulation
        if total > 0:
            additive_ratio = totals["additive"] / total * 100
            if additive_ratio > 5:
                rules.append(ValidationRule(
                    category="ratio",
                    severity="error",
                    message=f"Additive content is {additive_ratio:.0f}% (maximum 5%)",
                    recommendation=f"Reduce additives to ≤{0.05 * total:.1f}g total",
                    standard="Good Formulation Practice"
                ))
        
        # Rule 4: Nanocomposite specific checks
        if totals["nanocomposite"] > 0 and total_solids > 0:
            nano_ratio = totals["nanocomposite"] / total_solids * 100
            if nano_ratio > 5:
                rules.append(ValidationRule(
                    category="ratio",
                    severity="error",
                    message=f"Nanocomposite loading is {nano_ratio:.1f}% of solids (maximum 5%)",
                    recommendation=f"Reduce nanocomposite to ≤{0.05 * total_solids:.1f}g to avoid agglomeration",
                    standard="Nanocomposite Literature (2023-2026)"
                ))
            elif nano_ratio > 3:
                rules.append(ValidationRule(
                    category="ratio",
                    severity="warning",
                    message=f"Nanocomposite loading is {nano_ratio:.1f}% of solids. High loading may affect dispersion.",
                    recommendation="Ensure proper dispersion protocol with extended ultrasonication",
                    standard="Nanocomposite Dispersion Guidelines"
                ))
        
        # Rule 5: Pigment-to-Binder ratio (for anti-corrosion coatings)
        if totals["pigment"] > 0 and totals["resin"] > 0:
            pbr = totals["pigment"] / totals["resin"]
            if pbr > 1.5:
                rules.append(ValidationRule(
                    category="ratio",
                    severity="warning",
                    message=f"Pigment-to-Binder ratio is {pbr:.2f} (>1.5). High pigment loading may reduce adhesion.",
                    recommendation="Reduce pigment loading or increase resin for better binder coverage",
                    standard="ISO 12944-5:2019"
                ))
        
        return rules
    
    @staticmethod
    def validate_total_weight(formulation: FormulationRecord) -> List[ValidationRule]:
        """Validate total formulation weight."""
        rules = []
        total = formulation.total_weight()
        
        if total == 0:
            rules.append(ValidationRule(
                category="weight",
                severity="error",
                message="No ingredients added. Formulation is empty.",
                recommendation="Add at least one ingredient with weight > 0g",
                standard="ISO 12944-1:2017"
            ))
        elif abs(total - 100) > 5:
            if total < 95:
                rules.append(ValidationRule(
                    category="weight",
                    severity="error",
                    message=f"Total weight is {total:.1f}g (<95g). Below standard formulation weight.",
                    recommendation=f"Add {100 - total:.1f}g more ingredients to reach 100g standard",
                    standard="ISO 12944-1:2017 - Standard formulation weight: 100g ±5g"
                ))
            else:
                rules.append(ValidationRule(
                    category="weight",
                    severity="warning",
                    message=f"Total weight is {total:.1f}g (target: 100g ±5g)",
                    recommendation="Adjust to 100g for standardized research reproducibility",
                    standard="ISO 12944-1:2017"
                ))
        else:
            rules.append(ValidationRule(
                category="weight",
                severity="info",
                message=f"✓ Total weight {total:.1f}g is within specification (±5g of 100g)",
                recommendation="Good for standardized formulation",
                standard="ISO 12944-1:2017"
            ))
        
        return rules
    
    @staticmethod
    def validate_protocol_compliance(formulation: FormulationRecord) -> List[ValidationRule]:
        """Validate that formulation follows proper synthesis protocol."""
        rules = []
        
        # Check if nanocomposites require ultrasonication
        has_nanocomposites = any(
            IngredientDB.get(item.ingredient_name) and 
            IngredientDB.get(item.ingredient_name).category == "nanocomposite"
            for item in formulation.items
        )
        
        if has_nanocomposites:
            rules.append(ValidationRule(
                category="protocol",
                severity="info",
                message="Nanocomposites detected - ultrasonication required for proper dispersion",
                recommendation="Add ultrasonication step: 20-30 minutes at 40kHz for proper nanoparticle dispersion",
                standard="Nanocomposite Dispersion Protocol"
            ))
        
        # Check for epoxy-amine stoichiometry
        has_epoxy = any("Epoxy" in item.ingredient_name for item in formulation.items)
        has_amine = any("Curing Agent (Amine)" in item.ingredient_name for item in formulation.items)
        
        if has_epoxy and not has_amine:
            rules.append(ValidationRule(
                category="protocol",
                severity="error",
                message="Epoxy resin detected but no curing agent (amine) added",
                recommendation="Add Curing Agent (Amine) at 15-25% of epoxy weight for proper crosslinking",
                standard="Epoxy Chemistry"
            ))
        
        if has_epoxy and has_amine:
            epoxy_weight = sum(item.weight_grams for item in formulation.items if "Epoxy" in item.ingredient_name)
            amine_weight = sum(item.weight_grams for item in formulation.items if "Curing Agent (Amine)" in item.ingredient_name)
            
            if epoxy_weight > 0:
                amine_ratio = amine_weight / epoxy_weight * 100
                if amine_ratio < 10:
                    rules.append(ValidationRule(
                        category="protocol",
                        severity="error",
                        message=f"Amine hardener is only {amine_ratio:.0f}% of epoxy weight (minimum 10%)",
                        recommendation=f"Add {0.15 * epoxy_weight - amine_weight:.1f}g more curing agent",
                        standard="Epoxy Stoichiometry"
                    ))
                elif amine_ratio > 30:
                    rules.append(ValidationRule(
                        category="protocol",
                        severity="warning",
                        message=f"Amine hardener is {amine_ratio:.0f}% of epoxy weight (>30%). Excess amine may affect properties.",
                        recommendation="Reduce curing agent to 15-25% of epoxy weight",
                        standard="Epoxy Stoichiometry"
                    ))
        
        # Check curing requirements for anti-corrosion coatings
        if formulation.coating_type.value == "Anti-corrosion":
            rules.append(ValidationRule(
                category="protocol",
                severity="info",
                message="Anti-corrosion coating requires proper curing conditions",
                recommendation="Add curing step: 80°C for 2h + 120°C for 1h for epoxy systems",
                standard="ISO 12944-5:2019"
            ))
        
        return rules
    
    @staticmethod
    def validate_all(formulation: FormulationRecord) -> Tuple[List[ValidationRule], List[str], List[Dict]]:
        """Run all validations and return combined results."""
        all_rules = []
        
        # Run all validations
        all_rules.extend(FormulationValidator.validate_total_weight(formulation))
        all_rules.extend(FormulationValidator.validate_ingredient_limits(formulation))
        all_rules.extend(FormulationValidator.validate_category_ratios(formulation))
        all_rules.extend(FormulationValidator.validate_protocol_compliance(formulation))
        
        # Separate ISO compliance and violations
        iso_passed = []
        iso_violations = []
        
        for rule in all_rules:
            if rule.standard and ("ISO" in rule.standard or "EU" in rule.standard):
                if rule.severity == "error":
                    iso_violations.append({
                        "standard": rule.standard,
                        "reason": rule.message,
                        "citation": rule.recommendation
                    })
                elif rule.severity == "info":
                    iso_passed.append(rule.standard)
        
        return all_rules, iso_passed, iso_violations