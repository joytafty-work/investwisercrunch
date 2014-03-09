import requests
from pattern import web

def getALids_by_name(name):
    baseurl = "https://angel.co/"
    r = requests.get("%s%s" % (baseurl, name))
    
    dom = web.Element(r.text)
    div = dom.by_class(' dsss17 startups-show-sections fcs87 connections _a')
    if (div != []): 
        ALid = div[0].attrs['data-id']
    else: 
        ALid = None
        
    return ALid
