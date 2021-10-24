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
    def __init__(self, model, columns):
        self.model = model
        self.columns = columns
    def convert(self, inputlist):
        output = []
        for ipaword in inputlist:
            temparr = []
            #print(ipaword)
            temp = []
            for i in self.columns['Char']:
                
                if i in ipaword:
                    temp.append(1)
                else:
                    temp.append(0)
            temparr.append(temp)
            #print(temparr)
            #print(pd.read_csv('Allchars.csv')['Char'].values)
            answer = pd.DataFrame(temparr)
            answer.columns = self.columns['Char'].values
            prediction = self.model.predict(answer)
            output.append(prediction[0][0])
    
        return output
def getoutput(wordlist, model):
    output = []
    for ipaword in wordlist:
        temparr = []
        #print(ipaword)
        temp = []
        for i in pd.read_csv('Allchars.csv')['Char']:
            
            if i in ipaword:
                temp.append(1)
            else:
                temp.append(0)
        temparr.append(temp)
        #print(temparr)
        #print(pd.read_csv('Allchars.csv')['Char'].values)
        answer = pd.DataFrame(temparr)
        answer.columns = pd.read_csv('Allchars.csv')['Char'].values
        prediction = model.predict(answer)
        output.append(prediction[0][0])
    #print(prediction)
    return output

# print("Loading Model")
# model = tf.keras.models.load_model('IsAmericanEnglish')

# print(getoutput(["ɹɪˈsɪpɹəˌkeɪtɪŋ","ɪnˈkɔɹpɝˌeɪtɪŋ","hɪstɝi","ʔapˌʃɾɛkʊŋsmɪtel","ɒːtæʃneʃɒːn","²'øːvɛroːɖɳad"],model))
