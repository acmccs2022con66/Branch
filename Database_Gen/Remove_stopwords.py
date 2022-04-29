import pymongo
import nltk
import sys
import re
from collections import defaultdict
def Read_DB(test_db_name):
	global myclient,mydb,mydataread,mydatawrite,mytask_search,mytask_derive
	myclient = pymongo.MongoClient("mongodb://localhost:27017/")
	mydb = myclient[test_db_name]
	mydataread = mydb["id_keywords"]
	mydatawrite = mydb["id_keywords_filter"]
	mydatawrite.drop()
def sort_by_value(d,hip): 
	items=d.items()     
	backitems=[[v[1],v[0]] for v in items] 
	backitems.sort(reverse = True) 
	return [ (backitems[i][1],backitems[i][0]) for i in range(0,hip)] 
def remove_punctuation(line):
    rule = re.compile(r"[^a-zA-Z0-9\u4e00-\u9fa5]")
    line = rule.sub('',line)
    return line
if __name__ == '__main__':
	test_db_name = str(sys.argv[1])
	Read_DB(test_db_name)
	keywords_acc = defaultdict(int)
	stopwords = set(nltk.corpus.stopwords.words('english'))
	insert_list = []
	cnt = 0
	for x in mydataread.find({}):
		fl = [element.lower() for element in x["kset"] if element.lower() not in stopwords and remove_punctuation(element)!='' and element.find('\'s')==-1 and element!='']
		fl = list(set(fl))
		for element in fl:
			keywords_acc[element]+=1
		fll = [str(hash(element)) for element in fl]
		if len(fll) == 0:
			continue
		insert_list.append({"fid":x["fid"],"kset":fll})
		cnt = cnt+1
		if cnt != 0 and cnt% 10000 == 0:
			print(cnt)
			mydatawrite.insert_many(insert_list)
			insert_list = []
	if len(insert_list) > 0:
		mydatawrite.insert_many(insert_list)
	print(sort_by_value(keywords_acc,1000))	



