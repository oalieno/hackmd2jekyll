# -*- coding: utf-8 -*-

import os
import time
import sched
import requests
import subprocess

from log import Log
from config import links_hash, upload_script, time_gap

class MyException(Exception):
    pass

class Server:
    """
    Crawl the target list from https://hackmd.io/{links_hash}/download
    Crawl through all the targets
        If no change:
            just skip it
        Otherwise:
            Save the page to ../_post/
    If any page changed:
        git push to heroku
    """
    def __init__(self):
        self.log = Log("info")
        self.links_hash = links_hash
        self.upload_script = upload_script 
        self.hackmd = "https://hackmd.io/{}/download"
        self.s = sched.scheduler(time.time, time.sleep)

    @staticmethod
    def extract_targets(page):
        """
        @type      page: str
        @parameter page: the page crawled down
        @rtype:  list      
        @return: target list
        """
        return page.strip().split('\n')

    @staticmethod
    def extract_header(page):
        """
        @type      page: str
        @parameter page: the page crawled down
        @rtype:  dict
        @return: page header
        """
        header = {}
        # missing page header
        if len(page.split('---\n')) < 3:
            raise MyException("missing page header, please fix it")
        headers = page.split('---\n')[1].strip().split('\n')
        for line in headers:
            row = line.split(':')
            header[row[0]] = row[1].strip()
        # date and title are used for filename, must be set 
        if not header.get("date") or not header.get("title"):
            raise MyException("date or title not set in header, please fix it")
        # check date format
        date = header["date"]
        if not ( len(date) == 10 and date[4] == date[7] == '-' and date.replace('-','').isdigit() ):
            raise MyException("date format incorrect, please fix it")
        # some custom attribute
        header.setdefault("layout", "post")
        return header    

    @staticmethod
    def extract_content(page):
        """
        @type      page: str
        @parameter page: the page crawled down
        @rtype:  str
        @return: page content
        """
        return page.split('---\n')[-1]

    @staticmethod
    def combine(header, content):
        """
        @type      page: str
        @parameter page: the page crawled down
        @rtype:  str
        @return: processed page 
        """
        return "---\n{}\n---\n{}".format("\n".join(["{}: {}".format(key,value) for key,value in header.iteritems()]),content)

    def update(self):
        self.log.info("check for update...")
        self.s.enter(time_gap, 0, self.update, ())
        try:
            # Crawl the target list
            page = requests.get(self.hackmd.format(self.links_hash)).text.encode('utf-8')
            targets = self.extract_targets(page)
            change = False
            try:
                # Crawl all targets
                for target in targets:
                    self.log.info("checking {}".format(self.hackmd.format(target)))
                    
                    page = requests.get(self.hackmd.format(target)).text.encode('utf-8')
                    header = self.extract_header(page)
                    content = self.extract_content(page)
                    page = self.combine(header,content)
                    
                    filename = "../_posts/{}-{}.md".format(header["date"],header["title"])
                    # check whether file has changed
                    if os.path.isfile(filename):
                        with open(filename, 'r') as data:
                            file_content = data.read()
                            if file_content == page: continue 
                    # save file        
                    self.log.info("{} has new content".format(filename[10:]))
                    change = True        
                    with open(filename, 'w') as data:
                        data.write(page)
            except requests.exceptions.ConnectionError:
                self.log.warning("can't get the page, please check your network status")
            if change:
               subprocess.call(["bash",self.upload_script])
        except requests.exceptions.ConnectionError:
            self.log.error("can't get the target list, please check whether the links_hash in config.py have been set correctly")
        except MyException as e:
            self.log.warning(str(e))
        except:
            self.log.error("some unknown error happened in Server.update main block, please contact the developers")
    def run(self):
        self.s.enter(1, 0, self.update, ())
        self.s.run()
        
S = Server()
S.run()
