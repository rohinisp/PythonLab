#!/usr/bin/python
# -*- coding: utf-8 -*-

import psycopg2
import sys


con = None

try:
     
    con = psycopg2.connect(database='my_postgres_db', user='postgres_user', password='password') 
	cur = con.cursor()    
    cur.execute("SELECT title, location FROM listing")

    rows = cur.fetchall()

    for row in rows:
        print row
		
		

except psycopg2.DatabaseError, e:
    print 'Error %s' % e    
    sys.exit(1)
    
    
finally:
    
    if con:
        con.close()
		