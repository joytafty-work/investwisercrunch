#### Get facebook likes
import requests
from pattern import web
import json

def getFBstat(c):

    URI_SCHEME = "http"
    likeurl = "%s://graph.facebook.com/%s?fields=likes" % (URI_SCHEME, c)
    talkabouturl = "%s://graph.facebook.com/%s?fields=talking_about_count" % (URI_SCHEME, c)
    # FBurl = "http://graph.facebook.com/Facebook?fields=likes

    FBlikes = requests.get(likeurl)
    if FBlikes.status_code == 200:
        likes = FBlikes.json()['likes']
    else: 
        likes = 0
    
    FBtalks = requests.get(talkabouturl)
    if FBtalks.status_code == 200:        
        talking_about_count = FBtalks.json()['talking_about_count']
    else:
        talking_about_count = 0

    return likes, talking_about_count