import numpy as np
import pandas as pd
from collections import defaultdict 

corpus = ["The cat chased the mouse", "The dog chased the cat", "The mouse ran away from the cat"]

window_size = 2
vocab = set()
context_matrix = defaultdict(list)


for line in corpus:
    for word in line.split(' '):
        vocab.add(word)

df = pd.DataFrame(index=list(vocab), columns=list(vocab));
df = df.fillna(0)

# print(df)

for line in corpus:
    words = line.split(' ')
    for idx, word in enumerate(words):
        l = idx - window_size
        r = idx + window_size + 1
        if l < 0:
            l = 0
        if r >= len(words):
            r = len(words)
        for i in range(l, r):
            # print(i, word, words[i])
            if word != words[i]:
                df[word][words[i]] += 1

print(df)

word1 = "cat"; word2 = "dog"

r1 = df.index.get_loc(word1)
r2 = df.index.get_loc(word2)

sum = 0
sum_sq1 = 0; sum_sq2 = 0

for idx, score in enumerate(df[word1]):
    # print(idx, score, df.iloc[r2, idx])
    sum += score * df.iloc[r2, idx]
    sum_sq1 += score * score
    sum_sq2 += df.iloc[r2, idx] * df.iloc[r2, idx]

cos_similarity = sum / (np.sqrt(sum_sq1) * np.sqrt(sum_sq2))

print("Similarity between ", word1, " and ", word2, " is: ", cos_similarity)