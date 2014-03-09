import requests, put_founder_data

# Get founder info
def get_founder_by_ppid(company_name, company_ALid, company_img, ppid):
    user_baseapi = "https://api.angel.co/1/users/"
    
    d = dict()
    d['company_name'] = company_name
    d['company_ALid'] = company_ALid
    d['company_img'] = company_img
    
    if ppid != None: 
        for fid in ppid: 
            ### Grab founder info through API        
            furl = "%s%s" % (user_baseapi, fid)        
            print furl
            fr = requests.get(furl).json()
#             time.sleep(5)
            d['founder_name'] = fr['name']
            d['founder_followers'] = fr['follower_count']
            d['founder_img'] = fr['image']
    
            ### Grab info about other companies founder have invested
            froleurl = "https://api.angel.co/1/users/%s/roles" % fid
            frrole = requests.get(froleurl).json()['startup_roles']

            #### Roles: founder, investors, board_member
#         roles = [frrole[k]['role'] for k in range(len(frrole))]        
            d['nfounder'] = sum(['founder' in frrole[k]['role'] for k in range(len(frrole))])
            d['founder_company_ALids'] = [frrole[k]['startup']['id'] for k in range(len(frrole)) if 'founder' in frrole[k]['role']]
            d['founder_score'] = sum([frrole[k]['startup']['quality'] 
                           for k in range(len(frrole)) if 'founder' in frrole[k]['role']])
            d['ninvestor'] = sum(['investor' in frrole[k]['role'] for k in range(len(frrole))])  
            d['investor_company_ALids'] = [frrole[k]['startup']['id'] for k in range(len(frrole)) if 'founder' in frrole[k]['role']]
            d['investor_score'] = sum([frrole[k]['startup']['quality'] 
                           for k in range(len(frrole)) if 'investor' in frrole[k]['role']])
            d['nboard'] = sum(['board' in frrole[k]['role'] for k in range(len(frrole))])
            d['board_company_ALids'] = [frrole[k]['startup']['id'] for k in range(len(frrole)) if 'founder' in frrole[k]['role']]
            d['board_score'] = str(sum([frrole[k]['startup']['quality'] 
                    for k in range(len(frrole)) if 'board' in frrole[k]['role']]))
            put_founder_data(d) 
            
    else: 
        pass