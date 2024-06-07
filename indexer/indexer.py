import csv
import json
from elasticsearch import Elasticsearch, helpers

index_name = 'webtoons'
csv_file_path = 'data/naver.csv'
mapping_file_path = 'settings/mapping.json'

def create_client(): 
    return Elasticsearch('http://localhost:9200')

def create_index(client, index_name):
    with open(mapping_file_path, 'r') as f:
        mapping = json.load(f)
    client.indices.create(index=index_name, body=mapping)

def create_docs():
    bulk_docs = []
    with open(csv_file_path, 'r') as f:
        csv_reader = csv.reader(f)
        for line in csv_reader:
            if line[0] == 'id':
                continue
            j = {
                'id': line[0],
                'title': line[1],
                'author': line[2],
                'genre': line[3],
                'description': line[4],
                'rating': line[5],
                'date': line[6],
                'completed': True if line[7] == 'TRUE' else False,
                'age': line[8],
                'free': True if line[9] == 'TRUE' else False,
                'link': line[10]
            }
            bulk_docs.append({
                '_index': index_name,
                '_id': line[0],
                '_source': j
            })
    return bulk_docs

if __name__ == "__main__":
    es_client = create_client()
    create_index(client=es_client, index_name=index_name)
    bulk_docs = create_docs()
    helpers.bulk(es_client, bulk_docs)
