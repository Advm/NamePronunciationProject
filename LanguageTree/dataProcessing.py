import functions
import numpy as np
from config import maxLetters, languageTags
import pandas as pd

wordData = []
languageTreeData = []
masterDict = []

count = 0

for tag in languageTags.keys():
  print("Generation Dictionary for " + tag)
  dic = functions.generateDictionary(tag)
  for word in dic:
    masterDict.append(word)
  vct = functions.convertDictionaryToVector(dic)
  for vector in vct:
    wordData.append(vector)
  outputVct = functions.createOutputVector(count, len(languageTags))
  for i in range(len(vct)):
    languageTreeData.append(outputVct)
  count += 1

arr = []
for i in range(len(wordData)):
  entry = []
  entry.append(masterDict[i])
  for digit in languageTreeData[i]:
    entry.append(float(digit))
  for digit in wordData[i]:
    entry.append(float(digit))
  arr.append(entry)

arr = np.array(arr)
np.save('arr.npy', arr)
dff = pd.DataFrame(arr)
dff.to_csv('data.csv')



