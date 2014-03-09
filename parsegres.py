def parsegres(grestext):
    from datetime import datetime
    import re
    # extract data chunk from response
    p1 = grestext.split('"rows":')[1][:-4]
    # convert date string into FORMAT(%Y%M%d)
    dateRE = r'new Date\([0-9]{4},[0-9]{1,2},[0-9]{1,2}\)'
    p2 = re.sub(dateRE, lambda m: "%s" % datetime.strftime(datetime.strptime(m.group(0)[9:-1], '%Y,%M,%d'), '%Y%M%d'), p1)
    # JSONized     
    return json.loads(p2)