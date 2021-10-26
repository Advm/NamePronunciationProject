from nameui import *
from to_ipa import to_ipa
import csv
from NNModel import getoutput, convertToModelFormat
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import math
from random import choice
from ngrams import ngrams

ISAMERICANENGLISH = tf.keras.models.load_model('IsAmericanEnglish')

ipa_model = to_ipa()
with open("ipa_dicts/english-general_american.csv", encoding="utf8") as f:
    reader = csv.reader(f)
    corpus = [w[1:-1] for row in reader for w in row[1].split(', ')] # [w[1:-1] for row in reader for w in row[0].split(', ')] for words
 
#this is how ngrams object can be used, still need to implement the algorithms so right now all it can do is create a dictionary
#bi_gram = ngrams(corpus, 2)

def main(words):
    # <names> is a list of every name the user inputted
    names = list(words[0])

    # <ipa_names> is a list of the same length containing IPA transcriptions of each name
    #   i.e., ipa_names[i] is an IPA transcription of names[i]
    ipa_names = [ipa_model.to_ipa(name)[1:-1] for name in names]
    #print(ipa_names)

    # Get n-grams scores
    ngrams_scores = [ngrams_phoneme_algorithm(name) for name in ipa_names]
    #word_ngrams_scores = [ngrams_word_algorithm(name) for name in names]
    #print(ngrams_scores)

    # get neural net scores
    phonemeNN = convertToModelFormat(ISAMERICANENGLISH, pd.read_csv('Allchars.csv'))
    nn_scores = phonemeNN.convert(ipa_names)
    print(nn_scores)
    #print(nn_scores)

    final_scores = [round(((nn_scores[i] + ngrams_scores[i]) / 2) * 100, 2) for i in range(len(ngrams_scores))]
    final_scores = [round(100 - x, 2) for x in final_scores]

    return pd.concat([pd.DataFrame(names), pd.DataFrame(final_scores)], axis=1, ignore_index=True)


def testoutput():
    with open("ipa_dicts/english-general_american.csv", encoding="utf8") as f:
        reader = csv.reader(f)
        corpus = [w[1:-1] for row in reader for w in row[1].split(', ')]
    names = [choice(corpus) for _ in range(200)]
    ipa_names = [ipa_model.ipa(name)[1:-1] for name in names]
    ngrams_scores = [ngrams_phoneme_algorithm(name) for name in ipa_names]
    nn_scores = getoutput(ipa_names, model)
    final_scores = [round(((nn_scores[i] + ngrams_scores[i]) / 2) * 100, 2) for i in range(len(ngrams_scores))]
    final_scores = [round(100 - x, 2) for x in final_scores]
    with open("test-out.csv", 'w', encoding="utf8") as f:
        writer = csv.writer(f)
        writer.writerows([[names[i], final_scores[i]] for i in range(len(names))])


if __name__ == '__main__':
    # root = Root_Win(main)
    # root.mainloop()
    testoutput()
