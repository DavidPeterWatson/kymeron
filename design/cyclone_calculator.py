#!/usr/bin/env python3
"""
Cyclone Dust Collector Designer

This script calculates the optimal dimensions for a cyclone dust collector based on
input parameters such as airflow, inlet velocity, and particle size.

The calculation functions are separated from the main design function to allow for
designing multiple cyclones in series for separating particles of various sizes.
"""

import math
import matplotlib.pyplot as plt
import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional


@dataclass
class CycloneParameters:
    """Class to store cyclone dust collector parameters"""
    # Input parameters
    airflow: float  # in cubic meters per second (m³/s)
    inlet_velocity: float  # in meters per second (m/s)
    particle_size: float  # in micrometers (μm)
    gas_viscosity: float  # in kg/(m·s)
    gas_density: float  # in kg/m³
    particle_density: float  # in kg/m³
    
    # Calculated dimensions
    inlet_height: Optional[float] = None  # in meters
    inlet_width: Optional[float] = None  # in meters
    body_diameter: Optional[float] = None  # in meters
    cylinder_height: Optional[float] = None  # in meters
    cone_height: Optional[float] = None  # in meters
    vortex_finder_diameter: Optional[float] = None  # in meters
    vortex_finder_length: Optional[float] = None  # in meters
    dust_outlet_diameter: Optional[float] = None  # in meters
    total_height: Optional[float] = None  # in meters
    
    # Performance metrics
    pressure_drop: Optional[float] = None  # in pascals
    collection_efficiency: Optional[float] = None  # as a percentage
    cut_size: Optional[float] = None  # in micrometers


def calculate_inlet_dimensions(airflow: float, inlet_velocity: float) -> Tuple[float, float]:
    """
    Calculate the inlet dimensions based on airflow and inlet velocity.
    
    Args:
        airflow: Air flow rate in cubic meters per second (m³/s)
        inlet_velocity: Inlet velocity in meters per second (m/s)
        
    Returns:
        Tuple of (inlet_height, inlet_width) in meters
    """
    # The inlet area is determined by the airflow rate and inlet velocity
    inlet_area = airflow / inlet_velocity
    
    # For a rectangular inlet, we typically use a 1:2 height to width ratio
    inlet_width = math.sqrt(2 * inlet_area)
    inlet_height = inlet_area / inlet_width
    
    return inlet_height, inlet_width


def calculate_body_diameter(inlet_height: float, inlet_width: float) -> float:
    """
    Calculate the cyclone body diameter based on inlet dimensions.
    
    Args:
        inlet_height: Height of the inlet in meters
        inlet_width: Width of the inlet in meters
        
    Returns:
        Body diameter in meters
    """
    # The body diameter is typically 3-4 times the inlet width
    # We'll use 3.5 as a standard ratio
    body_diameter = 3.5 * inlet_width
    
    return body_diameter


def calculate_cylinder_height(body_diameter: float) -> float:
    """
    Calculate the cylinder height based on body diameter.
    
    Args:
        body_diameter: Body diameter in meters
        
    Returns:
        Cylinder height in meters
    """
    # The cylinder height is typically 1.5-2 times the body diameter
    # We'll use 1.75 as a standard ratio
    cylinder_height = 1.75 * body_diameter
    
    return cylinder_height


def calculate_cone_height(body_diameter: float) -> float:
    """
    Calculate the cone height based on body diameter.
    
    Args:
        body_diameter: Body diameter in meters
        
    Returns:
        Cone height in meters
    """
    # The cone height is typically 2-3 times the body diameter
    # We'll use 2.5 as a standard ratio
    cone_height = 2.5 * body_diameter
    
    return cone_height


def calculate_vortex_finder(body_diameter: float) -> Tuple[float, float]:
    """
    Calculate the vortex finder dimensions based on body diameter.
    
    Args:
        body_diameter: Body diameter in meters
        
    Returns:
        Tuple of (vortex_finder_diameter, vortex_finder_length) in meters
    """
    # The vortex finder diameter is typically 0.4-0.6 times the body diameter
    # We'll use 0.5 as a standard ratio
    vortex_finder_diameter = 0.5 * body_diameter
    
    # The vortex finder length is typically 0.5-0.8 times the body diameter
    # We'll use 0.6 as a standard ratio
    vortex_finder_length = 0.6 * body_diameter
    
    return vortex_finder_diameter, vortex_finder_length


def calculate_dust_outlet_diameter(body_diameter: float) -> float:
    """
    Calculate the dust outlet diameter based on body diameter.
    
    Args:
        body_diameter: Body diameter in meters
        
    Returns:
        Dust outlet diameter in meters
    """
    # The dust outlet diameter is typically 0.2-0.4 times the body diameter
    # We'll use 0.25 as a standard ratio
    dust_outlet_diameter = 0.25 * body_diameter
    
    return dust_outlet_diameter


def calculate_pressure_drop(
    airflow: float, 
    body_diameter: float, 
    inlet_height: float, 
    inlet_width: float,
    gas_density: float
) -> float:
    """
    Calculate the pressure drop across the cyclone.
    
    Args:
        airflow: Air flow rate in cubic meters per second (m³/s)
        body_diameter: Body diameter in meters
        inlet_height: Height of the inlet in meters
        inlet_width: Width of the inlet in meters
        gas_density: Density of the gas in kg/m³
        
    Returns:
        Pressure drop in pascals
    """
    # Calculate inlet velocity
    inlet_area = inlet_height * inlet_width
    inlet_velocity = airflow / inlet_area
    
    # Calculate the number of inlet velocity heads lost in the cyclone
    # This is an empirical value typically between 4-8
    velocity_heads = 6.0
    
    # Calculate pressure drop using the formula: ΔP = ρ * (v²/2) * velocity_heads
    # where ρ is gas density and v is inlet velocity
    pressure_drop = gas_density * (inlet_velocity ** 2 / 2) * velocity_heads
    
    return pressure_drop


def calculate_cut_size(
    body_diameter: float,
    airflow: float,
    gas_viscosity: float,
    particle_density: float,
    gas_density: float
) -> float:
    """
    Calculate the cut size (d50) of the cyclone.
    
    The cut size is the particle size that has a 50% chance of being collected.
    
    Args:
        body_diameter: Body diameter in meters
        airflow: Air flow rate in cubic meters per second (m³/s)
        gas_viscosity: Viscosity of the gas in kg/(m·s)
        particle_density: Density of the particles in kg/m³
        gas_density: Density of the gas in kg/m³
        
    Returns:
        Cut size in micrometers
    """
    # Calculate the effective number of turns in the cyclone
    # This is an empirical value typically between 5-10
    effective_turns = 8.0
    
    # Calculate the cut size using a simplified Lapple model
    # d50 = sqrt(9 * μ * W / (2 * π * N * v * (ρp - ρg)))
    # where:
    # μ = gas viscosity
    # W = body diameter
    # N = effective number of turns
    # v = inlet velocity
    # ρp = particle density
    # ρg = gas density
    
    # Calculate the inlet velocity based on the body diameter and airflow
    # Assuming the inlet area is approximately 0.1 * body_diameter²
    inlet_area = 0.1 * body_diameter ** 2
    inlet_velocity = airflow / inlet_area
    
    # Calculate the cut size in meters
    cut_size_m = math.sqrt(
        9 * gas_viscosity * body_diameter / 
        (2 * math.pi * effective_turns * inlet_velocity * (particle_density - gas_density))
    )
    
    # Convert to micrometers
    cut_size_um = cut_size_m * 1e6
    
    return cut_size_um


def calculate_collection_efficiency(
    particle_size: float,
    cut_size: float
) -> float:
    """
    Calculate the collection efficiency for a given particle size.
    
    Args:
        particle_size: Size of the particles in micrometers
        cut_size: Cut size (d50) of the cyclone in micrometers
        
    Returns:
        Collection efficiency as a percentage
    """
    # Using the Lapple model for collection efficiency
    # η = 1 / (1 + (d50/d)²)
    # where:
    # η = collection efficiency
    # d50 = cut size
    # d = particle size
    
    efficiency = 1 / (1 + (cut_size / particle_size) ** 2)
    
    # Convert to percentage
    efficiency_percent = efficiency * 100
    
    return efficiency_percent


def design_cyclone(params: CycloneParameters) -> CycloneParameters:
    """
    Design a cyclone dust collector based on input parameters.
    
    Args:
        params: CycloneParameters object with input parameters
        
    Returns:
        CycloneParameters object with calculated dimensions and performance metrics
    """
    # Calculate inlet dimensions
    params.inlet_height, params.inlet_width = calculate_inlet_dimensions(
        params.airflow, params.inlet_velocity
    )
    
    # Calculate body diameter
    params.body_diameter = calculate_body_diameter(params.inlet_height, params.inlet_width)
    
    # Calculate cylinder height
    params.cylinder_height = calculate_cylinder_height(params.body_diameter)
    
    # Calculate cone height
    params.cone_height = calculate_cone_height(params.body_diameter)
    
    # Calculate vortex finder dimensions
    params.vortex_finder_diameter, params.vortex_finder_length = calculate_vortex_finder(
        params.body_diameter
    )
    
    # Calculate dust outlet diameter
    params.dust_outlet_diameter = calculate_dust_outlet_diameter(params.body_diameter)
    
    # Calculate total height
    params.total_height = params.cylinder_height + params.cone_height
    
    # Calculate performance metrics
    params.pressure_drop = calculate_pressure_drop(
        params.airflow,
        params.body_diameter,
        params.inlet_height,
        params.inlet_width,
        params.gas_density
    )
    
    params.cut_size = calculate_cut_size(
        params.body_diameter,
        params.airflow,
        params.gas_viscosity,
        params.particle_density,
        params.gas_density
    )
    
    params.collection_efficiency = calculate_collection_efficiency(
        params.particle_size,
        params.cut_size
    )
    
    return params


def design_cyclone_series(
    airflow: float,
    inlet_velocity: float,
    particle_sizes: List[float],
    gas_viscosity: float = 1.81e-5,  # Air at 20°C
    gas_density: float = 1.2,  # Air at 20°C
    particle_density: float = 2500  # Wood dust
) -> List[CycloneParameters]:
    """
    Design a series of cyclones for separating particles of different sizes.
    
    Args:
        airflow: Initial air flow rate in cubic meters per second (m³/s)
        inlet_velocity: Inlet velocity in meters per second (m/s)
        particle_sizes: List of particle sizes to target in micrometers
        gas_viscosity: Viscosity of the gas in kg/(m·s)
        gas_density: Density of the gas in kg/m³
        particle_density: Density of the particles in kg/m³
        
    Returns:
        List of CycloneParameters objects for each cyclone in the series
    """
    cyclones = []
    current_airflow = airflow
    
    # Sort particle sizes from largest to smallest
    sorted_sizes = sorted(particle_sizes, reverse=True)
    
    for particle_size in sorted_sizes:
        params = CycloneParameters(
            airflow=current_airflow,
            inlet_velocity=inlet_velocity,
            particle_size=particle_size,
            gas_viscosity=gas_viscosity,
            gas_density=gas_density,
            particle_density=particle_density
        )
        
        # Design the cyclone
        designed_params = design_cyclone(params)
        cyclones.append(designed_params)
        
        # Reduce the airflow slightly for the next cyclone due to losses
        # Typically 2-5% loss per cyclone
        current_airflow *= 0.97
    
    return cyclones


def print_cyclone_design(params: CycloneParameters, index: Optional[int] = None) -> None:
    """
    Print the design parameters and performance metrics of a cyclone.
    
    Args:
        params: CycloneParameters object with calculated dimensions
        index: Optional index for the cyclone in a series
    """
    if index is not None:
        print(f"\n===== CYCLONE {index + 1} =====")
    else:
        print("\n===== CYCLONE DESIGN =====")
    
    print("\nInput Parameters:")
    print(f"Airflow: {params.airflow:.4f} m³/s ({params.airflow * 2118.88:.2f} CFM)")
    print(f"Inlet Velocity: {params.inlet_velocity:.2f} m/s")
    print(f"Target Particle Size: {params.particle_size:.2f} μm")
    print(f"Gas Viscosity: {params.gas_viscosity:.2e} kg/(m·s)")
    print(f"Gas Density: {params.gas_density:.2f} kg/m³")
    print(f"Particle Density: {params.particle_density:.2f} kg/m³")
    
    print("\nCalculated Dimensions:")
    print(f"Inlet Height: {params.inlet_height * 1000:.2f} mm")
    print(f"Inlet Width: {params.inlet_width * 1000:.2f} mm")
    print(f"Body Diameter: {params.body_diameter * 1000:.2f} mm")
    print(f"Cylinder Height: {params.cylinder_height * 1000:.2f} mm")
    print(f"Cone Height: {params.cone_height * 1000:.2f} mm")
    print(f"Vortex Finder Diameter: {params.vortex_finder_diameter * 1000:.2f} mm")
    print(f"Vortex Finder Length: {params.vortex_finder_length * 1000:.2f} mm")
    print(f"Dust Outlet Diameter: {params.dust_outlet_diameter * 1000:.2f} mm")
    print(f"Total Height: {params.total_height * 1000:.2f} mm")
    
    print("\nPerformance Metrics:")
    print(f"Pressure Drop: {params.pressure_drop:.2f} Pa ({params.pressure_drop / 249.09:.2f} inH₂O)")
    print(f"Cut Size (d50): {params.cut_size:.2f} μm")
    print(f"Collection Efficiency for {params.particle_size:.2f} μm particles: {params.collection_efficiency:.2f}%")


def plot_cyclone(params: CycloneParameters, ax=None) -> None:
    """
    Plot a simple 2D representation of the cyclone.
    
    Args:
        params: CycloneParameters object with calculated dimensions
        ax: Optional matplotlib axis to plot on
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 12))
    
    # Convert all dimensions to mm for better visualization
    bd = params.body_diameter * 1000
    ch = params.cylinder_height * 1000
    cnh = params.cone_height * 1000
    ih = params.inlet_height * 1000
    iw = params.inlet_width * 1000
    vfd = params.vortex_finder_diameter * 1000
    vfl = params.vortex_finder_length * 1000
    dod = params.dust_outlet_diameter * 1000
    
    # Plot the cylinder (upper part)
    cylinder_left = -bd/2
    cylinder_bottom = cnh  # Cone height is below the cylinder
    cylinder_width = bd
    cylinder_height = ch
    
    ax.add_patch(plt.Rectangle(
        (cylinder_left, cylinder_bottom),
        cylinder_width, cylinder_height,
        fill=False, edgecolor='blue', linewidth=2
    ))
    
    # Plot the cone (lower part)
    cone_top = cylinder_bottom  # Cone starts where cylinder ends
    cone_bottom = 0  # Cone bottom is at y=0
    cone_top_width = bd
    cone_bottom_width = dod
    
    cone_x = [
        -cone_top_width/2, -cone_bottom_width/2, 
        cone_bottom_width/2, cone_top_width/2
    ]
    cone_y = [cone_top, cone_bottom, cone_bottom, cone_top]
    
    ax.fill(cone_x, cone_y, fill=False, edgecolor='blue', linewidth=2)
    
    # Plot the inlet (on the side of the cylinder)
    inlet_left = cylinder_left - iw
    inlet_bottom = cylinder_bottom + ch - ih  # Near the top of the cylinder
    inlet_width = iw
    inlet_height = ih
    
    ax.add_patch(plt.Rectangle(
        (inlet_left, inlet_bottom),
        inlet_width, inlet_height,
        fill=False, edgecolor='red', linewidth=2
    ))
    
    # Plot the vortex finder (outlet at the top)
    vf_left = -vfd/2
    vf_bottom = cylinder_bottom + cylinder_height - vfl  # Extends from the top
    vf_width = vfd
    vf_height = vfl + 20  # Extend slightly above the cylinder for visibility
    
    ax.add_patch(plt.Rectangle(
        (vf_left, vf_bottom),
        vf_width, vf_height,
        fill=False, edgecolor='green', linewidth=2
    ))
    
    # Add labels
    ax.text(0, cone_top/2, f"Cone\nHeight\n{cnh:.1f} mm", 
            ha='center', va='center', fontsize=9)
    ax.text(0, cylinder_bottom + ch/2, f"Cylinder\nHeight\n{ch:.1f} mm", 
            ha='center', va='center', fontsize=9)
    ax.text(cylinder_left - iw/2, inlet_bottom + ih/2, f"Inlet\n{iw:.1f}x{ih:.1f} mm", 
            ha='center', va='center', fontsize=9)
    ax.text(0, vf_bottom + vfl/2, f"Vortex Finder\n{vfd:.1f}x{vfl:.1f} mm", 
            ha='center', va='center', fontsize=9)
    ax.text(0, cone_bottom - 20, f"Dust Outlet\n{dod:.1f} mm", 
            ha='center', va='center', fontsize=9)
    
    # Set axis limits and labels
    margin = max(bd, iw) * 0.2
    ax.set_xlim(cylinder_left - iw - margin, -cylinder_left + margin)
    ax.set_ylim(-margin - 40, cylinder_bottom + cylinder_height + vfl + margin)  # Adjusted for correct orientation
    ax.set_aspect('equal')
    ax.set_title('Cyclone Dust Collector Design')
    ax.set_xlabel('Width (mm)')
    ax.set_ylabel('Height (mm)')
    
    # Add dimensions
    ax.plot([cylinder_left, cylinder_left], [cylinder_bottom, cylinder_bottom + cylinder_height], 'k--', linewidth=1)
    ax.plot([cylinder_left + cylinder_width, cylinder_left + cylinder_width], 
            [cylinder_bottom, cylinder_bottom + cylinder_height], 'k--', linewidth=1)
    ax.plot([cylinder_left, cylinder_left + cylinder_width], 
            [cylinder_bottom, cylinder_bottom], 'k--', linewidth=1)
    
    # Add body diameter label
    ax.annotate(
        f'Body Diameter: {bd:.1f} mm',
        xy=(0, cylinder_bottom + 20),
        xytext=(0, cylinder_bottom + 100),
        ha='center',
        arrowprops=dict(arrowstyle='->'),
        fontsize=10
    )
    
    # Add dust collection bin suggestion (dotted lines)
    bin_height = 100  # Arbitrary height for the bin
    bin_width = bd * 1.2  # Slightly wider than the cyclone body
    bin_left = -bin_width/2
    bin_bottom = -bin_height
    
    ax.add_patch(plt.Rectangle(
        (bin_left, bin_bottom),
        bin_width, bin_height,
        fill=False, edgecolor='gray', linestyle='--', linewidth=1
    ))
    ax.text(0, bin_bottom + bin_height/2, "Dust Collection Bin\n(not to scale)", 
            ha='center', va='center', fontsize=8, color='gray')


def plot_efficiency_curve(cyclones: List[CycloneParameters]) -> None:
    """
    Plot the collection efficiency curve for each cyclone in the series.
    
    Args:
        cyclones: List of CycloneParameters objects
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Define a range of particle sizes to evaluate
    particle_sizes = np.logspace(0, 2, 100)  # 1 to 100 μm
    
    for i, cyclone in enumerate(cyclones):
        efficiencies = []
        for size in particle_sizes:
            efficiency = calculate_collection_efficiency(size, cyclone.cut_size)
            efficiencies.append(efficiency)
        
        ax.semilogx(particle_sizes, efficiencies, 
                   label=f'Cyclone {i+1} (d50 = {cyclone.cut_size:.2f} μm)')
    
    ax.grid(True, which="both", ls="-", alpha=0.2)
    ax.set_xlabel('Particle Size (μm)')
    ax.set_ylabel('Collection Efficiency (%)')
    ax.set_title('Cyclone Collection Efficiency vs. Particle Size')
    ax.set_xlim(1, 100)
    ax.set_ylim(0, 100)
    ax.legend()
    
    plt.tight_layout()
    plt.show()


def main():
    """
    Main function to demonstrate the cyclone design process.
    """
    print("Cyclone Dust Collector Designer")
    print("===============================")
    
    # Default values for a typical small CNC dust collection system
    default_airflow = 0.05  # m³/s (approximately 100 CFM)
    default_inlet_velocity = 20.0  # m/s
    default_particle_sizes = [30.0, 10.0, 5.0]  # μm
    default_gas_viscosity = 1.81e-5  # kg/(m·s) for air at 20°C
    default_gas_density = 1.2  # kg/m³ for air at 20°C
    default_particle_density = 700  # kg/m³ for wood dust
    
    # Get user input or use defaults
    try:
        print("\nEnter parameters (press Enter to use defaults):")
        
        airflow_input = input(f"Airflow in m³/s [{default_airflow}]: ")
        airflow = float(airflow_input) if airflow_input else default_airflow
        
        # Option to input airflow in CFM
        if airflow_input == "cfm":
            cfm_input = input("Airflow in CFM: ")
            airflow = float(cfm_input) / 2118.88  # Convert CFM to m³/s
        
        inlet_velocity_input = input(f"Inlet velocity in m/s [{default_inlet_velocity}]: ")
        inlet_velocity = float(inlet_velocity_input) if inlet_velocity_input else default_inlet_velocity
        
        particle_sizes_input = input(f"Particle sizes in μm (comma-separated) [{', '.join(map(str, default_particle_sizes))}]: ")
        particle_sizes = [float(x) for x in particle_sizes_input.split(',')] if particle_sizes_input else default_particle_sizes
        
        gas_viscosity_input = input(f"Gas viscosity in kg/(m·s) [{default_gas_viscosity}]: ")
        gas_viscosity = float(gas_viscosity_input) if gas_viscosity_input else default_gas_viscosity
        
        gas_density_input = input(f"Gas density in kg/m³ [{default_gas_density}]: ")
        gas_density = float(gas_density_input) if gas_density_input else default_gas_density
        
        particle_density_input = input(f"Particle density in kg/m³ [{default_particle_density}]: ")
        particle_density = float(particle_density_input) if particle_density_input else default_particle_density
        
    except ValueError:
        print("Invalid input. Using default values.")
        airflow = default_airflow
        inlet_velocity = default_inlet_velocity
        particle_sizes = default_particle_sizes
        gas_viscosity = default_gas_viscosity
        gas_density = default_gas_density
        particle_density = default_particle_density
    
    # Design the cyclone series
    cyclones = design_cyclone_series(
        airflow=airflow,
        inlet_velocity=inlet_velocity,
        particle_sizes=particle_sizes,
        gas_viscosity=gas_viscosity,
        gas_density=gas_density,
        particle_density=particle_density
    )
    
    # Print the design for each cyclone
    for i, cyclone in enumerate(cyclones):
        print_cyclone_design(cyclone, i)
    
    # Plot the cyclones
    fig, axes = plt.subplots(1, len(cyclones), figsize=(6 * len(cyclones), 10))
    if len(cyclones) == 1:
        axes = [axes]
    
    for i, (cyclone, ax) in enumerate(zip(cyclones, axes)):
        plot_cyclone(cyclone, ax)
        ax.set_title(f'Cyclone {i+1} Design')
    
    plt.tight_layout()
    
    # Plot the efficiency curves
    plot_efficiency_curve(cyclones)
    
    print("\nDesign complete! The plots show the cyclone dimensions and collection efficiency curves.")
    print("You can modify the input parameters to optimize the design for your specific needs.")


if __name__ == "__main__":
    main() 