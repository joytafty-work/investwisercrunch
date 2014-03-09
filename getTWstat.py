import requests
from pattern import web

def getTWstat(twitter_url):
    if ("http" in twitter_url):
        comptw = requests.get(twitter_url)
        if comptw.status_code == 200:
            domtw = web.Element(comptw.text)
            twstat = domtw.by_class("stats js-mini-profile-stats ")[0]
            tweets = twstat.children[1].children[0].by_tag('strong')[0].content
            following = twstat.children[3].children[0].by_tag('strong')[0].content
            followers = twstat.children[5].children[0].by_tag('strong')[0].content
            
            tweets = int(tweets.replace(',',''))
            following = int(following.replace(',',''))
            followers = int(followers.replace(',',''))
    else: 
        tweets = 'NULL'
        following = 'NULL'
        followers = 'NULL'
            
    return tweets, following, followers