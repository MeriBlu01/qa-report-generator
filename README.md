# QA Report Generator

## Project Overview
The **QA Report Generator** is a Python-based *executable*, created using the PyInstaller library, designed specifically to address the reporting needs of the QA team at my current company. 
This tool significantly improves efficiency by automating the creation of detailed activity reports, reducing the time spent on this task from **3-5 days** to just **a few seconds**.

The executable is configured with the specific requirements of the Delivery Manager and QA processes, ensuring seamless integration with the team's workflow.

## Features
- **Python Executable (.exe)**: Created using PyInstaller, easily deployable without requiring a Python environment.
  
- **Excel Integration**: 
  * **Tracker File**: QA team members use this file to report their activities (Task, Story, Epic, Bug, Adhoc) and include start/end dates, descriptions, status, and effort time.

<p align="center">
 <img src="https://portfolio-america-lagos.s3.amazonaws.com/imgs-portfolio-qa-report-generator-project/QA_Report.png" width="900" height="auto"/></p>

    
  * **Configuration File**: Acts as the UI for the Delivery Manager, allowing the selection of the reporting period (month-year), specifying the name file (document where QA engineers report),
    setting the WBS (Work Breakdown Structure) that will be reported, and finally the 'Last Item Number' value (this was requested to maintain serialization of reported activities).

<p align="center">
 <img src="https://portfolio-america-lagos.s3.amazonaws.com/imgs-portfolio-qa-report-generator-project/period_table.png" width="450" height="auto"/></p>

  
  <p>Below are the other tables that need to be configured (Sprints and Team tables). 
    The sprint table is just for record keeping, the data has no effect on the final report result.</p>    

<p align="center">
 <img src="https://portfolio-america-lagos.s3.amazonaws.com/imgs-portfolio-qa-report-generator-project/sprints_table.png" width="370" height="auto"/> &nbsp;&nbsp;
 <img src="https://portfolio-america-lagos.s3.amazonaws.com/imgs-portfolio-qa-report-generator-project/team_table.png" width="530" height="auto"/></p>

    
> Note: Find Excel file templates in the templates folder.


- **Error Handling**: 
  - If the Tracker file contains incorrect or incomplete data, the program logs the errors in a `error_log.txt` file and prevents the generation of an invalid final report.
  - Ensures data integrity by logging issues and alerting the user before continuing the process.
  - If no error is found, the executable will log the warning with the name of the final report that has been created.
    

## Efficiency Benefits
- **Time-Saving**: The Delivery Manager used to spend ***3-5 days*** manually compiling the QA final report. With this executable, the report is generated within ***seconds***,
  freeing up valuable time and ensuring accuracy.
- **Automation**: The tool automates repetitive tasks, reducing the risk of human error and improving the overall quality of the final report.
  
## Workflow
1. **Configuration Setup**: The Delivery Manager selects the reporting period and WBS via the Configuration file and specifies the Tracker file.
2. **Data Processing**: The executable processes the Tracker file data based on item type (Task, Story, Epic, Bug, Adhoc), time period, and other relevant fields like description and effort.
3. **Final Report Generation**: The processed data is generated in the required template and delivered as the final report.
4. **Error Logging**: In case of issues with the Tracker file data, an error report is created in `error_log.txt`, preventing the final report from being generated until errors are resolved.

## Files
- `Tracker.xlsx`: Excel file where QA team members report their activities.
- `Configuration.xlsx`: Excel file that serves as the UI for the Delivery Manager, selecting the reporting period and specifying the Tracker file.
- `error_log.txt`: A log file that captures errors if something is wrong in the Tracker report.

## How It Works
- **Error Handling**: If there are inconsistencies in the Tracker file (e.g., missing data, incorrect formatting),
  the `executable` will halt the report generation process and log the errors in a plain-text log file (`error_log.txt`).
- **Automatic Report Generation**: Once valid data is provided, the executable generates a well-formatted report in seconds, ready to be distributed to stakeholders and BI analysts.

## How to Use
1. **Prerequisites**: Ensure you have the required `.xlsx` files (Tracker and Configuration) set up. The excel files and the `executable` must be in the same directory location.
2. **Run the Executable**: Double-click the `executable` to start the process.
3. **Error Handling**: If there’s an issue with the Tracker file, check the `error_log.txt` for detailed error information and correct it before attempting to regenerate the report.
4. **Final Report**: Once the process completes without errors, the final report will be generated in the required template format.

## Technologies Used
- **Python**: Core programming language for data processing and error handling.
- **PyInstaller**: Used to package the Python script as an executable.
- **openpyxl**: Library to read and write Excel files.
- **Logging**: Error logging and tracking of any issues encountered during the report generation process.
- **numpy**: For soma required calculations.

## Future Enhancements
- **UI Enhancement**: Implementing a graphical interface for easier user interaction.
- **Additional Report Formats**: Supporting different formats (e.g., CSV, PDF) for the final report.
- **Cloud Integration**: Integrating with cloud services like AWS for storing reports.

---

# How to create the executable
## For Windows
1.  **Prerequisites**: Have python 3 and pip installed. The repository has been cloned.
2.  Open the Command Prompt.
3.  Locate to the directory where the Excel files and the cloned repository are placed.
   
      ```cd <path/to/your/files>```

4. Create a virtual environment.

      ```python -m venv <env_name>```

5. Activate your virtual environment.

     ```<env_name>\Scripts\activate```

6. Install the required libraries (**pyinstaller**, **openpyxl**, **numpy**). More detailed information can be found in the requirements.txt file located in this repository.

     ```pip install <library_name>```

7. Locate inside the project folder.

    ```cd qa_report_generator```

8. Create the executable.

   ```pyinstaller --onefile --icon=assets/app_icon.ico --name "QA_Report_Generator" main.py```

9. Two new folders will be created inside the project folder (build, dist). Inside the 'dist' folder the executable has been created. Move it to the same directory as the Excel files.
    You can delete those folders later.
10. Once the executable and the excel files are in the same location, you could double click the executable to run it and create the new final report.
11. The final Excel report will be created in the same location and it will be named as 'Report_%Y-%m-%d_hour-minutes.xlsx'
   
## For macOS
1.  **Prerequisites**: Have python 3 and pip installed. The repository has been cloned.
2.  Open the Command Prompt.
3.  Locate to the directory where the Excel files and the cloned repository are placed.
   
      ```cd <path/to/your/files>```

4. Create a virtual environment.

      ```python3 -m venv myenv```

5. Activate your virtual environment.

     ```source myenv/bin/activate```

6. Install the required libraries (**pyinstaller**, **openpyxl**, **numpy**). More detailed information can be found in the requirements.txt file located in this repository.

     ```python3 -m pip install <library_name>```

7. Locate inside the project folder.

    ```cd qa_report_generator```

8. Create the executable.

   ```python -m PyInstaller --onefile --icon=assets/app_icon.ico --name "QA_Report_Generator" main.py```

---

## Tests
The project has in its structure the folder `'tests'` which is where the scripts that are specifically to test the project's methods and classes with **unittest** framework will be stored.

