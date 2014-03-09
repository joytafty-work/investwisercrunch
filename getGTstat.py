#### Get google trend data
import requests
import json
import re
from pattern import web
import parsegres

def getGTstat(c):
    
    gdirpath = "gtrend_company_info"    
    gfile = "%s/%s.json" % (gdirpath, c)
    
    try: 
        with open(gfile):
            gres = open("%s/%s.json" % (gdirpath, c)).read()
            gjsoncontent = parsegres(gres)
            tsGvol = [gjsoncontent[k]['c'][1]['v'] for k in range(len(gjsoncontent))]
    except: 
        tsGvol = 0

    totGvol = sum(tsGvol)
    avgGvol = mean(tsGvol)
    sdGvol = std(tsGvol)
        
    return totGvol, avgGvol, sdGvol