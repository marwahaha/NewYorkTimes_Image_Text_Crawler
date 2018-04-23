from bs4 import BeautifulSoup
from urllib.request import *
from http.cookiejar import CookieJar
import re
from general import *


#This file crawl image captions from the NY Times website ACCORDING to urls in text files.

cj = CookieJar()
opener = build_opener(HTTPCookieProcessor(cj))

#Put in the path of directory containing all the txt files (crawled data)
directory = 'C:\\Users\\hyzha\\PycharmProjects\\NY Times World\\Test'

for filename in os.listdir(directory):
    filepath = directory + '\\' + filename
    if 'text.txt' in filepath:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            url = f.readlines()[-1]
            try:
                p = opener.open(url)
                soup = BeautifulSoup(p, 'html.parser')
                title = soup.find('h1').text
                title = title.replace('?', '').replace(':', '')
                # create file
                file = title + ' caption.txt'
                file = directory + "\\" + file
                with open(file, 'w') as c:
                    key = re.compile('src="(.*?)"')
                    key2 = re.compile('caption="(.*?)"')
                    item = soup.find_all('div', {'class': 'image'})
                    for i in item:
                        image = re.findall(key, str(i))
                        for j in image:
                            if 'superJumbo' in j:
                                caption = re.findall(key2, str(i))
                                if not caption:
                                    c.write("\n")
                                else:
                                    for k in caption:
                                        flag = 1
                                        words = k.split()
                                        if len(words) <= 3:
                                            flag = 0
                                            a = 0
                                            while a < len(words):
                                                if(words[a][0].islower()):
                                                    flag = 1
                                                a+=1

                                        if flag == 1:
                                            c.write(k + '\n')
                                        else:
                                            c.write('\n')
            except Exception as e:
                print(str(e))
