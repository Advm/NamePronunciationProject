# NamePronunciationProject
Requires the following packages:

Tkinter: In python by default

Pandas: by default: pip install pandas

g2p-en (https://pypi.org/project/g2p-en/) 

arpabet-syllabifier (https://github.com/vgautam/arpabet-syllabifier).

These can be installed with the GetDepenencides command, use the .command file if on linux or
mac, and .bat on windows. To do so, you must have python3 installed (see how here: https://www.python.org/downloads/). For installation to work properly, you must also download the files here: https://github.com/vgautam/arpabet-syllabifier.git and extract the arpabet-syllabifier file into the same file as the GetDepenencides file.

ON WINDOWS YOU MUST RUN THE BAT FILE AS AN ADMINISTRATOR OTHERWISE IT WILL NOT WORK. Right click the file and select run as administrator. When a popup appears, select yes and ok. 


To run the program, double-click the run.command or run.bat file, 
again depending on your operating system. If on Linux, make sure your file explorer is set
to ask you if you want to run text files when double clicked. To do so, go to the file explorer
options -> prefrences -> behavior, and make sure under "excecutable text files" you have
"Ask what to do" set. When prompted upon double clicking the Run file, select either "run" or
"run in terminal"

CSV inputs must be one column of names.
Old messages from the program are stored in message.log. These are rolled over once a week, 
and store the last week's messages as well, if you want to look at them. The same applies
to error.log.



Dev notes:

To do an English to IPA translation, run "from to_ipa import to_ipa," and then "model = to_ipa()" to create a model. To translate words, use "model.ipa('word')."


To send a message to the message log, use main_model.send_to_message_log(message, message_level), where message level is True if you want it to be a warning message (default) and false for an info message.
To send to error log, just raise an exception like normal
