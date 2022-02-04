"""
@author: 廖品捷
@Create Date: 2022/1/25
"""
from http.client import MULTI_STATUS
from pathlib import Path
from tracemalloc import start
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import threading
from tqdm import tqdm
import requests
import time
import sys
import urllib3
urllib3.disable_warnings()
#from utils import company_map, MultiThread_Crawl

def MultiThread(links, func):
    try:
        pipeline = []
        for url in links:
            pipeline.append(threading.Thread(target = func, args = (url,))) 
        for thread in pipeline:
            thread.start()
        for thread in pipeline:
            thread.join()
    except:
        print('Errors occur, unable to connect URL links')
        pass

def singleThread(url, headers):
    try:
        return requests.get(url, headers = headers)
    except:
        pass



def company_map(name):
    map = {'ltn':'自由時報','udn':'聯合報','chinatimes' : '中國時報'}
    return map[name]

# 中國時報新聞 crawler
class chinatimes_crawler():
    def __init__(self):
        self.company = 'chinatimes'
        print('Crawler for news company: {}'.format(company_map(self.company)))
        self.headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
        }
        self.save_path = './search_result/'
        self.responses = []
        self.start = time.time()
        self.end = time.time()
        self.MT = True

    def getResponse(self, url):
        self.responses.append(requests.get(url, headers = self.headers, verify=False))

    def GetLinks(self, response):
        links = []
        soup = BeautifulSoup(response.text, features="lxml")
        for i in soup.find_all('h3'):

            url = i.find('a')['href']
            links.append(url)
        return links
    
    def GetNews(self, response):
        soup = BeautifulSoup(response.text, features="lxml")
        #url = soup.find('link')['href']
        
        ndf = pd.DataFrame(data = [{'TITLE':soup.find('h1', attrs={'class':'article-title'}).text,
                                    'TIME':datetime.strptime(soup.find('meta', attrs={'property':'article:published_time'})['content'],'%Y-%m-%dT%H:%M:%S+08:00'),
                                    'CATEGORY':soup.find('meta',attrs={'property':'article:section'})['content'],
                                    'DESCRIPTION':soup.find('meta',attrs={'name':'description'})['content'],
                                    'CONTENT':'\n'.join(i.text for i in soup.find('div',attrs={'class':'article-body'}).find_all('p')),
                                    'KEYWORDS':soup.find('meta',{'name':'keywords'})['content'],
                                    'FROM':soup.find('meta',{'name':'publisher'})['content'],
                                    'LINK':soup.find('meta', {'property':'og:url'})['content']}],
                        columns = ['TITLE', 'TIME', 'CATEGORY', 'DESCRIPTION', 'CONTENT','KEYWORDS', 'FROM', 'LINK']) 
        return ndf

    
    def search(self, keywords, pages, CSV = False):
        # crawling
        links = []
        prev = 0
        
        for i in range(pages):
            url = 'https://www.chinatimes.com/search/{}?page={}'.format(keywords, i+1)
            resp = requests.get(url)
            links += self.GetLinks(resp)
            links = list(set(links))  
            page_n = len(links)
            print('There are {} links in page {} | total {}'.format(page_n - prev,str(i + 1), page_n))
            prev = page_n
        # 多線程爬蟲

        #self.responses = [requests.get(link, self.headers) for link in tqdm(links)]
        print('PARSING DATA & LOADING NEWS CONTENT')
        print('SUPPORT MULTI THREAD, BUT IT MAY LOSE SOME NEWS')

        if not self.MT:
            self.responses = [singleThread(link, self.headers) for link in tqdm(links)]
        else:
            MultiThread(links, self.getResponse)

        # 整理成DataFrame
        list_of_dataframes = []
        for response in tqdm(self.responses):
            try:
                ndf = self.GetNews(response)
                list_of_dataframes.append(ndf)
            except:
                
                pass
        self.end = time.time()
        print('Total time cost: {0:.2f} seconds'.format(self.end - self.start))
        df = pd.concat(list_of_dataframes, ignore_index=True)
        print('There are {} News in DataFrame.'.format(len(df)))
        if CSV:
            p = self.save_path + self.company + "_"+ keywords+'_' + str(pages)+'.csv'
            filepath = Path(p)  
            filepath.parent.mkdir(parents=True, exist_ok=True) 
            print('SAVING RESULT AT ' +  p)
            df.to_csv(filepath, encoding = 'utf_8_sig', index=False)
        return df


# 自由時報新聞
class ltn_crawler:
    def __init__(self):
        self.company = 'ltn'
        print('Crawler for news company: {}'.format(company_map(self.company)))
        self.headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
        }
        self.save_path = './search_result/'
        self.responses = []
        self.start = time.time()
        self.end = time.time()
        self.MT = True

    def getResponse(self, url):
        self.responses.append(requests.get(url, headers = self.headers, verify=False))

    def GetLinks(self, response):
        links = []
        soup = BeautifulSoup(response.text, features="lxml")
        for i in soup.find_all("div", {"class": "cont"}):
            url = i['href']
            links.append(url)
        return links
    
    def GetNews(self,response):
        soup = BeautifulSoup(response.text, features="lxml")
        ndf = pd.DataFrame(data = [{'TITLE':soup.find('meta',attrs={'property':'og:title'})['content'],
                                    'TIME':datetime.strptime(soup.find('meta', attrs={'property':'article:published_time'})['content'],'%Y-%m-%dT%H:%M:%S+08:00'),
                                    'CATEGORY':soup.find('meta',attrs={'property':'article:section'})['content'],
                                    'DESCRIPTION':soup.find('meta',attrs={'name':'description'})['content'],
                                    'CONTENT':'\n'.join(i.text for i in soup.find('div',attrs={'class':'text boxTitle boxText'}).find_all('p')),
                                    'KEYWORDS':soup.find('meta',{'name':'keywords'})['content'],
                                    'FROM':soup.find('meta',{'name':'author'})['content'],
                                    'LINK':soup.find('meta', {'property':'og:url'})['content']}],
                           columns = ['TITLE', 'TIME', 'CATEGORY', 'DESCRIPTION', 'CONTENT','KEYWORDS', 'FROM', 'LINK']) 
        return ndf
    '''
    def search_dt(self,keyword, dt_beg, dt_end, CSV = False):
        
        links = []
        i = 0
        page_n = 0
        while 1:
            try:
                url = 'https://search.ltn.com.tw/list?keyword={}&start_time={}&end_time={}&page={}'.format(keyword, dt_beg, dt_end, i)
                resp = requests.get(url)
                links += self.GetLinks(resp)
                links = list(set(links)) 
                print(len(links), page_n)
                if len(links) == page_n:
                    break 
                page_n = len(links)
                print('Current page: {} | News number: {} | Date : {} - {}'.format(i+1,page_n, dt_beg, dt_end))
                i+=1
            except:
                print(sys.exc_info()[0])
                break
        '''


    def search(self, keywords, pages, CSV =False):
        # crawling
        # https://search.ltn.com.tw/list?keyword=covid&start_time=20041201&end_time=20220125&sort=date&type=all&page=2
        links = []
        prev = 0
        for i in range(pages):
            url = 'https://search.ltn.com.tw/list?keyword={}&page={}'.format(keywords, i+1)
            resp = requests.get(url)
            links += self.GetLinks(resp)
            links = list(set(links))  
            page_n = len(links)
            print('There are {} links in page {} | total {}'.format(page_n - prev,str(i + 1), page_n))
            prev = page_n

        # 多線程爬蟲
        print('PARSING DATA & LOADING NEWS CONTENT')
        if not self.MT:
            self.responses = [singleThread(link, self.headers) for link in tqdm(links)]
        else:
            print('SUPPORT MULTI THREAD')
            MultiThread(links, self.getResponse)


        # 整理成DataFrame
        list_of_dataframes = []
        for response in tqdm(self.responses):
            try:
                ndf = self.GetNews(response)
                list_of_dataframes.append(ndf)
            except:
                pass
        self.end = time.time()
        print('Total time cost: {0:.2f} seconds'.format(self.end - self.start))
        df = pd.concat(list_of_dataframes, ignore_index=True)
        print('There are {} News in DataFrame.'.format(len(df)))
        if CSV:
            p = self.save_path + self.company + "_"+ keywords+'_' + str(pages)+'.csv'
            filepath = Path(p)  
            filepath.parent.mkdir(parents=True, exist_ok=True) 
            print('SAVING RESULT AT ' +  p)
            df.to_csv(filepath, encoding = 'utf_8_sig', index=False)
        return df


class udn_crawler:
    def __init__(self):
        self.company = 'udn'
        print('Crawler for news company: {}'.format(company_map(self.company)))
        self.headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
        }
        self.save_path = './search_result/'
        self.responses = []
        self.start = time.time()
        self.end = time.time()

    def getResponse(self, url):

        self.responses.append(requests.get(url, headers = self.headers , verify=False))

    def GetLinks(self,response):
        links = []
        respond_dt = response.json()
        articles_ls = respond_dt['lists']
        for article in articles_ls:
            links.append(article['titleLink'])
        return links
    
    def GetNews(self, response):
        soup = BeautifulSoup(response.text, features="lxml")
        #url = soup.find('link')['href']
        ndf = pd.DataFrame(data = [{'TITLE':soup.find('h1', attrs ={"class":"article-content__title"}).text,
                                    'TIME':datetime.strptime(soup.find('time', attrs={'class':'article-content__time'}).text,'%Y-%m-%d %H:%M'),
                                    'CATEGORY':soup.find('meta',attrs={'property':'article:section'})['content'],
                                    'DESCRIPTION':soup.find('meta',attrs={'property':'og:description'})['content'],
                                    'CONTENT':'\n'.join(i.text for i in soup.find('section',attrs={'class':'article-content__editor'}).find_all('p')),
                                    'KEYWORDS':soup.find('meta',{'name':'news_keywords'})['content'],
                                    'FROM':soup.find('meta',{'name':'author'})['content'],
                                    'LINK':soup.find('meta', {'property':'og:url'})['content']}],
                           columns = ['TITLE', 'TIME', 'CATEGORY', 'DESCRIPTION', 'CONTENT','KEYWORDS', 'FROM', 'LINK']) 
        return ndf
   
    def search(self, keywords, pages, CSV = False):
        # crawling
        # https://udn.com/api/more?page=0&id=search:covid&channelId=2&type=searchword&last_page=28
        links = []
        prev = 0
        for i in range(pages):
            url = 'https://udn.com/api/more?page={}&id=search:{}&channelId=2&type=searchword&last_page={}'.format(i,keywords,pages)
            resp = requests.get(url)
            links += self.GetLinks(resp)
            links = list(set(links))  
            page_n = len(links)
            print('There are {} links in page {} | total {}'.format(page_n - prev,str(i), page_n))
            prev = page_n

        # 多線程爬蟲
        print('PARSING DATA & LOADING NEWS CONTENT')
        print('DO NOT SUPPORT MULTI THREAD')
        self.responses = [singleThread(link, self.headers) for link in tqdm(links)]
        # 整理成DataFrame
        list_of_dataframes = []
        for response in tqdm(self.responses):
            try:
                ndf = self.GetNews(response)
                list_of_dataframes.append(ndf)
            except:
                pass
        self.end = time.time()
        print('Total time cost: {0:.2f} seconds'.format(self.end - self.start))
        df = pd.concat(list_of_dataframes, ignore_index=True)
        print('There are {} News in DataFrame.'.format(len(df)))
        if CSV:
            p = self.save_path + self.company + "_"+ keywords+'_' + str(pages)+'.csv'
            filepath = Path(p)  
            filepath.parent.mkdir(parents=True, exist_ok=True) 
            print('SAVING RESULT AT ' +  p)
            df.to_csv(filepath, encoding = 'utf_8_sig', index=False)
        return df
    