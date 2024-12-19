import numpy as np
import logging
from datetime import datetime

from .config_variables import date_formats


class DatesValidator:
    
    @staticmethod
    def parse_and_format_date(date_str):
        """For each format, it tries to parse the date string (date_str) into a datetime object.
        Once a valid date format is found, it converts the datetime object (parsed_date) back into a 
        formatted string using the strftime() method, specifically formatting it as 'mm/dd/YYYY'.
        
        :param date_str: The date string that will be formatted.
        :returns formatted_date: The date string formatted.
        """
    
        for fmt in date_formats:
            try:
                # Attempt to parse the date string with the current format
                parsed_date = datetime.strptime(date_str, fmt)
                formatted_date = parsed_date.strftime('%m/%d/%Y')   # 'mm/dd/YYYY'
                return formatted_date
            except ValueError:
                # If parsing fails, try the next format defined in the date_formats list
                continue
        
        # Return an error message if no formats match
        return "Invalid date format"


    @staticmethod
    def format_date(start_date, end_date, team_member, row):
        """It will apply the necessary format to the provided start and end dates.
        
        :param start_date: The start date string that will be formatted.
        :param end_date: The end date string that will be formatted.
        :param team_member: The team member owner of the dates reported, for logging purposes.
        :param row: The row where the dates will be found, for logging purposes.
        """

        if isinstance(start_date, datetime) and isinstance(end_date, datetime):
            fmt_start_date = start_date.strftime('%m/%d/%Y')
            fmt_end_date = end_date.strftime('%m/%d/%Y')
            logging.warning(f"Date format has been fixed - Collaborator: {team_member}, row: {row+3}")
        else:
            fmt_start_date = DatesValidator.parse_and_format_date(start_date)
            fmt_end_date = DatesValidator.parse_and_format_date(end_date)
        
        return fmt_start_date, fmt_end_date



    @staticmethod
    def convert_to_np_datetime64(date):
        """Ensures that the dates are converted to datetime64[D] (days) format.

        :param date: The date that will be converted.
        """
        
        try:
            if isinstance(date, datetime):
                return np.datetime64(date, 'D')   
            else:     
                # Parse the date string into a datetime object
                parsed_date = datetime.strptime(date, '%m/%d/%Y')
                # Format the datetime object into ISO 8601 format
                iso_date_str = parsed_date.strftime('%Y-%m-%d')
                # Convert the ISO formatted date string to np.datetime64
                return np.datetime64(iso_date_str, 'D')
                
        except ValueError as e:
            logging.error(f"Error parsing date: {date} - {e}")
            return e
        
    
    @staticmethod
    def get_business_days(start_date, end_date):
        """Get the business days betweeen two date (excluding holidays, Saturdays and Sundays).
        
        :param start_date: The start date period.
        :param end_date: The end date period.
        """
        np_start_date = DatesValidator.convert_to_np_datetime64(start_date)
        np_end_date = DatesValidator.convert_to_np_datetime64(end_date)
        return np.busday_count(np_start_date, np_end_date)


    @staticmethod
    def get_date_to_filter(date):
        """Returns the month and the year from the provided date.
        
        :param date: Date that will be processed.
        """
        # Convert the string back to a datetime object
        parsed_date = datetime.strptime(date, '%m/%d/%Y')

        # Extract the month number
        month = parsed_date.month

        # Get the full month name
        # month = parsed_date.strftime('%B')

        # Get the year
        year = parsed_date.year
        return month, year
    
    @staticmethod
    def date_within_period_inclusive(initial_date, final_date, input_date):
        """Check if the date lies within the range (inclusive).

        :param initial_date: The start date of the filter period.
        :param final_date: The end date of the filter period.
        :param input_date: The date that will be checked (inclusive).
        """

        # Convert all dates to datetime objects
        # All dates values are strings in 'MM/DD/YYYY' format
        check_date = datetime.strptime(input_date, "%m/%d/%Y")
        start_date = datetime.strptime(initial_date, "%m/%d/%Y")
        end_date = datetime.strptime(final_date, "%m/%d/%Y")

        # Check if the date lies within the range (inclusive)
        if start_date <= check_date <= end_date:
            return True
        else:
            return False