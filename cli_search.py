import sys
import os
sys.path.append(os.path.dirname(__file__))

import nltk
nltk.download('punkt_tab')

from TF_IDF.query100 import return_search_result

if __name__ == "__main__":
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = input("Enter your search query: ")
    
    results = return_search_result(query)
    if isinstance(results, str):
        print(results)
    else:
        for i, result in enumerate(results, 1):
            print(f"{i}. {result.get('name', 'No name')} - {result.get('difficulty', 'Unknown')}")
            print(f"   URL: {result.get('url', 'N/A')}")
            print()