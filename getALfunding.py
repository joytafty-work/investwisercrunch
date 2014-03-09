import os, requests

def getALfunding(CBtag):
    # Crunchbase
    api_base = "http://api.crunchbase.com/v/1/company/"
    CB_API_KEY = os.getenv('CRUNCHBASE_API_KEY'); 
    CBapiwkey = "%s%s.js?api_key=%s" % (api_base, CBtag, CB_API_KEY)
    getcompanyData(CBapiwkey)

def getcompanyData(CBapiwkey):
    r = requests.get(CBapiwkey)
    funding_json = []
    if r.status_code == 200:
        funding_json = r.json()
        if 'error' not in funding_json:
            name = funding_json['name']
                
        if funding_json['ipo']: 
            ipo = funding_json['ipo'] 
        else:
            ipo = 'NULL'
        
        if funding_json['acquisition']:
            acquisition = funding_json['acquisition']             
        else: 
            acquisition = 'NULL'
    
        if funding_json['funding_rounds']: 
            funding_rounds = funding_json['funding_rounds']
        else: 
            funding_rounds = 'NULL' 

    putfundingData(name, funding_rounds, ipo, acquisition)
#         putfundingData(name, funding_rounds)
        