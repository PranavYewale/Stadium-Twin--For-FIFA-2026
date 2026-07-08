import random

def get_ticket_scan_metrics():
    """
    Simulates ticket scanner data showing scans per minute across active gates.
    """
    return {
        'gate_a_scans': random.randint(10, 45),
        'gate_b_scans': random.randint(15, 60),
        'gate_c_scans': random.randint(5, 30),
        'vip_scans': random.randint(2, 10)
    }
