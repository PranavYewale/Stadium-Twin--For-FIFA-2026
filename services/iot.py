import random

def get_iot_telemetry(total_attendance, weather_info=None):
    """
    Computes real-time energy load, water flow, and climate control status
    based on current crowd size and ambient weather factors.
    """
    attendance_ratio = total_attendance / 80000.0
    
    # Power consumption spikes with more people (lighting, HVAC, screens)
    base_power = 800.0 # kW
    max_power_add = 1200.0
    energy_kwh = base_power + (max_power_add * attendance_ratio)
    
    # Temperature strain adjust (e.g. Heatwave or extreme temperatures spikes cooling load)
    if weather_info:
        cond = weather_info.get('condition', '')
        temp = weather_info.get('temp', 22.0)
        if cond == 'Heatwave' or temp > 35.0:
            energy_kwh += 650.0  # massive HVAC cooling strain
        elif cond == 'Heavy Rain':
            energy_kwh += 200.0  # drainage pumps active
            
    energy_kwh += random.uniform(-30, 30)
    
    # Water usage spikes with attendance, heatwaves (hydration), and heavy rain (drainage flow)
    base_water = 5.0 # liters/sec
    max_water_add = 25.0
    water_flow = base_water + (max_water_add * attendance_ratio)
    
    if weather_info:
        cond = weather_info.get('condition', '')
        temp = weather_info.get('temp', 22.0)
        if cond == 'Heatwave' or temp > 35.0:
            water_flow += 12.0  # high hydration and washroom demand
        elif cond == 'Heavy Rain':
            water_flow += 18.0  # stadium storm drain collection flow
            
    water_flow += random.uniform(-1, 1.5)
    
    # Carbon emissions = energy * factor
    carbon_footprint = energy_kwh * 0.42 # kg CO2 per kWh
    
    # HVAC load percentage reacts to crowd and climate
    hvac_load = 20.0 + (60.0 * attendance_ratio)
    if weather_info:
        temp = weather_info.get('temp', 22.0)
        if temp > 35.0:
            hvac_load += 25.0
        elif temp < 15.0:
            hvac_load += 15.0
            
    return {
        'energy_kwh': round(energy_kwh, 2),
        'water_liters_sec': round(water_flow, 2),
        'carbon_footprint_kg': round(carbon_footprint, 2),
        'hvac_load_pct': min(100.0, max(0.0, round(hvac_load, 1)))
    }
