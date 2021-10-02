# NamePronunciationProject

Using the IPA translator:

Dependencies are g2p-en (https://pypi.org/project/g2p-en/) and arpabet-syllabifier (https://github.com/vgautam/arpabet-syllabifier).

Run "from to_ipa import to_ipa," and then "model = to_ipa()" to create a model. To translate words, use "model.ipa('word')."
