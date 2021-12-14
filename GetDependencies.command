#!/bin/bash
pip install nltk
pip install inflect
pip install Distance
pip install pandas
pip install numpy
pip install tensorflow
pip install sklearn
pip install g2p-en

#git clone https://github.com/vgautam/arpabet-syllabifier.git
cd arpabet-syllabifier-master

python3 setup.py install
cd ..

