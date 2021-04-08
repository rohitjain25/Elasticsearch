#The python script to add more than one document in the index at time or bulk import of json in the index.

import sys
import json
from pprint import pprint
from elasticsearch import Elasticsearch
es = Elasticsearch(
    ['localhost'],
    port=9200

)

MyFile= open("books_details.json",'r').read()
ClearData = MyFile.splitlines(True)
i=0
json_str=""
docs ={}
for line in ClearData:
    line = ''.join(line.split())
    if line != "},":
        json_str = json_str+line
    else:
        docs[i]=json_str+"}"
        json_str=""
        print(docs[i])
        es.index(index='books_details', doc_type='Blog', id=i, body=docs[i])
        i=i+1
