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

def ngrams_phoneme_algorithm(corpus, phoneme):
    """ Given a corpus and a phoneme, *currently* compute the average bi-gram probability
        of the word. """
    bi_gram, bi_gram_pop = train_ngrams(corpus, 2)
    un_gram, un_gram_pop = train_ngrams(corpus, 1)
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

#Potential issue with words < the n length

# Working through the examples given https://blog.xrds.acm.org/2017/10/introduction-n-grams-need/

# (the number of times the previous word ‘wp’ occurs before the word ‘wn’) / 
# (the total number of times the previous word ‘wp’ occurs in the corpus)

#two_gram, y = train_ngrams(["abcd", "abefgahijk", "almno", "nopqr", "stuvnw"], 2)
#one_gram, x = train_ngrams(["abcd", "abefgahijk", "almno", "nopqr", "stuvnw"], 1)

#print(two_gram.get("cd") / one_gram.get("c")) #-> 100% of the time
#print(two_gram.get("no") / one_gram.get("n")) #-> 67% of the time



