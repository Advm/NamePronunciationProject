from nameui import *
from to_ipa import to_ipa
    
ipa_model = to_ipa()

def main(words):
    # <names> is a list of every name the user inputted
    names = list(words["Word"])

    # <ipa_names> is a list of the same length containing IPA transcriptions of each name
    #   i.e., ipa_names[i] is an IPA transcription of names[i]
    ipa_names = [ipa_model.ipa(name) for name in names]
    print(ipa_names)


    # --------------------
    # TODO
    # <IPA_NAMES> -> GRIFFIN'S TOOL

    # <IPA_NAMES> -> JACK'S TOOL

    # COMBINE SCORES

    # GWEN: RETURN THAT SCORE
    return words


if __name__ == '__main__':
    root = Root_Win(main)
    root.mainloop()