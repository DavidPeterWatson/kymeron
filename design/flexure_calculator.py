#!/usr/bin/env python3
"""
Flexure Force Calculator

This script calculates the maximum force a spring steel flexure can withstand
before permanent deformation occurs. It's designed for use with cartesian maker
machines that use flexures to provide rigidity in specific directions while
allowing flexibility in others.
"""

import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass


@dataclass
class FlexureMaterial:
    """Material properties for flexures"""
    name: str
    elastic_modulus: float  # Young's modulus in GPa
    yield_strength: float   # Yield strength in MPa
    poisson_ratio: float    # Poisson's ratio (dimensionless)


# Common materials used for flexures
MATERIALS = {
    "spring_steel": FlexureMaterial(
        name="Spring Steel",
        elastic_modulus=200.0,  # GPa
        yield_strength=1100.0,  # MPa
        poisson_ratio=0.29
    ),
    "stainless_steel": FlexureMaterial(
        name="Stainless Steel 304",
        elastic_modulus=193.0,  # GPa
        yield_strength=215.0,   # MPa
        poisson_ratio=0.29
    ),
    "titanium": FlexureMaterial(
        name="Titanium Alloy (Ti-6Al-4V)",
        elastic_modulus=114.0,  # GPa
        yield_strength=880.0,   # MPa
        poisson_ratio=0.34
    ),
    "aluminum": FlexureMaterial(
        name="Aluminum 7075-T6",
        elastic_modulus=71.0,   # GPa
        yield_strength=503.0,   # MPa
        poisson_ratio=0.33
    )
}


def calculate_max_force_cantilever(length, width, thickness, material, safety_factor=1.5):
    """
    Calculate maximum force for a cantilever beam flexure before permanent deformation.
    
    Args:
        length: Length of the flexure in mm
        width: Width of the flexure in mm
        thickness: Thickness of the flexure in mm
        material: Material properties (FlexureMaterial object)
        safety_factor: Safety factor to apply (default: 1.5)
        
    Returns:
        max_force: Maximum force in Newtons
        max_deflection: Maximum deflection in mm
    """
    # Convert units
    length_m = length / 1000  # mm to m
    width_m = width / 1000    # mm to m
    thickness_m = thickness / 1000  # mm to m
    
    # Calculate area moment of inertia for rectangular cross-section
    I = (width_m * thickness_m**3) / 12  # m^4
    
    # Calculate section modulus
    Z = I / (thickness_m / 2)  # m^3
    
    # Calculate maximum bending moment before yield
    yield_strength_pa = material.yield_strength * 1e6  # MPa to Pa
    max_moment = yield_strength_pa * Z / safety_factor  # N·m
    
    # Calculate maximum force
    max_force = max_moment / length_m  # N
    
    # Calculate maximum deflection at yield
    E = material.elastic_modulus * 1e9  # GPa to Pa
    max_deflection = (max_force * length_m**3) / (3 * E * I) * 1000  # m to mm
    
    return max_force, max_deflection


def calculate_max_force_parallel(length, width, thickness, material, safety_factor=1.5):
    """
    Calculate maximum force for a parallel beam flexure before permanent deformation.
    
    Args:
        length: Length of the flexure in mm
        width: Width of the flexure in mm
        thickness: Thickness of the flexure in mm
        material: Material properties (FlexureMaterial object)
        safety_factor: Safety factor to apply (default: 1.5)
        
    Returns:
        max_force: Maximum force in Newtons
        max_deflection: Maximum deflection in mm
    """
    # Convert units
    length_m = length / 1000  # mm to m
    width_m = width / 1000    # mm to m
    thickness_m = thickness / 1000  # mm to m
    
    # Calculate area moment of inertia for rectangular cross-section
    I = (width_m * thickness_m**3) / 12  # m^4
    
    # Calculate section modulus
    Z = I / (thickness_m / 2)  # m^3
    
    # Calculate maximum bending moment before yield
    yield_strength_pa = material.yield_strength * 1e6  # MPa to Pa
    max_moment = yield_strength_pa * Z / safety_factor  # N·m
    
    # For parallel beam flexure, the maximum force is different than cantilever
    max_force = (2 * max_moment) / length_m  # N
    
    # Calculate maximum deflection at yield
    E = material.elastic_modulus * 1e9  # GPa to Pa
    max_deflection = (max_force * length_m**3) / (12 * E * I) * 1000  # m to mm
    
    return max_force, max_deflection


def plot_force_vs_thickness(length, width, thickness_range, material, flexure_type="cantilever"):
    """
    Plot the relationship between flexure thickness and maximum force.
    
    Args:
        length: Length of the flexure in mm
        width: Width of the flexure in mm
        thickness_range: Range of thicknesses to plot (tuple of min, max, step)
        material: Material properties (FlexureMaterial object)
        flexure_type: Type of flexure ("cantilever" or "parallel")
    """
    thicknesses = np.arange(thickness_range[0], thickness_range[1], thickness_range[2])
    forces = []
    deflections = []
    
    for t in thicknesses:
        if flexure_type == "cantilever":
            force, deflection = calculate_max_force_cantilever(length, width, t, material)
        else:
            force, deflection = calculate_max_force_parallel(length, width, t, material)
        forces.append(force)
        deflections.append(deflection)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    ax1.plot(thicknesses, forces)
    ax1.set_xlabel('Thickness (mm)')
    ax1.set_ylabel('Maximum Force (N)')
    ax1.set_title(f'Maximum Force vs. Thickness\n({material.name}, {flexure_type})')
    ax1.grid(True)
    
    ax2.plot(thicknesses, deflections)
    ax2.set_xlabel('Thickness (mm)')
    ax2.set_ylabel('Maximum Deflection (mm)')
    ax2.set_title(f'Maximum Deflection vs. Thickness\n({material.name}, {flexure_type})')
    ax2.grid(True)
    
    plt.tight_layout()
    plt.savefig(f'{material.name.replace(" ", "_")}_{flexure_type}_force_deflection.png')
    plt.show()


def main():
    """Main function to run the calculator interactively"""
    print("Flexure Force Calculator")
    print("=======================")
    
    # Display available materials
    print("\nAvailable materials:")
    for i, (key, material) in enumerate(MATERIALS.items(), 1):
        print(f"{i}. {material.name} (E={material.elastic_modulus} GPa, σy={material.yield_strength} MPa)")
    
    # Get material selection
    while True:
        try:
            material_idx = int(input("\nSelect material (number): ")) - 1
            if 0 <= material_idx < len(MATERIALS):
                material_key = list(MATERIALS.keys())[material_idx]
                material = MATERIALS[material_key]
                break
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Get flexure type
    while True:
        flexure_type = input("\nFlexure type (cantilever/parallel): ").lower()
        if flexure_type in ["cantilever", "parallel"]:
            break
        else:
            print("Invalid flexure type. Please enter 'cantilever' or 'parallel'.")
    
    # Get dimensions
    length = float(input("\nFlexure length (mm): "))
    width = float(input("Flexure width (mm): "))
    thickness = float(input("Flexure thickness (mm): "))
    safety_factor = float(input("Safety factor (default 1.5): ") or "1.5")
    
    # Calculate and display results
    if flexure_type == "cantilever":
        max_force, max_deflection = calculate_max_force_cantilever(
            length, width, thickness, material, safety_factor
        )
    else:
        max_force, max_deflection = calculate_max_force_parallel(
            length, width, thickness, material, safety_factor
        )
    
    print("\nResults:")
    print(f"Maximum force before deformation: {max_force:.2f} N ({max_force/9.81:.2f} kg)")
    print(f"Maximum deflection at yield: {max_deflection:.2f} mm")
    
    # Ask if user wants to plot force vs thickness
    plot_choice = input("\nDo you want to plot force vs thickness? (y/n): ").lower()
    if plot_choice == 'y':
        min_thickness = float(input("Minimum thickness (mm): "))
        max_thickness = float(input("Maximum thickness (mm): "))
        step = float(input("Step size (mm): "))
        
        plot_force_vs_thickness(
            length, width, (min_thickness, max_thickness, step), 
            material, flexure_type
        )


if __name__ == "__main__":
    main() 