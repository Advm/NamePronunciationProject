import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
import os
from to_ipa import to_ipa


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