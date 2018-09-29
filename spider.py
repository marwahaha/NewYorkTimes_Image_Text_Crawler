from urllib.request import *
from http.cookiejar import CookieJar
import urllib
from domain import *
from general import *
from bs4 import BeautifulSoup
import re
import time


class Spider:
    StopCount = 0
    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    queue = set()
    crawled = set()

    def __init__(self, project_name, base_url, domain_name):
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.queue_file = Spider.project_name + '/queue.txt'
        Spider.crawled_file = Spider.project_name + '/crawled.txt'
        self.boot()
        self.crawl_page('First spider', Spider.base_url)


    # Creates directory and files for project on first run and starts the spider
    @staticmethod
    def boot():
        create_project_dir(Spider.project_name)
        create_data_files(Spider.project_name, Spider.base_url)
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)

    # Updates user display, fills queue and updates files
    @staticmethod
    def crawl_page(thread_name, page_url):

        if page_url not in Spider.crawled:
            print(thread_name + ' now crawling ' + page_url)
            print('Queue ' + str(len(Spider.queue)) + ' | Crawled  ' + str(len(Spider.crawled)))
            Spider.add_links_to_queue(Spider.gather_links(page_url))

            tmpURL = get_sub_domain_name(page_url)
            results = tmpURL.split('/')
            try:
                # if there is number in url, then it is an article page
                if  (results[1] == '2017' and (results[2] == '08' or results[2] =='09' or results[2] == '10' or results[2] == '11' or results[2] == '12' )) or results[1] == '2018':
                    cj = CookieJar()
                    opener = build_opener(HTTPCookieProcessor(cj))
                    try:
                        p = opener.open(page_url)
                        soup = BeautifulSoup(p, 'html.parser')
                        title = soup.find('h1').text
                        title = title.replace('?', '').replace(':','')
                        #create file
                        file1 = title + ' text.txt'
                        file2 = title + ' picture.txt'

                        #getting paragraph
                        tmp = soup.find_all('p')
                        i = -1
                        for paragraph in tmp:
                            flag = 0
                            if paragraph.text != 'Advertisement' and paragraph.text != 'See More »' and paragraph.text != 'Go to Home Page »' and paragraph.text != "Please verify you're not a robot by clicking the box." and paragraph.text != "Invalid email address. Please re-enter." and paragraph.text != "You must select a newsletter to subscribe to." and paragraph.text != "View all New York Times newsletters." and paragraph.text != "We’re interested in your feedback on this page. Tell us what you think.":
                                i += 1
                                if i == 0:
                                    if 'JAN.' in paragraph.text:
                                        append_byte_file(Spider.project_name + "/" + file1,paragraph.text.replace('JAN.', ' JAN.').encode(errors="ignore"))
                                        flag = 1
                                    if 'FEB.' in paragraph.text:
                                        append_byte_file(Spider.project_name + "/" + file1,paragraph.text.replace('FEB.', ' FEB.').encode(errors="ignore"))
                                        flag = 1
                                    if 'MARCH' in paragraph.text:
                                        append_byte_file(Spider.project_name + "/" + file1,
                                                         paragraph.text.replace('MARCH', ' MARCH').encode(errors="ignore"))
                                        flag =1
                                    if 'APRIL' in paragraph.text:
                                        append_byte_file(Spider.project_name + "/" + file1,
                                                         paragraph.text.replace('APRIL', ' APRIL').encode(errors="ignore"))
                                        flag = 1
                                    if 'MAY' in paragraph.text:
                                        append_byte_file(Spider.project_name + "/" + file1,
                                                         paragraph.text.replace('MAY', ' MAY').encode(errors="ignore"))
                                        flag = 1
                                    if 'JUNE' in paragraph.text:
                                        append_byte_file(Spider.project_name + "/" + file1,
                                                         paragraph.text.replace('JUNE', ' JUNE').encode(errors="ignore"))
                                        flag = 1
                                    if 'JULY' in paragraph.text:
                                        append_byte_file(Spider.project_name + "/" + file1,
                                                         paragraph.text.replace('JULY', ' JULY').encode(errors="ignore"))
                                        flag = 1
                                    if 'AUG.' in paragraph.text:
                                        append_byte_file(Spider.project_name + "/" + file1,
                                                         paragraph.text.replace('AUG.', ' AUG.').encode(errors="ignore"))
                                        flag = 1
                                    if 'SEPT.' in paragraph.text:
                                        append_byte_file(Spider.project_name + "/" + file1,
                                                         paragraph.text.replace('SEPT.', ' SEPT.').encode(errors="ignore"))
                                        flag = 1
                                    if 'OCT.' in paragraph.text:
                                        append_byte_file(Spider.project_name + "/" + file1,
                                                         paragraph.text.replace('OCT.', ' OCT.').encode(errors="ignore"))
                                        flag = 1
                                    if 'NOV.' in paragraph.text:
                                        append_byte_file(Spider.project_name + "/" + file1,
                                                         paragraph.text.replace('NOV.', ' NOV.').encode(errors="ignore"))
                                        flag = 1
                                    if 'DEC.' in paragraph.text:
                                        append_byte_file(Spider.project_name + "/" + file1,
                                                         paragraph.text.replace('DEC.', ' DEC.').encode(errors="ignore"))
                                        flag = 1
                                if flag == 0:
                                    append_byte_file(Spider.project_name + "/" + file1, paragraph.text.encode(errors="ignore"))
                        append_byte_file(Spider.project_name + "/" + file1, page_url.encode(errors="ignore"))
                        # getting picture related to article
                        key = re.compile('src="(.*?)"')
                        image = re.findall(key, str(soup.find_all('div', {'class': 'image'})))
                        write_file(Spider.project_name + "/" + file2, '')
                        for url in image:
                            if 'superJumbo' in url:
                                append_byte_file(Spider.project_name + "/" + file2, url.encode(errors="ignore"))
                    except Exception as e:
                        print(str(e))
                Spider.queue.remove(page_url)
                Spider.crawled.add(page_url)
                Spider.update_files()
            except Exception as e:
                print(str(e))

    # Converts raw response data into readable information and checks for proper html formatting
    @staticmethod
    def gather_links(page_url):
        html_string = ''
        try:
            cj = CookieJar()
            opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
            response = opener.open(page_url)
            soup = BeautifulSoup(response, 'html.parser')
            tmp = soup.find_all('a', href=True)
            links = set()
            for i in tmp:
                if 'http' in i['href']:
                    tmpURL = i['href']
                    tmpURL = 'http://' + get_sub_domain_name(tmpURL)
                    links.add(tmpURL)
        except Exception as e:
            print(str(e))
            return set()
        return links

    # Saves queue data to project files
    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            if (url in Spider.queue) or (url in Spider.crawled):
                continue
            if Spider.domain_name != get_domain_name(url):
                continue
            Spider.queue.add(url)

    @staticmethod
    def update_files():
        set_to_file(Spider.queue, Spider.queue_file)
        set_to_file(Spider.crawled, Spider.crawled_file)
        Spider.StopCount += 1

        if Spider.StopCount == 100:
            print("You can stop your program now")
            Spider.StopCount = 0
            time.sleep(5)

