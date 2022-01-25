"""
@author: 廖品捷
@Create Date: 2022/1/25
"""
from pathlib import Path
from pickle import FALSE
import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
import re
from datetime import datetime
import os
import threading
import ssl
import scrapy
from tqdm import tqdm
import re
import os
import requests
import urllib
from urllib.parse import urlparse, parse_qs, urlunparse
import time
from utils import company_map, MultiThread_Crawl
from pathlib import Path

# china times crwler
class chinatimes_crawler:
    def __init__(self):
        self.company = 'chinatimes'
        print('Crawler for news company: {}'.format(company_map(self.company)))
        self.headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
        }
        self.save_path = './search_result/'
        
    def GetLinks(self, response):
        links = []
        soup = BeautifulSoup(response.text, features="lxml")
        for i in soup.find_all('h3'):
            #print(i)
            url = i.find('a')['href']
            links.append(url)
        return links
    
    def GetNews(self, response):
        soup = BeautifulSoup(response.text, features="lxml")
        url = soup.find('link')['href']
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

        responses = [MultiThread_Crawl(link, self.headers) for link in links]

        # 整理成DataFrame
        list_of_dataframes = []
        for response in responses:
            try:
                ndf = self.GetNews(response)
                list_of_dataframes.append(ndf)
            except:
                pass
        df = pd.concat(list_of_dataframes, ignore_index=True)
        print('There are {} News in DataFrame.'.format(len(df)))
        if CSV:
            p = self.save_path + self.company + "_"+ keywords+'_' + str(pages)+'.csv'
            print('SAVING RESULT AT ' +  p)
            df.to_csv(p, index=False)
        return df

class ltn_crawler:
    def __init__(self):
        self.company = 'ltn'
        print('Crawler for news company: {}'.format(company_map(self.company)))
        self.headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
        }
        
    def GetLinks(self, response):
        links = []
        soup = BeautifulSoup(response.text, features="lxml")
        for i in soup.find_all("div", {"class": "cont"}):
            #print(i)
            url = i['href']
            links.append(url)
        return links
    
    def GetNews(self,response):
        soup = BeautifulSoup(response.text, features="lxml")
        url = soup.find('link')['href']
        ndf = pd.DataFrame(data = [{'TITLE':soup.find('h1').text,
                                    'TIME':datetime.strptime(soup.find('meta', attrs={'property':'article:published_time'})['content'],'%Y-%m-%dT%H:%M:%S+08:00'),
                                    'CATEGORY':soup.find('meta',attrs={'property':'article:section'})['content'],
                                    'DESCRIPTION':soup.find('meta',attrs={'name':'description'})['content'],
                                    'CONTENT':'\n'.join(i.text for i in soup.find('div',attrs={'class':'text boxTitle boxText'}).find_all('p')),
                                    'KEYWORDS':soup.find('meta',{'name':'keywords'})['content'],
                                    'FROM':soup.find('meta',{'name':'author'})['content'],
                                    'LINK':soup.find('meta', {'property':'og:url'})['content']}],
                           columns = ['TITLE', 'TIME', 'CATEGORY', 'DESCRIPTION', 'CONTENT','KEYWORDS', 'FROM', 'LINK']) 
        return ndf
    
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

        responses = [MultiThread_Crawl(link, self.headers) for link in links]

        # 整理成DataFrame
        list_of_dataframes = []
        for response in responses:
            try:
                ndf = self.GetNews(response)
                list_of_dataframes.append(ndf)
            except:
                pass
        df = pd.concat(list_of_dataframes, ignore_index=True)
        print('There are {} News in DataFrame.'.format(len(df)))
        if CSV:
            
            df.to_csv(index=False)
        return df


class udn_crawler:
    def __init__(self):
        self.company = 'udn'
        print('Crawler for news company: {}'.format(company_map(self.company)))
        self.headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
        }
        
    def GetLinks(self,response):
        links = []
        respond_dt = response.json()
        articles_ls = respond_dt['lists']
        for article in articles_ls:
            links.append(article['titleLink'])
        return links
    
    def GetNews(self, response):
        soup = BeautifulSoup(response.text, features="lxml")
        url = soup.find('link')['href']
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
    #https://udn.com/search/word/2/{}
   
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
        responses = [MultiThread_Crawl(link, self.headers) for link in links]
        # 整理成DataFrame
        list_of_dataframes = []
        for response in responses:
            try:
                ndf = self.GetNews(response)
                list_of_dataframes.append(ndf)
            except:
                pass
        df = pd.concat(list_of_dataframes, ignore_index=True)
        print('There are {} News in DataFrame.'.format(len(df)))
        if CSV:
            df.to_csv(index=False)
        return df
    