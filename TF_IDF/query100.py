import math
import json
import numpy as np
import pickle
import prepare
import pandas as pd


def preprocess_query_string():
    query = input("What you wan't to search ?")
    query_tokens = prepare.preprocess_text_string(query)
    return query_tokens

def load_vocab(filepath):
        # Load the list from the file
    with open(filepath, 'rb') as f:
        vocab = pickle.load(f)
    return vocab

def load_inverted_index(filepath):
        # Load the dict from the file
    with open(filepath, 'rb') as f:
        inv_indx = pickle.load(f)
    return inv_indx

def load_documents(filepath):
        # Load the DataFrame from the pickle file
    with open(filepath, 'rb') as file:
        dataframe = pickle.load(file)
    return dataframe

def load_question_details(filepath):
    with open(filepath,'r') as file:
        questions = json.load(file)
    return questions

def calculate_sorted_order_of_documents(query_terms,inverted_index,documents):
    sorted_documents =[]
    total_terms = len(query_terms)
    total_documents = len(documents)
    
    if total_terms == 0:
        return []

    # BM25 Constants
    k1 = 1.5
    b = 0.75
    
    # BM25 Constants
    k1 = 1.5
    b = 0.75
    
    # Pre-compute document lengths and average document length for BM25
    doc_lengths = [len(doc) for doc in documents['text']]
    avgdl = sum(doc_lengths) / total_documents if total_documents > 0 else 1.0

    #make a list of pair of (score,doc)
    #sort in descending order
    #return the docs with the highest score 
    score = []
    #for each query term calculate a list of tf values against each document
    for term in query_terms:
        tf_list = [0.0] * total_documents
        df = len(inverted_index.get(term, []))

        #calculate the idf value of that term from inverted index
        # using smoothed IDF to prevent ZeroDivisionError if term not in index
        idf = math.log((total_documents + 1) / (df + 1)) + 1

        #check if the given query word is present in vocab(inverted index in our case) or not 
        #if word is present in index calculate tf values against all docs in a tf list
        if term in inverted_index:
            for doc_term, freq in inverted_index[term]:
                if 1 <= doc_term <= total_documents:
                    # BM25 Term Frequency with Document Length Normalization
                    doc_len = doc_lengths[doc_term - 1]
                    tf = (freq * (k1 + 1)) / (freq + k1 * (1 - b + b * (doc_len / avgdl)))
                    tf_list[doc_term - 1] = tf

        #multiply idf of a word with the tf list of that word
        tf_idf_scores = [tf * idf for tf in tf_list]

        #take column average(calculating doc score)
        score.append(tf_idf_scores)

    # Convert to standard numpy array via temporary assignment to avoid static parser bugs
    score_list = list(score)  # type: ignore
    score_arr = np.asarray(score_list)
    avg_scores = np.sum(score_arr, axis=0) / total_terms
    
    # Coordinate Match Boost: Apply a gentle logarithmic multiplier
    # rather than a straight multiplicative boost which distorts BM25.
    matched_terms_count = np.sum(score_arr > 0, axis=0)
    # Give a ~20-30% boost per additional matching term rather than multiplying by 2x/3x
    boost_factor = 1 + (0.25 * (matched_terms_count - 1))
    # Ensure minimum boost is 1
    boost_factor = np.maximum(1.0, boost_factor)
    boosted_scores = avg_scores * boost_factor

    sorted_documents = [(float(score_val), doc_id) for doc_id, score_val in enumerate(boosted_scores, start=1)]
    sorted_documents = sorted(sorted_documents, key=lambda x: x[0], reverse=True)
    return sorted_documents

def return_search_result(permutation):
    index = 0
    questions = load_question_details('filtering/FreeLeetcode.json')
    for score,doc_id in permutation:
       index +=1
       if index<=40:
           print('name = %s, score = %d \n' %(questions[doc_id-1]['url'],score))
       else:
           break

def main():
    clean_doc = load_documents('TF_IDF/clean_doc.pkl')
    inverted_index = load_inverted_index('TF_IDF/inverted_index.pkl')
    query_terms = preprocess_query_string()

    permutation = calculate_sorted_order_of_documents(query_terms,inverted_index,clean_doc)
    return_search_result(permutation)
    
if __name__ == "__main__":
    main()