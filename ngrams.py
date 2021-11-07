import csv
class ngrams:
    def __init__(self, length, corpus="ipa_dicts/english-general_american.csv", occurence_table="unigram_freq.csv"):
        self.length = length
        self.corpus = corpus
        self.occurence_table = occurence_table
        self.letter_dictionary = {}
        self.phoneme_dictionary = {}
        self.letter_occurence_dictionary = {}
        self.phoneme_occurence_dictionary = {}
        self._generate_ngram_dictionaries()
        self._generate_occurence_dictionaries()
    
    def _generate_occurence_dictionaries(self):
        """ Opens and creates dictionaries that map each word/phoneme to how often it occurs
            (most is 1, least is 0)"""
        count = 0
        with open(self.occurence_table, encoding="utf8") as f:
            for row in csv.reader(f):
                #hard coded the lengths of the occurence dictionaries, will need to change later 
                #if user wants to provide their own
                self.letter_occurence_dictionary[row[0]] = ((333333 - count) / 333333)

                if self.phoneme_occurence_dictionary.get(row[1]) != None:
                    #this is done because there are a lot of words that are pronounced
                    #the same, but spelled differently
                    count += 1
                    continue
                self.phoneme_occurence_dictionary[row[1]] = ((333333 - count) / 333333)
                count += 1

    def generate_ngrams(self, str):
        """ Given a string and an n, return a list of all grams of that length"""
        answer = []
        for i in range(0, len(str) - self.length + 1):
            end = i + self.length
            answer.append(str[i:end])
        return answer

    def _generate_ngram_dictionaries(self):
        """ Generates the dictionaries for both letters and phonemes, keeping track of
            the total occurences"""
        with open(self.corpus, encoding="utf8") as f:
                letter_corpus = [w[1:-1] for row in csv.reader(f) \
                for w in row[0].split(', ')]
        with open(self.corpus, encoding="utf8") as f:       
                phoneme_corpus = [w[1:-1] for row in csv.reader(f) \
                for w in row[1].split(', ')]

        for str in letter_corpus:
            letter_grams = self.generate_ngrams(str)         
            for gram in letter_grams:
                if self.letter_dictionary.get(gram) is None:
                    self.letter_dictionary.update({gram: 1})
                else:
                    num = self.letter_dictionary.get(gram)
                    self.letter_dictionary.update({gram: num + 1})

        for str in phoneme_corpus:
            phoneme_grams = self.generate_ngrams(str)
            for gram in phoneme_grams:
                if self.phoneme_dictionary.get(gram) is None:
                    self.phoneme_dictionary.update({gram: 1})
                else:
                    num = self.phoneme_dictionary.get(gram)
                    self.phoneme_dictionary.update({gram: num + 1})
   
        return 

    def generate_dictionary_letter_probability(self, word):
        """ Given a word, scale data with 100 == most occurences in the dictionary,
            not to be confused with the occurence csv"""
        grams = self.generate_ngrams(word)
        max_occurences = max(self.letter_dictionary.values()) / 100
        average_gram_probability = 0
        for gram in grams:
            if self.letter_dictionary.get(gram) == None:
                #if the gram is not in the dictionary, treat it as zero to avoid
                #dividing NoneType
                continue
            average_gram_probability += self.letter_dictionary.get(gram) / max_occurences
            
        if average_gram_probability != 0:
            average_gram_probability = average_gram_probability / len(grams)
        return average_gram_probability

    def generate_dictionary_phoneme_probability(self, word):
        """ Given a phoneme, scale data with 100 == most occurences in the dictionary,
            not to be confused with the occurence csv"""
        grams = self.generate_ngrams(word)
        max_occurences = max(self.phoneme_dictionary.values()) / 100
        average_gram_probability = 0
        for gram in grams:
            if self.phoneme_dictionary.get(gram) == None:
                #if the gram is not in the dictionary, treat it as zero to avoid
                #dividing NoneType
                continue
            average_gram_probability += self.phoneme_dictionary.get(gram) / max_occurences
            
        if average_gram_probability != 0:
            average_gram_probability = average_gram_probability / len(grams)
        return average_gram_probability

    def generate_letter_prob_occurence(self, word):
        """ Given a word, call generate_dictionary_letter_probability, and then scale it up
            using the letter occurence table"""
        probability = self.generate_dictionary_letter_probability(word)
        if self.letter_occurence_dictionary.get(word) == None:
            #word is not in the occurence dictionary, so no scaling is done
            return probability
        scaler = float(self.letter_occurence_dictionary[word]) 
        probability += (100 - probability) * scaler
        return probability

    def generate_phoneme_prob_occurence(self, phoneme):
        """ Given a phoneme, call generate_dictionary_phoneme_probability, and then scale it up
            using the phoneme occurence table"""
        probability = self.generate_dictionary_phoneme_probability(phoneme)
        if self.phoneme_occurence_dictionary.get(phoneme) == None:
            #phoneme is not in the occurence dictionary, so no scaling is done
            return probability
        scaler = float(self.phoneme_occurence_dictionary[phoneme]) 
        probability += (100 - probability) * scaler
        return probability




# def generate_probability(self, word):
#     """ Given a word, compute the average gram probability """
#     grams = self.generate_ngrams(word)
#     average_gram_probability = 0
#     for gram in grams:
#         average_gram_probability += self.dictionary.get(gram) / self.population
    
#     if average_gram_probability != 0:
#         average_gram_probability = average_gram_probability / len(grams)
#     return average_gram_probability

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
