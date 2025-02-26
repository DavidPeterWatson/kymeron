import math

# Constants (can be adjusted as needed)
FLOW_RATE_L_MIN = 0.3  # Flow rate in L/min
PRESSURE_BAR = 3.0     # Pressure in bars
TUBE_ID_MM = 4.0       # Tube inner diameter in mm
ROTOR_DIAMETER_MM = 20.0  # Rotor diameter in mm
NUM_ROLLERS = 3        # Number of rollers in the pump
EFFICIENCY = 0.6       # Pump efficiency (60%)
STARTING_FACTOR = 1.5  # Multiplier for starting torque
SAFETY_MARGIN = 1.2    # Safety margin multiplier

def hydraulic_power(flow_rate_l_min, pressure_bar):
    """Calculate hydraulic power (W) from flow rate and pressure."""
    # Convert flow rate from L/min to m^3/s
    flow_rate_m3_s = (flow_rate_l_min / 60) * 0.001
    # Convert pressure from bar to Pa
    pressure_pa = pressure_bar * 1e5
    # Hydraulic power = flow rate * pressure
    power_h = flow_rate_m3_s * pressure_pa
    return power_h

def mechanical_power(hydraulic_power_w, efficiency):
    """Calculate mechanical power (W) accounting for pump efficiency."""
    power_m = hydraulic_power_w / efficiency
    return power_m

def volume_per_revolution(tube_id_mm, rotor_diameter_mm, num_rollers):
    """Calculate volume displaced per revolution (m^3)."""
    # Convert dimensions to meters
    tube_id_m = tube_id_mm / 1000
    rotor_diameter_m = rotor_diameter_mm / 1000
    # Tube cross-sectional area (m^2)
    area = math.pi * (tube_id_m / 2)**2
    # Length of tube squeezed per roller (m)
    length_per_roller = (math.pi * rotor_diameter_m) / num_rollers
    # Volume per revolution = area * length per roller * number of rollers
    vol_per_rev = area * length_per_roller * num_rollers
    return vol_per_rev

def rotational_speed(flow_rate_l_min, vol_per_rev_m3):
    """Calculate rotational speed (RPM) from flow rate and volume per revolution."""
    # Convert flow rate to m^3/s
    flow_rate_m3_s = (flow_rate_l_min / 60) * 0.001
    # Rotations per second (rps)
    rps = flow_rate_m3_s / vol_per_rev_m3
    # Convert to RPM
    rpm = rps * 60
    return rpm

def torque_from_power(mechanical_power_w, rpm):
    """Calculate torque (mN·m) from mechanical power and rotational speed."""
    # Convert RPM to rad/s
    angular_velocity = (2 * math.pi * rpm) / 60
    # Torque in N·m
    torque_nm = mechanical_power_w / angular_velocity if angular_velocity != 0 else float('inf')
    # Convert to mN·m
    torque_mnm = torque_nm * 1000
    return torque_mnm

def adjust_torque(base_torque_mnm, starting_factor=1.5, safety_margin=1.2):
    """Adjust torque for starting conditions and safety margin."""
    starting_torque = base_torque_mnm * starting_factor
    final_torque = starting_torque * safety_margin
    return final_torque

def flow_rate_to_ml_s(flow_rate_l_min):
    """Convert flow rate from L/min to mL/s."""
    return (flow_rate_l_min * 1000) / 60

def m3_to_ml(volume_m3):
    """Convert volume from cubic meters to milliliters."""
    return volume_m3 * 1e6

def rpm_to_rps(rpm):
    """Convert rotational speed from RPM to RPS."""
    return rpm / 60

def main():
    """Main function to compute and display torque."""
    # Step 1: Calculate hydraulic power
    power_h = hydraulic_power(FLOW_RATE_L_MIN, PRESSURE_BAR)
    flow_ml_s = flow_rate_to_ml_s(FLOW_RATE_L_MIN)
    print(f"Flow Rate: {flow_ml_s:.2f} mL/s")
    print(f"Hydraulic Power: {power_h:.2f} W")

    # Step 2: Calculate mechanical power
    power_m = mechanical_power(power_h, EFFICIENCY)
    print(f"Mechanical Power: {power_m:.2f} W")

    # Step 3: Calculate volume per revolution
    vol_per_rev = volume_per_revolution(TUBE_ID_MM, ROTOR_DIAMETER_MM, NUM_ROLLERS)
    vol_per_rev_ml = m3_to_ml(vol_per_rev)
    print(f"Volume per Revolution: {vol_per_rev_ml:.2f} mL ({vol_per_rev:.8f} m³)")

    # Step 4: Calculate rotational speed
    rpm = rotational_speed(FLOW_RATE_L_MIN, vol_per_rev)
    rps = rpm_to_rps(rpm)
    print(f"Rotational Speed: {rpm:.2f} RPM ({rps:.2f} RPS)")

    # Step 5: Calculate base torque
    torque_base = torque_from_power(power_m, rpm)
    print(f"Base Torque: {torque_base:.2f} mN·m")
    
    

    # Step 6: Adjust torque for starting and safety
    torque_final = adjust_torque(torque_base, STARTING_FACTOR, SAFETY_MARGIN)
    print(f"Final Torque (with starting and safety margin): {torque_final:.2f} mN·m")

    # Step 7: Check against NEMA 17 capability
    nema17_torque_typical = 378  # Typical torque at ~100 RPM in mN·m
    print(f"NEMA 17 Typical Torque at ~100 RPM: {nema17_torque_typical} mN·m")
    if torque_final <= nema17_torque_typical:
        print("NEMA 17 is sufficient.")
    else:
        print("NEMA 17 may not be sufficient; consider a higher torque motor or adjust parameters.")

if __name__ == "__main__":
    main()