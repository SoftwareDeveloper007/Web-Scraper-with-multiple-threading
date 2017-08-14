from urllib import *
from urllib.parse import urlparse, urljoin
from urllib.request import urlopen
import urllib.request
import requests

class input_data():
    def __init__(self, url_txt_nm, config_nm, patterns_nm):
        self.url_txt_nm = url_txt_nm
        self.config_nm = config_nm
        self.patterns_nm = patterns_nm

    def input_parser(self):
        # 1. Import 'link_hunter.sample_input.txt'
        input = open(self.url_txt_nm, 'r')
        urls = input.read().split('\n')
        input.close()
        self.urls = []
        for url in urls:
            #print(url, urlparse(url).netloc)
            if url == '' or url == None:
                continue
            try:
                self.urls.append({
                    'url': url,
                    'domain': urlparse(url).netloc
                })
            except:
                print('Error url: ', url)

        # 2. Import 'link_hunter.config'
        input = open(self.config_nm, 'r')
        configs = input.read().split('\n')
        input.close()
        self.configs = {}
        for config in configs:

            if config == '' or config == None:
                continue
            try:
                config = config.split('\t')
                '''
                self.configs.append({
                    config[0]: config[1]
                })
                '''
                self.configs[config[0]] = config[1]

            except:
                print('Error config: ', config)

        # 3. Import 'link_hunter.patterns'
        input = open(self.patterns_nm, 'r')
        patterns = input.read().split('\n')
        input.close()
        self.patterns = []
        for pattern in patterns:
            if pattern == '':
                continue
            try:
                pattern = pattern.split('\t')
                self.patterns.append(pattern)
            except:
                print('Error format: ', pattern)
