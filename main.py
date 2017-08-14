import threading
import time
import pymysql

from module.crawling import *
from module.input_processing import *
from module.save_db import *

class main_ctrler():
    def __init__(self):
        self.input = input_data("config/link_hunter.sample_input.txt", "config/link_hunter.config",
                       "config/link_hunter.patterns")
        self.input.input_parser()
        self.input.urls.reverse()
        self.urls = self.input.urls
        '''
        self.urls = queue.Queue()
        for url in self.input.urls:
            self.urls.put_nowait(url)
        '''
        self.configs = self.input.configs
        self.patterns = self.input.patterns

        self.total_result = []
        self.db = save_db(self.configs, self.patterns)
        self.db.remove_table()
        self.db.create_table()

    def one_url_processor(self):
        #url = self.urls.get()
        url = self.urls.pop()
        crawler = crawling(url, self.configs, self.patterns, self.db)
        crawler.crawling_process()

        print('==================================================')
        self.total_result.extend(crawler.result)


    def total_urls_processor(self):
        self.threads = []
        self.max_threads = 1000

        while self.threads or self.urls:
            for thread in self.threads:
                if not thread.is_alive():
                    self.threads.remove(thread)

            while len(self.threads) < self.max_threads and self.urls:
                thread = threading.Thread(target=self.one_url_processor)
                thread.setDaemon(True)
                thread.start()
                self.threads.append(thread)
        for element in self.total_result:
            self.db.store_data(element[0], element[1], element[2], element[3], element[4], element[5])
        self.db.db_close()



if __name__ == '__main__':
    start_time = time.time()
    app = main_ctrler()
    app.total_urls_processor()

    elapsed_time = time.time() - start_time
    print(elapsed_time)
