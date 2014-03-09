import MySQLdb as mdb
import json
import os

def writeRowFundingData(name, funding_round, funding_amount, funding_datetime):
	dbhost = os.getenv('DBHOST')
	dbusr = os.getenv('DBUSER')
	dbpwd = os.getenv('DBPASSWD')
	dbname = os.getenv('DBNAME')
    con = mdb.connect(dbhost, dbusr, dbpwd, dbname)
    with con:
        cur = con.cursor()
        cur.execute(
        """
        INSERT INTO founder_seed2A_funds
            (name,
            funding_round, 
            funding_amount, 
            funding_datetime
            ) VALUES (%s, %s, %s, %s) 
            ON DUPLICATE KEY UPDATE
            name = VALUES(name), 
            funding_round = VALUES(funding_round),
            funding_amount = VALUES(funding_amount), 
            funding_datetime = VALUES(funding_datetime)
            """, 
            (name, funding_round, funding_amount, funding_datetime)
            )
    cur.commit()
    cur.close()
    con.close()