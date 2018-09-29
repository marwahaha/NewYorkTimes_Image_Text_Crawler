import urllib.request
import os

directory = 'C:\\Users\\hyzha\\PycharmProjects\\NY Times World\\tmp'
for filename in os.listdir(directory):
    print (filename)
    filepath = directory + '\\' + filename
    if 'picture.txt' in filepath:
        with open(filepath, 'rt') as f:
            i = 0
            for line in f:
                i += 1
                line.replace('\n','')
                urllib.request.urlretrieve(line, 'tmp\\' + filename.replace('.txt',str(i) +'.jpg'))