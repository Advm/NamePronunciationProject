import pandas as pd

#Longest Word in English Language
maxLetters = 45

"""Reads in all """
# Germanic Language Family
df = pd.read_csv("/Users/adamvalencia/Git/NamePronunciationProject/ipa_dicts/Germanic/english-general_american.csv")
df2 = pd.read_csv("/Users/adamvalencia/Git/NamePronunciationProject/ipa_dicts/Germanic/english-received_pronunciation.csv")
df3 = pd.read_csv("/Users/adamvalencia/Git/NamePronunciationProject/ipa_dicts/Germanic/german.csv")
df4 = pd.read_csv("/Users/adamvalencia/Git/NamePronunciationProject/ipa_dicts/Germanic/swedish.csv")
df5 = pd.read_csv("/Users/adamvalencia/Git/NamePronunciationProject/ipa_dicts/Germanic/norwegian-bokmal.csv")

#Romance Language Family
df6 = pd.read_csv("/Users/adamvalencia/Git/NamePronunciationProject/ipa_dicts/Romance/french-france.csv")
df7 = pd.read_csv("/Users/adamvalencia/Git/NamePronunciationProject/ipa_dicts/Romance/french-quebec.csv")
df8 = pd.read_csv('/Users/adamvalencia/Git/NamePronunciationProject/ipa_dicts/Romance/spanish-mexico.csv')
df9 = pd.read_csv('/Users/adamvalencia/Git/NamePronunciationProject/ipa_dicts/Romance/spanish-spain.csv')

#Sino-Tebetan Family

#Cantonese is having an issue reading cantonese
# df10 = pd.read_csv('/Users/adamvalencia/Git/NamePronunciationProject/ipa_dicts/Sino-Tebetan/cantonese.csv')

#Mandarin has two spellings per word sometimes. Have to standardize data.
df11 = pd.read_csv('/Users/adamvalencia/Git/NamePronunciationProject/ipa_dicts/Sino-Tebetan/mandarin.csv')

#Japonic
df12 = pd.read_csv('/Users/adamvalencia/Git/NamePronunciationProject/ipa_dicts/japanese.csv')

cleanDatasets = [df, df2, df3, df4, df5, df6, df7, df8, df9, df11, df12]

def removeIpaSlash(s):
  """Function to remove slashses from the IPA Pronunciation"""
  return s.replace("/", "")

"""Cleans up all the datasets and removes the slashes stricly leaving the ipa-alphabet"""
for d in cleanDatasets:
  d['Pronunciations'] = d['Pronunciations'].map(removeIpaSlash)

languageTags = {
                "Germanic": [df,df2,df3,df4,df5],
                "Romance": [df6,df7,df8,df9],
                "Sino-Tebetan":[df11],
                "Japonic": [df12]
                }





