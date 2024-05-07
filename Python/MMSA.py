import nltk
# nltk.download('words')

from nltk.corpus import words

# Load English words from the nltk corpus
english_words = set(words.words())

# Input text
input_text = "Thisisagoodplacetolive"

# Tokens list
tokens = []

i = 0
while i < len(input_text):
    max_word = ""
    # Try to find the longest word from the dictionary
    for j in range(i, len(input_text)):
        temp = input_text[i:j+1]
        # If the word is in the English words set and longer than the previous max_word
        if temp in english_words and len(temp) > len(max_word):
            max_word = temp
    # If no valid word is found, add the single character as token
    if max_word == "":
        max_word = input_text[i]
    # Move the pointer to the end of the matched word
    i += len(max_word)
    # Append the matched word to tokens list
    tokens.append(max_word)
        
print(tokens)


# Testing accuracy 
lowercaseCorpus = set(word.lower() for word in words.words())

test_cases = [
    ("thisisinsaneandthatwasnotialwayswantedtogotodelhiandmyfrienddoesnot",
     ["this", "is", "in", "sane", "and", "that", "was", "not", "i", "always", "wanted", "to", "go", "to", "delhi", "and", "my", "friend", "does", "not"])
]

total_words = 0
correct_words = 0

for string, expected_words in test_cases:
    tokens = []
    i = 0
    while i < len(string):
        maxWord = ""
        for j in range(i, len(string)):
            tempWord = string[i:j+1]
            if tempWord in lowercaseCorpus and len(tempWord) > len(maxWord):
                maxWord = tempWord
        i = i+len(maxWord)
        tokens.append(maxWord)

    total_words += len(expected_words)
    correct_words += sum(1 for word in tokens if word in expected_words)

accuracy = (correct_words / total_words) * 100
print("Accuracy: {:.2f}%".format(accuracy))

