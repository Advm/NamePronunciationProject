from nameui import *
from to_ipa import to_ipa
import csv
from NNModel import convertToModelFormat, get_parent_languge
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import math
from random import choice
from ngrams import NgramManager, Ngrams
import os
import time


class MainModel:
    """ Class for the superclass that controls all of the main functionality and
        contains all of the other models as instance variables. """

    def __init__(self, path_to_csv="ipa_dicts/english-general_american.csv"):
        """ Initializes models and the corpus of words. """
        with open(path_to_csv, encoding="utf8") as f:
            self.corpus = [w[1:-1] for row in csv.reader(f) \
                           for w in row[1].split(', ')]

        self.ipa_model = to_ipa(self)
        # SAE is "Standard American English"
        self.SAE_model = tf.keras.models.load_model('IsAmericanEnglishv4.0')
        self.root_model = tf.keras.models.load_model('RootLanguageModel')

        self.ngrams = NgramManager(self, 2, 3)

        # Needed to communicate/share data across threads
        self._gui = None
        self.prog_val = None
        self.to_gui_message = ""
        self.is_warning = False
        self.result = None
        self.lock = threading.Lock()

    def processInput(self, words):
        """ Method to be called every time the user submits new words. """

        # <names> is a list of every name the user inputted
        names = list(map(lambda x: x.lower(), list(words[0])))
        self.addProgress(10)

        progressDivisor = len(names) % 100
        if progressDivisor == 0:
            progressDivisor = len(names)

        # <ipa_names> is a list of the same length containing IPA transcriptions of each name
        #   i.e., ipa_names[i] is an IPA transcription of names[i]
        ipa_names = []
        progressVal = 0
        for name in names:
            ipa_names.append(self.ipa_model.to_ipa(name)[1:-1])

            progressVal += (15 / progressDivisor)
            if progressVal > 1:
                self.addProgress(int(progressVal))
                progressVal = 0

        self.sendToMessageLog("IPA conversion complete", False)

        gram_letters  = []
        progressVal = 0
        for name in names:
            gram_letters.append(round(100 - self.ngrams.generateLetterProbs(name), 2))

            progressVal += (10 / progressDivisor)
            if progressVal > 1:
                self.addProgress(int(progressVal))
                progressVal = 0

        gram_phonemes = []
        progressVal = 0
        for name in ipa_names:
            gram_phonemes.append(round(100 - self.ngrams.generatePhonemeProbs(name), 2))

            progressVal += (10 / progressDivisor)
            if progressVal > 1:
                self.addProgress(int(progressVal))
                progressVal = 0

        self.sendToMessageLog("N-gram calculations complete", False)

        # get neural net scores
        # Tnks seems to take a while?
        phonemeNN = convertToModelFormat(self.SAE_model,
                                         pd.read_csv('Eng_2Chars.csv'),
                                         self)
        rootLanguageNN = convertToModelFormat(self.root_model,
                                         pd.read_csv('singleChars.csv'),
                                         self)

        nn_scores = phonemeNN.convert(names)
        root_NN_scores = rootLanguageNN.convert(ipa_names)
        root_Parents = get_parent_languge(root_NN_scores)

        self.sendToMessageLog("Neural Network calculations complete", False)

        final_scores = [round((gram_letters[i] + gram_phonemes[i]) / 2, 2)
                        for i in range(len(gram_letters))]

        # Threading Stuff - need to acquire the lock (just to make sure)
        # then write the dataframe to the result attribute before releasing
        # the lock and firing the end thread virtual event
        self.lock.acquire()
        self.result =  pd.concat([words[0],
                                  pd.DataFrame(final_scores),
                                  pd.DataFrame(gram_letters),
                                  pd.DataFrame(gram_phonemes),
                                  pd.DataFrame(nn_scores),
                                  pd.DataFrame(root_Parents)],
                                  axis=1, ignore_index=True)
        self.lock.release()
        self.addProgress(5)
        self._gui.generateEvent("<<ThreadEnded>>")

    def setGUI(self, gui_win):
        """
        Method used to set the object's gui attribute.
        @params - self
                - gui_win: the Root_Win object to set _gui to
        @returns - None
        """
        self._gui = gui_win


    def setNGrams(self, nlist):
        """
        Method used to set the object's NGram's manager object so the user
        can select which n they want to run with Ngrams. (This method cannot
        be run by the GUI while in a multithreaded state, that would
        probably create issues)
        @params - self
                - nlist: a list of ints to pass to the NGrams manager constructor
        @returns - None
        """
        self.ngrams = NgramManager(self, *nlist)

    def addProgress(self, value):
        """
        Method used to add progress to the progress bar. Sets prog_val to value
        and then fires the virtual event to add progress
        @params - self
                - value: the value to add to the progress bar
        @returns - None
        """
        self.lock.acquire()
        self.prog_val = value
        self.lock.release()
        self._gui.generateEvent("<<AddProgress>>")

    def sendToMessageLog(self, output, warning=True):
        """
        Method used to output a message to the message log. Sets is_warning to
        warning, to_gui_message to output, and fires the
        <<SendMessage>> virtual event
        @params - self
                - output: The message to be outputted to the log
                - warning: If true, the message is treated as a warning.
                           Otherwise, it is treated as an 'info' message.
        @returns - None
        """
        self.lock.acquire()
        self.is_warning = warning
        self.to_gui_message = output
        self.lock.release()
        self._gui.generateEvent("<<SendMessage>>")


    def test_gui(self, words):
        """
        Method used to test the gui without running the entire program.
        To use, on the line root = RootWin(model), add a true parameter
        to the RootWin constructor.
        """
        self._gui.generateEvent("<<ThreadEnded>>")

def main():
    """
    Main sets up the MainModel object and the GUI, then calls the GUI's
    mainloop.
    Since the GUI Needs to know about the model and the model about the GUI,
    we create the model first, then the GUI with the model, then set the model's
    gui to be the GUI we just created, before calling the mainloop.
    """
    try:
        model = MainModel()
        root = RootWin(model)
        model.setGUI(root)
    except Exception as e:
        output = "An error occured while setting up the program:\n"
        output += "".join(traceback.format_exception(type(e), e, e.__traceback__))
        print(output, file=sys.stderr)
        sys.exit(1)

    root.mainLoop()




if __name__ == '__main__':
    main()



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
