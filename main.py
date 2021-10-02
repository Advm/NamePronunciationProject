from nameui import *
from to_ipa import to_ipa
import csv

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

def ngrams_phoneme_algorithm(un_gram, bi_gram, phoneme):
    """ Given a corpus and a phoneme, *currently* compute the average bi-gram probability
        of the word. """
    word_bigrams = ngrams(phoneme, 2)

    average_bigram_prob = 0
    for gram in word_bigrams:
        # If the corpus doesn't have this bi-gram, continue on to the next bi-gram. 
        # Might need to change the weight of this later but for now it seems fine 
        if bi_gram.get(gram) == None:
            continue

        average_bigram_prob += bi_gram.get(gram) / un_gram.get(gram[0])

    # To make sure that the word isn't composed completely of bi-grams not found
    # in the corpus
    if average_bigram_prob != 0:
        average_bigram_prob = average_bigram_prob / len(word_bigrams)
    #average_corpus_prob = len(bi_gram) / un_gram_pop

    return average_bigram_prob





ipa_model = to_ipa()
with open("ipa_dicts/english-general_american.csv", 'r') as f:
    reader = csv.reader(f)
    corpus = [w[1:-1] for row in reader for w in row[1].split(', ')]
bi_grams, _ = train_ngrams(corpus, 2)
un_grams, _ = train_ngrams(corpus, 1)

def main(words):
    # <names> is a list of every name the user inputted
    names = list(words["Word"])

    # <ipa_names> is a list of the same length containing IPA transcriptions of each name
    #   i.e., ipa_names[i] is an IPA transcription of names[i]
    ipa_names = [ipa_model.ipa(name)[1:-1] for name in names]
    print(ipa_names)


    # --------------------
    # TODO
    # <IPA_NAMES> -> GRIFFIN'S TOOL

    # <IPA_NAMES> -> JACK'S TOOL
    
    # Kenny run the corpus (our dictionary) through train_ngrams with both n = 1 and n = 2

    # call ngrams_phoneme_algorithm and change "corpus" to two dictionary arguments taken
    # in (I was just computing them inside the function for testing)
    scores = [ngrams_phoneme_algorithm(un_grams, bi_grams, word) for word in words]
    print(scores)

    # COMBINE SCORES

    # GWEN: RETURN THAT SCORE
    return words

if __name__ == '__main__':
    root = Root_Win(main)
    root.mainloop()
