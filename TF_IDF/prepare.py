import os
import json
import pandas as pd
import numpy as np
import nltk
import pickle
from nltk.tokenize import word_tokenize

#Download if not in your system , remember it wont download over jio network
nltk.download('punkt')


def load_problem_title(filepath):
    # Load JSON data from LeetcodeUnique.json
    question_names = []
    with open(filepath,'r') as file:
        question_details = json.load(file)    
    
    for question in question_details:
        question_names.append(question["name"])
    return question_names

def test_load_problem_title():
    filepath = 'FreeLeetcode.json'
    question_names = load_problem_title(filepath)
    for index, name in enumerate(question_names, start=1):
        print(f"{index}. {name}")

def load_problem_statement(folder):
    documents=[]
    data_path = os.path.join(os.getcwd(), folder)

    for folder_num in range(1,2163):
        folder_path = os.path.join(data_path, str(folder_num))
        file_path = os.path.join(folder_path, str(folder_num) + ".txt")
        
        # Read the contents of the text file
        with open(file_path, "r",encoding="utf-8") as file:
            text = file.read()
        
        # Perform further processing with the text
        # (e.g., tokenize, preprocess, etc.)
        documents.append(text)
    df = pd.DataFrame(documents,columns=['text'])
    return df

def test_load_problem_statement():
    folder = 'QData'
    documents = load_problem_statement(folder)
    #iterate over every document in the list of diocuments and print it word-by-word
    for index,document in enumerate(documents['text'],start=1):
        words = document.split()
        print("Words in document %d: %s\n" %(index,words))
    
def merge_title_with_statement(question_names,df):
    # Append each row of the DataFrame with the corresponding string from the list MULTIPLE TIMES
    # This acts as a powerful title keyword boost for the BM25 algorithm.
    df['text'] = [f'{" ".join([string]*15)} {text}' for text, string in zip(df['text'], question_names)]
    return df

def test_merge():
    filepath = 'FreeLeetcode.json'
    folder = 'QData'
    question_names = load_problem_title(filepath)
    documents = load_problem_statement(folder)
    modified_documents = merge_title_with_statement(question_names,documents)
    for index,document in enumerate(modified_documents['text'],start=1):
        words = document.split()
        print("Words in document %d: %s\n" %(index,words))

def prepare_documents():
    filepath = 'filtering/FreeLeetcode.json'
    folder = 'QData'
    question_names = load_problem_title(filepath)
    documents = load_problem_statement(folder)
    modified_documents = merge_title_with_statement(question_names,documents)
    return modified_documents

def preprocess_text_string(text):
    
    # Convert to lowercase
    text = text.lower()
    
    # Tokenization
    tokens = word_tokenize(text)
    
    # Remove non-alphanumeric tokens
    tokens = [token for token in tokens if token.isalnum()]

    # Remove numbers that are standalone
    tokens = [token for token in tokens if not token.isdigit()]

    # Remove single-character tokens
    tokens = [token for token in tokens if len(token) > 1]

    return tokens

def preprocess_documents(df):
    #TODO : every preprocessing will happen in each row of df and will be stored there
    
    #trimming the sample testcase ,explanations etc
    df['text'] = df['text'].str.split('Example', n=1, expand=True)[0].str.strip()

    # Apply preprocessing to the dataframe
    df['text'] = df['text'].apply(preprocess_text_string)

    return df
   
def create_vocab(df):
    
    all_words = [word for doc in df['text'] for word in doc]
    vocab = sorted(set(all_words))
    return vocab

from typing import Dict, List, Tuple

def create_invertedIndex(df) -> Dict[str, List[Tuple[int, int]]]:
    #TODO token --->{ (doc1,freq1),(doc2,freq2),(doc3,freq3),(doc4,freq4)}
    inverted_index: Dict[str, List[Tuple[int, int]]] = {}
    for idx, document in enumerate(df['text'], start=1): 
        word_freq: Dict[str, int] = {}
        for word in document:   # frequency of all words in a document
            w = str(word)
            word_freq[w] = word_freq.get(w, 0) + 1
        
        for w, freq in word_freq.items():  #append the frequency of the word the word's list 
            inverted_index.setdefault(w, []).append((idx, freq))
            
    return inverted_index

#storing in files

def store_documents(df,filepath):
        # Store the DataFrame in a pickle file
    with open(filepath, 'wb') as file:
        pickle.dump(df, file)
    # Convert the DataFrame to a string representation
    df_str = df.to_string(header=False, index=False)
    
def store_vocab(vocab,filepath):

    # Save the list to a file
    with open(filepath, 'wb') as f:
        pickle.dump(vocab, f)

def store_inverted_index(inv_indx,file_path):
    # # Assuming 'vocab' is your vocabulary object
    with open(file_path, 'wb') as f:
        pickle.dump(inv_indx, f)

def main():
    documents = prepare_documents()
    store_documents(documents,'TF_IDF/unclean_doc.pkl')

    cleaned_documents = preprocess_documents(documents)
    store_documents(cleaned_documents,'TF_IDF/clean_doc.pkl')

    vocab = create_vocab(cleaned_documents)
    print (vocab)
    print(len(vocab))
    store_vocab(vocab,'TF_IDF/vocab.pkl')

    inv_indx = create_invertedIndex(cleaned_documents)
    store_inverted_index(inv_indx,'TF_IDF/inverted_index.pkl')
    
if __name__ == "__main__":
    main()
