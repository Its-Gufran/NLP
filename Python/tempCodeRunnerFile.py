def bigram_count(texts):
    bigram_counts = Counter()
    for text in texts:
        words = text.split()
        bigrams = [(words[i],words[i-1]) for i in range(len(words)-1)]
        bigram_counts.update(bigrams)
    return bigram_counts

bigram_counts = (df["text"])
def bigram_matrix(texts,bigram_counts,unigram_count):
    matrix = np.zeros((len(texts),len(bigram_counts)))
    for i, text in enumerate(texts):
        words = text.split()
        bigrams = [(words[i],words[i-1]) for i in range(len(words)-1)]
        for j, bigram in enumerate(bigram_counts):
            matrix[i,j] = bigram_counts[bigram]/unigram_count[bigram[0]]
    return matrix

bigram_count_matrix = bigram_matrix(df["text"], bigram_counts ,unigram_count)
bigram_count_matrix_df = pd.DataFrame(bigram_count_matrix, coulumns = bigram_counts.keys())
print(bigram_count_matrix_df)