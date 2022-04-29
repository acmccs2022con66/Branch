import os
import pdb
import pymongo
import sys
import nltk
import json
import string
from collections import defaultdict
def Setup_DB(test_db_name):
	global myclient,mydb,mydata,mytask_search,mytask_derive
	myclient = pymongo.MongoClient("mongodb://localhost:27017/")
	mydb = myclient[test_db_name]
	mydata = mydb["id_keywords"]
	mydata.drop()
def sort_by_value(d,hip): 
	items=d.items()     
	backitems=[[v[1],v[0]] for v in items] 
	backitems.sort(reverse = True) 
	return [ backitems[i][1] for i in range(0,hip)] 
def write_into_database(data_list):
	global keywords_acc,insert_list,cnt
	keywords_list = []
	for keywords in data_list:
		keywords_acc[keywords]+=1
		if keywords not in keywords_list:
			keywords_list.append(keywords)
	insert_list.append({"fid":'F'+str(cnt),"kset":keywords_list})
	cnt = cnt+1
	if cnt != 0 and cnt% 1000 == 0:
		mydata.insert_many(insert_list)
		insert_list = []
if __name__ == '__main__':
	rootdir = './wikidata'
	lsb  = os.listdir(rootdir)
	Setup_DB('Wikipedia')
	keywords_acc = defaultdict(int)
	insert_list = []
	cnt = 0
	document_count=0
	punct = set(string.punctuation)
	for flo in range(0, len(lsb)):
		floname = os.path.join(rootdir, lsb[flo])
		ls = os.listdir(floname)
		print (floname)
		for i in range(0, len(ls)):
			filename = os.path.join(floname,ls[i])
			if os.path.isfile(filename):
				fp = open (filename,'r', errors = 'ignore' )
				while 1:
					line = fp.readline()
					if line =='':
						break
					json_data = json.loads(line)
					data_list = nltk.word_tokenize(json_data['text'])
					data_list.append(json_data['title'])
					data_list = list(set(data_list))
					data_list = [element for element in data_list if element not in punct]
					write_into_database(data_list)
					document_count+=1
					if document_count == 2000000:
						break
				fp.close()
			if document_count == 2000000:
				break
		if document_count == 2000000:
			break
	if len(insert_list) > 0:
		mydata.insert_many(insert_list)
	print(sort_by_value(keywords_acc,800))

