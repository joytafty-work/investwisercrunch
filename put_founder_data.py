import MySQLdb as mdb
import json
import os

def put_founder_data(d): 

    dbhost = os.getenv('DBHOST')
    dbusr = os.getenv('DBUSER')
    dbpwd = os.getenv('DBPASSWD')
    dbname = os.getenv('DBNAME')

    con = mdb.connect(dbhost, dbuser, dbpwd, dbname)
    with con: 
        cur = con.cursor()
        cur.execute(
        """
        INSERT INTO founder_seed2A_info
            (company_name,
            company_img,
            company_ALid,
            founder_name,
            founder_followers,
            founder_img,
            nfounder,
            founder_company_ALids, 
            founder_score,
            ninvestor,
            investor_company_ALids,
            investor_score,
            nboard,
            board_company_ALids,
            board_score
            ) VALUES (%s,%s,%s,%s, %s,%s,%s,%s, %s,%s,%s,%s, %s,%s,%s)
            ON DUPLICATE KEY UPDATE
            company_name=VALUES(company_name),
            company_img=VALUES(company_img),
            company_ALid=VALUES(company_ALid),
            founder_name=VALUES(founder_name),
            founder_followers=VALUES(founder_followers),
            founder_img=VALUES(founder_img),
            nfounder=VALUES(nfounder),
            founder_company_ALids=VALUES(founder_company_ALids), 
            founder_score=VALUES(founder_score),
            ninvestor=VALUES(ninvestor),
            investor_company_ALids=VALUES(investor_company_ALids),
            investor_score=VALUES(investor_score),
            nboard=VALUES(nboard),
            board_company_ALids=VALUES(board_company_ALids),
            board_score=VALUES(board_score)
        """, (d['company_name'],
            d['company_img'],
            d['company_ALid'],
            d['founder_name'],
            d['founder_followers'],
            d['founder_img'],
            d['nfounder'],
            str(d['founder_company_ALids']), 
            d['founder_score'],
            d['ninvestor'],
            str(d['investor_company_ALids']),
            d['investor_score'],
            d['nboard'],
            str(d['board_company_ALids']),
            d['board_score'])
        )
    cur.commit()
    cur.close()
    con.close()