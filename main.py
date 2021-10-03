from nameui import *
from to_ipa import to_ipa
import csv
import math

def ngrams(str, n):
    """ Given a string and an n, return a list of all grams of that length"""
    answer = []
    for i in range(0, len(str) - n + 1):
        end = i + n
        answer.append(str[i:end])
    return answer

def train_ngrams(list_str, n):
    """ Given a list of strings, convert into a dictionary and keep track 
    of the number of occurances
    Also keeps track of the number of grams (which is different from the
    number of distinct grams which can get obtained using .len())"""
    population = 0
    mydict = {}
    for str in list_str:
        grams = ngrams(str, n)
        for gram in grams:
            population += 1
            if mydict.get(gram) is None:
                mydict.update({gram: 1})
            else:
                num = mydict.get(gram)
                mydict.update({gram: num + 1})
    return mydict, population

def ngrams_phoneme_algorithm(phoneme):
    """ Given a phoneme, compute the z-score from the average of the bi-gram calculations
        and convert to a float between 0-1 """
    word_bigrams = ngrams(phoneme, 2)

    average_bigram_prob = 0
    for gram in word_bigrams:
        # If the corpus doesn't have this bi-gram, continue on to the next bi-gram. 
        # Might need to change the weight of this later but for now it seems fine 
        if bi_grams.get(gram) == None:
            continue

        average_bigram_prob += bi_grams.get(gram) / un_grams.get(gram[0]) 
        #average_bigram_prob += bi_grams.get(gram) / bi_gram_pop

    # To make sure that the word isn't composed completely of bi-grams not found
    # in the corpus
    if average_bigram_prob != 0:
        average_bigram_prob = average_bigram_prob / len(word_bigrams)

    z_score = (average_bigram_prob - average_corpus_prob) / standard_deviation

    answer = .5 * (math.erf(z_score / 2 ** .5) + 1) # https://stackoverflow.com/questions/2782284/function-to-convert-a-z-score-into-a-percentage

    return answer #average_bigram_prob





ipa_model = to_ipa()
with open("ipa_dicts/english-general_american.csv", encoding="utf8") as f:
    reader = csv.reader(f)
    corpus = [w[1:-1] for row in reader for w in row[1].split(', ')]
bi_grams, bi_gram_pop = train_ngrams(corpus, 2)
un_grams, _ = train_ngrams(corpus, 1)

#average_corpus_prob = len(bi_grams) / bi_gram_pop
average_corpus_prob = 0
for gram in bi_grams:
    average_corpus_prob += bi_grams.get(gram) / un_grams.get(gram[0])
average_corpus_prob = average_corpus_prob / bi_gram_pop

standard_deviation = 0
for gram in bi_grams:
    standard_deviation += (bi_grams.get(gram) / un_grams.get(gram[0]) - average_corpus_prob) * (bi_grams.get(gram) / un_grams.get(gram[0]) - average_corpus_prob)
    #standard_deviation += ((bi_grams.get(gram) / bi_gram_pop) - average_corpus_prob) * ((bi_grams.get(gram) / bi_gram_pop) - average_corpus_prob)
standard_deviation = standard_deviation / (bi_gram_pop - 1)
standard_deviation = math.sqrt(standard_deviation)

def main(words):
    # <names> is a list of every name the user inputted
    names = list(words[0])

    # <ipa_names> is a list of the same length containing IPA transcriptions of each name
    #   i.e., ipa_names[i] is an IPA transcription of names[i]
    ipa_names = [ipa_model.ipa(name)[1:-1] for name in names]
    print(ipa_names)

    # Get n-grams scores
    ngrams_scores = [ngrams_phoneme_algorithm(name) for name in names]
    print(ngrams_scores)

    # --------------------
    # TODO    
    # <IPA_NAMES> -> GRIFFIN'S TOOL
    nn_scores = [] # left blank
    print(nn_scores)

    # COMBINE SCORES
    final_scores = []
    for i in range(len(ngrams_scores)):
        # apply some func to nn_scores[i] and ngrams_scores[i], append result to final_scores
        pass

    # GWEN: RETURN THAT SCORE FORMATTED AS DATAFRAME
    return final_scores

if __name__ == '__main__':
    root = Root_Win(main)
    root.mainloop()
