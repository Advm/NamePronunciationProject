import csv
class NgramManager:
    def __init__(self, *sizes):
        self.grams = [Ngrams(size) for size in sorted(sizes)]
    
    def generateLetterProbs(self, word):
        probs = []
        for gram in self.grams:
            if gram.length >= len(word):
                break
            probs.append(gram.generateDictionaryLetterProb(word))
        return sum(probs) / len(probs)
    
    def generatePhonemeProbs(self, word):
        probs = []
        for gram in self.grams:
            if gram.length >= len(word):
                break
            probs.append(gram.generateDictionaryPhonemeProb(word))
        return sum(probs) / len(probs)

class Ngrams:
    def __init__(self, length, corpus="ipa_dicts/english-general_american.csv", occurence_table="unigram_freq.csv"):
        self.length = length
        self.corpus = corpus
        self.occurence_table = occurence_table
        self.letter_dictionary = {}
        self.phoneme_dictionary = {}
        self.letter_occurence_dictionary = {}
        self.phoneme_occurence_dictionary = {}
        self._generateNgramDictionaries()
        #self._generateOtherOccurrenceDictionaries()
        self._generateOccurrenceDictionaries()

    def _generateOtherOccurrenceDictionaries(self):
        """ Opens and creates dictionaries that map each gram in the occurence dictionary to 
        how often it occurs, (most is 1, least is 0)"""
        print("starting to generate dictionaries")
        with open(self.occurence_table, encoding="utf8") as f:
            for row in csv.reader(f):
                #row[0] is the word, row[1] is the phoneme, row[2] is the occurence value
                letter_grams = self.generateNgrams(row[0])
                phoneme_grams = self.generateNgrams(row[1]) 
                for gram in letter_grams:
                    if self.letter_occurence_dictionary.get(gram) is None:
                        self.letter_occurence_dictionary.update({gram: row[2]})
                    else:
                        num = self.letter_occurence_dictionary.get(gram)
                        self.letter_occurence_dictionary.update({gram: num + row[2]})
                #print("finished letter dictionaries")
                for gram in phoneme_grams:
                    if self.phoneme_occurence_dictionary.get(gram) is None:
                        self.phoneme_occurence_dictionary.update({gram: row[2]})
                    else:
                        num = self.phoneme_occurence_dictionary.get(gram)
                        self.phoneme_occurence_dictionary.update({gram: num + row[2]})
        
        #now we have the dictionaries with the total occurences. sort them from highest to lowest
        # and then scale them
        print("generated non-scaled dictionaries")
        # print(self.letter_occurence_dictionary)
        # print(self.phoneme_occurence_dictionary)
        letter_sorted = sorted(self.letter_occurence_dictionary, key=self.letter_occurence_dictionary.get)
        for i in range(len(self.letter_occurence_dictionary)):
            self.letter_occurence_dictionary.update({letter_sorted[i]: ((i + 1) / len(self.letter_occurence_dictionary))})

        phoneme_sorted = sorted(self.phoneme_occurence_dictionary, key=self.phoneme_occurence_dictionary.get)
        for i in range(len(self.phoneme_occurence_dictionary)):
            self.phoneme_occurence_dictionary.update({phoneme_sorted[i]: ((i + 1) / len(self.phoneme_occurence_dictionary))})

        print("dont think we get here")
        return

    def _generateOccurrenceDictionaries(self):
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

    def generateNgrams(self, str):
        """ Given a string and an n, return a list of all grams of that length"""
        answer = []
        for i in range(0, len(str) - self.length + 1):
            end = i + self.length
            answer.append(str[i:end])
        return answer

    def _generateNgramDictionaries(self):
        """ Generates the dictionaries for both letters and phonemes, keeping track of
            the total occurences"""
        with open(self.corpus, encoding="utf8") as f:
                letter_corpus = [w[1:-1] for row in csv.reader(f) \
                for w in row[0].split(', ')]
        with open(self.corpus, encoding="utf8") as f:       
                phoneme_corpus = [w[1:-1] for row in csv.reader(f) \
                for w in row[1].split(', ')]

        for str in letter_corpus:
            letter_grams = self.generateNgrams(str)         
            for gram in letter_grams:
                if self.letter_dictionary.get(gram) is None:
                    self.letter_dictionary.update({gram: 1})
                else:
                    num = self.letter_dictionary.get(gram)
                    self.letter_dictionary.update({gram: num + 1})

        for str in phoneme_corpus:
            phoneme_grams = self.generateNgrams(str)
            for gram in phoneme_grams:
                if self.phoneme_dictionary.get(gram) is None:
                    self.phoneme_dictionary.update({gram: 1})
                else:
                    num = self.phoneme_dictionary.get(gram)
                    self.phoneme_dictionary.update({gram: num + 1})
   
        return 

    def generateDictionaryLetterProb(self, word):
        """ Given a word, scale data with 100 == most occurences in the dictionary,
            not to be confused with the occurence csv"""
        grams = self.generateNgrams(word)
        max_occurences = max(self.letter_dictionary.values()) / 100
        average_gram_prob = 0
        for gram in grams:
            if self.letter_dictionary.get(gram) == None:
                #if the gram is not in the dictionary, treat it as zero to avoid
                #dividing NoneType
                continue
            average_gram_prob += self.letter_dictionary.get(gram) / max_occurences
            
        if average_gram_prob != 0:
            average_gram_prob = average_gram_prob / len(grams)
        return average_gram_prob

    def generateDictionaryPhonemeProb(self, word):
        """ Given a phoneme, scale data with 100 == most occurences in the dictionary,
            not to be confused with the occurence csv"""
        grams = self.generateNgrams(word)
        max_occurences = max(self.phoneme_dictionary.values()) / 100
        average_gram_prob = 0
        for gram in grams:
            if self.phoneme_dictionary.get(gram) == None:
                #if the gram is not in the dictionary, treat it as zero to avoid
                #dividing NoneType
                continue
            average_gram_prob += self.phoneme_dictionary.get(gram) / max_occurences
            
        if average_gram_prob != 0:
            average_gram_prob = average_gram_prob / len(grams)
        return average_gram_prob

    def generateLetterProbOccurence(self, word):
        """ Given a word, call generateDictionaryLetterProb, and then scale it up
            using the letter occurence table"""
        prob = self.generateDictionaryLetterProb(word)
        if self.letter_occurence_dictionary.get(word) == None:
            #word is not in the occurence dictionary, so no scaling is done
            return prob
        scaler = float(self.letter_occurence_dictionary[word]) 
        prob += (100 - prob) * scaler
        return prob

    def generatePhonemeProbOccurence(self, phoneme):
        """ Given a phoneme, call generateDictionaryPhonemeProb, and then scale it up
            using the phoneme occurence table"""
        prob = self.generateDictionaryPhonemeProb(phoneme)
        if self.phoneme_occurence_dictionary.get(phoneme) == None:
            #phoneme is not in the occurence dictionary, so no scaling is done
            return prob
        scaler = float(self.phoneme_occurence_dictionary[phoneme]) 
        prob += (100 - prob) * scaler
        return prob


# def generateLetterProbOccurence(self, word):
#         """ Given a word, call generateDictionaryLetterProb, and then scale it up
#             using the letter occurence table"""
        # prob = self.generateDictionaryLetterProb(word)
        # average_scaler = 0
        # for gram in self.generateNgrams(word):
        #     if self.letter_occurence_dictionary.get(gram) == None:
        #         continue
        #     average_scaler += float(self.letter_occurence_dictionary[gram])
        # if average_scaler != 0:
        #     average_scaler = average_scaler / len(self.generateNgrams(word))
        # prob += (100 - prob) * average_scaler
        # return prob

# def generate_prob(self, word):
#     """ Given a word, compute the average gram prob """
#     grams = self.generateNgrams(word)
#     average_gram_prob = 0
#     for gram in grams:
#         average_gram_prob += self.dictionary.get(gram) / self.population
    
#     if average_gram_prob != 0:
#         average_gram_prob = average_gram_prob / len(grams)
#     return average_gram_prob

# data = ["hello", "world", "Ihope", "thisworks"]
# bi_gram = ngrams(data, 2)

# print(bi_gram.dictionary)
    # def ngrams_word_algorithm(word):
    #     """ Given a word, compute the tri_grams and get the average tri-gram value of the word 
    #         from the corpus """
    #     word_trigrams = self.generateNgrams(word, 3)
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
    #     word_bigrams = generateNgrams(phoneme, 2)

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
