#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import json
import pandas as pd
import pprint
import psycopg2

config = {
    'HOST': 'localhost',
    'USER': 'josephmisiti',
    'PORT': 5432,
    'PASSWORD': '',
    'NAME': 'plane'
}

def load():
    
    conn = psycopg2.connect(
        host=config['HOST'], 
        user=config['USER'], 
        port=config['PORT'], 
        password=config['PASSWORD'], 
        dbname=config['NAME'])
    cur = conn.cursor()
    
    events = pd.read_csv("data/events.txt")
    aircraft = pd.read_csv("data/aircraft.txt")
    events = pd.merge(events, aircraft, on='ev_id', how='outer')
    index = 1
    for event in json.loads(events.head(5000).to_json(orient='records')):
        try:
            sql_statement = """INSERT INTO 
                                events (id,acft_make, ev_month, ev_year,ev_type,ev_id,regis_no,ntsb_no) 
                               VALUES ({index},'{acft_make}',{ev_month},
                               {ev_year},'{ev_type}','{ev_id}','{regis_no}','{ntsb_no}')""".format(
                                   index=index, 
                                   acft_make=event['acft_make'].strip(), 
                                   ev_month=event['ev_month'],
                                   ev_year=event['ev_year'], 
                                   ev_type=event['ev_type'],
                                   ev_id=event['ev_id'],
                                   regis_no=event['regis_no'],
                                   ntsb_no=event['ntsb_no_x'],
                               )
            cur.execute(sql_statement)
            conn.commit()
            index += 1
        except UnicodeEncodeError, e:
            print("failed to add row %s %s" % (index, str(e)) )
            pass
        #pprint.pprint(event)
    

if __name__ == "__main__":
    sys.exit(load())