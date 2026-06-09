"""Performance graph widget with matplotlib and dynamic colors based on thresholds."""

import matplotlib
matplotlib.use('Qt5Agg')

from PySide6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle


class PerformanceGraphWidget(FigureCanvas):
    def __init__(self, result, parent=None):
        self.result = result
        self.figure = Figure(figsize=(12, 10), dpi=100)
        super().__init__(self.figure)
        self.setParent(parent)
        self.setMinimumHeight(800)
        self.setMinimumWidth(1000)
        
        # Define thresholds
        self.thresholds = {
            'salt_spray': {'min': 1000, 'target': 2000, 'excellent': 5000},
            'adhesion': {'min': 5, 'target': 8, 'excellent': 12},
            'corrosion_rate': {'min': 0.05, 'target': 0.01, 'excellent': 0.005},
            'volume_solids': {'min': 60, 'target': 70, 'excellent': 80},
            'voc': {'min': 420, 'target': 250, 'excellent': 100},  # Lower is better
            'service_life': {'min': 10, 'target': 20, 'excellent': 30}
        }
        
        self.plot_data()
    
    def get_color(self, value, key, lower_is_better=False):
        """Return color based on value thresholds."""
        thresholds = self.thresholds[key]
        
        if lower_is_better:
            # For VOC - lower is better
            if value <= thresholds['excellent']:
                return '#4CAF50'  # Green - Excellent
            elif value <= thresholds['target']:
                return '#8BC34A'  # Light Green - Good
            elif value <= thresholds['min']:
                return '#FF9800'  # Orange - Warning
            else:
                return '#f44336'  # Red - Fail
        else:
            # For most metrics - higher is better
            if value >= thresholds['excellent']:
                return '#4CAF50'  # Green - Excellent
            elif value >= thresholds['target']:
                return '#8BC34A'  # Light Green - Good
            elif value >= thresholds['min']:
                return '#FF9800'  # Orange - Warning
            else:
                return '#f44336'  # Red - Fail
    
    def calculate_service_life(self, dft_um=160, corrosion_rate=None, environment_factor=1.0):
        """
        Calculate scientifically plausible service life.
        
        Formula: Service Life (years) = (DFT / (Corrosion Rate * 1000)) * Environment Factor
        
        Where:
        - DFT: Dry Film Thickness in micrometers (typical: 160 for C5 environment)
        - Corrosion Rate: in mm/year
        - Environment Factor: 
            1.0 = C5 (very high corrosivity - marine/offshore)
            0.7 = C4 (high - industrial)
            0.5 = C3 (medium - urban)
            0.3 = C2 (low - rural)
            0.1 = C1 (very low - dry indoor)
        
        ISO 12944-5 minimum DFT: 160μm for C5 environment
        """
        if corrosion_rate is None or corrosion_rate <= 0:
            return 0
        
        # Convert DFT from μm to mm for calculation
        dft_mm = dft_um / 1000
        
        # Calculate life based on coating thickness and corrosion rate
        base_life = dft_mm / corrosion_rate
        
        # Apply environment factor
        service_life = base_life * environment_factor
        
        return service_life
    
    def get_environment_factor(self, environment):
        """Return environment factor based on ISO 12944-2 classification."""
        env_factors = {
            'C1': 0.1,
            'C2': 0.3,
            'C3': 0.5,
            'C4': 0.7,
            'C5': 1.0,
            'CX': 1.2
        }
        for key, factor in env_factors.items():
            if key in environment:
                return factor
        return 0.7  # Default to C4
    
    def plot_data(self):
        self.figure.clear()
        p = self.result.performance
        f = self.result.formulation
        
        # Get environment factor for service life calculation
        env_factor = self.get_environment_factor(f.target_environment)
        
        # Calculate scientifically plausible service life
        calculated_life = self.calculate_service_life(
            dft_um=160,
            corrosion_rate=p.corrosion_rate_mm_year,
            environment_factor=env_factor
        )
        
        # Use calculated life if it's more accurate than estimated
        if calculated_life > 0:
            service_life = calculated_life
        else:
            service_life = p.estimated_life_years
        
        # Create subplots
        gs = self.figure.add_gridspec(2, 2, hspace=0.3, wspace=0.3)
        
        # Graph 1: Key Performance Indicators
        ax1 = self.figure.add_subplot(gs[0, 0])
        categories = ['Corrosion\nRate', 'Adhesion', 'Contact\nAngle']
        values = [
            p.corrosion_rate_mm_year if p.corrosion_rate_mm_year else 0,
            p.adhesion_MPa if p.adhesion_MPa else 0,
            p.contact_angle_degrees if p.contact_angle_degrees else 0
        ]
        
        # Get colors for each metric
        colors1 = [
            self.get_color(values[0], 'corrosion_rate', lower_is_better=True),
            self.get_color(values[1], 'adhesion', lower_is_better=False),
            '#45b7d1'  # Default for contact angle
        ]
        
        bars1 = ax1.bar(categories, values, color=colors1, edgecolor='white', linewidth=2)
        ax1.set_ylabel('Value', fontsize=10, fontweight='bold')
        ax1.set_title('Key Performance Indicators', fontweight='bold', fontsize=12)
        ax1.grid(True, alpha=0.3, axis='y')
        
        # Add value labels
        for bar, val in zip(bars1, values):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(values)*0.02,
                    f'{val:.2f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        # Add threshold lines for adhesion
        ax1.axhline(y=self.thresholds['adhesion']['min'], color='red', linestyle='--', 
                   linewidth=1, alpha=0.7, label=f'Min: {self.thresholds["adhesion"]["min"]} MPa')
        ax1.axhline(y=self.thresholds['adhesion']['target'], color='orange', linestyle='--', 
                   linewidth=1, alpha=0.7, label=f'Target: {self.thresholds["adhesion"]["target"]} MPa')
        ax1.legend(loc='upper left', fontsize=8)
        
        # Graph 2: Salt Spray Resistance with dynamic color
        ax2 = self.figure.add_subplot(gs[0, 1])
        salt_spray = p.salt_spray_hours if p.salt_spray_hours else 0
        salt_color = self.get_color(salt_spray, 'salt_spray', lower_is_better=False)
        
        ax2.barh(['Salt Spray\nResistance'], [salt_spray], color=salt_color, edgecolor='white', linewidth=2)
        ax2.set_xlabel('Hours', fontsize=10, fontweight='bold')
        ax2.set_title('Salt Spray Resistance', fontweight='bold', fontsize=12)
        
        # Add threshold lines
        ax2.axvline(x=self.thresholds['salt_spray']['min'], color='red', linestyle='--', 
                   linewidth=2, label=f'Min: {self.thresholds["salt_spray"]["min"]}h')
        ax2.axvline(x=self.thresholds['salt_spray']['target'], color='orange', linestyle='--', 
                   linewidth=2, label=f'Target: {self.thresholds["salt_spray"]["target"]}h')
        ax2.axvline(x=self.thresholds['salt_spray']['excellent'], color='green', linestyle='--', 
                   linewidth=2, label=f'Excellent: {self.thresholds["salt_spray"]["excellent"]}h')
        
        ax2.legend(loc='lower right', fontsize=8)
        ax2.grid(True, alpha=0.3, axis='x')
        
        # Add value label
        ax2.text(salt_spray, 0, f' {salt_spray:,.0f}h', va='center', fontsize=10, fontweight='bold')
        
        # Add status text
        if salt_spray >= self.thresholds['salt_spray']['excellent']:
            status = "EXCELLENT"
            status_color = "#4CAF50"
        elif salt_spray >= self.thresholds['salt_spray']['target']:
            status = "GOOD"
            status_color = "#8BC34A"
        elif salt_spray >= self.thresholds['salt_spray']['min']:
            status = "WARNING - Below Target"
            status_color = "#FF9800"
        else:
            status = "FAIL - Below Minimum"
            status_color = "#f44336"
        
        ax2.text(salt_spray + self.thresholds['salt_spray']['min']*0.1, 0, 
                f'  {status}', va='center', fontsize=9, fontweight='bold', color=status_color)
        
        # Graph 3: Economic & Environmental Performance
        ax3 = self.figure.add_subplot(gs[1, 0])
        categories2 = ['Cost per L\n(€)', 'Volume Solids\n(%)', 'VOC\n(g/L)']
        values2 = [
            p.cost_per_liter if p.cost_per_liter else 0,
            p.theoretical_volume_solids if p.theoretical_volume_solids else 0,
            p.theoretical_voc if p.theoretical_voc else 0
        ]
        
        # Get colors for each metric
        colors3 = [
            '#f9ca24',  # Cost - neutral
            self.get_color(values2[1], 'volume_solids', lower_is_better=False),
            self.get_color(values2[2], 'voc', lower_is_better=True)
        ]
        
        bars3 = ax3.bar(categories2, values2, color=colors3, edgecolor='white', linewidth=2)
        ax3.set_ylabel('Value', fontsize=10, fontweight='bold')
        ax3.set_title('Economic & Environmental Performance', fontweight='bold', fontsize=12)
        ax3.grid(True, alpha=0.3, axis='y')
        
        # Add threshold lines
        ax3.axhline(y=self.thresholds['volume_solids']['min'], color='red', linestyle='--', 
                   linewidth=1.5, alpha=0.7, label=f'Min Solids: {self.thresholds["volume_solids"]["min"]}%')
        ax3.axhline(y=self.thresholds['voc']['min'], color='red', linestyle='--', 
                   linewidth=1.5, alpha=0.7, label=f'VOC Limit: {self.thresholds["voc"]["min"]} g/L')
        ax3.legend(loc='upper right', fontsize=8)
        
        # Add value labels
        for bar, val in zip(bars3, values2):
            ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(values2)*0.02,
                    f'{val:.1f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        # Graph 4: Service Life Expectancy with dynamic color
        ax4 = self.figure.add_subplot(gs[1, 1])
        max_life = max(30, service_life + 5)
        life_color = self.get_color(service_life, 'service_life', lower_is_better=False)
        
        ax4.barh(['Calculated\nService Life'], [service_life], color=life_color, edgecolor='white', linewidth=2)
        ax4.set_xlabel('Years', fontsize=10, fontweight='bold')
        ax4.set_title(f'Expected Service Life: {service_life:.1f} years', fontweight='bold', fontsize=12)
        ax4.set_xlim(0, max_life)
        
        # Add threshold lines
        ax4.axvline(x=self.thresholds['service_life']['min'], color='red', linestyle='--', 
                   linewidth=2, label=f'Min: {self.thresholds["service_life"]["min"]} years')
        ax4.axvline(x=self.thresholds['service_life']['target'], color='orange', linestyle='--', 
                   linewidth=2, label=f'Target: {self.thresholds["service_life"]["target"]} years')
        ax4.axvline(x=self.thresholds['service_life']['excellent'], color='green', linestyle='--', 
                   linewidth=2, label=f'Excellent: {self.thresholds["service_life"]["excellent"]} years')
        
        ax4.legend(loc='lower right', fontsize=8)
        ax4.grid(True, alpha=0.3, axis='x')
        
        # Add value label
        ax4.text(service_life, 0, f' {service_life:.1f} years', va='center', fontsize=10, fontweight='bold')
        
        # Add status text
        if service_life >= self.thresholds['service_life']['excellent']:
            status = "EXCELLENT"
            status_color = "#4CAF50"
        elif service_life >= self.thresholds['service_life']['target']:
            status = "GOOD"
            status_color = "#8BC34A"
        elif service_life >= self.thresholds['service_life']['min']:
            status = "WARNING - Below Target"
            status_color = "#FF9800"
        else:
            status = "FAIL - Below Minimum"
            status_color = "#f44336"
        
        ax4.text(service_life + 1, 0, f'  {status}', va='center', fontsize=9, fontweight='bold', color=status_color)
        
        # Add background color based on life expectancy
        if service_life >= self.thresholds['service_life']['excellent']:
            ax4.set_facecolor('#e8f5e9')
        elif service_life >= self.thresholds['service_life']['target']:
            ax4.set_facecolor('#f1f8e9')
        elif service_life >= self.thresholds['service_life']['min']:
            ax4.set_facecolor('#fff3e0')
        else:
            ax4.set_facecolor('#ffebee')
        
        # Add explanatory text for service life calculation
        ax4.text(0.5, -0.15, 
                f'Formula: Service Life = DFT / (Corrosion Rate × 1000) × Environment Factor\n'
                f'DFT = 160μm (ISO minimum), Environment Factor = {env_factor}',
                transform=ax4.transAxes, fontsize=8, ha='center', va='top',
                bbox=dict(boxstyle='round', facecolor='#f5f5f5', alpha=0.8))
        
        self.figure.tight_layout()
        self.draw()