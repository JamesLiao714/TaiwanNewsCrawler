"""
@author: 廖品捷
@Create Date: 2022/1/25
"""
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


def MultiThread_Crawl(url, headers):
    try:
        return requests.get(url, headers = headers)
    except:
        pass

def company_map(name):
    map = {'ltn':'自由時報','udn':'聯合報','chinatimes' : '中國時報'}
    return map[name]