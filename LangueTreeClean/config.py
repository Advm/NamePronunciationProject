import pandas as pd
max_letters = 12
language_tags = {

                'en':['actor', 'alcohol', 'cheque', 'cancer', 'chocolate', 'debate', 'hobby', 'melon', 'propaganda',
                      'religion', 'violin', 'england', 'MediaWiki'],

                'cs': ['praha', 'evropa', 'pyreneje', 'voda', 'housle', 'Náboženství', 'Příroda', 'Ekosystém',
                    'vzdělání', 'Irkso', 'Dům', 'Zpěvák', 'Zeus', 'Mykény', 'Starověké_Řecko', 'Renesance',
                    'Andrej_Babiš', 'Správa_železniční_dopravní_cesty', 'Kraje_v_Česku', 'Česko', 'Slezsko',
                    'Latina', 'Spojené_království', 'Římský_senát'],

                'de': ['Deutsche_Sprache', 'Deutschland', 'Kommunistische_Partei_der_Sowjetunion', 'Wasser',
                    'Festkörper', 'Seele', 'Geist', 'Dreifaltigkeit', 'Große', 'Christentum', 'Gott'],

                'sv': ['Svenska', 'Sverige', 'Danmark', 'Europeiska_unionen', 'Medeltiden', 'Feodalism', 'Kung',
                    'Kejsare', 'Monarki', 'Valmonarki', 'Choklad', 'Mjölk', 'Prolaktin', 'Kvinna', 'Eldvapen',
                    'Kina', 'Götar', 'Romantiken', 'Ideologi', 'Tänkande', 'Pedagogik', 'Sekund', 'Solen', 'Väder',
                    'Mellanöstern', 'Väte', 'Anatomi', 'Hjärta', 'Puls', 'Grekiska', 'Cypern'],

                'fr': ['Français', 'Langues_romanes', 'Charlemagne', 'Traité_de_Verdun', 'Louis_le_Pieux',
                    'Son_(physique)', 'Zoologie', 'Intelligence_animale', 'Intelligence', 'Tautologie',
                    'Pléonasme', 'Figure_de_style']

                # 'it': ['Lingua_italiana', 'Graffiti_(archeologia)', 'Impero_romano', 'Romolo_Augusto', 'Diritto_romano',
                #     'Europa', 'Continente', 'Islanda', 'Cioccolato', 'Alimento', 'Plantae', 'Aroma', 'Olfatto',
                #     'Organi_di_senso', 'Organismo_vivente', 'Epigenetica', 'Fenotipo', 'Composto_chimico',
                #     'Legame_covalente', 'Atomo', 'Materia_(fisica)', 'Energia', 'Fisica']
                 }


"""Reads in all """
# Germanic Language Family
df = pd.read_csv("/Users/vincent/Git/PronunciationProject/NamePronunciationProject/ipa_dicts/Germanic/english-general_american.csv")
df2 = pd.read_csv("/Users/vincent/Git/PronunciationProject/NamePronunciationProject/ipa_dicts/Germanic/english-received_pronunciation.csv")
df3 = pd.read_csv("/Users/vincent/Git/PronunciationProject/NamePronunciationProject/ipa_dicts/Germanic/german.csv")
df4 = pd.read_csv("/Users/vincent/Git/PronunciationProject/NamePronunciationProject/ipa_dicts/Germanic/swedish.csv")
df5 = pd.read_csv("/Users/vincent/Git/PronunciationProject/NamePronunciationProject/ipa_dicts/Germanic/norwegian-bokmal.csv")

#Romance Language Family
df6 = pd.read_csv("/Users/vincent/Git/PronunciationProject/NamePronunciationProject/ipa_dicts/Romance/french-france.csv")
df7 = pd.read_csv("/Users/vincent/Git/PronunciationProject/NamePronunciationProject/ipa_dicts/Romance/french-quebec.csv")
df8 = pd.read_csv('/Users/vincent/Git/PronunciationProject/NamePronunciationProject/ipa_dicts/Romance/spanish-mexico.csv')
df9 = pd.read_csv('/Users/vincent/Git/PronunciationProject/NamePronunciationProject/ipa_dicts/Romance/spanish-spain.csv')

#Sino-Tebetan Family
df10 = pd.read_csv('/Users/vincent/Git/PronunciationProject/NamePronunciationProject/ipa_dicts/Sino-Tebetan/cantonese.csv')
df11 = pd.read_csv('/Users/vincent/Git/PronunciationProject/NamePronunciationProject/ipa_dicts/Sino-Tebetan/mandarin.csv')

#Japonic
df12 = pd.read_csv('/Users/vincent/Git/PronunciationProject/NamePronunciationProject/ipa_dicts/japanese.csv')

cleanDatasets = [df, df2, df3, df4, df5]#, df6, df7, df8, df9, df10, df11, df12]
datasets = {"Germanic": [df,df2,df3,df4,df5], "Romance": [df6,df7,df8,df9], "ST":[df10,df11], "Japonic": [df12]}



