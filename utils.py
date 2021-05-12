#!/usr/bin/env python3

from config import config
import smtplib
import sqlite3
from datetime import datetime
import sys, os, traceback

def sendAlertEmail(errors):
    username = config['gmail']['username']
    password = config['gmail']['password']

    d = datetime.now().strftime("%m/%d/%Y, %H:%M:%S.%f")

    msg = "Subject: [ALERT] %s\n\n%s\n\n%s\n\n%s" % (errors[0], "\n".join(errors), config['gmail']['site_url'], d)
    fromaddr = config['gmail']['from_address']
    toaddrs = config['gmail']['to_addresses']

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()

def convert_c_to_f(temp_c):
    return 9.0/5.0 * float(temp_c) + 32.0

def getExceptionInfo(e):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    path = exc_tb.tb_frame.f_code.co_filename
    fname = os.path.split(path)[1]
    fdir = os.path.split(os.path.dirname(path))[1]
    return str(e)+'\n'+''.join(traceback.format_tb(exc_tb))

class dbConnection(object):
    conn = None

    def __new__(cls):
        if cls.conn is None:
            cls._instance = super(dbConnection, cls).__new__(cls)
            DIR = os.path.dirname(os.path.realpath(__file__))
            db_filename = 'sensor_values.db'
            db_filepath = os.path.join(DIR, 'database', db_filename)
            cls.conn = sqlite3.connect(db_filepath)

        return cls.conn
