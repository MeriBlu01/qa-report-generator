import logging

from .config_variables import combo_map, collabs_report_header 


# Find here custom functions that works as helpers

def req_rows_add(table, start_idx, end_idx, row):
    '''Find the flag from Created-Updated-Executed columns.
    
    :param table: The table where the data is located.
    :param start_idx: The column index to start reading.
    :param end_idx: The final column to read.
    :param row: The row index to read.
    :return flag: The flag that'll indicate whether there is an existing value ('V') or not ('N').
    '''
    flag = ''
    for column in range(start_idx, end_idx+1):
        if table[column][row] is not None:
            flag += 'V' # Value
        else: flag += 'N' # None
    return flag


def reqs_combo(item_type, flag):
    """Find requirement type and requirement sub type classification.

    :param item_type: The issue type of the activity reported (agile issue types).
    :param flag: The flag that'll indicate whether there is an existing value ('V') or not ('N').
    :return: A list of lists that will configure how the rows will be created.
    """
    return combo_map[item_type][flag]


def sum_values(table, row, start_col, end_col):
    """Sum the values between the indicated columns interval.

    :param table: The table where the data is located.
    :param row: The row index to read.
    :param start_col: The column to start the sum.
    :param end_col: The final column to sum.
    :return sum: The result of the sum.
    """
    sum = 0
    for column in range(start_col, end_col+1):
        if table[column][row] is not None:
            sum += table[column][row] # Value
    return sum


def look_negatives_values(team_member, table, row, start_col, end_col):
    """Check if there's a negative value and returns a boolean value.

    :param team_member: The team member owner of the reported table for logging purposes.
    :param table: The table where the data is located.
    :param row: The row index to read.
    :param start_col: The column to start search.
    :param end_col: The final column to search.
    :return negatives: A boolean value that represents the presence of negative value (True) or not (False)
    """
    negatives = False
    for column in range(start_col, end_col+1):
        if table[column][row] is not None:
            if table[column][row] < 0:
                logging.error(f"Invalid: Values cannot be negative - Collaborator: {team_member}, row: {row+3}, column(s): {collabs_report_header[column]}")
                negatives = True
    return negatives


def validate_team_member(values, team_member_name):
    """Validate that the required team member details are completely defined.

    :param values: A list of values to check for None. 
    :param team_member_name: The name of the team member for logging purposes.
    :returns team_member_status_config: A boolean indicating whether the team member is completely defined.
    """
    # Check if any value is None
    if any(v is None for v in values):
        print(f"\nCollaborator {team_member_name} is not completely defined, please check 'Configuration.xlsx' file, 'Team' sheet")
        team_member_status_config = False
        logging.error(f"Collaborator {team_member_name} is not completely defined, please check 'Configuration.xlsx' file, 'Team' sheet")
    else:
        print(f"\nFixed values created for: {team_member_name} are set!")
        team_member_status_config = True

    return team_member_status_config


def req_number_generator(prefix, item_count):
    """Create the unique id of the new row that will be reported.

    :param prefix: The initial wbs value.
    :param item_count: The id number of the new row.
    :returns: The value that will be a unique id for the new row added.
    """                     
    unique_id = str(item_count).zfill(7)
    return prefix+'-'+unique_id


def get_valid_value(table, col, row):
    """It avoids to save a value as 'None'.

    :param table: The table where the data is located.
    :param col: The column index to read.
    :param row: The row index to read.
    """
    value = 0
    if table[col][row] != None:
        value = table[col][row]    # Get Value
    return value