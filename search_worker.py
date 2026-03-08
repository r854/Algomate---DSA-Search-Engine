"""
search_worker.py
Thin CLI wrapper around query100.py.
Called by server.js via child_process.spawn.
Usage: python search_worker.py "two sum"
Outputs: a JSON array of search result objects to stdout.
"""
import sys
import os
import json

# Suppress NLTK download output (downloaded already)
import nltk
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)

# Make TF_IDF module importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'TF_IDF'))

import query100 as query
import prepare


def main():
    if len(sys.argv) < 2:
        print(json.dumps([]))
        return

    search_query = " ".join(sys.argv[1:])

    # Load data (paths are relative to hackathonapp root)
    base = os.path.dirname(__file__)
    clean_doc = query.load_documents(os.path.join(base, 'TF_IDF', 'clean_doc.pkl'))
    inverted_index = query.load_inverted_index(os.path.join(base, 'TF_IDF', 'inverted_index.pkl'))
    questions = query.load_question_details(os.path.join(base, 'filtering', 'FreeLeetcode.json'))

    # Preprocess query
    query_terms = prepare.preprocess_text_string(search_query)

    # Calculate ranking
    permutation = query.calculate_sorted_order_of_documents(query_terms, inverted_index, clean_doc)

    # Build result list (top 40)
    results = []
    for score, doc_id in permutation[:40]:
        if score <= 0:
            break
        q = questions[doc_id - 1]
        results.append({
            "name": q.get("name", ""),
            "url": q.get("url", ""),
            "tags": q.get("tags", []) if isinstance(q.get("tags"), list) else [],
            "difficulty": q.get("difficulty", ""),
        })

    print(json.dumps(results))


if __name__ == "__main__":
    main()
