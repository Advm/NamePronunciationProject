from nameui import *
from to_ipa import to_ipa
import csv
from isenglish import getoutput
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import math



print("Loading Model")
model = tf.keras.models.load_model('IsAmericanEnglish')

print(getoutput(["ɹɪˈsɪpɹəˌkeɪtɪŋ","ɪnˈkɔɹpɝˌeɪtɪŋ","hɪstɝi","ʔapˌʃɾɛkʊŋsmɪtel","ɒːtæʃneʃɒːn","²'øːvɛroːɖɳad"],model))