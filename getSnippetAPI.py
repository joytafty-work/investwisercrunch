import requests, getALids_by_name

def getSnippetAPI(name):
    ALid = getALids_by_name(name)
    apiurl = "https://api.angel.co/1/startups"
    
    res = requests.get("%s/%s" % (apiurl, ALid)).json()
    if res.has_key('high_concept'): 
        high_concept = res['high_concept']
    else: 
        high_concept = ''

    if res.has_key('product_desc'):
        product_desc = res['product_desc']
    else: 
        product_desc = ''
        
    if res.has_key('quality'):
        ALquality = res['quality']
    else: 
        ALquality = ''
        
    return ALid, ALquality, high_concept, product_desc