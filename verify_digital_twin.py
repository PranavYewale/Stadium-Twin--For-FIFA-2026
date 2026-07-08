# Verification test script for Stadium Digital Twin AI Console
import sys
import os
import unittest
import json

# Add project root to sys.path to resolve imports
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import app
from database.models import db, Zone, User, Alert, Sustainability

class TestStadiumTwin(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_landing_page(self):
        """1. Verify Landing Page renders correctly"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Arena.Twin', response.data)
        print("[OK] Landing Page (/) checks out successfully.")

    def test_login_routes(self):
        """2. Verify login redirects and page access bounds"""
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 302) # Redirects to login since unauthenticated
        print("[OK] Authenticated /dashboard redirects to login for anonymous operators.")
        
        # Test valid login submit
        payload = {'username': 'admin', 'password': 'worldcup2026'}
        response = self.client.post('/login', data=payload)
        self.assertEqual(response.status_code, 302) # Redirects to dashboard after authentication
        print("[OK] Authorized Operator connection authenticated successfully.")

    def test_simulation_status_polling(self):
        """2.5. Verify status polling yields valid telemetry payload"""
        response = self.client.get('/api/simulation/status')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('zones', data)
        self.assertIn('attendance', data)
        self.assertIn('weather', data)
        print("[OK] Simulation Status polling endpoint returns valid state telemetry.")

    def test_dashboard_api_attendance(self):
        """3. Verify Attendance computes Stands-only zones correctly (Case-insensitive check)"""
        with self.app.app_context():
            response = self.client.get('/api/dashboard')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            
            # Verify capacity is 80,000 (total capacity of stands)
            self.assertEqual(data['capacity'], 80000)
            self.assertTrue(data['attendance'] >= 0)
            print(f"[OK] Dashboard API attendance calculations check out: {data['attendance']} / {data['capacity']} ({data['occupancy_percentage']}%).")

    def test_simulation_overrides(self):
        """4. Verify Simulation Override panel endpoints store settings successfully"""
        payload = {
            'weather_condition': 'Heatwave',
            'crowd_scale': 1.2,
            'temp_adjust': 3.0,
            'power_cut': True
        }
        response = self.client.post('/api/simulation/override', 
                                   data=json.dumps(payload),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['overrides']['weather_condition'], 'Heatwave')
        self.assertEqual(data['overrides']['temp_adjust'], 3.0)
        self.assertEqual(data['overrides']['power_cut'], True)
        print("[OK] Simulation Override POST triggers and returns state overrides correctly.")

    def test_assistant_lost_child(self):
        """5. Verify Missing Spectator Assistant camera feeds and dispatches"""
        payload = {
            'name': 'Jamie',
            'color': 'Blue',
            'last_seen': 'gate_a'
        }
        response = self.client.post('/api/assistant/lost-child',
                                   data=json.dumps(payload),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('spotted_zone', data)
        self.assertEqual(data['spotted_zone']['id'], 'stand_lower') # Connections: gate_a -> stand_lower
        self.assertIn('Lower Tier Stands', data['message'])
        print(f"[OK] Lost Child search locates subject: '{data['message']}' at {data['spotted_zone']['name']}.")

    def test_assistant_accessibility(self):
        """6. Verify Safe Accessibility Transit Router elevator forecasts"""
        payload = {
            'source': 'parking_east',
            'destination': 'stand_lower',
            'type': 'wheelchair'
        }
        response = self.client.post('/api/assistant/accessibility',
                                   data=json.dumps(payload),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('route', data)
        self.assertGreater(len(data['route']), 0)
        self.assertTrue(2 <= data['elevator_wait_min'] <= 6)
        print(f"[OK] Accessibility safe route compiled: {data['route'][0]} (Wait time: {data['elevator_wait_min']}m).")

    def test_assistant_queue_optimizer(self):
        """7. Verify Queue Optimizer shifts concession resources and balances times"""
        response = self.client.post('/api/assistant/queue-optimize')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertGreater(len(data['actions']), 0)
        print(f"[OK] AI Queue Optimizer balances concessions: '{data['actions'][0]}'.")

    def test_assistant_sentiment_analysis(self):
        """8. Verify Social Feed Fan Sentiment scales indices correctly"""
        response = self.client.get('/api/assistant/sentiment')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertGreater(data['happiness_score'], 0)
        self.assertGreater(len(data['trending_tags']), 0)
        print(f"[OK] Social Feedback Sentiment parses: score={data['happiness_score']}% positive tags={data['trending_tags'][0]['tag']}.")

if __name__ == '__main__':
    print("=" * 60)
    print("STARTING FULL UNIT AND INTEGRATION TESTING FOR ARENA.TWIN OS...")
    print("=" * 60)
    unittest.main()
