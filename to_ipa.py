from g2p_en import G2p
from syllabifier import syllabifyARPA

class to_ipa:
    def __init__(self):
        self.g2p = G2p()
        self.map = {'AA': 'ɑ',
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
        
    def ipa(self, graphemes):
        """ Convert English graphemes to IPA. """
        word = "/"
        arpa = self.g2p(graphemes)
        try:
            for syl in syllabifyARPA(arpa):
                word += self.find_stress(syl)
                for phone in syl.split(" "):
                    word += self.map[phone[:2]]
        except:
            for phone in arpa:
                word += self.map[phone[:2]]
        
        return word + '/'

    def find_stress(self, syllable):
        """ Given an ARPABET syllable, return the appropriate IPA stress character. """
        s = "".join(syllable)
        for c in s:
            if c.isdigit():
                return self.stress[int(c)]
        return ''
