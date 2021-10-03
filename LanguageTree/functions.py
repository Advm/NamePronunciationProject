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
            uniEncoded.append(unidecode(lower))

    return uniEncoded


def generateDictionary(tag):
    """Generates a list of words found in the csv's"""
    unicodeWords = []

    """Get all the datasets given the family"""
    for df in config.languageTags[tag]:

        "Iterate through each dataset in the family tree"
        for ds in df:
            words = df['Word'].tolist()
            unicodeWords.extend(processWords(words, tag))

    return unicodeWords

def convertDictionaryToVector(dictionary):
    """Given a list of words convert the string to their binary
    vector counterpart."""
    vectorList = []
    for word in dictionary:
        vector = ''
        for letter in word:
            ind = ord(letter)-97
            vector += (str(0)*ind) + str(1) + str(0)*(25-ind)
        if len(word) < config.maxLetters:
            vector += str(0)*26*(config.maxLetters - len(word))
        vectorList.append(vector)
    
    return vectorList

def createOutputVector(tagIdx, numLanguages):
    return str(0)*tagIdx + str(1) + str(0)*(numLanguages - 1 - tagIdx)
