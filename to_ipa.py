from g2p_en import G2p
from syllabifier import syllabifyARPA
import sys

class to_ipa:
    def __init__(self):
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
            print(f"Unable to find stress for word {graphemes}. Analyzing with no stress markers.", file=sys.stderr)
            for phone in arpa:
                word += self.arpabet_to_ipa_mapping[phone[:2]]
        
        return word + '/'

    def find_stress(self, syllable):
        """ Given an ARPABET syllable, return the appropriate IPA stress character. """
        s = "".join(syllable)
        for c in s:
            if c.isdigit():
                return self.stress[int(c)]
        return ''
