# NamePronunciationProject
Requires the following packages:

Tkinter: In python by default

Pandas: by default: pip install pandas

g2p-en (https://pypi.org/project/g2p-en/) 

arpabet-syllabifier (https://github.com/vgautam/arpabet-syllabifier).


Dev notes:

To do an English to IPA translation, run "from to_ipa import to_ipa," and then "model = to_ipa()" to create a model. To translate words, use "model.ipa('word')."


To send a message to the message log, use main_model.send_to_message_log(message, message_level), where message level is True if you want it to be a warning message (default) and false for an info message.
To send to error log, just raise an exception like normal
