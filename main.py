import os
import sys
import logging
import traceback
from random import uniform

from src import DatesValidator
from src import ExcelFileHandler
from src import ReportGenerator
from src.config_variables import data_header_table, collabs_report_header, catalogue
import src.custom_functions as cf


def main():

    # Configure logging
    logging.basicConfig(
    filename='error_log.txt',  # Log file name
    filemode='w',  # Overwrite the log file
    level=logging.WARNING,  # Log only errors and above (WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date format in logs
    )

    try:

        # Determine if running as a PyInstaller bundle
        if getattr(sys, 'frozen', False):
            # If running in a bundle, get the location of the executable
            exe_base_path = os.path.dirname(os.path.abspath(sys.executable))
            logging.warning(f".exe location: {exe_base_path}")
        else:
            # If running in normal Python environment, get the script directory
            exe_base_path = os.path.dirname(os.path.abspath(__file__))

 
        ''' LOAD CONFIGURATION DATA '''

        # Configuration variables
        config_file_path = os.path.join(exe_base_path, 'Configuration.xlsx')

        # Initialize Configuration Workbook
        wb_config = ExcelFileHandler(config_file_path, 'Configuration.xlsx')

        wb_config.load_workbook()     # Load the configuration workbook
        sprints, team, period = wb_config.get_sheets_by_range(num_sheets=3)      # Retrieve the first 3 sheets (or any number you need)

        # Get table dimensions
        sprints_rows, sprints_cols = wb_config.find_table_dimensions(sprints, initial_row=0)
        team_rows, team_cols = wb_config.find_table_dimensions(team, initial_row=0)

        # Extract table data
        sprints_table = wb_config.extract_table_data(sprints, sprints_rows, sprints_cols, initial_row=2)
        team_table = wb_config.extract_table_data(team, team_rows, team_cols, initial_row=2)

        # Get specific cell values
        month_period = period['D5'].value
        year_period = period['D6'].value
        raw_file_name = period['C13'].value
        work_breakdown_structure = period['C18'].value
        last_item_number = period['C23'].value
        report_file_name = raw_file_name + ".xlsx"
        
        '''INSTANTIATE REPORT OBJECT'''
        report_wb = ReportGenerator()

        ''' LOAD RAW DATA '''
        raw_file_path = os.path.join(exe_base_path, report_file_name)
        wb_raw = ExcelFileHandler(raw_file_path, report_file_name)
        wb_raw.load_workbook()
    
        # Validate and process data
        data_table = [data_header_table]
        
        # Extracts the worksheet count from the workbook where the collaborators report
        sheet_count = wb_raw.sheet_count
    
        # Item counter
        item_count = last_item_number + 1

        # Find those team members that meet the wbs criteria
        sheets_criteria_wbs_fulfilled = []
        for sheet in range(sheet_count - 1):
            # Get the name of the actual sheet
            # The sheet_name will be the 'Created By' and 'Assigned To' value
            sheet_name = wb_raw.get_sheet_name(sheet)
            row_match_idx = wb_config.lookup_function(team_table,sheet_name,1)
            project_id = team_table[0][row_match_idx]
            
            if project_id == work_breakdown_structure:
                sheets_criteria_wbs_fulfilled.append(sheet_name)
        
        if len(sheets_criteria_wbs_fulfilled) == 0:
            report_wb.reason = 'WBS - Project ID'

        ''' ITERATE PER SHEET '''
        # We need to hide the last worksheet where the filling guide is located
        for sheet in range(len(sheets_criteria_wbs_fulfilled)):

            sheet_idx = wb_raw.get_sheet_index_by_name(sheets_criteria_wbs_fulfilled[sheet])
            raw = wb_raw.get_sheet_by_index(sheet_idx)

            # Find the wbs related to the sheet name, the 'Project ID' value
            sheet_name = wb_raw.get_sheet_name(sheet_idx)
            row_match_idx = wb_config.lookup_function(team_table,sheet_name,1)
            project_id = team_table[0][row_match_idx]
  
            # Get table dimensions
            raw_rows, raw_cols = wb_raw.find_table_dimensions(raw, initial_row=1)

            ''' EXTRACT RAW TABLE DATA '''
            raw_table = wb_raw.extract_table_data(raw, raw_rows, raw_cols, initial_row=3)
            # Save the value of the column length w/o header columns
            rows_data = len(raw_table[0])

            # Fixed values
            created_by = sheet_name
            peer_reviewer = team_table[2][row_match_idx]
            team_type = team_table[3][row_match_idx]
            module = team_table[4][row_match_idx]

            report_wb.creation_flag = cf.validate_team_member([peer_reviewer, team_type, module], created_by)

            ''' ITERATE PER ROW '''
            for row in range(rows_data):

                # Flag that indicates if the row is valid to add or not
                add = True

                # Validate if the activity has been completed so it can be reported
                if  'completed' in raw_table[3][row].lower():

                    short_description = raw_table[2][row]

                    # Create the new row that will be added to the custom report
                    new_row = [project_id,
                                created_by,
                                'unique id',
                                created_by,     # Assigned To
                                peer_reviewer,
                                short_description]

                    try:
                        item_type = raw_table[1][row]
                        if item_type is None:
                            raise ValueError("Item Type cannot be blank.")
                    except ValueError as item_type_not_found:
                        # Log the error and notify the user
                        logging.error(f"Invalid: {item_type_not_found} - Collaborator: {sheet_name}, row: {row+3}, column(s): {collabs_report_header[1]}")
                        report_wb.creation_flag = False

                    # Find the flag from Created-Updated-Executed columns
                    flag = cf.req_rows_add(raw_table, 4, 6, row)

                    try:
                        combo = cf.reqs_combo(item_type, flag)
                    except KeyError as e:
                        logging.error(f"Collaborator: {created_by} needs to fix > row: {row+3}, column(s): {collabs_report_header[4:7]} - Key not added: {e}")
                        add = False
                        report_wb.creation_flag = False

                    if add == True:    
                        # Create each row of the data table that will be saved into the Report file"
                        for coord in combo:

                            x, y = coord
                            
                            # 'Scheduled Start Date', 'Scheduled Finish Date' columns
                            # [14,15] > Analysis, [16,17] > Design, [18,19] > Execution
                            
                            if catalogue['Requirement Type'][x] == 'Test Execution & Reporting':
                                start, end = 18, 19
                            elif catalogue['Requirement Type'][x] == 'Test Analysis':
                                start, end = 14, 15
                            else: start, end = 16, 17

                            if raw_table[start][row] != None and raw_table[end][row] != None:

                                start_date, end_date = DatesValidator.format_date(raw_table[start][row], raw_table[end][row], created_by, row)   
                            else:
                                
                                logging.error(f"'NoneType' - Collaborator: {created_by}, row: {row+3}, column(s): {collabs_report_header[start:end+1]}")
                                raise ValueError("Required values cannot be 'None'.")


                            if start_date > end_date:
                                logging.error(f"Date has to be fixed - Collaborator: {created_by}, row: {row+3}")
                                valid_date = False
                                report_wb.creation_flag = False
                                raise ValueError("'Start Date' can't be greater than 'End Date'")
                            else: 
                                valid_date = True

                            month_name, year = DatesValidator.get_date_to_filter(start_date)
                            if month_name == month_period and year == year_period and valid_date == True:

                                # Request No Generator
                                req_id = cf.req_number_generator(project_id[7:], item_count)
                                
                                # Validate there are no negatives values
                                neg_values = cf.look_negatives_values(created_by, raw_table, row, 4, 13)
                                if neg_values == True:
                                    report_wb.creation_flag = False
                                    raise ValueError("Negative values need to be fixed.")
                                
                                # Sum all the required values for 'Number of Products (Generated or Modified)' column (Analysis & Design)
                                if catalogue['Requirement Subtype'][y] in ['Test Plan', 'Test Case']:
                                    created_n_updated_items =  cf.sum_values(raw_table, row, 4, 5) # Created & Updated Columns
                                elif catalogue['Requirement Subtype'][y] == 'Adhoc Testing':
                                    created_n_updated_items = 1
                                else: created_n_updated_items = 0

                                # Execution interval columns (Report Column)
                                if catalogue['Requirement Type'][x] == 'Test Execution & Reporting':
                                    
                                    total = cf.get_valid_value(raw_table, 6, row)   # Executed Column Value
                                    bugs_qty = cf.get_valid_value(raw_table, 10, row)
                                    pass_record = cf.get_valid_value(raw_table, 7, row)     # Get Pass qty
                                    fail = cf.get_valid_value(raw_table, 8, row)    # Get Fail qty
                                    cant_test = cf.get_valid_value(raw_table, 9, row)   # Get Untested qty
                                    bugs_closed = 0
                                    new_bugs = bugs_qty

                                    if item_type == 'Bug' or item_type == 'Adhoc':

                                        total = 0
                                        pass_record = 0
                                        fail = 0
                                        cant_test = 0
                                        if item_type == 'Bug':
                                            bugs_closed = 1
                                            new_bugs = 0
                                        
                                    

                                    execution_bugs += [
                                        total,          # Total
                                        pass_record,    # Pass
                                        fail,           # Fail
                                        cant_test,      # Cant Test
                                        bugs_closed,    # Quantity of Bugs Closed: Defect Verification
                                        0,              # Quantity of Bugs Re-opened
                                        0,              # Quantity of Bugs Verified
                                        new_bugs        # Quantity of New Bugs Found: Test Case Execution
                                        ]   
                                else:
                                    execution_bugs = [0,0,0,0,0,0,0,0]
                                
                                # Release/Build
                                if 'regression' in short_description.lower():
                                    delivery_type = catalogue['Release/Build'][0]
                                else: delivery_type = catalogue['Release/Build'][1]
                                
                                # Complete %
                                if catalogue['Requirement Type'][x] == 'Test Execution & Reporting' and item_type != 'Bug':
                                    try:
                                        suma_values = pass_record + fail + cant_test
                                        check = round(suma_values / total, 1)
                                        
                                        if check != 1.0:
                                            completion = check * 100
                                            raise ValueError("Total 'Test Cases Executed' cannot be lower than the sum of Pass, Fail & Untested")
                                        else: completion = 100

                                    except (ValueError, ZeroDivisionError) as total_sum_not_right:
                                        # Log the error and notify the user
                                        logging.error(f"{total_sum_not_right} - Collaborator: {created_by}, row: {row+3}, column(s): {collabs_report_header[7:10]}")
                                        report_wb.creation_flag = False

                                else: completion = 0
                                
                                # Calculate number of weekdays (excluding weekends, holidays)
                                # Assuming your dates are in datetime or timestamp format
                                weekdays = DatesValidator.get_business_days(start_date, end_date)
                                
                                # Scheduled Duration column
                                if start_date == end_date:
                                    scheduled_duration = 1
                                else:
                                    scheduled_duration = weekdays
                                
                                time_constraint = scheduled_duration * 8 # Each labor day is for 8 hours

                                # Actual Effort calculation
                                #   'Action': ['Create', 'Update', 'Review', 'NA'], 
                                if x == 3:
                                    # 'Test Execution & Reporting'
                                    actual_effort_col = 13
                                    action = catalogue['Action'][3]   # NA
                                elif x == 1:
                                    # 'Test Analysis'
                                    actual_effort_col = 11
                                    action = catalogue['Action'][2]   # Review
                                else:
                                    # 'Test Design'
                                    actual_effort_col = 12
                                    if flag == 'NVN':
                                        action = catalogue['Action'][1]   # Update
                                    else: action = catalogue['Action'][0]   # Create

                                actual_effort = raw_table[actual_effort_col][row]
                                
                                try:
                                    if actual_effort is None or actual_effort == 0:
                                        report_wb.creation_flag = False
                                        raise ValueError("'Actual Effort' cannot be 0 or None.")
                                    elif actual_effort > time_constraint:
                                        report_wb.creation_flag = False
                                        raise ValueError("'Actual Effort' cannot be greater than specified time period (within dates)")
                                    elif actual_effort < 0:
                                        report_wb.creation_flag = False
                                        raise ValueError("'Actual Effort' a negative number")
                                    
                                    # Scheduled Effort column
                                    scheduled_effort = actual_effort
                                    # new_row.append(actual_effort)
                                except ValueError as effort_value_not_found:
                                    # Log the error and notify the user
                                    logging.error(f"Invalid: {effort_value_not_found} - Collaborator: {sheet_name}, row: {row+3}, column(s): {collabs_report_header[actual_effort_col]}")
                                    report_wb.creation_flag = False


                                # 'Peer Review Scheduled Effort (hrs)', 'Scheduled Rework Effort (hrs)'
                                if catalogue['Requirement Subtype'][y] in ['Test Plan', 'Test Case']:

                                    try:
                                        design_effort = raw_table[12][row]
                                        if design_effort != None:
                                            multiply = uniform(0.05, 0.15)
                                            peer_first_check = round(design_effort*multiply,2)
                                            peer_last_check = round(peer_first_check/2,2)
                                        else:
                                            raise TypeError("'Design Effort' cannot be blank")
                                    except TypeError as missing_value:
                                        logging.error(f"Invalid: {missing_value} - Collaborator: {sheet_name}, row: {row+3}, column(s): {collabs_report_header[12]}")
                                        report_wb.creation_flag = False

                                else: 
                                    peer_first_check = 0
                                    peer_last_check = 0

                                # Replace with the Request No value
                                new_row[2] = req_id

                                new_row += [
                                    catalogue['Requirement Type'][x],
                                    catalogue['Requirement Subtype'][y],
                                    module,     # Module / Feature
                                    team_type,  # Team
                                    created_n_updated_items
                                ]

                                new_row.extend(execution_bugs)

                                new_row += [
                                    delivery_type,
                                    completion,
                                    start_date,
                                    end_date,
                                    scheduled_duration,
                                    scheduled_effort,
                                    peer_first_check,
                                    peer_last_check,
                                    start_date,
                                    end_date,
                                    scheduled_duration,
                                    actual_effort,
                                    peer_first_check,
                                    catalogue['ForClosing'],
                                    action
                                ]
                            
                                
                                item_count += 1
                                data_table.append(new_row)
                                new_row = new_row[:6]
                                execution_bugs.clear()
                            else:
                                report_wb.reason = 'Reporting period'
                else: 
                    report_wb.reason = 'Without any completed items' 
            
        
        data_table_length = (len(data_table))

        # Generate the report
        report_wb.generate_report(data_table, config = {'data_table_length': data_table_length})  # Add more configurations if needed

    except Exception as e:  # Generic catch-all for any other exceptions
        # Log the error with a traceback
        # logging.error("\nERROR: %s", str(e))
        report_wb.creation_flag = False
        logging.error(traceback.format_exc())
        print("\nAn unexpected error occurred.")
        print(f"Error details: {e}")

    finally:
        if report_wb.creation_flag == True:
            print(f"\nNew Report saved as: {report_wb.report_filename}")
            logging.warning(f"New Report saved as: {report_wb.report_filename}")
        else:
            logging.warning(f"Report file wasn't created.")
            print(f"\nReport file wasn't created, please review the 'error_log.txt' file for more details.")

if __name__ == "__main__":
    main()