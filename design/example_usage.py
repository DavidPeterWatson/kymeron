#!/usr/bin/env python3
"""
Example usage of the Flexure Force Calculator
This script demonstrates how to use the flexure calculator programmatically
rather than through the interactive interface.
"""

from design.flexure_calculator import (
    MATERIALS,
    calculate_max_force_cantilever,
    calculate_max_force_parallel,
    plot_force_vs_thickness
)

def main():
    """Example usage of the flexure calculator"""
    print("Flexure Calculator Example Usage")
    print("================================")
    
    # Example 1: Calculate force for a spring steel cantilever flexure
    print("\nExample 1: Spring Steel Cantilever Flexure")
    material = MATERIALS["spring_steel"]
    length = 50.0  # mm
    width = 20.0   # mm
    thickness = 0.5  # mm
    
    max_force, max_deflection = calculate_max_force_cantilever(
        length, width, thickness, material
    )
    
    print(f"Material: {material.name}")
    print(f"Dimensions: {length}mm x {width}mm x {thickness}mm")
    print(f"Maximum force: {max_force:.2f} N ({max_force/9.81:.2f} kg)")
    print(f"Maximum deflection: {max_deflection:.2f} mm")
    
    # Example 2: Compare different materials for the same dimensions
    print("\nExample 2: Material Comparison (Parallel Flexure)")
    print(f"Dimensions: {length}mm x {width}mm x {thickness}mm")
    print("Material                  Max Force (N)    Max Deflection (mm)")
    print("----------------------------------------------------------")
    
    for material_key, material in MATERIALS.items():
        max_force, max_deflection = calculate_max_force_parallel(
            length, width, thickness, material
        )
        print(f"{material.name:<25} {max_force:>10.2f} N      {max_deflection:>10.2f}")
    
    # Example 3: Generate a plot for different thicknesses
    print("\nExample 3: Generating force vs thickness plot for spring steel")
    material = MATERIALS["spring_steel"]
    thickness_range = (0.1, 1.0, 0.05)  # min, max, step in mm
    
    plot_force_vs_thickness(
        length, width, thickness_range, material, "cantilever"
    )
    
    print("Plot generated and saved as 'Spring_Steel_cantilever_force_deflection.png'")

if __name__ == "__main__":
    main() 