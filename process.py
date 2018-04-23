import csv
import os
import re
import io
import unidecode
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktTrainer
from nltk.corpus import gutenberg



#This python file process all text files (crawled data) into two csv files, NY Times World and NY Times World PhotoID

#Put in the path of the directory containing all txt files
txt_dir = 'C:\\Users\\hyzha\\PycharmProjects\\NY Times World\\NY Times World'

n = 1
m = 100000
text = ""
for file_id in gutenberg.fileids():
    text += gutenberg.raw(file_id)
trainer = PunktTrainer()
trainer.INCLUDE_ALL_COLLOCS = True
trainer.train(text)
tokenizer = PunktSentenceTokenizer(trainer.get_params())
with open('abr.txt', 'r') as abr:
    for j in abr:
        tokenizer._params.abbrev_types.add(j.replace('\n',''))

with open('NY Times World PhotoID.csv', 'w', newline='') as IDcsv:
    with open('NY Times World.csv','w', newline = '') as mycsv:

        directory = txt_dir
        for filename in os.listdir(directory):
            filepath = directory + '\\' + filename
            if 'text.txt' in filepath:
                try:
                    print(n)
                    with open('new.txt', 'w', encoding="utf-8") as new:
                        with io.open(filepath, 'r', encoding='utf-8') as f:

                            i = 0
                            for line in f:
                                i += 1
                                line += ' '
                                line = unidecode.unidecode(line)
                                if(i == 1):
                                    first = re.sub('[^a-zA-Z0-9\n.:/\-\'\"‘’“”,!@#$%^&*()_+=~`{}|;<>?]', ' ', line)
                                    first = first.replace("“", "\"")
                                    first = first.replace("”", "\"")
                                    first = first.replace("’", "\'")
                                    first = first.replace("‘", "\'")
                                else:
                                    line = re.sub('[^a-zA-Z0-9\n.:/\-\'\",‘’“”!@#$%^&*()_+=~`{}|;<>?]', ' ', line)
                                    line = line.replace("“", "\"")
                                    line = line.replace("”", "\"")
                                    line = line.replace("’", "\'")
                                    line = line.replace("‘", "\'")
                                    line = line.replace('\n', '')
                                    new.write(line)
                    new.close()

                    tmp = first.split(' ')

                    count = 0
                    for i in tmp:
                        count+=1
                        if(i == 'JAN.'):
                            month = 1
                            break
                        if(i == 'FEB.'):
                            month = 2
                            break
                        if (i == 'MARCH'):
                            month = 3
                            break
                        if (i == 'APRIL'):
                            month = 4
                            break
                        if (i == 'MAY'):
                            month = 5
                            break
                        if (i == 'JUNE'):
                            month = 6
                            break
                        if (i == 'JULY'):
                            month = 7
                            break
                        if (i == 'AUG.'):
                            month = 8
                            break
                        if (i == 'SEPT.'):
                            month = 9
                            break
                        if (i == 'OCT.'):
                            month = 10
                            break
                        if (i == 'NOV.'):
                            month = 11
                            break
                        if (i == 'DEC.'):
                            month = 12
                            break
                    day = tmp[count].replace(',','')
                    year = tmp[count+1].replace('\n','')
                    content =[]
                    content.append("NYW"+str(n))
                    content.append(str(month) + '/' + day +'/' + year)

                    newFileName = re.sub('[^a-zA-Z0-9\n.:/\-\'\"‘’“”,!@#$%^&*()_+=~`{}|;<>?]', ' ', filename)
                    newFileName = newFileName.replace("“", "\"")
                    newFileName = newFileName.replace("”", "\"")
                    newFileName = newFileName.replace("’", "\'")
                    newFileName = newFileName.replace("‘", "\'")
                    content.append(newFileName.replace('text.txt', ''))

                    senNum = 0;
                    with open('new.txt', 'r', encoding="utf-8") as new2:
                        data = new2.read()
                        sentences = tokenizer.tokenize(data)
                        sen = ''
                        number = len(sentences)

                        i = 0
                        while i < len(sentences):
                            reset = 0
                            words = sentences[i].split()
                            j = 0
                            while j < len(words) - 1:
                                 if(words[j][0].islower() and words[j][-1] == '.' and words[j+1][0].isupper()):
                                     words[j]+='/#/'
                                     reset = 1
                                 j+=1

                            if(reset == 1):
                                newSen = ' '.join(words)
                                sentences[i] = newSen
                            flag = 0

                            print(sentences[i])
                            if i < number - 1:
                                if sentences[i + 1][0].islower():
                                    sen += sentences[i]
                                    sen += ' '
                                    flag = 1
                                elif(sentences[i][-2] == 'r' and sentences[i][-3] == 'M'):
                                    sen += sentences[i]
                                    sen += ' '
                                    flag = 1
                                else:
                                    sen += sentences[i]
                            else:
                                sen += sentences[i]
                            if i != number - 1 and flag == 0:
                                sen += "/#/"
                                senNum += 1
                            i += 1

                        if senNum != 0:
                            senNum += 1

                    content.append(senNum)
                    content.append(sen)

                    imgURL = ''
                    photoID = ''

                    prevURL = ""
                    dup = 0
                    for name in os.listdir(directory):
                        if name == filename.replace('text.txt','picture.txt'):
                            path = directory + '\\' + name
                            name = filename.replace('text.txt', 'caption.txt')
                            captionPath = directory + '\\' + name

                            with open(path, 'r', encoding='utf-8', errors='ignore') as picFile:
                                i = 0
                                for line in picFile:
                                    if(prevURL != line):
                                        i+=1
                                    prevURL = line
                            with open(path, 'r', encoding='utf-8', errors='ignore') as picFile:
                                a = 0
                                prevURL = ""
                                j = 0
                                for line in picFile:
                                    a+=1
                                    content2= []
                                    content2.append("NYW" + str(m))
                                    content2.append("NYW" + str(n))
                                    content2.append(line)

                                    if (prevURL == line):
                                        dup = 1
                                    prevURL = line

                                    if(dup == 0):
                                        j+=1
                                        photoID += "NYW" + str(m)
                                        k=0
                                        with open(captionPath, 'r') as capFile:
                                            for line2 in capFile:
                                                k += 1
                                                if k == a:
                                                    newFileCaption = re.sub('[^a-zA-Z0-9\n.:/\-\'\"‘’“”,!@#$%^&*()_+=~`{}|;<>?]', ' ', line2)
                                                    newFileCaption = newFileCaption.replace("“", "\"")
                                                    newFileCaption = newFileCaption.replace("”", "\"")
                                                    newFileCaption = newFileCaption.replace("’", "\'")
                                                    newFileCaption = newFileCaption.replace("‘", "\'")
                                                    content2.append(newFileCaption)
                                        writer = csv.writer(IDcsv, quoting=csv.QUOTE_ALL)
                                        writer.writerow(content2)
                                        imgURL += line
                                        if(j != i):
                                            imgURL +='/#/'
                                            photoID += '/#/'
                                    m+=1
                                    dup = 0

                    content.append(photoID)
                    content.append(imgURL)
                    if(imgURL != ''):
                        writer = csv.writer(mycsv, quoting=csv.QUOTE_ALL)
                        writer.writerow(content)
                        n+=1

                except Exception as e:
                    print(str(e))

