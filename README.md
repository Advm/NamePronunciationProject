# NamePronunciationProject
Requires the following packages:

Tkinter: In python by default

Pandas: by default: pip install pandas

openpyxl for writing to Excel files: pip install openpyxl

g2p-en (https://pypi.org/project/g2p-en/) 

arpabet-syllabifier (https://github.com/vgautam/arpabet-syllabifier).


Dev notes:

To do an English to IPA translation, run "from to_ipa import to_ipa," and then "model = to_ipa()" to create a model. To translate words, use "model.ipa('word')."
