import pickle
import math
import numpy as np
import json

def load_inverted_index(filepath):
    with open(filepath, 'rb') as f:
        return pickle.load(f)

def load_documents(filepath):
    with open(filepath, 'rb') as file:
        return pickle.load(file)

def load_question_details(filepath):
    with open(filepath,'r') as file:
        questions = json.load(file)
    return questions

inv_idx = load_inverted_index('TF_IDF/inverted_index.pkl')
docs = load_documents('TF_IDF/clean_doc.pkl')
questions = load_question_details('filtering/FreeLeetcode.json')
total_docs = len(docs)

query_terms = ['two', 'sum']
score = []
for term in query_terms:
    tf_list = [0.0] * total_docs
    df = len(inv_idx.get(term, []))
    idf = math.log((total_docs + 1) / (df + 1)) + 1
    if term in inv_idx:
        for doc_term, freq in inv_idx[term]:
            if 1 <= doc_term <= total_docs:
                tf_list[doc_term - 1] = 1 + math.log(freq) if freq > 0 else 0.0
    tf_idf_scores = [tf * idf for tf in tf_list]
    score.append(tf_idf_scores)

score = np.array(score)

avg_scores = np.sum(score, axis=0) / len(query_terms)
sorted_docs_current = sorted([(float(avg), doc_id) for doc_id, avg in enumerate(avg_scores, start=1)], key=lambda x: x[0], reverse=True)
print('Current Top 10 for "two sum":')
for score_val, doc_id in sorted_docs_current[:10]:
    print(f'Doc {doc_id} | Score {score_val:.2f} | {questions[doc_id-1]["name"]}')

matched_terms = np.sum(score > 0, axis=0)
boosted_scores = avg_scores * matched_terms
sorted_docs_boosted = sorted([(float(s), doc_id) for doc_id, s in enumerate(boosted_scores, start=1)], key=lambda x: x[0], reverse=True)
print('\nBoosted Top 10 for "two sum" (score * matched_terms):')
for score_val, doc_id in sorted_docs_boosted[:10]:
    tf_two = score[0][doc_id-1]
    tf_sum = score[1][doc_id-1]
    print(f'Doc {doc_id} | Boosted {score_val:.2f} | two:{tf_two:.2f} sum:{tf_sum:.2f} | {questions[doc_id-1]["name"]}')
