#this is the "top level" module that is run when data for an entire year is to be simulated once
#it is started directly by a user on the server

from datetime import datetime
import time
from getpass import getpass

import SPD_helper_functions as HF
import SPD_db_functions as DBF
import SPD_email as EM
import SPD_attributes as ATT


def simulate_entire_year(year, amount_of_cases):
    user = "local_mysql_user"
    password = getpass("Please enter the password for the MySQL user " + "'" + user + "'" + ": ")
    starttime = datetime.now()
    print("Simulation starts ...")
    DBF.set_username(user)
    DBF.set_password(password)
    
    bodies = EM.get_bodies_of_open_mails()
    for body in bodies:
        DBF.execute_mail_body(body)
        print(' '.join(["The following email body has been executed:", body]))
        
    DBF.get_and_set_latest_data_from_db()
    
    current_case_id = DBF.get_highest_case_id_from_db()
    
    activity_table = []
    case_table = []
    for case in range (0, amount_of_cases):
        current_case_id += 1
        case_timestamp = HF.simulate_case_timestamp_for_entire_year(year)
        
        location_id, location_name = HF.simulate_location()
        variant_id = int(HF.simulate_variant_id(location_id))
        
        #simulate and insert all records into the activity table for the given case id
        activity_table_records = HF.simulate_activity_table_records(current_case_id, case_timestamp, variant_id)
        activity_table = activity_table + activity_table_records
        
        timestamp_of_last_activity = activity_table_records[-1][-2]
        
        #simulate and insert the record in the case table
        case_table_record = HF.simulate_case_table_record(current_case_id, case_timestamp, location_id, location_name, variant_id, timestamp_of_last_activity)
        case_table.append(case_table_record)
        
     
    DBF.write_entire_case_table_to_db(case_table)
    DBF.write_entire_activity_table_to_db(activity_table)
    
    HF.case_table_to_csv(case_table, year)
    HF.activity_table_to_csv(activity_table, year)
    
    endtime = datetime.now()
    print("Simulation finished in " + str(round((endtime-starttime).total_seconds())) + " seconds")
    print(str(amount_of_cases) + " cases and corresponding activities have been simulated")
    print("Data was written into the database and put out as CSV Files into the directory " + HF.output_dir)
    


def get_year_from_user():
    year = 0;
    now = datetime.now()
    while True:
        inp = input("Please enter the year (>2014) for which you want to simulate data: ")
        try:
            year = int(inp)
            if year >= 2015 and year <= now.year:
                return year
            else:
                print("Invalid input! Try again.")
        except ValueError:
            print("Invalid input! Try again.")
    return year



def get_amount_from_user():
    amount = 0;
    while True:
        inp = input("Please enter the amount of cases(max 20.000) you want to simulate: ")
        try:
            amount = int(inp)
            if amount >= 1 and amount <= 20000:
                return amount
            else:
                print("Invalid input! Try again.")
        except ValueError:
            print("Invalid input! Try again.")
    return amount



year = get_year_from_user()
amount_of_cases = get_amount_from_user()
simulate_entire_year(year, amount_of_cases)
