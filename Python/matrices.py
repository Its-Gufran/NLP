import requests

Sports_URLs = ['https://en.wikipedia.org/wiki/Association_football',
        'https://en.wikipedia.org/wiki/Cricket',
        'https://en.wikipedia.org/wiki/Badminton',
        'https://en.wikipedia.org/wiki/Basketball',
        'https://en.wikipedia.org/wiki/Hockey']

Education_URLs = ['https://en.wikipedia.org/wiki/School',
        'https://en.wikipedia.org/wiki/College',
        'https://en.wikipedia.org/wiki/University',
        'https://en.wikipedia.org/wiki/Professor',
        'https://en.wikipedia.org/wiki/Teacher']

def fetch_URLs(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        print("Unable to fetch")
        return None
    
sports_content = []
education_content = []

for url in Sports_URLs:
    content = fetch_URLs(url)
    if content:
        sports_content.append(content)

for url in Education_URLs:
    content = fetch_URLs(url)
    if content:
        education_content.append(content)

# print(sports_content)

import re
from bs4 import BeautifulSoup
def clean_content(content):
    soup = BeautifulSoup(content, 'html.parser')
    cleaned_content = re.sub(r'<.*?>','',soup.get_text(separator=' ', strip="True"))
    cleaned_content = re.sub(r'^a-zA-Z\s',' ',cleaned_content)
    cleaned_content = re.sub(r'\s+',' ',cleaned_content)
    return cleaned_content

cleaned_sports_content = []
cleaned_education_content = []

for data in sports_content:
    content = clean_content(data)
    cleaned_sports_content.append(content)


for data in education_content:
    content = clean_content(data)
    cleaned_education_content.append(content)

# print(cleaned_education_content)
combined_list = cleaned_sports_content+cleaned_education_content

import pandas as pd

df = pd.DataFrame({
    "text":combined_list,
    "category":["sports"]*len(cleaned_sports_content)+["education"]*len(cleaned_education_content)
})

# print(df)

# Unigram Count Matrix
from collections import Counter
import numpy as np

def unigram_counts(texts):
    unigram_count = Counter()
    for text in texts:
        unigram_count.update(text.split())
    return unigram_count

unigram_counts = unigram_counts(df["text"])

def unigram_count_matrix(texts, unigram_count):
    matrix = np.zeros((len(texts),len(unigram_count)))
    for i, text in enumerate(texts):
        counts = Counter(text.split())
        for j, word in enumerate(unigram_count):
            matrix[i,j] = counts[word]
    return matrix

matrix = unigram_count_matrix(df["text"], unigram_counts)
# print(matrix)
unigram_count_df = pd.DataFrame(matrix, columns = unigram_counts.keys())
# print(unigram_count_df)


# Bigram matrix

def bigram_count(texts):
    bigram_counts = Counter()
    for text in texts:
        words = text.split()
        bigrams = [(words[i],words[i-1]) for i in range(len(words)-1)]
        bigram_counts.update(bigrams)
    return bigram_counts

# bigram_counts = bigram_count(df["text"])
def bigram_matrix(texts,bigram_counts,unigram_count):
    matrix = np.zeros((len(texts),len(bigram_counts)))
    for i, text in enumerate(texts):
        words = text.split()
        bigrams = [(words[i],words[i-1]) for i in range(len(words)-1)]
        for j, bigram in enumerate(bigrams):
            matrix[i,j] = bigram_counts[bigram]/unigram_count[bigram[0]]
    return matrix

# bigram_count_matrix = bigram_matrix(df["text"], bigram_counts ,unigram_counts)
# bigram_count_matrix_df = pd.DataFrame(bigram_count_matrix, columns = bigram_counts.keys())
# print(bigram_count_matrix_df)

# tf-idf matrix 

def get_tf_matrix(texts, unigram_counts):
    matrix = np.zeros((len(texts), len(unigram_counts)))
    for i, text in enumerate(texts):
        counts = Counter(text.split())
        for j, word in enumerate(unigram_counts):
            matrix[i, j] = counts[word]/len(unigram_counts)
    return matrix

tf_matrix = get_tf_matrix(df["text"], unigram_counts)

def get_idf_vector(texts, unigram_counts):
    idf_vector = np.zeros(len(unigram_counts))
    for j, word in enumerate(unigram_counts):
        idf_vector[j] = np.log((len(texts)/sum([1 for text in texts if word in text]))+1)
    return idf_vector

idf_vector = get_idf_vector(df["text"], unigram_counts)

def get_tfidf_matrix(tf_matrix, idf_vector):
    return tf_matrix*idf_vector

tfidf_matrix = get_tfidf_matrix(tf_matrix, idf_vector)

tfidf_df = pd.DataFrame(tfidf_matrix, columns=unigram_counts.keys())
print(tfidf_df)
