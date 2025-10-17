import unittest
from scraper.ecourts_scraper import ECourtsScraper

class TestECourtsScraper(unittest.TestCase):
    def setUp(self):
        self.scraper = ECourtsScraper()
        
    def test_get_states(self):
        states = self.scraper.get_states()
        self.assertIsInstance(states, list)
        self.assertGreater(len(states), 0)
        
    def test_state_district_flow(self):
        states = self.scraper.get_states()
        if states:
            districts = self.scraper.get_districts(states[0]['value'])
            self.assertIsInstance(districts, list)
            
    def tearDown(self):
        self.scraper.cleanup()

if __name__ == '__main__':
    unittest.main()
