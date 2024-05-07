# Reading from files
# with open('1.txt', 'r') as file:
#     content = file.read()
#     print(content)

# "It removes preceding and trailing spaces from the content. Remove all grammatical errors from this."
# with open('1.txt', 'r') as file1:
#     for line in file1:
#         print(line.strip())

# Reading from URLs
import requests

def fetch_URLs(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        Print("Error while fetching content")
        return None

url = input("Enter URL")

content = fetch_URLs(url)
# print(content) 

# Preprocessing the fetched content
from bs4 import BeautifulSoup
import re
def clean_content(content):
    soup = BeautifulSoup(content, 'html.parser')
    text_content = re.sub(r'<.*?>', '', soup.get_text(separator=' ', strip='True')) #HTML tags n all are replace by "empty string"
    # text_content = re.sub(r'[^a-zA-Z\s]', '', text_content) # other than a-z/A-Z to "empty string"
    # text_content = re.sub(r'\s+',' ', text_content) #new line to " "
    return text_content

cleaned_text = clean_content(content)
# print(cleaned_text)

# Writing to files
def write_to_file(cleaned_text, filename = "2.txt"):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(cleaned_text)

# write_to_file(cleaned_text)

# Tokenize the content
import nltk

def word_tokenize(content):
    tokens = nltk.word_tokenize(content)
    unique_words = list(set(tokens))
    return unique_words

# unique_words = word_tokenize(cleaned_text)
# print(unique_words)


# Sent_tokenize
def prepare_sentence_list(text):
    sentences = nltk.sent_tokenize(text)
    return sentences

# sent_tokens = prepare_sentence_list(cleaned_text)
# print(sent_tokens)


# Paragraph_tokenize

soup = BeautifulSoup(content, 'html.parser')

# for data in soup.find_all("p"):
    # print(data.get_text())

# Anchor tags

for data in soup.find_all("a"):
    print(data["href"])


