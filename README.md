# Django backend project.

## Features
- This project allows you to get the report of all the restaurants and their respective uptimes and downtimes for the past hour, past day and past week respectively.
## Assumptions 
- Since the data provided is a static csv file which is not being updated past January 25th for certain restaurant. Need to make some assumptions regarding the tasks that needed to be performed.
- The last_day_uptime/last_day_downtime asked in the problem statement is calculated from the current day , Example - if today is 25th of Feb 2023 then the uptime and downtime will be calculated as per the record updates from the previous day i.e. 24th Feb 2023.
- The last_week_uptime/last_week_downtime asked in the problem statement is calculated from the current day , Example - if today is 25th of Feb 2023 then the uptime and downtime will be calculated as per the record updates from the previous week starting from the previous day and not including the updates of the current day i.e. updates of  19th , 20th, 21st, 22nd, 23rd , 24th Feb will be included fro calculations.

## Tech

This assignment these tech stacks:

- [Django] - Python.
- [MySQL] - Relational Database for storing and querying DATA.

## Installation

- This project requires python to be installed into your system. Create a virtual envirnonment for python and install the proper dependencies required for this particular project as with the help of requirements.txt file present in the project folder with following command : 
 pip install -r <path to requirements.txt> (Run this after activating your requirement.)
- For MySQL setup create the tables by executing queries present in the assignment_scripts file in the loop_assignment folder in the project.
- There are two API's in the project : 
    1)trigger_report - This generates the report_id for the report that will be generated and this report_id will be stored in the report_status table in the assignment DB created by the SQL scripts. This process is an asynchronous process which will just give back the report_id and then keep on executing the creation of report in the background.
    2)get_report - This fetches CSV data if the report has been generated completely and if not then returns the status as "Running".
