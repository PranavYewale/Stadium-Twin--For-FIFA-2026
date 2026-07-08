# Route optimization algorithms for crowd management

STADIUM_ADJACENCY = {
    'gate_a': ['gate_b', 'gate_c', 'metro_station'],
    'gate_b': ['gate_a', 'gate_c', 'parking_east'],
    'gate_c': ['gate_a', 'gate_b', 'parking_west'],
    'vip_entrance': ['parking_vip', 'stand_101'],
    'metro_station': ['gate_a', 'gate_b'],
    'parking_east': ['gate_b'],
    'parking_west': ['gate_c'],
}

def get_redirection_strategy(overloaded_zone_id, zones_dict):
    """
    Given an overloaded zone (e.g. gate_a), suggests alternative zones and diversion percentages.
    """
    overloaded = zones_dict.get(overloaded_zone_id)
    if not overloaded:
        return None
        
    alternatives = []
    zone_type = overloaded.get('zone_type')
    
    # Find adjacent or similar zones that are not overloaded
    for zid, zval in zones_dict.items():
        if zid == overloaded_zone_id:
            continue
        if zval.get('zone_type') == zone_type:
            # Similar zone (e.g. gate B or C for gate A)
            congestion_ratio = zval.get('current_crowd', 0) / max(1, zval.get('capacity', 1))
            if congestion_ratio < 0.7:
                alternatives.append((zid, zval, congestion_ratio))
                
    if not alternatives:
        return {
            'action': 'Broadcast warning',
            'details': f'All {zone_type}s are near capacity. Recommend pausing entry/exit.',
            'redirects': []
        }
        
    # Sort alternatives by congestion ratio (lowest congestion first)
    alternatives.sort(key=lambda x: x[2])
    
    # Calculate diversion distribution (prefer least busy gates)
    redirects = []
    total_space = sum(max(0, x[1]['capacity'] - x[1]['current_crowd']) for x in alternatives)
    
    if total_space > 0:
        for zid, zval, ratio in alternatives[:2]:  # top 2 alternatives
            space = max(0, zval['capacity'] - zval['current_crowd'])
            pct = int((space / total_space) * 100)
            redirects.append({
                'to_zone': zid,
                'name': zval['name'],
                'percentage': pct,
                'queue_wait_est': f"{zval.get('queue_length', 0) // 2} mins"
            })
    else:
        # Equal split
        for zid, zval, ratio in alternatives[:2]:
            redirects.append({
                'to_zone': zid,
                'name': zval['name'],
                'percentage': 50,
                'queue_wait_est': f"{zval.get('queue_length', 0) // 2} mins"
            })
            
    return {
        'action': 'Redirect Crowd',
        'from_zone': overloaded_zone_id,
        'from_name': overloaded['name'],
        'redirects': redirects
    }
