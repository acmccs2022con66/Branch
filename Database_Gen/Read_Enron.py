import os
import pdb
import pymongo
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

def write_into_database(data_list,i):
	global keywords_acc,insert_list,cnt
	keywords_list = []
	for keywords in data_list:
		keywords_acc[keywords]+=1
		if keywords not in keywords_list:
			keywords_list.append(keywords)
		insert_list.append({"fid":'F'+str(i),"kset":keywords_list})
		cnt = cnt+1
		if cnt != 0 and cnt% 1000 == 0:
			mydata.insert_many(insert_list)
			insert_list = []

if __name__ == '__main__':
	rootdir = './stem'
	ls = os.listdir(rootdir)
	keywords_acc = defaultdict(int)
	insert_list = []
	cnt = 0
	Setup_DB('Enron_all_documents')
	for i in range(0, len(ls)):
		stemname = os.path.join(rootdir, ls[i])
		print(stemname)
		if os.path.isfile(stemname):
			infile = open(stemname, 'r' , errors='ignore')
			data_list = []
			while True:
				output = ''
				line = infile.readline()
				if line == '':
					break
				if line == '\n':
					continue
				line = line.rstrip().split(" ")
				line_no = []
				for x in line:
					if x == '':
						continue
					line_no.append(x)
				data_list += line_no
			infile.close()
			write_into_database(data_list,i)
	if len(insert_list) > 0:
		mydata.insert_many(insert_list)
	print(sort_by_value(keywords_acc,400))


