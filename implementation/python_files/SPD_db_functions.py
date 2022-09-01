#this module contains the functions that interact with the database (read or write)

import mysql.connector
import logging

import SPD_attributes as ATT

#credentials for accessing the mysql database
username = ""
password = ""

log = logging.getLogger("SPD_simulate_continuously.py")

def set_username(input):
    global username
    username = input

def set_password(input):
    global password
    password = input


def connect_to_db():
    global username
    global password
    
    #note: ip adress needs to be changed when transitioning between server and local machine, e.g. for testing
    mysql_server_ip = "127.0.0.1"
    
    db = "db_gbs_information_system"
    return mysql.connector.connect(host=mysql_server_ip, user=username,passwd=password, database=db)
	


def get_bike_types_from_db():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT bike_type_id, bike_type_name FROM bike_type")
    return dict(cursor.fetchall())


def get_locations_from_db():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT location_id, location_name FROM location")
    return dict(cursor.fetchall())


def get_customers_from_db():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT customer_id, customer_name FROM customer")
    return dict(cursor.fetchall())


def get_bike_types_distr_from_db():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT bike_type_id, percentage FROM bike_type_distr")
    return dict(cursor.fetchall())


def get_locations_distr_from_db():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT location_id, percentage FROM location_distr")
    return dict(cursor.fetchall())


def get_months_distr_from_db():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT month_id, percentage FROM month_distr")
    return dict(cursor.fetchall())


def get_hours_distr_from_db():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT hour_id, percentage FROM hour_distr")
    return dict(cursor.fetchall())


def get_bike_types_costs_from_db():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT bike_type_id, cost_per_minute_in_cents FROM bike_type")
    return dict(cursor.fetchall())


def get_variants_distr_from_db():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT variant_id, percentage FROM variant_distr")
    return dict(cursor.fetchall())
    
    
def get_customer_discount_rates_from_db():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT customer_id, discount_rate FROM customer_discount_rate")
    return dict(cursor.fetchall())


def get_unblocked_customer_ids_from_db():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT customer_id FROM customer WHERE blocked = FALSE")
    res = cursor.fetchall()
    res = [id[0] for id in res ]
    return res
    
    
def get_locations_with_credit_check_from_db():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT location_id FROM location WHERE credit_check = TRUE")
    res = cursor.fetchall()
    res = [id[0] for id in res ]
    return res


def get_highest_case_id_from_db():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT count(case_id) FROM case_table")
    amount_existing_case_ids = cursor.fetchone()[0]
    current_case_id = 0
    if amount_existing_case_ids != 0:
        cursor.execute("SELECT MAX(case_id) FROM case_table")
        current_case_id = cursor.fetchone()[0]
    return current_case_id



sql_insert_into_case_table = "INSERT INTO case_table (case_id, casetime, customer_id, customer_name, bike_type_id, bike_type_name, location_id, location_name, renting_duration, net_value, variant_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"


#this function is only called for the simulation of an entire year (SPD_simulate_entire_year.py)
def write_entire_case_table_to_db(case_table):
    global sql_insert_into_case_table
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.executemany(sql_insert_into_case_table, case_table)
    conn.commit()
    print(str(cursor.rowcount) + " record(s) inserted into Case Table on the database")
    cursor.close()
    conn.close()


def write_case_table_record_to_db(case_table_record):
    global sql_insert_into_case_table
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute(sql_insert_into_case_table, case_table_record)
    conn.commit()
    log.info(str(cursor.rowcount) + " record(s) inserted into Case Table on the database")
    cursor.close()
    conn.close()


sql_insert_into_activity_table = "INSERT INTO activity_table (case_id, activity, eventtime, sort) VALUES (%s, %s, %s, %s)"

#this function is only called for the simulation of an entire year (SPD_simulate_entire_year.py)
def write_entire_activity_table_to_db(activity_table):
    global insert_into_activity_table
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.executemany(sql_insert_into_activity_table, activity_table)
    conn.commit()
    print(str(cursor.rowcount) + " record(s) inserted into Activity Table on the database")
    cursor.close()
    conn.close()


def write_activity_table_records_to_db(activity_table_records):
    global sql_insert_into_activity_table
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.executemany(sql_insert_into_activity_table, activity_table_records)
    conn.commit()
    log.info(str(cursor.rowcount) + " record(s) inserted into Activity Table on the database")
    cursor.close()
    conn.close()


#this function is called once in every simulation run
def get_and_set_latest_data_from_db():
    ATT.set_customers(get_customers_from_db())
    ATT.set_bike_types(get_bike_types_from_db())
    ATT.set_locations(get_locations_from_db())
    ATT.set_bike_types_distr(get_bike_types_distr_from_db())
    ATT.set_locations_distr(get_locations_distr_from_db())
    ATT.set_months_distr(get_months_distr_from_db())
    ATT.set_hours_distr(get_hours_distr_from_db())
    ATT.set_variants_distr(get_variants_distr_from_db())
    ATT.set_bike_types_costs(get_bike_types_costs_from_db())
    ATT.set_customer_discount_rates(get_customer_discount_rates_from_db())
    ATT.set_unblocked_customer_ids(get_unblocked_customer_ids_from_db())
    ATT.set_locations_with_credit_check(get_locations_with_credit_check_from_db())
    

def reset_discount_rate_on_db(customer_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE customer_discount_rate SET discount_rate = 0.00 WHERE customer_id = " + str(customer_id) + ";")
    cursor.close()
    conn.close()


def execute_mail_body(body):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute(body)
    conn.commit()
    cursor.close()
    conn.close()
    


