import os
import pickle
import pymongo

def Setup_DB(test_db_name):
    global myclient,mydb,mydata,mytask_search,mytask_derive
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["lucene"]
    mydata = mydb["id_keywords"]
    mydata.drop()
def load_dataset(dataset_path):
    if not os.path.exists(dataset_path):
        raise ValueError("The file {} does not exist".format(dataset_path))
    
    with open(dataset_path, "rb") as f:
        doc = pickle.load(f)

    return doc
if __name__ == "__main__":
    Setup_DB("lucene")
    p = './lucene_doc.pkl'
    docs = load_dataset(p)
    cnt = 0
    insert_list = []
    for doc in docs:
            insert_list.append({"fid":'F'+str(cnt),"kset":doc})
            cnt+=1
            if len(insert_list) > 10000:
                    mydata.insert_many(insert_list)
                    insert_list = []
    if len(insert_list) > 10000:
        mydata.insert_many(insert_list)
