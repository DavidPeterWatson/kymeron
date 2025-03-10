# Cyclone Dust Collector: Design Principles and Calculations

## Introduction

A cyclone dust collector is a mechanical device that uses centrifugal force to separate particulate matter from an air stream. They are widely used in woodworking, metalworking, and other industrial applications where dust collection is necessary. This document explains the key components of a cyclone separator and the calculations used to design an efficient system.

## How Cyclone Separators Work

Cyclone separators operate on a simple principle: when air containing dust particles enters the cyclone tangentially at high velocity, it creates a vortex. The centrifugal force pushes the heavier particles outward against the walls of the cyclone, where they lose momentum and spiral downward into a collection bin. The cleaner air forms an inner vortex that moves upward and exits through the vortex finder at the top.

## Key Components of a Cyclone Separator

![Cyclone Separator Diagram](https://i.imgur.com/example.jpg)

### 1. Inlet

The inlet is where dust-laden air enters the cyclone. It's typically rectangular and positioned tangentially to the cyclone body to create the initial circular motion.

**Key dimensions:**
- **Inlet Height**: Typically 1/2 of the inlet width
- **Inlet Width**: Calculated based on the desired airflow and inlet velocity

### 2. Cylinder (Main Body)

The cylindrical section is where the primary vortex forms. The dust-laden air spirals around the inner wall of this section.

**Key dimensions:**
- **Body Diameter**: Typically 3-4 times the inlet width
- **Cylinder Height**: Typically 1.5-2 times the body diameter

### 3. Cone

The conical section below the cylinder helps maintain the vortex while directing separated particles downward to the dust outlet.

**Key dimensions:**
- **Cone Height**: Typically 2-3 times the body diameter
- **Cone Angle**: Usually between 10-30 degrees

### 4. Vortex Finder (Clean Air Outlet)

The vortex finder is a tube that extends from the top of the cyclone into the cylinder. It provides a path for the clean air to exit without re-entraining the separated dust.

**Key dimensions:**
- **Vortex Finder Diameter**: Typically 0.4-0.6 times the body diameter
- **Vortex Finder Length**: Typically 0.5-0.8 times the body diameter

### 5. Dust Outlet

The dust outlet is at the bottom of the cone where separated particles exit into a collection bin.

**Key dimensions:**
- **Dust Outlet Diameter**: Typically 0.2-0.4 times the body diameter

## Design Calculations

### Inlet Dimensions

The inlet dimensions are calculated based on the desired airflow rate and inlet velocity:

```
Inlet Area = Airflow / Inlet Velocity
```

For a rectangular inlet with a 1:2 height-to-width ratio:

```
Inlet Width = √(2 × Inlet Area)
Inlet Height = Inlet Area / Inlet Width
```

### Body Diameter

The body diameter is typically proportional to the inlet width:

```
Body Diameter = 3.5 × Inlet Width
```

### Cylinder and Cone Heights

The cylinder and cone heights are proportional to the body diameter:

```
Cylinder Height = 1.75 × Body Diameter
Cone Height = 2.5 × Body Diameter
```

### Vortex Finder Dimensions

The vortex finder dimensions are also proportional to the body diameter:

```
Vortex Finder Diameter = 0.5 × Body Diameter
Vortex Finder Length = 0.6 × Body Diameter
```

### Dust Outlet Diameter

```
Dust Outlet Diameter = 0.25 × Body Diameter
```

## Performance Metrics

### Pressure Drop

The pressure drop across a cyclone is an important consideration as it affects the power requirements of the system. It can be calculated using:

```
Pressure Drop = Gas Density × (Inlet Velocity²/2) × Velocity Heads
```

Where "Velocity Heads" is an empirical value typically between 4-8.

### Cut Size (d50)

The cut size (d50) is the particle size that has a 50% chance of being collected. It's a key performance metric for cyclone separators:

```
d50 = √(9 × Gas Viscosity × Body Diameter / (2 × π × N × Inlet Velocity × (Particle Density - Gas Density)))
```

Where:
- N = Number of effective turns in the cyclone (typically 5-10)

### Collection Efficiency

The collection efficiency for a given particle size can be estimated using the Lapple model:

```
Efficiency = 1 / (1 + (d50/Particle Size)²)
```

This equation shows that efficiency increases with particle size and decreases with cut size.

## Designing Cyclones in Series

For applications requiring the separation of particles of various sizes, multiple cyclones can be arranged in series. Each cyclone in the series can be optimized for a different particle size range:

1. The first cyclone typically has a larger body diameter and is designed to capture larger particles.
2. Subsequent cyclones have progressively smaller body diameters to capture finer particles.
3. The airflow decreases slightly through the series due to pressure losses.

## Practical Considerations for CNC Applications

For CNC machine dust collection:

1. **Airflow Requirements**: Typically 350-800 CFM (0.17-0.38 m³/s) depending on the machine size and type of material being cut.

2. **Particle Sizes**: 
   - Large chips: >100 μm
   - Medium dust: 10-100 μm
   - Fine dust: <10 μm (most harmful to respiratory health)

3. **Material Density**: 
   - Wood dust: ~700 kg/m³
   - Metal chips: ~2700-7800 kg/m³ (depending on the metal)

4. **System Integration**:
   - Ensure adequate ducting size (typically 4-6 inches for hobby/small CNC machines)
   - Consider using a pre-separator for larger chips before the cyclone
   - Add a fine filter after the cyclone for capturing the smallest particles

## Optimization Tips

1. **Increasing Efficiency**:
   - Increase the length of the cylinder and cone
   - Decrease the vortex finder diameter
   - Increase the inlet velocity (but be aware this increases pressure drop)

2. **Reducing Pressure Drop**:
   - Increase the body diameter
   - Increase the vortex finder diameter
   - Decrease the inlet velocity

3. **Balancing Efficiency and Pressure Drop**:
   - There's always a trade-off between collection efficiency and pressure drop
   - Design for the minimum efficiency required to capture the target particle size
   - Consider the available fan/blower power when calculating pressure drop

## References

1. Cooper, C.D. and Alley, F.C. (2011). Air Pollution Control: A Design Approach. Waveland Press.
2. Lapple, C.E. (1951). Processes use many collector types. Chemical Engineering, 58(5), 144-151.
3. Hoffmann, A.C. and Stein, L.E. (2008). Gas Cyclones and Swirl Tubes: Principles, Design, and Operation. Springer.

## Using the Cyclone Calculator Script

The accompanying Python script (`cyclone_calculator.py`) automates these calculations and provides visual representations of the cyclone design. It allows you to:

1. Input your specific parameters (airflow, inlet velocity, particle sizes)
2. Calculate all dimensions based on established engineering principles
3. Visualize the cyclone design with proper proportions
4. Estimate performance metrics like pressure drop and collection efficiency
5. Design multiple cyclones in series for capturing different particle size ranges

Run the script with:
```
python cyclone_calculator.py
```

Follow the prompts to enter your specific parameters or use the defaults for a typical CNC dust collection system. 