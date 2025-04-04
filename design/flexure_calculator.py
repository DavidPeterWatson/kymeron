#!/usr/bin/env python3
"""
Flexure Force Calculator

This script calculates the maximum force a spring steel flexure can withstand
before permanent deformation occurs. It's designed for use with cartesian maker
machines that use flexures to provide rigidity in specific directions while
allowing flexibility in others.

The calculator handles both out-of-plane bending (traditional flexure) and
in-plane loading (force colinear with width and length of the plate).
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
    This is for out-of-plane loading (force perpendicular to the plate).
    
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
    This is for out-of-plane loading (force perpendicular to the plate).
    
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


def calculate_in_plane_tension(length, width, thickness, material, safety_factor=1.5):
    """
    Calculate maximum in-plane tensile force before yielding.
    This is for in-plane loading (force colinear with length and width).
    
    Args:
        length: Length of the flexure in mm
        width: Width of the flexure in mm
        thickness: Thickness of the flexure in mm
        material: Material properties (FlexureMaterial object)
        safety_factor: Safety factor to apply (default: 1.5)
        
    Returns:
        max_force: Maximum force in Newtons
        max_elongation: Maximum elongation in mm
    """
    # Convert units
    length_m = length / 1000  # mm to m
    width_m = width / 1000    # mm to m
    thickness_m = thickness / 1000  # mm to m
    
    # Calculate cross-sectional area
    area = width_m * thickness_m  # m^2
    
    # Calculate maximum stress before yield
    yield_strength_pa = material.yield_strength * 1e6  # MPa to Pa
    max_stress = yield_strength_pa / safety_factor  # Pa
    
    # Calculate maximum force
    max_force = max_stress * area  # N
    
    # Calculate maximum elongation at yield
    E = material.elastic_modulus * 1e9  # GPa to Pa
    max_strain = max_stress / E  # dimensionless
    max_elongation = max_strain * length_m * 1000  # m to mm
    
    return max_force, max_elongation


def calculate_buckling_critical_load(length, width, thickness, material, end_condition=4.0, safety_factor=1.5):
    """
    Calculate the critical buckling load for a thin plate under compression.
    This is for in-plane loading (force colinear with length and width).
    
    Args:
        length: Length of the flexure in mm
        width: Width of the flexure in mm
        thickness: Thickness of the flexure in mm
        material: Material properties (FlexureMaterial object)
        end_condition: End condition factor (default: 4.0 for fixed-fixed)
                      1.0: Pinned-pinned
                      2.0: Fixed-pinned
                      4.0: Fixed-fixed
        safety_factor: Safety factor to apply (default: 1.5)
        
    Returns:
        critical_load: Critical buckling load in Newtons
    """
    # Convert units
    length_m = length / 1000  # mm to m
    width_m = width / 1000    # mm to m
    thickness_m = thickness / 1000  # mm to m
    
    # Calculate area moment of inertia for buckling direction
    # For a plate loaded along its length, buckling occurs around the width axis
    I = (thickness_m * width_m**3) / 12  # m^4
    
    # Calculate cross-sectional area
    area = width_m * thickness_m  # m^2
    
    # Calculate Euler's critical buckling load
    E = material.elastic_modulus * 1e9  # GPa to Pa
    P_euler = (end_condition * np.pi**2 * E * I) / (length_m**2)  # N
    
    # Calculate slenderness ratio
    radius_of_gyration = np.sqrt(I / area)  # m
    slenderness_ratio = length_m / radius_of_gyration
    
    # Calculate Johnson's critical buckling load for intermediate columns
    yield_strength_pa = material.yield_strength * 1e6  # MPa to Pa
    P_johnson = area * yield_strength_pa * (1 - (yield_strength_pa * slenderness_ratio**2) / (4 * np.pi**2 * E))  # N
    
    # Use the smaller of Euler and Johnson buckling loads
    critical_load = min(P_euler, P_johnson) / safety_factor  # N
    
    return critical_load


def calculate_plate_buckling(length, width, thickness, material, k=4.0, safety_factor=1.5):
    """
    Calculate the critical buckling stress for a thin rectangular plate.
    This uses plate buckling theory rather than column buckling.
    
    Args:
        length: Length of the flexure in mm (direction of compression)
        width: Width of the flexure in mm
        thickness: Thickness of the flexure in mm
        material: Material properties (FlexureMaterial object)
        k: Buckling coefficient (depends on boundary conditions and aspect ratio)
           k=4.0 for simply supported edges
           k=6.97 for fixed edges
        safety_factor: Safety factor to apply (default: 1.5)
        
    Returns:
        critical_load: Critical buckling load in Newtons
    """
    # Convert units
    length_m = length / 1000  # mm to m
    width_m = width / 1000    # mm to m
    thickness_m = thickness / 1000  # mm to m
    
    # Calculate critical buckling stress using plate buckling formula
    E = material.elastic_modulus * 1e9  # GPa to Pa
    poisson = material.poisson_ratio
    
    # Critical stress formula for plate buckling
    critical_stress = (k * np.pi**2 * E) / (12 * (1 - poisson**2)) * (thickness_m / length_m)**2  # Pa
    
    # Calculate cross-sectional area
    area = width_m * thickness_m  # m^2
    
    # Calculate critical load
    critical_load = critical_stress * area / safety_factor  # N
    
    return critical_load


def calculate_deflection_due_to_force(length, width, thickness, material, force):
    """
    Calculate the deflection of a cantilever beam due to a force applied at one end.
    
    Args:
        length: Length of the flexure in mm
        width: Width of the flexure in mm
        thickness: Thickness of the flexure in mm
        material: Material properties (FlexureMaterial object)
        force: Force applied at the end in Newtons
        
    Returns:
        deflection: Deflection at the free end in mm
    """
    # Convert units
    length_m = length / 1000  # mm to m
    width_m = width / 1000    # mm to m
    thickness_m = thickness / 1000  # mm to m
    
    # Calculate area moment of inertia for rectangular cross-section
    I = (width_m * thickness_m**3) / 12  # m^4
    
    # Calculate deflection
    E = material.elastic_modulus * 1e9  # GPa to Pa
    deflection = (force * length_m**3) / (3 * E * I) * 1000  # m to mm
    
    return deflection


def calculate_force_for_deflection(length, width, thickness, material, deflection):
    """
    Calculate the force required to achieve a given deflection at the free end of a cantilever beam.
    
    Args:
        length: Length of the flexure in mm
        width: Width of the flexure in mm
        thickness: Thickness of the flexure in mm
        material: Material properties (FlexureMaterial object)
        deflection: Desired deflection at the free end in mm
        
    Returns:
        force: Force required in Newtons
    """
    # Convert units
    length_m = length / 1000  # mm to m
    width_m = width / 1000    # mm to m
    thickness_m = thickness / 1000  # mm to m
    
    # Calculate area moment of inertia for rectangular cross-section
    I = (width_m * thickness_m**3) / 12  # m^4
    
    # Calculate force
    E = material.elastic_modulus * 1e9  # GPa to Pa
    force = (3 * E * I * deflection / 1000) / (length_m**3)  # mm to m
    
    return force


def calculate_length_decrease_due_to_deflection(length, deflection, end_condition="fixed_free"):
    """
    Calculate the decrease in length of a flexure when it is deflected, based on the end condition.
    
    Args:
        length: Original length of the flexure in mm
        deflection: Deflection at the end in mm
        end_condition: Type of end condition ("fixed_free", "fixed_guided")
        
    Returns:
        length_decrease: Decrease in length in mm
    """
    if end_condition == "fixed_free":
        # For a cantilever (fixed-free), use the original formula
        length_decrease = (deflection**2) / (2 * length)
    elif end_condition == "fixed_guided":
        # For a fixed-guided beam, the decrease in length is typically less
        # due to the constraint on rotation at the guided end.
        # This is a simplified approximation.
        length_decrease = (deflection**2) / (3 * length)
    else:
        raise ValueError("Unsupported end condition. Choose 'fixed_free' or 'fixed_guided'.")
    
    return length_decrease


def calculate_deflection_fixed_guided(length, width, thickness, material, force):
    """
    Calculate the deflection of a beam with a fixed end and a guided end due to a force applied at the guided end.
    
    Args:
        length: Length of the flexure in mm
        width: Width of the flexure in mm
        thickness: Thickness of the flexure in mm
        material: Material properties (FlexureMaterial object)
        force: Force applied at the guided end in Newtons
        
    Returns:
        deflection: Deflection at the guided end in mm
    """
    # Convert units
    length_m = length / 1000  # mm to m
    width_m = width / 1000    # mm to m
    thickness_m = thickness / 1000  # mm to m
    
    # Calculate area moment of inertia for rectangular cross-section
    I = (width_m * thickness_m**3) / 12  # m^4
    
    # Calculate deflection
    E = material.elastic_modulus * 1e9  # GPa to Pa
    deflection = (force * length_m**3) / (12 * E * I) * 1000  # m to mm
    
    return deflection


def calculate_deflection_with_end_condition(length, width, thickness, material, force, end_condition="cantilever"):
    """
    Calculate the deflection of a beam based on the specified end condition.
    
    Args:
        length: Length of the flexure in mm
        width: Width of the flexure in mm
        thickness: Thickness of the flexure in mm
        material: Material properties (FlexureMaterial object)
        force: Force applied at the end in Newtons
        end_condition: Type of end condition ("cantilever", "fixed_guided")
        
    Returns:
        deflection: Deflection at the end in mm
    """
    if end_condition == "cantilever":
        return calculate_deflection_due_to_force(length, width, thickness, material, force)
    elif end_condition == "fixed_guided":
        return calculate_deflection_fixed_guided(length, width, thickness, material, force)
    else:
        raise ValueError("Unsupported end condition. Choose 'cantilever' or 'fixed_guided'.")


def calculate_force_for_deflection_fixed_guided(length, width, thickness, material, deflection):
    """
    Calculate the force required to achieve a given deflection at the guided end of a fixed-guided beam.
    
    Args:
        length: Length of the flexure in mm
        width: Width of the flexure in mm
        thickness: Thickness of the flexure in mm
        material: Material properties (FlexureMaterial object)
        deflection: Desired deflection at the guided end in mm
        
    Returns:
        force: Force required in Newtons
    """
    # Convert units
    length_m = length / 1000  # mm to m
    width_m = width / 1000    # mm to m
    thickness_m = thickness / 1000  # mm to m
    
    # Calculate area moment of inertia for rectangular cross-section
    I = (width_m * thickness_m**3) / 12  # m^4
    
    # Calculate force
    E = material.elastic_modulus * 1e9  # GPa to Pa
    force = (12 * E * I * deflection / 1000) / (length_m**3)  # mm to m
    
    return force


def calculate_force_for_deflection_with_end_condition(length, width, thickness, material, deflection, end_condition="cantilever"):
    """
    Calculate the force required to achieve a given deflection based on the specified end condition.
    
    Args:
        length: Length of the flexure in mm
        width: Width of the flexure in mm
        thickness: Thickness of the flexure in mm
        material: Material properties (FlexureMaterial object)
        deflection: Desired deflection at the end in mm
        end_condition: Type of end condition ("cantilever", "fixed_guided")
        
    Returns:
        force: Force required in Newtons
    """
    if end_condition == "cantilever":
        return calculate_force_for_deflection(length, width, thickness, material, deflection)
    elif end_condition == "fixed_guided":
        return calculate_force_for_deflection_fixed_guided(length, width, thickness, material, deflection)
    else:
        raise ValueError("Unsupported end condition. Choose 'cantilever' or 'fixed_guided'.")


def plot_force_vs_thickness(length, width, thickness_range, material, flexure_type="cantilever"):
    """
    Plot the relationship between flexure thickness and maximum force.
    
    Args:
        length: Length of the flexure in mm
        width: Width of the flexure in mm
        thickness_range: Range of thicknesses to plot (tuple of min, max, step)
        material: Material properties (FlexureMaterial object)
        flexure_type: Type of flexure ("cantilever", "parallel", "in_plane", "buckling")
    """
    thicknesses = np.arange(thickness_range[0], thickness_range[1], thickness_range[2])
    forces = []
    deflections_or_elongations = []
    
    for t in thicknesses:
        if flexure_type == "cantilever":
            force, deflection = calculate_max_force_cantilever(length, width, t, material)
            deflections_or_elongations.append(deflection)
        elif flexure_type == "parallel":
            force, deflection = calculate_max_force_parallel(length, width, t, material)
            deflections_or_elongations.append(deflection)
        elif flexure_type == "in_plane":
            force, elongation = calculate_in_plane_tension(length, width, t, material)
            deflections_or_elongations.append(elongation)
        elif flexure_type == "buckling":
            force = calculate_buckling_critical_load(length, width, t, material)
            plate_force = calculate_plate_buckling(length, width, t, material)
            # Use the smaller of the two buckling loads
            force = min(force, plate_force)
            deflections_or_elongations.append(0)  # No meaningful deflection for buckling
        forces.append(force)
    
    fig, ax1 = plt.subplots(figsize=(10, 6))
    
    ax1.plot(thicknesses, forces)
    ax1.set_xlabel('Thickness (mm)')
    ax1.set_ylabel('Maximum Force (N)')
    ax1.set_title(f'Maximum Force vs. Thickness\n({material.name}, {flexure_type})')
    ax1.grid(True)
    
    if flexure_type != "buckling":
        ax2 = ax1.twinx()
        ax2.plot(thicknesses, deflections_or_elongations, 'r-')
        if flexure_type == "in_plane":
            ax2.set_ylabel('Maximum Elongation (mm)', color='r')
        else:
            ax2.set_ylabel('Maximum Deflection (mm)', color='r')
        ax2.tick_params(axis='y', labelcolor='r')
    
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
    print("\nFlexure loading types:")
    print("1. Cantilever (out-of-plane bending)")
    print("2. Parallel (out-of-plane bending)")
    print("3. In-plane tension (force colinear with length)")
    print("4. Buckling (in-plane compression)")
    
    while True:
        try:
            flexure_type_idx = int(input("\nSelect loading type (number): "))
            if 1 <= flexure_type_idx <= 4:
                flexure_types = ["cantilever", "parallel", "in_plane", "buckling"]
                flexure_type = flexure_types[flexure_type_idx - 1]
                break
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Please enter a valid number.")
    
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
        print("\nResults:")
        print(f"Maximum force before deformation: {max_force:.2f} N ({max_force/9.81:.2f} kg)")
        print(f"Maximum deflection at yield: {max_deflection:.2f} mm")
        
    elif flexure_type == "parallel":
        max_force, max_deflection = calculate_max_force_parallel(
            length, width, thickness, material, safety_factor
        )
        print("\nResults:")
        print(f"Maximum force before deformation: {max_force:.2f} N ({max_force/9.81:.2f} kg)")
        print(f"Maximum deflection at yield: {max_deflection:.2f} mm")
        
    elif flexure_type == "in_plane":
        max_force, max_elongation = calculate_in_plane_tension(
            length, width, thickness, material, safety_factor
        )
        print("\nResults:")
        print(f"Maximum tensile force before yielding: {max_force:.2f} N ({max_force/9.81:.2f} kg)")
        print(f"Maximum elongation at yield: {max_elongation:.2f} mm")
        
    elif flexure_type == "buckling":
        # Get end condition for buckling
        print("\nEnd conditions for buckling:")
        print("1. Pinned-pinned (k=1.0)")
        print("2. Fixed-pinned (k=2.0)")
        print("3. Fixed-fixed (k=4.0)")
        
        while True:
            try:
                end_condition_idx = int(input("\nSelect end condition (number): "))
                if 1 <= end_condition_idx <= 3:
                    end_conditions = [1.0, 2.0, 4.0]
                    end_condition = end_conditions[end_condition_idx - 1]
                    break
                else:
                    print("Invalid selection. Please try again.")
            except ValueError:
                print("Please enter a valid number.")
        
        euler_critical_load = calculate_buckling_critical_load(
            length, width, thickness, material, end_condition, safety_factor
        )
        
        plate_critical_load = calculate_plate_buckling(
            length, width, thickness, material, 
            k=4.0 if end_condition_idx == 1 else 6.97,  # k depends on boundary conditions
            safety_factor=safety_factor
        )
        
        critical_load = min(euler_critical_load, plate_critical_load)
        
        print("\nResults:")
        print(f"Euler column buckling load: {euler_critical_load:.2f} N ({euler_critical_load/9.81:.2f} kg)")
        print(f"Plate buckling load: {plate_critical_load:.2f} N ({plate_critical_load/9.81:.2f} kg)")
        print(f"Critical buckling load (minimum): {critical_load:.2f} N ({critical_load/9.81:.2f} kg)")
    
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