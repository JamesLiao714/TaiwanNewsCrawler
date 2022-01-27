"""
@author: 廖品捷
@Create Date: 2022/1/25
"""
import requests
from datetime import datetime
import threading
from tqdm import tqdm
import requests


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