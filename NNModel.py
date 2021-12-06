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
            time1 = time.time()
            
            temp = []
            for i in self.columns['Char(s)']:

                if i in ipaword:
                    temp.append(1)
                else:
                    temp.append(0)
            
            temparr.append(temp)
            time2 = time.time()
        time3 = time.time()
        answer = pd.DataFrame(temparr)
        answer.columns = self.columns['Char(s)'].values
        prediction = self.model.predict(temparr)
        print(prediction)
        time4 = time.time()
        roundedpred = []
        for i in prediction:
            temp = []
            for j in i:
                temp.append(j.round())
            roundedpred.append(temp)
        print(roundedpred)
        time5 = time.time()
        output.append(roundedpred)

        progressVal += 25 / progressDivisor
        if progressVal > 1:
            self.mainModel.addProgress(int(progressVal))
            progressVal = 0
        print(ipaword, time2-time1*10000, time3-time2*10000, time4-time3*10000, time5-time4*10000)
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
