#this is the "top level" module that is run when data is to be simulated continuously
#it is started directly by a user on the server

from datetime import datetime
import time
from getpass import getpass
import logging

import SPD_helper_functions as HF
import SPD_db_functions as DBF
import SPD_email as EM
import SPD_attributes as ATT

log_time = datetime.now()
logfile_title = "logfile_starting_" + str(log_time.year) + "-" + str(log_time.month) + "-" + str(log_time.day) + ".log"
logging.basicConfig(level=logging.DEBUG, filename=logfile_title, filemode='w', format='%(message)s')


def simulate_continuously(sleeptime_in_minutes):
    starttime = time.time()
    sleeptime = sleeptime_in_minutes*60
    
    user = "local_mysql_user"
    password = getpass("Please enter the password for the MySQL user " + "'" + user + "'" + ": ")
    DBF.set_username(user)
    DBF.set_password(password)
    print("You can now close this terminal/session. Simulation is running in the background.")	

    #this loop is executed once in every simulation run (e.g., every 60 minutes)
    while True:
        now = datetime.now()
        logging.info("-"*50)
        logging.info(' '.join(["New simulation run starts now:", now.strftime("%Y-%m-%d %H:%M:%S")]))
        
        #handle the emails from the action engine that contain sql update statements
        bodies = EM.get_bodies_of_open_mails()
        for body in bodies:
            DBF.execute_mail_body(body)
            logging.info(' '.join(["The following email body has been executed:", body]))
        
        DBF.get_and_set_latest_data_from_db()
        
        #the amount of cases that are simulated in this simulation run
        amount_of_cases = HF.simulate_amount_of_cases(now.month, now.hour)
        
        current_case_id = DBF.get_highest_case_id_from_db()
        
        if amount_of_cases != 0:
            for case in range (1, amount_of_cases+1):
                current_case_id += 1
                case_timestamp = str(datetime(now.year, now.month, now.day, now.hour, now.minute, now.second))
                
                location_id, location_name = HF.simulate_location()
                variant_id = int(HF.simulate_variant_id(location_id))
                
                activity_table_records = HF.simulate_activity_table_records(current_case_id, case_timestamp, variant_id)
                logging.info("\nActivity Table Record(s):")
                for record in activity_table_records:
                    logging.info(record)
                
                timestamp_of_last_activity = activity_table_records[-1][-2]

                case_table_record = HF.simulate_case_table_record(current_case_id, case_timestamp, location_id, location_name, variant_id, timestamp_of_last_activity)
                logging.info("\nCase Table Record:")
                logging.info(case_table_record)
                logging.info("")
                
                DBF.write_activity_table_records_to_db(activity_table_records)
                DBF.write_case_table_record_to_db(case_table_record)
        
        endtime = datetime.now()
        logging.info(' '.join(["\nSimulation run finished at", endtime.strftime("%Y-%m-%d %H:%M:%S")]))
        logging.info("Duration: " + str(round((endtime-now).total_seconds())) + " second(s)")
        logging.info("Waiting for next simulation run in about " + str(sleeptime_in_minutes) + " minutes ...")
        
        time.sleep(sleeptime - ((time.time() - starttime) % 60.0))


#currently not in use
def get_sleeptime_from_user():
    sleeptime = 0;
    while True:
        inp = input("Please enter how many minutes(max 10080) should be between two runs of the simulation(60 is recommended): ")
        try:
            sleeptime = int(inp)
            if sleeptime >= 1 and sleeptime <= 10080:
                return sleeptime
            else:
                print("Invalid input! Try again.")
        except ValueError:
            print("Invalid input! Try again.")
    return sleeptime
    

#time between simulation runs in minutes
#sleeptime = get_sleeptime_from_user()
sleeptime = 60


try:
    simulate_continuously(sleeptime)
except Exception as e:
    print("An exception occurred:")
    print(e)
    print("Please check the logfile for further information, resolve the issue and restart the script.")
    logging.exception("message")
    #the following function does not work when the script runs on a server
    #HF.send_exception_mail()
  
