import os
import json
from datetime import datetime

from elasticsearch import Elasticsearch
from elasticsearch import helpers
from elasticsearch import client
from elasticsearch import exceptions
from elasticsearch import exceptions, ImproperlyConfigured, ElasticsearchException

ES_HOST = "127.0.0.1"
ES_PORT = "9200"
BULK_INSERT_SIZE = 1000


es_con = Elasticsearch("http://{0}:{1}".format(ES_HOST,ES_PORT))

def write_to_es(file_name):
    """
    input parmeter : filename
    Write user documents of a logfile into ES
    """
    try:
        # Get file in folder
        log_dir = os.path.join('logs',file_name)
        f = open(log_dir, 'r')
        # read file
        try:
            # Find all indices
            index_client = client.IndicesClient(es_con)
            print index_client
            index_name = 'demo_1'
            #check Index exist or not on list of indices
            if not index_client.exists(index=index_name):
                # create new mapping for new index
                body_dict = {
                          "mappings": {
                            "user": {
                              "dynamic_templates": [
                                {
                                  "string_template": {
                                    "match_mapping_type": "string",
                                    "mapping": {
                                      "index": "not_analyzed",
                                      "type": "string"
                                    },
                                    "match": "*"
                                  }
                                }
                              ]
                            }
                          }
                        }
                # create new index
                index_client.create(index=index_name, body=body_dict)
                # Refresh Index
                index_client.refresh(index=index_name)
            es_doc_list = []
            # get all user doc's one by one from logfile
            for each_dict in f:
                try:
                    user_dict = json.loads(each_dict)
                    uid = int(user_dict['uid'])
                    # Update datetime  of user doc on each action
                    user_dict['updated'] = datetime.now()
                    try:
                        # check user exist or not
                        uid_exists = es_con.exists(index=index_name, doc_type="user", id=uid)
                    except:
                        uid_exists = None

                    if uid_exists:
                        # update user doc
                        es_doc = {
                            "_op_type": "update",
                            "_index": index_name,
                            "_type": "user",
                            "_id": uid,
                            "script" : "ctx._source['name']=name\n ctx._source['age'] = age\n ctx._source['gender'] = gender\n ctx._source['mobile'] = mobile\n ctx._source.events.add(events)\n ctx._source['updated'] = updated",
                            "params" : {
                                            "name": user_dict['name'],
                                            "age": user_dict['age'],
                                            "gender": user_dict['gender'],
                                            "mobile": user_dict['mobile'],
                                            "events" : user_dict['events'],
                                            "updated": user_dict['updated']
                                       }
                        }

                    else:
                        # create new user doc
                        es_doc = {
                            "_index": index_name,
                            "_type": "user",
                            "_id": uid,
                            "_source": user_dict
                        }
                    
                    es_doc_list.append(es_doc)
                    # Insert document on every BULK_INSERT_SIZE 
                    if (len(es_doc_list) == BULK_INSERT_SIZE):
                        helpers.bulk(es_con, es_doc_list)
                        es_doc_list = []

                except ValueError as e:
                    print (e)
                    pass

            # Insert remain documents
            if es_doc_list:
                helpers.bulk(es_con, es_doc_list)
                es_doc_list = []
        
        except (ImproperlyConfigured, ElasticsearchException) as e:
            print (e)
            pass
        f.close()
    except IOError as e:
        print (e)
        pass

def get_all_docs():
    """
    Select all documents in index
    """
    query = { "query" : { "match_all" : {} }}
    doc_list = helpers.scan(es_con,index='demo_1',doc_type="user",query=query)
    for each_doc in doc_list:
        print each_doc

def main():
    try:
        # Find all log files from a logs folder with sort by filename
        input_file_list = sorted([file for file in os.listdir('logs') if file.endswith("log")])
        for each_log in input_file_list:
            write_to_es(each_log)
    except OSError as e:
        print (e)
        pass
    #get_all_docs()






if __name__ == "__main__":
    main()