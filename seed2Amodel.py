import pandas as pd
import MySQLdb as mdb
import json
import os

def loadfeatures():
	dbhost = os.getenv('DBHOST')
	dbusr = os.getenv('DBUSER')
	dbpwd = os.getenv('DBPASSWD')
	dbname = os.getenv('DBNAME')

	con = mdb.connect(dbhost, dbusr, dbpwd, dbname)

	with con: 
    	d = pd.io.sql.read_frame('SELECT DISTINCT * FROM founder_seed2A_funds ORDER BY name', con)     
    	ppl = pd.io.sql.read_frame('SELECT DISTINCT * FROM founder_seed2A_info ORDER BY company_name', con)
	con.close()

	return d, ppl

def process_features(d, ppl):
	from datetime import datetime, date
	import numpy as np
	##### Convert funding data type
	d['funding_datetime'] = pd.to_datetime(d['funding_datetime'])
	d['funding_amount'].replace('None', 1e1, inplace=True)
	d['funding_amount'].replace('NaN', 1e1, inplace=True)
	d.funding_amount = d.funding_amount.astype(float)

	### Convert people data type
	ppl['founder_followers'] = ppl['founder_followers'].astype(float) 
	ppl['nfounder'] = ppl['nfounder'].astype(float) 
	ppl['founder_score'] = ppl['founder_score'].astype(float) 
	ppl['ninvestor'] = ppl['ninvestor'].astype(float) 
	ppl['investor_score'] = ppl['investor_score'].astype(float) 
	ppl['nboard'] = ppl['nboard'].astype(float) 
	ppl['board_score'] = ppl['board_score'].astype(float) 
	ppl.replace('None', '0')

	return d, ppl

def parse_sets(d):
	##### Separate dataset into groups
	seed = d[d.funding_round == 'seed']
	seed.rename(columns={'funding_datetime': 'seed_date', 'funding_amount': 'seed_amount'}, inplace=True)
	seed_group = seed.groupby('name')

	seriesA = d[d.funding_round == 'a']
	seriesA.rename(columns={'funding_datetime': 'seriesA_date', 'funding_amount': 'seriesA_amount'}, inplace=True)
	seriesA_group = seriesA.groupby('name')

	### companies already received seriesA funding
	winset = pd.merge(seed, seriesA, how='inner', on='name')
	winset['td'] = pd.Series(winset['seriesA_date'] - winset['seed_date']).apply(lambda x: float(x)*1.15741e-14)
	winset['lifetime'] = pd.Series(date.today() - winset['seed_date']).apply(lambda x: float(x)*1.15741e-14)

	##### Companies not yet received series A 
	from datetime import date
	pred = pd.merge(seed, seriesA, how='outer', on='name')
	predset = pred[pred.seriesA_date.isnull()]
	predset['td'] = pd.Series(date.today()-predset['seed_date']).apply(lambda x: float(x)*1.15741e-14)
	predset['lifetime'] = pd.Series(date.today() - predset['seed_date']).apply(lambda x: float(x)*1.15741e-14)

	### Combine data set
	a = winset.copy()
	allset = a.append(predset)

	### Generate labels
	winy = np.zeros(len(winset))
	predy = np.zeros(len(predset))+1
	ally = pd.Series(np.concatenate((winy, predy)))

	return allx, ally

def build_predictive_features(ppl):
	pplgrp = ppl.groupby('name')
	ppl = ppl.rename(columns={'company_name':'name'})
	winppl = pd.merge(winset, ppl, on='name', how='inner')
	predppl = pd.merge(predset, ppl, on='name', how='inner')

	pplgrp.founder_followers = pplgrp['founder_followers'].aggregate(np.mean)
	founder_sumfollowers = pplgrp['founder_followers'].aggregate(np.sum)
	nfounder = pplgrp['nfounder'].aggregate(np.mean)
	nfounder_sum = pplgrp['nfounder'].aggregate(np.sum)
	founder_score = pplgrp['founder_score'].aggregate(np.mean)

	ninvestor = pplgrp['ninvestor'].aggregate(np.mean)
	ninvestor_sum = pplgrp['ninvestor'].aggregate(np.sum)
	investor_score = pplgrp['investor_score'].aggregate(np.mean)

	nboard = pplgrp['nboard'].aggregate(np.mean)
	nboard_sum = pplgrp['nboard'].aggregate(np.sum)
	board_score = pplgrp['board_score'].aggregate(np.mean)

	wingroup = winppl.groupby('name')
	predgroup = predppl.groupby('name')

	### Prepare Data from ML
	winX = wingroup['td', 'lifetime', 'founder_followers', 
                'nfounder', 'founder_score', 
                'ninvestor', 'investor_score', 
                'nboard', 'board_score'].aggregate(np.mean)
	winX['founder_sumfollowers'] = wingroup['founder_followers'].aggregate(np.sum)
	winX['nfounder_sum'] = wingroup['nfounder'].aggregate(np.sum)
	winX['ninvestor_sum'] = wingroup['ninvestor'].aggregate(np.sum)
	winX['nboard_sum'] = wingroup['nboard'].aggregate(np.sum)
	winX['seed_amount'] = np.log10(wingroup['seed_amount'].aggregate(np.sum))
	winyC = pd.Series(np.zeros(len(winX)))+1
	winy = np.log10(wingroup['seriesA_amount'].aggregate(np.sum))
	winy[winy == 0] = np.mean(winy) - np.std(winy)

	predX = predgroup['td','lifetime', 'founder_followers', 'nfounder', 'founder_score', 'ninvestor', 'investor_score', 'nboard', 'board_score'].aggregate(np.mean)
	predX['founder_sumfollowers'] = predgroup['founder_followers'].aggregate(np.sum)
	predX['nfounder_sum'] = predgroup['nfounder'].aggregate(np.sum)
	predX['ninvestor_sum'] = predgroup['ninvestor'].aggregate(np.sum)
	predX['nboard_sum'] = predgroup['nboard'].aggregate(np.sum)

	predX['seed_amount'] = np.log10(predgroup['seed_amount'].aggregate(np.sum))
	predyC = pd.Series(np.zeros(len(predX)))
	predy = np.log10(predgroup['seriesA_amount'].aggregate(np.sum))

	return winX, winy, predX, predy

def run_model(datX, daty): 
	#### Apply Random Forest Classification
	from sklearn.ensemble import RandomForestClassifier as RFC
	from sklearn.ensemble import ExtraTreesClassifier as ETC
	from sklearn.cross_validation import cross_val_score

	rfc1 = RFC(n_estimators=10, max_depth=None, min_samples_split=1, random_state=0)
	etc1 = ETC(n_estimators=10, max_depth=None, min_samples_split=1, random_state=0)

	# Fit 
	datX_scaled = (datX - datX.mean())/datX.std()
	datXfilled = datX_scaled.fillna(0);
	rfc1.fit(datXfilled, daty)
	scRF = cross_val_score(rfc1, datXfilled, daty)
	
	### Random Forest Class prediction and class probability 
	RFC1class = rfc1.predict(datXfilled)
	RFC1prob = rfc1.predict_proba(datXfilled)
	RFC1_probA = RFC1prob[:, 1]
	RFC1acc = sum(RF1class*daty)/len(daty)*100

	# scET = cross_val_score(etc1, datXfilled, daty)
	# etc1.fit(datXfilled, daty)
	
	# ### Extreme Tree Class prediction and class probability 
	# ETC1class = etc1.predict(allXfilled)
	# ETC1prob = etc1.predict_proba(allXfilled)
	# ETC1_probA = ETC1prob[:, 1]
	# ETC1acc = sum(ET1class*ally)/len(ally)*100

	out = datX.copy()
	out['RFCprobA'] = RFC1_probA

	return out

def save_prediction(fpath, fname, d, dy):
	#### save data to csv
	d.to_csv('%s/RFlog_%s.csv' % fpath)
	dy.to_csv('%s%s.csv' % (fpath, fname), header=True, index=False)

def parsedata(out):
	ts = np.median(out.td)
	ps = 0.5

	fpath = "/Users/joytafty1/work/InsightData_Jan6_2014/investwiser/static/predictions/"

	# 1. young companies, high chance
	yh = out[(out['lifetime'] <= ts)&(out['RFCprobA'] >= ps)]
	yh['diffR'] = abs(yh.RFRval - yh.RFRpred)
	yh = yh.sort('diffR', ascending=True)
	yhh = pd.DataFrame(yh.index, yh.diffR)
	yhh.rename(columns={'name' : 'company_name'}, inplace=True)
	cyh = pd.merge(yhh, c, how='inner', on='company_name')

	save_prediction(fpath, "companies_log_class1YH", yh, cyh)


	# 2. mature companies, high chance
	mh = out[(out['lifetime'] > ts)&(out['RFCprobA'] >= ps)]
	mh['diffR'] = abs(mh.RFRval - mh.RFRpred)
	mh = mh.sort('diffR', ascending=True)
	mhh = pd.DataFrame(mh.index)
	mhh.rename(columns={'name' : 'company_name'}, inplace=True)
	cmh = pd.merge(c, mhh, how='inner', on='company_name')

	save_prediction(fpath, "companies_log_class2MH", mh, cmh)

	# # 3. young companies, low chance
	yl = out[(out['lifetime'] <= ts)&(out['RFCprobA'] < ps)]
	yl['diffR'] = abs(yl.RFRval - yl.RFRpred)
	yl = yl.sort('diffR', ascending=True)
	ylh = pd.DataFrame(yl.index)
	ylh.rename(columns={'name' : 'company_name'}, inplace=True)
	cyl = pd.merge(c, ylh, how='inner', on='company_name')

	save_prediction(fpath, "companies_log_class3YL", mh, cmh)

	# # 4. mature companies, low chance
	ml = out[(out['td'] > ts)&(out['RFCprobA'] < ps)]
	ml['diffR'] = abs(ml.RFRval - ml.RFRpred)
	ml = ml.sort('diffR', ascending=True)
	ymh = pd.DataFrame(ml.index)
	ymh.rename(columns={'name' : 'company_name'}, inplace=True)
	cml = pd.merge(c, ymh, how='inner', on='company_name')

	save_prediction(fpath, "companies_log_class4ML", mh, cmh)
	