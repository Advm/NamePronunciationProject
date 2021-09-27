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


# Working through the examples given https://blog.xrds.acm.org/2017/10/introduction-n-grams-need/

# (the number of times the previous word ‘wp’ occurs before the word ‘wn’) / 
# (the total number of times the previous word ‘wp’ occurs in the corpus)

# two_gram, y = train_ngrams(["abcd", "abefgahijk", "almno", "nopqr", "stuvnw"], 2)
# one_gram, x = train_ngrams(["abcd", "abefgahijk", "almno", "nopqr", "stuvnw"], 1)

# print(two_gram.get("cd") / one_gram.get("c")) -> 100% of the time
# print(two_gram.get("no") / one_gram.get("n")) -> 67% of the time



