"""
this module contains "master data" for the other modules
some of the data is hard coded (e.g. possible activities and variants),
some is queried from the database in every new simulation run
"""

bike_types = {}
def set_bike_types(db_bike_types):
    global bike_types
    bike_types= db_bike_types


locations = {}
def set_locations(db_locations):
    global locations
    locations = db_locations


customers = {}
def set_customers(db_customers):
    global customers
    customers = db_customers


bike_types_distr = {}
def set_bike_types_distr(db_bike_types_distr):
    global bike_types_distr
    bike_types_distr = db_bike_types_distr


locations_distr = {}
def set_locations_distr(db_locations_distr):
    global locations_distr
    locations_distr = db_locations_distr


months_distr = {}
def set_months_distr(db_months_distr):
    global months_distr
    months_distr = db_months_distr


hours_distr = {}
def set_hours_distr(db_hours_distr):
    global hours_distr
    hours_distr = db_hours_distr


bike_types_costs = {}
def set_bike_types_costs(db_bike_types_costs):
    global bike_types_costs
    bike_types_costs = db_bike_types_costs


variants_distr = {}
def set_variants_distr(db_variants_distr):
    global variants_distr
    variants_distr = db_variants_distr
    

customer_discount_rates = {}
def set_customer_discount_rates(db_customer_discount_rates):
    global customer_discount_rates
    customer_discount_rates = db_customer_discount_rates
    
unblocked_customer_ids = []
def set_unblocked_customer_ids(db_unblocked_customer_ids):
    global unblocked_customer_ids
    unblocked_customer_ids = db_unblocked_customer_ids


locations_with_credit_check = []
def set_locations_with_credit_check(db_locations_with_credit_check):
    global locations_with_credit_check
    locations_with_credit_check = db_locations_with_credit_check


#over the time span of one year, the continuous simulation should roughly simulate this many cases
annual_target_amount_of_cases = 10000

#all possible activities
act_bb = "Book Bike"
act_ct = "Change Time"
act_cli = "Clear Invoice"
act_cri = "Create Invoice"
act_cc = "Credit Check"
act_db = "Decline Booking"
act_re = "Report Error"
act_rb = "Reserve Bike"
act_sbra = "Start Bike Rental App"

#possible process variants (14 chosen from the 35 that exists in the static data set)
var01 = (act_sbra, act_rb, act_bb, act_ct, act_cri, act_cli)
var02 = (act_sbra, act_rb, act_bb, act_ct, act_cri)
var03 = (act_sbra, act_rb, act_bb, act_cri, act_cli)
var04 = (act_sbra, act_rb,act_cc, act_bb, act_ct, act_cri, act_cli)
var05 = (act_sbra, act_rb, act_cc, act_bb, act_ct, act_cri)
var06 = (act_sbra, act_rb, act_bb, act_cri)
var07 = (act_sbra, act_rb, act_bb, act_ct)
var08 = (act_sbra, act_rb, act_cc, act_bb, act_cri)
var09 = (act_sbra, act_rb, act_cc, act_bb, act_cri, act_cli)
var10 = (act_sbra, act_rb, act_re)
var11 = (act_sbra, act_rb, act_bb)
var12 = (act_sbra, act_rb, act_cc,act_db)
var13 = (act_sbra, act_rb, act_cc, act_bb)
var14 = (act_sbra, act_rb, act_cc, act_bb, act_ct)

dict_variants = {1: var01, 2: var02, 3: var03, 4: var04, 5: var05, 6: var06, 7: var07, 8: var08, 9: var09, 10: var10, 11: var11, 12:var12}

#currently not in use (10.01.2022)
variants_incl_uncleared_invoices = {2,5,6,8}

variants_incl_credit_check = [4,5,8,9,12]
variants_incl_credit_check_distr = {4: 0.33, 5:0.29, 8:0.21, 9:0.13, 12:0.04 }

variants_incl_create_invoice = [1,2,3,4,5,6,8,9]












