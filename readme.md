# Flexure Force Calculator

A Python tool for calculating the maximum force a spring steel flexure can withstand before permanent deformation occurs. This is particularly useful for designing and analyzing flexures used in cartesian maker machines, automated tool changers, and other precision mechanical systems.

## Overview

Flexures are compliant mechanisms that provide motion through elastic deformation rather than traditional joints. They are commonly used in precision machines to:

- Allow motion in specific directions while providing rigidity in others
- Prevent binding due to small deviations in distances
- Eliminate backlash and friction issues associated with traditional joints

This calculator helps determine the maximum force a flexure can withstand before permanent deformation, which is critical for proper design and operation.

## Features

- Calculate maximum force and deflection for both out-of-plane and in-plane loading:
  - Out-of-plane bending (traditional flexure behavior)
  - In-plane tension/compression (force colinear with width and length)
  - Buckling analysis for thin plates under compression
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
2. Choose the loading type (out-of-plane bending, in-plane tension, or buckling)
3. Enter dimensions (length, width, thickness)
4. Set a safety factor
5. Optionally generate plots

## Loading Types

### Out-of-Plane Bending
Traditional flexure behavior where the force is applied perpendicular to the plate surface.
- **Cantilever**: A beam fixed at one end and free at the other
- **Parallel**: Two beams connected in parallel

### In-Plane Loading
Force is applied colinear with the width and length of the plate.
- **Tension**: Stretching the flexure along its length
- **Compression/Buckling**: Compressing the flexure along its length, which can lead to buckling failure

## Buckling Analysis

The calculator includes two approaches to buckling analysis:
1. **Euler Column Buckling**: Treats the flexure as a slender column
2. **Plate Buckling**: Uses plate buckling theory for thin rectangular plates

The calculator automatically determines the critical buckling load as the minimum of these two approaches.

## Example Application

In a cartesian maker machine with an automated tool changer, spring steel flexures might be used on the bed that moves up and down on the Z-axis. These flexures:

- Are attached at each corner to a linear rail
- Use simple sheets of spring steel as flexures
- Are oriented perpendicular to the diagonals to hold the bed in place
- Experience forces that are colinear with the width and length of the plate
- Must resist both tension and compression (buckling) forces

## Formulas Used

### Out-of-Plane Bending
1. Maximum force before yield:
   - For cantilever: F = (σy × I) / (y × L × SF)
   - For parallel: F = 2 × (σy × I) / (y × L × SF)

2. Maximum deflection at yield:
   - For cantilever: δ = (F × L³) / (3 × E × I)
   - For parallel: δ = (F × L³) / (12 × E × I)

### In-Plane Tension
1. Maximum force before yield:
   - F = (σy × A) / SF

2. Maximum elongation at yield:
   - δ = (σy × L) / (E × SF)

### Buckling
1. Euler column buckling:
   - Pcr = (k × π² × E × I) / L²

2. Plate buckling:
   - σcr = [k × π² × E / (12 × (1-ν²))] × (t/b)²
   - Pcr = σcr × A

Where:
- σy = Yield strength
- I = Area moment of inertia
- y = Distance from neutral axis to extreme fiber
- L = Length of flexure
- SF = Safety factor
- E = Young's modulus
- A = Cross-sectional area
- k = End condition factor or buckling coefficient
- ν = Poisson's ratio
- t = Thickness
- b = Width

## License

MIT
