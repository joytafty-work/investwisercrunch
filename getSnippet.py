import requests
from pattern import web

def getSnippet(name): 
    burl = "https://angel.co/"
    url = "%s%s" % (burl, name)
    print url
    r = requests.get(url).text

    a = web.Element(r).by_class("high_concept")
    if hasattr(a, 'by_tag') and len(a) > 0: 
        snp  = a[0].by_tag("p")[0].content
    else: 
        snp = ''

    return snp