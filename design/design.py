from flexure_calculator import calculate_plate_buckling, calculate_deflection_due_to_force, calculate_force_for_deflection_with_end_condition, calculate_length_decrease_due_to_deflection, MATERIALS

bed_flexure_length = 160
bed_flexure_width = 100
bed_flexure_thickness = 1.0
safety_factor = 1.5
end_condition = 4.0
material = MATERIALS['spring_steel']

bed_flexure_critical_vertical_load = calculate_plate_buckling(
            bed_flexure_length, bed_flexure_width, bed_flexure_thickness, material, end_condition,  # k depends on boundary conditions
            safety_factor=safety_factor
        )

print(f'Bed flexure critical vertical load: {bed_flexure_critical_vertical_load} N')


bed_flexure_parallel_horizontal_force = 1000

# Swap width and length because force is parralel to width
bed_flexure_parallel_deflection = calculate_deflection_due_to_force(
    bed_flexure_length, bed_flexure_thickness, bed_flexure_width, material, bed_flexure_parallel_horizontal_force
)

print(f'Bed flexure parallel deflection at {bed_flexure_parallel_horizontal_force} N: {bed_flexure_parallel_deflection} mm')

bed_flexure_perpendicular_deflection = 3

bed_flexure_perpendicular_force = calculate_force_for_deflection_with_end_condition(
    bed_flexure_length, bed_flexure_width, bed_flexure_thickness, material, bed_flexure_perpendicular_deflection, 'fixed_guided'
)

print(f'Bed flexure perpendicular force at {bed_flexure_perpendicular_deflection} mm deflection: {bed_flexure_perpendicular_force} N')


bed_height_drop_from_perpendicular_deflection = calculate_length_decrease_due_to_deflection(bed_flexure_length, bed_flexure_perpendicular_deflection, 'fixed_guided')

print(f'Bed height drop from {bed_flexure_perpendicular_deflection} mm perpendicular deflection: {bed_height_drop_from_perpendicular_deflection} mm')