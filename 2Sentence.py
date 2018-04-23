import csv

#This file find possible incorrect sentences segmentation in old labeled csv file for further manually checking
csv.field_size_limit(1000000)

#put the path of the txt where you want to save incorrect labeled ID
with open('nyw.txt', 'w') as file:
    with open('nywdata(new).csv', 'r', newline='', encoding='utf-8') as mycsv:
        reader = csv.reader(mycsv)
        sen = []
        pic = []
        name = []
        for row in reader:
            name.append(row[0])
            sen.append(row[2])
            pic.append(row[1])

        c = 0
        for i in sen:
            i = i.split('/#/')
            sen[c] = i
            c += 1

        c = 0
        for i in sen:
            for j in i:
                words = j.split()
                m = 0
                reset = 0
                while m < len(words)-1 and reset == 0:
                    if ((words[m][0].islower() or words[m][0] != 'M' )and words[m][-1] == '.' and words[m+1][0].isupper()):
                        print(pic[c])
                        file.write(str(pic[c]) +'\n')
                        reset = 1
                    m+=1

            c+=1