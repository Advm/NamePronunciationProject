class ngrams:
    def __init__(self, corpus, length):
        self.corpus = corpus
        self.length = length
        self.population = 0
        self.dictionary = {}
        self._generate_ngram_dictionary()
        
    def generate_ngrams(self, str):
        """ Given a string and an n, return a list of all grams of that length"""
        answer = []
        for i in range(0, len(str) - self.length + 1):
            end = i + self.length
            answer.append(str[i:end])
        return answer

    def _generate_ngram_dictionary(self):
        """ Given a list of strings, convert into a dictionary and keep track
        of the number of occurances
        Also keeps track of the number of grams (which is different from the
        number of distinct grams which can get obtained using .len())"""
        population = 0
        mydict = {}
        for str in self.corpus:
            grams = self.generate_ngrams(str)
            for gram in grams:
                population += 1
                if mydict.get(gram) is None:
                    mydict.update({gram: 1})
                else:
                    num = mydict.get(gram)
                    mydict.update({gram: num + 1})
        self.population = population
        self.dictionary = mydict
        return 

# data = ["hello", "world", "Ihope", "thisworks"]
# bi_gram = ngrams(data, 2)

# print(bi_gram.dictionary)
    # def ngrams_word_algorithm(word):
    #     """ Given a word, compute the tri_grams and get the average tri-gram value of the word 
    #         from the corpus """
    #     word_trigrams = self.generate_ngrams(word, 3)
    #     average_trigram_prob = 0
    #     for gram in word_trigrams:
    #         average_trigram_prob += tri_grams.get(gram) / bi_grams.get(gram[:-1])

    #     # To make sure that the word isn't composed completely of tri-grams not found
    #     # in the corpus
    #     if average_trigram_prob != 0:
    #         average_trigram_prob = average_trigram_prob / len(word_trigrams)

    #     return average_trigram_prob 

    # def ngrams_phoneme_algorithm(phoneme):
    #     """ Given a phoneme, compute the z-score from the average of the bi-gram calculations
    #         and convert to a float between 0-1 """
    #     word_bigrams = generate_ngrams(phoneme, 2)

    #     average_bigram_prob = 0
    #     for gram in word_bigrams:
    #         # If the corpus doesn't have this bi-gram, continue on to the next bi-gram.
    #         # Might need to change the weight of this later but for now it seems fine
    #         if bi_grams.get(gram) == None:
    #             continue

    #         average_bigram_prob += bi_grams.get(gram) / un_grams.get(gram[0])
    #         #average_bigram_prob += bi_grams.get(gram) / bi_gram_pop

    #     # To make sure that the word isn't composed completely of bi-grams not found
    #     # in the corpus
    #     if average_bigram_prob != 0:
    #         average_bigram_prob = average_bigram_prob / len(word_bigrams)

    #     z_score = (average_bigram_prob - average_corpus_prob) / standard_deviation

    #     answer = .5 * (math.erf(z_score / 2 ** .5) + 1) # https://stackoverflow.com/questions/2782284/function-to-convert-a-z-score-into-a-percentage

    #     return answer #average_bigram_prob
    #average_corpus_prob = len(bi_grams) / bi_gram_pop
# average_corpus_prob = 0
# for gram in bi_grams:
#     average_corpus_prob += bi_grams.get(gram) / un_grams.get(gram[0])
# average_corpus_prob = average_corpus_prob / bi_gram_pop

# standard_deviation = 0
# for gram in bi_grams:
#     standard_deviation += (bi_grams.get(gram) / un_grams.get(gram[0]) - average_corpus_prob) * (bi_grams.get(gram) / un_grams.get(gram[0]) - average_corpus_prob)
#     #standard_deviation += ((bi_grams.get(gram) / bi_gram_pop) - average_corpus_prob) * ((bi_grams.get(gram) / bi_gram_pop) - average_corpus_prob)
# standard_deviation = standard_deviation / (bi_gram_pop - 1)
# standard_deviation = math.sqrt(standard_deviation)