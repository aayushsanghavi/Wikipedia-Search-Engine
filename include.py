import re
import os
import sys
import pickle
import base64
from Stemmer import Stemmer

stemmer = Stemmer("english")
pattern = re.compile("[^a-zA-Z]")
field_chars = ["t", "b", "i", "c"]
stop_words = {}
reg = re.compile("\"|,| ")
stop_file = open("files/Stop_words.txt", "r")
content = stop_file.read()
content = re.split(reg, content)
for word in content :
	if word :
		stop_words[word] = True