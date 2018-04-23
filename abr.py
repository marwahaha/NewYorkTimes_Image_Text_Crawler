import os
import re
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktTrainer
from nltk.corpus import gutenberg



#This file add possible abreviation into a txt file for nltk to learn in "process.py"

#Put in the path of the directory containing all txt files (crawled data)
directory = 'C:\\Users\\hyzha\\PycharmProjects\\NY Times World\\NY Times World'
text = ""
for file_id in gutenberg.fileids():
    text += gutenberg.raw(file_id)
trainer = PunktTrainer()
trainer.INCLUDE_ALL_COLLOCS = True
trainer.train(text)
tokenizer = PunktSentenceTokenizer(trainer.get_params())
abr = []

n = 1
for filename in os.listdir(directory):
            filepath = directory + '\\' + filename
            if 'text.txt' in filepath:
                try:
                    with open('new.txt', 'w') as new:
                        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                            print(n)
                            n+=1
                            i = 0
                            for line in f:
                                i += 1
                                line += ' '
                                line = re.sub('[^a-zA-Z0-9\n\.:/\-\.\',!@#$%^&*()_+=~`{}|;<>?]', ' ', line)
                                line = line.replace('\n', '')
                                new.write(line)
                        new.close()

                    with open('new.txt', 'r') as new2:
                        data = new2.read()
                        sentences = tokenizer.tokenize(data)
                        for tmp in sentences:
                            if(tmp[0].isupper() and " " not in tmp and len(tmp) <= 5 and tmp[-1] == "." ):
                                if(tmp.replace(".","").lower() != "" and tmp.replace(".","").lower() not in abr):
                                    abr.append(tmp.replace(".","").lower())

                except Exception as e:
                    print(str(e))
                    print(filename)

with open ('abr.txt', 'w') as f2:
    for i in abr:
        f2.write(i + '\n')