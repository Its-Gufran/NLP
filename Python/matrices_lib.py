import requests
from bs4 import BeautifulSoup
import re
from collections import Counter
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import numpy as np

Sports_URLs = ['https://en.wikipedia.org/wiki/Football',
               'https://en.wikipedia.org/wiki/Cricket',
               'https://en.wikipedia.org/wiki/Badminton',
               'https://en.wikipedia.org/wiki/Basketball',
               'https://en.wikipedia.org/wiki/Hockey']

Education_URLs = ['https://en.wikipedia.org/wiki/School',
                  'https://en.wikipedia.org/wiki/College',
                  'https://en.wikipedia.org/wiki/University',
                  'https://en.wikipedia.org/wiki/Professor',
                  'https://en.wikipedia.org/wiki/Teacher']

def get_page_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return None
    
def clean_text(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    text_content = re.sub(r'<.*?>', '', soup.get_text(separator=' ', strip=True))
    text_content = re.sub(r'[^a-zA-Z\s]', '', text_content)
    text_content = re.sub(r'\s+', ' ', text_content)
    return text_content

def get_text_from_urls(url_list):
    text_content = []
    for url in url_list:
        content = get_page_content(url)
        if content:
            cleaned_content = clean_text(content)
            text_content.append(cleaned_content)
        else:
            text_content.append("")  # Append an empty string if content retrieval fails
    return text_content

# Get sports and education content
sports_content = get_text_from_urls(Sports_URLs)
education_content = get_text_from_urls(Education_URLs)

# Combine sports and education content
combined_content = sports_content + education_content

# Labels for sports and education
sports_labels = ['Sports'] * len(sports_content)
education_labels = ['Education'] * len(education_content)
combined_labels = sports_labels + education_labels

# Unigram matrix
vectorizer = CountVectorizer()
X_unigram = vectorizer.fit_transform(combined_content)
unigram_feature_names = vectorizer.get_feature_names_out()
unigram_df = pd.DataFrame(X_unigram.toarray(), columns=unigram_feature_names)

# Bigram matrix
vectorizer_bigram = CountVectorizer(ngram_range=(2, 2))
X_bigram = vectorizer_bigram.fit_transform(combined_content)
bigram_feature_names = vectorizer_bigram.get_feature_names_out()
bigram_df = pd.DataFrame(X_bigram.toarray(), columns=bigram_feature_names)

# TF-IDF matrix
tfidf_transformer = TfidfTransformer()
X_tfidf = tfidf_transformer.fit_transform(X_unigram)
tfidf_df = pd.DataFrame(X_tfidf.toarray(), columns=unigram_feature_names)

# Add labels to DataFrames
unigram_df['category'] = combined_labels
bigram_df['category'] = combined_labels
tfidf_df['category'] = combined_labels

# Print or use DataFrames as needed
print("Unigram Matrix:")
print(unigram_df.head())

print("\nBigram Matrix:")
print(bigram_df.head())

print("\nTF-IDF Matrix:")
print(tfidf_df.head())
