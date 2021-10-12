import re
import config
import pandas as pd
from googletrans import Translator
from unidecode import unidecode

translator = Translator()

def processWords(words, tag):
    """Process a string to standardize data"""
    uniEncoded = []
    for word in words:
        if tag == "Mandarin":
            lower = translator.translate(word, src='zh-cn').text.lower()
        if tag == "Japanese":
            lower = translator.translate(word, src='ja').text.lower()
        else:
            lower = word.lower()
        
        if len(lower) <= config.maxLetters:
            uniEncoded.append(lower)

    return uniEncoded


def generateDictionary(tag):
    """Generates a list of words found in the csv's"""
    unicodeWords = []

    """Get all the datasets given the family"""
    for df in config.languageTags[tag]:
        
        # print(df)
        # "Iterate through each dataset in the family tree"
        # for ds in df:
        #     print(ds)
        #     print("Current Tag is " + tag)
        print("We are working with dataset " + df.name)
        words = df['Word'].tolist()
         #   print("The length of this datasets words are " + len(words))
        unicodeWords.extend(processWords(words, tag))
         #   print("Unicdoe words is now " + len(unicodeWords) + " L ong")

    print(len(unicodeWords))
    return unicodeWords

def asciiConverter(char):
    """Returns the array ascii representation for a word
    There are 52 total lettesr in ASCII"""
    asciiVal = ord(char)
    #Ranges for ASCII Represneation of word
    if asciiVal in range(97, 123):
        return asciiVal - 97
    elif asciiVal in range(129,142):
        return asciiVal - 129
    elif asciiVal in range(147, 153):
        return asciiVal - 147
    elif asciiVal in range(160, 165):
        return asciiVal - 160
    elif asciiVal == 228:
        return asciiVal - 228
    else:
        return asciiVal - 198

def convertDictionaryToVector(dictionary):
    """Given a list of words convert the string to their binary
    vector counterpart."""
    vectorList = []
    for word in dictionary:
        vector = ''
        for letter in word:
            ind = asciiConverter(letter)
            vector += (str(0)*ind) + str(1) + str(0)*(51-ind)
        if len(word) < config.maxLetters:
            vector += str(0)*52*(config.maxLetters - len(word))
        vectorList.append(vector)
    
    return vectorList

def createOutputVector(tagIdx, numLanguages):
    return str(0)*tagIdx + str(1) + str(0)*(numLanguages - 1 - tagIdx)
