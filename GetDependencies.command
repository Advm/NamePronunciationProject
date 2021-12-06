#!/bin/bash
pip install nltk
pip install inflect
pip install Distance
pip install pandas
pip install numpy
pip install g2p-en

git clone https://github.com/vgautam/arpabet-syllabifier.git
pwd
cd arpabet-syllabifier
pwd
python setup.py install
cd ..
pwd

