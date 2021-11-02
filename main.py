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
import os


class MainModel:
    """ Class for the superclass that controls all of the main functionality and
        contains all of the other models as instance variables. """

    def __init__(self, path_to_csv="ipa_dicts/english-general_american.csv"):
        """ Initializes models and the corpus of words. """
        with open(path_to_csv, encoding="utf8") as f:
            self.corpus = [w[1:-1] for row in csv.reader(f) \
                           for w in row[1].split(', ')]

        self.ipa_model = to_ipa()
        # SAE is "Standard American English"
        self.SAE_model = tf.keras.models.load_model('IsAmericanEnglish')
        self.twograms = ngrams(self.corpus, 2, "unigram_freq.csv")
        self.threegrams = ngrams(self.corpus, 3, "unigram_freq.csv")

        # Needed to communicate/share data across threads
        self._gui = None
        self.result = None
        self.lock = threading.Lock()

    def process_input(self, words):
        """ Method to be called every time the user submits new words. """

        # <names> is a list of every name the user inputted
        names = list(words[0])

        # <ipa_names> is a list of the same length containing IPA transcriptions of each name
        #   i.e., ipa_names[i] is an IPA transcription of names[i]
        ipa_names = [self.ipa_model.to_ipa(name)[1:-1] for name in names]

        # Get n-grams scores
        ngrams_scores = [self.twograms.generate_probability(name) for name in ipa_names]

        # get neural net scores
        phonemeNN = convertToModelFormat(self.SAE_model,
                                         pd.read_csv('Allchars.csv'))
        nn_scores = phonemeNN.convert(ipa_names)

        final_scores = [round(((nn_scores[i] + ngrams_scores[i]) / 2) * 100, 2)\
                        for i in range(len(ngrams_scores))]
        final_scores = [round(100 - x, 2) for x in final_scores]

        # Threading Stuff - need to acquire the lock (just to make sure)
        # then write the dataframe to the result attribute before releasing
        # the lock and firing the end thread virtual event
        self.lock.acquire()
        self.result =  pd.concat([pd.DataFrame(names),
                                   pd.DataFrame(final_scores)],
                                   axis=1, ignore_index=True)
        self.lock.release()
        self._gui.generate_event("<<ThreadEnded>>")

    def set_gui(self, gui_win):
        """
        Method used to set the object's gui attribute.
        """
        self._gui = gui_win


    def test_gui(self, words):
        """
        Method used to test the gui without running the entire program.
        """
        print(words)
        time.sleep(5)
        column2 = pd.DataFrame([2] * len(words.index))
        self.lock.acquire()
        self.result = pd.concat([words, column2], axis=1, ignore_index=True)
        self.lock.release()
        self._gui.generate_event("<<ThreadEnded>>")


def main():
    """
    Main sets up the MainModel object and the GUI, then calls the GUI's
    mainloop.
    Since the GUI Needs to know about the model and the model about the GUI,
    we create the model first, then the GUI with the model, then set the model's
    gui to be the GUI we just created, before calling the mainloop.
    """
    model = MainModel()
    root = Root_Win(model)
    model.set_gui(root)

    root.mainloop()


if __name__ == '__main__':
    main()

# with open("ipa_dicts/english-general_american.csv", encoding="utf8") as f:
#     corpus = [w[1:-1] for row in csv.reader(f) for w in row[1].split(', ')] 
#     ngram = ngrams(corpus, 1)
#     ipa_model = to_ipa()
#     word = "kenny"
#     print(f"{word}: ", ngram.generate_other_probability(ipa_model.to_ipa(word)[1:-1]))
#     print(ipa_model.to_ipa(word))


# def testoutput():
#     with open("ipa_dicts/english-general_american.csv", encoding="utf8") as f:
#         reader = csv.reader(f)
#         corpus = [w[1:-1] for row in reader for w in row[1].split(', ')]
#     names = [choice(corpus) for _ in range(200)]
#     ipa_names = [ipa_model.ipa(name)[1:-1] for name in names]
#     ngrams_scores = [ngrams_phoneme_algorithm(name) for name in ipa_names]
#     nn_scores = getoutput(ipa_names, model)
#     final_scores = [round(((nn_scores[i] + ngrams_scores[i]) / 2) * 100, 2) for i in range(len(ngrams_scores))]
#     final_scores = [round(100 - x, 2) for x in final_scores]
#     with open("test-out.csv", 'w', encoding="utf8") as f:
#         writer = csv.writer(f)
#         writer.writerows([[names[i], final_scores[i]] for i in range(len(names))])
