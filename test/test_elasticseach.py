from elasticsearch import Elasticsearch
es = Elasticsearch('https://localhost:9200')

es.index(index='my_index',doc_type='my_index',id=1,body={'test':'this is a test'})
es.index(index='my_index',doc_type="my_index",id=2,body={'test2','this is second test'})

res1 = es.search(index='my_index',doc_type='my_index',
                body={'query':{'match':{'test':'this test'}}})

print(res1)