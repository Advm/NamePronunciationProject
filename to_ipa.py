from g2p_en import G2p
from syllabifier import syllabifyARPA
import sys
import csv
import os

class to_ipa:
    def __init__(self, main_model):
        self._main_model = main_model

        self.graph_to_phone_model = G2p()
        self.arpabet_to_ipa_mapping = {'AA': 'ɑ',
                                        'AE': 'æ',
                                        'AH': 'ə',
                                        'AO': 'ɔ',
                                        'AW': 'aʊ',
                                        'AY': 'aɪ',
                                        'B': 'b',
                                        'CH': 'tʃ',
                                        'D': 'd',
                                        'DH': 'ð',
                                        'EH': 'ɛ',
                                        'ER': 'ɝ',
                                        'EY': 'eɪ',
                                        'F': 'f',
                                        'G': 'ɡ',
                                        'HH': 'h',
                                        'IH': 'ɪ',
                                        'IY': 'i',
                                        'JH': 'dʒ',
                                        'K': 'k',
                                        'L': 'ɫ',
                                        'M': 'm',
                                        'N': 'n',
                                        'NG': 'ŋ',
                                        'OW': 'oʊ',
                                        'OY': 'ɔɪ',
                                        'P': 'p',
                                        'R': 'ɹ',
                                        'S': 's',
                                        'SH': 'ʃ',
                                        'T': 't',
                                        'TH': 'θ',
                                        'UH': 'ʊ',
                                        'UW': 'u',
                                        'V': 'v',
                                        'W': 'w',
                                        'Y': 'j',
                                        'Z': 'z',
                                        'ZH': 'ʒ'
                                        }
        self.stress = ['', 'ˈ', 'ˌ']

    def to_ipa(self, graphemes):
        """ Convert English graphemes to IPA. """
        word = "/"
        arpa = self.graph_to_phone_model(graphemes)
        try:
            for syl in syllabifyARPA(arpa):
                word += self.find_stress(syl)
                for phone in syl.split(" "):
                    word += self.arpabet_to_ipa_mapping[phone[:2]]
        except:
            self._main_model.send_to_message_log(f"Unable to find stress for word {graphemes}. Analyzing with no stress markers.")
            for phone in arpa:
                try:
                    word += self.arpabet_to_ipa_mapping[phone[:2]]
                except:
                    self._main_model.send_to_message_log(f"Unable to interpret syllable {phone}. Ignoring.")
        return word + '/'

    def find_stress(self, syllable):
        """ Given an ARPABET syllable, return the appropriate IPA stress character. """
        s = "".join(syllable)
        for c in s:
            if c.isdigit():
                return self.stress[int(c)]
        return ''



# def add_ipa_to_csv(csv_name):
#     """ This is a function to be called once, to add IPA translations to a CSV file."""
#     ipamodel = to_ipa()
#     with open(csv_name, encoding="utf8") as f, open(f"temp_{csv_name}", 'w') as out:
#         reader = csv.reader(f)
#         writer = csv.writer(out)
#         for row in reader:
#             writer.writerow([row[0], ipamodel.to_ipa(row[0])[1:-1], row[1]])
#     os.remove(csv_name)
#     os.rename(f"temp_{csv_name}", csv_name)
