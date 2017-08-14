from urllib import *
from urllib.parse import urlparse, urljoin
from urllib.request import urlopen
import urllib.request
import requests
from bs4 import BeautifulSoup
from module.common import download
import threading
import time

class crawling():
    def __init__(self, url, configs, patterns, db):
        self.start_urls = [url["url"]]
        self.start_urls_record = [url["url"]]
        self.domain = url["domain"]
        self.user_agent = configs['user_agent']
        self.delay = int(configs['scraping_delay_in_seconds'])
        self.max_urls = int(configs['max_URLs_per_domain'])
        self.configs = configs
        self.patterns = patterns
        self.failed_urls = []
        self.result = []
        self.db = db
        self.call_cnt = 0
        self.lookforNewUrls()

    def crawling_process(self):
        self.threads = []
        self.max_threads = 5
        while self.threads or (self.call_cnt < self.max_urls and self.start_urls):
            for thread in self.threads:
                if not thread.is_alive():
                    self.threads.remove(thread)

            while len(self.threads) < self.max_threads and (self.call_cnt < self.max_urls and self.start_urls):
                thread = threading.Thread(target=self.lookforNewUrls)
                thread.setDaemon(True)
                thread.start()
                self.threads.append(thread)

            time.sleep(self.delay)

        print('All done sucessfully: ', len(self.start_urls_record))

    def lookforNewUrls(self):
        start_url = self.start_urls.pop()
        self.html = download(start_url, self.user_agent)
        if self.html is not None:
            soup = BeautifulSoup(self.html, 'html.parser')
            links = soup.find_all('a')

            for link in links:
                try:
                    new_link = link.attrs['href']
                    if 'http' not in new_link:
                        new_link = 'http://' + self.domain + new_link

                    if self.domain in new_link and new_link not in self.start_urls_record\
                            and 'pdf' not in new_link and 'doc' not in new_link and 'ppt' not in new_link:
                        self.start_urls.append(new_link)
                        self.start_urls_record.append(new_link)
                        self.call_cnt += 1

                except:
                    pass

            text = soup.text.lower()
            words = text.split(' ')

            temp_result = {}

            for pattern in self.patterns:
                temp_result[pattern[2]] = 0
            for word in words:
                for pattern in self.patterns:
                    if calibrate_word(word) in pattern[2].lower().split('|'):
                        temp_result[pattern[2]] += 1

            self.result.append([
                start_url,
                self.domain,
                temp_result[self.patterns[0][2]],
                temp_result[self.patterns[1][2]],
                temp_result[self.patterns[2][2]],
                temp_result[self.patterns[3][2]],
            ])

        else:
            return


def calibrate_word(word):
    stop_words = ['\n', '\t', '(', ')', '[', ']', ',', '.', ':', ';', '?', '%', '/', '@', '-', '"']
    for stop_word in stop_words:
        while stop_word in word:
            word = word.replace(stop_word, "")
    return word

