import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
import os
from to_ipa import to_ipa

class convertToModelFormat():
    def __init__(self, model, columns, mainModel):
        self.model = model
        self.columns = columns
        self.columns.columns = ["Char(s)"]
        self.mainModel = mainModel


    def convert(self, inputlist):
        output = []
        progressDivisor = len(inputlist) % 10
        if progressDivisor == 0:
            progressDivisor = len(inputlist)

        progressVal = 0
        for ipaword in inputlist:
            temparr = []
            temp = []
            for i in self.columns['Char(s)']:

                if i in ipaword:
                    temp.append(1)
                else:
                    temp.append(0)
            temparr.append(temp)

            answer = pd.DataFrame(temparr)
            answer.columns = self.columns['Char(s)'].values
            prediction = self.model.predict(answer)

            roundedpred = []
            for i in prediction[0]:
                roundedpred.append(round(i))
            output.append(roundedpred)

            progressVal += 25 / progressDivisor
            if progressVal > 1:
                self.mainModel.addProgress(int(progressVal))
                progressVal = 0

        return output
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
