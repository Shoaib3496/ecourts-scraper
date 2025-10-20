import unittest
from scraper.ecourts_scraper import ECourtsScraper

class TestECourtsScraper(unittest.TestCase):
    def test_sample_states(self):
        s = ECourtsScraper()
        states = s.get_states()
        self.assertIsInstance(states, list)
        self.assertGreater(len(states), 0)

if __name__ == '__main__':
    unittest.main()
