import unittest
import main
import json

class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.f = open('Level_1_data\input.json', )
        self.data = json.load(self.f)
    def tearDown(self):
        self.f.close()
    def test_inExclusion(self):
        self.assertEqual(main.inExclusion(4,4), False)
    def test_detect_defect(self):
        self.assertTrue(main.detect_defect(self.data))

if __name__ == '__main__':
    unittest.main()
