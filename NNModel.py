import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
import time
import os
from to_ipa import to_ipa

class convertToModelFormat():
    def __init__(self, model, columns, mainModel):
        self.model = model
        self.columns = columns
        self.columns.columns = ["Char(s)"]
        self.mainModel = mainModel



    def convert(self, inputlist):
        """Takes in inputs, and uses the columns given by preselected csv to run on the matching model
        """
        output = []
        progressDivisor = len(inputlist) % 10
        if progressDivisor == 0:
            progressDivisor = len(inputlist)

        progressVal = 0
        temparr = []

        for ipaword in inputlist:

            temp = []
            for i in self.columns['Char(s)']:

                if i in ipaword:
                    temp.append(1)
                else:
                    temp.append(0)

            temparr.append(temp)
            progressVal += 25 / progressDivisor
            if progressVal > 1:
                self.mainModel.addProgress(int(progressVal))
                progressVal = 0


        answer = pd.DataFrame(temparr)
        answer.columns = self.columns['Char(s)'].values

        # Most of the runtime, presumably. Unpack?
        prediction = self.model.predict(temparr)


        roundedpred = []
        for i in prediction:
            temp = []
            for j in i:
                temp.append(j.round())
            roundedpred.append(temp)

        #output.append(roundedpred)

        return roundedpred

def get_parent_languge(arr):
    outputs = []
    for i in arr:
        if i[0] == 1:
            outputs.append("Germanic")
        elif i[1] == 1:
            outputs.append("Romance")
        elif i[2] == 1:
            outputs.append("Sino-Tebetan")
        else:
            outputs.append("Japonic")
    return outputs

def get_combined_output(model, final_scores, gram_letters, gram_phonemes, nn_scores):
    """Takes in the model, and the outputs from all other aspects of the program, and combines them into one score"""
    #The STDDEV and mean of the training data, used for scaling the outputs
    STDDEV = 0.136461
    MEAN = 1.251892
    inputDF = pd.DataFrame()
    temp = []
    for i in nn_scores:
        temp.append(i[0])
    inputDF["FinScores"] = final_scores
    inputDF["LetterNGramScores"] = gram_letters
    inputDF["PhonemeNGramScores"] = gram_letters
    inputDF["NNscores"] = temp
    prediction = model.predict(inputDF)
    holder = []
    for i in prediction:
        for j in i:
            #Ensures score is never over 100 or below 0
            if ((((j-MEAN)/STDDEV)*33) +50)> 100:
                holder+=[100.0]
            elif ((((j-MEAN)/STDDEV)*33) + 50)< 0:
                holder+=[0.0]
            else:
                #Scaled by 33 to make results spread wider across all values between 0-100, not centered around 50
                holder+=[(((j-MEAN)/STDDEV)*33) + 50]
   
    return holder

 