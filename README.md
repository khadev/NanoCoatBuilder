
<div align="center">

# 🔬 NanoCoatBuilder

## Advanced Coating Formulation Software for Research & Development

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![PySide6](https://img.shields.io/badge/PySide6-6.5+-green.svg)](https://doc.qt.io/qtforpython/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)]()
[![Version](https://img.shields.io/badge/Version-1.0-orange.svg)]()

</div>

---

## 📖 Overview

**NanoCoatBuilder** is a professional desktop application for designing, analyzing, and optimizing coating formulations. Built for researchers, chemists, and materials scientists, it provides intelligent predictions, ISO compliance validation, and automatic synthesis protocol generation.

---

## ✨ Key Features

| Feature | Description | Status |
|:-------:|-------------|:------:|
| 🧪 **Smart Formulation** | Drag-and-drop ingredient selection with real-time weight tracking | ✅ |
| 🔬 **Nanocomposites** | Support for Graphene, CNT, MXene, ZnO, and advanced nanomaterials | ✅ |
| 📊 **Performance Prediction** | AI-powered predictions for corrosion, adhesion, and durability | ✅ |
| ✅ **ISO Compliance** | Automatic validation against ISO 12944, 9227, 2409 standards | ✅ |
| ⚙️ **Protocol Generator** | Automatic synthesis protocol with safety notes | ✅ |
| 🌍 **Multi-language** | Full English and French interface | ✅ |
| 📄 **Export** | HTML reports and JSON data for publication | ✅ |
| 📜 **History & Compare** | Save, load, and compare formulations side-by-side | ✅ |

---

## 🚀 Quick Start

### Prerequisites

| Requirement | Version |
|-------------|---------|
| Python | 3.10 or higher |
| pip | Latest version |
| RAM | 4GB minimum |
| Disk Space | 500MB |

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/NanoCoatBuilder.git
cd NanoCoatBuilder

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| PySide6 | ≥6.5.0 | Qt6 GUI Framework |
| matplotlib | ≥3.7.0 | Performance Graphs |
| numpy | ≥1.24.0 | Numerical Analysis |
| pydantic | ≥2.0.0 | Data Validation |

---

## 📁 Project Structure

| Directory | Description |
|-----------|-------------|
| `main.py` | Application entry point with splash screen |
| `core/` | Core business logic |
| `core/database/` | Ingredient database management |
| `core/models/` | Pydantic data models |
| `core/analysis/` | Performance analysis & validation |
| `core/utils/` | Utilities, constants & translations |
| `ui/` | User interface components |
| `ui/widgets/` | Reusable UI widgets |
| `ui/dialogs/` | Dialog windows |
| `Screenshots/` | Captured screenshots (auto-created) |

---

## 🎮 Usage Guide

| Step | Action | Description |
|:----:|--------|-------------|
| 1 | **Select Category** | Choose ingredient type (Resins, Nanocomposites, Pigments, etc.) |
| 2 | **Add Ingredients** | Click ADD and select from database |
| 3 | **Enter Weights** | Input grams (target total: **100g**) |
| 4 | **Choose Sector** | Select application (Navy, Aviation, Space, etc.) |
| 5 | **Validate** | Save formulation to history |
| 6 | **Analyze** | Get predictions, graphs, and protocol |
| 7 | **Export** | Save as HTML report or JSON data |

---

## 📊 Supported Application Sectors

| Sector | Icon | Salt Spray | Adhesion | Solids | VOC |
|--------|:----:|:----------:|:--------:|:------:|:---:|
| Navy / Marine | ⚓ | ≥3000h | ≥8 MPa | ≥65% | ≤350 |
| Aviation / Aerospace | ✈️ | ≥2000h | ≥10 MPa | ≥70% | ≤250 |
| Space / Satellite | 🚀 | ≥5000h | ≥12 MPa | ≥80% | ≤100 |
| Industry / Manufacturing | 🏭 | ≥1500h | ≥6 MPa | ≥60% | ≤420 |
| Infrastructure / Bridges | 🌉 | ≥2000h | ≥7 MPa | ≥60% | ≤420 |
| Building / Construction | 🏗️ | ≥1000h | ≥5 MPa | ≥55% | ≤420 |
| Automotive | 🚗 | ≥1000h | ≥6 MPa | ≥55% | ≤350 |
| Oil & Gas | 🛢️ | ≥3500h | ≥9 MPa | ≥70% | ≤350 |
| Nuclear | ☢️ | ≥4000h | ≥10 MPa | ≥75% | ≤200 |
| Medical | 🏥 | ≥500h | ≥5 MPa | ≥50% | ≤250 |

---

## 🧪 Ingredient Database

### Resins

| Ingredient | Min Loading | Max Loading | Cost (€/kg) |
|------------|:-----------:|:-----------:|:-----------:|
| Epoxy Resin (DGEBA) | 20% | 60% | 5.50 |
| Polyurethane (Aliphatic) | 20% | 55% | 6.20 |
| Acrylic (Waterborne) | 30% | 65% | 3.80 |
| Silicone Resin | 15% | 50% | 12.00 |
| Polyimide | 10% | 40% | 25.00 |

### Nanocomposites

| Ingredient | Type | Min Loading | Max Loading | Cost (€/kg) |
|------------|------|:-----------:|:-----------:|:-----------:|
| Graphene Oxide (GO) | Graphene | 0.1% | 2.0% | 150 |
| Carbon Nanotubes (CNT) | CNT | 0.05% | 1.0% | 200 |
| MXene (Ti3C2Tx) | 2D Material | 0.2% | 3.0% | 500 |
| ZnO Nanoparticles | Metal Oxide | 0.5% | 5.0% | 45 |
| TiO2 Nanoparticles | Metal Oxide | 0.5% | 6.0% | 35 |
| SiO2 Nanoparticles | Metal Oxide | 0.5% | 7.0% | 25 |

### Solvents

| Solvent | Density (g/cm³) | Min Loading | Max Loading | Cost (€/kg) |
|---------|:---------------:|:-----------:|:-----------:|:-----------:|
| Xylene | 0.87 | 10% | 40% | 1.20 |
| Butyl Acetate | 0.88 | 10% | 40% | 1.50 |
| Water | 1.00 | 5% | 30% | 0.01 |
| Acetone | 0.79 | 5% | 30% | 1.00 |
| Ethanol | 0.79 | 5% | 25% | 0.80 |
| Toluene | 0.87 | 10% | 40% | 1.30 |

### Additives

| Additive | Min Loading | Max Loading | Cost (€/kg) |
|----------|:-----------:|:-----------:|:-----------:|
| Dispersant (BYK-110) | 0.1% | 2.0% | 15.00 |
| Defoamer (BYK-024) | 0.05% | 1.0% | 18.00 |
| Curing Agent (Amine) | 10% | 25% | 8.00 |
| UV Absorber | 0.5% | 3.0% | 25.00 |
| Rheology Modifier | 0.1% | 2.5% | 12.00 |

### Fillers

| Filler | Min Loading | Max Loading | Cost (€/kg) |
|--------|:-----------:|:-----------:|:-----------:|
| Glass Fibers (short) | 5% | 30% | 3.00 |
| Carbon Fibers (milled) | 5% | 25% | 25.00 |
| Aramid Pulp | 3% | 20% | 40.00 |
| Cellulose Nanofibers | 1% | 15% | 50.00 |

---

## 📈 Performance Predictions

| Property | Unit | Excellent | Good | Poor |
|----------|:----:|:---------:|:----:|:----:|
| Corrosion Rate | mm/year | <0.01 | 0.01-0.05 | >0.05 |
| Adhesion | MPa | >8 | 5-8 | <5 |
| Salt Spray | hours | >5000 | 2000-5000 | <2000 |
| Volume Solids | % | >70 | 60-70 | <60 |
| VOC | g/L | <250 | 250-420 | >420 |
| Service Life | years | >20 | 10-20 | <10 |

---

## ✅ ISO Standards Compliance

| Standard | Requirement | Acceptance Criteria |
|----------|-------------|---------------------|
| **ISO 12944-1** | Formulation weight | 100g ±5g |
| **ISO 12944-5** | Volume solids | ≥60% |
| **ISO 12944-5** | Resin content | ≥30% of solids |
| **ISO 9227** | Salt spray resistance | ≥1000 hours |
| **ISO 2409** | Cross-cut adhesion | Class 0 or 1 |
| **ISO 15184** | Pencil hardness | ≥H |
| **EU 2004/42/EC** | VOC limit | ≤420 g/L |

---

## 🔧 Validation Rules

| Category | Rule | Severity |
|----------|------|:--------:|
| Weight | Total weight must be 100g ±5g | Error |
| Resin | Resin content ≥30% of solids | Error |
| Solvent | Solvent content ≥15% of total | Error |
| Additive | Additive content ≤5% of total | Error |
| Nanocomposite | Nanocomposite loading ≤5% of solids | Error |
| Epoxy-Amine | Curing agent required with epoxy | Error |
| Nanocomposite | Ultrasonication required | Warning |

---

## 🛠️ Development

### Building Executable

| Platform | Command |
|----------|---------|
| Windows | `pyinstaller --onefile --windowed --name NanoCoatBuilder main.py` |
| Linux | `pyinstaller --onefile --name NanoCoatBuilder main.py` |
| macOS | `pyinstaller --onefile --windowed --name NanoCoatBuilder main.py` |

### Running Tests

```bash
python -m pytest tests/
```

### Adding New Ingredients

Edit `core/database/ingredient_db.py`:

```python
cls._ingredients["New Ingredient"] = Ingredient(
    name="New Ingredient",
    category="resin",  # resin, solvent, pigment, additive, nanocomposite, filler
    min_loading_wt=0,
    max_loading_wt=100,
    properties=ChemicalProperty(density=1.0, cost_per_kg=10.0)
)
```

---

## 📋 Changelog

| Version | Date | Changes |
|:-------:|:----:|---------|
| 1.0.0 | 2026-06 | Initial release |
| 1.0.1 | 2026-06 | Bug fixes and performance improvements |

---

## 👨‍💻 Author

**Oukil Khaled Ibn Elwalid**

| Platform | Link |
|----------|------|
| GitHub | [@khadev](https://github.com/khadev) |
| Email | oukil.khaled@gmail.com |

---

## 🙏 Acknowledgments

| Tool/Framework | Purpose |
|----------------|---------|
| Qt for Python (PySide6) | GUI Framework |
| Matplotlib | Graphing capabilities |
| Pydantic | Data validation |
| NumPy | Numerical computations |

---

<div align="center">
<br>
<strong>Made with 🔬 for the research community</strong><br>
<sub>© 2026 Oukil Khaled Ibn Elwalid</sub>
</div>
