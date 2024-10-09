import unittest
from unittest.mock import patch, MagicMock
from src.report_generator import ReportGenerator


class TestDatesValidator(unittest.TestCase):

    def setUp(self):
        """Set up the test fixture before each test."""
        self.report_generator = ReportGenerator()

    @patch('src.report_generator.datetime')
    def test_1_generate_filename(self, mock_datetime):
        # Mock the datetime to return a fixed timestamp
        mock_datetime.now.return_value.strftime.return_value = '2024-10-07_12-00'
        
        filename = self.report_generator.generate_filename()
        
        # Check if the filename is generated as expected
        self.assertEqual(filename, 'Report_2024-10-07_12-00.xlsx')

    def test_2_create_table_n_apply_table_style(self):
        # Test if the correct table style is applied
        table_range = "A1:B3"
        table = self.report_generator.create_table_n_apply_table_style(table_range)
        
        # Check if the returned table has the correct properties
        self.assertEqual(table.displayName, "ReportTable")
        self.assertEqual(table.ref, table_range)
        self.assertEqual(table.tableStyleInfo.name, "TableStyleMedium2")
        self.assertTrue(table.tableStyleInfo.showRowStripes)


if __name__ == "__main__":
    unittest.main(verbosity=2)