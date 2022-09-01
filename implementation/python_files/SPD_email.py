"""
This module provides functionalitiy for handling emails that have been sent
from within the action engine. These emails contain SQL Update statements.
This is a workaround to link Actions from the Action Engine to the MySQL Database Server. 
"""

import imaplib
import email
from email.header import decode_header
import os

username = "mysql.server.bachelor.thesis@outlook.de"
password = "Jeter2Berra8!"


"""
This function checks if the body of an email is an SQL statement that is allowed to be executed on the database.
This is necessary as the email body can be altered by learners before they send the email. 
Emails bodies are only allowed to have the following 3 forms:
UPDATE customer_discount_rate SET discount_rate = 0.20 WHERE customer_id = ${customer_id};
UPDATE customer SET blocked = TRUE WHERE customer_id = ${customer_id};
UPDATE location SET credit_check = TRUE WHERE location_id = ${location_id};
"""
def check_sql_validity(sql_split):
    #the following customers and locations are allowed
    customer_ids = ["1;", "2;", "3;", "4;", "5;", "6;", "7;", "8;", "9;", "10;"]
    location_ids = ["1;", "2;", "3;"]
    
    if len(sql_split) != 10:
        return False
    if sql_split[0].lower() != "update":
        return False
    if sql_split[2].lower() != "set":
        return False
    if sql_split[4] != "=":
        return False
    if sql_split[6].lower() != "where":
        return False
    if sql_split[8] != "=":
        return False
    
    #id for the databse table that is affected
    table = 0
    if sql_split[1].lower() == "customer_discount_rate":
        table = 1
    if sql_split[1].lower() == "customer":
        table = 2
    if sql_split[1].lower() == "location":
        table = 3
    
    if table == 0:
        return False
    
    if table == 1:
        if sql_split[3].lower() != "discount_rate" or sql_split[7].lower() != "customer_id":
            return False
        if sql_split[9] not in customer_ids:
            return False
        try:
            x = float(sql_split[5])
            if x < 0 or x > 0.9: #discount rate is allowed to be between 0 and 0.9
                return False
        except:
            return False
    
    if table == 2:
        if sql_split[3].lower() != "blocked" or sql_split[7].lower() != "customer_id":
            return False
        if sql_split[5].lower() != "true":
            return False
        if sql_split[9] not in customer_ids:
            return False
    
    if table == 3:
        if sql_split[3].lower() != "credit_check" or sql_split[7].lower() != "location_id":
            return False
        if sql_split[5].lower() != "true":
            return False
        if sql_split[9] not in location_ids:
            return False
    
    return True



#get_bodies_of_open_mails function is largely based on
#https://www.thepythoncode.com/article/reading-emails-in-python
#accessed 9th Jan 2022

#this function returns a list of email bodies, i.e. SQL Update statements.
#every email contians exactly one SQL Update Statement.
def get_bodies_of_open_mails():
    bodies = []
    imap = imaplib.IMAP4_SSL("imap-mail.outlook.com")
    imap.login(username, password)

    status, messages = imap.select("INBOX")
    amount_of_messages = int(messages[0])
    
    for i in range(amount_of_messages, 0, -1):
        # fetch the email message by ID
        status, msg = imap.fetch(str(i), "(RFC822)")
        for elem in msg:
            if isinstance(elem, tuple):
                # parse a bytes email into a message object
                msg = email.message_from_bytes(elem[1])
                
                # decode the email subject
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    # if it's a bytes, decode to str
                    if isinstance(encoding, type(None)):
                        subject = ""
                    else:
                        subject = subject.decode(encoding)
                
                if "sql input" in subject.lower():
                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            if content_type == "text/plain":
                                try:
                                    body = part.get_payload(decode=True).decode()
                                    body = body.strip()
                                    body_split = body.split()
                                    if check_sql_validity(body_split):
                                        bodies.append(body)
                                except:
                                    pass
                                #delete the email
                                imap.store(str(i), "+FLAGS", "\\Deleted")
                                imap.expunge()
                else:
                    continue
                
    imap.close()
    imap.logout()
    return bodies
    
 

