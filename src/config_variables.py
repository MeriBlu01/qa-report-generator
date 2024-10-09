"""
This file will save: Static Data, Constants, Configuration Files
"""

# List of possible date formats
date_formats = ['%Y-%m-%d', '%m/%d/%Y', '%d-%m-%Y', '%d/%m/%Y','%m-%d-%y','%m/%d/%y']

combo_map = {
    'Bug':{
        'NNN': [[3,3]]
    },
    'Story':{
        'VNN': [[1,2], [2,0]],
        'NNV': [[3,1]],
        'VVV': [[1,2],[2,0],[3,1]],
        'VVN': [[1,2],[2,0]],
        'VNV': [[1,2],[2,0],[3,1]],
        'NVV': [[2,0],[3,1]],
        'NVN': [[2,0]]
    },
    'Test Suite':{
        'VNN': [[0,5]],
        'VVN': [[0,5]],
        'NVN': [[0,5]]
    },
    'Task':{
        'NNV': [[3,1]],
        'NVV': [[2,0],[3,1]],
        'VVV': [[1,2],[2,0],[3,1]],
        'VNN': [[0,5]],
        'VVN': [[0,5]],
        'NVN': [[0,5]],
        'VNV': [[0,5],[3,1]]
    },
    'Epic':{
        'NNV': [[3,1]]
    },
    'Adhoc':{
        'NNN': [[3,4]]
    }
}


catalogue = {
        'Requirement Type': ['Test Planning', 'Test Analysis', 'Test Design', 'Test Execution & Reporting', 'Test Implementation', 'Project Tracking Activities'],
        'Requirement Subtype': ['Test Case', 'Test Case Execution', 'Functional Requirements', 'Defect Verification', 'Adhoc Testing','Test Plan'],
        'Action': ['Create', 'Update', 'Review', 'NA'], 
        'Module / Feature': ['Core', 'Station Management', 'Station Integration & Diagnostics'],
        'Team': ['Manual', 'Automated'],
        'Release/Build': ['Regression', 'Sprint'],
        'Complete': [0, 100],
        'ForClosing': 'Closed'
}


collabs_report_header = ['Item ID','Item Type',	'Item description', 'QA Status', 'Created',	
                            'Updated', 'Executed', 'Pass', 'Fail', 'Untested', 'Qty', 'Analysis', 'Design', 'Execution', 
                            'A_Start',	'A_End', 'B_Start', 'B_End', 'C_Start', 'C_End', 'Comments']


data_header_table = ['Project ID', 'Created By', 'Request No', 'Assigned To', 'Peer Reviewer',
                        'Short Description', 'Requirement Type', 'Requirement Subtype', 'Module / Feature',
                        'Team', 'Number of Products (Generated or Modified)', 'Total', 'Pass', 'Fail',
                        'Cant Test', 'Quantity of Bugs Closed', 'Quantity of Bugs Re-opened', 'Quantity of Bugs Verified',
                        'Quantity of New Bugs Found', 'Release/Build', 'Complete %', 'Scheduled Start Date', 'Scheduled Finish Date',
                        'Scheduled Duration', 'Scheduled Effort', 'Peer Review Scheduled Effort (hrs)', 'Scheduled Rework Effort (hrs)',
                        'Actual Start Date', 'Actual Finish Date', 'Actual Duration', 'Actual Effort', 'Peer Review Actual Effort (hrs)',
                        'ForClosing', 'Action']