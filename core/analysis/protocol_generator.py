"""Synthesis protocol generator."""

from core.models.formulation import FormulationRecord, SynthesisProtocol
from core.models.ingredient import SynthesisMethod
from core.database.ingredient_db import IngredientDB


class ProtocolGenerator:
    @staticmethod
    def generate_synthesis_protocol(formulation: FormulationRecord) -> SynthesisProtocol:
        has_nano = any(IngredientDB.get(i.ingredient_name) and 
                      IngredientDB.get(i.ingredient_name).category == "nanocomposite" 
                      for i in formulation.items)
        
        steps = [
            "MATERIAL PREPARATION",
            "Weigh all ingredients according to the formulation",
            f"Total weight target: {formulation.total_weight():.1f}g (standard 100g)",
            "",
            "NANOPARTICLE DISPERSION" if has_nano else "",
            "Add nanoparticles to 30% of total solvent volume" if has_nano else "",
            "Ultrasonicate for 30 minutes at 40kHz, 200W" if has_nano else "",
            "Maintain temperature below 40°C using ice bath" if has_nano else "",
            "",
            "RESIN DISSOLUTION",
            "Add resin to mixing vessel",
            "Add remaining solvent slowly while stirring at 400-600 rpm",
            "Continue stirring until complete dissolution (approx. 30 minutes)",
            "",
            "PIGMENT AND FILLER ADDITION",
            "Add pigments and fillers gradually while mixing at 800 rpm",
            "Increase speed to 1500 rpm for high-shear dispersion",
            "Mix for 20-30 minutes until uniform",
            "",
            "ADDITIVE INCORPORATION",
            "Add additives in sequence: dispersant first, then defoamer, then others",
            "Mix for 5 minutes between each addition",
            "",
            "DEGASSING",
            "Place mixture under vacuum (500 mbar) for 15 minutes",
            "Or allow to stand covered for 2 hours",
            "",
            "APPLICATION",
            "Apply using spray gun (1.2mm nozzle, 2.5 bar) OR drawdown bar (50-100μm)",
            "",
            "CURING",
            "Option 1: Ambient cure - 7 days at 25°C, 50% RH",
            "Option 2: Forced cure - 2 hours at 80°C, then 1 hour at 120°C",
            "",
            "QUALITY CONTROL",
            "Measure dry film thickness (minimum 160μm for C5 environment)",
            "Perform cross-cut adhesion test (ISO 2409)",
            "Measure pencil hardness (minimum H for industrial coatings)"
        ]
        
        steps = [s for s in steps if s]
        
        return SynthesisProtocol(
            method=SynthesisMethod.IN_SITU_POLYMERIZATION if has_nano else SynthesisMethod.SOLUTION_BLENDING,
            steps=steps,
            temperature_c=25,
            time_hours=2.5,
            stirring_speed_rpm=600,
            sonication_minutes=30 if has_nano else 0,
            curing_conditions="80°C for 2h + 120°C for 1h (forced) OR 7 days ambient",
            post_treatment="Store in sealed container at room temperature",
            safety_notes=[
                "Wear appropriate PPE (gloves, goggles, lab coat, respirator for spray application)",
                "Work in a well-ventilated area or fume hood",
                "Dispose of waste according to local regulations",
                "Avoid skin contact with uncured resins and solvents",
                "Keep flammables away from ignition sources"
            ],
            equipment_needed=["Mixing vessel", "Mechanical stirrer", "Ultrasonic bath" if has_nano else ""]
        )