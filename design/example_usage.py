#!/usr/bin/env python3
"""
Example usage of the Flexure Force Calculator
This script demonstrates how to use the flexure calculator programmatically
rather than through the interactive interface.
"""

from flexure_calculator import (
    MATERIALS,
    calculate_max_force_cantilever,
    calculate_max_force_parallel,
    calculate_in_plane_tension,
    calculate_buckling_critical_load,
    calculate_plate_buckling,
    plot_force_vs_thickness
)

def main():
    """Example usage of the flexure calculator"""
    print("Flexure Calculator Example Usage")
    print("================================")
    
    # Example 1: Calculate force for a spring steel cantilever flexure (out-of-plane bending)
    print("\nExample 1: Spring Steel Cantilever Flexure (Out-of-plane Bending)")
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
    
    # Example 2: In-plane tension (force colinear with length and width)
    print("\nExample 2: In-plane Tension (Force Colinear with Length)")
    max_force, max_elongation = calculate_in_plane_tension(
        length, width, thickness, material
    )
    
    print(f"Material: {material.name}")
    print(f"Dimensions: {length}mm x {width}mm x {thickness}mm")
    print(f"Maximum tensile force: {max_force:.2f} N ({max_force/9.81:.2f} kg)")
    print(f"Maximum elongation: {max_elongation:.2f} mm")
    
    # Example 3: Buckling (in-plane compression)
    print("\nExample 3: Buckling Analysis (In-plane Compression)")
    
    # Fixed-fixed end condition (k=4.0)
    end_condition = 4.0
    
    euler_critical_load = calculate_buckling_critical_load(
        length, width, thickness, material, end_condition
    )
    
    plate_critical_load = calculate_plate_buckling(
        length, width, thickness, material, k=6.97  # k for fixed edges
    )
    
    critical_load = min(euler_critical_load, plate_critical_load)
    
    print(f"Material: {material.name}")
    print(f"Dimensions: {length}mm x {width}mm x {thickness}mm")
    print(f"End condition: Fixed-fixed (k={end_condition})")
    print(f"Euler column buckling load: {euler_critical_load:.2f} N ({euler_critical_load/9.81:.2f} kg)")
    print(f"Plate buckling load: {plate_critical_load:.2f} N ({plate_critical_load/9.81:.2f} kg)")
    print(f"Critical buckling load (minimum): {critical_load:.2f} N ({critical_load/9.81:.2f} kg)")
    
    # Example 4: Compare different materials for in-plane loading
    print("\nExample 4: Material Comparison (In-plane Loading)")
    print(f"Dimensions: {length}mm x {width}mm x {thickness}mm")
    print("\nTensile Loading:")
    print("Material                  Max Tensile Force (N)    Max Elongation (mm)")
    print("------------------------------------------------------------------")
    
    for material_key, material in MATERIALS.items():
        max_force, max_elongation = calculate_in_plane_tension(
            length, width, thickness, material
        )
        print(f"{material.name:<25} {max_force:>15.2f} N      {max_elongation:>10.2f}")
    
    print("\nCompressive Loading (Buckling):")
    print("Material                  Critical Buckling Load (N)")
    print("------------------------------------------------")
    
    for material_key, material in MATERIALS.items():
        euler_load = calculate_buckling_critical_load(
            length, width, thickness, material, end_condition=4.0
        )
        plate_load = calculate_plate_buckling(
            length, width, thickness, material, k=6.97
        )
        critical_load = min(euler_load, plate_load)
        print(f"{material.name:<25} {critical_load:>15.2f} N")
    
    # Example 5: Generate plots for different loading types
    print("\nExample 5: Generating force vs thickness plots")
    material = MATERIALS["spring_steel"]
    thickness_range = (0.1, 1.0, 0.05)  # min, max, step in mm
    
    # Plot for out-of-plane bending (cantilever)
    plot_force_vs_thickness(
        length, width, thickness_range, material, "cantilever"
    )
    print("Plot generated for cantilever flexure")
    
    # Plot for in-plane tension
    plot_force_vs_thickness(
        length, width, thickness_range, material, "in_plane"
    )
    print("Plot generated for in-plane tension")
    
    # Plot for buckling
    plot_force_vs_thickness(
        length, width, thickness_range, material, "buckling"
    )
    print("Plot generated for buckling")
    
    # Example 6: Specific case for cartesian maker machine bed flexures
    print("\nExample 6: Cartesian Maker Machine Bed Flexures")
    
    # Typical dimensions for a bed flexure
    length = 75.0  # mm
    width = 25.0   # mm
    thickness = 0.5  # mm  # Spring steel sheet
    material = MATERIALS["spring_steel"]
    
    # For flexures oriented perpendicular to the diagonals
    # The force is in-plane with the flexure
    max_tensile_force, _ = calculate_in_plane_tension(
        length, width, thickness, material
    )
    
    critical_buckling_load = min(
        calculate_buckling_critical_load(length, width, thickness, material, end_condition=4.0),
        calculate_plate_buckling(length, width, thickness, material, k=6.97)
    )
    
    print(f"Bed flexure dimensions: {length}mm x {width}mm x {thickness}mm")
    print(f"Material: {material.name}")
    print(f"Maximum tensile force: {max_tensile_force:.2f} N ({max_tensile_force/9.81:.2f} kg)")
    print(f"Critical buckling load: {critical_buckling_load:.2f} N ({critical_buckling_load/9.81:.2f} kg)")
    print(f"Safe working load (compression): {critical_buckling_load/2:.2f} N ({critical_buckling_load/9.81/2:.2f} kg)")


if __name__ == "__main__":
    main() 