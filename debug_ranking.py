import sys
sys.path.append('TF_IDF')
import pickle
import math
import numpy as np

def load_inverted_index(filepath):
    with open(filepath, 'rb') as f:
        inv_indx = pickle.load(f)
    return inv_indx

def load_documents(filepath):
    with open(filepath, 'rb') as file:
        dataframe = pickle.load(file)
    return dataframe

def load_question_details(filepath):
    import json
    with open(filepath,'r') as file:
        questions = json.load(file)
    return questions

def calculate_sorted_order_of_documents(query_terms, inverted_index, documents):
    import query
    return query.calculate_sorted_order_of_documents(query_terms, inverted_index, documents)

if __name__ == '__main__':
    print("Loading data...")
    clean_doc = load_documents('TF_IDF/clean_doc.pkl')
    inverted_index = load_inverted_index('TF_IDF/inverted_index.pkl')
    questions = load_question_details('filtering/FreeLeetcode.json')
    
    query_terms = ['two', 'sum']
    print(f"Tokens: {query_terms}")
    
    permutation = calculate_sorted_order_of_documents(query_terms, inverted_index, clean_doc)
    
    print(f"Top 10 raw results:")
    for score, doc_id in permutation[:10]:
        try:
            url = questions[doc_id-1]['url']
        except:
            url = "ERR"
        print(f"Doc {doc_id}, Score: {score:.4f}, URL: {url}")
