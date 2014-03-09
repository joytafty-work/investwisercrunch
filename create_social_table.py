import MySQLdb as mdb
import json
import os

def create_social_table():
    dbhost = os.getenv('DBHOST')
    dbusr = os.getenv('DBUSER')
    dbpwd = os.getenv('DBPASSWD')
    dbname = os.getenv('DBNAME')

    con = mdb.connect('localhost', 'joyinsight', 'san00k', 'insightdata')
    with con: 
        cur = con.cursor()    
        cur.execute(
        """
        CREATE TABLE IF NOT EXISTS startups_seed_visibility
            (name TINYTEXT, 
            FBlikes TINYTEXT,
            FBtalking_about_count TINYTEXT,
            tweets TINYTEXT, 
            TWfollowing TINYTEXT, 
            TWfollowers TINYTEXT,
            total_GTrends_vol TINYTEXT, 
            avg_GTrends_vol TINYTEXT,
            sd_GTrends_vol TINYTEXT
            )
        """)   
        cur.close()
    con.close()