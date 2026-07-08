import random

def get_iot_telemetry(total_attendance):
    """
    Computes real-time energy load, water flow, and climate control status
    based on current crowd size.
    """
    attendance_ratio = total_attendance / 80000.0
    
    # Power consumption spikes with more people (lighting, HVAC, screens)
    base_power = 800.0 # kW
    max_power_add = 1200.0
    energy_kwh = base_power + (max_power_add * attendance_ratio) + random.uniform(-50, 50)
    
    # Water usage spikes during breaks / high attendance
    base_water = 5.0 # liters/sec
    max_water_add = 25.0
    water_flow = base_water + (max_water_add * attendance_ratio) + random.uniform(-1, 2)
    
    # Carbon emissions = energy * factor
    carbon_footprint = energy_kwh * 0.42 # kg CO2 per kWh
    
    return {
        'energy_kwh': round(energy_kwh, 2),
        'water_liters_sec': round(water_flow, 2),
        'carbon_footprint_kg': round(carbon_footprint, 2),
        'hvac_load_pct': min(100.0, round(20.0 + (80.0 * attendance_ratio), 1))
    }
