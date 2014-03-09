import MySQLdb as mdb
import json

def parseDatetime(Y, M, d):
    return datetime.strftime(datetime.strptime("%s-%s-%s" % (Y, M, d), "%Y-%M-%d"), "%Y-%M-%d")

def parseFunderType(funder):
    if funder[0]['person'] != None: 
        funderType = 'person'
    elif funder[0]['company'] != None: 
        funderType = 'company'
    elif funder[0]['financial_org'] != None: 
        funderType = 'financial_org'
    else:
        funderType = 'unattributed'
    return funderType

# def parseIPOAC
from datetime import datetime
def putfundingData(name, funding_rounds):
    for i in range(len(funding_rounds)):
        n = funding_rounds[i]
        funding_round = n['round_code']
        funding_amount = str(n['raised_amount'])
        if n['funded_month'] == 'null' or n['funded_month'] == None:
            n['funded_month'] = 1
        if n['funded_day'] == 'null' or n['funded_day'] == None:
            n['funded_day'] = 1
        funding_datetime = parseDatetime(n['funded_year'], n['funded_month'], n['funded_day'])
        writeRowFundingData(name, funding_round, funding_amount, funding_datetime)

    if acquisition:
        funding_round = 'acquisition'
        funding_amount = acquisition['price_amount']
        funding_datetime = parseDatetime(n['funded_year'], n['funded_month'], n['funded_day'])
        writeRowFundingData(name, funding_round, funding_amount, funding_datetime)
        
    if ipo: 
        funding_round = 'ipo'
        funding_amount = str(ipo['valuation_amount'])
        funding_datetime = parseDatetime(n['funded_year'], n['funded_month'], n['funded_day'])
        writeRowFundingData(name, funding_round, funding_amount, funding_datetime)
        