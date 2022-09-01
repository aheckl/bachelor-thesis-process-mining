#this module contains functions that represent the "simulation logic" and the corresponding helper functions

from datetime import datetime
from datetime import timedelta
import random
from random import randint
import os
from pathlib import Path
import time
import csv
import numpy as np
import mysql.connector
import math
import logging
import smtplib

import SPD_attributes as ATT
import SPD_db_functions as DBF

log = logging.getLogger("SPD_simulate_continuously.py")

"""
Anmerkung: Diese Funktion (send_exception_mail()) sollte ausgefuehrt werden, falls im Skript eine Exception autritt.
Es soll eine Email Benachrichtigung an mich (a.heckl@hotmail.de) versendet werden. Auf meinem Linux Laptop funktioniert das auch, allerdings
nicht vom Linode Server aus. Das haengt wohl mit den Firewall Einstellungen zusammen, ich habe das leider nicht hinbekommen.
Da auf dem TUM Server sowieso nochmal strengere Sicherheitsvorschriften gelten und alles ueber VPn laueft, wusste ich, dass selbst wenn ich es auf dem Linode hinbekomme, 
das lange noch nicht bedeutet, dass es auch auf dem TUM Server geht. Deswegen habe ich es auch nicht weiter verfolgt. 
Ich will hier nur darstellen wie die eine sinnvolle Funktion zur Benachrichtigung ausssieht und dass ich daran gedacht hab, dass eine solche Benachrichtigung wichtig ist.
"""

#code for this funciton is largely based on
#https://www.c-sharpcorner.com/article/send-email-through-python-console-with-gmail-hotmail-and-ya/
#accessed 19.02.2022
def send_exception_mail():
    user = 'mysql.server.bachelor.thesis@outlook.de'
    pwd = 'Jeter2Berra8!'

    mail_text = "Bitte pruefen Sie das Logfile, korrigieren Sie das Skript entsprechend und starten es erneut."
    subject = "Exception im Python Skript"

    MAIL_FROM = "mysql.server.bachelor.thesis@outlook.de"
    RCP_TO = "a.heckl@hotmail.de"

    DATA = "From:%s\nTo:%s\nSubject:%s\n\n%s" % (MAIL_FROM, RCP_TO, subject, mail_text)

    server = smtplib.SMTP('smtp-mail.outlook.com:587')
    server.starttls()
    server.login(user, pwd)
    server.sendmail(MAIL_FROM, RCP_TO, DATA)
    server.quit()


def simulate_case_table_record(current_case_id, case_timestamp, location_id, location_name, variant_id, timestamp_of_last_activity):
    customer_id, customer_name = simulate_customer()
    bike_type_id, bike_type_name = simulate_bike_type()
    renting_duration = simulate_renting_duration(variant_id, case_timestamp, timestamp_of_last_activity)
    
    #net value calculation: cost of bike per minute * renting time in minutes * (1-discount rate)
    discount_rate = ATT.customer_discount_rates[customer_id]
    net_value = round(ATT.bike_types_costs[bike_type_id] * renting_duration * (1 - discount_rate))
    
    #after discount rate has been applied, it is set back to 0
    if discount_rate > 0:
        DBF.reset_discount_rate_on_db(customer_id)
    
    return (current_case_id, case_timestamp, customer_id, customer_name, bike_type_id, bike_type_name, location_id, location_name, renting_duration, net_value, variant_id)


def simulate_customer():
    #customers are equally distributed:
    customer_id = random.choice(ATT.unblocked_customer_ids)
    return customer_id, ATT.customers[customer_id]


def simulate_bike_type():
    bike_types_ids = list(ATT.bike_types.keys())
    bike_types_probs = []
    for id in bike_types_ids:
        bike_types_probs.append(ATT.bike_types_distr[id])
    simulated_bike_type_id = int(np.random.choice(bike_types_ids, 1,p=bike_types_probs)[0])
    
    return simulated_bike_type_id, ATT.bike_types[simulated_bike_type_id]


def simulate_location():
    locations_ids = list(ATT.locations.keys())
    locations_probs = []
    for id in locations_ids:
        locations_probs.append(ATT.locations_distr[id])
    simulated_location_id = int(np.random.choice(locations_ids, 1,p=locations_probs)[0])
    
    return simulated_location_id, ATT.locations[simulated_location_id]


#helper function for simulating the renting duration
def get_max_duration(start_str, end_str):
    date_format_str = "%Y-%m-%d %H:%M:%S"
    start_time = datetime.strptime(start_str, date_format_str)
    end_time = datetime.strptime(end_str, date_format_str)
    diff = end_time - start_time
    minutes = math.floor(divmod((end_time - start_time).total_seconds(), 60)[0])
    
    return minutes


def simulate_renting_duration(variant_id, case_timestamp, timestamp_of_last_activity):
    #if an invoice was created, renting duration cannnot be longer than diff between start and creation of invoice
    if variant_id in ATT.variants_incl_create_invoice:
        date_format_str = "%Y-%m-%d %H:%M:%S"
        max_duration = get_max_duration(case_timestamp, timestamp_of_last_activity)
        if max_duration == 0:
            return 1
        else:
            return randint(1, max_duration)
    else:
        #defining 3 intervals: 5-30 min, 31-120min und 121-210 min
        intervals = [1,2,3]
        intervals_distr = [0.2, 0.72, 0.08]
        interval = np.random.choice(intervals, 1,p=intervals_distr)[0]
        if interval == 1:
            return randint(5,30)
        elif interval == 2:
            return randint(31, 120)
        else:
            return randint(121, 210)



#returns all activity table records given a certain variant
def simulate_activity_table_records(current_case_id, case_timestamp, variant_id):
    sort = 0
    records = []
    
    #"new" timestamp = previous timestamp + duration of the previous activity
    prev_activity_timestamp = ""
    prev_activity_duration = 0
    current_activity_timestamp = ""
    current_activity_duration = 0
    for activity in ATT.dict_variants[variant_id]:
        sort +=1
        if sort == 1:
            current_activity_timestamp = case_timestamp    
        else:
            current_activity_timestamp = add_minutes_to_timestamp(prev_activity_timestamp, prev_activity_duration)
            
        current_activity_duration = simulate_activity_duration(activity)
        records.append((current_case_id, activity, current_activity_timestamp, sort))
        
        prev_activity_timestamp = current_activity_timestamp
        prev_activity_duration = current_activity_duration
        
    return records


def simulate_variant_id(location_id):
    variants_ids = []
    variants_probs = []
    
    #if the given location requires a credit check, only certain activities can be simulated (those that include the activity "credit check")
    if location_id in ATT.locations_with_credit_check:
        variants_ids = ATT.variants_incl_credit_check
        for id in variants_ids:
            variants_probs.append(ATT.variants_incl_credit_check_distr[id])
    else:
        variants_ids = list(ATT.variants_distr.keys())
        for id in variants_ids:
            variants_probs.append(ATT.variants_distr[id])
    
    return np.random.choice(variants_ids, 1,p=variants_probs)[0]


#this function is only called for the simulation of an entire year (SPD_simulate_entire_year.py)
def simulate_month():
    months_ids = list(ATT.months_distr.keys())
    months_probs = []
    for id in months_ids:
        months_probs.append(ATT.months_distr[id])
    
    return np.random.choice(months_ids, 1,p=months_probs)[0]


#this function is only called for the simulation of an entire year (SPD_simulate_entire_year.py)
def simulate_hour():
    hours_ids = list(ATT.hours_distr.keys())
    hours_probs = []
    for id in hours_ids:
        hours_probs.append(ATT.hours_distr[id])
    
    return np.random.choice(hours_ids, 1,p=hours_probs)[0]


#this function is only called for the simulation of an entire year (SPD_simulate_entire_year.py)
def simulate_case_timestamp_for_entire_year(year): 
    #when simulating data for an entire year, days, minutes and seconds are uniformly distributed
    #months and hours follow certain distributions (e.g. more rentals in summer months)
    month = simulate_month()
    day = randint(1,28)
    hour = simulate_hour()
    minute = randint(1,59)
    second = randint(1,59)
    
    return str(datetime(year, month, day, hour, minute, second))


#Input is a timestamp as a String 
#Output is also a timestamp as a String
def add_minutes_to_timestamp(timestamp, n):
    date_format_str = "%Y-%m-%d %H:%M:%S"
    given_time = datetime.strptime(timestamp, date_format_str)
    new_time = given_time + timedelta(minutes=n)
    new_timestamp = new_time.strftime(date_format_str)
    
    return new_timestamp


#this function determines how many cases are simulated in the current simulation run
def simulate_amount_of_cases(month, hour): 
    prob_month = float(ATT.months_distr[month])
    prob_day = 1/30
    prob_hour = float(ATT.hours_distr[hour])
    
    #calculate the expected amount of cases in the specified hour
    expected_amount_of_cases = prob_month * prob_day * prob_hour * ATT.annual_target_amount_of_cases
    deviation = 0.5
    left_bound = math.floor((1 - deviation) * expected_amount_of_cases)
    right_bound = math.ceil((1 + deviation) * expected_amount_of_cases)
    log.info("The amount of cases simulated in this run is chosen from the following Interval: [" + str(left_bound) + ", " +str(right_bound) + "]")
    
    #within the specified interval, the values are uniformly distributed
    amount = randint(left_bound, right_bound)
    log.info("This many cases are simulated in this run: " + str(amount))
    
    return amount


#this function is only called for the simulation of an entire year (SPD_simulate_entire_year.py)
def activity_table_to_csv(activity_table, year):
    table_to_csv(activity_table, "Activity_Table", year)


#this function is only called for the simulation of an entire year (SPD_simulate_entire_year.py)
def case_table_to_csv(case_table, year):
    table_to_csv(case_table, "Case_Table", year)


output_dir = 'Output_CSVs_of_entire_years'

#this function is only called for the simulation of an entire year (SPD_simulate_entire_year.py)
def table_to_csv(tableobject, tablename, year):
    global output_dir
    now = datetime.now()
    timestamp = str(now.year)+"-"+str(now.month)+"-"+str(now.day)+"-"+str(now.hour)+"-"+str(now.minute)
    filename = str(year) + "_" + tablename + "_" + timestamp + '.csv'
    
    #make new output directory if it doesn't exist already:
    Path(os.getcwd() + os.path.sep + output_dir).mkdir(parents=True, exist_ok=True)
    
    output_path = os.getcwd() + os.path.sep + output_dir + os.path.sep
    with open(output_path + filename, 'w', newline='') as f:
        write = csv.writer(f) 
        write.writerows(tableobject)
    


def simulate_activity_duration(activity):
    #the values for the intervals were chosen similar to the existing, static dataset
    #the Excel Analysis Ultimate File (Sheet "Intervalle pro Activity") can be used to retrace the values
    #for an example of how to read & understand the statements, look at the first elif statement below
    if activity == ATT.act_sbra:
        intervals = [1,2]
        intervals_distr = [0.9971, 0.0029]
        interval = np.random.choice(intervals, 1,p=intervals_distr)[0]
        if interval == 1:
            return 1
        else:
            return randint(2,374)
    
    #example of how to read these statements:
    #if the given activity is "reserve bike", the probablity that this activity has a duration that is between 1 and 5 minutes(fist interval)
    #is 70%, and the probability that it has a duration between 6 and 971 minutes (second interval) is 30%
    #within an interval, the possible values are uniformly (i.e., randomly) distributed
    elif activity == ATT.act_rb:
        intervals = [1,2]
        intervals_distr = [0.7, 0.3]
        interval = np.random.choice(intervals, 1,p=intervals_distr)[0]
        if interval == 1:
            return randint(1, 5)
        else: 
            return randint(6, 371)
    
    elif activity == ATT.act_bb:
        intervals = [1,2,3,4,5]
        intervals_distr = [0.06, 0.2, 0.08, 0.6597, 0.0003]
        interval = np.random.choice(intervals, 1,p=intervals_distr)[0]
        if interval == 1:
            return 1
        elif interval == 2:
            return randint(2,10)
        elif interval == 3:
            return randint(11,25)
        elif interval == 4:
            return randint(26, 371)
        else:
            return randint(1600,2200)
        
    elif activity == ATT.act_ct:
        intervals = [1,2,3]
        intervals_distr = [0.18, 0.8194, 0.0006]
        interval = np.random.choice(intervals, 1,p=intervals_distr)[0]
        if interval == 1:
            return 1
        elif interval == 2:
            return randint(2,15)
        else:
            return randint(65, 90)    
    
    elif activity == ATT.act_cri:
        intervals = [1,2,3]
        intervals_distr = [0.46, 0.5399, 0.0001]
        interval = np.random.choice(intervals, 1,p=intervals_distr)[0]
        if interval == 1:
            return 1
        elif interval == 2:
            return randint(2,25)
        else:
            return randint(300, 400)
        
    elif activity == ATT.act_cc:
        intervals = [1,2]
        intervals_distr = [0.07, 0.93]
        interval = np.random.choice(intervals, 1,p=intervals_distr)[0]
        if interval == 1:
            return 1
        else: 
            return randint(2,50)
    
    elif activity == ATT.act_re:
        intervals = [1,2]
        intervals_distr = [0.48, 0.52]
        interval = np.random.choice(intervals, 1,p=intervals_distr)[0]
        if interval == 1:
            return 1
        else: 
            return randint(2,75)

    elif activity == ATT.act_db:
        return 1
    elif activity == ATT.act_cli:
        return 1
    else:
        return 1 #Assumption: an unknown activity takes one minute (this should not happen at all)
