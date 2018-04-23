from __future__ import division
from test_imgs import *
import os
import numpy as np
import matplotlib.pyplot as plt
import shutil


#ALL folder should be named as following, taking ceremony for example, "ceremony" for the folder with correct ceremony img, and "MISceremony" for the folder with incorrect img, NO SPACE in the folder name
#PUT IN THE IMAGE PATH and THE RESULT PATH WHERE YOU WANT TO SAVE THE RESULT

#Put the path of the folder here
path = "C:/Users/hyzha/Desktop/auto_category/"

#Put the path where you want to save the results folders
result_path = "C:/Users/hyzha/Desktop/result_new/"


dir = ['ceremony_txt', 'MISceremony_txt', 'conferencepress_txt', 'MISconferencepress_txt', 'protest_txt', 'MISprotest_txt', 'scenary_txt', 'MISscenary_txt',
       'singleperson_txt', 'MISsingleperson_txt', 'terrorism_txt', 'MISterrorism_txt', 'text_txt', 'MIStext_txt', 'military_txt', 'MISmilitary_txt']

path_txt = path + "txt/"
for i in dir:
    if not os.path.exists(path_txt + i):
        os.makedirs(path_txt + i)

category = ['ceremony', 'military', 'conferencepress', 'protest', 'scenary', 'singleperson', 'terrorism', 'text']
'''
for cat in category:
    for f in os.listdir(path + cat):
        with open(path_txt + cat + "_txt/"+ f.replace('.jpg', '.txt'), 'w') as file:
            result = get_img_cat_score(path + cat + '/'+ f)
            i = 0
            while i <= 6:
                file.write(str(result[0][i]) + ' ' + str(result[1][i]) + '\n')
                i+=1

    for f in os.listdir(path + "MIS" + cat):
        with open(path_txt + "MIS" + cat + "_txt/" + f.replace('.jpg', '.txt'), 'w') as file:
            result = get_img_cat_score(path + 'MIS' + cat + '/'+ f)
            i = 0
            while i <= 6:
                file.write(str(result[0][i]) + ' ' + str(result[1][i]) + '\n')
                i+=1
'''
path_threshold = path + 'threshold/'
for i in category:
    if not os.path.exists(path_threshold + i +'_threshold'):
        os.makedirs(path_threshold + i+'_threshold')
    if not os.path.exists(result_path + i +'_data'):
        os.makedirs(result_path + i+'_data')

for cat in category:
    print(cat)
    true_positive = 0
    false_positive = 0
    false_negative = 0
    true_negative = 0

    array = np.arange(0.00, 1.00, 0.01)
    a = 0
    while a < 100:
        i = array[a]
        true_positive = 0
        false_positive = 0
        false_negative = 0
        true_negative = 0
        for f in os.listdir(path_txt + cat + "_txt/"):
            with open(path_txt + cat + "_txt/" + f, 'r') as file:
                for line in file:
                    if cat == "singleperson":
                        if "single person" in line:
                            tmp = line.replace('single person ', '')
                            tmp = (float)(tmp.replace('\n',''))
                            if(tmp >= i):
                                true_positive += 1
                            else:
                                false_negative += 1
                    if cat == "conferencepress":
                        if "conference press" in line:
                            tmp = line.replace('conference press ', '')
                            tmp = (float)(tmp.replace('\n', ''))
                            if (tmp >= i):
                                true_positive += 1
                            else:
                                false_negative += 1
                    else:
                        if cat in line:
                            tmp = line.replace(cat + ' ', '')
                            tmp = (float)(tmp.replace('\n', ''))
                            if (tmp >= i):
                                true_positive += 1
                            else:
                                false_negative += 1
        for f in os.listdir(path_txt + "MIS" + cat + "_txt/"):
            with open(path_txt + "MIS" + cat + "_txt/" + f, 'r') as file:
                for line in file:
                    if cat == "singleperson":
                        if "single person" in line:
                            tmp = line.replace('single person ', '')
                            tmp = (float)(tmp.replace('\n', ''))
                            if (tmp >= i):
                                false_positive += 1
                            else:
                                true_negative += 1
                    if cat == "conferencepress":
                        if "conference press" in line:
                            tmp = line.replace('conference press ', '')
                            tmp = (float)(tmp.replace('\n', ''))
                            if (tmp >= i):
                                false_positive += 1
                            else:
                                true_negative += 1
                    else:
                        if cat in line:
                            tmp = line.replace(cat + ' ', '')
                            tmp = (float)(tmp.replace('\n', ''))
                            if (tmp >= i):
                                false_positive += 1
                            else:
                                true_negative += 1

        with open(path_threshold + cat + '_threshold/'+ str(i) + '.txt', 'w' ) as t:
            t.write(str(true_positive) + '\n')
            t.write(str(false_positive) + '\n')
            t.write(str(false_negative) + '\n')
            t.write(str(true_negative) + '\n')

        a+=1

    precision = []
    recall = []

    for f in os.listdir(path_threshold + cat + '_threshold/'):
        with open(path_threshold + cat + '_threshold/' + f, 'r') as t:
            i = 0
            for line in t:
                if(i == 0):
                    true_positive = int(line.replace('\n',''))
                if(i == 1):
                    false_positive = int(line.replace('\n',''))
                if (i == 2):
                    false_negative = int(line.replace('\n',''))
                if (i == 3):
                    true_negative = int(line.replace('\n',''))
                i+=1

            if(true_positive+false_positive != 0):
                p = (true_positive)/ (true_positive+false_positive)
            else:
                p = 1
            if(true_positive+false_negative != 0):
                r = (true_positive)/ (true_positive+false_negative)
            else:
                r = 1
            precision.append(p)
            recall.append(r)

    print(precision)
    print(recall)
    plt.scatter(recall, precision)
    plt.xlabel("recall")
    plt.ylabel("precision")
    plt.savefig(result_path + cat + "_data" + "/figure.jpg")
    plt.clf()
    with open(result_path + cat + "_data" + '/correct.txt', 'w') as data:
        for f in os.listdir(path_txt + cat + "_txt"):
            data.write(f.replace('.txt', '') + '\n')

    with open(result_path + cat + "_data" + '/incorrect.txt', 'w') as data:
        for f in os.listdir(path_txt + "MIS" + cat + "_txt/"):
            data.write(f.replace('.txt', '') + '\n')

    with open(result_path + cat + "_data" + '/threshold.txt', 'w') as data:
        for f in os.listdir(path_threshold + cat + "_threshold"):
            threshold = f.replace('.txt', '')
            with open(path_threshold + cat + "_threshold" + '/' + f, 'r') as file:
                data.write(f.replace('.txt', '') + ' ')
                for line in file:
                    data.write(line.replace('\n', '') + ' ')
                data.write('\n')


#delete unnecassary folder

#I didn't delete the folder with txt of img score since it takes too long to run for the next time

shutil.rmtree(path+'/threshold')
