import pandas as pd

#Longest Word in English Language
maxLetters = 15

"""Reads in all """
# Germanic Language Family
df = pd.read_csv("/Users/vincent/Git/PronunciationProject/NamePronunciationProject/ipa_dicts/Germanic/english-general_american.csv")
df.name = "English"
df2 = pd.read_csv("/Users/vincent/Git/PronunciationProject/NamePronunciationProject/ipa_dicts/Germanic/english-received_pronunciation.csv")
df2.name = "recevied"
df3 = pd.read_csv("/Users/vincent/Git/PronunciationProject/NamePronunciationProject/ipa_dicts/Germanic/german.csv")
df3.name = "german"
df4 = pd.read_csv("/Users/vincent/Git/PronunciationProject/NamePronunciationProject/ipa_dicts/Germanic/swedish.csv")
df4.name = "swed"
df5 = pd.read_csv("/Users/vincent/Git/PronunciationProject/NamePronunciationProject/ipa_dicts/Germanic/norwegian-bokmal.csv")
df5.name = "nor"

#Romance Language Family
df6 = pd.read_csv("/Users/vincent/Git/PronunciationProject/NamePronunciationProject/ipa_dicts/Romance/french-france.csv")
df6.name = "french"
df7 = pd.read_csv("/Users/vincent/Git/PronunciationProject/NamePronunciationProject/ipa_dicts/Romance/french-quebec.csv")
df7.name = "quebec"
df8 = pd.read_csv('/Users/vincent/Git/PronunciationProject/NamePronunciationProject/ipa_dicts/Romance/spanish-mexico.csv')
df8.name = "mexico"
df9 = pd.read_csv('/Users/vincent/Git/PronunciationProject/NamePronunciationProject/ipa_dicts/Romance/spanish-spain.csv')
df9.name = "spain"

#Sino-Tebetan Family

#Cantonese is having an issue reading cantonese
# df10 = pd.read_csv('/Users/adamvalencia/Git/NamePronunciationProject/ipa_dicts/Sino-Tebetan/cantonese.csv')

#Mandarin has two spellings per word sometimes. Have to standardize data.
df11 = pd.read_csv('/Users/vincent/Git/PronunciationProject/NamePronunciationProject/ipa_dicts/Sino-Tebetan/mandarin.csv')
df11.name = "mandarin"

#Japonic
df12 = pd.read_csv('/Users/vincent/Git/PronunciationProject/NamePronunciationProject/ipa_dicts/japanese.csv')
df12.name = "japonic"

cleanDatasets = [df, df2, df3, df4, df5, df7, df8, df11, df12]

def removeIpaSlash(s):
  """Function to remove slashses from the IPA Pronunciation"""
  return s.replace("/", "")

def removeQuote(s):
  return s.replace("'", "")

"""Cleans up all the datasets and removes the slashes stricly leaving the ipa-alphabet"""
for d in cleanDatasets:
  d['Pronunciations'] = d['Pronunciations'].map(removeIpaSlash)
  d['Word'] = d['Word'].map(removeQuote)

languageTags = {
                "Germanic": [df,df2,df3,df4,df5],
                "Romance": [df7,df8],
                "Sino-Tebetan":[df11],
                "Japonic": [df12]
                }

# languageTags = {
#                 "Germanic": [0,1,2,3,4],
#                 "Romance": [5,6,7,8],
#                 "Sino-Tebetan":[9],
#                 "Japonic": [10]
#                 }



