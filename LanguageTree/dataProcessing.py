import functions
import numpy as np
from config import maxLetters, languageTags
import pandas as pd
import time

# The vectorized version of the word i.e. Hello becomes 0001000101....
wordData = []

#This is the familial origin of the words i.e. germanic, romance, etc.
languageTreeData = []

#this contains the actual ASCII represnation of the word i.e. "Hello"
masterDict = []

count = 0

for tag in languageTags.keys():
  
  print("Generating Dictionary for " + tag)
  dic = functions.generateDictionary(tag)
  for word in dic:
    masterDict.append(word)
  vct = functions.convertDictionaryToVector(dic)
  for vector in vct:
    wordData.append(vector)
  outputVct = functions.createOutputVector(count, len(languageTags))
  for i in range(len(vct)):
    languageTreeData.append(outputVct)

  arr = []
  print("Word data " + str(len(wordData)))
  print("Fam data " + str(len(languageTreeData)))
  print("ASCII WORD " + str(len(masterDict)))
  time.sleep(2)
  for i in range(len(wordData)):
    entry = []
    entry.append(masterDict[i])
    for digit in languageTreeData[i]:
      entry.append(float(digit))
    for digit in wordData[i]:
      entry.append(float(digit))
    arr.append(entry)
    print("Finished iteration " + str(i))
  
  count += 1
  
arr = np.array(arr)
np.save('arr.npy', arr)
arr = []
df=pd.DataFrame(arr)
df.to_csv('data.csv')


print("Finished Processing!")




