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
        #print(self.columns)


    def convert(self, inputlist):
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

        output.append(roundedpred)

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
