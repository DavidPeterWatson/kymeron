# Flexure Force Calculator

A Python tool for calculating the maximum force a spring steel flexure can withstand before permanent deformation occurs. This is particularly useful for designing and analyzing flexures used in cartesian maker machines, automated tool changers, and other precision mechanical systems.

## Overview

Flexures are compliant mechanisms that provide motion through elastic deformation rather than traditional joints. They are commonly used in precision machines to:

- Allow motion in specific directions while providing rigidity in others
- Prevent binding due to small deviations in distances
- Eliminate backlash and friction issues associated with traditional joints

This calculator helps determine the maximum force a flexure can withstand before permanent deformation, which is critical for proper design and operation.

## Features

- Calculate maximum force and deflection for both cantilever and parallel beam flexures
- Support for multiple materials (Spring Steel, Stainless Steel, Titanium, Aluminum)
- Interactive command-line interface
- Visualization of force vs. thickness relationships
- Configurable safety factor

## Requirements

- Python 3.6+
- NumPy
- Matplotlib

Install dependencies with:

```bash
pip install numpy matplotlib
```

## Usage

Run the script with:

```bash
python flexure_calculator.py
```

Follow the interactive prompts to:
1. Select a material
2. Choose the flexure type (cantilever or parallel)
3. Enter dimensions (length, width, thickness)
4. Set a safety factor
5. Optionally generate plots

## Flexure Types

### Cantilever Flexure
A beam fixed at one end and free at the other. The force is applied at the free end.

### Parallel Flexure
Two beams connected in parallel, providing more stiffness in certain directions while maintaining flexibility in others.

## Example Application

In a cartesian maker machine with an automated tool changer, spring steel flexures might be used on the bed that moves up and down on the Z-axis. These flexures:

- Are attached at each corner to a linear rail
- Use simple sheets of spring steel as flexures
- Are oriented perpendicular to the diagonals to hold the bed in place
- Allow small deviations in one direction while maintaining rigidity in others

## Formulas Used

The calculator uses beam theory to determine:

1. Maximum force before yield:
   - For cantilever: F = (σy × I) / (y × L × SF)
   - For parallel: F = 2 × (σy × I) / (y × L × SF)

2. Maximum deflection at yield:
   - For cantilever: δ = (F × L³) / (3 × E × I)
   - For parallel: δ = (F × L³) / (12 × E × I)

Where:
- σy = Yield strength
- I = Area moment of inertia
- y = Distance from neutral axis to extreme fiber
- L = Length of flexure
- SF = Safety factor
- E = Young's modulus

## License

MIT
