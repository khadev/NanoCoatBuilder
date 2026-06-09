"""Ingredient database management."""

from typing import List, Dict, Optional
from core.models.ingredient import Ingredient, ChemicalProperty, Polymer, Nanocomposite


class IngredientDB:
    """Complete database of coating ingredients including nanocomposites."""
    _ingredients: Dict[str, Ingredient] = {}

    @classmethod
    def init(cls):
        # RESINS
        cls._ingredients["Epoxy Resin (DGEBA)"] = Ingredient(
            name="Epoxy Resin (DGEBA)", category="resin",
            polymer=Polymer(name="Epoxy", chemical_properties=ChemicalProperty(density=1.16, cost_per_kg=5.5), tg=50),
            typical_loading_wt=40, min_loading_wt=20, max_loading_wt=60,
            notes="Standard epoxy for anti-corrosion"
        )
        cls._ingredients["Polyurethane (Aliphatic)"] = Ingredient(
            name="Polyurethane (Aliphatic)", category="resin",
            polymer=Polymer(name="PU", chemical_properties=ChemicalProperty(density=1.12, cost_per_kg=6.2), tg=45),
            typical_loading_wt=35, min_loading_wt=20, max_loading_wt=55,
            notes="Excellent UV resistance"
        )
        cls._ingredients["Acrylic (Waterborne)"] = Ingredient(
            name="Acrylic (Waterborne)", category="resin",
            polymer=Polymer(name="Acrylic", chemical_properties=ChemicalProperty(density=1.05, cost_per_kg=3.8), tg=30),
            typical_loading_wt=45, min_loading_wt=30, max_loading_wt=65,
            notes="Low VOC, environmentally friendly"
        )
        cls._ingredients["Silicone Resin"] = Ingredient(
            name="Silicone Resin", category="resin",
            polymer=Polymer(name="Silicone", chemical_properties=ChemicalProperty(density=1.02, cost_per_kg=12.0), tg=120),
            typical_loading_wt=30, min_loading_wt=15, max_loading_wt=50,
            notes="High temperature resistance"
        )
        cls._ingredients["Polyimide"] = Ingredient(
            name="Polyimide", category="resin",
            polymer=Polymer(name="PI", chemical_properties=ChemicalProperty(density=1.43, cost_per_kg=25.0), tg=280),
            typical_loading_wt=25, min_loading_wt=10, max_loading_wt=40,
            notes="Extreme thermal stability"
        )

        # NANOCOMPOSITES
        cls._ingredients["Graphene Oxide (GO)"] = Ingredient(
            name="Graphene Oxide (GO)", category="nanocomposite",
            nanocomposite=Nanocomposite(name="GO", type="Graphene", particle_size_nm=500, surface_area_m2_g=800,
                purity_percent=99.5, properties=ChemicalProperty(density=1.8, cost_per_kg=150.0),
                recommended_loading_wt=0.5, max_loading_wt=2.0, min_loading_wt=0.1),
            typical_loading_wt=0.5, min_loading_wt=0.1, max_loading_wt=2.0,
            notes="Excellent barrier properties"
        )
        cls._ingredients["Carbon Nanotubes (CNT)"] = Ingredient(
            name="Carbon Nanotubes (CNT)", category="nanocomposite",
            nanocomposite=Nanocomposite(name="CNT", type="CNT", particle_size_nm=20, surface_area_m2_g=400,
                purity_percent=95.0, properties=ChemicalProperty(density=2.1, cost_per_kg=200.0),
                recommended_loading_wt=0.2, max_loading_wt=1.0, min_loading_wt=0.05),
            typical_loading_wt=0.2, min_loading_wt=0.05, max_loading_wt=1.0,
            notes="High electrical conductivity"
        )
        cls._ingredients["ZnO Nanoparticles"] = Ingredient(
            name="ZnO Nanoparticles", category="nanocomposite",
            nanocomposite=Nanocomposite(name="ZnO", type="Metal oxide", particle_size_nm=50, surface_area_m2_g=30,
                purity_percent=99.9, properties=ChemicalProperty(density=5.6, cost_per_kg=45.0),
                recommended_loading_wt=1.5, max_loading_wt=5.0, min_loading_wt=0.5),
            typical_loading_wt=1.5, min_loading_wt=0.5, max_loading_wt=5.0,
            notes="Antimicrobial, UV protection"
        )
        cls._ingredients["MXene (Ti3C2Tx)"] = Ingredient(
            name="MXene (Ti3C2Tx)", category="nanocomposite",
            nanocomposite=Nanocomposite(name="MXene", type="2D material", particle_size_nm=200, surface_area_m2_g=50,
                purity_percent=99.0, properties=ChemicalProperty(density=3.8, cost_per_kg=500.0),
                recommended_loading_wt=1.0, max_loading_wt=3.0, min_loading_wt=0.2),
            typical_loading_wt=1.0, min_loading_wt=0.2, max_loading_wt=3.0,
            notes="Excellent EMI shielding, corrosion protection"
        )
        cls._ingredients["TiO2 Nanoparticles"] = Ingredient(
            name="TiO2 Nanoparticles", category="nanocomposite",
            nanocomposite=Nanocomposite(name="TiO2", type="Metal oxide", particle_size_nm=25, surface_area_m2_g=50,
                purity_percent=99.5, properties=ChemicalProperty(density=4.2, cost_per_kg=35.0),
                recommended_loading_wt=2.0, max_loading_wt=6.0, min_loading_wt=0.5),
            typical_loading_wt=2.0, min_loading_wt=0.5, max_loading_wt=6.0,
            notes="Photocatalytic, self-cleaning"
        )
        cls._ingredients["SiO2 Nanoparticles"] = Ingredient(
            name="SiO2 Nanoparticles", category="nanocomposite",
            nanocomposite=Nanocomposite(name="SiO2", type="Metal oxide", particle_size_nm=30, surface_area_m2_g=200,
                purity_percent=99.8, properties=ChemicalProperty(density=2.2, cost_per_kg=25.0),
                recommended_loading_wt=2.5, max_loading_wt=7.0, min_loading_wt=0.5),
            typical_loading_wt=2.5, min_loading_wt=0.5, max_loading_wt=7.0,
            notes="Improved mechanical properties"
        )

        # SOLVENTS
        solvents = [
            ("Xylene", 0.87, 1.2, 10, 40), ("Butyl Acetate", 0.88, 1.5, 10, 40),
            ("Water", 1.00, 0.01, 5, 30), ("Acetone", 0.79, 1.0, 5, 30),
            ("Ethanol", 0.79, 0.8, 5, 25), ("Toluene", 0.87, 1.3, 10, 40),
            ("Methyl Ethyl Ketone (MEK)", 0.81, 1.8, 5, 35), ("Isopropanol", 0.79, 0.9, 5, 25)
        ]
        for name, density, cost, min_l, max_l in solvents:
            cls._ingredients[name] = Ingredient(name=name, category="solvent",
                properties=ChemicalProperty(density=density, cost_per_kg=cost),
                min_loading_wt=min_l, max_loading_wt=max_l)

        # PIGMENTS
        pigments = [
            ("Zinc Phosphate", 3.1, 3.2, 5, 20), ("Zinc Dust", 7.1, 4.5, 30, 80),
            ("Titanium Dioxide (Rutile)", 4.2, 2.8, 5, 25), ("Carbon Black", 1.8, 4.0, 0.5, 5),
            ("Iron Oxide Red", 5.2, 2.5, 2, 15), ("Aluminum Flakes", 2.7, 6.0, 5, 20),
            ("Mica", 2.8, 1.5, 5, 20), ("Talc", 2.8, 0.8, 5, 30)
        ]
        for name, density, cost, min_l, max_l in pigments:
            cls._ingredients[name] = Ingredient(name=name, category="pigment",
                properties=ChemicalProperty(density=density, cost_per_kg=cost),
                min_loading_wt=min_l, max_loading_wt=max_l)

        # ADDITIVES
        additives = [
            ("Dispersant (BYK-110)", 1.02, 15.0, 0.1, 2.0), ("Defoamer (BYK-024)", 0.95, 18.0, 0.05, 1.0),
            ("Curing Agent (Amine)", 1.00, 8.0, 10, 25), ("UV Absorber", 1.10, 25.0, 0.5, 3.0),
            ("Rheology Modifier", 1.05, 12.0, 0.1, 2.5), ("Flow Agent", 0.98, 20.0, 0.1, 1.5),
            ("Corrosion Inhibitor", 1.05, 25.0, 0.5, 3.0), ("Biocide", 1.08, 30.0, 0.1, 1.0)
        ]
        for name, density, cost, min_l, max_l in additives:
            cls._ingredients[name] = Ingredient(name=name, category="additive",
                properties=ChemicalProperty(density=density, cost_per_kg=cost),
                min_loading_wt=min_l, max_loading_wt=max_l)

        # FILLERS
        fillers = [
            ("Glass Fibers (short)", 2.5, 3.0, 5, 30), ("Carbon Fibers (milled)", 1.8, 25.0, 5, 25),
            ("Aramid Pulp", 1.4, 40.0, 3, 20), ("Cellulose Nanofibers", 1.5, 50.0, 1, 15)
        ]
        for name, density, cost, min_l, max_l in fillers:
            cls._ingredients[name] = Ingredient(name=name, category="filler",
                properties=ChemicalProperty(density=density, cost_per_kg=cost),
                min_loading_wt=min_l, max_loading_wt=max_l)

    @classmethod
    def get(cls, name: str) -> Optional[Ingredient]:
        return cls._ingredients.get(name)
    
    @classmethod
    def get_by_category(cls, category: str) -> List[Ingredient]:
        return [i for i in cls._ingredients.values() if i.category == category]
    
    @classmethod
    def get_all(cls) -> List[Ingredient]:
        return list(cls._ingredients.values())