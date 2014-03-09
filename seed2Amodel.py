import pandas as pd
import MySQLdb as mdb
import json
import os

def loadfeatures():
	dbhost = os.getenv('DBHOST')
	dbusr = os.getenv('DBUSER')
	dbpwd = os.getenv('DBPASSWD')
	dbname = os.getenv('DBNAME')
    
    con = mdb.connect(dbhost, dbusr, dbpwd, dbname)

	with con: 
    	d = pd.io.sql.read_frame('SELECT DISTINCT * FROM founder_seed2A_funds ORDER BY name', con)     
    	ppl = pd.io.sql.read_frame('SELECT DISTINCT * FROM founder_seed2A_info ORDER BY company_name', con)
	con.close()

	return d, ppl