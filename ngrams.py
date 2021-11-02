import csv
class ngrams:
    def __init__(self, corpus, length, occurence_table):
        self.corpus = corpus
        self.length = length
        self.occurence_table = occurence_table
        self.population = 0
        self.dictionary = {}
        self.occurence_dictionary = {}
        self._generate_ngram_dictionary()
        self._generate_occurence_dictionary()

    def _generate_occurence_dictionary(self):
        """Given a occurence file, open and create a dictionary that maps each
        word to the number of times it occurs"""
        count = 0
        with open(self.occurence_table, encoding="utf8") as f:
            for row in csv.reader(f):
                #row[0] is the word, row[1] is the occurence #
                #self.occurence_dictionary[row[0]] = row[1]
                #print(((333333 - count) / 333333))
                self.occurence_dictionary[row[0]] = ((333333 - count) / 333333)
                count += 1
        #print("length of dictionary: ", len(self.occurence_dictionary))
                
        
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
    
    def generate_probability(self, word):
        """ Given a word, compute the average gram probability """
        grams = self.generate_ngrams(word)
        average_gram_probability = 0
        for gram in grams:
            average_gram_probability += self.dictionary.get(gram) / self.population
        
        if average_gram_probability != 0:
            average_gram_probability = average_gram_probability / len(grams)
        return average_gram_probability
    
    def generate_other_probability(self, word):
        """Given a word, scale data with 100 == most occurences"""
        grams = self.generate_ngrams(word)
        max_occurences = max(self.dictionary.values()) / 100
        #print(max(self.dictionary.values()))
        average_gram_probability = 0
        for gram in grams:
            #print(f"{gram}: {self.dictionary[gram]}")
            average_gram_probability += self.dictionary.get(gram) / max_occurences
        
        if average_gram_probability != 0:
            average_gram_probability = average_gram_probability / len(grams)
        return average_gram_probability

    def generate_prob_occurence(self, word):
        """Given a word, call generate_other_probability, and then scale it up
            using the occurence table"""
        probability = self.generate_other_probability(word)
        #currently hard-coding in the highest name in the occurence dictionary (jan)
        #but for beta will hopefully use buckets instead
        if self.occurence_dictionary.get(word) == None:
            #word in not in the occurence dictionary, so no scaling is done
            return probability
        scaler = float(self.occurence_dictionary[word]) #/ int(self.occurence_dictionary["jan"])
        probability += (100 - probability) * scaler
        return probability

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
