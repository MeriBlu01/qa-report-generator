import unittest
from datetime import datetime
from src.dates_validation import DatesValidator


class TestDatesValidator(unittest.TestCase):

    def setUp(self):
        """Set up the test fixture before each test."""
        self.class_under_test = DatesValidator()

    def test_1_parse_and_format_date(self):
        raw_date = "4/14/2024"
        expected_date = "04/14/2024"
        self.assertEqual(self.class_under_test.parse_and_format_date(raw_date), expected_date)

    def test_2_parse_and_format_date(self):
        raw_date = "may/11/2024"
        expected_result = "Invalid date format"
        self.assertEqual(self.class_under_test.parse_and_format_date(raw_date), expected_result)




    
    '''
    def test_format_date_invalid(self):
        raw_date = "invalid-date"
        self.assertIsNone(DatesValidator.format_date(raw_date), "Should return None for invalid date format")

    def test_validate_date_range_valid(self):
        start_date = datetime(2023, 1, 1)
        end_date = datetime(2023, 12, 31)
        self.assertTrue(DatesValidator.validate_date_range(start_date, end_date, "Sheet1", 2))

    def test_validate_date_range_invalid(self):
        start_date = datetime(2023, 12, 31)
        end_date = datetime(2023, 1, 1)
        with self.assertRaises(ValueError):
            DatesValidator.validate_date_range(start_date, end_date, "Sheet1", 2)
    '''

if __name__ == "__main__":
    unittest.main(verbosity=2)